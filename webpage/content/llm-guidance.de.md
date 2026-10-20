# Welches KI-Modell und welchen Agenten solltest du nutzen?

*Praktische Hinweise, um die Blueprints dieser Seite mit einem Coding-Agenten nachzubauen.*

## Warum das Modell zählt

Die Prompts in meinen Blueprints sind für einen Coding-**Agenten** geschrieben, nicht für ein Chatfenster. Der Agent muss einen Projekt-Brief lesen, Änderungen über mehrere Dateien planen, Befehle ausführen, Fehlermeldungen auswerten und die Regeln des Projekts über eine lange Sitzung im Blick behalten. Genau darin unterscheiden sich Modelle stark. Derselbe Prompt liefert mit einem Modell ein funktionierendes Backend und mit einem anderen ein Durcheinander, das nur plausibel aussieht.

Modellnamen und Rankings ändern sich alle paar Monate. Diese Seite spricht deshalb von Modellklassen, nicht von Versionen. Prüfe vor dem Start, was aktuell ist.

## Die kurze Empfehlung

Nimm das **stärkste Modell, auf das du Zugriff hast**: Claude Opus oder ein vergleichbares Spitzenmodell eines anderen Anbieters. Setze es dort ein, wo Fehler teuer sind: bei Architektur, Backend und allem, was Hardware, Linux-Desktop-Einstellungen oder Deployment betrifft. Für die wiederkehrenden Teile wie Feinschliff an der Oberfläche, kleine Korrekturen und die Admin-Seite reicht meist ein Modell der mittleren Klasse (Sonnet-Klasse oder ähnlich), das auch günstiger ist. Kleinere oder offene Modelle können ebenfalls funktionieren, aber plane kleinere Arbeitsschritte und mehr Kontrolle ein.

Eine Faustregel aus eigener Erfahrung, kein Benchmark:

| Teil des Home Information Screen | Was das Modell leisten muss | Empfohlene Klasse |
|---|---|---|
| Backend und Integrationsmuster (Cache, veraltete Daten, Rückfall) | Konsistentes Design über viele Dateien, Disziplin bei Vorgaben | Spitzenklasse |
| Integrationen (Kalender-Wiederholungen, Anwesenheit, Webhooks, Sensoren) | Genaues Lesen von Protokollen und Randfällen | Spitzen- oder Mittelklasse |
| Pi-Einrichtung (Wayland, Touch-Zuordnung, systemd, Hintergrundbeleuchtung) | Spezielles, versionsabhängiges Linux-Wissen, Fehlersuche anhand von Logs | Spitzenklasse |
| Bildschirm-Oberfläche und Design-System | Viele kleine Stilregeln gleichzeitig befolgen | Mittelklasse reicht oft |
| Bewegungs- und Schlaf-Dienst | Kleines Programm, Referenzimplementierung liegt bei | Mittelklasse |
| Docker-Image und Auslieferung | Bekannte Muster, aber unverzeihlich | Mittelklasse |
| Admin-Seite | Routine-Formulare und CRUD | Mittelklasse |

## Tipps für jeden Agenten

- **Führe einen kurzen Projekt-Brief** (`CLAUDE.md` oder `AGENTS.md`) mit den festen Entscheidungen: Architektur, Stack, Sicherheits- und Design-Regeln. Das Blueprint enthält eine Vorlage für beide Dateinamen. Eine Seite, die der Agent in jeder Sitzung liest, schlägt ein langes Wiki, das er ignoriert.
- **Ein Prompt pro Sitzung oder Aufgabe.** Füge nicht alle Prompts auf einmal ein. Ein Teil fertigstellen, am echten Gerät testen, committen, dann weitermachen.
- **Gib dem Agenten die Referenzdateien.** Der Ordner `reference/` existiert, weil genaue Skripte und Verträge besser sind als Beschreibungen.
- **Lass ihn zuerst planen.** Bitte um einen kurzen Plan und lies ihn, bevor Code entsteht. Korrekturen sind dann am billigsten.
- **Führe aus und gib die Ausgabe zurück.** Baue, teste und lies Logs selbst oder lass den Agenten das tun, und füge echte Fehlermeldungen ein, statt sie zu beschreiben.
- **Committe oft.** Läuft eine Sitzung schief, willst du einen sauberen Punkt zum Zurückkehren haben.
- **Führe ein Entscheidungsprotokoll.** Datierte Einträge zu Entscheidungen und Fehlern. Es wird der Kontext, den du einer frischen Sitzung mitgeben kannst.
- **Starte lange Sitzungen neu.** Vergisst der Agent Regeln oder wiederholt Fehler, beginne eine neue Sitzung mit Brief und Entscheidungsprotokoll.
- **Lass ihn keine Sicherheit aufweichen, damit etwas läuft.** Die Regel des Blueprints lautet: TLS-Prüfung nie abschalten.

## Tipps für Mistral Vibe und ähnliche Agenten

Der Agent von Mistral ist eine gute Wahl, wenn du einen europäischen Anbieter bevorzugst oder dir Optionen offenhalten willst. Ich habe diese Blueprints nicht durchgängig damit getestet. Nimm das Folgende deshalb als sinnvolle Ausgangspunkte und nicht als geprüfte Ergebnisse.

- **Prüfe, welche Brief-Datei er liest** (`AGENTS.md` ist eine verbreitete Konvention) und lege den Projekt-Brief dort ab. Das Blueprint enthält eine `AGENTS.md`.
- **Nutze kleinere Schritte.** Teile jeden Blueprint-Prompt in Teilaufgaben, etwa zuerst "Datenmodell und Speicher", dann "Kalender-Integration". Eine Aufgabe, eine Dateiliste, ein Ziel.
- **Nenne Dateien und Stack ausdrücklich.** Schreibe "Go, nur Standardbibliothek, eine YAML-Datei je Speicher" in jede Aufgabe, statt darauf zu vertrauen, dass der Agent es behält.
- **Füge das Referenzmaterial ein oder verweise darauf**, wenn das Verhalten exakt sein muss, etwa bei den Pi-Skripten und dem API-Vertrag.
- **Lass dir den Plan zeigen und prüfe ihn.** Schwächere Modelle legen häufiger auf Basis einer falschen Annahme los.
- **Kontrolliere mehr.** Führe nach jedem Schritt Tests und Build aus und teste an der echten Hardware, bevor es weitergeht.
- **Gib die schweren Probleme nach oben.** Hängst du bei Wayland-Drehung, Touch-Zuordnung oder einer systemd-Unit, gib genau dieses Problem einem Spitzenmodell und mach danach mit deinem bevorzugten Agenten weiter.
- **Halte den Kontext klein.** Eine frische Sitzung pro Aufgabe, mit Brief und Entscheidungsprotokoll.

## Wenn etwas schiefgeht

Ist das Ergebnis plausibel, aber falsch, liegt es meist an einem von drei Dingen: Die Aufgabe war zu groß, eine Regel aus dem Brief ging verloren, oder dem Modell fehlte Wissen über die konkrete Hardware oder Softwareversion. Mach die Aufgabe kleiner, wiederhole die Regel oder wechsle für diesen Schritt auf ein stärkeres Modell.
