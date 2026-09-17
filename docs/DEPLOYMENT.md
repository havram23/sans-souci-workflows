# Statische Website ergänzend ausliefern

Nach Tests und Paketbau nur den Inhalt von `site/` in das neue Webverzeichnis `/gratis-workflows/` kopieren. Die vorhandene Firmenwebsite, ihre Navigation, Rechtstexte und Startseite nicht durch dieses Projekt ersetzen. Eine ergänzende Verlinkung ist ein eigener, getrennt prüfbarer Schritt.

Die Site erwartet genau diesen Basispfad. Das bestehende `robots.txt` und die bestehende Sitemap nicht überschreiben. Die zusätzliche `sitemap.xml` kann nach erfolgreicher Veröffentlichung in die vorhandene Sitemap-Struktur aufgenommen werden. Die lokale Vorschau liefert absichtlich `noindex`; sie ist kein Webserver für öffentliche Kunden.

Vor Veröffentlichung prüfen:

- Alle 16 HTML-Seiten, Assets und 16 ZIP-Dateien sind vorhanden.
- ZIP-Dateien stimmen mit `downloads/SHA256SUMS.txt` überein.
- Hosting liefert `.js`, `.css`, `.woff2`, `.json` und `.zip` mit passenden MIME-Typen.
- HTTPS ist gültig; Verzeichnisauflistung ist deaktiviert.
- Auf der öffentlichen Route ist kein versehentliches `noindex` aktiv.
- Links zu Firmenwebsite, Kontakt, Impressum und Datenschutz stimmen mit der tatsächlich betriebenen Seite überein.
- Nur das statische Verzeichnis wird öffentlich. Chatarchive, Testnachweise und private Projekte werden nicht mit hochgeladen.

Empfohlene HTTP-Header: `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`. Im Hosting passend konfigurieren und im Browser prüfen; eine Datei allein garantiert keine wirksame Serverkonfiguration.

GitHub Actions prüft die Quellen und kann manuell ein statisches Artefakt erzeugen. Es enthält keine Hosting-Zugangsdaten und führt keine Produktiv-Veröffentlichung aus. GitHub-Pages-Auslieferung unter einem Repository-Basispfad benötigt eine separate Pfadanpassung; nicht ungeprüft aktivieren.
