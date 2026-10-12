# Meshy Player – Animation Quality V2

Prüfstand: 12.10.2026, Unreal Engine 5.8.2 / macOS. Ausgangs-HEAD `8c3ea2d`.
Der Arbeitsbaum enthielt bereits die offene Meshy-V1-Integration. Diese wurde erhalten; kein Commit, Push, Restore oder Löschen bestehender Projektdateien.

## Quellen und Erhalt

- Original: `Art/Characters/YoungTrainer/Source/Player_Meshy_V1.blend`.
- Funktionierende V1: `Art/Characters/YoungTrainer/Source/Player_Meshy_GameReady_V1.blend`.
- Neue Arbeitsdatei: `Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend`.
- Beide V1-Quellen, alle drei V1-FBX-Dateien und alle acht V1-Unreal-Assets sind bytegleich erhalten. V2 wurde über die bestehende Blender-MCP-Verbindung bearbeitet, mit drei gepackten Texturen gespeichert und erfolgreich erneut geöffnet.
- Die bestehenden PlayerCharacter-Anbindungsänderungen aus V1 wurden in diesem Auftrag nicht weiter verändert. Maps, Bewegung, Gameplay, Kamera und Spielstand bleiben erhalten.

## Ursache und Überarbeitung

V1 hatte einen 1-s-Zyklus mit etwa 23 cm Fußweg in der Standphase. Das entsprach nicht 210 cm/s und begünstigte den rutschenden Eindruck. Becken und Oberkörper bewegten sich kaum; die Tasche hatte keine Laufanimation und nur einen sehr kleinen separat gewichteten Bereich. Der Umhang hatte geringe gebackene Bewegung ohne Reaktion auf Stops oder Richtungswechsel.

V2 enthält einen vollständigen 0,55-s-Zyklus bei 60 Samples/s. Eine Standphase dauert 0,275 s; der Fuß bewegt sich dabei im Modell etwa 57,75 cm entgegen der Laufrichtung. Das passt rechnerisch zu 210 cm/s. Die gesamte Schrittlänge beträgt 115,5 cm pro Doppelzyklus. Bei dieser Geschwindigkeit handelt es sich für die kleine Figur um einen zügigen Gang; keine Änderung der Spielgeschwindigkeit.

- Gegengleicher Armschwung, leichte Beckenrotation, seitliche Gewichtsverlagerung, gegengleiche Oberkörperrotation und dezente Schulterbewegung.
- Zwei-Gelenk-Beinlösung mit alternierenden Stand-/Rückholphasen, Kniebeugung, Fußorientierung und etwa 6,6 cm Rückholhöhe.
- Referenzkörper weiterhin 140 cm bei Scale 1. Die Laufpose ist durch gebeugte Knie niedriger; Mesh-/Weltmaßstab wurde nicht verändert. Die vertikale Beckenvariation bleibt etwa 1,2 cm Spitze zu Spitze.
- Idle: ruhiger 3-s-Atemzyklus.
- Prüfung aller 34 gebackenen Walk-Frames an der tatsächlich verformten Mesh-Geometrie: niedrigster Vertex etwa 0,05 cm über Blender-Z=0. Dies ist ein Quellenaudit, keine pauschale Garantie für jedes spätere Terrain.
- Eine bei der Bearbeitung gefundene falsche Zuordnung unterer Ärmel zum Umhang wurde korrigiert; die entsprechende räumliche Weight-Grenze schließt die Ärmel nun aus.

## Rig und Sekundärbewegung

25 Knochen statt 23, ergänzt um `cape_left` und `cape_right`. Vorhandene `cape_upper`, `cape_lower` und `bag` bleiben erhalten. Der Taschen-Knochen sitzt am oberen Taschenansatz; 843 Vertices erhalten anteilige Taschengewichte, statt des sehr kleinen V1-Bereichs. Der diagonale Riemen und die oberen Anbindungen bleiben bei der Körpergewichtung. 6614 Vertices werden für die räumlich abgegrenzte Umhangfläche verteilt.

Die native `PokeMonsterMeshyAnimInstance` liest auf dem Game Thread Geschwindigkeit und Modelldrehung aus der bestehenden Darstellungskomponente. Sie extrahiert und mischt die zwei Clips, ohne Root Motion oder Gameplay-Bewegung zu erzeugen. Idle/Walk wird über 0,18 s überblendet; die Walk-Phase wird beim Stop erhalten. Abspielrate = tatsächliche horizontale Geschwindigkeit / 210 cm/s.

Drei gedämpfte, begrenzte Federzustände erzeugen zusätzliche Umhang-/Taschenbewegung aus Beschleunigung und Drehgeschwindigkeit. Unterteilung maximal 1/120 s, verarbeitete Hitch-Zeit maximal 0,1 s. Grenzwerte: Umhangneigung ±9°, seitliche Umhangantwort ±12°, Tasche ±9°. Die Offsets werden nur auf die fünf Zubehörknochen angewandt. Kein Cloth-Solver, keine Physik-Kollision und keine zusätzliche Spielsteuerung. Bei Stop und konstantem Stillstand gehen diese Federzustände gegen null.

V2-Mesh, eigenes Skelett und zwei Clips liegen unter `/Game/Characters/YoungTrainer/MeshyV2`. Material und Texturen aus MeshyV1 werden unverändert wiederverwendet. Originale V1-Assets bleiben verfügbar. `MeshyVisual.SetMeshyEnabled(false)` schaltet weiterhin auf die vorhandenen acht Paper2D-Richtungen zurück.

## Tatsächliche Prüfungen

- Mac-Development-Editor-Build erfolgreich (`Saved/MeshyPlayerMotionV2/BuildFinal.log`). Der erste Linkversuch hing im UBA-IPC-Initialisierer; derselbe Build wurde ohne UBA-Detours erfolgreich abgeschlossen. Keine Toolchain-/Projekteinstellung geändert.
- Abschließender Gesamtlauf im frischen Editor: **39/39 Tests erfolgreich**, 0 fehlgeschlagen, 0 übersprungen. Nachweis `AutomationFreshParsed.json` im Reviewordner.
- Ein vorheriger Wiederholungslauf derselben Sitzung hatte 38/39: `Battle.Session.ValidationAndReplay` meldete beim Garbage Collect ein noch initialisiertes LandscapeSubsystem eines zuvor geladenen Healing-House-Testlevels. Der Player-Test bestand. Dieser Engine-/Testsitzungsfehler war im frischen vollständigen Lauf nicht reproduzierbar; Battle-/Landscape-Code wurde dafür nicht verändert.
- Aktualisierter `Player.MeshyPresentation` prüft Clip-Laden, Skelett, 140-cm-Bounds, Root-Motion-Verbot, alternierende Schritte, tatsächliches Tempo, Teilüberblendung, Drehantwort, Auspendeln und Paper2D-Fallback. Bestehende Foundation-/Scale-/Gameplay-Tests unverändert.
- Letzter normaler PIE-Fußlauf in `Dev_TestMap`: **bestanden**, etwa 16,67 m ohne Teleports. Acht tatsächliche Enhanced-Input-Richtungen, jeweils 210 cm/s, korrekte Modelldrehung, Richtungsbeibehaltung nach Stop, Wanderer-Interaktion mit Dialogsperre sowie Inventarmenü mit korrekter Rückgabe der Eingabe.
- Bestehende Baumstamm-Kollision geprüft: Bewegung blockiert, Velocity 0, kein Durchfallen. Paper2D-Fallback in PIE aus-/eingeschaltet und geprüft. Die letzte Clip-Korrektur betraf nur kombinierte Schulter-/Umhangrotationen; Collision und Fallback sind außerdem im endgültigen Automationstest abgesichert.
- Kamera weiterhin 2500 cm, Pitch −55°, Yaw −45°, FOV 35°. Capsule Radius 28 cm / Höhe 96 cm, Bewegung 210 cm/s, Interaktion, Input und Karten unverändert.
- Dev-Save bytegleich; keine ungespeicherten Content-/Map-Packages am Abschluss. Temporäre Prüfcallbacks entfernt und Throttle-Einstellung wiederhergestellt.

## Bewegungsnachweise und Qualitätsgrenzen

Reviewordner: `Saved/MeshyPlayerMotionV2/` (ignorierte Arbeitsartefakte).

- `PIE_AnimationV2.gif`: tatsächliche Spielkamera, etwa 14 s, 99 aufgenommene Frames mit Zeitstempeln. Stehen, Loslaufen, mehrere Zyklen, Stop, 90°-/180°-Drehung und acht Richtungen.
- `PIE_AnimationV2_Close.gif`: vergrößerter Ausschnitt derselben Aufnahme; kein Kamerazoom oder neues Detailmaterial.
- `PIE_DirectionsV2.gif` / `PIE_DirectionsV2_Close.gif`: zusätzliche Richtungsfolge nach Fußweg zum weiteren offenen Bereich.
- `Sequence.json`, `Sequence_OpenDirections.json`: Zeitstempel, Walk-Phase, tatsächliches Tempo, Überblendung und Zubehör-Federzustände.
- `PIE_GaitSequence.png`, `PIE_OpenEightDirections.png`, `PIE_SelectedEightDirections.png`: nachvollziehbare Einzelbildübersichten. Die ausgewählte Richtungsübersicht kombiniert echte Frames aus beiden Laufwegen, um die Verdeckung zu reduzieren. Einige bestehende Vegetationskronen verdecken den Player in Teilen der Wege. Die Map wurde dafür nicht umgebaut; nicht jeder Aufnahmeframe eignet sich zur Beurteilung der Füße.

Das Gangbild hat nun größere, gegengleiche Schritte und ein bewegtes Becken statt der bisherigen fast starren Haltung. Umhangsaum und Tasche verändern ihre Lage und reagieren auf Drehungen/Stops. Dennoch ist dies **keine finale Artfreigabe**:

- Das dichte, aus Meshy stammende Kleidungsmesh hat keine saubere getrennte Stofftopologie. Lokale Falten, Quetschungen und Umhang-/Beinüberschneidungen sind bei einzelnen Posen weiterhin möglich.
- Keine vollständige Körperkontakt-/Cloth-Kollisionslösung; begrenzte Knochenbewegung reduziert Risiken, verhindert sie nicht generell.
- Füße sind jeweils ein starrer Knochen ohne separat artikulierte Zehen. Das Modell trägt keine Stiefel; Modell-/Texturdetails wurden in diesem Animationsauftrag nicht erweitert.
- Standphasen sind rechnerisch auf 210 cm/s abgestimmt. Auf abrupten Stops, bei Beschleunigung, beim Richtungswechsel und in der 0,18-s-Überblendung bleiben lokale Fußkorrekturen möglich. Keine Motion-Matching- oder Terrain-Foot-IK-Garantie.
- Helle bestehende Außenbeleuchtung und kleine Bildschirmdarstellung begrenzen die Beurteilbarkeit feiner Taschen-/Gewichtungsdetails; der vergrößerte Reviewcrop erzeugt keine zusätzliche Auflösung.
- Die Bildsequenz ist eine zeitgestempelte Screenshotaufnahme mit etwa 7–8 Bildern/s und Renderhitches; sie ersetzt keine 60-fps-Mocap- oder finale Animator-Abnahme. Ein verworfener HighResShot-Versuch verlangsamte das Gameplay-Timing und wird nicht als gültiger Echtzeitnachweis verwendet.

## Dateien dieser V2-Aufgabe

Neu:

- `Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend`
- `Art/Characters/YoungTrainer/Exports/MeshyV2/SK_Player_Meshy_V2.fbx`
- `Art/Characters/YoungTrainer/Exports/MeshyV2/A_Player_Meshy_Idle_V2.fbx`
- `Art/Characters/YoungTrainer/Exports/MeshyV2/A_Player_Meshy_Walk_V2.fbx`
- `Content/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2.uasset`
- `Content/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2_Skeleton.uasset`
- `Content/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Idle_V2.uasset`
- `Content/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Walk_V2.uasset`
- `Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.h`
- `Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.cpp`
- `Tools/Blender/AnimateMeshyPlayerV2.py`
- `Tools/Blender/ExportMeshyPlayerV2.py`
- `Tools/ImportMeshyPlayerV2.py`
- dieser Prüfbericht

Geändert gegenüber dem offenen V1-Arbeitsstand:

- `Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.h`
- `Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.cpp`
- `Source/PokeMonster/Tests/PokeMonsterMeshyPlayerTest.cpp`
- `Docs/TECHNIK.md`
- `Docs/ENTSCHEIDUNGEN.md`

Die offene V1-Integration bleibt zusätzlich im Git-Status enthalten. Ein späterer Sicherungspunkt muss V1-Grundlage und V2 gemeinsam berücksichtigen; keine Reviewbilder, Logs, `.blend1`-Backups oder Prüfaufnahmen aus `Saved/` versionieren. Visuelle Sichtprüfung durch Harry steht aus.

## Abschlussaudit und Git

14 neue V2-Projektdateien, 5 Änderungen gegenüber dem offenen V1-Stand. `git diff --check` ohne Ausgabe; Text-/Markdownprüfung bestanden. Keine Änderungen gestaged. Quellen-/Map-Prüfung: `Saved/MeshyPlayerMotionV2/FinalAudit.json`.

Abschließender offener Git-Status (enthält die erhaltene V1-Integration):

```text
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h
?? Art/Characters/YoungTrainer/Exports/
?? Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend
?? Art/Characters/YoungTrainer/Source/Player_Meshy_GameReady_V1.blend
?? Art/Characters/YoungTrainer/Source/Player_Meshy_V1.blend
?? Art/Characters/YoungTrainer/Textures/MeshyV1/
?? Content/Characters/YoungTrainer/
?? Docs/MESHY_PLAYER_ANIMATION_QUALITY_V2_PRUEFBERICHT.md
?? Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.cpp
?? Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.h
?? Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.cpp
?? Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.h
?? Source/PokeMonster/Tests/PokeMonsterMeshyPlayerTest.cpp
?? Tools/Blender/AnimateMeshyPlayerV2.py
?? Tools/Blender/ExportMeshyPlayerV1.py
?? Tools/Blender/ExportMeshyPlayerV2.py
?? Tools/Blender/PrepareMeshyPlayerV1.py
?? Tools/ImportMeshyPlayerV1.py
?? Tools/ImportMeshyPlayerV2.py
```

Nach Harrys Sichtprüfung ist die gemeinsame V1-/V2-Integration ein sinnvoller Sicherungspunkt. Gezielter Stage-Vorschlag, hier nicht ausgeführt:

```sh
git add -- \
  Art/Characters/YoungTrainer/Source/Player_Meshy_V1.blend \
  Art/Characters/YoungTrainer/Source/Player_Meshy_GameReady_V1.blend \
  Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend \
  Art/Characters/YoungTrainer/Exports/MeshyV1 \
  Art/Characters/YoungTrainer/Exports/MeshyV2 \
  Art/Characters/YoungTrainer/Textures/MeshyV1 \
  Content/Characters/YoungTrainer/MeshyV1 \
  Content/Characters/YoungTrainer/MeshyV2 \
  Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp \
  Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h \
  Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.cpp \
  Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.h \
  Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.cpp \
  Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.h \
  Source/PokeMonster/Tests/PokeMonsterMeshyPlayerTest.cpp \
  Tools/Blender/PrepareMeshyPlayerV1.py \
  Tools/Blender/ExportMeshyPlayerV1.py \
  Tools/Blender/AnimateMeshyPlayerV2.py \
  Tools/Blender/ExportMeshyPlayerV2.py \
  Tools/ImportMeshyPlayerV1.py \
  Tools/ImportMeshyPlayerV2.py \
  Docs/TECHNIK.md \
  Docs/ENTSCHEIDUNGEN.md \
  Docs/MESHY_PLAYER_ANIMATION_QUALITY_V2_PRUEFBERICHT.md
```
