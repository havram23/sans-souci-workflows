# CSV in Kalendertermine

Aus einer Terminliste entsteht eine importierbare ICS-Datei mit eindeutigem Zeitbezug.

**Eingabe:** CSV mit Titel, Start und Ende inklusive Zeitzone

**Ergebnis:** ICS-Datei mit UTC-Zeitpunkten

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters calendar-export examples/appointments.csv output/appointments.ics
```

1. Termine mit explizitem UTC-Offset eintragen.
2. ICS-Datei erzeugen.
3. Zuerst in einen separaten Testkalender importieren.

## Grenzen

Kein Einladungsversand, keine Synchronisation und keine Duplikatgarantie des Zielkalenders. Wiederkehrende Termine nicht enthalten.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Planung und Kalenderfreigaben kontrolliert in Ihren Prozess integrieren. Persönliche Unterstützung: https://sans-souci.at/#kontakt
