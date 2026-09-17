# Kleines Betriebshandbuch für einen Workflow

Vorlage zur eigenen Ergänzung. Keine Schlüssel, Passwörter, Kundenlisten oder privaten Serveradressen öffentlich eintragen.

## Zuständigkeit und Zweck

Workflowname: ___. Fachliche Rolle: ___. Technische Rolle: ___. Vertretung: ___. Erwartetes Intervall: ___. Zulässige Verspätung: ___.

## Erfolg und Fehler

- Erfolg bedeutet konkret: ___
- Fehlercodes mit Handlungsanweisung: ___
- Fehlender Lauf wird erkannt durch: ___
- Doppelte Vorgänge werden verhindert durch: ___
- Empfänger eines Vorfalls und Reaktionsziel: ___

## Sicherer Wiederanlauf

1. Zustand von Quelle, Queue und Ziel dokumentieren.
2. Bereits abgeschlossene Geschäftsaktionen feststellen.
3. Ursache beheben und mit einem synthetischen Beispiel prüfen.
4. Nur geeignete offene Vorgänge mit stabiler ID erneut zustellen.
5. Mengen und Ergebnisse abgleichen; menschliche Freigabe dokumentieren.

Eine HTTP-Bestätigung allein beweist keinen abgeschlossenen Geschäftsprozess.

## Wartung

| Aufgabe | Verantwortliche Rolle | Rhythmus | Nachweis |
| --- | --- | --- | --- |
| Berechtigungen und Schlüsselablauf prüfen | | | |
| Wiederherstellung aus Backup testen | | | |
| Fehlerfälle und Queue-Alter prüfen | | | |
| Datenaufbewahrung und Löschung prüfen | | | |
| Änderungen und Versionen dokumentieren | | | |
| Abhängigkeiten und Sicherheitsupdates prüfen | | | |

## Abnahme und Änderung

Version: ___. Datum: ___. Testfälle: ___. Beobachtete Grenzen: ___. Fachliche Freigabe: ___. Rücknahmeplan: ___.
