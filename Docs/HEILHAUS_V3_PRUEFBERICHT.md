# Healing House V3 – Frontkorrektur, Dressing und Atmosphäre

Stand: 03.10.2026. Ausgangs-HEAD: `477e6f6 Move healing house Blender versions to Git LFS`. Der Arbeitsbaum war zu Beginn sauber. Kein Commit, kein Push und kein Restore wurden ausgeführt.

## Frontkorrektur

1. **Tür:** Die in Unreal tatsächlich verwendete freie Passage wurde gezielt von **170 × 215 cm auf 150 × 215 cm** verkleinert. Wandöffnung, Türrahmen, Steinrahmung, geöffneter Türflügel und angrenzendes Fachwerk passen dazu. Keine globale Skalierung. Gebäude 900 × 930 cm, nominaler First 640 cm unverändert. Die bestehende Dach-Bevel-Geometrie reicht gemessen bis ca. 638,9 cm; sie wurde in Z nicht verändert.
2. **Trigger:** Von **40 × 170 × 215 cm auf 40 × 150 × 215 cm**, Zentrum weiterhin (-450, 0, 107,5) cm. Extent (20, 75, 107,5) cm. Die Übergangsposition, 4-cm-Hysterese, 0,4-s-Fade und CPD-0-Dither bleiben erhalten.
3. **Mittelachse:** Türmitte, geteilter senkrechter Mittelbalken und Rundfenster liegen auf **Y=0**. Das zuvor etwa 52,4 cm versetzte Rundfenster einschließlich seiner Öffnung wurde auf die Türmitte gesetzt. Der Mittelbalken unterbricht am Fenster und schneidet die Glasfläche nicht.
4. **Symmetrie:** Oberes Fachwerk, Streben und Stützen sind links/rechts um diese Achse ausgeglichen. Die seitlichen Frontfenster bleiben ähnlich breit und gleichmäßig vom Eingang entfernt. Sockel und Rahmen folgen der schmaleren Öffnung; kleine bestehende handwerkliche Unterschiede bleiben erhalten.
5. **Dach/Giebel:** Giebelspitze, Dachprofil und obere Fachwerkverbindungen sind mittig geordnet. Fantasy-Silhouette und Dachüberstände bleiben erhalten. Hauptdach, Entry-Dach und Cutaway-Module bleiben getrennt. Zwölf vorhandene Architektur-Meshes wurden aktualisiert; die vorhandene Unreal-Hierarchie bleibt bestehen.
6. **Phase-1-PIE-Gate:** Vor jeglichem Dressing bestanden: normaler Außenstart → Vorplatz → vor die Tür → gerade hinein → hinaus → diagonal hinein → Innenraum → Schwelle/Hysterese → diagonal hinaus → Außenstart. Normale Slate-WASD-Eingaben, keine Spawn-Overrides oder Test-Teleports. Vor der Schwelle bleibt der Cutaway aus, innen ist der Fade vollständig, außen die Fassade wieder sichtbar. Die Tür wirkt gegenüber der 140-cm-Figur kompakter und bleibt bequem passierbar. Achse und Frontkomposition sind auch in der schrägen tatsächlichen Spielkamera nachvollziehbar; perspektivisch müssen die Elemente keine senkrechte Bildschirm-Pixellinie bilden.

Nachweise: `Art/HealingHouse/Review/V3/Front/GeometryAudit.json`, `PIEGate.json`, `FootRoute.jsonl` sowie die dortigen tatsächlichen PIE-Bilder. Das Front-Gate wurde zuerst abgeschlossen; danach begann Dressing.

## V3

7. **Außen-Dressing:** Zwei bepflanzte Fensterkästen, sparsame Ranken an äußeren Frontpfosten, warme Eingangslaterne, wenige Fässer/Kiste und kleiner Holzstapel am Vorbau, einzelne Stein-/Wegdetails sowie verstreute vorhandene Wildblumen-, Gras- und Moosstein-Sprites. Eingang und Schild bleiben frei. Frontnahe Pflanzen stehen paarweise ausgewogen; kleine Bodenpflanzen sind bewusst ungleichmäßig verteilt.
8. **Hüter-Symbol:** Eigenes freundliches Zeichen aus Schutzkreis, zwei Blättern/Blattspross und kleinen Pfotenpunkten. Keine Pokéball- oder Center-Kopie. Auf einer kleinen Tafel an einem separaten schmiedeeisernen Ausleger neben dem Eingang. Das einfache helle Zeichen bleibt bei 2500 cm lesbar.
9. **Innen-Dressing:** Zwei Liegen, Kräuterregal, Bücherregal, Kräutertisch, wenige Bücher und Phiolen, Behandlungstücher/Schale, Teppich mit ruhiger Randzeichnung, kleine Sitzecke mit Tisch/Bank und wenige getrocknete Kräuter. Der zentrale und diagonale Laufweg bleibt frei. Tresen und Hüterin wurden nicht versetzt.
10. **Blender-Props:** Acht separate Meshes: `TreatmentBedSmall`, `TreatmentBedLarge`, `HerbShelf`, `Bookcase`, `HerbTable`, `SignBracket`, `GuardianSign`, `Lantern`. Insgesamt 8128 Dreiecke, lokale wiederverwendbare Pivots. Liegenrahmen ca. 140 × 82 cm und 180 × 105 cm; einschließlich kleiner Kopfstützenüberstände gemessen ca. 144 × 83 × 70 cm und 184 × 106 × 70 cm. Unterschiedliche Kreaturengrößen sind damit plausibel. Keine Kreaturenanimation oder Behandlungssimulation.
11. **Unreal-Props:** Kleine Bücher, Flaschen, Pflanzen, Vorräte, Holz, Behandlungsmaterial, Wegdetails und Sitzecke sind einzeln editierbare Actors mit Engine-Meshes oder bestehenden Paper2D-Sprites. Keine komplette monolithische Innendekoration in Blender. Neue Content-Assets: acht Meshes und neun einfache Materialien ausschließlich unter `/Game/Environment/HealingHouse/V3`. Insgesamt 186 zusätzliche Dressing-/Licht-Actors, überwiegend kleine schattenfreie Dekoration.
12. **Beleuchtung:** Bestehendes weiches Tages-/Fülllicht bleibt erhalten, warme Fenster ebenfalls. Drei schwache warme Point Lights ergänzen Eingang, Tresen und Ruhebereich (Intensitäten 2,8 / 3,6 / 2,4, Reichweiten 280 / 430 / 330 cm, ohne inverse-square falloff und ohne Schatten). Der erste PIE-Vergleich war überhell; die Werte wurden gezielt reduziert. Keine neue dramatische Lichtstimmung.
13. **Collision:** Große feste Möbel blockieren; fünf importierte Möbel verwenden jeweils einen einfachen Convex-Körper. Kleine Deko, Pflanzen, Bücher, Phiolen, Teppich und Schild bleiben `NoCollision`. Möbel ignorieren `Visibility` für die vorhandene Interaktion. Die ursprünglichen Blockout-Möbel bleiben erhalten, sind aber ausgeblendet und ohne zusätzliche unsichtbare Collision. Zusätzlich wurden Liege und Bücherregal nach Neuladen der gespeicherten Map in einer frischen Editor-Sitzung zu Fuß angelaufen: beide blockieren sichtbar korrekt; der Rückweg durch die Tür bleibt frei (`FreshLoadCollisionPIE.json`). Die tatsächlichen Türwand-Kanten liegen bei ±75 cm. Capsule-Sweeps prüfen freie Laufwege und echtes Blocking an Liege/Bücherregal.
14. **Cutaway:** Schwellenprinzip unverändert. Neue frontseitige Mesh-Dekoration wird mit maskiertem CPD-0-Material und vorhandener Occluder-Liste ebenfalls ausgeblendet. Kein vorzeitiges Ausblenden, kein Annäherungs-Cutaway, Collision unabhängig vom Fade. Innen bleiben Möbel, Hüterin und Rückwände sichtbar; beim Austritt erscheint die Front wieder.
15. **Tatsächliche Kamera:** Live geprüft: 2500 cm, FOV 35°, Rotation (-55°, -45°, 0°), Lag 6, maximal 180 cm; Bewegung 210 cm/s. Die 140-cm-Figur bleibt lesbar. Der Eingang wirkt weniger breit, das Schild identifiziert die Hüterstätte. Innen ergeben Liegen, Vorräte und Sitzecke eine funktionale Aufteilung. Stilisiertes V3-Dressing auf bestehenden Architektur-Platzhaltern, noch keine finale Konzeptgrafik. Das komplette Haus passt unmittelbar am Eingang weiterhin nicht ins Bild; Kamera und FOV wurden auftragsgemäß nicht angepasst.
16. **Finaler PIE-Fußweg:** Vollständig bestanden: normaler Außenstart → Vorplatz → neue Tür gerade → hinaus und diagonal hinein → Innenraum → Hüterin → regulärer E-Dialog → Enter/Heilung → Heil-/Save-/Checkpoint-Bestätigung → Dialog schließen → Liegen/Kräutertisch entlang freier Laufwege ansehen → Schwelle → diagonal hinaus → Vorplatz → Außenstart. Keine Teleports. Player/Hüterin lesbar, keine neuen Blockaden, kein vorzeitiger Fade. Die PIE-Testgruppe hatte bereits volle HP; Wiederherstellung reduzierter HP/PP wird durch Automation geprüft. Der bestehende Dev-Spielstand wurde vor dem Test gesichert und anschließend bytegleich wiederhergestellt, SHA-256 `f47190b969bdd940be90d8f4869239e2b1d689180b9ef85368507cc8cf731544`.
17. **Build/Tests/Map Check:** Abschließender Mac-Development-Build erfolgreich. Alle **35 PokeMonster-Automationstests erfolgreich**, 0 Fehler, 0 Testwarnungen, 0 nicht ausgeführte Tests, einschließlich Player Foundation/ScaleCalibration und aller drei HealingHouse-Tests. Map Check der endgültigen gespeicherten Map: **0 Fehler, 0 Warnungen**. Finale Ergebnisse: `Review/V3/Dressing/AutomationResults.json`, `Validation.json` und `FinalPIE.json`.

Gefundene und behobene Probleme: Der Interchange-Import übernahm automatische Möbel-Collision im Commandlet nicht; sie wurde im vollständigen Editor erzeugt, gespeichert und per tatsächlichen Sweeps verifiziert. Neue statische PaperSprite-Komponenten wiesen `SetSprite` ab; temporäre Beweglichkeit, geprüfte Zuweisung und anschließend statische Komponenten lösen dies ohne Änderungen an bestehenden Assets. Überhelle Point Lights wurden reduziert. Eine Editor-Speicherdruck-Benachrichtigung fing zwischenzeitlich Tastatureingaben ab; nach Schließen und Refokussieren war der Tresenbereich frei begehbar. Der endgültige vollständige Durchlauf wurde danach wiederholt. Die zusätzliche Sprite-Testprüfung benötigte eine kleine Const-Korrektur für Unreals Getter. Eine frische Null-RHI-Sitzung zeigte anschließend, dass die isolierte Testwelt importierte Convex-Physikdaten vor dem Kopieren mit `CreatePhysicsMeshes` vorbereiten muss. Gespeichert sind jeweils ein Convex-Körper pro Möbel; danach bestehen die echten Blocking-Sweeps und alle 35 Tests auch nach einem frischen Engine-Start. Der abschließende Build ist erfolgreich.

## Quellsicherung und Erhalt bestehender Systeme

Die neue Quelle wurde ausdrücklich gespeichert und lesend wieder geöffnet; Blender-Exterior-/Porch-/Interior-Renders wurden vor dem modularen FBX-Export geprüft. Vollständiger Pfad:

`/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/HealingHouse/Source/HealingHouse_V3.blend`

Front-Gate-Quelle: `Art/HealingHouse/Source/HealingHouse_V3_Front.blend`. In den Quellen des Ausgangs-HEAD war noch die frühere 10,30-m-/2,40-m-Geometrie enthalten, während die Unreal-Map bereits die bestätigten V2-Proportionen verwendete. Die neue V3-Kopie rekonstruiert diese gezielt und korrigiert danach die Front. Bestehende V1/V2/PreProportions-Dateien wurden nicht überschrieben.

511 ursprünglich getrackte Dateien wurden per SHA-256 gegen den sauberen Ausgangsstand geprüft. Außer zwölf Heilhaus-Meshes, Heilhaus-Testmap, Heilhaus-Testcode und den beiden aktualisierten Dokumenten sind sie bytegleich. Gameplay-C++, Player-Assets, Bewegung/Input, Healing/RestPoint/Checkpoint/Save/Quest/Battle, `Dev_TestMap` und die bisherigen Blender-Quellen bleiben unverändert. Originale Actor-Positionen wurden vor dem Front-Import geprüft; Tresen/Hüterin bleiben an ihrem bisherigen Ort. Die normale Editor-Sitzung und Blender-Szene des Nutzers wurden nicht gespeichert; zusätzliche Testprozesse wurden beendet.

## Dateien und Git

18. Die vollständige Liste aller neuen/geänderten Dateien folgt unten. Gruppen: zwölf aktualisierte Architektur-Meshes, eine Map, ein Test-C++-File, drei Dokumente, neue V3-Quellen/FBXs, acht Meshes/neun Materialien, acht gezielte Arbeits-Skripte und Prüfartefakte.
19. `git diff --check`: abschließend geprüft; Ergebnis wird unten festgehalten. Zusätzlich werden neue Markdown-/Python-/JSON-Dateien auf abschließende Newline und nachgestellte Leerzeichen geprüft.
20. `git status --short`: abschließende Ausgabe steht unten. Keine Datei wurde gestaged, kein Commit und kein Push durchgeführt.

Ein sinnvoller Git-Sicherungspunkt besteht nach eigener Sichtfreigabe dieses V3-Stands. Nur als späterer Vorschlag, hier **nicht ausgeführt**:

```sh
git diff --check
git status --short
git add Art/HealingHouse Content/Environment/HealingHouse Content/Maps/Dev_HealingHouseTestMap.umap Docs/TECHNIK.md Docs/ENTSCHEIDUNGEN.md Docs/HEILHAUS_V3_PRUEFBERICHT.md Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp Tools/*HealingHouseV3*.py Tools/Blender/*HealingHouseV3*.py
git commit -m "Healing house V3 front correction and dressing"
```

## Vollständige Dateiliste

**16 bestehende Dateien geändert, 99 neue Dateien** (einschließlich Prüfberichte und Bildnachweise).

Bestehende Dateien:

- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorFrame.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorLeaf.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Front.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Rear.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Loft.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Main.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Trim.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Front.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Front.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Rear.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Front.uasset`
- `Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Loft.uasset`
- `Content/Maps/Dev_HealingHouseTestMap.umap`
- `Docs/ENTSCHEIDUNGEN.md`
- `Docs/TECHNIK.md`
- `Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp`

Neue Dateien:

- `Art/HealingHouse/Exports/HealingHouse_V3.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_DoorFrame.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_DoorLeaf.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Gable_Front.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Gable_Rear.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Glass_Loft.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Roof_Main.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Roof_Trim.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Stone_Front.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Timber_Front.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Timber_Rear.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Walls_Front.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V2_Windows_Loft.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V3_Bookcase.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V3_GuardianSign.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V3_HerbShelf.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V3_HerbTable.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V3_Lantern.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V3_SignBracket.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V3_TreatmentBedLarge.fbx`
- `Art/HealingHouse/Exports/V3Modules/SM_HH_V3_TreatmentBedSmall.fbx`
- `Art/HealingHouse/Review/V3/Dressing/01_Exterior.png`
- `Art/HealingHouse/Review/V3/Dressing/02_Forecourt.png`
- `Art/HealingHouse/Review/V3/Dressing/03_DoorBefore.png`
- `Art/HealingHouse/Review/V3/Dressing/04_StraightEntry.png`
- `Art/HealingHouse/Review/V3/Dressing/05_DiagonalEntry.png`
- `Art/HealingHouse/Review/V3/Dressing/06_Interior.png`
- `Art/HealingHouse/Review/V3/Dressing/07_Counter.png`
- `Art/HealingHouse/Review/V3/Dressing/08_HealerApproach.png`
- `Art/HealingHouse/Review/V3/Dressing/09_HealerDialogue.png`
- `Art/HealingHouse/Review/V3/Dressing/10_HealSaveConfirmation.png`
- `Art/HealingHouse/Review/V3/Dressing/11_BedsHerbTable.png`
- `Art/HealingHouse/Review/V3/Dressing/12_InteriorCirculation.png`
- `Art/HealingHouse/Review/V3/Dressing/13_Threshold.png`
- `Art/HealingHouse/Review/V3/Dressing/14_DiagonalExit.png`
- `Art/HealingHouse/Review/V3/Dressing/15_OutsideRestored.png`
- `Art/HealingHouse/Review/V3/Dressing/16_ReturnToSpawn.png`
- `Art/HealingHouse/Review/V3/Dressing/17_FreshLoadBedCollision.png`
- `Art/HealingHouse/Review/V3/Dressing/18_FreshLoadBookcaseCollision.png`
- `Art/HealingHouse/Review/V3/Dressing/19_FreshLoadReturn.png`
- `Art/HealingHouse/Review/V3/Dressing/AutomationResults.json`
- `Art/HealingHouse/Review/V3/Dressing/Blender_Exterior.png`
- `Art/HealingHouse/Review/V3/Dressing/Blender_Interior.png`
- `Art/HealingHouse/Review/V3/Dressing/Blender_Porch.png`
- `Art/HealingHouse/Review/V3/Dressing/CollisionFix.json`
- `Art/HealingHouse/Review/V3/Dressing/FinalPIE.json`
- `Art/HealingHouse/Review/V3/Dressing/FootRoute.jsonl`
- `Art/HealingHouse/Review/V3/Dressing/FreshLoadCollisionPIE.json`
- `Art/HealingHouse/Review/V3/Dressing/PreservationAudit.json`
- `Art/HealingHouse/Review/V3/Dressing/PropAudit.json`
- `Art/HealingHouse/Review/V3/Dressing/SavePreservation.json`
- `Art/HealingHouse/Review/V3/Dressing/UnrealDressingAudit.json`
- `Art/HealingHouse/Review/V3/Dressing/Validation.json`
- `Art/HealingHouse/Review/V3/Dressing/VisualCorrections.json`
- `Art/HealingHouse/Review/V3/Front/01_Exterior.png`
- `Art/HealingHouse/Review/V3/Front/02_Forecourt.png`
- `Art/HealingHouse/Review/V3/Front/03_DoorBefore.png`
- `Art/HealingHouse/Review/V3/Front/04_StraightInside.png`
- `Art/HealingHouse/Review/V3/Front/05_OutsideAgain.png`
- `Art/HealingHouse/Review/V3/Front/06_DiagonalInside.png`
- `Art/HealingHouse/Review/V3/Front/07_Interior.png`
- `Art/HealingHouse/Review/V3/Front/08_ThresholdHysteresis.png`
- `Art/HealingHouse/Review/V3/Front/09_DiagonalOutside.png`
- `Art/HealingHouse/Review/V3/Front/10_Return.png`
- `Art/HealingHouse/Review/V3/Front/Blender_Exterior.png`
- `Art/HealingHouse/Review/V3/Front/Blender_Interior.png`
- `Art/HealingHouse/Review/V3/Front/Blender_Porch.png`
- `Art/HealingHouse/Review/V3/Front/FootRoute.jsonl`
- `Art/HealingHouse/Review/V3/Front/GeometryAudit.json`
- `Art/HealingHouse/Review/V3/Front/PIEGate.json`
- `Art/HealingHouse/Review/V3/Front/UnrealChanges.json`
- `Art/HealingHouse/Source/HealingHouse_V3.blend`
- `Art/HealingHouse/Source/HealingHouse_V3_Front.blend`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Book.uasset`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Bottle.uasset`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Cream.uasset`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Flower.uasset`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Herb.uasset`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Lamp.uasset`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Linen.uasset`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Ochre.uasset`
- `Content/Environment/HealingHouse/V3/Materials/M_HH_V3_Sage.uasset`
- `Content/Environment/HealingHouse/V3/Meshes/SM_HH_V3_Bookcase.uasset`
- `Content/Environment/HealingHouse/V3/Meshes/SM_HH_V3_GuardianSign.uasset`
- `Content/Environment/HealingHouse/V3/Meshes/SM_HH_V3_HerbShelf.uasset`
- `Content/Environment/HealingHouse/V3/Meshes/SM_HH_V3_HerbTable.uasset`
- `Content/Environment/HealingHouse/V3/Meshes/SM_HH_V3_Lantern.uasset`
- `Content/Environment/HealingHouse/V3/Meshes/SM_HH_V3_SignBracket.uasset`
- `Content/Environment/HealingHouse/V3/Meshes/SM_HH_V3_TreatmentBedLarge.uasset`
- `Content/Environment/HealingHouse/V3/Meshes/SM_HH_V3_TreatmentBedSmall.uasset`
- `Docs/HEILHAUS_V3_PRUEFBERICHT.md`
- `Tools/Blender/BuildHealingHouseV3Front.py`
- `Tools/Blender/DressHealingHouseV3.py`
- `Tools/Blender/ExportHealingHouseV3.py`
- `Tools/Blender/ReviewHealingHouseV3.py`
- `Tools/DressHealingHouseV3.py`
- `Tools/FinalizeHealingHouseV3Collision.py`
- `Tools/ImportHealingHouseV3Front.py`
- `Tools/RefineHealingHouseV3.py`

## Abschließende Git-Prüfung

`git diff --check`: erfolgreich, keine Ausgabe. Neue Textdateien zusätzlich auf Syntax, nachgestellte Leerzeichen und abschließende Newline geprüft. HEAD bleibt `477e6f6`; Index nicht verändert.

```text
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorFrame.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorLeaf.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Front.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Rear.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Loft.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Main.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Trim.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Front.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Front.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Rear.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Front.uasset
 M Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Loft.uasset
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp
?? Art/HealingHouse/Exports/HealingHouse_V3.fbx
?? Art/HealingHouse/Exports/V3Modules/
?? Art/HealingHouse/Review/V3/
?? Art/HealingHouse/Source/HealingHouse_V3.blend
?? Art/HealingHouse/Source/HealingHouse_V3_Front.blend
?? Content/Environment/HealingHouse/V3/
?? Docs/HEILHAUS_V3_PRUEFBERICHT.md
?? Tools/Blender/BuildHealingHouseV3Front.py
?? Tools/Blender/DressHealingHouseV3.py
?? Tools/Blender/ExportHealingHouseV3.py
?? Tools/Blender/ReviewHealingHouseV3.py
?? Tools/DressHealingHouseV3.py
?? Tools/FinalizeHealingHouseV3Collision.py
?? Tools/ImportHealingHouseV3Front.py
?? Tools/RefineHealingHouseV3.py
```
