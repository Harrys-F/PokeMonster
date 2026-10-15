from pathlib import Path
import json,subprocess
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');B=R/'Art/Characters/NPCs/Westland/HobbitBase';P=B/'Review/4K_Base_V1';A=json.loads((P/'TechnicalAudit.json').read_text());V=json.loads((P/'VirtualSeamAudit.json').read_text());F=json.loads((P/'FullIntersectionAudit.json').read_text());I=json.loads((P/'InputGLB.json').read_text());Z=json.loads((P/'ProtectionAfter.json').read_text())
text=f'''# Westland Hobbit NPC – neuer GLB-Import / 4K Base V1

Prüfdatum: 14.10.2026. Blender 5.2.2 LTS über vorhandenes Blender-MCP und separate Blender-Hintergrundprozesse. Ausgangs-HEAD: `{Z['git_head']}`. Der Arbeitsbaum war bereits durch Sprint-/NPC-Arbeiten verändert; alle vorhandenen Änderungen wurden erhalten.

## Ergebnis und Freigabestatus

Die ausdrücklich genannte neue iCloud-Datei wurde unverändert importiert und als eigenständige Blender-Arbeitsdatei sowie bytegleiche Importreferenz gesichert. Sie ist als detailreiche visuelle Highpoly-Quelle brauchbar. **Noch kein fertig animationsfähiger, modularer oder für Unreal optimierter Hobbit-Master.** Die Optik ist freundlich und konsistent, das Gesicht wirkt allerdings jugendlich statt eindeutig erwachsen.

**Die Datei enthält keine 4K-Texturen:** Base Color, Normal und Metallic/Roughness sind jeweils 2048 × 2048 Pixel. Der gewünschte Dateiname „4K_Base_V1“ ist die Auftragsbezeichnung, keine nachgewiesene Texturqualität. Es wurde kein Ersatzmodell verwendet und nichts hochgerechnet.

## Tatsächlich verwendete Quelle und Sicherung

- iCloud-Quelle: `{I['source']}`
- Dateigröße: {I['bytes']:,} Bytes.
- SHA-256: `{I['sha256']}`.
- Unveränderte GLB-Projektkopie: `{I['copy']}`.
- Arbeitsdatei: `{B/'Source/Hobbit_NPC_4K_Base_V1.blend'}`.
- Separate Importreferenz: `{B/'Source/Hobbit_NPC_4K_Base_V1_ImportReference.blend'}`.

Arbeitsdatei und Referenz sind bei Abschluss bytegleich, aber eigenständige Dateien. Sie enthalten keine verknüpften Bibliotheksdaten des Players oder alter Hobbits. Drei originale JPEG-Bilddaten wurden zusätzlich unverändert extrahiert und in der Blender-Datei gepackt. V1–V4 und MeshyBase V1/V2 wurden nicht als Geometriequelle verwendet.

## Import, Maße und Struktur

| Merkmal | Tatsächliches Ergebnis |
| --- | --- |
| Charakter-Mesh-Objekte | 1 (`Mesh_0.001`) |
| Vertices | 1.466.192 |
| Kanten | 4.114.722 |
| Polygone / Dreiecke | 2.652.461 / 2.652.461 |
| Quads / Ngons | 0 / 0 |
| Geometrieinseln im importierten Vertexgraph | 3.949 |
| Materialslots | 1 |
| UV-Layer | 1 (`UVMap`) |
| Armatures / Skin / Vertex Groups / Animationen | 0 / 0 / 0 / 0 |
| Objekt-Scale | 1 / 1 / 1; Weltmatrix Identität |
| Blender-Einheiten | Meter, Unit Scale 1 |
| Gesamthöhe einschließlich Haaren | 1,399999857 m ≈ 140 cm |
| Minimum Z | 0 m |
| Ausdehnung in T-Pose | 1,427609 × 0,418060 × 1,400000 m |

Es wurde nicht auf 1,32 m skaliert. Der glTF-Y-up→Blender-Z-up-Achsenwechsel ist die notwendige Importkonvention, keine Proportionsänderung. Alle Vertexpositionen, Dreiecksindizes und UV-Koordinaten wurden mit dem GLB verglichen: **maximaler Positions-/UV-Fehler 0; Indizes identisch.** Keine Subdivision, Retopologie, Reduktion, globale Reparatur oder Materialverbesserung.

## Geometrieprüfung und richtige Interpretation der Inseln

Im unveränderten Blender-Vertexgraph:

- 272.061 Boundary-Kanten; keine Kante mit mehr als zwei anliegenden Flächen.
- 142.156 redundante Vertices an exakt gleichen Positionen, in 129.905 Positionsgruppen.
- Keine isolierten Vertices, losen Kanten oder Nullflächen.
- Keine Flächen unter 1e−12 m²; kleinste Fläche etwa 3,77e−9 m².
- Keine nicht endlichen Positions-, UV- oder Normalenwerte.
- Keine widersprüchliche Kantenorientierung zwischen direkt verbundenen Dreiecken.

Die vielen Inseln und Positionsduplikate sind überwiegend getrennte UV-/Normalennähte. Ihre Zahl beweist weder 3.949 unabhängige Kleidungsstücke noch 272.061 sichtbare Löcher. Eine **rein rechnerische, exakte Positionsgleichsetzung**, ohne Änderungen am Blender-Mesh, ergibt:

- 1 zusammenhängende geometrische Komponente.
- 28 verbleibende offene Kanten, Länge etwa 0,078–1,623 mm.
- 60 Kanten mit mehr als zwei Flächen, Länge etwa 0,103–1,159 mm.
- Keine doppelten Dreiecke nach exakter Positionsgleichsetzung.

Diese kleinen Reststellen liegen ungefähr zwischen Z 0,615 und 1,364 m, insbesondere an Haar-/Übergangsflächen; alle Koordinaten stehen in `ResidualEdges.json`. Das Modell ist **nicht vollständig manifold**. Es wurde nichts automatisch verschweißt. Spätere Bereinigung muss UVs und Custom Normals an Nähten erhalten.

### Selbstüberschneidungen und Normalen

Ganzes Mesh: BVH-Prüfung aller 2.652.461 Dreiecke mit zusätzlichem Segment-Dreieck-Test, Ausschluss gemeinsam genutzter/exakt deckungsgleicher Vertexkontakte. Ergebnis: **126 bestätigte nicht koplanare Dreieckspaar-Kreuzungen**, davon 124 mit Schwerpunkt oberhalb Z 1,10 m (Kopf/Haare), zwei am hinteren Kragen-/Halsbereich um Z 1,072 m. Es handelt sich um Dreieckspaare, nicht 126 getrennte sichtbare Risse.

Sechs zusätzliche regionale Prüfungen von Nase/Mund, beiden Händen, beiden Füßen und Umhangsaum fanden keine bestätigten nicht koplanaren Kreuzungen in ihren jeweiligen Ausschnitten. Die Ganzmesh-Prüfung hat keine ungelösten koplanaren Kandidaten geliefert. Grenzen: Nulltoleranz-BVH, Gleitkommaungenauigkeit, Beinahekontakte sowie Berührungen an geteilten Vertices sind keine mathematisch lückenlose Fehlerfreiheit. Ausschließlich ungeriggte Ausgangspose geprüft.

Custom Normals vorhanden, endlich und näherungsweise Einheitslänge. **9.443 Corner-Normalen auf 7.631 Dreiecken** zeigen entgegen der geometrischen Flächennormalen (negatives Skalarprodukt). Das ist eine lokale Auffälligkeit des gelieferten Imports, kein Nachweis, dass sämtliche Flächennormalen verkehrt sind. Flächenwindung, geglättete importierte Normalen und Haarübergänge müssen vor späteren Reparaturen lokal verglichen werden. Keine Normalen global neu berechnet.

### Sichtprüfung

Front, Rücken, beide Seiten, Dreiviertel, 2,5D, Kopf, beide Hände, Füße, Kleidung sowie Clay-/Wireframe-Aufnahmen tatsächlich gerendert und betrachtet. Keine großflächigen schwarzen Risse oder fehlenden Gliedmaßen in diesen Ansichten. Haarzwischenräume sind überwiegend modellierte Zwischenräume und Schatten; kleine Überschneidungen bleiben technisch vorhanden. Hände besitzen je fünf erkennbare Finger einschließlich Daumen, Füße je fünf Zehen. Hände wirken in Nahansicht weich und teilweise durch Textur-/Normalmap-Flecken unruhig; Fingeransätze benötigen einen späteren Deformationstest. Fußbehaarung ist als kräftige Relief-/Strähnenform modelliert. Im Nahbild grob, in der erhöhten Ansicht lesbar.

## UVs, Materialien und Texturen

Ein gemeinsamer Atlas für Haut, Haare und Kleidung. UV-Werte liegen innerhalb 0–1 und sind endlich. Keine unabhängigen Body-/Hair-/Cloth-Materialslots. Kein vollständiger Texel-Dichte-/UV-Überlappungstest durchgeführt; Wiederverwendung/Symmetrie kann im Atlas beabsichtigt sein.

| GLB-Bild | Funktion | Größe | Farbraum | Unveränderte Projektkopie |
| --- | --- | --- | --- | --- |
| Image_0 | Base Color | 2048 × 2048 | sRGB | `{B/'Textures/4K_Base_V1/GLB_Image_1.jpg'}` |
| Image_1 | Metallic/Roughness | 2048 × 2048 | Non-Color | `{B/'Textures/4K_Base_V1/GLB_Image_2.jpg'}` |
| Image_2 | Normal | 2048 × 2048 | Non-Color | `{B/'Textures/4K_Base_V1/GLB_Image_0.jpg'}` |

Alle drei gepackten JPEG-Daten haben denselben SHA-256 wie die aus dem GLB extrahierten Originaldaten. Texture-Nodes und glTF-PBR-Verbindungen wurden erhalten. glTF-AlphaMode ist mangels Angabe OPAQUE; Double Sided ist aktiv. Blender-Backface-Culling deaktiviert, Alpha 1 ohne Verbindung. `DITHERED` ist die Blender-Surface-Einstellung, **keine tatsächlich aktive Transparenz/Alpha-Clipping-Maske**. Keine transparente Haarkarte eingerichtet.

Die ersten Packpfade trugen Blender-Suffixnamen ohne externe Dateien; beim ersten Normalisieren wurden entsprechende Pfadwarnungen protokolliert. Die Metadaten wurden auf die tatsächlich extrahierten JPEGs korrigiert, ohne Pixeländerung. Wiederöffnungsprüfung und alle nachfolgenden Renderprozesse finden die Texturen, ohne diese Warnungen. Das ursprüngliche Log bleibt als Nachweis erhalten. Der automatisch erzeugte `.blend1` ist nur der erste Zwischenstand und nicht die empfohlene Arbeitsdatei.

## Technische Rig-Referenz – noch keine Übertragung

Lesend geprüft: `{B/'Source/Hobbit_NPC_MeshyBase_V2_Cleanup.blend'}`. Nur Armature-Daten und Actions in einen separaten Prüfprozess geladen; keine alte Körpergeometrie übernommen, keine alten Dateien gespeichert.

25 Deform-Bones: root → pelvis → spine → chest → neck → head; je clavicle/upperarm/lowerarm/hand und thigh/shin/foot links/rechts; cape_upper/cape_lower/cape_left/cape_right und bag. Keine unabhängigen Finger-, Zehen-, Gesichts- oder Augenbones. Vorhandene Clips:

| Action | Framebereich |
| --- | --- |
| HNM2_Idle_V2 | 1–181 |
| HNM2_Walk_V2 | 1–34 |
| HNM2_Run_V1 | 1–28 |

Die T-Pose, Größenordnung und Körpergliederung machen die Struktur als Ausgangspunkt für einfache NPC-Idle-/Lauf-/Drehbewegungen plausibel. Das ist **keine geprüfte Bindung**. Erforderlich in einer freizugebenden nächsten Version:

1. Kopf/Hals, Schulteransätze/Clavicles, Ellbogen, Handgelenke und Hüft-/Knie-/Knöchelpunkte am neuen Mesh kontrollieren und gegebenenfalls Bonepositionen/Bone-Roll im neuen Rig passend setzen. Verdeckte Gelenke unter Kleidung sind mit dieser Oberflächenprüfung nicht exakt bestimmt.
2. Neue Skin Weights. Die Vertex-IDs des alten Cleanup-Meshes sind nicht auf den neuen Highpoly-Import übertragbar. Nähe-/Oberflächentransfer wäre nur ein Start, danach Schulter-/Knie-/Finger-/Kleidungsprüfung nötig.
3. Haare im ersten Pass dem Kopf zuordnen; Kragen am Oberkörper, Umhang mit kontrollierter Verteilung auf die vier vorhandenen Umhangbones, Tasche auf bag, Riemen körpernah. Umhang/Beine können nach dem Binden kollidieren; die Ausgangspose beweist keine Bewegungsfreiheit.
4. Bestehende Clips auf einer eigenen Rig-Kopie wiederverwenden/retargeten und erneut testen. Anpassungen an Rest Pose oder Bonepositionen können Fußkontakt/Schrittlänge verändern. Keine Animation wurde auf dem neuen Modell abgespielt, weil noch keine Bindung besteht.
5. Allgemeine Arm-/Handgesprächsgesten sind mit dem Layout plausibel. Greifen mit einzelnen Fingern, Zehenrollen, Blinzeln und Mimik benötigen zusätzliche Bones beziehungsweise Shapes und lokale Deformationstopologie. Keine Skeleton-Erweiterung vorgenommen.

Keine IK-Steuerung aus der alten Referenz als neues System übernommen. Die neue Masterdatei enthält bewusst weder Rig noch Animationsdaten.

## Größenvarianten

Nur rechnerisch geprüft, keine Originalskalierung vorgenommen:

| Zielhöhe | Uniformer Faktor gegenüber geliefertem Import |
| --- | --- |
| 1,20 m | 0,857143 |
| 1,32 m | 0,942857 |
| 1,45 m | 1,035714 |

Eine einheitliche Skalierung von Mesh, Rig und Zubehör um den Boden-Root kann diese Höhen ohne Proportionsänderung erreichen. Alle Varianten könnten dasselbe logische Skelettlayout und dieselben Grundclips verwenden. Bei gleicher Weltgeschwindigkeit muss die Cliprate zur skalierten Schrittlänge passen; Deformation und Foot Sliding sind noch offen. Bei individuellen Körperformen reicht ein globaler Faktor nicht: Bone-Restpositionen und Gewichte müssen kontrolliert angepasst werden. Keine Größenvariante ist in Unreal oder animiert getestet.

## Modulares NPC-System: Ist-Zustand und Vorschlag

Körper, Kopf, Haare, Hemd, Weste, Hose, Umhang, Gürtel und Taschen sind **keine austauschbaren separaten Mesh-Objekte**. Die 3.949 Importinseln dürfen nicht als Module behandelt werden; nach virtueller Nahtgleichsetzung ist es eine zusammenhängende Gesamtoberfläche. Optisch unterschiedliche Bereiche teilen denselben Atlas und sind stellenweise aneinander modelliert. Ein vollständig ausgearbeiteter unsichtbarer Körper unter Kleidung ist nicht nachgewiesen. Augen sind keine separat riggbaren Augäpfel.

Empfohlener späterer Aufbau: gemeinsamer Deformationskörper mit definierten Schnitt-/Anschlussstellen an Hals, Handgelenken und Knöcheln; separate Hair-, Shirt-, Vest-, Trousers-, Cape- und Accessories-Meshes mit identischem Bind-Rig. Die sichtbare Highpoly-Quelle bleibt unangetastet als Bake-/Silhouettenreferenz. Kontrollierte Retopologie/Trennung an Kleidungsgrenzen und gezielte Ergänzung bisher verdeckter Hautflächen auf neuer Arbeitskopie, kein automatisches Löschen vermeintlich kleiner Inseln. Gesichtsalter und Kopfvarianten separat künstlerisch prüfen.

| Geplante Variante | Vorbereitbarer Unterschied | Voraussetzungen |
| --- | --- | --- |
| Dorfbewohner | ruhige Hemd-/Weste-/Hosenfarben, später schlichtes Haar; Umhang optional | Alterswirkung klären; Module und verdeckte Hautflächen erst erstellen |
| Bauer | gröbere Arbeitskleidung, gedeckte Farbtöne, später Schürze/kleine Werkzeugtasche | Zubehör als neues skinnbares/gesockeltes Modul, keine neue Rig-Hierarchie zwingend |
| Händler | gepflegte Weste, andere Stofffarben, zusätzliche Tasche oder Gürtelzubehör | Atlas-/Materialvarianten sauber planen, Riemen am Körper halten |

Vorerst könnten nur Texturfarbvarianten ohne Formwechsel vorbereitet werden. Drei ausgearbeitete Varianten wurden nicht erstellt. Haar-/Kleidungswechsel und erwachsene Gesichtsvarianten sind noch Arbeit, kein vorhandenes Feature.

## Prüfung, Grenzen und nächste Schritte

- Masterdatei tatsächlich mit einem neuen Blender-Prozess erneut geöffnet; korrekte aktive Szene und ein Charaktermesh.
- Unveränderte Geometrie-, UV- und Normalenhashes bestätigt. Gepackte Texturen bytegleich, externe Pfade vorhanden. Importreferenz bytegleich zur Masterdatei.
- Keine neuen Deformations-, Lauf-, Unreal- oder Gameplaytests behauptet. Kein Unreal-Import, keine Maps und keine C++-/Animdateien bearbeitet; deshalb kein Unreal-Build ausgeführt.
- **{Z['protected_files_checked']} bereits vorhandene Projekt-/NPC-Dateien SHA-geprüft: keine verändert, keine fehlt.** Vorhandene offene Sprint-/Player-Änderungen bleiben bestehen.
- Die Highpoly-Datei ist mit 2,65 Millionen Dreiecken als normaler NPC für viele Instanzen nicht geeignet. Keine Runtime-Reduktion, LOD-Erstellung oder Performance-Messung vorgenommen. Eine separate kontrolliert optimierte Runtime-Variante ist später erforderlich.
- Kopf/Haar und Kleidung wirken in Front/Profil/Dreiviertel konsistent, aber Gesicht eindeutig eher jung. Keine automatische Freigabe als neutraler erwachsener Westland-Master.

**Empfehlung:** die erhaltene Datei als hochwertige visuelle Ausgangsquelle behalten. Nach Harrys visueller Prüfung zunächst klären, ob die jugendliche Alterswirkung gewünscht ist oder erwachsene Varianten nötig sind. Danach auf neuer Kopie lokale Problemstellen/Deformationstopologie und kontrollierte Rig-Anpassung mit neuen Gewichten durchführen. Erst nach echten Idle-/Walk-/Run-Deformationstests als Animationsmaster beurteilen. Noch keine Freigabe und keine Fortsetzung über diesen Stopp-Punkt hinaus.

## Rendernachweise und Pfade

22 einzelne echte Cycles-Renderings: 1100 × 1100 Pixel, 24 Samples mit Denoising. Zusätzlich vier Blender-Pixeltafeln aus diesen Originalrenderings. Keine generierten Konzeptbilder. `06_2_5D_Close` ist eine erhöhte Nahansicht bei ungefähr 50° für Formkontrolle. `18_2_5D_GameScale` ist ein **Blender-Maßstabsvergleich**, perspektivisch mit 28,5 m Abstand und 35° horizontalem FOV bei 1100 × 619; kein Unreal-Screenshot. Die reale Gameplaykamera und Welt wurden nicht geändert.

Alle Bildpfade:

'''
for p in sorted((P/'Previews').glob('*.png')):text+=f'- [{p.name}]({p})\n'
text+='\n## Git-Abschluss\n\n`git diff --check`: Exit 0, keine Ausgabe. Nichts gestaged, kein Commit, kein Push. Neue Dateien ausschließlich im HobbitBase-Arbeitsbereich. Die folgende Statusausgabe umfasst auch die bereits vor diesem Auftrag bestehenden Änderungen:\n\n```text\n'+Z['git_status']+'```\n\n## Vollständige neue Dateiliste dieses Auftrags\n\n'
report=P/'PRUEFBERICHT.md';text+=f'- `{report}`\n'
roots=[B/'Review/4K_Base_V1',B/'Tools/4K_Base_V1',B/'Incoming/4K_Base_V1',B/'Textures/4K_Base_V1']
for p in sorted([p for root in roots for p in root.rglob('*') if p.is_file()]+list((B/'Source').glob('Hobbit_NPC_4K*'))):
 if p!=report:text+=f'- `{p}`\n'
report.write_text(text)
assert not any(line.rstrip()!=line for line in text.splitlines());print('REPORT_WRITTEN',len(text),flush=True)
