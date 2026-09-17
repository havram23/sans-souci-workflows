# n8n: Formelähnliche Texte markieren

Verdächtige Textwerte vor einer späteren Tabellenübergabe als Text kennzeichnen.

**Eingabe:** JSON mit Zeichenketten und Zahlen

**Ergebnis:** JSON mit abgesicherten Zeichenketten

## Start

Die JSON-Datei in eine eigene n8n-Instanz importieren:

```text
n8n/n8n-formula-values.json
```

1. Vorlage mit den Beispielen manuell starten.
2. Ausgaben im Code-Knoten nachvollziehen.
3. Den anschließenden CSV-Export einschließlich Kopfzeilen gesondert prüfen.

## Grenzen

Bearbeitet oberste Textwerte; erzeugt selbst keine CSV. Keine vollständige Absicherung eines nachgelagerten Exports. Echter Importtest erforderlich.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Sichere Exporte und geprüfte Datenübergaben in Ihre Systeme integrieren. Persönliche Unterstützung: https://sans-souci.at/#kontakt
