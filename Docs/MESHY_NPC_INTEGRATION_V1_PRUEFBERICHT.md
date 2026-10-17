# Meshy NPC Integration V1 – Prüfbericht

Stand: 15.10.2026. **Teilweise umgesetzt: ein stationärer NPC integriert, drei weitere Rig-Kandidaten importiert, sechs statische Prüfimporte. Keine Freigabe als zehn fertige animierte NPCs.**

## 1. Ausgangslage und Schutz

Ausgangs-HEAD: `351a3ef Add YoungTrainer sprint V1 and in-place run animation`. Anfangs ausschließlich zehn unversionierte GLBs in [Incoming](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Incoming). Keine GLTF-, FBX- oder ZIP-Eingänge. AGENTS und relevante Technik-, Stil-, Spielidee-, Spielregeln- und Entscheidungsunterlagen gelesen. Blender 5.2.2 LTS, Unreal 5.8.2/macOS.

1.927 Ausgangsdateien per SHA-256 geschützt. Verändert sind ausschließlich die erlaubte VisualV2-Karte, der lesende Dialog-Getter und die beiden ergänzten technischen Dokumente. Kein Ausgangsmodell, Player-/Animationsasset oder andere Karte verändert; keine Ausgangsdatei fehlt. Incoming bleibt bytegleich. Kein Commit, Push, Reset oder Staging.

## 2. Gefundene Modelle, Maße und Status

Alle Eingänge: GLB 2.0, ein Mesh, ein Material, drei eingebettete 2048×2048-JPEGs, kein Rig und keine Animation. Es sind **keine 4K-Texturen**. Importierte Vorderseite visuell als Blender −Y geprüft; Blender Meter, Unreal Zentimeter. Maße sind gesamte sichtbare Silhouetten einschließlich Hut/Waffen/Reitern, keine anatomisch verbindlichen Körperhöhen. Originale bleiben unverändert; nur neue Arbeitskopien wurden einheitlich pro Figur skaliert und auf den Boden gestellt.

| Originaldatei | Technische ID | Originalhöhe m → Arbeitsmaß m | Original Dreiecke / Vertices | UE-Dreiecke | Status |
|---|---|---:|---:|---:|---|
| Aragorn_V1.glb | Ranger | 1.8626 → 1.80 | 2,337,180 / 1,266,132 | 90,000 | vollständig integriert |
| Arwen_V1.glb | SilverLady | 1.9026 → 1.90 | 7,215,648 / 4,045,138 | 149,999 | Nacharbeit erforderlich |
| Baumbart_V1.glb | TreeBeing | 1.7985 → 3.80 | 2,385,308 / 1,297,268 | 150,000 | eingeschränkt verwendbar |
| Elrond_V1.glb | ElvenScholar | 1.9000 → 1.95 | 5,549,014 / 3,090,180 | 149,999 | Nacharbeit erforderlich |
| Gandalf_V1.glb | Wizard | 1.8792 → 2.05 | 2,296,550 / 1,229,725 | 150,000 | Nacharbeit erforderlich |
| Geralt_V1.glb | WhiteHairedWarrior | 1.8421 → 1.85 | 1,794,254 / 946,699 | 90,000 | importiert, aber noch nicht eingebunden |
| Gimli_V1.glb | DwarfWarrior | 1.7709 → 1.32 | 3,984,350 / 2,169,452 | 90,000 | importiert, aber noch nicht eingebunden |
| Gollum_V1.glb | CrouchedCreature | 1.6377 → 1.10 | 793,382 / 437,732 | 150,000 | Nacharbeit erforderlich |
| Legolas_V1.glb | ElvenArcher | 1.8783 → 1.95 | 2,269,806 / 1,250,242 | 90,000 | importiert, aber noch nicht eingebunden |
| Sauron_V1.glb | DarkArmored | 1.7035 → 2.25 | 3,482,656 / 1,898,546 | 150,000 | Nacharbeit erforderlich |


Orangehaarige Trainerin, Trainer mit Kappe und Trainer mit grüner Weste fehlen. Stattdessen liegen ElvenScholar, WhiteHairedWarrior und CrouchedCreature vor. Keine erfundene Trainerzuordnung. Dateinamen begründen technische Arbeitsnamen, keine neuen Storyidentitäten.

## 3. Blenderquellen und Exporte

Jede Figur besitzt Source, Exports, Textures und Previews in einem eigenen neuen Ordner. Die importierte High-Poly-Referenz mit gepackten Originaltexturen bleibt innerhalb der neuen Quellen erhalten.

| Figur | Unabhängige Importquelle | Weiterer Arbeitsstand |
|---|---|---|
| Ranger | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Source/Ranger_NPC_Source_V1.blend) | [Ranger_NPC_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Source/Ranger_NPC_V1.blend) |
| SilverLady | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/SilverLady/Source/SilverLady_NPC_Source_V1.blend) | [SilverLady_NPC_StaticReview_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/SilverLady/Source/SilverLady_NPC_StaticReview_V1.blend) |
| TreeBeing | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/TreeBeing/Source/TreeBeing_NPC_Source_V1.blend) | [TreeBeing_NPC_StaticReview_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/TreeBeing/Source/TreeBeing_NPC_StaticReview_V1.blend) |
| ElvenScholar | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenScholar/Source/ElvenScholar_NPC_Source_V1.blend) | [ElvenScholar_NPC_StaticReview_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenScholar/Source/ElvenScholar_NPC_StaticReview_V1.blend) |
| Wizard | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Wizard/Source/Wizard_NPC_Source_V1.blend) | [Wizard_NPC_StaticReview_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Wizard/Source/Wizard_NPC_StaticReview_V1.blend) |
| WhiteHairedWarrior | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/WhiteHairedWarrior/Source/WhiteHairedWarrior_NPC_Source_V1.blend) | [WhiteHairedWarrior_NPC_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/WhiteHairedWarrior/Source/WhiteHairedWarrior_NPC_V1.blend) |
| DwarfWarrior | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DwarfWarrior/Source/DwarfWarrior_NPC_Source_V1.blend) | [DwarfWarrior_NPC_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DwarfWarrior/Source/DwarfWarrior_NPC_V1.blend) |
| CrouchedCreature | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/CrouchedCreature/Source/CrouchedCreature_NPC_Source_V1.blend) | [CrouchedCreature_NPC_StaticReview_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/CrouchedCreature/Source/CrouchedCreature_NPC_StaticReview_V1.blend) |
| ElvenArcher | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenArcher/Source/ElvenArcher_NPC_Source_V1.blend) | [ElvenArcher_NPC_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenArcher/Source/ElvenArcher_NPC_V1.blend) |
| DarkArmored | [Quelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DarkArmored/Source/DarkArmored_NPC_Source_V1.blend) | [DarkArmored_NPC_StaticReview_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DarkArmored/Source/DarkArmored_NPC_StaticReview_V1.blend) |


Zehn Importquellen und vier Rig-Master vollständig erneut geöffnet: je drei gepackte Texturen, erwartete Mesh-/Rig-Struktur, beide gespeicherten Aktionen vorhanden. Neun zusätzliche statische Reviewdateien über Blender-Datenblöcke lesend validiert; TreeBeing zusätzlich vollständig geöffnet. Vollständige erneute Szenenevaluierung aller statischen Dateien nicht abgeschlossen: das Laden berechnet den teuren unapplizierten Decimate erneut. Eigene rein lesende Prüfprozesse wurden abgebrochen, keine Datei gespeichert oder beschädigt. Dies wird nicht als neun vollständig geprüfte Szenenöffnungen ausgegeben.

FBX-Dateien: pro humanoidem Kandidaten SK und getrennte Idle-/Talk-Dateien im jeweiligen Exports-Ordner. Sechs tatsächlich nach Unreal importierte statische FBX-Prüfdateien. Drei zusätzliche statische Reviewexporte der später geriggten Modelle bleiben als Arbeitsartefakte erhalten.

## 4. Geometrie- und Materialanalyse

Die Millionen-Polygon-Originale sind nicht als Runtime-NPCs eingesetzt. Humanoide Runtimekopien: 90.000 Dreiecke, UVs/Material erhalten, gezieltes Zusammenführen identischer Nahtpositionen und kontrollierter Reduktionsversuch. Dies ist **keine animationsfertige Quad-Retopologie**. Statische Prüfkopien: rund 150.000 Dreiecke mit reversiblem Decimate-Modifikator; gerade SilverLady zeigt sichtbar schlechtere Stoff-/Oberflächenformen.

Die Quellen enthalten viele technisch getrennte UV-/Normalennähte. Rohkomponenten → Komponenten nach ausschließlich analytischem Zusammenfassen exakt gleicher Positionen:

| Figur | Rohkomponenten | nach Nahtanalyse |
|---|---:|---:|
| Ranger | 2,793 | 1 |
| SilverLady | 14,599 | 2 |
| TreeBeing | 2,349 | 1 |
| ElvenScholar | 11,149 | 3 |
| Wizard | 1,875 | 1 |
| WhiteHairedWarrior | 1,017 | 1 |
| DwarfWarrior | 4,090 | 1 |
| CrouchedCreature | 1,214 | 4 |
| ElvenArcher | 3,977 | 2 |
| DarkArmored | 4,494 | 1 |


Keine isolierten Kanten, Flächen mit mehr als zwei angrenzenden Faces, Nullflächen oder nichtendlichen Koordinaten in den protokollierten Quellenchecks. Viele rohe Randkanten sind Nahtartefakte und **kein Beweis für offene Löcher**. Vollständiger Selbstüberschneidungs- und semantischer Trennungstest nicht durchgeführt. Die Reiter des Baumwesens sind keine eigenständigen Meshobjekte; nach Nahtanalyse eine verbundene Geometrie.

Unreal: ein neuer gemeinsamer opaker, zweiseitiger Materialparent, zehn Instanzen, drei Texturen je Figur. Base Color sRGB, Normal/Roughness-Metallic linear, OpenGL-Normalgrün für Unreal umgekehrt. Roughness aus G, Metallic aus B entsprechend dem tatsächlichen glTF-Graphen. Keine willkürlichen Rollen nach Bildnummern. Die fehlende Skeletal-Mesh-Nutzung der drei Reserve-Materialinstanzen wurde diagnostiziert, explizit gesetzt, neu kompiliert und gespeichert; danach farbige Spielkameraansichten geprüft.

## 5. Rigging und Animationen

Der existierende Player-Workflow wurde gelesen und als technische Vorlage genutzt; Playerquellen, Rig und Animation Quality V2 bleiben unverändert. Ranger besitzt ein eigenständiges 24-Bone-Rig. WhiteHairedWarrior und ElvenArcher besitzen kompatible Kernbenennung, eigene Gelenkpositionen, Gewichte und Skeletons; DwarfWarrior 25 Bones mit zusätzlichem Bartknochen. Kein ungeprüftes Player-Retargeting und kein menschliches Standardskelett für den Ent.

Viermal Idle (3 s) und Talk (2 s), 30 fps, auf der Stelle. Blender-Auswertung über jeweils 91 bzw. 61 Frames; kein negativer gemessener Sohlen-Minimalwert. Sanfter Gesprächsblend 0,18 s, Blickwendung nur am Darstellungsactor. Die ursprünglichen regionalen Sleeve-Spitzen wurden am Ranger durch gezielte Korrektur von 6.923 Vertices behoben; 410 rückwärtige Schwertvertices fest zugeordnet. Beim Bogenschützen 3.307 Ausrüstungsvertices nachkorrigiert. Fehlender Fake User der drei Talk-Aktionen behoben, Aktionen nach erneutem Öffnen nachgewiesen.

**Nicht vorhanden/geprüft:** NPC-Walk, acht bewegte NPC-Richtungen, NPC-Foot-Sliding bei einer Bewegungsgeschwindigkeit, vollständige dynamische Umhang-/Taschen-/Haar-Nachläufe, Finger-/Gesichtsanimation. Alle vorhandenen Zielrollen stehen still; deshalb wurde keine neue NPC-Fortbewegung eingeführt. Die acht Player-Richtungen wurden im Fußlauf geprüft. Accessoiregewichte und kleine vorhandene Knochenbewegungen ersetzen keine vollständig abgenommene Stofflösung.

## 6. Tatsächliche Unreal-Einbindung

Bearbeitete Karte: `/Game/Maps/Dev_TestMap_VisualV2`. Ausschließlich `Slice_Wanderer_Hinweis` erhält `NPCVisual_Wanderer_Ranger_V1` als angehängte Darstellung. Original-NPC: Position (−920, −1080, 65) cm, Name Wanderer, DA_SliceGuideDialogue und Interaktionskapsel unverändert. Visuelle Füße (−920, −1080, 3) cm. Kein zusätzlicher Gameplay-Collider oder Navigationseinfluss.

Die Spielkamera-Prüfung fand einen Python-Rotator-Fehler: anfänglich Pitch −45 statt gewünschter Yaw. Auf explizite Schlüsselwörter korrigiert; finale Darstellung Pitch 0, Yaw 135, Roll 0. Im Gespräch dreht die vorhandene neue Präsentationsfunktion horizontal zum Player.

Archivarin, Liora und Heilerin behalten Identität, Position und Darstellung. Kein passender männlicher Gelehrter oder Zwergen-Dorfbewohner vorhanden; die Vorschlagsrollen wurden nicht erzwungen. Original Dev_TestMap, Dev_WestlandRegion und Dev_WestlandAssetLibrary sind bytegleich.

Neue UE-Ablage: `/Game/Characters/NPCs/<ID>/Meshes`, `Materials`, `Textures`, für die vier Humanoiden zusätzlich `Animations`. 63 Assets: zehn Meshes, vier Skeletons, acht AnimSequences, zehn MIs, dreißig Texturen, ein gemeinsamer Parent. Keine Physics Assets, keine Gameplay-ABPs ersetzt. Native neue AnimInstance statt unnötigem Blueprint-Duplikat.

## 7. Nicht eingebundene Modelle


- **SilverLady – Nacharbeit erforderlich:** Nur statischer Prüfimport; sichtbare Reduktionsartefakte, Kleid und weite Ärmel nicht sicher geriggt.

- **TreeBeing – eingeschränkt verwendbar:** Nur statischer Prüfimport; eigenes Baum-Rig und Reitertrennung offen.

- **ElvenScholar – Nacharbeit erforderlich:** Nur statischer Prüfimport; lange Kleidung/weite Ärmel benötigen kontrollierte Gewichte.

- **Wizard – Nacharbeit erforderlich:** Nur statischer Prüfimport; Bart, Mantel, Hut und Taschen brauchen eigene Zuordnung.

- **WhiteHairedWarrior – importiert, aber noch nicht eingebunden:** Stationärer Rig-Kandidat; keine passende bestehende Rolle.

- **DwarfWarrior – importiert, aber noch nicht eingebunden:** Stationärer Rig-Kandidat mit eigenem Bartknochen; kein passender Dorfbewohner.

- **CrouchedCreature – Nacharbeit erforderlich:** Nur statischer Prüfimport; abweichende Haltung/Anatomie benötigt eigenes Rig.

- **ElvenArcher – importiert, aber noch nicht eingebunden:** Stationärer Rig-Kandidat; hintere Haare/Ausrüstung nur grob gewichtet.

- **DarkArmored – Nacharbeit erforderlich:** Nur statischer Prüfimport; Schulterpanzer/Umhang nicht für Standardgewichte freigegeben.

## 8. Echte visuelle Nachweise

Alle zehn Figuren: echte Blender-Front-, rechte Seiten- und Dreiviertelrenderings. Alle vier humanoiden Kandidaten zusätzlich aus der unveränderten Unreal-Spielkamera aufgenommen. Reservefiguren wurden dafür nur temporär am eigenen Präsentationsactor in einer verworfenen PIE-Sitzung gezeigt; keine zusätzliche Figur in der Karte gespeichert. Sechs statische Kandidaten besitzen **keine tatsächliche Unreal-Spielkamera-Abnahme**.

Die unten verlinkten letzten Aufnahmen enthalten die korrigierte Ausrichtung und Materialien. Frühere fehlerhafte/diagnostische Bilder bleiben zur Nachvollziehbarkeit erhalten und gelten nicht als Abnahme. Keine Konzeptbilder als Unreal-Nachweis.


- **Ranger:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Previews/03_ThreeQuarter.png); [finale Spielkamera](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Previews/Unreal_Validated_GameCamera00004.png)

- **SilverLady:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/SilverLady/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/SilverLady/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/SilverLady/Previews/03_ThreeQuarter.png); Spielkamera offen.

- **TreeBeing:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/TreeBeing/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/TreeBeing/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/TreeBeing/Previews/03_ThreeQuarter.png); Spielkamera offen.

- **ElvenScholar:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenScholar/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenScholar/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenScholar/Previews/03_ThreeQuarter.png); Spielkamera offen.

- **Wizard:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Wizard/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Wizard/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Wizard/Previews/03_ThreeQuarter.png); Spielkamera offen.

- **WhiteHairedWarrior:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/WhiteHairedWarrior/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/WhiteHairedWarrior/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/WhiteHairedWarrior/Previews/03_ThreeQuarter.png); [finale Spielkamera](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/WhiteHairedWarrior/Previews/Unreal_Validated_GameCamera00003.png)

- **DwarfWarrior:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DwarfWarrior/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DwarfWarrior/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DwarfWarrior/Previews/03_ThreeQuarter.png); [finale Spielkamera](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DwarfWarrior/Previews/Unreal_Validated_GameCamera00003.png)

- **CrouchedCreature:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/CrouchedCreature/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/CrouchedCreature/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/CrouchedCreature/Previews/03_ThreeQuarter.png); Spielkamera offen.

- **ElvenArcher:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenArcher/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenArcher/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenArcher/Previews/03_ThreeQuarter.png); [finale Spielkamera](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/ElvenArcher/Previews/Unreal_Validated_GameCamera00003.png)

- **DarkArmored:** [Blender Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DarkArmored/Previews/01_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DarkArmored/Previews/02_Right.png), [3/4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/DarkArmored/Previews/03_ThreeQuarter.png); Spielkamera offen.


Weitere Rundwegaufnahmen, Dialog und Bildsequenzen: [PIE-Nachweise](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/MeshyNPCIntegrationV1). Alle exakten Bildpfade: [Screenshotindex](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/FinalScreenshots.json). Video nicht erstellt. Figuren wirken detailreicher und realistischer als die malerische Umgebung; Material-/Stilangleichung bleibt offen. Dunkle Kleidung im Waldschatten ist aus großer Entfernung weniger lesbar.

## 9. Performance

Embedded Editor-PIE, Medium, 75 %, VSync aus, unlimitiert. Je Ort 5 s Warmlauf und 15 s Messfenster, gleiche Route ohne Testteleports. **1280×740 wurde angefordert, der eingebettete Viewport blieb tatsächlich 2331×1346.** Daher kein behaupteter 1280×740-Vergleich. Gleiche tatsächliche Auflösung für Vorher/Nachher; Wald-/Wegpositionen wegen Fußsteuerung um wenige cm verschieden.

| Ort | Vorher FPS | final Nachher FPS | mediane Framezeit vorher → nachher ms |
|---|---:|---:|---:|
| Dorf | 26.75 | 23.48 | 35.88 → 42.77 |
| Wald | 26.03 | 23.27 | 38.01 → 43.45 |
| OffenerWeg | 27.22 | 24.32 | 35.48 → 40.77 |


Gemessene Verschlechterung; keine erfolgreiche Performanceoptimierung behauptet. Finaler GPU-Median Dorf/Wald/Weg etwa 39,01 / 39,21 / 36,74 ms, Game Thread 6,45 / 6,23 / 6,19 ms. GPU-Schatten-Depths etwa 1,72 / 1,71 / 1,58 ms; Shadow Projection 2,51 / 2,49 / 2,20 ms. Animationsanteil am Game Thread rund 0,05–0,06 ms. CSV-Draw-Call-Werte konstant 0 und RenderThread-Zeiten nahezu 0 sind hier nicht belastbar und werden nicht als echte Nullkosten ausgegeben.

Zusätzlicher direkter NPC-an/aus-Test: aus 23,98/23,63 FPS, an 23,54/22,54 FPS. Keine sichere Trennung von GPU-Last, Speicher-/Temperaturdrift und NPC-Kosten aus diesen kurzen Läufen; keine kausale Zuschreibung des gesamten Langzeitverlusts. Keine pauschale Qualitätsreduktion. Animation nur bei Sichtbarkeit, Update-Rate-Optimierung und Actor-Tick nur während Blickwendung; keine LOD-Kette oder Animation-Sharing-Abnahme. Statische Prüfimporte sind nicht in der Welt platziert. Standalone-Messung offen. Rohdaten: [Performancezähler](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/PerformanceCounters.json).

## 10. PIE-Fußlauf und Save/Load

Zweimal vollständiger echter eingebetteter PIE-Fußlauf über vorhandenes Enhanced Input, ohne Test-Teleports. Final nach Ausrichtungskorrektur: 264.26 m, 190.33 s reale Zeit, maximal gemessen 210.000 cm/s. Der reguläre Heilhaus-Innenraumwechsel nutzt weiterhin die bestehende Relocation.

Bestanden: Menü-/Dialog-Eingabesperre und Freigabe, Wanderer/Queststart, Wildkampf/Fangen, Liora-Sieg, Questaktualisierung, Save/Load vor dem Archiv, Archivflag/Questabschluss, Rückkehrdialog, Dorf-/Brücken-/Waldwege, Heilhaus gerade und diagonal hinein/hinaus, Cutaway, Heilerin, volle HP/PP, Checkpoint/Save, acht Player-Richtungen, Anhalten und Kronenfreistellung. Ranger-Gesprächszustand und Blend-Alpha im echten Dialog geprüft. Keine neuen Kollisionen/verschobenen Interaktionspunkte gefunden.

Dev-Spielstand vor Tests gesichert und am Ende bytegleich wiederhergestellt (SHA-256 `626d58c2f512b3c63f90a18537fd646f611adecb76d52827428a67f578bbd21e`). Spielerhöhe 140 cm, Kamera 2850/−50/−45/FOV35, Eingaben, Bewegungs-/Sprintsystem und Playeranimationen unverändert. Kein Test neuer NPC-Lokomotion, weil nicht implementiert. Foot-Ergebnis: [FootTest.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/MeshyNPCIntegrationV1/FootTest.json).

## 11. Build und Automation

Mac Development Editor Build erfolgreich, 67,96 s. Neue Darstellungsklassen plus ein Test; einzig bestehender Codeeingriff ist der Blueprint-lesende `GetActiveSource()` am Dialogsubsystem mit benötigtem Actor-Include. Keine Dialogentscheidung oder Battle-/Save-Regel geändert.

Erster Editor-Gesamtlauf 43/43 erfolgreich. Wiederholung in der langen Editor-Sitzung 42/43: `Battle.Session.ValidationAndReplay` traf beim Garbage Collect auf einen noch initialisierten LandscapeSubsystem aus Dev_HealingHouseTestMap. Zusätzlich alte Engine-Toolwarnung zum idevice_id-Executable. Nicht verschwiegen und nicht durch Gameplayänderung unterdrückt. Abschließender frischer Unreal-Prozess mit NullRHI: **43 erfolgreich, 0 Fehler, 0 Warnungstests, 0 nicht ausgeführt**; 3,50 s reine Testdauer. NullRHI ersetzt nicht die separat durchgeführten visuellen PIE-Tests.

Neuer Test `PokeMonster.NPC.PresentationAndFallback`: eigene Mesh-/Clip-Skeleton-Kompatibilität, keine Root Motion, keine neue Collision, kein permanenter Actor-Tick, erhaltener NPC-Transform, Sprite-Fallback. Ergebnisse: [frischer Gesamtlauf](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/AutomationCleanResults.json) und [Editor-Wiederholung mit Ensure](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/AutomationFinalResults.json).

## 12. Map Check und Importwarnungen

Finaler Map Check der VisualV2: **0 Fehler, 0 Warnungen**. Keine fremden schmutzigen Content-Pakete oder Maps beim finalen Audit.

Die sechs statischen Prüfimporte melden jeweils nahezu null Tangenten und Bi-Normalen, insgesamt zwölf entsprechende Warnungen. Nicht unterdrückt, nicht als behoben erklärt. Im FBX-UV-Audit sind je nach Modell 130–234 Dreiecke mit sehr kleinem UV-Determinanten (<1e−8), keine nichtendlichen UV-Werte und keine Determinanten <1e−12 gemessen. Das ist ein konkreter Ansatz für die Tangentenreparatur, noch kein vollständiger Ursachenbeweis oder Reparaturnachweis. Diese Assets bleiben eingeschränkt/Nacharbeit. Vier Skeletal-Importe ohne diese statischen Tangentenwarnungen.

Blender meldete beim ursprünglichen Packen teils leere externe Image-Pfade und behielt die gepackten Daten; erneute Prüfung bestätigt drei gepackte Bilder mit 2048² und vorhandene neue externe JPEGs. Material-Nutzungswarnungen wurden wie in Abschnitt 4 tatsächlich behoben. Alte API-/Diagnosefehler und der erste verworfene Rig-Pilot sind in den Arbeitsprotokollen erhalten. [Logaudit](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/FinalLogAudit.json), [FBX-UV-Audit](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/StaticFBXUV.json).

## 13. Offene Qualität und Animation Quality V3

Priorität: manuelle Kleid-/Ärmel-/Ausrüstungsgewichte, verlässliche Tangenten, dann bedarfsgerechte LODs mit Silhouettenvergleich und erneutem Budgettest. Für bewegte Rollen erst passende Walk-Zyklen pro Körperbau/Tempo, Fußkontakte und kontrollierte Umhang-/Taschen-Nachläufe entwickeln. Kein globales Übertragen der Player-210-cm/s-Animation. Baumwesen benötigt eigenes Rig und separat geprüfte Reiterbehandlung. Finger- und spätere Gesprächsgesten benötigen zusätzliche Freigabe/geeignete Knochen. Lange Haare des Bogenschützen sind im korrigierten hinteren Ausrüstungsband überwiegend brustgeführt.

90k-Dreiecks-Humanoide und 150k-Static-Prüfstände sind keine abschließend optimierten Produktions-NPCs. Die realistische Rüstungs-/Texturoptik passt noch nicht vollständig zum handgemalten Westland. Keine zusätzlichen Storyrollen oder Traineridentitäten anlegen, bevor passende Originalmodelle vorliegen.

## 14. Änderungen und Dateinachweis

Bestehende Dateien geändert:

- [Content/Maps/Dev_TestMap_VisualV2.umap](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Content/Maps/Dev_TestMap_VisualV2.umap)
- [Source/PokeMonster/Dialogue/PokeMonsterDialogueSubsystem.h](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Source/PokeMonster/Dialogue/PokeMonsterDialogueSubsystem.h)
- [Docs/TECHNIK.md](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Docs/TECHNIK.md)
- [Docs/ENTSCHEIDUNGEN.md](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Docs/ENTSCHEIDUNGEN.md)

Neu: vier native Darstellungsdateien, ein Automationstest, dieses Dokument, zehn Figurenordner mit Quellen/Exporten/Texturen/Previews, 63 Unreal-Assets und [reproduzierbare Integrationswerkzeuge](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/MeshyNPCIntegrationV1). [Arbeitsnachweise](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1) enthalten Audits, verworfene Pilotbilder und Messdaten. Automatische neue `.blend1`-Sicherungen und Logs bleiben unangetastet; sie sind keine zusätzliche Assetfreigabe. Incoming war schon am Anfang unversioniert und bleibt unverändert.

Vollständige Datei- und Assetlisten werden in [Files.txt](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/Files.txt) und [FinalEditorAudit.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/FinalEditorAudit.json) geführt. LFS-Regeln für neue `.blend` und `.uasset` geprüft: `filter=lfs`. Nichts gestaged.

## 15. Git-Prüfung und Abschluss

`git diff --check` erfolgreich, keine Ausgabe. Der vollständige abschließende Git-Status steht unten und zusätzlich in [GitStatus.txt](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/IntegrationV1/GitStatus.txt). Kein Commit oder Push. Das Ergebnis bleibt zur visuellen Prüfung offen; insbesondere sechs statische Modelle und NPC-Walk sind nicht abgeschlossen.

```text
 M Content/Maps/Dev_TestMap_VisualV2.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Dialogue/PokeMonsterDialogueSubsystem.h
?? Art/Characters/NPCs/CrouchedCreature/
?? Art/Characters/NPCs/DarkArmored/
?? Art/Characters/NPCs/DwarfWarrior/
?? Art/Characters/NPCs/ElvenArcher/
?? Art/Characters/NPCs/ElvenScholar/
?? Art/Characters/NPCs/Incoming/
?? Art/Characters/NPCs/IntegrationV1/
?? Art/Characters/NPCs/Ranger/
?? Art/Characters/NPCs/SilverLady/
?? Art/Characters/NPCs/TreeBeing/
?? Art/Characters/NPCs/WhiteHairedWarrior/
?? Art/Characters/NPCs/Wizard/
?? Content/Characters/NPCs/
?? Docs/MESHY_NPC_INTEGRATION_V1_PRUEFBERICHT.md
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.h
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.h
?? Source/PokeMonster/Tests/PokeMonsterNPCPresentationTest.cpp
?? Tools/MeshyNPCIntegrationV1/
```
