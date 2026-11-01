# Third Person V2 – Standardkamera und Gamepad-Steuerung

Stand01.11.2026, Ausgangscommit `ec06f268`, vorhandene Engineinstallation `UE_5.8` meldet5.8.4/CL58902052. Keine Engineänderung. Die Projektanweisung nennt noch5.8.2. Neue Standardperspektive ausdrücklich vom Projektinhaber beauftragt; die Standardentscheidung des V1-Testmodus ist damit ersetzt.

## Standard und Umschaltung

Die bereits vorhandene Third-Person-Kamera wird am bestehenden Player beim tatsächlichen BeginPlay aktiviert. Das gilt für PIE, separaten Development-Spielprozess, neue Sitzung und neu erzeugte Pawns nach Mapwechsel. Die vorhandene Spieler-Synchronisation nach regulärem Laden aktiviert sie ebenfalls. Es gibt kein zusätzliches Save-Feld und keine neue Kameraarchitektur.

```text
pm.Camera ThirdPerson
pm.Camera 2D
pm.Camera Status
```

Alle drei Befehle bleiben erhalten. `2D` gilt für den aktuellen laufenden Pawn bis zur nächsten expliziten Umschaltung, regulären Wiederherstellung eines Spielstands oder einem Neustart/Mapwechsel. Laden stellt die neue Standardperspektive wieder her. Ein Moduswechsel selbst lädt keine Map neu und versetzt die Figur nicht. Die originale 2,5D-Kamera samt raumfester Innenkamera und ihren bestehenden Einstellungen bleibt vollständig erhalten.

Third Person behält350cm Arm,120cm Drehpunkt über der Kapselunterkante,−12° Startpitch,75° FOV,200–600cm Zoom,12cm Kollisionsprobe und bestehenden Positionsnachlauf. Kein automatisches Drehen der Kamera hinter die laufende Figur.

## Belegung und Empfindlichkeit

| Eingabe | Wirkung |
|---|---|
| Linker Stick | Bewegung in alle Richtungen, normierte Diagonalen |
| Rechter Stick | Unabhängiger Kameraorbit, oben hebt den Blick, unten senkt ihn |
| L3 | Vorhandene Sprint-Umschaltung, unverändert |
| WASD / Pfeiltasten | Bisherige kamerabezogene Tastaturbewegung |
| Maus | Bisheriger deltabasierter Kameraorbit |
| Shift | Bestehender gehaltener Sprint |
| Mausrad | Vorhandener Zoom200–600cm |
| B / A, X, Plus, D-Pad, L/R | Bestehende Bestätigungs-/Abbruch-/Menü-/Navigationsbelegung unverändert |

Rechter Stick: **120°/s horizontal**, **90°/s vertikal**, radiale Deadzone**0,15**, vertikaler Winkel−65° bis+5°. Keine invertierten Stickachsen. Die radiale Ausgabe wird nach der Deadzone kontinuierlich von0 bis1 skaliert, ohne gespeicherte Drehgeschwindigkeit oder Nachlauf bei Neutralstellung. Die Drehung verwendet DeltaSeconds statt Grad pro Inputereignis. Die vorhandene Kamera folgt weiterhin mit SpringArm-Lag; kein zweites Kameraticksystem.

Einstellbar am Character unter `PokeMonster|Camera|Gamepad`: `GamepadCameraYawSpeed`, `GamepadCameraPitchSpeed`, `GamepadCameraDeadZone`, `GamepadDirectionChangeDegrees` (Standard5°). Die linke radiale0,25-Deadzone aus der bestehenden Belegung bleibt erhalten. Rechter Stick verwendet die rohe Enhanced-Input-Achse und genau eine eigene radiale Deadzone; keine zusätzliche linke Deadzone auf diese Kameraaktion übertragen.

### Unabhängige Laufrichtung

Beim Ansetzen des linken Sticks wird dessen Bewegungsbasis aus der aktuellen horizontalen Kameraausrichtung übernommen. Solange dieselbe Stickrichtung gehalten wird, bleibt diese Weltbewegungsbasis während des Umsehens erhalten. Die Kamera kann unabhängig nach links/rechts gedreht werden, ohne die Figur mitzuziehen. Neutralstellung oder eine Richtungsänderung ab5° übernimmt wieder die aktuelle Kamerabasis. Änderungen nur der Stickstärke lösen keinen Richtungswechsel aus. Diese Toleranz verhindert eine Neuausrichtung durch geringes Analogzittern.

Maus-/Tastaturbewegung behält ihr bisheriges Verhalten. Ein Maus-/Tastaturwechsel löst die Stickbasis. Die vorhandene Meshy-Präsentation dreht die Figur weich zur tatsächlichen Weltbewegung; Kamera und Controllerrotation treiben keine zusätzliche Figurdrehung an.

## Technische Integration

- Bestehender Player, MappingContext und Bewegungsfunktion bleiben zuständig. `MoveAction` bleibt für Tastatur/Pfeile verfügbar. Der bestehende linke Stick-Key wird mit unveränderter radialer Deadzone an `GamepadMoveAction` gebunden; beide Quellen rufen dieselbe `ApplyMoveInput`-Funktion auf. Die Quellen sind getrennt, damit nur der Stick seine Weltbewegungsbasis beim Umsehen hält. Keine zweite Bewegung oder Spielfigur.
- Neue `GamepadLookAction` für `Gamepad_Right2D`; die vorhandene Mausaktion bleibt getrennt, weil Delta und Grad/Sekunde verschiedene Einheiten sind. Keine doppelte Verarbeitung derselben Stickachse. Insgesamt22 statt21 Mappings; Foundation-/Switch-Pro-Tests entsprechend angepasst.
- Bestehende Eingabesperre blockiert Bewegung und Kamera in Menüs, Dialogen, Kampf und Entwicklung. Eine Sperre verwirft die temporäre Stickbewegungsbasis. Beim Schließen einer Oberfläche übernimmt der bestehende Third-Person-Mechanismus wieder den Mausblick.
- `SynchronizeRestoredPlayer` ergänzt ausschließlich einen Aufruf der vorhandenen Kameramodusfunktion. Save-Schema, Position/Blickrichtung, Team, AP, Weltuhr und andere Daten bleiben unverändert. Keine Änderung von Nutzerspielständen.

## Build und Automation

- `Saved/ProjectRefinement/ThirdPersonV2/Build01/Result.json`: Editor-Build **Exit0**,65,80s.
- `ThirdPersonV2/Automation02`: **316 erfolgreich,0 Warnungstests,0 fehlgeschlagen,0 übersprungen; Engine Exit0 und strenger QA-Wrapper Exit0**,42,57s. Vollständiger vorhandener QA-Vertrag mit ausdrücklich isoliertem UserDir statt Nutzerspeicher.
- Neuer Test `PokeMonster.Player.ThirdPersonDefaultAndGamepad`: tatsächliches BeginPlay mit aktivem Third Person; linke/rechte Stick- und Mausbelegung; kein Drift bei neutralen Werten und radialer Deadzone;120°/s bei30 und120 Aktualisierungen/s; nicht invertiertes vertikales90°/s; Winkelgrenzen; gleichzeitiger freier Orbit bei erhaltener Weltbewegung; Neuausrichtung nach Loslassen; normierte Diagonalen; Eingabesperren; rechter Stick wirkungslos im2D-Modus; Standard nach bestehender Lade-Synchronisation; Tastatur bleibt kamerabezogen. Die315 bisherigen Tests wurden vollständig mit ausgeführt.
- Vorlauf `Automation01`:316 funktional bestanden, davon ein Warnungstest; **strenger Exit1, nicht vollständig bestanden**. Im bestehenden NPC-Test HTTP-Timeout zu `https://www.google.com/generate_204`. Keine Warnung unterdrückt; einmaliger vollständiger Wiederholungslauf oben bestanden.

## Tatsächliche Spielprüfungen

Separater Development-Spielprozess, vollständiger finaler Lauf `Saved/ProjectRefinement/EvolutionV3/ThirdPersonV2Native01`: **67 Schritte bestanden**, Engine Exit0,103,44s. Ausschließlich kopierte QA-Fixture im eigenen UserDir.

- Automatischer Third-Person-Start ohne Kamerabefehl; originale2D-Ansicht weiterhin explizit erreichbar; zehn Konsolen-Rundwechsel ohne Positions-/Kameradrift.
- Mausorbit und physische Characterbewegung über vorhandenes Enhanced Input.
- **Simulierte Sticks gleichzeitig:** reale Bewegung761,39cm, unabhängige Kameradrehung121,98°, beibehaltene Weltbewegungsbasis; vorhandener L3-Sprint315cm/s. Keine synthetische Änderung der Figurposition zur Erfüllung dieser Distanz; kontrollierter Ausgangspunkt vor dem Test gesondert gesetzt.
- Bestehende Karpador→Garados-Entwicklung mit Bestätigung, Abbruch, erneutem Angebot und vollständigem Abschluss; individuelle Identität, AP, Repertoire, Status, HP-Differenz und Reserveinstanz erhalten. Begleiter und Save/Load vor/nach Entwicklung geprüft.
- Reguläre Begegnung mit natürlichem Wild-Pokémon, ClassicBattle, schädigende Attacke mit genau einem AP-Verbrauch, MasterBall-Fang, neues individuelles Teammitglied, Rückkehr des Begleiters und vollständiges Team-Save/Load.
- Frischer Prozess `ThirdPersonV2Restart01`: **4 Prüfphasen bestanden**,22,38s. Entwickeltes/gefangenes Team exakt wiederhergestellt. Tatsächlicher Wechsel VisualV2→Dev_TestMap→VisualV2; neue Pawns jeweils Third Person, beide Konsolenmodi verwendbar. Team und fortlaufende Weltzeit erhalten.
- Grafikprofil unverändert: Software-Lumen/IFG0/0, ScreenPercentage75, TAAU1, VisualV2-VSM4. Bestehende map-spezifische Ausnahme bedeutet auf Dev_TestMap8, nach Rückkehr wieder4. Keine Renderingkonfiguration geändert.

### Echte PIE-Regression

- `ThirdPersonV2/PIEWalk02/Result.json`: **bestanden**,95,95s,165,15m tatsächliche Bewegung nach kontrolliertem Ausgangspunkt. Dorfwege, Heilhausvorplatz, Gebäudeeintritt, Innenraum und Heilerinnendialog über normale Interaktion, Rückweg durch Nordwald, Waldrand und Waldweg. Sprint315cm/s und reguläres Gehen210cm/s. Reale SpringArm-Kollisionskorrektur gegen einen transienten Prüfblocker bestätigt; eigenen Blocker entfernt. Keine Mapänderung.
- Menü-Save/Load ausdrücklich auch aus manuell gewähltem2D geprüft: eigener Testspielstand gespeichert, `pm.Camera 2D`, regulär geladen, danach Third Person mit identischer Position und vollständigen Teamfeldern. Slot `PokeMonster_SaveV2_Test_ThirdPersonV2` ausschließlich im eigenen Editor-UserDir. Keine Nutzerspeicherdatei verwendet.
- `ThirdPersonV2/PIEInput.json`: **bestanden**, Mausradgrenzen200/600cm und Rückkehr des Mausblicks nach Schließen des vorhandenen Menüs.
- `ThirdPersonV2/PIEAreas03/Result.json`: **bestanden**,17,45s, weitere16,90m Bewegung. Vorhandene Bachbrücke überquert; Teichrand nach separat gesetztem kontrolliertem Ausgangspunkt geprüft. Beide Kameraperspektiven aufgenommen. Kein lückenloser Fußlauf über jeden Bereich der Map behauptet.
- `ThirdPersonV2/PIEDefault.json`: **5 Prüfungen bestanden** in einer zweiten frischen PIE-Sitzung, vor jedem Lade-/Kamerabefehl Third Person aktiv. Simuliertes radiales Stickrauschen(.1,.1) erzeugt keine Kameradrift; rechte Y-Achse hebt den Blick; gleichzeitige Sticks erzeugen157,66cm physische Bewegung und59,66° Orbit mit erhaltener Weltbewegungsbasis. Rechter Stick verändert die erhaltene2D-Kamera nicht. Ein reiner Prüfskript-Pfadvergleich war zunächst relativ statt absolut; vor jeder Spielaktion korrigiert, dann derselbe unveränderte frische Start geprüft. Kein Produktionsfehler.

### Map Checks und Stabilität

**Zwölf Map Checks bestanden**, jeweils0 Fehler und0 Warnungen. `ThirdPersonV2/MapChecks.json` enthält sämtliche vorhandenen Maps; die zwölf `THIRD_PERSON_V2_MAPCHECK_BEGIN/END`-Abschnitte in `Editor01/Engine.log` enthalten die tatsächlichen Unreal-Ergebnisse. Geschützte Westland-/Biom-Maps nur geladen und geprüft, nicht gespeichert; anschließend VisualV2 wiederhergestellt. Keine schmutzigen Map-/Content-Pakete.

Zwei vollständige eigene PIE-Start/Stopp-Zyklen sowie zwei separate native Spielprozesse geordnet beendet. Eigenen Prüfeditor PID11492 nach Wiederherstellung der ursprünglichen Editoroption und Prüfung auf ungespeicherte Inhalte regulär geschlossen. Kein Stillstand, Force Quit oder Verwerfen von Nutzeränderungen.

## Echte Aufnahmen

QHD2560×1440, direkt aus Unreal, keine generierten Bilder:

- `Saved/ProjectRefinement/EvolutionV3/ThirdPersonV2Native01/Camera_DefaultThirdPerson.png`: frischer Spielstart ohne Kamerabefehl, visuell geprüft.
- Im selben Verzeichnis `Camera_2D.png`, `Camera_ThirdPerson.png` sowie bestehende Entwicklungs-/Abbruchaufnahmen als zusätzliche Regression.
- `Saved/ProjectRefinement/ThirdPersonV2/PIE_DefaultThirdPerson.png`: zweite frische PIE-Sitzung vor jeglichem Lade-/Kamerabefehl.
- `ThirdPersonV2/PIEWalk02/`: `Start_2D.png`, `Start_ThirdPerson.png`, `Heilhaus_ThirdPerson.png`, `Interior_ThirdPerson.png`, `Interior_2D.png`, `Wald_ThirdPerson.png`, `Waldweg_ThirdPerson.png`, `CollisionProbe.png`, `Return_2D.png`.
- `ThirdPersonV2/PIEAreas03/`: `BachBridge_ThirdPerson.png`, `Teich_ThirdPerson.png`, `Teich_2D.png`. Diese Pfade liegen sämtlich unter `Saved/ProjectRefinement/`.

## Hardwareprüfung und Einschränkungen

**Kein physischer Gamepad-Praxistest bestätigt.** Apples GameController-Framework meldete beim Start dieser Prüfung nach Geräteinitialisierung0 erkannte Controller (`ThirdPersonV2/ControllerProbe.json` und Abschlussprobe `ControllerProbeFinal.json`, jeweils0). Keine Kopplung, Treiberinstallation oder Systemänderung vorgenommen. Neue Stickfunktionen wurden automatisiert sowie durch simulierte Enhanced-Input-Aktionen im tatsächlich laufenden Spiel geprüft. Das ersetzt keine persönliche Prüfung der physischen Stickachsen und des tatsächlichen Controllergefühls. Die bestehenden Switch-Pro-UI-/Sprintsoftwaretests bleiben bestanden.

Die bekannten visuellen Grenzen von V1 bestehen: offene Kulissen-/Himmelsränder, bisher verdeckte Gebäudeseiten, flache Dekorationen, offener oberer Raumabschluss durch die vorhandene Innenraum-Cutaway-Technik. Große Begleiter wie Garados können aus der niedrigen Perspektive das Bild in engen Räumen verdecken. Keine Modelle skaliert/ersetzt, keine Welt dafür umgebaut. Keine neue visuelle Freigabe oder FPS-Verbesserung behauptet.

Externe/Engine-Startmeldungen werden getrennt von tatsächlichen Testergebnissen bewertet: bekannte UnifiedError-/Condition-failed-Startmeldungen, Python-Namenskollision, Plugin-/Layoutmeldungen und bereits im V1-Log vorhandener fehlender Engine-`PythonTestRunner`. Ein anfänglicher CharacterMovement-Warm-up-Hinweis im nativen Prozess betrifft einen langen Startframe. Keine dadurch ausgelöste neue Gameplay-/Kameraregression beobachtet. Tatsächliche PokeMonster-Testfehler:0. Die externe iOS-Helfermeldung `idevice_id: Bad CPU type in executable` wurde in den aktuellen abschließenden Logs nicht beobachtet; kein Engine-/iOS-Reparaturauftrag. Der erfolgreiche strenge QA-Exit0 bezieht sich auf den vollständigen Testbericht, nicht auf die Behauptung eines vollständig meldungsfreien Engine-Starts.

## Projektschutz und Sicherung

Ausgangsstand vor Änderung erfasst:6017 versionierte Dateien,651 vorhandene Save-Dateien und34 geschützte unversionierte Dateien. Endvergleich nach regulärem Editorende bestanden (`ThirdPersonV2/FinalProtectionCheck.json`): alle651 zuvor vorhandenen Save-Dateien unverändert, keine fehlende geschützte unversionierte Datei, beide Vollbackup-Verweise unverändert auf03492bd96b4dba44692f675c19d5f11abfa86b4b. Unter den6017 vorab erfassten versionierten Dateien ausschließlich die elf vorgesehenen eigenen Kamera-/Input-/Test- und Dokumentationsdateien geändert; hinzu kommen dieser Bericht und der neue Gamepadtest. Alle Maps, Assets, Originalquellen und die bereits vorhandene Nutzeränderung in DefaultEngine.ini entsprechen weiterhin dem Ausgangszustand. Nur notwendige Kamera-/Inputquellen, Tests und die wegen der ausdrücklich geänderten Standardperspektive betroffenen Projektdokumente sichern. Bestehende lokale Änderung in `Config/DefaultEngine.ini` bleibt außerhalb dieses Auftrags. Keine Maps, Assets, Originalquellen, Grafikprofile oder Nutzerspielstände bearbeiten; keine neuen Maps/Worktrees, keine destruktiven Git-Befehle, kein Force Quit.

Commit, tatsächlicher Remote- und LFS-Status werden nach bestandener Endprüfung im Chat mitgeteilt und sind über Git nachvollziehbar. Medien, große Messdaten, Testprogramme und QA-Spielstände unter Saved werden nicht committed.
