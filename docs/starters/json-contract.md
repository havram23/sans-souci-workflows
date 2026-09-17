# JSON-Pflichtfelder prüfen

Erwartete Felder und einfache Datentypen vor der Übergabe an den nächsten Prozess prüfen.

**Eingabe:** JSON-Liste und Feld-/Typvertrag

**Ergebnis:** Bericht mit Zeilennummern und Fehlercodes

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters json-contract examples/records.json output/contract-report.json --contract examples/contract.json
```

1. Pflichtfelder und Datentypen im Vertrag festlegen.
2. Beispielprüfung ausführen.
3. Exitcode 2 als Befund im eigenen Ablauf behandeln.

## Grenzen

Einfacher Typvertrag, kein vollständiger JSON-Schema-Validator und keine fachliche Freigabe.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Verbindliche Schnittstellenverträge und automatisierte Regressionstests aufbauen. Persönliche Unterstützung: https://sans-souci.at/#kontakt
