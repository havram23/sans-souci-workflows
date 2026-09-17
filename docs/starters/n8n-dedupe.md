# n8n: Dubletten markieren

Mehrfache IDs kennzeichnen und auf das erste Vorkommen verweisen, ohne Datensätze zu löschen.

**Eingabe:** JSON-Datensätze mit einer ID

**Ergebnis:** JSON mit Dublettenkennzeichen und Eingangsindex

## Start

Die JSON-Datei in eine eigene n8n-Instanz importieren:

```text
n8n/n8n-dedupe.json
```

1. Vorlage importieren und manuell ausführen.
2. Schlüsselfeld im Code-Knoten anpassen.
3. Markierte Fälle in einem eigenen Freigabeschritt bearbeiten.

## Grenzen

Nur innerhalb eines Laufs. Fehlende IDs bleiben eigenständige Fälle. Kein systemübergreifender Abgleich; echter Importtest erforderlich.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Persistente Idempotenz und systemübergreifende Datenabgleiche entwickeln. Persönliche Unterstützung: https://sans-souci.at/#kontakt
