# Ein ruhiges Wand-Dashboard für die Familie: Home Information Screen mit Raspberry Pi

*Gebaut mit einem KI-Coding-Agenten. Kein Code zum Herunterladen, sondern ein Bauplan und die Prompts dazu.*

**Titelbild:** der montierte Bildschirm im Flur, Kalender sichtbar.

## Einleitung

Unsere Termine lebten in fünf Apps, und keine wurde im richtigen Moment
geöffnet. Also hängt jetzt ein Bildschirm im Flur. Er zeigt den gemeinsamen
Kalender, das Wetter, wer zu Hause ist, wer heute mit dem Abwasch dran ist, ob im
Keller etwas ausläuft, und eine Wand voller Notizzettel ("bin gegen 19 Uhr
zurück"). Er wacht auf, wenn jemand vorbeigeht, und wird dunkel, wenn niemand da ist.

Ich habe ihn in etwa drei Wochen mit KI-Agenten gebaut. Diese Anleitung gibt dir
nicht meinen Code. Dein Kalenderserver, dein Router und dein Haushalt sind anders
als meine. Sie gibt dir deshalb das, was sich besser übertragen lässt: die
Architektur, die Design-Regeln, die Verkabelung, meine Fehler und die Prompts, mit
denen ich jedes Teil gebaut habe.

**Zeit:** ein paar Abende Hardware plus Agent-Sitzungen für die Software.
**Niveau:** Terminal und Docker sollten vertraut sein. Den Code schreibt der Agent.
**Kosten:** etwa ein Pi 4, ein Touchscreen und ein PIR-Sensor, dazu ein Server, den
du vermutlich schon hast.

## Material

- Full-HD-Touchscreen ab 14" mit USB-Touch, im Hochformat montiert
- Raspberry Pi 4B (4 GB) mit Raspberry Pi OS Trixie (64 Bit)
- PIR-Bewegungsmelder (HC-SR501 o. ä.), drei Buchse-Buchse-Jumperkabel
- Ein dauerhaft laufender Rechner mit Docker: NAS, Mini-PC oder alter Laptop
- HDMI- und USB-Kabel, 20 bis 30 cm
- Optional: 3D-Drucker (ASA), Magnete, dünnes Stahlblech und VHB-Band für die Halterung
- Optional: UniFi-Gateway (Anwesenheit, Leck-Sensoren) und CalDAV-Server
- Ein KI-Coding-Agent deiner Wahl

## Schritt 1: Die eine große Entscheidung verstehen

**Der Pi zeigt an, der Server rechnet.**

Der Pi startet nur einen Vollbild-Browser und liest den Bewegungsmelder. Alles, was
Kalender abfragt, Wetter zwischenspeichert, Notizen ablegt und prüft, wer zu Hause
ist, läuft in einem kleinen Container auf deinem Server. So kannst du den Pi neu
aufsetzen, ohne etwas zu verlieren, und er hat neben dem Browser genug Speicher.

Folgen, die du einplanen musst: Der Bildschirm spricht über dein LAN mit dem Server,
ein gemeinsamer API-Schlüssel ist das einzige Schloss, und liegen beide Geräte in
verschiedenen Netzsegmenten, brauchst du Firewall-Regeln für API- **und**
Webhook-Port.

## Schritt 2: Festlegen, wofür der Bildschirm da ist

Sieben Bildschirme, bedient über eine schwebende Tab-Leiste mit Symbolen:

1. **Ruhe:** riesige Uhr, Wetter in einer Zeile, wer zu Hause ist.
2. **Kalender:** die nächsten sieben Tage, groß der nächste Termin, nur lesend.
3. **Essen:** Restaurant-Kacheln, Zufallswahl, "das Übliche" pro Person.
4. **Aufgaben:** heutige Aufgaben je Person mit runden Häkchen.
5. **Wetter:** animierter Himmel, Stundenleiste, Regen gegen Sonnenschein.
6. **Sensoren:** Türen, Fenster, Lecks, Temperatur, Feuchte.
7. **Notizen:** verschiebbare Zettel mit Bildschirmtastatur.

Der Startbildschirm folgt der Uhrzeit: morgens Kalender, mittags Wetter, abends
Essen, nachts Ruhe. Ein Tippen übersteuert das, bis der Bildschirm schläft.

## Schritt 3: Hardware montieren und verkabeln

Den Bildschirm im Hochformat montieren (90° nach links gedreht). Den Pi im normalen
Gehäuse kopfüber unter ein Brett hängen, mit Magneten gehalten, damit die SD-Karte
mit einem Zug erreichbar bleibt.

PIR an die 40-polige Stiftleiste:

| PIR | Pi |
|---|---|
| VCC | Pin 2 (5 V) |
| GND | Pin 6 |
| OUT | Pin 12 (GPIO18) |

Tipps: Das Trimmpoti für die Haltezeit auf Minimum stellen und die Regel "fünf
Minuten ohne Bewegung" in Software lösen. Nach dem Einschalten eine Minute warmlaufen
lassen. Die Kuppel nie mit Kunststoff abdecken und nicht direkt neben den heißen
Chip setzen.

**Stromversorgung prüfen.** Ein Pi 4 braucht 5 V bei 3 A. Am USB-Anschluss des
Monitors bootet er oft und bricht dann unter Last ein. Zeigt sich die
Unterspannungswarnung, nimm ein richtiges USB-C-Netzteil.

## Schritt 4: Drehung und Touch einrichten (Wayland, nicht X11)

Das aktuelle Raspberry Pi OS nutzt den Wayland-Compositor labwc. Die üblichen
`xrandr`- und `xinput`-Tipps funktionieren deshalb nicht. Die Bildschirmausrichtung
im Desktop-Bereich "Bildschirme" auf 270 stellen und Touch in
`~/.config/labwc/rc.xml` zuordnen:

```xml
<touch deviceName="vollständiger Gerätename deines Touch-Controllers"
       mapToOutput="HDMI-A-1" mouseEmulation="no"/>
```

Zwei Fallen:

- `mouseEmulation` muss `"no"` sein, sonst funktioniert das Wischen überall nicht.
- Der Gerätename enthält den USB-Port-Pfad. Wird das Kabel umgesteckt, ändert er
  sich und Touch fällt stumm aus.

## Schritt 5: Regeln festlegen, bevor der Agent eine Zeile schreibt

Lege einen kurzen Projekt-Brief (`CLAUDE.md`) mit den festen Entscheidungen an:
Architektur, Stack (Go auf dem Server, Svelte am Bildschirm, YAML-Dateien statt
Datenbank, Polling statt WebSockets), die TLS-Regel (Prüfung nie abschalten) und die
Design-Regeln. Das Blueprint-Repo enthält eine ausfüllbare Vorlage.

Ein einseitiger Brief, den der Agent in jeder Sitzung liest, schlägt ein langes Wiki,
das er ignoriert. Führe außerdem ab sofort ein Entscheidungsprotokoll mit
datierten Einträgen zu Entscheidungen und jedem Fehler. Es wird die wertvollste Datei
des Projekts.

## Schritt 6: Backend mit dem Agenten bauen

Gib dem Agenten Prompt 01: ein Go-Server nur mit der Standardbibliothek, ein
gemeinsamer API-Schlüssel beim ersten Start, eine YAML-Datei je Speicher und ein
wiederverwendbares Muster für jede Integration: **Cache, veraltete Daten bei Fehlern
und eine Testdatei als letzte Rückfalloption**. Deshalb ist der Bildschirm nie leer
und zeigt nie einen rohen Fehler.

Auf dem echten Gerät prüfen, bevor es weitergeht.

## Schritt 7: Integrationen einzeln ergänzen

Prompt 02 deckt Kalender (den Server wiederkehrende Termine auflösen lassen), Wetter
(Open-Meteo braucht keinen Schlüssel), Anwesenheit, Webhooks und Sensoren ab. Was mir
Stunden gespart hat:

- Handy-Anwesenheit über die Clientliste des Routers schlägt Ping, weil ein
  schlafendes Handy-WLAN Pings ignoriert.
- Alarmsysteme senden Schwellenwert-Ereignisse, keine Messwerte. Den Sensor-Bildschirm
  für "zu warm" entwerfen, nicht für 23,4 °C.
- Wasserlecks melden nie "behoben". Sie rasten ein, der Quittieren-Knopf gehört auf den
  Bildschirm selbst.
- TLS-Prüfung nie abschalten. Eine kleine eigene Zertifizierungsstelle anlegen und nur
  diese eine Wurzel vertrauen.

## Schritt 8: Den Bildschirm bauen

Prompt 03 baut die Oberfläche nach einem Design-System namens Ruhe: keine Karten, keine
Rahmen, keine transparenten Tönungen, alles rund, Farbe nur für Zustand, Person oder
Restaurant, eine Palettendatei, große Schrift. Das Display hängt 16 Stunden am Tag
da und muss aus vier Schritten Entfernung in zwei Sekunden lesbar sein.

Zwei Details, die ich mag: Notizzettel sind um wenige Grad geneigt, abgeleitet aus
ihrer ID, sodass die Wand handgesetzt wirkt, ohne bei jedem Neuzeichnen zu zittern.
Das Wetterdiagramm zeigt Regenwahrscheinlichkeit gegen die echte Sonnenscheindauer.

## Schritt 9: Schlafen lassen

Prompt 04 baut einen kleinen Bewegungs-Dienst: Fünf Minuten keine Bewegung, und die
Hintergrundbeleuchtung geht aus. Bewegung oder Berührung weckt ihn. Schlafen und
Aufwachen laufen lokal und funktionieren auch ohne Netzwerk. Das Blueprint-Repo
enthält meine funktionierende Version (etwa 200 Zeilen Go, dazu systemd-Unit und
Konfigurationsdatei) unter `reference/pi/`, damit dein Agent das genaue Verhalten
vor Augen hat.

Zum Abschalten `wlopm` benutzen, **nicht** `wlr-randr --off`, das den Browser
abstürzen lässt. Den Browser-Dienst mit `Restart=always` betreiben und den
gespeicherten Beendigungsstatus des Browsers beim Start korrigieren, damit nach einem
Stromausfall keine Wiederherstellungsabfrage erscheint.

## Schritt 10: Ausliefern

Prompt 05: ein mehrstufiges Docker-Image mit Distroless-Laufzeit, auf dem
Entwicklungsrechner gebaut, in eine Registry geschoben, auf dem Server gezogen. Ein
Versionsfeld im Health-Endpunkt gleich am Anfang einbauen. Als ein "Redeploy bewirkt
nichts"-Abend verloren ging, hat genau dieses Feld ein altes Image-Tag aufgedeckt.

Denk daran: Der Bildschirm zeigt die Seite, die beim Start geladen wurde. Nach einer
Frontend-Änderung den Kiosk-Dienst neu starten.

## Schritt 11: Admin-Seite

Prompt 06 ergänzt eine laptoptaugliche Seite für Zeitplan, Kalender-Zugang,
Anwesenheitsgeräte, Personen und Sensoren, damit niemand per SSH eine Farbe oder IP
ändern muss.

## Fehlersuche

Die Lessons-Learned-Seite des Blueprints listet jeden Fehler samt Symptom, etwa den
Webhook, der stumm in den Timeout läuft (Firewall), den Container, der keinen
Raw-ICMP-Socket öffnen kann, und das NAS, das sich selbst gesperrt hat.

## Was fehlt noch

Anmeldung pro Person am Bildschirm (entworfen als NFC-Chip zum Antippen), Aufgaben in
der Oberfläche bearbeiten, ein Geheimnis-Manager und Tests. Besser, das offen zu
sagen, als dich etwas verlassen zu lassen, das es nicht gibt.

## Den Bauplan holen

Architektur, Design-System, Hardware-Notizen, Lessons Learned, alle sieben Prompts
und ein Ordner `reference/` mit den Pi-Skripten (Kiosk-Start, Bewegungs-Dienst,
systemd-Units), dem API-Vertrag, der Farbpaletten-Datei und einem erfundenen
Demo-Haushalt als Testdaten: <https://github.com/realitytoday/home-information-screen-blueprint>

*Die englische Version dieser Anleitung steht auf der Begleitseite.*
