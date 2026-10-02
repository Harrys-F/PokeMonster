# Heilhaus V1: Blender → Unreal – Prüfbericht

Stand: 02.10.2026. Funktionaler Architektur-Blockout nach der gelieferten Konzepttafel, noch keine finale Spielgrafik.

## 1–3. Ausgangsstand

- Branch: `main`.
- HEAD: `c7733e3 Add healing house prototype`.
- `git status --short` vor Beginn: leer, Arbeitsstand sauber.
- Keine fremden Änderungen zurückgesetzt, keine Commits und keine Pushes ausgeführt.

## 4. Blender-Quelle

`Art/HealingHouse/Source/HealingHouse_V1.blend`, außerhalb von `Content`.

Eigenständige Szene `HealingHouse_V1`; Meter, Unit Scale 1. Die ursprüngliche Live-Szene mit Cube, Camera und Light bleibt erhalten. Die eigene Quelldatei wurde separat gespeichert und erfolgreich in Blender wieder geöffnet.

## 5. Tatsächliche Abmessungen

| Teil | Maß |
| --- | --- |
| Hauptkörper, Breite × Tiefe | 10,30 × 9,30 m |
| Gesamt mit Überständen/Vorbau | 12,20 × 9,90 m |
| Dachfirst über Laufboden | 6,40 m |
| Kaminoberkante über Laufboden | 7,02 m |
| Außenwandstärke | 0,30 m |
| Eingang, lichte Breite × Höhe | 2,40 × 2,30 m |
| Fußbodenoberkante/Schwelle | 0,00 m |

Die Gesamtbreite liegt durch den seitlichen Vorbau 20 cm über dem ungefähren 12-m-Richtwert. Der Hauptkörper liegt im gewünschten Bereich. Kein begehbares Obergeschoss wurde ergänzt.

## 6. Blender-Module

- `HH_Floor`
- `HH_Foundation`
- `HH_Walls_Front`
- `HH_Walls_CameraSide`
- `HH_Walls`
- `HH_Glass_Front`
- `HH_WindowFrames_Front`
- `HH_Glass_CameraSide`
- `HH_WindowFrames_CameraSide`
- `HH_Glass_Back`
- `HH_WindowFrames`
- `HH_Gable_Front`
- `HH_Gable_Rear`
- `HH_Roof_Main`
- `HH_Roof_Porch`
- `HH_Timber_Porch`
- `HH_PorchFloor`
- `HH_Timber_Front`
- `HH_Timber`
- `HH_Timber_CameraSide`
- `HH_DoorFrame`
- `HH_Chimney`
- `HH_ChimneyCap`
- `HH_Counter`

Zusätzlich `HH_ScaleReference_140cm` in `HH_ReviewOnly`, ausschließlich als Prüfblock; nicht exportiert. Architektur liegt in `HH_Architecture`.

## 7–8. Geometrie und Material-Slots

24 Architekturmeshes, insgesamt 1.124 Dreiecke. Gemeinsamer Gebäudeursprung, Rotation 0 und Scale 1. Boolean-Türöffnung sowie sechs echte Fensteröffnungen. Geometrieaudit: keine nichtmanifold Kanten oder Nullflächen; positive Volumen und neu berechnete Normalen. Außen-, Vorbau- und Cutaway-Innenansichten wurden geprüft. Keine offensichtlichen flimmernden Oberflächen beobachtet.

Sieben Slots: `Plaster`, `Wood`, `Timber`, `Stone`, `Roof`, `Metal`, `Glass`. Einfache warme Putz-, Holz-, Stein-, Dach- und Fensterfarben; keine finalen Texturen, Einzelziegel, Ornamente oder Vegetation.

## 9–10. Export und Unreal-Import

FBX: `Art/HealingHouse/Exports/HealingHouse_V1.fbx`.

Nur Architekturmeshes, trianguliert; keine Kameras, Lichter, Animationen oder Maßstabsblöcke. FBX Unit Scale, X Forward/Z Up. Unreal: Import Scale 1, Einheitenkonvertierung Meter → Zentimeter; separate Static Meshes, keine automatische Ganzhaus-Collision. Blender-Y wird bei der linkshändigen Unreal-Konvertierung gespiegelt; die Quelle berücksichtigt dies bereits. Alle 24 importierten Mesh-Grenzen stimmen innerhalb 3 mm mit der Quelle überein.

Importpfade:

- `/Game/Environment/HealingHouse/Meshes/SM_HH_*` – 24 Meshes.
- `/Game/Environment/HealingHouse/Materials/M_HH_*` – sieben Materialien.
- Integration ausschließlich in `/Game/Maps/Dev_HealingHouseTestMap`.

Der erste Vergleich fand 12 m neben dem alten Blockout statt. Erst nach Maß-/Grundrissprüfung wurden die neuen Module an den ursprünglichen Gebäudeursprung gesetzt. Alte Gebäudeteile bleiben unsichtbar mit Tag `HealingHouse_RetainedBlockout` erhalten.

## 11. Größenvergleich mit dem Player

Der vorhandene Idle-Sprite hat vor Skalierung eine Flächenhöhe von 150,59 cm. Die bestehende BeginPlay-Skalierung 0,36 ergibt etwa 54,21 cm in der Sprite-Ebene; dies ist keine Körperhöhenmessung entlang Welt-Z. Die separate 1,40-m-Blender-Prüfhilfe stellt den architektonischen Richtwert dar. Der reale Player wurde nicht vergrößert. Die größere Eingangspassage bleibt auch für spätere normale humanoide Figuren geeignet.

Playergeschwindigkeit bleibt 210 cm/s. Kamera bleibt bei Arm Length 1.400 cm, Pitch −55°, Yaw −45°, FOV 35 und Camera Lag Speed 6. Bestehende acht Blickrichtungen, Laufanimationen und Input wurden nicht geändert. Die im Editor eingestellte Review-Kamera verändert keine Spielkamera.

## 12–14. Eingang, Innenraum, Collision und Cutaway

Ebenerdige, frei passierbare Tür; zentrale Laufzone, Tresen, unveränderte Hüterin und bestehende Ruhe-/Reserveeinrichtung. Seitlicher offener Vorbau ohne zweiten Innenraum.

Bestehende einfache Boden-, Wand- und Tresen-Collision bleibt maßgeblich. Neue Architekturmeshes verwenden `NoCollision`; kein konvexes Ganzhaus und keine per-poly-Ganzhaus-Collision. Der Tresen blockiert den Player und erlaubt den vorhandenen Interaktionstrace.

Das vorhandene `PokeMonsterBuildingCutaway` erhält zusätzlich 14 Dach-/Fassadenmodule, einschließlich vorderem Giebel, Türrahmen, kameraseitigem Fachwerk, Fenstern und Kamin. Sein C++-Verhalten wurde nicht geändert. NPC und Player bleiben sichtbar.

## 15. Build und automatisierte Tests

- `PokeMonsterEditor Mac Development`: erfolgreich, keine Compile Errors.
- `Automation RunTests PokeMonster`: 34 erfolgreich, 0 fehlgeschlagen, 0 nicht ausgeführt, 0 mit Warnungen.
- Enthalten: alle drei Heilhaus-Tests, Player, Interaktion über Encounter/Dialog, RestPoint/Checkpoint/Save, Overworld-UI, Quest, Battle, Team, Capture, Inventar, Kreaturen und Attacken.
- Layout-Test erweitert um Importmodule, Scale/Origin, NoCollision, Cutaway-Anbindung und 6,40-m-Firsthöhe.
- Bestehende Capsule-Sweeps prüfen Eingang, diagonale Laufpassagen und Tresen-/Wandblockierung.
- Map Check im Editor: 0 Fehler, 0 Warnungen.
- Persistente Kurzfassung der Ergebnisse: `Art/HealingHouse/Review/ValidationResults.json`.

Nur `Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp` wurde in C++ ergänzt. Kein Gameplay-C++ wurde verändert.

## 16. Echter PIE-Test und Grenzen

Nach Editor-Neustart war die native Tastatureingabe möglich. Route ohne Teleports oder Spawn-Override:

1. Normaler Außen-PlayerStart.
2. Zu Fuß durch den Haupteingang; Dach und nahe Fassade verschwinden.
3. Zentralen Innenbereich bis vor den Tresen durchqueren.
4. Hüterin mit `E` ansprechen.
5. Mit Enter bestätigen: vollständige Heilung, Speichern und Rückkehrort werden angezeigt; Save-Log bestätigt `PokeMonster_Dev`.
6. Dialog schließen; Steuerung wieder nutzbar.
7. Zu Fuß durch denselben Eingang nach draußen; Fassade wieder sichtbar.

Keine Türblockade, kein Feststecken und keine Map-Lücke auf dieser Route beobachtet. Player und Animationen blieben sichtbar.

Nicht manuell geprüft: gleichzeitig gehaltene diagonale Tastenkombinationen, alle Innenraum-Ecken sowie eine Heilung zuvor beschädigter Kreaturen in PIE. CUA akzeptiert keine Kombination zweier Nicht-Modifikatortasten; die gelaufene Route verwendete einzelne bzw. abwechselnde Bewegungstasten. Diagonal-Collision und Wiederherstellung reduzierter HP/PP werden automatisiert geprüft. Das PIE-Team startete bereits mit vollen HP.

Der bestehende lange Hüterinnen-Einleitungstext überschreitet den Dialogpanel-Rahmen; Darstellung und Dialoglogik wurden im Architekturauftrag unverändert belassen. Die nachfolgende Erfolgsmeldung ist vollständig lesbar.

Der reguläre Heilvorgang hat den Dev-Slot gespeichert. Vorheriger Slot wurde unter `/private/tmp/HH_V1_PreHeal_DevSave.sav` gesichert; keine Save-Datei ist Teil der Git-Änderungen.

## 17. Sämtliche neuen/geänderten Dateien

Die folgende vollständige Git-Dateiliste enthält alle neuen Quellen, Assets, Prüfbelege, Skripte und Dokumente. Andere Maps und Kernsysteme wurden nicht geändert.

## 18–19. Git-Prüfung und finaler Status

`git diff --check`: erfolgreich, keine Ausgabe. Neue Python-/Markdown-/JSON-Dateien zusätzlich auf Syntax bzw. Whitespace geprüft. Branch und HEAD unverändert.

### Vollständiger Status mit Einzeldateien

```text
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp
?? Art/HealingHouse/Exports/HealingHouse_V1.fbx
?? Art/HealingHouse/Review/Concept_HealingHouse.png
?? Art/HealingHouse/Review/Exterior.png
?? Art/HealingHouse/Review/GeometryAudit.json
?? Art/HealingHouse/Review/Interior.png
?? Art/HealingHouse/Review/Porch.png
?? Art/HealingHouse/Review/UnrealImportAudit.json
?? Art/HealingHouse/Review/ValidationResults.json
?? Art/HealingHouse/Source/HealingHouse_V1.blend
?? Content/Environment/HealingHouse/Materials/M_HH_Glass.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_Metal.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_Plaster.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_Roof.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_Stone.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_Timber.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_Wood.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Chimney.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_ChimneyCap.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Counter.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_DoorFrame.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Floor.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Foundation.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Gable_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Gable_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Glass_Back.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Glass_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Glass_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_PorchFloor.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Roof_Main.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Roof_Porch.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Timber.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Timber_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Timber_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Timber_Porch.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Walls.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Walls_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_Walls_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_WindowFrames.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_WindowFrames_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_WindowFrames_Front.uasset
?? Docs/HEILHAUS_V1_PRUEFBERICHT.md
?? Tools/Blender/BuildHealingHouseV1.py
?? Tools/Blender/FinalizeHealingHouseSource.py
?? Tools/ImportHealingHouseV1.py
```

### Sinnvoller Sicherungspunkt

Nach Harrys Abnahme dieses funktionalen Blockouts ist ein Git-Sicherungspunkt sinnvoll. Optionale Befehle, hier nicht ausgeführt:

```sh
git add Art/HealingHouse Content/Environment/HealingHouse Content/Maps/Dev_HealingHouseTestMap.umap Docs/ENTSCHEIDUNGEN.md Docs/TECHNIK.md Docs/HEILHAUS_V1_PRUEFBERICHT.md Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp Tools/Blender/BuildHealingHouseV1.py Tools/Blender/FinalizeHealingHouseSource.py Tools/ImportHealingHouseV1.py
git commit -m "Add modular Blender healing house V1"
```

## Nachtrag: Scale Calibration 2026-10-02

Die ursprünglichen 54,21 cm waren die gesamte transparente Sprite-Leinwand, nicht die Körperhöhe. Die spätere Messung ergibt vor der Korrektur 45,42–46,38 cm Alpha-Körper in der geneigten Sprite-Ebene. Die anschließende reine Player-Darstellungskalibrierung erzeugt 140 cm sichtbare Welt-Z-Körperhöhe bei unveränderter Capsule, Kamera und Architektur. Vollständige Frame-/Pivot-/PPU-Messwerte, Größenreferenzen, PIE-Beurteilung und Tests stehen in `SCALE_CALIBRATION.md`. Dieser Nachtrag ersetzt keine historischen V1-Testergebnisse.
