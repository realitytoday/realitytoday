# Die ganze Server-Flotte in einem Terminalfenster: vps-fleet

*Ein Bauplan samt Prompts für ein tastaturgesteuertes SSH-Cockpit, dazu der fertige Go-Code.*

## Einleitung

Ich betreibe ein paar kleine Server: eine Web-Maschine, eine Datenbank, ein VPN-Gateway
und einige Hobby-VPS. Sie zu prüfen hieß ein SSH-Tab pro Server, und die Frage "ist irgendwo
etwas voll, überlastet oder wartet auf einen Neustart?" kostete zehn Tabs und zehn Befehle.
Monitoring-Stacks beantworten sie, sind aber selbst Server, die man betreiben, absichern und
aktualisieren muss.

Also habe ich ein Cockpit gebaut: ein Terminalfenster, das die Gesundheit jedes Servers auf
einen Blick zeigt, und dasselbe Fenster reicht, um zu beheben, was es zeigt. Laufende Prozesse
ansehen, den Ausreißer beenden, den Dienst neu starten, eine Datei verschieben. Es nutzt den
SSH-Zugang, den du schon hast, und installiert **nichts** auf den Servern.

Gebaut in wenigen Tagen mit KI-Coding-Agenten. Anders als meine anderen Blueprints besteht dieses
aus zwei Teilen: den **Prompts und Begründungen** (diese Anleitung und das Blueprint-Repo) und dem
**fertigen Code** (das Code-Repo). Du kannst es also so nutzen, wie es ist, oder deinen Agenten eine
Version bauen lassen, die zu deinen eigenen Servern passt.

**Zeit:** ein Abend zum Lesen und Ausprobieren, ein Wochenende für die eigene Version.
**Niveau:** Terminal und SSH-Schlüssel sollten vertraut sein. Den Code schreibt der Agent.
**Kosten:** nichts außer den Servern, die du schon hast.

## Was es kann

- **Flottenübersicht:** jeder Server mit CPU-, Speicher- und Platten-Balken, Last, Laufzeit und
  Warnungen für ausgefallene Dienste, volle Platten, hohe Last, ausstehende Updates und nötigen
  Neustart. Tabelle oder Karten, Gruppen, Live-Filter, Sortierung.
- **Dashboard:** Trendlinien über fünf Minuten, Platten- und Netzwerkdurchsatz und daneben eine
  Live-Prozessliste im top-Stil.
- **Top-Ansicht und Kill:** eine Vollbild-Prozessliste; jedes Signal an jeden Prozess senden.
- **Befehls-Runner:** Befehle mit bleibendem Arbeitsverzeichnis und Aliasen, Verlauf, Rückwärtssuche
  und Tab-Vervollständigung von Remote-Pfaden.
- **Systemd-Manager:** Units auflisten, starten, stoppen, neu starten.
- **Dateimanager:** lokal und Server nebeneinander, Hoch- und Herunterladen mit Fortschritt, Ansehen,
  Löschen, chmod, chown, chgrp.
- **Profile:** getrennte Serverlisten für Arbeit, Zuhause oder Kunden.

## Die Entscheidungen, auf die es ankommt

**Agentenlos.** Wenn du dich per `ssh` einloggen kannst, lässt sich der Server verwalten: kein Daemon,
kein Exporter, kein offener Port. Der Preis: Jede Zahl stammt bei jeder Abfrage aus einem Shell-Befehl.
Das Metrik-Skript ist deshalb sorgfältig entworfen: eine SSH-Sitzung, eine Zeile mit Präfix pro Metrik,
ausgewertet nach Präfix statt nach Position.

**Dem ersten `top`-Bild nie trauen.** Seine CPU-Werte sind seit dem Prozessstart gemittelt. Das Werkzeug
ruft `top` zweimal auf und behält das zweite Bild. Auf minimalen Systemen wie Alpine fällt es auf `ps`
zurück und sagt das auch.

**Alles quoten.** Eine Datei namens `$(reboot).txt` auf einem Server darf beim nächsten Löschen nichts
ausführen. Jeder Wert in einem Remote-Befehl, auch Namen, die vom Server selbst kamen, steht in einfachen
Anführungszeichen mit vorangestelltem `--`.

**Host-Keys prüfen.** Meine erste Version hat die Prüfung übersprungen. Das war das Erste, was ich vor
der Veröffentlichung korrigiert habe: Das Werkzeug merkt sich einen Server beim ersten Kontakt und lehnt
ihn ab, wenn sich sein Schlüssel jemals ändert.

## Mit dem Agenten bauen

Beginne mit dem Projekt-Brief: Lege `prompts/00-project-brief.md` als `CLAUDE.md` oder `AGENTS.md` in ein
neues Repository und fülle die Platzhalter aus. Gib dem Agenten dann die sechs Prompts der Reihe nach,
einen pro Sitzung, und prüfe jeweils die Abnahmekriterien an einem echten Server, bevor du weitermachst:

1. Fundament und SSH: Konfiguration und Profile, SSH-Client, Host-Keys, Quoting-Helfer.
2. Metriken und Flottenübersicht: Metrik-Skript, Zustand und Warnungen, Sortieren und Filtern.
3. Dashboard und Prozesse: Trends, Prozessliste, Top-Ansicht und Kill-Dialog.
4. Befehls-Runner und Systemd-Manager.
5. Der Zwei-Fenster-Dateimanager.
6. Profile, Einstellungen und die Checkliste für die Veröffentlichung.

Teste mit mindestens zwei Arten von Servern (zum Beispiel Debian und Alpine). Parser, die bei einer
Distribution funktionieren, brechen bei einer anderen oft.

## Die fertige Version starten

Zum Bauen brauchst du Go. Unter Linux oder macOS:

```sh
git clone https://github.com/realitytoday/vps-fleet-tui.git
cd vps-fleet-tui
go build -o vps-fleet ./cmd/vps-fleet
./vps-fleet
```

Unter Windows braucht die Ausgabedatei die Endung `.exe`, sonst führt Windows sie nicht aus:

```powershell
go build -o vps-fleet.exe ./cmd/vps-fleet
.\vps-fleet.exe
```

Beim ersten Start legt es eine Beispielkonfiguration in `~/.config/vps-fleet/` an. Trage dort deine
Server ein. Nimm lieber SSH-Schlüssel als das Feld `password`, das im Klartext gespeichert wird.

## Was noch fehlt

Der Befehls-Runner führt einzelne Befehle aus, ist also kein vollwertiges interaktives Terminal; Programme
wie `vim` oder `htop` laufen darin nicht. Ganze Ordner kopieren kann der Dateimanager noch nicht, und ein
WireGuard-Plugin, eine Hilfe-Ansicht und das Anzeigen von Logs gibt es auch nicht. Es gibt keinen Verlauf
und keine Alarmierung, wenn das Fenster geschlossen ist: ein Cockpit, kein Monitoring-System. Windows-Server
sind nicht vorgesehen. Besser, das zu sagen, als dich auf etwas bauen zu lassen, das es nicht gibt.

## Den Bauplan holen

Die Prompts, die Architektur, die Tastenbelegung und die Lessons Learned liegen im Blueprint-Repo, der
fertige Go-Code im Code-Repo.
