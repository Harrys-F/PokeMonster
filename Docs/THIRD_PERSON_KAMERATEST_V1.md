# Umschaltbare Third-Person-Kamera V1

Stand: 01.11.2026. Ausgangscommit `bca21ef1`. Die vorhandene Installation unter `UE_5.8` meldet tatsächlich **5.8.4, CL58902052** (`Engine/Build/Build.version` und Laufzeitlog), macOS/Metal. Die Projektanweisung nennt noch 5.8.2; keine Engine installiert, ersetzt oder umkonfiguriert. Zusätzlicher reversibler Testmodus auf ausdrücklichen Auftrag; Standardperspektive bleibt Kamera B (2,5D).

## Bedienung

In der Unreal-Konsole während eines aktiven Spiels (PIE oder separater Spielprozess):

```text
pm.Camera ThirdPerson
pm.Camera Status
pm.Camera 2D
```

Die Ausgabe lautet `PM_CAMERA ThirdPerson` bzw. `PM_CAMERA 2.5D`. Ungültige Argumente ändern nichts. Die Umschaltung verwendet denselben Pawn und verändert seine Position nicht. Jeder neu erzeugte Pawn beginnt in 2,5D, auch nach einem echten Mapwechsel oder Prozessneustart. Save/Load innerhalb derselben Welt erhält den laufenden Modus; es gibt kein neues SaveGame-Feld.

Third Person: WASD relativ zur horizontalen Kameraausrichtung, Maus für Orbit, Shift für vorhandenen Sprint, Mausrad für Abstand. W vorwärts, S zurück, A/D seitwärts. Die vorhandene Meshy-Präsentation dreht die Figur weich in Bewegungsrichtung. Die Kamera kann unabhängig um die stehende Figur gedreht werden. Diagonale Eingaben bleiben auf Einheitslänge begrenzt. Menü-, Dialog-, Kampf- und Entwicklungssteuerung bleibt beim vorhandenen Controller; diese Oberflächen behalten ihre eigene Darstellung. Nach der Freigabe ihrer Eingabesperre wird der Mausblick wieder übernommen.

`pm.Camera 2D` aktiviert wieder die ursprüngliche FollowCamera und den bisherigen Bewegungsbezug. Die ursprünglichen Einstellungen werden nie als Third-Person-Einstellungen wiederverwendet oder überschrieben. Keine Mapneuladung beim Umschalten. Wiederholtes Aktivieren desselben Modus ist wirkungslos.

## Einstellungen und technische Änderung

| Einstellung | Third Person |
|---|---:|
| Abstand / Neustart eines Modus | 350 cm |
| Höhe des Drehpunkts ab Kapselunterkante | 120 cm |
| Initialer Pitch | −12° |
| Vertikale Begrenzung | −65° bis +5° |
| FOV | 75° |
| Zoom | 200–600 cm, 35 cm je Mausradeinheit |
| Maussensitivität | 0,12° je Deltaeinheit |
| Kamerakollision | SpringArm, Probe 12 cm, Camera-Kanal |
| Positionsnachlauf | vorhandene SpringArm-Mechanik, Geschwindigkeit 12, Substepping |

Höhe, Standard-/Mindest-/Höchstabstand, FOV und Empfindlichkeit sind am bestehenden Character als Blueprint-Eigenschaften `PokeMonster|Camera` einstellbar. Die anfängliche horizontale Ausrichtung folgt der aktuellen Weltblickrichtung der Figur, sodass die Kamera hinter ihr startet. Der Weltblick wird dabei erhalten; Orbit allein dreht das Modell nicht mit.

Unveränderte 2,5D-Kamera: Arm 2850 cm, Pitch −50°, Yaw −45°, TargetOffset Z 35 cm, FOV 35°. Die vorhandene Innenraumkamera, ihre Übergänge und Bewegungsbasis bleiben erhalten. Im Third-Person-Modus wird deren feste POV nur übergangen; Gebäudeeintritt, Cutaway und Relokation bleiben die bestehenden Systeme. Beim Rückschalten im Innenraum greift die bisherige Innenraumdarstellung.

Ergänzt wurden eine SpringArm- und eine CameraComponent am bestehenden Character, zwei Enhanced-Input-Aktionen (Maus/Zoom) und eine zentrale Modusumschaltung in `PokeMonsterPlayerCamera.cpp`. Kein zusätzlicher CameraActor, Player oder KI-Controller. Der neue Arm tickt nur im aktiven Third-Person-Modus. Der vorhandene Character-Tick wird in diesem Modus für Präsentation und Rückkehr aus UI-Sperren verwendet. Die originale Eingabebelegung bleibt erhalten; der Foundation-Test berücksichtigt nun 21 statt 19 Mappings.

Keine Änderungen an Renderingprofilen, Weltuhr, KI, Speicherschema, Pokémon-Assets, Animationen oder Maps. Die zuvor vorhandene lokale Änderung in `Config/DefaultEngine.ini` ist unverändert und gehört nicht zu diesem Auftrag/Commit.

## Technische Tests

- Finaler Editor-Build `Saved/ProjectRefinement/ThirdPersonV1/Build06/Result.json`: Exit 0, 7,67 s.
- Vollständige finale Automation `ThirdPersonV1/Automation04`: **315 erfolgreich, 0 Warnungstests, 0 Fehler, 0 übersprungen; Engine Exit 0, strenger Wrapper Exit 0**, 42,82 s. Zuvor bereits Automation03 ebenfalls 315/315, streng Exit 0.
- Neuer Test `PokeMonster.Player.ThirdPersonCamera`: zehn Umschaltungen, idempotente Aktivierung, Start hinter der Blickrichtung, unveränderte Weltblickrichtung, vertikale Grenze, normale diagonale Eingabestärke, kamerarelatives Vorwärts, Eingabesperre sowie unveränderte Originalkamera und Position.
- Vorläufe offen ausgewiesen: Build02 scheiterte an einer mehrdeutigen numerischen Testüberladung (korrigiert). Automation01 lief dadurch nicht gegen den fertigen Teststand und ist kein Abnahmenachweis. Automation02: 314/315, streng Exit 1 wegen der alten 19-Mappings-Erwartung; korrigiert und vollständig wiederholt. Keine Fehler oder Warnungen unterdrückt.

## Separater Spielprozess und Save/Load

Finaler tatsächlicher Gameplaydurchlauf `Saved/ProjectRefinement/EvolutionV3/ThirdPersonNative03`: **62 Schritte bestanden**, Engine Exit 0. Ausschließlich eigener UserDir und kopierter QA-Spielstand, keine Nutzerspeicherdatei verwendet.

Nachgewiesen: frischer Start in 2,5D; beide Konsolenmodi; Enhanced-Input-Mausdrehung; physische Characterbewegung über vorhandene InputAction; zehn echte Konsolen-Rundwechsel ohne Positions-/Kameradrift. Danach im Third-Person-Modus die normale Karpador→Garados-Entwicklung mit Angebot, Abbruch während der Sequenz, erneutem Levelangebot und vollständiger Enthüllung. Persönliche Identität, Erfahrung, Status, HP-Differenz, Attackenrepertoire und AP sowie die Reserveinstanz bleiben erhalten. Isoliertes Save/Load vor/nach Entwicklung; Begleiter aktualisiert sein Modell; Besuch und Rückkehr aus dem bestehenden Modelltestgelände.

Anschließend tatsächliche Interaktion mit einem natürlichen Wild-Pokémon, ClassicBattle, reguläre schädigende Attacke mit exakt einem AP-Verbrauch, MasterBall-Fang, zusätzliche individuelle Teaminstanz, Rückkehr des Begleiters und vollständiges Save/Load des Teams. Keine zweite Kampf-/Entwicklungslogik.

Die Laufzeitprüfung bestätigte unverändert Software-Lumen/IFG (`r.Lumen.HardwareRayTracing=0`, `r.Lumen.FinalGatherMethod=0`), TAAU=1, ScreenPercentage=75, VSM-Strahlen=4 auf VisualV2. QHD-Aufnahmen sind 2560×1440. Keine Performanceoptimierung oder neue FPS-Zusage Bestandteil dieses Auftrags.

Der erste native Vorlauf endete geordnet nach einem Python-Prüfwerkzeugfehler: Deferred-Actor-Spawn ist dort nicht veröffentlicht. Die Kollisionsprüfung wurde deshalb mit dem bestehenden PIE-Prüfhelfer vorbereitet. Kein Produktionsfehler und keine Änderung der Engine dafür. Alle Vorläufe bleiben unter Saved nachvollziehbar.

## PIE, Map Checks und Neustart

- **PIE-Fußlauf bestanden:** `Saved/ProjectRefinement/ThirdPersonV1/PIEWalk02/Result.json`, 102,27 s, 16.505,96 cm (ca.165,06 m) tatsächlich zurückgelegter Bewegung, nach initialem kontrolliertem Startpunkt. Vorhandenes Enhanced Input statt direkter Positionsfortschreibung. Dorfwege, Heilhausvorplatz, Gebäudeeintritt über den vorhandenen Übergang, Innenraum, Heilerinnendialog über normale Interaktion, Gebäudeausgang, Nordwald, Waldrand, Waldweg und Rückweg. Sprint zeigt 315 cm/s, reguläres Gehen 210 cm/s. Große Innenraumrelokation wird nicht als gelaufene Distanz mitgezählt.
- **Physische Kamera-Kollisionsprobe bestanden:** bestehender `PokeMonsterCreaturePolishLibrary.spawn_review_actor` erzeugt ausschließlich im PIE einen transienten Blocker; SpringArm meldet tatsächlich angewendete Kollisionskorrektur. Eigenen Blocker unmittelbar entfernt, keine Mapänderung.
- **Zusätzliche Eingabeprüfung bestanden:** `PIEInput.json`: Mausrad über die echte InputAction auf 200 und 600 cm begrenzt; Menü sperrt Eingaben und zeigt Cursor, Schließen kehrt zu verborgenem Cursor und Third-Person-Mausblick zurück.
- **Bach/Teich bestanden:** `PIEAreas03/Result.json`, 18,16 s und weitere17,03 m regulärer Bewegung. Bachbrücke einschließlich Ein-/Austritt gelaufen; Teichrand nach gesondertem kontrolliertem Ausgangspunkt geprüft und beide Perspektiven aufgenommen. Keine Behauptung eines lückenlosen Fußlaufs über die gesamte Map.
- **PIE-Menü-Save/Load bestanden:** eigener Slot `PokeMonster_SaveV2_Test_ThirdPersonV1` im eigenen Editor-UserDir. Exakte Teamfelder und Spielerposition erhalten, Modus bleibt Third Person. Normale Rückkehr zu 2,5D und Statusausgabe geprüft. Keine Verwendung von Nutzerspielständen.
- **Frischer Prozess + echte Mapwechsel bestanden:** `Saved/ProjectRefinement/EvolutionV3/ThirdPersonRestart03/Result.json`, 22,92 s. Exaktes entwickeltes/gefangenes Testteam nach Neustart geladen; Start2,5D, ThirdPerson aktiviert; tatsächlicher Wechsel VisualV2→Dev_TestMap→VisualV2. Neue Pawns starten2,5D, Konsolenumschaltung bleibt funktionsfähig, Team und fortlaufende zentrale Weltzeit erhalten. Grafikprofil C bleibt erhalten. Die bestehende VSM4-Ausnahme gilt nur auf VisualV2, dazwischen auf Dev_TestMap unverändert8; nach Rückkehr wieder4.
- **Zwölf Map Checks bestanden:** `ThirdPersonV1/MapChecks.json` und die zwölf `THIRD_PERSON_MAPCHECK_BEGIN/END`-Abschnitte in `Editor01/Engine.log`. Jeweils0 Fehler/0 Warnungen, keine Map gespeichert. Alle zwölf vorhandenen Maps einschließlich der geschützten Westland-/Biom-Maps lediglich geladen/geprüft, danach VisualV2 wiederhergestellt.
- Eigener Editor PID7836 regulär beendet, keine ungespeicherten Maps/Assets, ursprüngliche Editoroption wiederhergestellt. Zwei erfolgreiche PIE-Start/Stopp-Zyklen (erster abgebrochener Prüfskript-Vorlauf und finaler Lauf) sowie mehrere geordnet beendete native Prozesse; kein Stillstand/Force Quit.

Auch Prüfskriptfehler bleiben ausgewiesen: PIE-Vorlauf verwendete den falschen Namen `SprintAction` statt bestehendem `SprintHoldAction`, danach neue isolierte Sitzung vollständig bestanden. Zwei Neustart-Vorläufe hatten unzutreffende Annahmen zu map-spezifischen VSM-Strahlen bzw. zu nur in PIE verfügbaren Zeit-Debugbefehlen. Prüfungen anhand der vorhandenen Architektur korrigiert; keine Produktionsfunktion dafür umgebaut.

### Warnungen getrennt von Testergebnissen

Finale Automation: keine Warnungstests, strenger Exit0. Das bedeutet nicht, dass jede Editor-Startmeldung warnungsfrei ist. Bereits im vorigen Garados-Prüflog vorhandene Startmeldungen `UnifiedErrorTest` und `LogAutomationTest: Condition failed` erscheinen vor Engine-Initialisierung erneut; die vollständigen tatsächlichen PokeMonster-Testergebnisse stehen separat im Automation-JSON. Zudem bekannte Python-Namenskollision `bInformation/Information`, Plugin-Lizenzhinweis, Layoutmigration, eine Console-Lookup-Performancewarnung sowie ein ausstehender Epic-Telemetrie-HTTP-Aufruf beim geordneten Editorende. Keine neue schwerwiegende Kameraregression oder Absturz beobachtet. Die externe iOS-Helfermeldung `idevice_id: Bad CPU type in executable` wurde in diesen finalen Logs nicht beobachtet; keine iOS-/Engine-Reparatur Bestandteil dieses Auftrags.

## Echte Aufnahmen und visuelle Grenzen

Die Aufnahmen stammen direkt aus dem Spiel, ohne generierte Bilder:

- `Saved/ProjectRefinement/EvolutionV3/ThirdPersonNative03/Camera_2D.png`
- `Saved/ProjectRefinement/EvolutionV3/ThirdPersonNative03/Camera_ThirdPerson.png`
- Entwicklungs-/Abbruchaufnahmen desselben Durchlaufs als zusätzliche Regression.
- `Saved/ProjectRefinement/ThirdPersonV1/PIEWalk02/Start_2D.png`, `Start_ThirdPerson.png`, `Return_2D.png`
- `Saved/ProjectRefinement/ThirdPersonV1/PIEWalk02/Heilhaus_ThirdPerson.png`, `Interior_ThirdPerson.png`, `Interior_2D.png`, `Wald_ThirdPerson.png`, `Waldweg_ThirdPerson.png`, `CollisionProbe.png`
- `Saved/ProjectRefinement/ThirdPersonV1/PIEAreas03/BachBridge_ThirdPerson.png`, `Teich_ThirdPerson.png`, `Teich_2D.png`

Alle genannten Aufnahmen2560×1440. Visuell geprüft wurden insbesondere die Rückansicht beim Aktivieren, Wald, Brücke und Innenraum. Im Innenraum zeigt die bestehende Cutaway-Technik den offenen oberen Raumabschluss. Sehr große Begleiter wie Garados können das Bild dort erheblich überdecken; Orbit/Zoom ermöglichen eine andere Sicht, aber es gibt keine neue automatische Ausblendung oder Größenanpassung des Begleiters. Dies bleibt eine ausdrücklich dokumentierte visuelle Grenze des Testmodus.

Die niedrige Perspektive zeigt bisher verdeckte Kulissen: offene Map-/Himmelsränder, vereinfachte Gebäudeseiten, einzelne flache/billboardartige Dekorationen und bislang unauffällige technische Geometrie. Das ist dokumentiert, nicht durch einen Landschafts- oder Assetumbau verdeckt. Die bestehende Welt wurde für eine schräge 2,5D-Kamera gestaltet; keine endgültige visuelle Third-Person-Abnahme behauptet. Kleine Pflanzen besitzen teils keine Kamerakollision; die Probe reagiert auf tatsächlich blockierende Kollisionsgeometrie.

Die vorhandenen Controllerbewegungs-/Menübindungen sind unverändert. Eine zusätzliche rechte-Stick-Orbitsteuerung ist nicht implementiert; angefordert und geprüft ist Mausorbit. Keine neue physische Controllerabnahme behauptet. Die Software-Automation umfasst die vorhandenen Switch-Pro-Tests.

## Projektschutz und Git

Prüfsummenvergleich gegen den vorab erfassten Arbeitsstand: **6014 versionierte Dateien geprüft**, ausschließlich die vorgesehenen eigenen Quellen/Entscheidungsnotiz verändert; **639 bereits vorhandene Save-Dateien unverändert**. Originalmodelle, alle Maps und bestehende lokale Engine-Konfiguration unverändert. Neue Testspielstände liegen ausschließlich in eigenen QA-UserDirs. 34 geschützte unversionierte Dateien bleiben außerhalb des Commits. Keine Programme zwangsbeendet, keine neuen Maps, Projektkopien oder Worktrees.

Gezielt zu sichern sind dieser Bericht, die Entscheidungsnotiz, Character-Header/-Quelle, die neue Kameradatei, der neue Kameratest und die angepasste Mapping-Erwartung. Kontrollmedien und Testspielstände unter Saved werden nicht committed. Commit-/Remote-/LFS-Ergebnis wird nach erfolgreicher Endprüfung im Chat mitgeteilt und ist über Git nachvollziehbar.
