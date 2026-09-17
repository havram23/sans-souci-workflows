from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from . import core


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Kostenlose, lokale Sans-Souci-Workflow-Starter. Vorhandene Dateien werden nie überschrieben.")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("csv-audit", "csv-dedupe", "csv-map", "csv-safe-export", "jsonl-filter", "json-contract", "utm-builder", "calendar-export", "file-manifest", "manifest-verify"):
        sub = commands.add_parser(name)
        sub.add_argument("input", type=Path)
        sub.add_argument("output", type=Path)
        if name.startswith("csv-") or name in {"utm-builder", "calendar-export"}:
            sub.add_argument("--delimiter", choices=("comma", "semicolon", "tab"), default="comma")
        if name == "csv-dedupe": sub.add_argument("--keys", nargs="+", required=True)
        if name == "csv-map": sub.add_argument("--mapping", type=Path, required=True)
        if name == "jsonl-filter": sub.add_argument("--fields", nargs="+", required=True)
        if name == "json-contract": sub.add_argument("--contract", type=Path, required=True)
        if name == "manifest-verify": sub.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        summary = {"command": args.command, "status": "ok"}
        status = 0
        if hasattr(args, "delimiter"):
            columns, rows = core.read_csv(args.input, {"comma": ",", "semicolon": ";", "tab": "\t"}[args.delimiter])
        if args.command == "csv-audit":
            text = core.json_output(core.audit_csv(columns, rows))
        elif args.command == "csv-dedupe":
            kept, summary_data = core.dedupe(columns, rows, args.keys)
            summary.update(summary_data)
            text = core.csv_output(columns, kept)
        elif args.command == "csv-map":
            mapped_columns, mapped_rows = core.map_csv(columns, rows, core.strict_json(core.read_text(args.mapping)))
            text = core.csv_output(mapped_columns, mapped_rows)
        elif args.command == "csv-safe-export":
            text = core.csv_output(columns, rows)
        elif args.command == "jsonl-filter":
            text = core.filter_jsonl(core.read_text(args.input), args.fields)
        elif args.command == "json-contract":
            report = core.check_contract(core.strict_json(core.read_text(args.input)), core.strict_json(core.read_text(args.contract)))
            text, status = core.json_output(report), 0 if report["valid"] else 2
        elif args.command == "utm-builder":
            text = core.csv_output(["url"], core.utm_links(columns, rows))
        elif args.command == "calendar-export":
            text = core.calendar_export(columns, rows)
        elif args.command == "file-manifest":
            if args.output.resolve().is_relative_to(args.input.resolve()):
                raise core.InputError("Manifest außerhalb des inventarisierten Ordners speichern.")
            text = core.json_output(core.make_manifest(args.input))
        else:
            report = core.verify_manifest(args.input, core.strict_json(core.read_text(args.manifest)))
            text, status = core.json_output(report), 0 if report["valid"] else 2
        core.write_new(args.output, text)
        summary["status"] = "findings" if status else "ok"
        print(json.dumps(summary, ensure_ascii=False))
        return status
    except (core.InputError, OSError, UnicodeError, ValueError, OverflowError) as exc:
        # User data and credential-like input values are not echoed in error output.
        message = str(exc) if isinstance(exc, core.InputError) else "Datei oder Eingabe konnte nicht verarbeitet werden. Format, Pfad und Rechte prüfen."
        print(json.dumps({"status": "error", "message": message}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
