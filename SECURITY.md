# Sicherheitsmeldungen und Daten

Bitte keine Zugangsdaten, privaten Dateien oder Kundendaten in öffentliche Issues und Pull Requests schreiben. Eine Sicherheitsmeldung ohne vertrauliche Inhalte kann an die auf https://sans-souci.at/impressum.html veröffentlichte Kontaktadresse gesendet werden. Keine produktiven Systeme ohne Freigabe testen.

Die Werkzeuge verarbeiten lokale Dateien. Ausschließlich `clients/monitor_event.py` kann beim ausdrücklichen Aufruf Daten an das konfigurierte Monitor-Ziel senden. Dieser Client folgt keinen Weiterleitungen, verlangt HTTPS außerhalb von Loopback und schreibt keine Schlüssel in seine Warteschlange.

Lokale Dateiprüfungen sind für ein vertrauenswürdiges, nicht gleichzeitig manipuliertes Dateisystem ausgelegt. Nicht auf Verzeichnisse anwenden, die ein anderer Prozess gezielt während der Prüfung verändert. Ergebnisse vor einem Import oder einer Weitergabe fachlich prüfen.

Die Downloadarchive werden aus einer Positivliste gebaut. Private Verkaufsprodukte, Datenbanken, `.env`-Dateien, Chatarchive und Zugangsdaten sind kein Bestandteil dieses Projekts.
