# Westland Building Kit V1 – Prüfbericht

Stand: 03.10.2026. Ausgangs-HEAD **`4b035cd Complete healing house V3`**, Arbeitsbaum zu Beginn sauber. Kein Commit, Push oder Staging.

## Quelle, Raster und Module

1. **Ausgangs-HEAD:** `4b035cd`. 559 ursprünglich getrackte Dateien per SHA-256 gesichert; bestehende Assets, Quellen, C++ und Maps werden gegen diesen Ausgangsstand verglichen.
2. **Blenderquelle:** `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Architecture/Westland/Source/WestlandBuildingKit_V1.blend`. Explizit gespeichert, danach in einer getrennten Hintergrundinstanz wieder geöffnet, auf Geometrie/Origins/Materialien geprüft und außen/innen gerendert. Erst nach Sichtprüfung modular als FBX exportiert. Die Live-Blender-Szene und HealingHouse_V3.blend bleiben unverändert. Keine extern verlinkten Blender-Daten.
3. **Maßsystem:** 1-m-Grundraster; 2-m-Wandfelder, zusätzliche 1-m-Wand; 3-m-Wandhöhe, 20-cm-Wanddicke. Tür 1,30×2,00 m, Bogenfenster 1,00×1,10 m ab 1-m-Brüstung, Doppelfenster 1,10×1,10 m, Rundfenster ca. 70 cm. Standarddach und Halbgiebel für 6-m-Spannweite, Neigung 2:3, 1-m-Dachlängen plus 30-cm-Endstücke. Andere Hauslängen benötigen Wiederholungen, andere Dachspannweiten künftig ergänzende kompatible Varianten. Keine gestreckten Türen/Fenster oder globale Hausskalierung.

Blender +X weist ins Gebäude, -Y entlang des Wandfelds, +Z nach oben. FBX importiert dies in Unreal +X/+Y/+Z. Alle Bibliotheksobjekte haben Origin am Montageanker, angewandte Rotation und Scale 1. Wand-/Bodenanker liegen am Bay-/Kachelanfang; Türanker am Fuß-/Scharnierpunkt, Dachanker an First/Traufe. Die 14-cm-Fachwerkauflage gegenüber der Wandmittelebene ist eine feste Konstruktionsregel für sichtbar vorstehende Balken, keine manuelle Snap-Korrektur.

4./10. **Vollständige Modulliste und tatsächlich verwendete Häufigkeiten:**

| Modul (`SM_WL_…`) | Gruppe | Instanzen im Wohnhaus |
|---|---|---:|
| WallSolid1m | Walls | 0 |
| WallSolid2m | Walls | 8 |
| WallWindowArch2m | Walls | 2 |
| WallWindowDouble2m | Walls | 1 |
| WallDoor2m | Walls | 1 |
| GableHalf3m | Walls | 4 |
| CornerPost3m | Timber | 4 |
| VerticalPost3m | Timber | 8 |
| HorizontalBeam2m | Timber | 12 |
| DiagonalBrace1m | Timber | 4 |
| StonePlinth1m | Structural | 22 |
| RoofPanel1m | Roof | 12 |
| RoofPanelEnd30cm | Roof | 4 |
| EaveTrim1m | Roof | 12 |
| GableTrimHalf3m | Roof | 4 |
| RidgeCap1m | Roof | 6 |
| DoorFrame130x200 | Doors | 1 |
| DoorLeaf130x200 | Doors | 1 |
| WindowArch | Windows | 2 |
| WindowDouble | Windows | 1 |
| WindowRound | Windows | 0 |
| Chimney60cm | Structural | 1 |
| Porch160cm | Structural | 1 |
| Floor1m | Structural | 36 |
| Threshold130cm | Structural | 1 |

5. **Meshzahl:** 25 wiederverwendbare Static Meshes, insgesamt 5.468 Dreiecke in der Modulbibliothek. Wohnhaus: 148 Instanzen, 21.448 Dreiecke. 23 Modularten werden im Haus verwendet; 1-m-Wand und Rundfenster stehen zusätzlich in der Galerie zur Verfügung. Die Quelle enthält getrennte Module, benannte UCX-Collision-Quellen und eine Hauskomposition mit gemeinsam verwendeten Modul-Meshdaten.
6. **Materialien:** Sieben eigene Westland-Materialgraphen für Plaster, Wood, Timber, Stone, Roof, Metal und Glass. Die unveränderten V2/V3-Architekturmaterialien werden unabhängig nach `M_WL_*` kopiert; vorhandene Texturen und Engine-Materialfunktionen bleiben lesend gemeinsam nutzbar. Änderungen am neuen Materialgraphen ändern V3 nicht. Gemeinsame Texturquellen dürfen nicht für Westland überschrieben werden. Bestehende PaintedGround-/SoftPath-Materialien dienen unverändert nur dem Testgelände.
7. **Unreal-Struktur:** `/Game/Environment/Architecture/Westland/Materials` sowie `Meshes/{Walls,Timber,Roof,Windows,Doors,Structural}`. Die Building-Komposition ist im Actor-Ordner `Westland/Buildings/Cottage` der neuen Map organisiert; der exakte portable Bauplan ist `Art/Architecture/Westland/Buildings/WL_Cottage_V1.json`. Keine neue Blueprint-/Gameplayklasse und kein monolithischer Gebäude-Mesh erforderlich. Einzelmodule stehen in einer abgesetzten Galerie ab Y=13 m; Galerie ist NoCollision.

## Privates Wohnhaus

8. **Maße:** Konstruktionsraster 6,00×6,00 m; die 20-cm-Wände stehen um die Rasterlinien, Außenwandhülle daher ca. 6,20×6,20 m. Dach einschließlich Überständen ca. 6,60×6,60 m. First nominal 5,00 m, kleine Schindel-/Firstleistenüberstände darüber; Kamin bis ca. 5,68 m. Es ist ein einfaches Satteldachhaus mit drei Fenstern und kleiner Regenhaube, nicht eine global verkleinerte Heilhauskopie. Kein Hüter-Schild, öffentlicher Seitentrakt oder vollständiges Wohnungs-Dressing.
9. **Tür:** Freie Passage **130×200 cm**, gegenüber dem öffentlichen V3-Eingang von 150×215 cm bewusst privater. Bei 56-cm-Capsule-Breite bleiben nominell 37 cm je Seite. Türblatt ca. 128×195 cm, eigener Scharnier-Pivot, im Test nach außen 90° geöffnet. Die decorative Tür besitzt keine unsichtbare Passage-Collision.
11. **Sonderteile:** Keine nur für dieses Haus erzeugten Meshes. Sämtliche sichtbaren Hausbestandteile stammen aus dem Kit. Nur Instanzpositionen, Materialkopien, Testgelände, PlayerStart und Konfiguration des vorhandenen Cutaway-Actors sind gebäudespezifisch. Die beiden strukturierten JSON-Dateien und die Blenderquelle erlauben nachvollziehbare Wiederverwendung; kein erfundener NPC-Haushalt oder neues Spielsystem.
12. **Innenraum:** Begehbares Erdgeschoss, ca. 5,80×5,80 m lichte Fläche. Bewusst frei für spätere Tisch-/Bett-/Kamin-/Regalplatzierung. Der vollständige diagonale Laufraum und der Eingang bleiben frei. Bodenmodule schließen ohne Lücken; Übergang vom Testgelände zum Boden nur wenige Zentimeter, normal begehbar. Noch kein Obergeschoss oder Interior-Dressing.
13. **Collision:** Explizite UCX-Boxgeometrie in den Modul-FBXs: 1 Körper je einfache Wand/Boden/Schwelle, 4 je Fensterwand, 3 getrennte Körper für die Türwand (links, rechts, Lintel). Die UCX-Boxen werden als Convex-Körper importiert. Kein einzelner Konvexkörper über der Türöffnung. Kleine Balken, Rahmen, Fenster, Dach, Schornstein, Regenhaube und Galerie bleiben NoCollision. Blocking-Wände ignorieren den Visibility-Interaktionskanal. Unabhängig vom Cutaway bleiben die Wände physisch aktiv.
14. **Cutaway:** Die bestehende `PokeMonsterBuildingCutaway`-Klasse ist bereits allgemein konfigurierbar und wird ohne C++-Änderung verwendet. Türschwelle **40×130×200 cm**, Weltzentrum **(-300,0,100) cm**, lokale +X-Richtung ins Haus. 4-cm-Hysterese und 0,4-s-Fade bleiben bestehen. CPD-Index 0 und maskierte Dither-Materialien sind übernommen; Dach, kameraseitige Fassaden, Fenster, Tür und zugehöriges Fachwerk sind konfiguriert. Kein Distanz-/Annäherungs-Fade.
15. **Spielkamera:** Live-Werte 2500 cm, FOV 35°, Winkel (-55°,-45°,0°), Lag-Geschwindigkeit 6 und maximal 180 cm, Player 140 cm und Bewegung 210 cm/s bleiben unverändert. Die private Tür, drei Fenster und kleine Regenhaube lesen sich kompakter als beim Heilhaus. Player bleibt innen/außen gut erkennbar; Holz/Putz/dunkles Fachwerk und Dach bleiben getrennt. Direkt vor der Fassade werden obere Dachbereiche unter der fest vorgegebenen playerzentrierten Kamera teilweise vom Bildrand abgeschnitten; Kamera/FOV werden dafür nicht verändert. Dies ist ein modularer Architektur-Proof, keine finale Welt-/Beleuchtungsinszenierung.
16. **PIE-Fußweg:** normaler Außenstart → Vorderseite → vor der Schwelle → gerade hinein → Mitte → mehrere diagonale Innenraumwege → diagonal hinaus → diagonal wieder hinein → gerade hinaus → zurück zum Start. Ausschließlich normale Slate-WASD-Eingaben, keine Teleports, keine Spawn-Overrides. Cutaway außen 0, vor Schwelle 0, innen 1, außen wieder 0. Freie Passage und Innenlaufwege bestanden. Auch die Modulgalerie wurde zu Fuß über vier Kontrollpunkte geprüft und anschließend zum Außenstart zurückgelaufen. Dach-/Fenster-/Strukturmodule sind sichtbar; die Galerie verwendet keine Collision. Screenshots und Positionen liegen in `GalleryPIE.json` sowie den Bildern 13–16.

## Prüfungen und Erhalt bestehender Systeme

17. Der Blender-Audit prüft alle 25 Module auf manifold Geometrie, vollständige Materialien, angewandte Origins/Rotation/Scale und fehlende externe Bibliothekslinks. Der Unreal-Audit prüft alle Mesh-Bounds gegen Meter→Zentimeter (3-mm-Toleranz), sämtliche 30 Material-Slots, gespeicherte Collision-Körper, 148 Instanzen und exakte Modulhäufigkeiten. Acht Kapsel-Laufsegmente plus diagonaler Türdurchgang sind frei; Front-/Rückwand und Fensterbrüstung blockieren. Map Check der neuen gespeicherten Map: **0 Fehler, 0 Warnungen**. Kein C++ verändert, daher kein C++-Build notwendig/ausgeführt. Der gesamte bestehende Automationstestbestand wurde anschließend in einem frischen Null-RHI-Prozess ausgeführt: **35 erfolgreich, 0 fehlgeschlagen, 0 mit Warnungen, 0 nicht ausgeführt**, Exit-Code 0. Darunter Player Foundation/ScaleCalibration, drei HealingHouse-Tests sowie Battle, Quest und Save. Abschließender Editor-Audit und Map Check wurden nach Stop PIE erneut ausgeführt und bestanden.

Gefundene und behobene Arbeitsfehler: Erste Fachwerk-Instanzen lagen zu tief im Putz und wurden nach der Blender-Sichtprüfung an die Außenflächen gesetzt. Legacy-FBX benötigt Slate und kann in dieser Engine im PythonScript-Commandlet abstürzen; der Import erfolgte danach erfolgreich im getrennten vollständigen Editor. Die erste Collision-Diagnose verwendete eine Funktion, die Convex-Körper ausdrücklich nicht mitzählt; sie wurde um `get_convex_collision_count` ergänzt. Die Körper waren bereits korrekt gespeichert. Python-Traces geben bei freier Strecke `None` zurück, keinen Bool/Hit-Tuple; der Audit wurde entsprechend korrigiert. Keine dieser Korrekturen erfordert Änderungen an bestehenden Gameplay-Systemen.

Nachweise liegen ausschließlich unter dem bereits ignorierten `Saved/WestlandKitV1`: Blender-Referenz-/Validierung, drei Blender-Renders, UnrealImport/RuntimeValidation, FootPIE/FootRoute, tatsächliche PIE-Bilder sowie abschließende Automationsergebnisse. Diese Arbeitsartefakte gehören nicht in Git.

18. Sämtliche neuen/geänderten versionierungswürdigen Dateien folgen unten. Bestehende Dateiänderungen sind auf die zwei Dokumente TECHNIK und ENTSCHEIDUNGEN beschränkt; alle anderen 557 Ausgangsdateien sind nach dem finalen Automationstest SHA-256-bytegleich geprüft. Insbesondere HealingHouse V3, Dev_TestMap, andere bestehende Maps, Player-/Kamera-/Input-/Gameplaycode bleiben unverändert.
19. **`git diff --check`: Exit-Code 0, keine Ausgabe.** Neue Python-Dateien sind per AST geparst, JSON-Dateien geladen und neue Markdown-/JSON-/Python-Dateien zusätzlich auf Schluss-Newline und trailing whitespace geprüft; alles bestanden.
20. Abschließendes `git status --short` steht unten. **67 neue Dateien, 2 ergänzte Dokumente**; nichts gestagt. HEAD bleibt `4b035cd`. Kein Commit oder Push.

Sinnvoller späterer Sicherungspunkt nach eigener Sichtfreigabe; hier nicht ausgeführt:

```sh
git diff --check
git status --short
git add Art/Architecture/Westland Content/Environment/Architecture/Westland Content/Maps/Dev_BuildingKitTestMap.umap Docs/TECHNIK.md Docs/ENTSCHEIDUNGEN.md Docs/WESTLAND_BUILDING_KIT_V1_PRUEFBERICHT.md Tools/Blender/*WestlandBuildingKitV1.py Tools/*WestlandBuildingKitV1.py
git commit -m "Add Westland building kit V1 and cottage proof"
```

## Vollständige Dateiliste

Alle folgenden Pfade sind relativ zum Projektstamm `/Users/harry/Developer/PokeMonster/Game/PokeMonster`. 67 neue Dateien:

```text
Art/Architecture/Westland/Buildings/WL_Cottage_V1.json
Art/Architecture/Westland/Exports/Modules/SM_WL_Chimney60cm.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_CornerPost3m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_DiagonalBrace1m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_DoorFrame130x200.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_DoorLeaf130x200.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_EaveTrim1m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_Floor1m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_GableHalf3m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_GableTrimHalf3m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_HorizontalBeam2m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_Porch160cm.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_RidgeCap1m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_RoofPanel1m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_RoofPanelEnd30cm.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_StonePlinth1m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_Threshold130cm.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_VerticalPost3m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_WallDoor2m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_WallSolid1m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_WallSolid2m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_WallWindowArch2m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_WallWindowDouble2m.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_WindowArch.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_WindowDouble.fbx
Art/Architecture/Westland/Exports/Modules/SM_WL_WindowRound.fbx
Art/Architecture/Westland/Source/WestlandBuildingKit_V1.blend
Art/Architecture/Westland/WestlandBuildingKit_V1.json
Content/Environment/Architecture/Westland/Materials/M_WL_Glass.uasset
Content/Environment/Architecture/Westland/Materials/M_WL_Metal.uasset
Content/Environment/Architecture/Westland/Materials/M_WL_Plaster.uasset
Content/Environment/Architecture/Westland/Materials/M_WL_Roof.uasset
Content/Environment/Architecture/Westland/Materials/M_WL_Stone.uasset
Content/Environment/Architecture/Westland/Materials/M_WL_Timber.uasset
Content/Environment/Architecture/Westland/Materials/M_WL_Wood.uasset
Content/Environment/Architecture/Westland/Meshes/Doors/SM_WL_DoorFrame130x200.uasset
Content/Environment/Architecture/Westland/Meshes/Doors/SM_WL_DoorLeaf130x200.uasset
Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_EaveTrim1m.uasset
Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_GableTrimHalf3m.uasset
Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RidgeCap1m.uasset
Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RoofPanel1m.uasset
Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RoofPanelEnd30cm.uasset
Content/Environment/Architecture/Westland/Meshes/Structural/SM_WL_Chimney60cm.uasset
Content/Environment/Architecture/Westland/Meshes/Structural/SM_WL_Floor1m.uasset
Content/Environment/Architecture/Westland/Meshes/Structural/SM_WL_Porch160cm.uasset
Content/Environment/Architecture/Westland/Meshes/Structural/SM_WL_StonePlinth1m.uasset
Content/Environment/Architecture/Westland/Meshes/Structural/SM_WL_Threshold130cm.uasset
Content/Environment/Architecture/Westland/Meshes/Timber/SM_WL_CornerPost3m.uasset
Content/Environment/Architecture/Westland/Meshes/Timber/SM_WL_DiagonalBrace1m.uasset
Content/Environment/Architecture/Westland/Meshes/Timber/SM_WL_HorizontalBeam2m.uasset
Content/Environment/Architecture/Westland/Meshes/Timber/SM_WL_VerticalPost3m.uasset
Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_GableHalf3m.uasset
Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_WallDoor2m.uasset
Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_WallSolid1m.uasset
Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_WallSolid2m.uasset
Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_WallWindowArch2m.uasset
Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_WallWindowDouble2m.uasset
Content/Environment/Architecture/Westland/Meshes/Windows/SM_WL_WindowArch.uasset
Content/Environment/Architecture/Westland/Meshes/Windows/SM_WL_WindowDouble.uasset
Content/Environment/Architecture/Westland/Meshes/Windows/SM_WL_WindowRound.uasset
Content/Maps/Dev_BuildingKitTestMap.umap
Docs/WESTLAND_BUILDING_KIT_V1_PRUEFBERICHT.md
Tools/Blender/BuildWestlandBuildingKitV1.py
Tools/Blender/ExportWestlandBuildingKitV1.py
Tools/Blender/ReviewWestlandBuildingKitV1.py
Tools/ImportWestlandBuildingKitV1.py
Tools/ValidateWestlandBuildingKitV1.py
```

Geändert (nur ergänzte Dokumentation):

```text
Docs/ENTSCHEIDUNGEN.md
Docs/TECHNIK.md
```

## Abschließender Git-Status

```text
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
?? Art/Architecture/
?? Content/Environment/Architecture/
?? Content/Maps/Dev_BuildingKitTestMap.umap
?? Docs/WESTLAND_BUILDING_KIT_V1_PRUEFBERICHT.md
?? Tools/Blender/BuildWestlandBuildingKitV1.py
?? Tools/Blender/ExportWestlandBuildingKitV1.py
?? Tools/Blender/ReviewWestlandBuildingKitV1.py
?? Tools/ImportWestlandBuildingKitV1.py
?? Tools/ValidateWestlandBuildingKitV1.py
```

Die kompakten `??`-Verzeichniseinträge oben enthalten ausschließlich die neuen Dateien der vollständigen Liste. Ignorierte Arbeitsnachweise unter `Saved/WestlandKitV1` und temporäre Logs unter `/private/tmp/WestlandKitV1` sind kein Bestandteil dieses Status. Die `.blend` ist eine echte neue Quelle, keine `.blend1`-Sicherung; die FBX-Dateien sind dauerhafte Reimport-Quellen.
