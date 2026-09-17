# Monitor-Sendeclient mit Warteschlange

Statusereignisse gezielt senden oder ohne Zugangsdaten in einer lokalen Warteschlange ablegen.

**Eingabe:** Status, Ereigniscode und separat konfigurierte Monitor-Verbindung

**Ergebnis:** Empfangsbestätigung oder lokale Ereignisdatei

## Start

Im entpackten Projektordner zuerst `output` anlegen. Keine zusätzlichen Python-Pakete erforderlich.

```text
python clients/monitor_event.py enqueue --status heartbeat --code STARTER_TEST --queue-dir output/outbox
```

1. Zuerst ein synthetisches Ereignis lokal in die Queue schreiben.
2. PILOT_INGEST_URL und PILOT_INGEST_TOKEN in Ihrer Umgebung setzen.
3. Mit python clients/monitor_event.py flush --queue-dir output/outbox zustellen und Ergebnis prüfen.

## Grenzen

Versand erfolgt nur beim expliziten Aufruf. Keine automatische Hintergrundzustellung; ein Queue-Worker je Ordner. Monitor, Hosting und Betrieb sind separat erforderlich. Der Pilot lehnt Ereignisse älter als 24 Stunden ab; solche Dateien bleiben zur Prüfung erhalten.

Vorhandene Dateien werden nicht überschrieben. Beispiele sind synthetisch. Eigene Ergebnisse vor Übernahme oder Weitergabe prüfen.

## Wenn mehr gebraucht wird

Zentrale Vorfälle, Teamrollen, Integration und laufenden Monitor-Betrieb einrichten. Persönliche Unterstützung: https://sans-souci.at/#kontakt
