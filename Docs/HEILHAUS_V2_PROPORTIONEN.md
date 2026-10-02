# Heilhaus V2 – Proportions-Pass

Stand 2026-10-02; HEAD `8705b16 Refine camera and healing house cutaway`. Die Aufgabe setzt den vorhandenen offenen V2-Arbeitsstand fort. Keine Commits oder Pushes.

## Maße und gezielte Anpassung

| Größe | Vorher | Nachher |
| --- | --- | --- |
| Freie Türpassage | 2,40 × 2,30 m | **1,70 × 2,15 m** |
| Hauptkörperbreite | 10,30 m | **9,00 m** |
| Hauptkörpertiefe | 9,30 m | 9,30 m |
| Firsthöhe | 6,40 m | 6,40 m |
| Tresenoberkante | 92 cm | 92 cm |
| Innenbodenbreite | 9,70 m | 8,40 m |
| Türschwellen-Box | 40 × 240 × 230 cm | 40 × 170 × 215 cm |
| Schwellenzentrum | (-450, 0, 115) cm | (-450, 0, 107,5) cm |

36 von 39 Gebäudemodulen gezielt angepasst; Actor-Scale bleibt (1,1,1). Frontfassade und Türöffnung erhalten getrennte Maßanpassungen. Frontfenster und Rahmen werden um 35 cm nach innen versetzt, ihre Formen und Größen bleiben erhalten. Seitenwände und Vorbau rücken um 65 cm nach innen. Dachbreite und Giebel folgen dem engeren Grundriss; First und Gebäudetiefe bleiben erhalten. Eingangshaube, Türrahmen und offenes Türblatt werden separat angepasst. Die drei eigenständig wiederverwendbaren Fensterbibliotheks-Assets bleiben unverändert.

Der Innenboden und die Randarchitektur werden schmaler, der zentrale Gang bleibt frei. Die vorhandenen Liegen behalten ihre Positionen. Das bestehende Regal samt drei vorhandenen Gefäßen rückt um 50 cm nach innen, damit es nicht in der neuen Seitenwand steckt. **Tresen, Tresenblocker und Hüterin werden nicht versetzt oder skaliert.** Kein neues Dressing.

Die einfachen Front-/Seiten-/Rückwandblocker werden passend zu den neuen Grenzen gesetzt. Alle Collision-Profile bleiben erhalten. Die einzige Triggeranpassung ist die oben angegebene map-konfigurierte Box; X-Schwelle -450 cm, 4-cm-Hysterese, 0,4-s-Fade, Occluder-Liste und Cutaway-C++ bleiben unverändert. Die generischen Klassenvorgaben werden nicht verändert.

## Quelle und Export

- Aktuell: `Art/HealingHouse/Source/HealingHouse_V2.blend`. Explizit gespeichert, für Sichtprüfung und Export wieder geöffnet; sieben Texturen eingebettet.
- Unveränderter vorheriger Stand: `Art/HealingHouse/Source/HealingHouse_V2_PreProportions.blend`.
- Hauptexport nach Sichtprüfung: `Art/HealingHouse/Exports/HealingHouse_V2.fbx`.
- 36 einzelne geänderte Module unter `Art/HealingHouse/Exports/V2Modules`, damit Reimport-Dateien dauerhaft im Projekt liegen. Keine zusätzliche Unreal-Hierarchie und keine neuen Unreal-Assets.
- Weiterhin 15.256 Gebäudedreiecke plus 2.308 Dreiecke der unveränderten Fensterbibliothek. Keine neue Geometrie-Deko.
- BVH-Prüfung bestätigt eine echte offene Passage von 170 × 215 cm: innerhalb frei, außerhalb Wandkontakt. Mesh-Konnektivität bleibt unverändert. Bei den zwei Innenbalkenmodulen waren schon vorher jeweils acht nicht-manifold Kanten vorhanden; keine zusätzlichen Kanten. Die frühere pauschale 0-Aussage im V2-Bericht wurde berichtigt.

## Beurteilung aus der tatsächlichen Spielkamera

Unverändert in PIE gelesen: 2500 cm, FOV 35°, Rotation (-55°, -45°, 0°), Camera Lag 6 / maximal 180 cm, Bewegung 210 cm/s. Player-Sprite/Flipbook-Skalierung und die bestätigten 140 cm Körperhöhe sind unverändert.

- **Vor dem Haus:** Front und Dach wirken weniger überbreit; der unverändert hohe First erhält die Fantasy-Silhouette. Die Tür ist deutlich schlanker und wirkt eher wie ein Hauseingang als ein breites Tor. Direkt am Vorplatz bleibt der obere Dachbereich wie zuvor angeschnitten; keine Kameraänderung, um dies zu kaschieren.
- **Im Eingang:** Die 140-cm-Figur ist klar lesbar und passt zur neuen 215-cm-Höhe. 180-cm-Humanoide haben 35 cm rechnerische Kopffreiheit; 210 cm sind mit nur 5 cm knapp. Die gewünschte 170-cm-Passage bleibt für die unveränderte 56-cm-Capsule bequem passierbar.
- **Im Innenraum:** Kompaktere Seitenbegrenzung, weiterhin ausreichend Platz im mittleren Bereich und diagonale Laufwege. Tresen und Hüterin bleiben sichtbar. Vorhandene Platzhalter-Einrichtung und Beleuchtung bleiben erhalten.

## PIE: vollständiger Fußweg ohne Teleports

Normaler PlayerStart; ausschließlich normale Slate-WASD-Eingaben. Keine Positionswrites und kein Spawn-Override.

| Schritt | Tatsächliche Playerposition (cm, gerundet) | Cutaway | Ergebnis |
| --- | --- | --- | --- |
| Vor der Schwelle | (-494, -7, 50) | aus / 0 | Keine vorzeitige Ausblendung |
| Gerade hinein | (-389, 1, 50) | an / 1 | Passage frei |
| Diagonalstart außen | (-508, 35, 50) | aus / 0 | Rückweg vorher ebenfalls frei |
| Diagonal hinein (W) | (-396, -77, 50) | an / 1 | Kein Feststecken |
| Innenraum | (-201, 73, 50) | an / 1 | Diagonaler Weg frei |
| Tresen | (144, -71, 50) | an / 1 | Unveränderter Blocker und Maßstab |
| Hüterin | (150, -182, 50) | an / 1 | E öffnet den vorhandenen Dialog |
| Bestätigung | gleiche Position | an / 1 | Teamheilung, Speichern und Checkpoint bestätigt |
| Rückweg innen | (-356, -20, 50) | an / 1 | Bewegung nach Dialog freigegeben |
| Türmitte | (-454, -9, 50) | an / 1 | Stabil im 4-cm-Hystereseband |
| Diagonal hinaus (S) | (-574, 111, 50) | aus / 0 | Dach/Fassade wieder vollständig sichtbar |
| Vorplatz | (-672, -13, 50) | aus / 0 | Kompaktere Front gut lesbar |
| Wieder beim Außenstart | (-1005, -2, 50) | aus / 0 | Vollständiger Fußweg abgeschlossen |

Bilder und Positionsprotokoll stehen unter `Art/HealingHouse/Review/V2/Proportions`. Die Vorher-Bilder stammen aus dem bereits bestätigten vorherigen V2-Test, nicht aus einem neu gestarteten Vorher-Durchlauf. Die ersten Bilder enthalten eine editorseitige Speicherdruck-Benachrichtigung; spätere Bilder erfassen direkt den tatsächlichen Spielviewport. Kamera und Gameplay werden dadurch nicht verändert.

Die originale offene Editor-/Blender-Sitzung bleibt erhalten; der separate Testeditor wurde nach bestätigtem PIE-Stopp und „Alle gespeichert“ geschlossen. Der vorhandene Dev-Spielstand wurde nach dem Test bytegleich wiederhergestellt: SHA-256 `59f6f2f7af77f45e08c07d3358314be1131bac7a7f9f0e4e33359313ccf0bbbf`.

## Tests und unveränderte Systeme

- Mac Development Build **erfolgreich**. Einzige C++-Änderung: geometrieabhängige Testassertionen in `PokeMonsterHealingHouseTest.cpp`; keine Gameplay-C++-Änderung.
- Gesamter bestehender PokeMonster-Testbestand: **35 erfolgreich, 0 fehlgeschlagen, 0 Warnungen**. Enthält Player Foundation, Scale Calibration und alle drei HealingHouse-Tests.
- Map Check nach Import: **0 Fehler, 0 Warnungen**.
- Python-Syntaxprüfung aller drei neuen Werkzeuge erfolgreich.
- Hashvergleich zum offenen Ausgangsstand bestätigt unveränderte Gameplay-/Player-Quellen, Dev_TestMap, V1-Quelle/Export, sämtliche V2-Materialien/Texturen, Fensterbibliothek, Tresen- und Kamin-Assets.
- Heilung, RestPoint, Checkpoint, Save, Quest, Battle, Input und Animationen unverändert.
- Keine neue Lichtstimmung, Vegetation, Detaildeko oder V3-Features.

## Dateien dieses Proportions-Passes

Die folgende Liste vergleicht mit dem **offenen V2-Ausgangsstand**, nicht nur mit HEAD.

Geändert: **44** Dateien; neu: **65** Dateien.

```text
M Art/HealingHouse/Exports/HealingHouse_V2.fbx
M Art/HealingHouse/Review/V2/GeometryAudit.json
M Art/HealingHouse/Source/HealingHouse_V2.blend
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorFrame.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorLeaf.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Floor.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Foundation.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Front.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Rear.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_CameraSide.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Far.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Front.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Loft.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorBeams.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorBeams_CameraSide.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorStone.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_PorchFloor.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Entry.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Main.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Porch.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Trim.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_CameraSide.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Far.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Front.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Rear.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_CameraSide.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Entry.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Far.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Front.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Porch.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Rear.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_CameraSide.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Far.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Front.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Rear.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_CameraSide.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Far.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Front.uasset
M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Loft.uasset
M Content/Maps/Dev_HealingHouseTestMap.umap
M Docs/ENTSCHEIDUNGEN.md
M Docs/HEILHAUS_V2_PRUEFBERICHT.md
M Docs/TECHNIK.md
M Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_DoorFrame.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_DoorLeaf.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Floor.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Foundation.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Gable_Front.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Gable_Rear.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Glass_CameraSide.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Glass_Far.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Glass_Front.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Glass_Loft.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_InteriorBeams.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_InteriorBeams_CameraSide.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_InteriorStone.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_PorchFloor.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Roof_Entry.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Roof_Main.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Roof_Porch.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Roof_Trim.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Stone_CameraSide.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Stone_Far.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Stone_Front.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Stone_Rear.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Timber_CameraSide.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Timber_Entry.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Timber_Far.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Timber_Front.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Timber_Porch.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Timber_Rear.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Walls_CameraSide.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Walls_Far.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Walls_Front.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Walls_Rear.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Windows_CameraSide.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Windows_Far.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Windows_Front.fbx
A Art/HealingHouse/Exports/V2Modules/SM_HH_V2_Windows_Loft.fbx
A Art/HealingHouse/Review/V2/Proportions/BeforeGeometryAudit.json
A Art/HealingHouse/Review/V2/Proportions/Before_PIE_V2_AtCounter_2500.png
A Art/HealingHouse/Review/V2/Proportions/Before_PIE_V2_Forecourt_2500.png
A Art/HealingHouse/Review/V2/Proportions/Blender_Exterior.png
A Art/HealingHouse/Review/V2/Proportions/Blender_Interior.png
A Art/HealingHouse/Review/V2/Proportions/Blender_Porch.png
A Art/HealingHouse/Review/V2/Proportions/FootRoute.jsonl
A Art/HealingHouse/Review/V2/Proportions/GeometryChanges.json
A Art/HealingHouse/Review/V2/Proportions/PIE_BeforeThreshold.png
A Art/HealingHouse/Review/V2/Proportions/PIE_Counter.png
A Art/HealingHouse/Review/V2/Proportions/PIE_DiagonalEntry.png
A Art/HealingHouse/Review/V2/Proportions/PIE_DiagonalExit.png
A Art/HealingHouse/Review/V2/Proportions/PIE_DiagonalStart.png
A Art/HealingHouse/Review/V2/Proportions/PIE_Exterior.png
A Art/HealingHouse/Review/V2/Proportions/PIE_Forecourt.png
A Art/HealingHouse/Review/V2/Proportions/PIE_HealerApproach.png
A Art/HealingHouse/Review/V2/Proportions/PIE_HealerDialogue.png
A Art/HealingHouse/Review/V2/Proportions/PIE_HealingConfirmed.png
A Art/HealingHouse/Review/V2/Proportions/PIE_InDoorway.png
A Art/HealingHouse/Review/V2/Proportions/PIE_Interior.png
A Art/HealingHouse/Review/V2/Proportions/PIE_ReturnInterior.png
A Art/HealingHouse/Review/V2/Proportions/PIE_StraightEntry.png
A Art/HealingHouse/Review/V2/Proportions/UnrealChanges.json
A Art/HealingHouse/Review/V2/Proportions/ValidationResults.json
A Art/HealingHouse/Source/HealingHouse_V2_PreProportions.blend
A Docs/HEILHAUS_V2_PROPORTIONEN.md
A Tools/Blender/ApplyHealingHouseV2Proportions.py
A Tools/Blender/ExportHealingHouseV2Proportions.py
A Tools/ImportHealingHouseV2Proportions.py
```

## Git-Prüfung

`git diff --check`: erfolgreich, keine Whitespace-Fehler. Kein Commit oder Push. Der vollständige Status enthält auch die bereits vorher offenen V2-Dateien:

```text
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp
?? Art/HealingHouse/Exports/HealingHouse_V2.fbx
?? Art/HealingHouse/Exports/HealingHouse_V2_WindowModules.fbx
?? Art/HealingHouse/Exports/V2Modules/
?? Art/HealingHouse/Review/V2/
?? Art/HealingHouse/Source/HealingHouse_V2.blend
?? Art/HealingHouse/Source/HealingHouse_V2_PreProportions.blend
?? Art/HealingHouse/Textures/
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Glass.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Metal.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Plaster.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Roof.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Stone.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Timber.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Wood.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Chimney.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_ChimneyCap.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Counter.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorFrame.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorLeaf.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Floor.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Foundation.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Loft.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorBeams.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorBeams_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorStone.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_PorchFloor.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Entry.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Main.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Porch.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Trim.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Entry.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Porch.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Arch.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Round.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Twin.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Loft.uasset
?? Content/Environment/HealingHouse/Textures/
?? Docs/HEILHAUS_V2_PROPORTIONEN.md
?? Docs/HEILHAUS_V2_PRUEFBERICHT.md
?? Tools/Blender/ApplyHealingHouseV2Proportions.py
?? Tools/Blender/BuildHealingHouseV2.py
?? Tools/Blender/BuildHealingHouseV2WindowLibrary.py
?? Tools/Blender/ExportHealingHouseV2Proportions.py
?? Tools/Blender/ReviewHealingHouseV2.py
?? Tools/GenerateHealingHouseV2Textures.py
?? Tools/ImportHealingHouseV2.py
?? Tools/ImportHealingHouseV2Proportions.py
?? Tools/ImportHealingHouseV2WindowLibrary.py
```

## Optionaler Git-Sicherungspunkt

Der geprüfte V2-Stand einschließlich Proportionen ist ein sinnvoller Sicherungspunkt nach Harrys Sichtprüfung. Folgende Befehle sind nur dokumentiert und wurden **nicht ausgeführt**:

```sh
git add -- Art/HealingHouse Content/Environment/HealingHouse Content/Maps/Dev_HealingHouseTestMap.umap Docs/ENTSCHEIDUNGEN.md Docs/TECHNIK.md Docs/HEILHAUS_V2_PRUEFBERICHT.md Docs/HEILHAUS_V2_PROPORTIONEN.md Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp Tools/Blender Tools/GenerateHealingHouseV2Textures.py Tools/ImportHealingHouseV2.py Tools/ImportHealingHouseV2WindowLibrary.py Tools/ImportHealingHouseV2Proportions.py
git commit -m "Refine Healing House V2 architecture and proportions"
```
