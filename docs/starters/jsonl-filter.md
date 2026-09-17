# JSONL-Feldfilter

Nur ausdrücklich ausgewählte Felder in einen neuen Export übernehmen.

**Eingabe:** JSONL mit einem Objekt pro Zeile

**Ergebnis:** JSONL mit den erlaubten Feldern

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters jsonl-filter examples/events.jsonl output/events.jsonl --fields event_id status
```

1. Eine minimale Feldliste festlegen.
2. Den gefilterten Export prüfen.
3. Vor Weitergabe kontrollieren, ob erlaubte Felder noch vertrauliche Inhalte enthalten.

## Grenzen

Filtert oberste Felder. Keine Anonymisierung und keine Prüfung verschachtelter Inhalte.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Datenminimierung und Berechtigungen entlang Ihrer Schnittstellen umsetzen. Persönliche Unterstützung: https://sans-souci.at/#kontakt
