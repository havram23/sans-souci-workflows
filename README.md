# Sans Souci · kostenlose Workflow-Starter

15 kleine, nachvollziehbare Automatisierungen für Datenqualität, Planung und Betrieb. Entwickelt als kostenloser Einstieg in die Automatisierung wiederkehrender Aufgaben. Code und Dokumentation dürfen unter MIT auch kommerziell verwendet werden. Kein Login, kein Newsletter-Zwang und keine API-Kosten für die enthaltenen lokalen Beispiele.

**Voraussetzungen:** Python 3.11 oder neuer für die Python-Werkzeuge; eine eigene n8n-Installation für n8n-Vorlagen. n8n-Lizenz, Hosting und externe Dienste haben eigene Bedingungen und können kostenpflichtig sein. Die Vorlagen ersetzen keine fachliche Prüfung oder überwachten Produktivbetrieb.

## In drei Schritten starten

1. Archiv herunterladen und entpacken oder dieses Repository klonen.
2. Im Projektordner `output` anlegen, zum Beispiel mit `mkdir output`.
3. Das erste Beispiel ausführen:

```sh
python -m sans_starters csv-audit examples/contacts.csv output/audit.json
```

Das Ergebnis liegt in `output/audit.json`. Die Beispieldaten sind synthetisch. Vorhandene Ausgabedateien werden nicht überschrieben; für einen weiteren Lauf einen neuen Dateinamen wählen.

## Bibliothek

Die vollständige Liste mit Einstieg, Ergebnis und Grenzen steht in [docs/KATALOG.md](docs/KATALOG.md). Jeder Starter hat eine eigene Anleitung in `docs/starters/`. Die Website in `site/` ist für die zusätzliche Route `https://sans-souci.at/gratis-workflows/` vorbereitet.

- **10 Python-Werkzeuge:** CSV-Qualitätscheck, Dublettenbereinigung, Spaltenmapping, Formelwertschutz, JSONL-Feldfilter, JSON-Pflichtfelder, UTM-Links, ICS-Kalenderexport, SHA-256-Inventur und Manifestprüfung.
- **1 Monitor-Client:** expliziter Statusversand, Wiederholungen und lokale Warteschlange ohne gespeicherte Zugangsdaten.
- **4 n8n-Vorlagen:** manuell startbare, inaktive Workflows mit synthetischen Beispielen und ausschließlich lokalen Code-Knoten.
- **GitHub Actions:** Tests und geprüfter Paketbau; zusätzliche manuell zu aktivierende Vorlagen in `github-templates/`.

## Ausführung und Grenzen

- Nur UTF-8-Eingaben; CSV standardmäßig mit Komma. Für Semikolon oder Tab `--delimiter semicolon` beziehungsweise `--delimiter tab` verwenden.
- Maximal 20 MiB je Texteingabe, 100.000 Datenzeilen und 64 KiB je CSV-Feld.
- Alle Python-CSV-Ausgaben markieren formelähnliche Zellen und Kopfzeilen mit Apostroph. Dadurch können etwa negative Textzahlen als Text erscheinen. Nachgelagerte Tabellenimporte müssen trotzdem geprüft werden.
- Exitcodes: `0` erfolgreich, `1` ungültige Eingabe/Ausführung, `2` fachlicher Prüfbefund bei JSON-Vertrag oder Manifest.
- Filterung ist keine Anonymisierung. Prüfsummen sind kein Backup, keine Signatur und kein Nachweis vollständiger Wiederherstellbarkeit.
- Keine Python-Abhängigkeiten zu installieren. Für die lokalen JavaScript-Tests genügt Node.js 22 oder neuer.

## n8n

Eine Datei aus `n8n/` über den Workflow-Import laden und zuerst manuell ausführen. Die Code-Knoten werden in isolierten JavaScript-Tests ausgeführt; ein Import- und Laufzeittest in einer echten n8n-Instanz wurde nicht vorgenommen. Deshalb zuerst die eigene Version und Knotenkompatibilität prüfen. Die Workflows sind inaktiv, haben keine Credentials und versenden keine Daten.

## Workflow-Monitor anbinden

```sh
python clients/monitor_event.py enqueue --status failure --code LOCAL_JOB_FAILED --queue-dir output/outbox
```

Erst zur Übertragung `PILOT_INGEST_URL` und `PILOT_INGEST_TOKEN` in der eigenen Umgebung oder in GitHub Actions Secrets setzen. Keine Schlüssel in Dateien, Kommandozeilenargumente oder Commits schreiben.

```sh
python clients/monitor_event.py flush --queue-dir output/outbox
```

Die Queue speichert nur UUID, Zeitpunkt, Status und einen begrenzten Ereigniscode. Ein bestätigtes Ereignis wird entfernt; bei Fehler bleibt die Datei erhalten. Genau einen Queue-Worker je Ordner ausführen. Die Queue stellt ohne erneuten Aufruf nichts zu. Der Sans-Souci-Pilot akzeptiert Ereignisse nur innerhalb seines Zeitfensters; nach 24 Stunden abgewiesene Ereignisse bleiben zur manuellen Prüfung liegen. Empfang bedeutet weder fachlichen Erfolg noch Behebung eines Vorfalls.

## Entwicklung und Prüfungen

```sh
python tools/build_n8n.py
python -m unittest discover -s tests -v
node --test tests/n8n.test.cjs
python tools/build_site.py
python tools/build_downloads.py
python tools/build_site.py
python tools/check_release.py
python preview.py
```

Lokale Vorschau: `http://127.0.0.1:8772/gratis-workflows/`. Die Vorschau ist kein Produktionsserver.

Optionale Browserprüfung: Playwright separat installieren (`npm install --no-save playwright`, anschließend `npx playwright install chromium`) und `node tests/browser.cjs` ausführen. `PYTHON_EXECUTABLE` kann auf den Python-Interpreter zeigen. Der Test verwendet einen isolierten lokalen Server und ein neues Browserprofil. Ergebnisse liegen im nicht veröffentlichten Ordner `evidence/`.

Zusätzliche Arbeitsvorlagen: [Prozess-Steckbrief](docs/vorlagen/prozess-steckbrief.md), [Datenmapping](docs/vorlagen/datenmapping.csv) und [Betriebshandbuch](docs/vorlagen/betriebshandbuch.md). Hinweise zur Website-Auslieferung: [DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Vom Starter in den Betrieb

Die kostenlosen Werkzeuge bleiben unabhängig nutzbar. Individuelle Systemanbindung, Fehlerbehandlung, Teamrollen, Überwachung und laufende Betreuung erfordern zusätzliche Arbeit. Dafür bietet Sans Souci projektbezogene Unterstützung an: [sans-souci.at](https://sans-souci.at/).

Aktivitäten, Umsatz und Werbe-RPM werden durch die Veröffentlichung dieser Bibliothek nicht garantiert. Produktangebot, Kundennutzen, Vertriebswege und Betriebskosten müssen separat validiert werden.
