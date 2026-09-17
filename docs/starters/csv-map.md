# CSV-Spaltenmapper

Ausgewählte Felder in eine klare Zielstruktur bringen, ohne das Original zu verändern.

**Eingabe:** CSV und JSON-Datei mit Quell-/Zielspalten

**Ergebnis:** Neue CSV mit ausschließlich den gewählten Feldern

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters csv-map examples/contacts.csv output/mapped.csv --mapping examples/mapping.json
```

1. Das Mapping an Ihre Zielspalten anpassen.
2. Mit einer Kopie Ihres Exports ausführen.
3. Ergebnis vor dem Import in das Zielsystem prüfen.

## Grenzen

Keine Typkonvertierung, Übersetzung oder automatische Verbindung zu einem CRM.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Wiederkehrende Importe mit Validierung und Fehlerbehandlung einrichten. Persönliche Unterstützung: https://sans-souci.at/#kontakt
