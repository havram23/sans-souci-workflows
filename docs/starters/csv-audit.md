# CSV-Qualitätscheck

Leere Felder, auffällige Formelwerte und Feldlängen erkennen, bevor ein Export weiterverarbeitet wird.

**Eingabe:** CSV mit eindeutiger Kopfzeile

**Ergebnis:** JSON-Bericht mit Kennzahlen je Spalte

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters csv-audit examples/contacts.csv output/audit.json
```

1. Beispieldatei unverändert ausprobieren.
2. Eigene UTF-8-CSV mit eindeutigen Spaltennamen verwenden.
3. Leere oder auffällige Felder im Quellsystem prüfen.

## Grenzen

Prüft Struktur und Füllstände; bestätigt weder korrekte Inhalte noch datenschutzrechtliche Zulässigkeit.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Prüfregeln und Datenübernahme in Ihre Systeme integrieren. Persönliche Unterstützung: https://sans-souci.at/#kontakt
