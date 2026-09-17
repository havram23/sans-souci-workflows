# Dubletten kontrolliert entfernen

Mehrfache Datensätze anhand selbst gewählter Schlüssel erkennen. Das erste Vorkommen bleibt erhalten.

**Eingabe:** CSV und eine oder mehrere Schlüsselspalten

**Ergebnis:** Neue CSV und Zusammenfassung der entfernten Zeilen

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters csv-dedupe examples/contacts.csv output/clean.csv --keys id
```

1. Geeignete fachliche Schlüssel festlegen.
2. Ergebnis mit dem Original vergleichen.
3. Fehlende Schlüssel separat nachbearbeiten; diese Datensätze bleiben erhalten.

## Grenzen

Trimmt und vergleicht Schlüssel ohne Groß-/Kleinschreibung. Kein unscharfer Personenabgleich und keine Prüfung über mehrere Dateien.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Datenqualität kontinuierlich im CRM oder ERP absichern. Persönliche Unterstützung: https://sans-souci.at/#kontakt
