# Westland Hobbit NPC – unabhängige Meshy-Basis V1

14.10.2026 · Ausgangs-HEAD `3c6dc47`.

## Ergebnis

Eine vollständige, eigenständige Blender-Kopie des vorhandenen Meshy-Spielers wurde erstellt und separat erneut geöffnet. Mesh, UVs, Gewichte, Rig und vorhandene Animationen bleiben unverändert. **Die Kopie ist eine untersuchte Ausgangsbasis, noch kein fertiges modulares Erwachsenen-NPC-System.** Besonders die fragmentierte Geometrie sowie die gemeinsame Körper-/Kleidungs-/Haarstruktur erfordern weitere Modellierungsarbeit.

Master: [Hobbit_NPC_MeshyBase_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_MeshyBase_V1.blend).

Der Master behält für diesen ausdrücklich auf Kopieren und Prüfen begrenzten Schritt die ursprüngliche **1,40-m-Referenzhöhe einschließlich Haaren** bei. Die geplante NPC-Standardhöhe **1,32 m** ist dokumentiert und lediglich in einem ungespeicherten Prüfprozess getestet, nicht als Umgestaltung des Masters umgesetzt. Keine Proportionsänderung, kein neuer Körper, keine Kleidungstrennung und kein Retopologie-/Rigging-Pass.

## Verwendete Quellen und tatsächliche Unreal-Referenzen

AGENTS.md, relevante Projektunterlagen, Meshy-V2- und Sprint-Prüfbericht sowie die aktuellen Player-/Animationsdateien wurden gelesen. Der vorhandene Arbeitsbaum enthält offene Player-/Sprint-Arbeiten; diese wurden vollständig bewahrt.

- Ursprüngliches Meshy-Modell: `Art/Characters/YoungTrainer/Source/Player_Meshy_V1.blend`.
- Funktionierende erste Bearbeitung: `Player_Meshy_GameReady_V1.blend`.
- Aktuelle V2-Mesh-/Rig-/Idle-/Walk-Quelle: [Player_Meshy_AnimationQuality_V2.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend).
- Jüngste ergänzte Arbeitsquelle: [Player_Meshy_Sprint_V1.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer/Source/Player_Meshy_Sprint_V1.blend). Sie enthält das unveränderte V2-Mesh/Rig, aber nur die Run-Action. Sie wurde für Mesh, Rig, Materialien, Texturen und Run kopiert; Idle/Walk wurden zusätzlich aus V2 angehängt und unabhängig kopiert.

Die aktuellen C++-Standardreferenzen der `PokeMonsterMeshyVisualComponent` und die gespeicherten Asset-Referenzen stimmen überein:

| Verwendung | Unreal-Asset |
| --- | --- |
| Mesh | `/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2` |
| Skeleton | `/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2_Skeleton` |
| Idle | `/Game/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Idle_V2` |
| Walk | `/Game/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Walk_V2` |
| Run | `/Game/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Run_V1` |
| Material | `/Game/Characters/YoungTrainer/MeshyV1/Materials/M_Player_Meshy` |

Die Import-Metadaten der gespeicherten `.uasset`-Dateien wurden lesend geprüft. Mesh, Idle und Walk referenzieren die vorhandenen FBX-Dateien unter `Art/Characters/YoungTrainer/Exports/MeshyV2/`, Run sein FBX unter `Exports/SprintV1/`. Alle vier aktuellen FBX-Dateien stimmen per MD5 mit den gespeicherten Import-Hashes überein. [Rohbeleg](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/UnrealStoredReferences.json).

**Prüfgrenze:** Eine frische Live-Abfrage des laufenden Unreal-Players war nicht möglich: keine vorhandene Remote-Python-Sitzung wurde entdeckt. Keine Verbindungseinstellungen geändert, kein weiterer Editor gestartet und kein PIE gestartet. Der aktuelle Code und gespeicherte Assets sind geprüft; mögliche ungespeicherte Runtime-Overrides sind hier nicht bestätigt. Ältere erfolgreiche PIE-Berichte werden nicht als neu durchgeführter Test ausgegeben.

## Eigenständigkeit der Kopie

Neue lokale Datenblöcke mit `HNM1_`-Präfix:

- Ein Mesh-Objekt `HNM1_Body` mit eigener Mesh-Datenstruktur und unveränderten Vertexgruppen/Gewichten/UVs.
- Eine Armature `HNM1_Rig` mit eigener Armature-Datenstruktur; unveränderte Bone-Namen und Elternhierarchie für Animationskompatibilität.
- Eigene Materialkopie, eigener Node Tree und eigene Image-Datenblöcke.
- Drei eigene Animations-Actions: `HNM1_Idle_V2`, `HNM1_Walk_V2`, `HNM1_Run_V1`; die Action-Slots sind an die kopierte Armature gebunden. Keine Überschreibung der Spielerclips.
- Drei gepackte 2048 × 2048-Texturen: BaseColor (sRGB), Normal und ORM (Non-Color). Zusätzlich separate PNG-Dateien unter `Art/Characters/NPCs/Westland/HobbitBase/Textures/MeshyBaseV1/`; relative Bildpfade zeigen ausschließlich dorthin, nicht zu Spielertexturen.
- Eigenständige Review-Kamera, Welt und Studiolichter. `HNM1_MODEL_RIG` und `HNM1_REVIEW_STUDIO` trennen Modell und Prüfung.

Keine extern verlinkten Modell-Datenblöcke. Parent und Armature-Modifier referenzieren das kopierte Rig. Original-Spielerszenen und Hobbit V1–V4 bleiben im geöffneten Blender erhalten. Keine vorhandene unsaved Szene durch Laden einer anderen Hauptdatei verworfen.

Der Master wird in **REST** angezeigt, damit die Ausgangsform überprüfbar bleibt. Für Animationen im Armature-Data-Tab **Pose Position** einstellen, passende `HNM1_`-Action wählen und bei 60 fps abspielen. Die Vorschau-Prüfung hat dies ausdrücklich mit korrektem Action-Slot getan. Master und Originalaktionen wurden dabei nicht verändert.

## Rig und Animationen

**25 Bones**, davon:

- `root`, `pelvis`, `spine`, `chest`, `neck`, `head`.
- Je Seite: `clavicle`, `upperarm`, `lowerarm`, `hand`, `thigh`, `shin`, `foot`.
- Zubehör: `cape_upper`, `cape_lower`, `cape_left`, `cape_right`, `bag`.

Keine einzelnen Finger-/Zehenbones, keine Gesichts-/Augen-/Lidbones und kein getrenntes universelles Clothing-Rig. Die vorhandene Zubehörhierarchie ist auf den Spielerumhang und die Tasche zugeschnitten. Rig und Gewichte sind für die vorhandenen Clips technisch wiederverwendbar, nicht bereits für beliebige erwachsene Körperformen freigegeben.

| Kopierter Clip | Frames bei 60 fps | Dauer |
| --- | ---: | ---: |
| Idle V2 | 1–181 | 3,00 s |
| Walk V2 | 1–34 | 0,55 s |
| Run V1 | 1–28 | 0,45 s |

Alle **243 gespeicherten Clipframes** an der tatsächlich verformten Mesh-Geometrie geprüft. Keine ungültigen Bone-Action-Pfade und keine nicht endlichen Vertexkoordinaten. Root-Translation 0 m. Die erfassten linken/rechten Sohlenvertices bleiben mindestens ungefähr **0,000500 m = 0,05 cm** über Blender-Z=0. Dies ist eine Quellenaudit-Prüfung, keine Garantie für Terrain, Beschleunigungen, neue Körperproportionen oder Animation-Blending in Unreal.

Ausgewählte Idle-/Walk-/Run-Posen zusätzlich tatsächlich gerendert und visuell geprüft. Schulter/Ärmel, Ellenbogen, Hüfte und Knie bewegen sich; eine saubere universelle Gelenktopologie ist dadurch nicht bewiesen. In den Kniefaltungen und an Haut-/Stoffgrenzen sind Risse und kantige Übergänge sichtbar. Keine vollständige Winkelbereichs-, Selbstüberschneidungs- oder Kontaktprüfung. Die zusätzlichen Umhang-/Taschenfedern des C++-Players wurden **nicht** in Blender dupliziert; die Action-Bewegung ist vorhanden, aber die dynamische Unreal-Sekundärbewegung ist kein Bestandteil dieser Blenderquelle.

## Geometrie- und Kopierprüfung

[Rohprüfung aus erneut geöffneter NPC-Datei](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/ReopenAudit.json).

| Merkmal | Ergebnis |
| --- | ---: |
| Mesh-Objekte | 1 |
| Vertices | 52.699 |
| Flächen / Dreiecke | 47.744 / 47.744 |
| Materialslots / UV-Layer | 1 / 1 (`UVMap`) |
| Ungewichtete Vertices | 0 |
| Maximale Bone-Einflüsse | 3 |
| Maximale Abweichung der Gewichtssumme von 1 | 0,00000981 |
| Degenerierte Flächen | 0 |
| Lose Vertices | 2.625 |
| Offene Kanten | 45.476 |
| Non-Manifold-Kanten | 47.634 |
| Topologische Komponenten vor Nahtanalyse | 3.949 |

**Die hohen Fragment-/Kantenzahlen sind vorhandene Quelldefizite, kein Schaden durch die Kopie:** Positions-/Polygon-/Gewichts-/UV-Hash stimmt exakt mit der Sprintquelle überein; Positionen/Gewichte und Bone-Hierarchie stimmen zusätzlich mit der aktuellen V2-Quelle überein. Das Mesh ist ausdrücklich keine zusammenhängende saubere Körper-Quadtopologie.

Zur Unterscheidung zwischen gesplitteten Nähten und tatsächlicher Fragmentierung wurde ausschließlich in einem ungespeicherten BMesh mit 1-µm-Toleranz verschweißt: weiterhin **3.798 Komponenten, 45.414 offene Kanten und 47.572 Non-Manifold-Kanten**. Die Problematik lässt sich daher nicht allein als übliche UV-Nahtduplikation abtun. Es wurde nichts verschweißt, gelöscht oder in den Master zurückgeschrieben. Kleine Komponenten enthalten unter anderem lose Vertices; die Zahlen bedeuten nicht zusätzliche anatomische Gliedmaßen.

Sichtprüfung: vollständige Figur, T-/Referenzpose, zwei Arme und Beine; vorhandene große barfüßige Füße. Deutlich näher an der bestehenden Spieleroptik als die prozeduralen NPC-Vorgänger, jedoch erkennbar jugendliches Gesicht und technische Oberflächenfehler. Keine Produktionsfreigabe.

## Eignung für erwachsene Hobbits und Größenvarianten

**Bereits passend:** kompakte Gesamtsilhouette, relativ großer Kopf, kurze Beinwirkung und große breite barfüßige Füße. **Noch nicht passend:** das Gesicht wirkt jung; die NPC-Standardhöhe ist noch nicht umgesetzt; Haare/Kleidung sind weder austauschbar noch als vollständig saubere Einzelteile vorhanden.

Im ungespeicherten Prüfprozess sind gemeinsame uniforme Rig-/Mesh-Skalierungen auf **1,20 / 1,32 / 1,45 m** möglich. Resthöhe und Bodenniveau bleiben innerhalb numerischer Toleranz korrekt. Der 1,32-m-Faktor wäre **1,32 / 1,40 = 0,942857**. Diese Varianten sind nur geprüft, nicht als neue Modelle gespeichert. Keine neue Capsule und keine Gameplay-Änderung.

Uniforme Größenvarianten können die Hierarchie beibehalten. Bei kürzeren Beinen, breiteren Schultern oder geänderter Kopfform müssen Restpose, Gewichte und Clips gemeinsam beurteilt werden; direkte Wiederverwendung ist dann nicht automatisch korrekt. Angewandte Bone-Skalierung kann Retargeting oder angepasste Fußbahnen erfordern.

Die bestehenden Walk-/Run-Clips sind auf 210/315 cm/s bei 1,40 m ausgelegt. Bei uniform 1,32 m sind die Schritte bei gleicher Rate 5,7 % kürzer. Für unveränderte 210 cm/s wäre rechnerisch etwa **1,0606-fache Walk-Rate** nötig; NPC-Geschwindigkeiten sollten später separat festgelegt und visuell abgestimmt werden. Keine entsprechende Runtime-Änderung in diesem Auftrag.

## Empfohlene nächste Modellierungsschritte – noch nicht durchgeführt

1. Nach Sichtfreigabe die unabhängige NPC-Kopie auf 1,32 m abstimmen; zunächst uniformen Größenvergleich, anschließend bewusste Erwachsenen-Proportionen.
2. Das vorhandene Mesh als Form-/Texturreferenz erhalten. Sauberen vollständigen Körper mit überprüfbaren Schulter-, Ellenbogen-, Hüft-, Knie- und Knöchelschleifen herstellen; dabei unbekannte Körperflächen unter Kleidung prüfen und erforderlichenfalls ergänzen. Automatisches Trennen liefert nicht zwangsläufig einen vollständigen nackten Basiskörper.
3. Haare, Hemd, Weste, Hose, Gürtel und optionalen Umhang/Tasche gezielt als getrennte Module aufbauen, UVs und Texturen übertragen. Nicht nur anhand topologischer Komponenten automatisch aufteilen.
4. Gemeinsame Hobbit-Bone-Namen/-Hierarchie definieren, bestehende Clips weiterverwenden und benötigte Erweiterungen für Gesten/Zehen/Gesicht bewusst planen. Keine unnötige Rig-Neuerfindung.
5. Bereinigte Meshes auf diese Hierarchie gewichten; Schulter-/Ellbogen-/Hüft-/Kniebeugung und Fußkontakte über alle Größen-/Körpervarianten prüfen. Run bleibt optional für gewöhnliche NPCs.
6. Erst danach optimierte Runtime-/LOD-Varianten und modulare Unreal-Darstellung prüfen. Keine derzeitige NPC-Crowd-Performancebehauptung.

## Echte Blender-Vorschauen

Cycles CPU, 32 Samples, vier Threads, neutrales eigenes Studio, 1200². **Blender-Renderings, keine Unreal-Screenshots.** Die schräge 2,5D-Nahansicht ist absichtlich groß zur Formbeurteilung; sie verändert weder die Projektkamera noch imitiert sie deren 2850-cm-Bildausschnitt.

- [Vorne](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_01_Front.png)
- [Hinten](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_02_Back.png)
- [Seite −X](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_03_Left.png)
- [Seite +X](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_04_Right.png)
- [Dreiviertel](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_05_ThreeQuarter.png)
- [Schräge 2,5D-Nahansicht](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_06_Camera25D.png)
- [Idle-Pose](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_Pose_Idle.png)
- [Walk-Pose links](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_Pose_Walk_Left.png)
- [Walk-Pose rechts](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_Pose_Walk_Right.png)
- [Run-Pose](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Previews/Hobbit_MeshyBase_V1_Pose_Run.png)

## Erhaltung, Dateien und Stopp

Alle **1.632 vor Arbeitsbeginn erfassten Dateien** bleiben bytegleich erhalten, einschließlich Hobbit V1–V4, Spielerquellen, bestehenden Unreal-Assets und offenen Sprint-/C++-Arbeiten. [Erhaltungsprüfung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/Preservation.json).

Neue Dateien ausschließlich unter HobbitBase: Master/Blender-Backup in `Source/`, eigene drei Texturen in `Textures/MeshyBaseV1/`, Werkzeuge in `Tools/MeshyBaseV1/` und Bericht/Prüfdaten/zehn Renderings in `Review/MeshyBaseV1/`. [Vollständige neue Dateiliste](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/NewFiles.json). Kein Unreal-Import, keine Karten-/Gameplay-/Spieleränderung, kein Build nötig. Keine Unreal-Automationstests ausgeführt; Blender-Kopier-, Reopen-, Textur-, Rig-/Clip- und Variantenprüfungen wurden durchgeführt.

`git diff --check` ohne Ausgabe; neue Markdown-Datei zusätzlich auf nachgestellte Leerzeichen geprüft. [Finaler Git-Status](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/GitStatus_Final.txt). Kein Commit, kein Push, nichts gestaged.

Stopp nach unabhängiger Kopie, Eignungsprüfung und Vorschauen. Weitere Umgestaltung erst nach Harrys ausdrücklicher Freigabe.
