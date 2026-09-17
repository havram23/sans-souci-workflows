"""Bounded local transformations; never read credentials or contact services."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from uuid import NAMESPACE_URL, uuid5

MAX_INPUT_BYTES = 20 * 1024 * 1024
MAX_ROWS = 100_000
MAX_FIELD = 65_536
MAX_FILES = 10_000
MAX_FILE_BYTES = 256 * 1024 * 1024
csv.field_size_limit(MAX_FIELD)


class InputError(ValueError):
    """An input cannot be processed safely under the documented limits."""


def read_text(path: Path) -> str:
    with path.open("rb") as stream:
        data = stream.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise InputError("Eingabe größer als 20 MiB.")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputError("Eingabe muss UTF-8 sein.") from exc
    if "\x00" in text:
        raise InputError("NUL-Zeichen in Eingabe nicht erlaubt.")
    return text


def strict_json(text: str):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise InputError("Doppelte JSON-Feldnamen sind nicht erlaubt.")
            result[key] = value
        return result

    def invalid_constant(_):
        raise InputError("NaN und Infinity sind keine gültigen JSON-Werte.")

    try:
        return json.loads(text, object_pairs_hook=unique, parse_constant=invalid_constant)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise InputError("Ungültige oder zu tief verschachtelte JSON-Eingabe.") from exc


def read_csv(path: Path, delimiter: str = ",") -> tuple[list[str], list[dict[str, str]]]:
    try:
        reader = csv.reader(io.StringIO(read_text(path), newline=""), delimiter=delimiter, strict=True)
        columns = next(reader, None)
        if not columns or any(not value.strip() for value in columns):
            raise InputError("Eine CSV-Kopfzeile mit benannten Spalten ist erforderlich.")
        if len(set(columns)) != len(columns):
            raise InputError("CSV-Spaltennamen müssen eindeutig sein.")
        rows = []
        for index, values in enumerate(reader, 2):
            if len(values) != len(columns):
                raise InputError(f"CSV-Zeile {index}: Spaltenanzahl stimmt nicht.")
            rows.append(dict(zip(columns, values)))
            if len(rows) > MAX_ROWS:
                raise InputError("Höchstens 100.000 Datenzeilen erlaubt.")
        return columns, rows
    except csv.Error as exc:
        raise InputError("Ungültiges CSV-Format oder Feld größer als 64 KiB.") from exc


def require_fields(columns: list[str], fields: list[str]):
    if not fields or len(set(fields)) != len(fields) or any(field not in columns for field in fields):
        raise InputError("Gewünschte Felder müssen eindeutig sein und in der Eingabe vorkommen.")


def formula_risk(value: str) -> bool:
    return bool(value) and (value[0] in "\t\r\n" or value.lstrip().startswith(("=", "+", "-", "@")))


def safe_cell(value: str) -> str:
    return "'" + value if formula_risk(value) else value


def csv_output(columns: list[str], rows: list[dict[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\r\n")
    writer.writerow([safe_cell(column) for column in columns])
    for row in rows:
        writer.writerow([safe_cell(str(row.get(column, ""))) for column in columns])
    return stream.getvalue()


def json_output(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def write_new(path: Path, text: str):
    """Exclusive create: existing files, including symlinks, are never replaced."""
    try:
        with path.open("x", encoding="utf-8", newline="") as stream:
            stream.write(text)
    except FileExistsError as exc:
        raise InputError("Ausgabedatei existiert bereits. Bitte neuen Namen wählen.") from exc


def audit_csv(columns: list[str], rows: list[dict[str, str]]) -> dict:
    return {
        "rows": len(rows), "columns": len(columns),
        "fields": [{"name": field, "empty": sum(not row[field].strip() for row in rows),
                    "formula_like": sum(formula_risk(row[field]) for row in rows),
                    "max_length": max((len(row[field]) for row in rows), default=0)} for field in columns],
        "note": "Strukturprüfung; kein Nachweis fachlicher Richtigkeit oder Anonymität.",
    }


def dedupe(columns: list[str], rows: list[dict[str, str]], keys: list[str]) -> tuple[list[dict], dict]:
    require_fields(columns, keys)
    seen = set()
    output = []
    duplicate_rows = []
    for number, row in enumerate(rows, 2):
        key = tuple(row[field].strip().casefold() for field in keys)
        # Missing identifiers do not prove that two records represent the same entity.
        if all(key) and key in seen:
            duplicate_rows.append(number)
            continue
        if all(key):
            seen.add(key)
        output.append(row)
    return output, {"input_rows": len(rows), "kept_rows": len(output), "duplicate_row_numbers": duplicate_rows}


def map_csv(columns: list[str], rows: list[dict[str, str]], mapping: dict) -> tuple[list[str], list[dict]]:
    if not isinstance(mapping, dict) or not mapping or any(not isinstance(k, str) or not isinstance(v, str) or not v.strip() for k, v in mapping.items()):
        raise InputError("Mapping muss Quellspalten auf nichtleere Zielspalten abbilden.")
    require_fields(columns, list(mapping))
    if len(set(mapping.values())) != len(mapping):
        raise InputError("Zielspalten müssen eindeutig sein.")
    return list(mapping.values()), [{target: row[source] for source, target in mapping.items()} for row in rows]


def filter_jsonl(text: str, fields: list[str]) -> str:
    if not fields or any(not field for field in fields) or len(set(fields)) != len(fields):
        raise InputError("Eine eindeutige, nichtleere Feldliste ist erforderlich.")
    lines = text.splitlines()
    if len(lines) > MAX_ROWS:
        raise InputError("Höchstens 100.000 JSONL-Zeilen erlaubt.")
    output = []
    for number, line in enumerate(lines, 1):
        if not line.strip():
            raise InputError(f"JSONL-Zeile {number} ist leer.")
        record = strict_json(line)
        if not isinstance(record, dict):
            raise InputError(f"JSONL-Zeile {number} muss ein Objekt sein.")
        output.append(json.dumps({key: record[key] for key in fields if key in record}, ensure_ascii=False, allow_nan=False))
    return "\n".join(output) + ("\n" if output else "")


def check_contract(records, contract) -> dict:
    types = {"string": lambda x: isinstance(x, str), "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
             "number": lambda x: (isinstance(x, int) and not isinstance(x, bool)) or (isinstance(x, float) and math.isfinite(x)),
             "boolean": lambda x: isinstance(x, bool), "object": lambda x: isinstance(x, dict), "array": lambda x: isinstance(x, list)}
    if not isinstance(contract, dict) or not contract or any(not isinstance(k, str) or not isinstance(v, str) or v not in types for k, v in contract.items()):
        raise InputError("Vertrag muss Feldnamen auf string, integer, number, boolean, object oder array abbilden.")
    if not isinstance(records, list) or len(records) > MAX_ROWS:
        raise InputError("Eingabe muss eine Liste mit höchstens 100.000 Objekten sein.")
    errors = []
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict):
            errors.append({"row": index, "code": "not_object"})
            continue
        for field, kind in contract.items():
            if field not in record:
                errors.append({"row": index, "field": field, "code": "missing"})
            elif not types[kind](record[field]):
                errors.append({"row": index, "field": field, "code": "wrong_type"})
    return {"rows": len(records), "valid": not errors, "errors": errors, "note": "Einfacher Pflichtfelder-/Typcheck; kein JSON-Schema-Validator."}


def utm_links(columns: list[str], rows: list[dict[str, str]]) -> list[dict[str, str]]:
    require_fields(columns, ["url", "source", "medium", "campaign"])
    output = []
    for number, row in enumerate(rows, 2):
        try:
            parts = urlsplit(row["url"].strip())
            _ = parts.port
            if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username is not None or parts.password is not None:
                raise ValueError()
            if any(char.isspace() or ord(char) < 32 for char in row["url"].strip()):
                raise ValueError()
            if any(not row[field].strip() for field in ("source", "medium", "campaign")):
                raise ValueError()
        except ValueError as exc:
            raise InputError(f"Zeile {number}: URL oder erforderliche Kampagnenfelder ungültig.") from exc
        pairs = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True, max_num_fields=200) if not k.casefold().startswith("utm_")]
        pairs.extend(("utm_" + field, row[field].strip()) for field in ("source", "medium", "campaign", "term", "content") if row.get(field, "").strip())
        output.append({"url": urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(pairs), parts.fragment))})
    return output


def calendar_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")


def fold_ics(line: str) -> str:
    parts, current, length = [], "", 0
    for char in line:
        size = len(char.encode("utf-8"))
        if length + size > 75:
            parts.append(current)
            current, length = " ", 1
        current += char
        length += size
    parts.append(current)
    return "\r\n".join(parts)


def calendar_export(columns: list[str], rows: list[dict[str, str]], now: datetime | None = None) -> str:
    require_fields(columns, ["title", "start", "end"])
    stamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Sans Souci//Free Workflow Starter 1.0//DE", "CALSCALE:GREGORIAN"]
    seen = set()
    for number, row in enumerate(rows, 2):
        try:
            start, end = (datetime.fromisoformat(row[field].replace("Z", "+00:00")) for field in ("start", "end"))
            if not row["title"].strip() or start.tzinfo is None or end.tzinfo is None or end <= start:
                raise ValueError()
        except (ValueError, TypeError) as exc:
            raise InputError(f"Zeile {number}: Titel, Zeitzone oder Terminreihenfolge ungültig.") from exc
        identity = row.get("id", "").strip() or json.dumps([row["title"], start.isoformat(), end.isoformat()])
        uid = str(uuid5(NAMESPACE_URL, "sans-souci-starter:" + identity)) + "@sans-souci.at"
        if uid in seen:
            raise InputError(f"Zeile {number}: doppelte Terminidentität.")
        seen.add(uid)
        lines.extend(["BEGIN:VEVENT", "UID:" + uid, "DTSTAMP:" + stamp,
                      "DTSTART:" + start.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                      "DTEND:" + end.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ"), "SUMMARY:" + calendar_text(row["title"])])
        for source, target in (("description", "DESCRIPTION"), ("location", "LOCATION")):
            if row.get(source):
                lines.append(target + ":" + calendar_text(row[source]))
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold_ics(line) for line in lines) + "\r\n"


def hash_file(path: Path) -> tuple[int, str]:
    if path.is_symlink() or not path.is_file():
        raise InputError("Nur reguläre Dateien, keine symbolischen Links erlaubt.")
    digest, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            count += len(chunk)
            if count > MAX_FILE_BYTES:
                raise InputError("Einzeldatei größer als 256 MiB.")
            digest.update(chunk)
    return count, digest.hexdigest()


def make_manifest(folder: Path) -> dict:
    if folder.is_symlink() or not folder.is_dir():
        raise InputError("Ein regulärer Quellordner ist erforderlich.")
    root, files = folder.resolve(), []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise InputError("Symbolische Links im Quellordner nicht erlaubt.")
        if path.is_file():
            if len(files) >= MAX_FILES:
                raise InputError("Höchstens 10.000 Dateien erlaubt.")
            size, digest = hash_file(path)
            files.append({"path": path.relative_to(root).as_posix(), "bytes": size, "sha256": digest})
    return {"format": "sans-souci-sha256-v1", "files": files}


def verify_manifest(folder: Path, manifest) -> dict:
    if folder.is_symlink() or not folder.is_dir():
        raise InputError("Ein regulärer Quellordner ist erforderlich.")
    if not isinstance(manifest, dict) or manifest.get("format") != "sans-souci-sha256-v1" or not isinstance(manifest.get("files"), list) or len(manifest["files"]) > MAX_FILES:
        raise InputError("Unbekanntes oder zu großes Manifest.")
    if not manifest["files"]:
        raise InputError("Ein leeres Manifest liefert keinen Prüfungsnachweis.")
    root, seen, problems, valid = folder.resolve(), set(), [], 0
    for entry in manifest["files"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise InputError("Ungültiger Manifest-Eintrag.")
        relative = PurePosixPath(entry["path"])
        if not relative.parts or relative.is_absolute() or relative.as_posix() != entry["path"] or any(part in {"..", "."} for part in relative.parts) or "\\" in entry["path"] or ":" in entry["path"] or entry["path"].casefold() in seen:
            raise InputError("Manifest enthält unzulässige oder doppelte Pfade.")
        if not isinstance(entry.get("bytes"), int) or isinstance(entry["bytes"], bool) or entry["bytes"] < 0 or not isinstance(entry.get("sha256"), str) or len(entry["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in entry["sha256"]):
            raise InputError("Ungültige Größe oder Prüfsumme.")
        seen.add(entry["path"].casefold())
        candidate = root.joinpath(*relative.parts)
        if any(parent.is_symlink() for parent in [candidate, *candidate.parents] if parent != root and root in parent.parents):
            raise InputError("Symbolische Links im Prüfpfad nicht erlaubt.")
        if not candidate.resolve().is_relative_to(root):
            raise InputError("Datei liegt außerhalb des Quellordners.")
        if not candidate.is_file():
            problems.append({"path": entry["path"], "code": "missing"})
            continue
        size, digest = hash_file(candidate)
        if (size, digest) != (entry["bytes"], entry["sha256"]):
            problems.append({"path": entry["path"], "code": "changed"})
        else:
            valid += 1
    return {"valid": not problems, "checked": len(seen), "unchanged": valid, "problems": problems,
            "note": "Prüft die aufgeführten Dateien. Kein Backup, keine Signatur und keine Vollständigkeitsprüfung zusätzlicher Dateien."}
