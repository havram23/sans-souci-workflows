# CSV-Formelwerte absichern

Formelähnliche Texte werden beim Export mit einem führenden Apostroph als Text markiert.

**Eingabe:** UTF-8-CSV

**Ergebnis:** Neue CSV mit abgesicherten Kopfzeilen und Zelltexten

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python -m sans_starters csv-safe-export examples/contacts.csv output/safe.csv
```

1. Exportdatei lokal auswählen.
2. Neue Ausgabedatei erzeugen.
3. In der vorgesehenen Tabellenanwendung kontrollieren.

## Grenzen

Auch negative Textzahlen können als Text ausgegeben werden. Kein Ersatz für sichere Importeinstellungen; spätere Bearbeitung kann Schutzzeichen entfernen.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Exportwege in Ihren Anwendungen dauerhaft absichern. Persönliche Unterstützung: https://sans-souci.at/#kontakt
