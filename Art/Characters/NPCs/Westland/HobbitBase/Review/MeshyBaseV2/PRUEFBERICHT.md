# Hobbit NPC MeshyBase V2 – Fehleranalyse und gezielte Bereinigung

14.10.2026 · Ausgangs-HEAD `3c6dc47` · Blender 5.2.2 LTS.

## Ergebnis

[Hobbit_NPC_MeshyBase_V2_Cleanup.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_MeshyBase_V2_Cleanup.blend) wurde aus der unabhängigen [MeshyBase V1](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_MeshyBase_V1.blend) erstellt, gespeichert und in separaten Blender-Prozessen erneut geöffnet.

**Sichere technische Teilbereinigung erreicht, sichtbare Risse weiterhin offen.** Die Erscheinung und die vorhandenen Animationen bleiben erhalten. Unbenutzte Geometrie und gewichtskompatible, exakt deckungsgleiche Vertices wurden bereinigt. Es wurden keine sichtbaren Dreiecksflächen neu erzeugt oder gelöscht. Keine vollständige Reparatur der stark fragmentierten Oberfläche und keine automatische Master-NPC-Freigabe.

Das Erfolgskriterium ist bezüglich weniger Daten-/Topologiefehler und unveränderter Darstellung/Animation nachgewiesen. Eine sichtbar rissärmere Oberfläche ist **noch nicht erreicht**; dies wird nicht als vollständig erledigt ausgegeben.

## Schutz und tatsächliche Ausgangslage

AGENTS.md, relevante Projekt-/Stilunterlagen, aktueller MeshyBase-V1-Bericht sowie vorhandene Meshy-Rig-/Animationswerkzeuge wurden gelesen. Der Arbeitsbaum enthält weiterhin offene Player-/Sprint-Arbeiten. Kein Reset, Restore, Clean, Commit oder Push.

Die SHA256-Erhaltungsprüfung umfasst **1.672 vor Beginn vorhandene Dateien**: keine verändert und keine fehlend. Originalspieler, Hobbit V1–V4, MeshyBase V1, bestehende Animationen, Unreal-Assets und Maps bleiben bytegleich erhalten. Neue Dateien ausschließlich unter HobbitBase. [Erhaltungsprüfung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Preservation.json).

## Fehlerursachen: Geometrie gegen Material

Echte Blender-Vergleiche wurden mit Originalmaterial, neutralem Clay ohne Texturen/Normalmap und Wireframe durchgeführt. Die gleichen schwarzen Öffnungen und gestuften Flächen bleiben in Clay/Wireframe erkennbar. **Die auffälligen Risse sind überwiegend tatsächliche Spalten, zerlegte Oberflächen und überlagerte Dreiecke, keine bloßen schwarzen Albedo-Striche.** Stoff-/Haartexturen und Normalmap beeinflussen den Detailkontrast zusätzlich.

Nachgewiesen:

- Ein Modell-Mesh, aber V1 besitzt 3.470 topologische Komponenten mit Flächen; 3.949 Komponenten insgesamt einschließlich nicht rendernder Draht-/Punktgeometrie. Es handelt sich nicht um 3.949 zusätzliche anatomische Teile.
- 45.476 offene Kanten und 2.158 Kanten ohne Flächen. Keine Kanten mit mehr als zwei angrenzenden Flächen.
- Viele nicht benachbarte Dreieckkreuzungen, kantige Inselränder und echte Öffnungen, insbesondere am Umhang, an Stofffalten und Haut-/Kleidungsübergängen.
- 3.612 Ecknormalen zeigen entgegen der jeweiligen geometrischen Flächennormale; 5.956 besitzen ein Skalarprodukt unter 0,2. Normale sind endlich. Wegen dünner Schichten, Faltungen und importierter Custom-Normalen ist dies kein Anlass, alle Flächen pauschal umzudrehen. Keine inkonsistent gewundenen gemeinsamen manifold Kanten erkannt.
- Alle UV-Koordinaten endlich und im 0–1-Bereich; keine degenerierten UV-Dreiecke. Ein UV-Layer und ein Materialslot.
- Drei korrekt gepackte 2048²-Texturen. BaseColor sRGB, ORM/Normal Non-Color. ORM-Green steuert Roughness, Blue Metallic; Normalmap bleibt unverändert.
- Alpha **1,0**, kein Alpha-Link, Transmission **0**, Backface-Culling **aus** und keine angeschlossene Displacement-Ausgabe. Die vorhandene Dithered-Oberflächeneinstellung verursacht bei dieser vollständig opaken Anbindung kein Alpha-Clipping. Sie wurde nicht pauschal ersetzt.

Die ursprünglich gespeicherte Meshy-Datei `Player_Meshy_V1.blend` besitzt **1.466.192 Vertices / 2.652.461 Flächen**, die reduzierte Basis 52.699 Vertices / 47.744 Dreiecke. Die extreme Reduktion ist ein plausibler Zusammenhang mit den zerlegten, kantigen Oberflächen; **der genaue historische Entstehungsschritt jedes Risses wurde nicht reproduziert**, weshalb keine umfassende kausale Behauptung darüber erfolgt. Die große Originalquelle wurde nur lesend untersucht; eine eigene unverbundene Diagnosekopie anschließend aus RAM entfernt, keine Quelldatei gelöscht.

[Rohdiagnose V1](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Diagnosis_V1.json), [Rohdiagnose V2](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Diagnosis_V2.json).

### Warum kein pauschales Vernähen oder Remesh?

Eine rein diagnostische Schweißtoleranz-Reihe von 1 µm bis 1 mm wurde in wegwerfbaren BMeshes geprüft, nicht gespeichert. Selbst bei 1 mm bleiben sehr viele offene Kanten. Größere Toleranzen würden Haar-/Stoffschichten, Finger und Falten unkontrolliert verbinden.

Ein gezielter Test an 3.843 Unterarm-/Umhang-Randkanten suchte Gegenstücke mit maximal 0,5 mm Spalt, entgegengesetzter Kantenrichtung, passenden Flächennormalen, UV-Kontinuität und ähnlichen Gewichten. **Kein sicherer Kandidat** erfüllt sämtliche Kriterien. Daher keine automatische Brücke angenommen und keine willkürlichen Löcher geschlossen. [Kandidatenprüfung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/SeamCandidates.json).

## Tatsächlich übernommene Reparaturen

1. **2.625 Vertices ohne irgendeine angrenzende Fläche entfernt**, einschließlich nicht rendernder Drahtreste. Keine kleine Haar-/Kleidungsinsel mit Flächen entfernt.
2. **198 Vertices zusammengeführt**, ausschließlich bei exakt gleichen Koordinaten und exakt gleichen Bone-Gewichten. Keine räumliche Näherung, keine Verschiebung oder Glättung. Unterschiedliche Gewichte werden nicht vereinigt.
3. Alle 47.744 ursprünglichen Flächen, ihre räumlichen Eckpunkte, Materialzuordnung und UV-Corners erhalten. Gewichte für erhaltene Vertices exakt wiederhergestellt.
4. Bestehende Custom-Normal-Vektoren als Eingabe wieder eingesetzt, keine globale Neuberechnung/Glättung. Blenders erneute interne Normalencodierung erzeugt eine maximale Vektordifferenz von **0,007236**, ungefähr 0,42°. Negative-Normal-Zähler bleiben unverändert. Daher keine Behauptung bitgleicher Normalen oder umfassend reparierter Normalen.
5. Unabhängige V2-Datenblöcke, unveränderte 25-Bone-Hierarchie, eigene kopierte Idle-/Walk-/Run-Actions und eigene gepackte Texturbilder. Die drei PNG-Kopien unter `Textures/MeshyBaseV2/` sind bytegleich zu ihren V1-Texturen, besitzen aber eigene Pfade.

[Reparaturlog mit entfernten Original-IDs und Merge-Paaren](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Repairs.json). Das Attribut `V1_OriginalVertexID` ermöglicht den Rückvergleich. Eigene Vorher-Sicherung: `Source/StagesMeshyBaseV2/Hobbit_MeshyBase_V2_00_BeforeCleanup.blend`; V1 bleibt zusätzlich unverändert. Keine Voxel-Operation, keine breite Retopologie, keine neuen Körper-Primitive und kein Materialtrick zur Kaschierung.

Zusätzlich wurden drei **leere interne Dateinamen in den Packed-Image-Datensätzen** diagnostiziert und ausschließlich in V2 und der eigenen Vorher-Sicherung korrigiert. Die sichtbaren Image-Dateipfade waren bereits korrekt; die eingebetteten Dateinamensfelder waren leer und verursachten eine Blender-Meldung beim Öffnen der Sicherung. Texturbytes vor/nach der Metadatenkorrektur per SHA256 identisch. [Metadaten-Reparaturlog](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/PackedPathRepair_Master.json). Keine Änderung von Bildinhalten oder Materialwirkung.

## Polygonzahlen und verbleibende Defekte

| Merkmal | V1 | V2 |
| --- | ---: | ---: |
| Modell-Meshes | 1 | 1 |
| Vertices | 52.699 | 49.876 |
| Dreiecke / Flächen | 47.744 | 47.744 |
| Komponenten mit Flächen | 3.470 | 3.324 |
| Komponenten einschließlich Draht-/Punktresten | 3.949 | 3.324 |
| Offene Kanten | 45.476 | 45.416 |
| Non-Manifold-Kanten einschließlich Drahtresten | 47.634 | 45.416 |
| Nicht rendernde Vertices | 2.625 | 0 |
| Degenerierte Flächen | 0 | 0 |
| Materialslots / UV-Layer | 1 / 1 | 1 / 1 |
| Exakt deckungsgleiche, gewichtskompatible Vertices zusammengeführt | — | 198 |

V1: 7.756, V2: 7.749 erfasste eigentliche nicht benachbarte Dreieckkreuzungspaare. **Die sieben weniger sind keine nachgewiesene physische Reparatur dieser Kreuzungen**: Verschweißte Vertices ändern, welche Paare als benachbart ausgeschlossen werden. Alle sichtbaren Dreiecksflächen bleiben gleich. Der Test schließt gemeinsame Vertexpaare, koplanare Überlappungen und tangentiale Kontakte aus; Haar-/Kleidungsschichten können auch beabsichtigt überlagert sein. Keine formale Kollisionsfreiheit.

Weiterhin offene Problemstellen:

- Arme/Hände: Risse an Haut-/Ärmelübergängen und kantige Handflächen/Fingerbereiche.
- Füße: fragmentierte Haar-/Hautoberflächen, keine artikulierten Zehen; die barfüßige Form bleibt erhalten.
- Haare: viele einzelne Oberflächenteile, unregelmäßige Kanten; keine pauschale Entfernung, da sie die Frisur bestimmen.
- Kleidung/Umhang: sichtbare Löcher, überlappende Dreiecksflächen und gestufte Falten. Keine saubere vollständige Cloth-Topologie.
- Knie/Hüfte in Walk/Run: ausgeprägte tiefe Beugehaltung sowie vorhandene Stoffquetschungen/-überschneidungen; keine Animation-Umarbeitung in diesem Bereinigungspass.

## Rig-Prüfung

Bone-Namen, Eltern, Rest-Head/-Tail, Matrix/Achsen und Deform-Flags stimmen exakt mit V1 überein. Armature- und Mesh-Transformation im Master: Identität, Scale 1, Root am Ursprung. Master in REST; für Animationsprüfung wurde POSE benutzt. Keine Skelett-Hierarchieänderung.

25 bestehende Bones: sechs Kernbones, je sieben Gliedmaßenbones und fünf Umhang-/Taschenbones. Vollständige [Bone-Hierarchie und Koordinaten](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/RIG_HIERARCHIE.md).

Keine vorhandenen Pose-Constraints, IK- oder separaten Steuerbones. Die Zweigelenk-Beinlösung wurde beim ursprünglichen Authoring in FK-Keyframes gebacken. Handgesten durch Arm/Hand/Kopf sind grundsätzlich möglich; unabhängige Finger-, Zehen-, Augen-, Lid- und Gesichtsbones fehlen. Solche Ergänzungen brauchen eine gesonderte Freigabe. Keine automatischen neuen Gesprächsgesten erzeugt.

Die vorhandene Hierarchie ist für Idle/Walk/Run wiederverwendbar. Eine spätere NPC-Unreal-Übernahme kann dieselben Bone-Namen/Restpose verwenden, braucht aber eigene geprüfte Mesh-/Importdaten; **kein Export oder Unreal-Import in diesem Auftrag**. Die Player-Skeleton-Assets bleiben unverändert. Importtransformationen wurden nicht durch einen tatsächlichen neuen Unreal-Import validiert.

## Vollständige Animations- und Größenprüfung

[AnimationAudit.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/AnimationAudit.json):

- Idle **181 Frames / 3,00 s**, Walk **34 / 0,55 s**, Run **28 / 0,45 s**, jeweils 60 fps.
- Alle Action-Curves/Keys unverändert, alle 25 Rig-Bone-Signaturen identisch.
- Alle **243 Originalframes**: maximaler V1-/V2-Abstand der erhaltenen verformten Vertices **0 m**. UV-Corners exakt gleich. Damit kein neuer Verformungsfehler an den erhaltenen Oberflächen durch diese Bereinigung festgestellt.
- Zusätzlich alle Frames bei temporären **1,20 / 1,32 / 1,45 m**, insgesamt **972 Frameprüfungen** einschließlich Mastermaß. Gemeinsame uniforme Armature-/Mesh-Skalierung; keine neue gespeicherte NPC-Variante.
- Erfasste Sohlenminima: bei 1,40 m ungefähr **0,050 cm**, bei 1,20 m **0,043 cm**, bei 1,32 m **0,047 cm**, bei 1,45 m **0,052 cm** über Z=0. Keine erkannte Bodenpenetration in diesen gespeicherten Frames.
- Root-Translation in allen Fällen **0 m**. Alle ausgewerteten Vertexkoordinaten endlich.
- Geschätzter Foot-Sliding-Drift eines festen Sohlenreferenzpunkts in der angenommenen Standphase bei konstant 210/315 cm/s: Walk etwa **0,15–0,17 cm**, Run **0,18–0,20 cm**. Das ist eine virtuelle konstante Bodengeschwindigkeit, keine tatsächliche Overworld-Messung. Bei Größenvarianten wird das zur skalierten Schrittlänge passende Tempo verwendet. Gleiche Weltgeschwindigkeit ohne Ratenanpassung würde bei kleineren Varianten stärker rutschen.

Visuell wurden je acht gerenderte Posen über den gesamten Idle-/Walk-/Run-Zyklus geprüft. Gegengleiche Beine, Fußkontakt und Kleidung sichtbar; die vorhandenen Quetschungen und Risse bleiben. Keine zusätzliche Verschlechterung festgestellt. Die Standbildsequenzen ersetzen kein Echtzeitvideo oder lückenloses visuelles Prüfen jedes Zwischenzeitpunkts.

Keine Terrain-IK, Start-/Stop-/Dreh-Blends, dynamischen Player-Zubehörfedern oder Echtzeit-Unreal-Tests durchgeführt. Zwischen gespeicherten Frames keine exhaustive Selbstüberschneidungsprüfung. Masterhöhe bleibt **1,399999976 m**, Sohlenminimum 0, Unit Scale 1,0; Größenfestlegung auf 1,32 m nicht übernommen.

## Sichtvergleich und künstlerische Qualität

Vorher/Nachher frontal und hinten verwenden identische orthografische Kamera, 1100², 24 Cycles-CPU-Samples, gleiche Studiolichter und unveränderte Texturen. Links V1, rechts V2. Zusätzliche Seiten-, Dreiviertel-, Unterarm-, Fuß- und Umhangbilder vorhanden. Clay/Wire-Materialien sind nur temporäre Diagnosen, nicht im Master ersetzt.

Die Erscheinung bleibt praktisch gleich. Mittlere absolute RGB-Pixeldifferenz auf 0–1-Skala: Front **0,00000153**, hinten **0,00000104**. Einzelpixel weichen stärker ab; Normalencodierung, Tangenten und Render-Sampling können kleine Unterschiede erzeugen. Diese Zahl ersetzt keine Sichtprüfung. Bilder und exakte Flächen-/Deformationsvergleiche bestätigen keinen erkennbaren künstlerischen Qualitätsverlust, aber auch keinen großen sichtbaren Reparaturgewinn. [Vergleichsdaten](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/VisualComparison.json).

## Vorschauen und modulare Planung

Alle echten Renderings und Bildsequenzen mit anklickbaren vollständigen Pfaden stehen in [RENDERINGS.md](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/RENDERINGS.md). Keine KI-Konzeptbilder als Blendernachweise ausgegeben.

Wichtigste Übersichten:

- [Vorne: V1 / V2](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/BeforeAfter_Front.png)
- [Hinten: V1 / V2](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/BeforeAfter_Back.png)
- [Umhang: Textur / Clay / Wire](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/Diagnosis_Cape_Textured_Clay_Wire.png)
- [Arm: Textur / Clay / Wire](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/Diagnosis_Arm_Textured_Clay_Wire.png)
- [Idle-Sequenz](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/Sequence_Idle_V2.png)
- [Walk-Sequenz](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/Sequence_Walk_V2.png)
- [Run-Sequenz](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/Sequence_Run_V1.png)
- [Temporäre Körpergrößen](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/Scale_120_132_145.png)
- [Bestehendes Rig](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/Previews/Rig_Existing25Bones.png)

Die Animationsübersichten zeigen acht Originalrenderings chronologisch, oben links nach rechts, dann unten links nach rechts, einschließlich Zyklus-Endpose. Keine Videoaufnahme erstellt. Riglinien sind nur aus den tatsächlichen Bone-Endpunkten erzeugte Review-Kurven; sie sind keine zusätzlichen Bones oder Modellteile im Master. Größeninstanzen sind nur temporär gerendert.

[Konkreter modularer Vorschlag](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/MODULARER_VORSCHLAG.md): Kopf/Haar, Körper, Hemd, Weste, Hose, Umhang, Tasche/Gürtel und Füße mit gemeinsamen Anschluss-/Rig-Regeln. Keine automatische Trennung durchgeführt. Priorität vor Modularisierung: eine kleine, klar begrenzte Unterarm- oder Umhangstelle fachlich reparieren und gegen die hochauflösende Originalform sowie alle vorhandenen Posen vergleichen.

## Abschluss und offene Arbeit

Die sicher diagnostizierten nicht rendernden Reste und exakt deckungsgleichen gewichtskompatiblen Vertices sind bereinigt. Größere Risse und überlagerte Flächen benötigen weiter gezielte lokale Modellierungsarbeit; eine automatische Komplettreparatur wäre hier nicht sicher und wurde nicht erzwungen. Keine Freigabe als fertiger Master.

`git diff --check` erfolgreich, neue Markdown-Dateien zusätzlich geprüft. [Git-Status](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/GitStatus_Final.txt), [neue Dateien](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV2/NewFiles.json).

Keine Änderungen an Unreal/Maps/Gameplay/Spieler oder Haupt-Projektdokumentation, kein Build und keine Unreal-Automationstests erforderlich oder ausgeführt. Blender-Reopen-, Geometrie-, Kopier-/Flächen-, UV-, Rig-, Clip-, Größen- und Sichtprüfungen tatsächlich durchgeführt. Stopp nach Bereinigung, Prüfbericht und Vorschauen. Kein Commit, kein Push, keine weitere Entwicklungsphase automatisch gestartet.
