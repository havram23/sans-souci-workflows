# n8n: Felder gezielt weitergeben

Vor der nächsten Workflow-Stufe ausschließlich eine festgelegte Auswahl an Feldern übernehmen.

**Eingabe:** JSON-Datensätze mit Beispieldaten

**Ergebnis:** JSON mit ausdrücklich erlaubten Feldern

## Start

Die JSON-Datei in eine eigene n8n-Instanz importieren:

```text
n8n/n8n-field-filter.json
```

1. Vorlage importieren.
2. Erlaubte Felder im Code-Knoten festlegen.
3. Ausgabe vor dem Anschluss eines Zielsystems prüfen.

## Grenzen

Keine Anonymisierung. Verschachtelte oder erlaubte Felder können weiterhin vertrauliche Inhalte enthalten. Echter Importtest erforderlich.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Datenflüsse und Zugriffsgrenzen für Ihre Integrationen festlegen. Persönliche Unterstützung: https://sans-souci.at/#kontakt
