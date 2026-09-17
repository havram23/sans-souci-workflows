"""Explicit status delivery with retries and an optional token-free disk queue."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import uuid


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def payload_for(status="heartbeat", event_id=None, code="", occurred_at=None):
    if status not in {"heartbeat", "success", "failure"} or not isinstance(code, str) or not re.fullmatch(r"[A-Z0-9_-]{0,40}", code):
        raise ValueError("Status oder Ereigniscode ungültig.")
    try:
        identifier = str(uuid.UUID(event_id)) if event_id else str(uuid.uuid4())
        stamp = datetime.fromisoformat(occurred_at.replace("Z", "+00:00")) if occurred_at else datetime.now(timezone.utc)
        if stamp.tzinfo is None:
            raise ValueError()
    except (ValueError, AttributeError, TypeError):
        raise ValueError("Ereignis-ID oder Zeitstempel ungültig.") from None
    return {"event_id": identifier, "status": status, "occurred_at": stamp.astimezone(timezone.utc).isoformat(), "code": code}


def send_event(url, token, status="heartbeat", event_id=None, code="", attempts=3, opener=None, sleep=time.sleep, occurred_at=None):
    try:
        parsed = urlsplit(url)
        _ = parsed.port
        if not parsed.hostname or (parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"})):
            raise ValueError()
        if parsed.username is not None or parsed.password is not None or parsed.query or parsed.fragment or not re.fullmatch(r"/ingest/[A-Za-z0-9_-]{3,80}", parsed.path):
            raise ValueError()
    except ValueError:
        raise ValueError("Direkte HTTPS-Ereignis-URL erforderlich; HTTP nur für Loopback-Tests.") from None
    if not re.fullmatch(r"wm_[A-Za-z0-9_-]{12,200}", token):
        raise ValueError("Ereignisschlüssel fehlt oder hat falsches Format.")
    if type(attempts) is not int or not 1 <= attempts <= 3:
        raise ValueError("Zwischen einem und drei Zustellversuchen erlaubt.")
    payload = payload_for(status, event_id, code, occurred_at)
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    client = opener or build_opener(NoRedirect)
    for attempt in range(attempts):
        request = Request(url, data=body, headers={"Content-Type":"application/json", "Authorization":"Bearer " + token}, method="POST")
        try:
            with client.open(request, timeout=10) as response:
                raw = response.read(16_385)
            if len(raw) > 16_384:
                raise RuntimeError("Unerwartet große Empfangsbestätigung.")
            result = json.loads(raw)
            if not isinstance(result, dict) or result.get("accepted") is not True:
                raise RuntimeError("Server hat den Empfang nicht bestätigt.")
            return {key: result[key] for key in ("accepted", "duplicate", "received_at") if key in result}
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == attempts - 1:
                raise RuntimeError(f"Ereignis nicht angenommen (HTTP {exc.code}).") from None
        except (URLError, TimeoutError, ConnectionError):
            if attempt == attempts - 1:
                raise RuntimeError("Ereignisempfang nicht bestätigt. Verbindung prüfen.") from None
        except (json.JSONDecodeError, UnicodeError):
            raise RuntimeError("Ungültige Empfangsbestätigung.") from None
        sleep(2 ** attempt)
    raise RuntimeError("Kein Zustellversuch ausgeführt.")


def queue_event(folder: Path, status="heartbeat", event_id=None, code="", occurred_at=None) -> str:
    if folder.is_symlink():
        raise ValueError("Queue-Verzeichnis darf kein symbolischer Link sein.")
    folder.mkdir(parents=True, exist_ok=True)
    if sum(1 for _ in folder.glob("*.json")) >= 1000:
        raise ValueError("Queue enthält bereits 1.000 Ereignisse. Bestand prüfen.")
    payload = payload_for(status, event_id, code, occurred_at)
    target = folder / (payload["event_id"] + ".json")
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(payload, stream, separators=(",", ":"))
        stream.flush()
        os.fsync(stream.fileno())
    return payload["event_id"]


def flush_queue(folder: Path, url: str, token: str, max_events=10, sender=send_event) -> dict:
    if folder.is_symlink() or not folder.is_dir() or type(max_events) is not int or not 1 <= max_events <= 100:
        raise ValueError("Reguläres Queue-Verzeichnis und Grenze zwischen 1 und 100 erforderlich.")
    sent, failed = 0, 0
    for path in sorted(folder.glob("*.json"))[:max_events]:
        try:
            if path.is_symlink():
                raise ValueError()
            with path.open("rb") as stream:
                raw = stream.read(4097)
            if len(raw) > 4096:
                raise ValueError()
            payload = json.loads(raw)
            if not isinstance(payload, dict) or set(payload) != {"event_id", "status", "occurred_at", "code"}:
                raise ValueError()
            checked = payload_for(**payload)
            if path.stem != checked["event_id"]:
                raise ValueError()
            result = sender(url, token, **checked)
            if result.get("accepted") is not True:
                raise RuntimeError()
            # Only remove this exact acknowledged payload; concurrent changes remain queued.
            if path.is_symlink() or path.read_bytes() != raw:
                raise RuntimeError()
            path.unlink()
            sent += 1
        except (ValueError, OSError, RuntimeError, TypeError, KeyError):
            failed += 1
    return {"sent": sent, "failed": failed, "pending": sum(1 for _ in folder.glob("*.json"))}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("send", "enqueue", "flush"), default="send")
    parser.add_argument("--status", choices=("success", "failure", "heartbeat"), default="heartbeat")
    parser.add_argument("--event-id")
    parser.add_argument("--code", default="")
    parser.add_argument("--queue-dir", type=Path)
    parser.add_argument("--max-events", type=int, default=10)
    args = parser.parse_args(argv)
    try:
        if args.mode == "enqueue":
            if args.queue_dir is None: raise ValueError("--queue-dir ist erforderlich.")
            queue_event(args.queue_dir, args.status, args.event_id, args.code)
            result = {"queued": True}
        elif args.mode == "flush":
            if args.queue_dir is None: raise ValueError("--queue-dir ist erforderlich.")
            result = flush_queue(args.queue_dir, os.environ.get("PILOT_INGEST_URL", ""), os.environ.get("PILOT_INGEST_TOKEN", ""), args.max_events)
        else:
            result = send_event(os.environ.get("PILOT_INGEST_URL", ""), os.environ.get("PILOT_INGEST_TOKEN", ""), args.status, args.event_id, args.code)
        print(json.dumps(result))
        return 1 if result.get("failed") else 0
    except (ValueError, RuntimeError, OSError) as exc:
        print(json.dumps({"error": str(exc) if isinstance(exc, (ValueError, RuntimeError)) else "Lokale Queue konnte nicht verarbeitet werden."}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
