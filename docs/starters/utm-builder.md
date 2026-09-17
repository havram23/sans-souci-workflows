# UTM-Linkbuilder

Kampagnenlinks aus einer Tabelle konsistent zusammensetzen, ohne einen Onlinedienst aufzurufen.

**Eingabe:** CSV mit URL, Quelle, Medium und Kampagne

**Ergebnis:** CSV mit fertig kodierten Links

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters utm-builder examples/campaigns.csv output/links.csv
```

1. Kampagnennamen und Schreibweise im Team festlegen.
2. Vorhandene Beispiel-URLs ersetzen.
3. Erzeugte Links vor der Veröffentlichung öffnen und prüfen.

## Grenzen

Bestehende UTM-Parameter werden ersetzt. Kein Tracking, keine Analyseinstallation und keine automatische Veröffentlichung.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Kampagnen, CRM-Zuordnung und nachvollziehbare Auswertung verbinden. Persönliche Unterstützung: https://sans-souci.at/#kontakt
