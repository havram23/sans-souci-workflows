# Datei-Inventur mit SHA-256

Eine nachvollziehbare Liste aus Dateinamen, Größen und Prüfsummen erstellen.

**Eingabe:** Lokaler Ordner mit regulären Dateien

**Ergebnis:** Manifest außerhalb des Quellordners

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters file-manifest examples/sample-files output/manifest.json
```

1. Einen klar begrenzten Ordner auswählen.
2. Manifest außerhalb dieses Ordners speichern.
3. Manifest getrennt und gegen nachträgliche Änderungen geschützt aufbewahren.

## Grenzen

Erstellt kein Backup. Symbolische Links werden abgewiesen; maximal 10.000 Dateien und 256 MiB pro Datei.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Backup-Routinen mit Wiederherstellungstests und Alarmierung aufbauen. Persönliche Unterstützung: https://sans-souci.at/#kontakt
