# n8n: Pflichtfelder sichtbar prüfen

Eine manuell startbare Vorlage ergänzt jeden Datensatz um ein nachvollziehbares Prüfergebnis.

**Eingabe:** Synthetische JSON-Beispiele im Code-Knoten

**Ergebnis:** JSON-Datensätze mit gültig/ungültig und fehlenden Feldern

## Start

Die JSON-Datei in eine eigene n8n-Instanz importieren:

```text
n8n/n8n-required-fields.json
```

1. JSON-Datei in n8n importieren.
2. Manuell mit den enthaltenen Beispieldaten ausführen.
3. Pflichtfelder und Datenquelle vor einer Integration anpassen.

## Grenzen

JSON-Struktur und JavaScript-Knoten werden getestet. Ein echter Importlauf in Ihrer n8n-Version ist separat erforderlich. Keine externen Aufrufe oder Zugangsdaten.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Fehlerwege, Freigaben und den überwachten Betrieb des Workflows ergänzen. Persönliche Unterstützung: https://sans-souci.at/#kontakt
