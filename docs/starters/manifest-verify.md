# Dateibestand gegenprüfen

Fehlende oder geänderte Dateien anhand eines zuvor erzeugten Manifests sichtbar machen.

**Eingabe:** Lokaler Ordner und SHA-256-Manifest

**Ergebnis:** Bericht mit unveränderten, fehlenden und geänderten Dateien

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters manifest-verify examples/sample-files output/verification.json --manifest output/manifest.json
```

1. Zuerst den Starter Datei-Inventur ausführen.
2. Bestand gegen das aufbewahrte Manifest prüfen.
3. Befunde untersuchen; Exitcode 2 signalisiert Abweichungen.

## Grenzen

Prüft nur aufgeführte Dateien. Zusätzliche Dateien, Echtheit des Manifests und Wiederherstellbarkeit werden nicht bestätigt.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Regelmäßige Prüfungen und Zuständigkeiten im Betrieb verankern. Persönliche Unterstützung: https://sans-souci.at/#kontakt
