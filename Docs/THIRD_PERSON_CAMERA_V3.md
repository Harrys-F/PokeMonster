# Third-Person-Kamera V3 – feste Höhe und Neigung

Stand01.11.2026; Ausgangscommit `62ba032b`. Vorhandene Engineinstallation unter `UE_5.8` meldet5.8.4/CL58902052; Projektanweisung nennt noch5.8.2. Keine Engineänderung. Ausschließlich bestehende Kamera angepasst, keine neue Kameralösung.

## Neue Geometrie und Bedienung

| Einstellung | Wert |
|---|---:|
| Tatsächlich gemessene Kamerahöhe auf ebenem Boden | **172,15cm** |
| Feste Neigung der tatsächlichen Kamera | **−12°** |
| Standardabstand horizontal | **350cm** |
| SpringArm-Pitch | **0°** |
| Armhöhe ab Kapselunterkante | **170cm** |
| FOV | unverändert75° |
| Mausrad-Zoom | unverändert200–600cm |
| Horizontaler Stick | unverändert120°/s bei vollem Ausschlag |
| Vertikaler Stick / vertikale Maus | **ohne Wirkung** |
| Horizontaler Orbit |360°, normalisierter Yaw ohne Winkelanschlag |

Die frühere V2-Geometrie legte−12° auf den350cm langen Arm. Damit lag die Kamera zusätzlich `350·sin(12°)≈72,77cm` über dem Armursprung. Die Pivot-Höhe allein war deshalb keine Aussage über die tatsächliche Kamerahöhe.

V3 führt denselben Arm waagerecht und legt die feste Neigung ausschließlich auf dieselbe vorhandene CameraComponent. Beim Zoomen verändert sich nur die horizontale Entfernung. Kollisionsverkürzung bewegt die Kamera ebenfalls entlang dieses waagerechten Arms. Kein zusätzlicher Höhengewinn durch einen schrägen Arm. Der bestehende physikalische Bodenabstand der Kapsel erklärt die Differenz zwischen170cm ab Kapselunterkante und gemessenen172,15cm über dem Boden. Welt-/Figurmaßstab140cm unverändert.

`ThirdPersonPitch` ist eine vor Spielstart einstellbare, Blueprint-schreibgeschützte Kameraeinstellung, Standard−12°; es gibt keine vertikale Spielersteuerung mehr. Das bisherige vertikale Stickgeschwindigkeitsfeld entfällt. Bei jedem Aktivieren von Third Person werden Armhöhe, horizontaler Arm und feste Kameraneigung wiederhergestellt. Horizontale Eingaben setzen keinen variablen Pitch mehr.

Stick-Y wird **vor** dem horizontalen Deadzone-Test verworfen. Deshalb kann eine große vertikale Auslenkung auch kleine horizontale Werte innerhalb der0,15-Deadzone nicht aktivieren oder deren Drehgeschwindigkeit verändern. Die erhaltene Deadzone-Einstellung wird hier auf die horizontale Achse angewandt. Maus-Y wird ignoriert und löst die gehaltene Stickbewegungsbasis nicht. Maus-X behält die bisherige Empfindlichkeit0,12° je Deltaeinheit.

WASD, linker Stick, gehaltene Weltbewegungsbasis beim freien Umsehen, weiche Modelldrehung, Laufanimationen, Shift und L3 bleiben unverändert. Keine automatische Kameraausrichtung an der Laufrichtung. Kein zusätzlicher Tick und keine Rendering-/Performanceänderung.

## Standard und Befehle

Third Person bleibt Standard beim BeginPlay, nach regulärem Laden, Neustart und Mapwechsel. Keine neuen Save-Felder oder Änderungen der Spielstanddaten.

```text
pm.Camera ThirdPerson
pm.Camera 2D
pm.Camera Status
```

Die erhaltene2,5D-Kamera bleibt unverändert2850cm/−50°/FOV35°. Zurückwechseln aktiviert wieder das neue horizontale Rig mit fester−12° Kamera. Umschalten allein versetzt die Figur nicht und lädt keine Map neu.

## Technische Prüfung

- Editor-Build `Saved/ProjectRefinement/ThirdPersonV3/Build01/Result.json`: **Exit0**,28,59s.
- Vollständige relevante Automation `ThirdPersonV3/Automation01`: **317 erfolgreich,0 Warnungstests,0 Fehler,0 übersprungen; Engine Exit0, strenger QA-Wrapper Exit0**,79,56s. Die316 bisherigen Tests weiter ausgeführt und ihre inzwischen ausdrücklich ersetzten vertikalen Erwartungen angepasst.
- Neuer Test `PokeMonster.Player.ThirdPersonFixedHeightAndPitch`: tatsächliche Engine-Kamera-/Socketposition bei Standard und Zoomextremen; gleicher Pitch; reine Vertikale und horizontales Sub-Deadzone-Rauschen trotz voller Y-Auslenkung ohne Wirkung; horizontaler Umlauf erhält Pitch; nachgeführte Höhe statt global festem Z;2D-Rundwechsel stellt Rig wieder her. Für die exakte isolierte Geometrieprüfung sind Nachlauf und Kollision nur am Test-Pawn abgeschaltet; produktive Einstellungen bleiben aktiviert und werden in PIE gesondert geprüft.
- Bestehende Kameratests prüfen weiter zehn Moduswechsel, unveränderte2D-Kamera, Bewegungsnormierung,120°/s bei30/120 Updates/s, gleichzeitige Bewegung/Orbit, Eingabesperren und Standard nach Laden.

## Tatsächlicher separater Spielprozess

`Saved/ProjectRefinement/EvolutionV3/ThirdPersonV3Native01`: **68 Schritte bestanden**, Engine Exit0,104,41s. Ausschließlich eigenes UserDir mit kopiertem QA-Spielstand.

Tatsächlicher gerenderter Standpunkt über PlayerCameraManager vor jedem Moduswechsel gemessen:

- Kamera-Weltposition cm: `(-495.051731,-1638.697212,172.150002)`.
- Per vorhandener Visibility-LineTrace ermittelter Boden unter der Spielfigur: Z≈0cm.
- Kamera deshalb **172,150002cm über diesem Boden**, tatsächlicher Pitch **−12°**, Roll0°.

Die echte QHD-Spielaufnahme wurde angesehen: Die vollständige Spielfigur und der Weg sind aus dem neuen, niedrigeren Standpunkt erkennbar.350cm/−12° wurden deshalb als Ausgangswerte beibehalten; keine zusätzliche Variantenreihe oder Weltgestaltung.

Weitere bestandene Regression: frischer Third-Person-Start, explizites2D, zehn Konsolen-Rundwechsel ohne Drift/Versatz, Mausorbit, tatsächliche Characterbewegung über Enhanced Input, gleichzeitig simulierte Sticks und bestehender L3-Sprint315cm/s. Vorhandene Karpador→Garados-Entwicklung mit Abbruch/erneutem Angebot/vollständigem Abschluss, Erhalt individueller Daten/Repertoire/AP/Reserveinstanz, Begleiter und Modelltestgelände; normale Wildbegegnung, ClassicBattle, schädigende Attacke mit exakt einem AP, MasterBall-Fang, Rückkehr zur Welt und vollständiges Team-Save/Load.

Frischer Prozess `ThirdPersonV3Restart01`: **4 Prüfphasen bestanden**, tatsächlicher Wechsel VisualV2→Dev_TestMap→VisualV2, neue Pawns jeweils Third Person, beide Modi verfügbar; exakt gespeichertes entwickeltes/gefangenes Team und fortlaufende Weltzeit erhalten. Unverändertes Grafikprofil C: Software-Lumen/IFG0/0,75%,TAAU1,VSM4 auf VisualV2. Bestehende map-spezifische VSM-Ausnahme auf Dev_TestMap bleibt8.

## PIE-Höhen-, Kollisions- und Geländemessungen

Die ersten zehn Messprüfungen in `ThirdPersonV3/Geometry01/Result.json` bestätigten bei Maus-Y ±5000, Stick-Y ±1, horizontalem Orbit, Zoom200/600 und tatsächlich angewendeter SpringArm-Kollisionskorrektur jeweils **172,15cm** über dem ebenen Boden und **−12°** tatsächlichen View-Pitch. Dieser Vorlauf ist **nicht vollständig bestanden**: Die anschließende Rampenvorbereitung verwendete eine nicht veröffentlichte Python-Funktion `RestoreSavedFacing`. Transiente Prüfobjekte wurden entfernt; keine Produktionsdatei dafür geändert. Der korrigierte Gesamtlauf `ThirdPersonV3/Geometry02/Result.json` ist **vollständig bestanden**,12 Prüfungen,34,07s. In allen ebenen Messpunkten einschließlich Zoom200/600 und echter Kollisionskorrektur172,15cm/−12°. Vertikale Maus-/Stickbewegung ohne Änderung; voller horizontaler Stick mit gleichzeitig voller Y-Auslenkung dreht weiter horizontal, ohne zusätzlichen Pitch.

Der Rampentest verwendete ausschließlich ein mit dem vorhandenen PIE-Prüfwerkzeug erzeugtes **transientes** Cube-Rampencollider mit10° Neigung, keine vorhandene Landschaft verändert.33 Bewegungsstichproben: Pitch durchgehend exakt−12°, Kamera-Welt-Z stieg mit der Figur von172,15 auf318,24cm. Nach Stillstand Kamera-Z321,58cm, Boden unter der Figur149,14cm: Kamerahöhe dort172,43cm. Die Kamera stand dabei350cm hinter der Figur über dem tieferen Rampenteil (Boden dort87,43cm, eigene Bodenfreiheit234,15cm). Damit sind mitbewegte Figurenhöhe und Geländeabstand direkt unter der Kamera ausdrücklich getrennt; auf Steigungen wird keine überall identische Bodenfreiheit behauptet. Rampe und Kollisionsblocker wurden entfernt, Spielerposition wiederhergestellt.

Zusätzlicher zusammenhängender PIE-Fußlauf `ThirdPersonV3/PIEWalk02/Result.json`: **bestanden**,96,10s,164,89m tatsächliche Bewegung nach kontrolliertem Ausgangspunkt. Dorf, Heilhaus und bestehender Gebäudeübergang, normale Heilerinnen-Interaktion/Dialog, Rückkehr über Wald und Wege. Sprint315cm/s, Gehen210cm/s. Bestehende Kollisionsprobe reagiert tatsächlich auf blockierende Geometrie. Menü-Save/Load im eigenen Slot `PokeMonster_SaveV2_Test_ThirdPersonV3`: vollständige Teamfelder/Position erhalten; explizit von manuellem2D wieder zu Third Person geladen, tatsächlicher Pitch danach−12°. Kein Nutzerspielstand verwendet.

`ThirdPersonV3/PIEInput.json`: **bestanden**, Zoomgrenzen200/600cm, Mausrückkehr nach Menü. `PIEAreas03/Result.json`: **bestanden**,17,71s und weitere16,96m Bewegung über die vorhandene Bachbrücke und am Teichrand; für den Teich ein separat kontrollierter Ausgangspunkt. Keine lückenlose Begehung jedes Mapbereichs behauptet.

**Zwölf Map Checks bestanden**, jeweils0 Fehler/0 Warnungen. Tatsächliche Namen in `ThirdPersonV3/MapChecks.json`, Ergebnisse in den zwölf `THIRD_PERSON_V3_MAPCHECK_BEGIN/END`-Abschnitten in `Editor01/Engine.log`. Geschützte Westland-/Biom-Maps ausschließlich geladen/geprüft, keine Map gespeichert; VisualV2 anschließend wiederhergestellt. Eigene PIE-Sitzung und eigener Prüfeditor PID14719 nach Kontrolle auf ungespeicherte Pakete und Wiederherstellung der Editoroption regulär beendet. Zwei separate Spielprozesse ebenfalls geordnet beendet. Keine ungespeicherten Inhalte verworfen und kein Force Quit.

Höhenangaben werden getrennt nach Boden unter der Figur und Boden direkt unter der Kamera protokolliert. Auf Steigungen müssen diese Werte geometrisch nicht gleich sein: Die Kamera folgt der Figur mit dem vorhandenen Nachlauf; sie wird nicht auf ein globales Welt-Z oder per neuer Bodenregelung festgehalten. Der feste Blickwinkel wird dadurch nicht verändert.

## Echte Aufnahmen

- `Saved/ProjectRefinement/EvolutionV3/ThirdPersonV3Native01/Camera_DefaultThirdPerson.png`: frischer Spielstart, neue Perspektive, QHD2560×1440, visuell geprüft.
- Im selben Verzeichnis `Camera_2D.png`, `Camera_ThirdPerson.png` und bestehende Entwicklungs-/Abbruchbilder als zusätzliche Regression.
- `Saved/ProjectRefinement/ThirdPersonV3/Geometry02/NewPerspective.png`, `Collision.png`, `Slope.png`: tatsächliche PIE-Aufnahmen der normalen Ansicht und transienten Geometrieprüfungen.
- `ThirdPersonV3/PIEWalk02/`: `Start_ThirdPerson.png`, `Heilhaus_ThirdPerson.png`, `Interior_ThirdPerson.png`, `Interior_2D.png`, `Wald_ThirdPerson.png`, `Waldweg_ThirdPerson.png`, `Return_2D.png`.
- `ThirdPersonV3/PIEAreas03/`: `BachBridge_ThirdPerson.png`, `Teich_ThirdPerson.png`, `Teich_2D.png`. Diese Pfade liegen unter `Saved/ProjectRefinement/`. Keine generierten Bilder oder neuen Bildfolgen/Videos.

## Hardwarestatus, Warnungen und Grenzen

Apples GameController-Framework meldete0 erkannte Controller (`ThirdPersonV3/ControllerProbe.json`). **Keine neue physische Gamepadprüfung als bestanden ausgewiesen.** Sticktests sind ausdrücklich automatisiert bzw. simulierte Enhanced-Input-Eingaben im tatsächlichen Spiel. Die physische Achsen-/Bediengefühlprüfung bleibt Harry vorbehalten.

Die bekannten Kulissengrenzen und große, in engen Räumen sichtverdeckende Begleiter bleiben bestehen. Nahe Zoomstufen und physische Hindernisse können den Bildausschnitt stark verkürzen; keine Modelle/Geometrie für diesen Auftrag verändert. Die endgültige visuelle Bewertung erfolgt jetzt durch Harrys eigenen Test. Keine Performanceoptimierung oder FPS-Zusage.

Der strenge QA-Exit0 betrifft den vollständigen Testbericht, nicht einen vollständig meldungsfreien Engine-Start. Bereits bekannte Engine-/Plugin-Startmeldungen (UnifiedError/Condition failed, Python-Namenskollision, fehlender Engine-PythonTestRunner, Layout-/Pluginhinweise) getrennt von funktionalen PokeMonster-Testfehlern behandeln. Tatsächliche Testfehler0. Die externe iOS-Helfermeldung `idevice_id: Bad CPU type in executable` wurde in den aktuellen abschließenden Logs nicht beobachtet. Keine Engine-/iOS-Änderung.

## Projektschutz und Abschluss

Ausgangsstand erfasst:6019 versionierte Dateien,657 vorhandene Save-Dateien,34 geschützte unversionierte Dateien. Endvergleich nach regulärem Editorende **bestanden** (`ThirdPersonV3/FinalProtectionCheck.json`): alle657 zuvor vorhandenen Save-Dateien unverändert; alle34 geschützten unversionierten Dateien vorhanden; beide Vollbackup-Verweise unverändert auf03492bd96b4dba44692f675c19d5f11abfa86b4b. Unter6019 vorab erfassten versionierten Dateien ausschließlich die acht vorgesehenen Kamera-/Test-/Dokumentationsdateien geändert. Hinzu kommen nur dieser Bericht und der neue Rigtest. Alle Maps, Modelle, Originalquellen, Grafikprofile und die bestehende lokale Engine-Konfiguration entsprechen dem Ausgangszustand. Vorhandene lokale DefaultEngine.ini-Änderung außerhalb dieses Auftrags erhalten. Keine neuen Maps/Worktrees, keine destruktiven Git-Befehle, keine erzwungene Prozessbeendigung. Nur erforderliche Kameraquellen, Tests und wegen der ersetzten Vertikalsteuerung notwendige Dokumentation sichern; keine Medien oder QA-Spielstände committen.

Nach dieser technischen Prüfung und gezielten Git-Sicherung **keine weitere Kameraänderung**, bevor Harry die neue Perspektive selbst auf VisualV2 ausprobiert hat. Kein automatischer Folgeschritt zur Kulissen-, Begleiter- oder Kameraneugestaltung.
