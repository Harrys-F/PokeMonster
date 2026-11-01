# Garados Animation Polish V3

Stand: 01.11.2026. Projekt `/Users/harry/Developer/PokeMonster`, VisualV2. Ausgangsstand `f10dc77ff8131514c1633febd81d885b10e9d0ca`; Garados Water Movement V2 aus `bca21ef1` wird gezielt verfeinert. Keine neue KI, Map, Kamera, Geometrie oder Renderingkonfiguration. Die Buchenwald-Rücknahme bleibt erhalten. Die abschließende künstlerische Beurteilung erfolgt durch Harry im Spiel.

## Bestand und Schutz

Einzige ursprüngliche Modellquelle: Harrys `Art/Characters/Creatures/Incoming/Garados.glb`, SHA-256 `ce0661729d56dfa628a3232f4296bd5ae3bd51a914f417e8e82426e33133f5b9`. Originalquelle `Garados_Meshy_V1.blend` und bestehende technische Wasser-Ableitung `Garados_Water_V2.blend` bleiben unverändert. Letztere: SHA-256 `70a84ad317bbcf99bdc04ccd73033e17e9fb12acf89f4cfba5492567783c0990`.

V3 verwendet exakt das vorhandene WaterV2-SkeletalMesh und dessen Skeleton: 24.049 Vertices, 26.298 Dreiecke, 20 Wirbelsäulensegmente plus Kopf/Root. Keine Änderungen an Oberfläche, Ruhepose, Gewichten, UVs, Materialien oder Normalen. Der bisherige V2-Bericht beschreibt die schon damals vorgenommene horizontale Ableitung; V3 erzeugt keine weitere Modellform.

Die neue Arbeitsquelle `Art/Characters/Creatures/Garados/Source/Garados_Water_V3.blend` enthält ausschließlich zusätzliche Animationen. Sieben FBXs unter `Exports/WaterV3` enthalten nur Animation/Skeletonkanäle, keine neue Geometrie. Unreal importiert sie auf das **bestehende** WaterV2-Skeleton. Das einzige geänderte bestehende Content-Asset ist `MeshyV1/DA_Garados_Presentation`: sieben Wasser-Grundbindungen und drei visuelle Parameter. Alle sieben ursprünglichen Land-/Kampfclips und die vier WaterV2-Reaktionen Attack/Hit/Faint/Happy bleiben bytegleich.

## Veränderte Wasseranimationen

Alle sieben neuen Clips haben 2,8 s, 60-Hz-Sampling und 169 Schlüsselbilder einschließlich identischer Schleifen-Endpose. Die vorherige normale Wasserperiode betrug 1,6 s. Geometrie-/Rig-/Skin-/UV-/Material-Fingerabdruck vor/nach Animationserstellung identisch: `e2fcccbba88c3553d8a3ff771d635b675b35af3bfdc4584307adc5cb6dfa7ff7`.

| Clip | Relative Wellenstärke | Zweck |
|---|---:|---|
| SwimIdle | 0,10 | Ruhige horizontale Wasserhaltung |
| SwimSlow | 0,42 | Kleine, langsame Körperwellen |
| SwimNormal | 0,80 | Kraftvolle normale Fortbewegung |
| SwimFast | 1,12 | Stärkere Wellen bei höherer Geschwindigkeit |
| SwimTurnLeft / Right | 0,80 | Dezente Kurvenlage, Bank bis 4° im Quellclip |
| SwimObserve | 0,10 | Vorderkörper/Kopf angehoben, Hinterkörper im Wasser |

Die Welle läuft über 1,15 Phasenzyklen vom Vorderkörper zum Schwanz. Der Kopf bewegt sich zurückhaltend, die Amplitude nimmt nach hinten zu. Alle Wasser-Grundclips teilen eine normierte Phase im vorhandenen Animationsproxy; dadurch wechseln Idle, Geschwindigkeitsposen und Beobachtung nicht mehr zwischen gegeneinander laufenden Animationszeiten. Das vorhandene Ratenmapping bleibt geschwindigkeitsabhängig, im Wasser gedämpft und auf 0,45–1,35 begrenzt. Bei Referenzrate 1 dauert ein Zyklus 2,8 s.

## Verbesserte Übergänge

- Wasser-Bewegungsblend und Abspielrate: exponentielle Annäherung mit Zeitkonstante 0,55 s; Slow/Fast-Mischung 0,40 s. Framerateunabhängig und ohne Überschwingen. Landmischungen bleiben unverändert.
- Richtungswechsel: vorhandener Actor-/Bewegungsplaner bleibt bei 35°/s und 70°/s². Eine begrenzte visuelle Richtungshistorie mit 60-Hz-Abtastung lässt den Kopf führen und die 20 Körpersegmente zunehmend verzögert folgen; Schwanz bis 1,1 s, Korrektur höchstens 32°. Die Gelenkpositionen werden mit denselben Segmentlängen aufgebaut. Keine abrupte gleichzeitige Drehpose aller Segmente.
- Diese zusätzliche Richtungskorrektur ist datengetrieben opt-in (`SwimBodyFollowSeconds`, standardmäßig 0), nur bei Garados aktiviert und ausschließlich auf dem separaten Wasser-Rig ausgewertet. Beim Wechsel zu Land werden Historie und Korrekturen verworfen. Keine neuen Actor-Ticks/Controller/AnimBlueprints.
- Die vorhandenen Turn-Clips tragen nur noch bis 35 % bei, abhängig von Bewegung und Beobachtungsalpha. Beim Aufrichten wird die Kurvenlage weich zurückgenommen.
- Aufrichten/Absenken: 3,2-s-Verlauf mit Smoothstep und bestehenden 3 s Nachhaltezeit. Aufrichten erst unter 10,5 cm/s visueller Geschwindigkeit; der bestehende V2-Mechanismus reduziert das Schwimmtempo passend zur Haltung. Die eigentliche Erkennung von Observe/Alert/Warning/Curious/Social ist unverändert. Bei pausierter Weltuhr bleibt der Haltungsverlauf stehen.

Die vollständigen 1.183 Offline-Animationsframes bleiben innerhalb 370,05 cm horizontalem Radius. Die tatsächliche kombinierte Unreal-Skin-Auswertung während Geschwindigkeit, Kurve und Aufrichten erreichte 380,94 cm. Der vorhandene konservative Gelände-Freiraum bleibt **400 cm**. Das ist ein geprüfter endlicher Testumfang, kein mathematischer Beweis sämtlicher denkbarer Posen. Tatsächlich ausgewertete Kopfanhebung: 106,04 cm; Hinterkörper bleibt überwiegend unter Wasser. Navigation, Tiefgang 180 cm, Geländeprüfung und Fischkontakt wurden nicht geändert.

## Technische Tests

| Prüfung | Tatsächliches Ergebnis / Nachweis unter Saved/ProjectRefinement/GaradosPolishV3 |
|---|---|
| Finaler Editor-Build | Build04: Exit 0, 6,54 s; vorher Build01–03 ebenfalls erfolgreich |
| Vollständige finale Automation | AutomationFinal über den versionierten V3-Runner: 320/320 erfolgreich, 0 Warnungstests, 0 Fehler, 0 Skips; Engine Exit 0, strenger Wrapper Exit 0; 31,43 s. Automation02 zuvor ebenfalls 320/320 und Exit 0, 29,38 s |
| Neue Tests | 3: verzögerte Richtung/±180°/Pause/Frameraten; exponentielle Pose-Dämpfung; tatsächliche volle Skin-Auswertung/Grenzen/Kopfanhebung/Land-Isolation |
| Bestehende Wasserregression | Alle fünf V2-Tests in der vollständigen Serie, einschließlich tatsächlicher Attack/Hit/Faint-Auswertung beider Rigs und vorhandener Navigation/Fischkontakt |
| Zwölf Map Checks | Editor01: jede Map 0 Fehler/0 Warnungen; Marker GARADOS_POLISH_V3_MAPCHECK_BEGIN/END; MapChecks.json |
| Separater Development-Spielprozess | Functional02: bestanden, 95,15 s; alle qualifizierten Wasserphasen, Menü-Save/Load und ursprünglicher Garados-Landbegleiter |
| Echter PIE auf VisualV2 | PIE02: bestanden, 102,45 s; alle Wasserphasen, Kamera von drei Uferseiten, Menü-Save/Load und Landbegleiter |
| Echter Garados-Kampf und Fang im PIE | PIEBattle01.json: bestanden, 12,28 s; normale Uferinteraktion → ClassicBattle auf ursprünglichem Meshy-Rig → regulärer MasterBall-Fang, unterschiedliche Instanzidentität, Bestandsteam erhalten |
| Save/Load | Vollständige Teamfelder einschließlich Identitäten/Attacken/AP, genaue Position und pausierte Weltzeit in eigener Testparty exakt wiederhergestellt |
| Kamerawerte | Tatsächliche Weltkamera auf ebenem Ufer Z=172,15 cm bei Boden Z=0,15 cm, somit 1,72 m; Pitch −12°, Arm 350 cm. Keine Kameraeinstellung verändert |
| Echter physischer Controller | Nicht geprüft; keine Controllerbelegung geändert |

Die vollständige Automation umfasst die bisherige Referenz 317 plus drei neue Tests. Der strenge Runner ist vom vorhandenen GaradosWaterV2-Wrapper abgeleitet: bestehender Automation-/Report-Vertrag, eigener UserDir, keine Warnungstests zugelassen; keine globale Logunterdrückung. Reproduzierbarer Aufruf und Grenzen unter `Tools/GaradosPolishV3/README.md`. Tatsächlich installierte Engine laut Build.version: **5.8.4, CL58902052**, aus dem bestehenden UE_5.8-Verzeichnis; keine Engineinstallation oder Projektzuordnung verändert. Dies wird nicht als Test unter 5.8.2 ausgegeben.

### Fehlversuche und externe Diagnosen

- Automation01 brach am neuen Test ab: `GetCPUSkinnedVertices` erwartet ein Render-MeshObject, das bei NullRHI fehlt. Test korrigiert auf tatsächliches CPU-Skinning aus aktuellen Bone-Matrizen/LOD-SkinWeights; kein Null-/Referenzpose-Ersatz. Focus01 bestand 3/3, danach vollständige Automation02 320/320. Der frühe strenge Exit 1 bleibt fehlgeschlagen.
- Functional01 scheiterte am Zugriff des Python-Helfers auf eine geschützte Presentation-Eigenschaft; Helfer verwendet danach das öffentliche Datenasset. PIE01 scheiterte an einem einzelnen vorübergehend nicht erreichbaren Vorschauziel beim Absenken; bounded Retry mit weiteren sicheren Zielen, danach PIE02 bestanden. Keine Kollisionsabschaltung oder abgeschwächte Produktionsregeln.
- Engine-Startlogs enthalten weiterhin bekannte Toolset-`Condition failed`-Diagnosen (17 im Editor/Automation), teils MCP-HTTP-Bindefehler Port 8000 und Python-Namenskonflikt. Native `-game`-Starts melden einen fehlenden `unreal.PythonTestRunner` in einem Engine-Toolset-Startskript. Im Editor zudem bestehende Westland-Materialwarnung zur InstancedStaticMeshes-Usage und Telemetrie-Shutdown-Warnungen. Diese werden nicht als Garados-Fehler behoben.
- In den ausgewerteten finalen Logs kein `idevice_id: Bad CPU type` aufgetreten; externe iOS-Helferwarnungen wären separat zu behandeln. Keine Behauptung global warnungsfreier Engine-Logs. Der finale Automation-Report selbst ist warnungsfrei.
- Eigene PIE-/Editor-/Spielprozesse regulär beendet, keine gewaltsame Prozessbeendigung und kein neuer reproduzierter Editorstillstand.

## Echte Bildnachweise und visuelle Grenzen

Vorher: `Saved/ProjectRefinement/GaradosPolishV3/BaselineView01/Before_V2_Observe_ThirdPerson.png` und zugehöriger Seitenblick. Nachher: `PIE02/01_Idle.png` bis `PIE02/12_ReturnToSwim.png`, insbesondere `03_Normal.png`, `05_DelayedTurn.png`, `07_Raising.png`, `08_Observe.png`, `10_ObserveSouth.png`, `11_Lowering.png`. Echte 2560×1440-Unreal-Aufnahmen. Kamera bleibt V3; am seitlichen Ufer kann ein Teil des großen Körpers am Bildrand liegen. Der südliche Blick zeigt den angehobenen Vorderkörper und den im Wasser verbleibenden Rest gut.

Kein Anspruch auf pixelidentischen Vorher-/Nachhervergleich: Garados bewegt/dreht sich in den echten Durchläufen. Die Vorherbilder dokumentieren den Ausgangszustand, keine kontrollierte Beleuchtungsstudie. Das vorhandene große aufgerichtete Garados-Landbegleitermodell kann vom Ufer die Sicht verdecken; für spätere Fotos/Film wurde nur in der eigenen QA-Party der bestehende kleine Enton vorübergehend nach vorn sortiert und anschließend die ursprüngliche Reihenfolge wiederhergestellt. Regulärer Garados-Landbegleiter wurde getrennt geprüft.

Die bestehende Wasseroberfläche verdeckt Unterwasserteile. Keine Transparenz-/Materialänderung, neue Wassersimulation oder künstliche Aufhellung für die Aufnahme. Grenzen der ursprünglichen Meshy-Oberflächenstruktur und der V2-Ruhepose bleiben bestehen. Künstlerische Freigabe durch Harry bleibt offen; keine Aussage vollkommen unverformter Oberfläche. Keine Performanceoptimierung oder neue FPS-Zusage.

## Medienprüfung

Die native macOS-Fensteraufnahme bleibt durch ScreenCaptureKit/TCC −3801 blockiert. Keine Berechtigung oder Systemeinstellung geändert. Motion01 lieferte zwar 514 korrekt datierte, dekodierbare Frames, aber schwarze Bilder; der daraus erzeugte `Garados_V3_Motion.mp4` ist ausdrücklich **unbrauchbar**. `Motion01/Assessment.json` kennzeichnet ihn; die reine Zeitstempelverifikation ist kein visueller Nachweis.

Der alternative Aufnahmeweg verwendet Unreals funktionierenden `Shot`-/`SaveImageByExtension`-Pfad mit echten QHD-JPEGs. Ausschließlich der separate Aufnahmeprozess verwendet feste Simulationsschritte von 30 Hz und ca. 15 Aufnahmebilder pro Spielsekunde. Keine künstlich vervielfachten oder interpolierten Bilder, keine Änderung des HDR-Backbufferformats oder der Grafikqualität. Die normalen Funktionstests Functional02 und PIE02 liefen ohne diesen festen Zeitschritt. Ein solcher Offline-Film ist **kein** Nachweis normaler Gameplay-FPS oder einer 30-FPS-Echtzeitaufnahme.

Motion02 erreichte alle Wasserphasen bis zum Absenken, aber keinen qualifizierten Wiederanlauf vor dem begrenzten 900-Frame-Aufnahmelimit; sein Gesamtergebnis ist fehlgeschlagen. Der nächste reine Aufnahmeversuch prüft mehr Ziele mit demselben unveränderten sicheren Planer. Die normale Funktionsabnahme bleibt durch Functional02/PIE02 separat nachgewiesen. Der abschließende Motion03-Lauf bestand sämtliche Phasen; Werte nachfolgend.

## Projektschutz und Git

Der Dateischutzvergleich vor Dokumentation prüfte 6.021 zuvor versionierte Dateien (ca.9,90 GB), 351 geschützte/unversionierte Dateien einschließlich lokaler Fab-Originale (ca.7,52 GB) und alle 665 zuvor vorhandenen Save-Dateien. Ausschließlich die vorgesehenen drei Präsentations-C++-/Headerdateien, der eigene QA-Launcher und Garados' Präsentations-Datenasset waren verändert; keine fehlende Datei. Eigene isolierte Testspielstände liegen zusätzlich nur unter dem neuen QA-Verzeichnis.

Die bereits vor Auftrag vorhandenen vier lokalen Zeilen in `Config/DefaultEngine.ini` bleiben bytegleich und werden nicht mitcommittet. Alle ursprünglichen Pokémon-Assets, übrigen Animationen und alle Maps bleiben bytegleich. VisualV2-SHA256 weiterhin `ae9ed79aa91fc2b83d6c328010aa6a7d176d12c6a6f84140ed07ee0389c98a34`; die Forest-Rücknahme `f10dc77f` wird nicht rückgängig gemacht. Lokale Fab-Assets und ihre Ignore-Regeln sowie beide Vollbackup-Refs bleiben erhalten.

Nur eigene neue Animationsquellen/FBXs/Assets, Präsentationsänderungen, drei Tests, gezielt erweiterte QA-Werkzeuge und Dokumentation werden gesichert. Kontrollmedien und Messdaten unter Saved bleiben lokal. Bestehendes LFS verwenden, kein Prune, keine Budget-/Zahlungsänderung, kein Force-Push. Der zugehörige Commit ist über `git log -1 -- Docs/GARADOS_ANIMATION_POLISH_V3.md` eindeutig auffindbar; der konkrete Hash und das nach dem Push geprüfte Remote-/LFS-Ergebnis werden im Chat mitgeteilt.


## Abschließender Film und Schlussprüfung

**Gültiges Testvideo:** `Saved/ProjectRefinement/GaradosPolishV3/Garados_V3_Animation_Review.mp4`. H.264, **2560×1440**, **57,60 s**, **864 echte Frames**, tatsächlich **15,00 Bilder pro Spielsekunde**. Motion03: alle zwölf qualifizierten Aufnahmepunkte bestanden, zuletzt Beobachtungsalpha 0 und erneute Bewegung 42 cm/s; Prozess regulär mit Exit 0 beendet. Der Film enthält auch eine längere sichere Neuorientierungs-/Wartephase vor dem Wiederanlauf; keine Änderung der Navigation, kein Herausschneiden als angeblicher ununterbrochener Bewegungsnachweis.

Die Aufnahme benötigte ca.135,16 s reale Zeit für 57,53 s zwischen erstem/letztem Simulationsbild, entsprechend **6,38 tatsächlich aufgenommenen Bildern pro realer Sekunde**. Nur der getrennte Offline-Aufnahmeprozess verwendet 30-Hz-Simulationsschritte. Die 15-FPS-Wiedergabe folgt den echten Spielzeitabständen; keine interpolierten/duplizierten Ersatzframes. Das ist keine 15- oder 30-FPS-Echtzeit-Leistungsmessung des regulären Spiels.

Verifikation `VideoVerificationFinal.json`: 864/864 dekodiert, eindeutige PTS, maximaler Zeitfehler ca.3,00 µs, keine zusätzlichen Frames. `VideoPixelCheckFinal.json` prüft die tatsächlichen dekodierten Pixel **jedes** Frames: keine schwarzen/flachen Bilder, minimaler Stichproben-Helligkeitsmittelwert 91,37/255, minimale Helligkeitsstreuung 40,19. Zusätzlich vier echte dekodierte QHD-Bildbelege `FinalVideoProof_0.png`, `_200.png`, `_450.png`, `_863.png` gesichtet. Damit wird der frühe schwarze Aufnahmefehler nicht allein durch Codec-Metadaten übersehen.

Die erste Kodierung dieses farbigen Materials (`Garados_V3_Motion_Review.mp4`) enthielt wegen des ersten Quellzeitpunkts bei 1/30 s einen automatisch vorgeschalteten schwarzen AVFoundation-Frame und scheiterte an der Verifikation (865 statt 864). Dieser Film ist ebenfalls **kein** gültiger Nachweis. Für den oben genannten endgültigen Film wurde ausschließlich der gemeinsame Zeitursprung um 1/30 s auf null verschoben; Original-JPEGs und rohe CSV bleiben erhalten. Die abgeleitete Eingabe unter `Motion03/EncodeInput` referenziert dieselben unveränderten JPEGs, ohne zusätzliche Bildkopien oder Resampling. Der Aufnahmehelfer beginnt künftig direkt beim ersten aufgenommenen Bild mit PTS 0.

Die endgültige technische Gesamtserie `AutomationFinal` bestätigte nach allen Produktionsänderungen erneut **320 erfolgreiche Tests und strengen Exit 0**. C++/Assets sind seit Build04 unverändert. Die spätere QA-Helferkorrektur betrifft ausschließlich Aufnahme/Metadaten; keine erneute Produktionskompilierung dafür nötig. Keine Behauptung einer vollständigen hochfrequenten künstlerischen Freigabe: Der 15-FPS-Film und die vorhandene Wasseroberfläche begrenzen die visuelle Beurteilung feiner schneller Details. Harry beurteilt V3 anschließend selbst auf der bestehenden Map.
