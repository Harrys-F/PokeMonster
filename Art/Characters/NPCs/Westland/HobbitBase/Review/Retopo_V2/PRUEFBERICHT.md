# PokeMonster – Hobbit NPC Kontrollierte Retopologie V2

## Ergebnis und verbindlicher Stopp

**Retopologie-Arbeitsplatz vorbereitet; kein gültiger Lowpoly-Kopfpilot erstellt.** Die vom Auftrag erlaubte manuelle Fortsetzung ist erforderlich. Es wurde keine vereinfachte Dreieckshülle und kein gescheitertes QuadriFlow-/Decimate-Mesh als neue Grundlage verwendet.

Die neue Arbeitsdatei enthält die unveränderte Highpoly-Referenz und einen ausdrücklich leeren Retopo-Zielkörper. Dessen 0 Vertices / 0 Faces sind kein Optimierungserfolg. Augen- und Mundloops, neue Kopfoberfläche, neue UVs und gebackene Zielmaterialien fehlen. **Die Voraussetzungen für spätere Animationen sind deshalb noch nicht erfüllt.** Kein Rigging, keine Haare-/Kleidungsretopologie und kein Unreal-Import.

Der Auftrag nennt: „Wenn eine saubere Ausführung ohne manuelle Modellierungsarbeit nicht zuverlässig möglich ist, bereite den Retopologie-Arbeitsplatz vollständig vor, dokumentiere die notwendigen Handgriffe und stoppe.“ Dieser Stopp-Zweig wurde genutzt. Weitere automatische Reduktion würde den bereits festgestellten Fehler wiederholen. Ein über einen generischen Kopf projiziertes Raster würde passende Augen-/Mundloops, Nasenflügel und Ohreinbettung nicht zuverlässig belegen. Der neue Arbeitsplatz ersetzt diese Modellierungsarbeit nicht.

## Ausgangslage und Schutz

- Ausgangs-HEAD: `3c6dc47 Extend player sight visibility to all test map tree families`.
- Der Arbeitsbaum war bereits durch Player/Sprint und frühere Hobbit-Arbeiten verändert; diese wurden vollständig erhalten.
- Eingelesene Geometrie: `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_4K_Base_V1.blend`.
- Neue unabhängige Arbeitsdatei: `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_Retopo_V2.blend`.
- Blender: **5.2.2 LTS**, Meter, Unit Scale 1.
- Bestehende Highpoly-Masterdatei, projektinterne Original-GLB, frühere Hobbit-Dateien/Retopologie-Tests sowie sämtliche Player-/Unreal-Dateien wurden nicht gespeichert, überschrieben oder geändert.
- Hashschutz: **1980 vorhandene Dateien, 0 geändert, 0 fehlend** (`ProtectedBefore.json`, `ProtectionAfter.json`). Das schließt auch bestehende ignorierte Dateien im HobbitBase-Bereich ein.

Die Live-Verbindung wurde über Blender-MCP verwendet. Vorhandene offene Szenen wurden nicht durch `open_mainfile` ersetzt oder gespeichert. Die neue Referenz wurde separat aus der geschützten Masterdatei angehängt. Wiederöffnen und Rendern fanden in separaten Blender-Prozessen statt. Das Addon meldet Protokoll 11 statt 13; die benötigten API-Aufrufe und Vorschau-Fallbacks funktionierten. Kein Addon-Update, Plugin oder externer Dienst wurde verwendet.

## Tatsächliche Quellenstruktur

| Eigenschaft | Gemessen |
|---|---:|
| Mesh-Objekte der Referenz | 1 |
| Vertices | 1,466,192 |
| Kanten | 4,114,722 |
| Polygone / Dreiecke | 2,652,461 / 2,652,461 |
| Materialien am Referenzmesh | 1 |
| UV-Layer | UVMap |
| Texturen | 3 × 2048 × 2048, gepackt |
| Höhe inklusive Haaren | 1.399999857 m, praktisch 1,40 m |
| Unterster Punkt | Z=0 m |
| Rig / Animationen in der neuen Datei | keine |
| Neue Zielgeometrie | 0 Vertices, 0 Faces, 0 Dreiecke |
| Neue Augen-/Mundloops | keine |

„4K“ ist der Dateiname und kein Nachweis für 4K-Texturen. Die Quelle hat drei 2K-Bilder: Base Color (sRGB), Metallic/Roughness (Non-Color) und Normal (Non-Color).

Der aktuelle Geometrie-, UV- und Custom-Normal-Hash entspricht der zuvor geprüften Quelle. Daher sind die älteren read-only Strukturdiagnosen derselben Geometrie weiterhin einschlägig: 3.949 rohe Index-Komponenten durch viele UV-/Normal-Seams; nach **nur virtueller** Gleichsetzung exakt identischer Positionen 1 physisch zusammenhängende Komponente, 28 Rest-Randkanten und 60 Kanten mit mehr als zwei angrenzenden Dreiecken. Diese Zahlen stammen aus `Review/4K_Base_V1/VirtualSeamAudit.json`, nicht aus einer heute ausgeführten Reparatur. Die dort ebenfalls dokumentierten Überschneidungen sind nicht repariert. Der Highpoly ist eine visuell brauchbare Referenz/Baking-Quelle mit bekannten Restproblemen, kein fertiges Deformationsmesh.

### Neue räumliche Diagnose – keine tatsächliche Zerlegung

Dreieckmittelpunkte wurden räumlich gefiltert. Die Kandidaten überlappen; Grenzen schneiden teilweise angrenzende Dreiecke und enthalten gemischte Inhalte. Sie wurden ausschließlich in Arrays ausgewertet, **nicht** als geschnittene Meshes erzeugt. Bounds und Referenzvertexzahlen stehen in `WorkspaceAudit.json`.

| Kandidat | Filter | Dreiecke |
|---|---|---:|
| head_hair_neck_candidate | Z ≥ 1,075 m | 1,622,058 |
| front_face_candidate | |X| < 0,115 m, Y < −0,025 m, 1,075 < Z < 1,275 m | 121,791 |
| upper_hair_candidate | Z ≥ 1,28 m | 547,409 |
| torso_clothing_candidate | |X| < 0,36 m, 0,62 ≤ Z < 1,075 m | 493,231 |
| back_cape_candidate | Y > 0,04 m, 0,26 < Z < 1,08 m | 354,048 |

Materialslots liefern keine Trennung zwischen Haut, Haaren, Hemd, Weste oder Umhang: ein gemeinsamer Slot/Atlas. UV-Seams dürfen nicht als zuverlässige Modulgrenzen interpretiert werden. Die sichtbaren Farbbereiche sind Hinweise für die manuelle Auswahl, keine gesicherte automatische Segmentierung. Besonders unter Haaren und Kleidung ist eine eigenständige, vollständige Schädel-/Körperoberfläche nicht nachgewiesen.

## Dokumentierte Trennungsstrategie

1. Das komplette Highpoly bleibt unter `HIGH_POLY_REFERENCE` unverändert und gegen Auswahl gesperrt.
2. Sichtbare Haut-/Haar-/Kleidungsgrenzen zuerst mit Originalmaterial, Clay und beiden Profilen kontrollieren. Auswahl nur an einer später angelegten, unabhängigen Helferkopie bestätigen. Nicht das Original schneiden.
3. Kopf und Hals bewusst an anatomisch geeigneten Anschlussringen neu aufbauen. Keine pauschale Höhenabschneidung am Kiefer. Unter Haaren verdeckte Schädelbereiche erfordern manuelle Rekonstruktion; dies ist nicht als exaktes Quelldetail auszugeben.
4. Haare später als kontrollierte Lockengruppen mit erhaltenen tragenden Außenkonturen optimieren. Kleine Inseln nicht ungeprüft löschen.
5. Kleidungsränder, Armausschnitte, Hals, Westenkanten und Umhangsäume manuell verfolgen. Gegebenenfalls neue verdeckte Körperflächen für Varianten rekonstruieren. Die Collections behaupten keine schon vorhandene Modularität.
6. Für spätere Bakes dürfen separat bestätigte Quellgruppen erstellt werden, um Treffer auf benachbarte Haare/Kragen zu vermeiden. In V2 wurde keine solche Hilfszerlegung ausgeführt.

## Gespeicherter Arbeitsplatz

Alle acht verlangten Collections sind vorhanden:

- `HIGH_POLY_REFERENCE`: ein vollständiges unverändertes Highpoly-Mesh.
- `RETOPO_HEAD`: `RTV2_Head_MANUAL_RETOPO_REQUIRED`, derzeit leer, für manuelle Neugeometrie.
- `RETOPO_BODY`, `RETOPO_HAIR`, `RETOPO_CLOTHING`, `RETOPO_ACCESSORIES`: leere organisatorische Bereiche.
- `BAKING`: leer; keine ungesicherten Zieltexturen.
- `REVIEW`: Studiolicht, Kontrollkameras, zusätzlicher Unterbereich `REVIEW_REF_IMAGES`.

**Snapping:** aktiviert, Blender-5.2-`FACE_PROJECT` (individuelle Flächenprojektion), Closest, Nicht-Edit-Ziele erlaubt, auch gegen Auswahl gesperrte Referenz. Selbst-/Edit-Snapping aus. Das frühere Python-Property `use_snap_project` existiert hier nicht; die tatsächlichen gespeicherten Einstellungen wurden nach dem Wiederöffnen geprüft.

**Zielmodifier:** Mirror X, Clipping, Merge 0,1 mm; Shrinkwrap Nearest Surface Point auf die Highpoly-Referenz, Offset 0,5 mm, Anzeige im Edit Mode. Der neue Zielkörper steht „In Front“. Mirror ist nur eine Starthilfe; die Quelle besitzt Asymmetrien. Shrinkwrap kann an Haaren/Ohren/Kragen die falsche Oberfläche treffen und ist dort kontrolliert zu deaktivieren beziehungsweise auf später geprüfte Helfer zu beschränken.

**Ansichten:** orthografische Front, linkes/rechtes Profil, Dreiviertel und schräge 2,5D-Nahansicht gespeichert. Front = −Y, Höhenachse = Z, Symmetrieachse = X. Drei gepackte Referenzbild-Empties (Front, links, rechts) mit 35 % Deckkraft und identischem orthografischen Maßstab sind korrekt an denselben Kopfmittelpunkt ausgerichtet und gesperrt. Standardmäßig verborgen, damit sie die reale Oberfläche nicht überlagern. Die Kameras/Lichter sind im Viewport verborgen, im Render aktiv.

**Prüfhilfen:** gespeicherte Clay-/Wire-Review-Materialien, Face-Orientation-Overlay über Blender, und ein read-only bmesh-Prüfskript für das kleine Zielmesh im Text Editor. `RTV2_START_HERE` und die vollständige Anleitung sind in der Datei enthalten. Die Originalmaterialzuordnung bleibt unangetastet.

Die konkrete Anleitung für Augenringe, Mundringe, Nasenstreifen, Wangenverbindungen, Kiefer, Ohren und Halsanschluss steht in `MANUELLE_RETOPO_ANLEITUNG.md`. Ohne sie umzusetzen und visuell zu prüfen gibt es keinen Kopf-Piloten.

## Haare und Kleidung: technischer Plan, keine Umsetzung

| Bereich | Geometrisch erhalten | Für Normal-/Roughness-Bake geeignet |
|---|---|---|
| Haare | Außenkontur, markante Stirnfransen, große Lockengruppen, Übergänge an Ohr/Nacken | kleine Innenrillen, feine Oberflächenstruktur außerhalb der Silhouette |
| Hemd/Weste | Ausschnitte, Säume, offene Westenkanten, tiefe konturprägende Falten | Stoffkorn, flaches Nahtrelief, kleine Falten |
| Umhang | Außenkante, erkennbare Dicke, große Falten, Schulterkontakt | flache Falten und Oberflächendetails |
| Haut/Kopf | Nase, Lippen, Lider, Ohren, Kieferkontur | feines Oberflächenrelief; keine Kompensation falscher Silhouette |

Normals können den Außenumriss oder fehlende Mund-/Lid-Geometrie nicht ersetzen. Eine modulare Kleidung erfordert außerdem definierte Körperanschlüsse und verdeckte Abdeckung; diese existieren nicht nachweislich als separate Quelle.

## Echte Renderings und offene Vergleiche

Neun neue echte Blender-Cycles-Renderings, 1000 × 1000, 12 Samples mit Denoising, identisches übernommenes Studiolicht und Originalmaßstab. Zwei zusätzliche Kontaktbögen ordnen diese Renderings an. Alle zeigen **ausschließlich die unveränderte Highpoly-Referenz**. Keine synthetischen Konzeptbilder, keine Zielmaterialbakes, keine „Nachher“-Geometrie.

Die 2,5D-Ansicht ist eine orthografische Blender-Nahansicht zur Formprüfung, ungefähr 50° erhöht, nicht ein Screenshot aus Unreal oder ein Test der tatsächlichen 2850-cm-Perspektivkamera.

- Kopf vorne, Originalmaterial: [01_Reference_Front.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/01_Reference_Front.png)
- Kopf rechtes Profil, Originalmaterial: [02_Reference_Right.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/02_Reference_Right.png)
- Kopf linkes Profil, Originalmaterial: [03_Reference_Left.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/03_Reference_Left.png)
- Kopf Dreiviertel, Originalmaterial: [04_Reference_ThreeQuarter.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/04_Reference_ThreeQuarter.png)
- Kopf vorne, neutraler Clay-Override: [05_Reference_Clay_Front.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/05_Reference_Clay_Front.png)
- Kopf vorne, sichtbare Highpoly-Dreieckstruktur: [06_Reference_Wire_Front.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/06_Reference_Wire_Front.png)
- Gesamtfigur in schräger orthografischer 2,5D-Nahansicht: [07_Reference_2_5D.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/07_Reference_2_5D.png)
- Kopf Dreiviertel, Clay-Override: [08_Reference_Clay_ThreeQuarter.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/08_Reference_Clay_ThreeQuarter.png)
- Kopf rechtes Profil, Highpoly-Wire-Override: [09_Reference_Wire_Profile.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/09_Reference_Wire_Profile.png)
- Kontaktbogen: Front / rechtes Profil / Dreiviertel: [10_Reference_Views.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/10_Reference_Views.png)
- Kontaktbogen: Clay / Highpoly-Wire: [11_Reference_Clay_Wire.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/11_Reference_Clay_Wire.png)

| Verlangter Nachweis | Tatsächlicher Stand |
|---|---|
| Kopf Front / Profile / Dreiviertel | Referenz neu gerendert; kein Lowpoly-Nachher vorhanden |
| Clay und Wire | Referenz neu gerendert; keine kontrollierten Ziel-Loops zu bewerten |
| Kopf mit gebackenen Zielmaterialien | **Nicht durchgeführt**, da keine gültige Zielgeometrie/UVs |
| 2,5D | Referenz-Nahansicht gerendert; keine optimierte Variante |
| A/B-Vergleich Augen/Mund/Nase/Silhouette | **Nicht möglich**, kein gültiger Kopfpilot; keine vorgetäuschte Gleichheit |
| Deformations-/Animationseignung | **Nicht nachgewiesen**, manuelle Modellierung und später Tests erforderlich |

### Selbstkritische visuelle Bewertung

Front, beide Profile, Dreiviertel, Clay, Wire und 2,5D wurden tatsächlich betrachtet. Das Original behält eine gute Frisuren-/Gesichtssilhouette. Im Clay fehlen jedoch eindeutig getrennte Augäpfel und ein nachgewiesener offener Mundinnenraum; ein erheblicher Teil der Augenwirkung stammt aus dem Material. Dichte Dreiecke und teils überlappende Haarflächen erschweren zuverlässige automatisch projizierte Gesichtsloops. Die neuen Bilder belegen keine qualitative Verbesserung einer Retopologie, weil diese noch nicht modelliert wurde.

## Tatsächliche Prüfung

- Neue Datei in separatem Blender gespeichert und final erneut geöffnet: erfolgreich.
- Geometrie-, UV- und Normal-Hashes identisch zur Highpoly-Quelle; Originalmaterialgraph einschließlich Links, Principled-Eingängen und gepackten Bildinhalten identisch.
- Höhe/Transformationsmaßstab erhalten: praktisch 1,40 m; keine Anpassung auf 1,32 m in diesem Auftrag.
- Alle Collections, Face Project, Mirror/Shrinkwrap-Ziel, Offset, Auswahl-Lock, gepackte Bildreferenzen und eingebettete Anleitung nach Wiederöffnung geprüft.
- Nur zwei Mesh-Objekte in der neuen Szene: komplette Quelle und leerer Zielkörper. Kein alter Testproxy, kein Armature-Objekt, keine Actions.
- Erste QA lief an einem exakten Float-Vergleich für den 0,5-mm-Offset aus; korrekte Float-Toleranz ergänzt. Wiederholung erfolgreich. Das war ein Prüfscriptthema, kein Geometriefehler.
- Keine neuen Manifold-/Normalen-/Selbstschnitt-Ergebnisse für einen retopologisierten Kopf: es gibt keinen solchen Kopf. Vorbereitete Prüfhilfen sind nicht mit bestandenen Deformationstests gleichzusetzen.
- Keine Unreal-Builds/Automationstests: Unreal und Gameplay wurden nicht verändert.

## Empfehlung und offene Arbeit

**Manuelle Kopfretopologie vor jeder weiteren Automatisierung.** Zuerst Lid- und Mundloops samt Nasen-/Wangenverbindungen sichtbar aufbauen und Front/Profil/Dreiviertel prüfen. Danach Schädel, Ohren und Hals schließen, ursprüngliche Asymmetrien lokal berücksichtigen und definierte Arbeitsränder/Poles auditieren. Erst nach bestätigter Form UVs und einen lokalen Bake-Piloten erstellen. Die Highpoly-Quelle bleibt dafür erhalten, ihre bekannten Kontakt-/Topologiefehler müssen bei Bake-Projektion gezielt berücksichtigt werden.

Dieses Ergebnis ist ein sicherer, dokumentierter Start für manuelle Arbeit, **keine Freigabe als animationsfähiger oder game-ready NPC**. Hier wurde gestoppt. Keine Haare, Kleidung, Retopologie der übrigen Figur, Rigging oder Unreal-Integration begonnen.

## Git und Dateien

Kein Commit, kein Push, nichts gestaged. Bestehende Änderungen unverändert. `git diff --check` und abschließender Status werden in `GitFinal.json` protokolliert. Da der gesamte NPC-Ordner schon vorher untracked war, zeigt der kurze Gesamtstatus neue V2-Dateien nicht einzeln; der gezielte Status ist dort zusätzlich enthalten.

Aktueller gezielter Git-Status vor Erstellung dieses Berichts:

```text
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/MANUELLE_RETOPO_ANLEITUNG.md
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/PreviewManifest.json
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/01_Reference_Front.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/02_Reference_Right.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/03_Reference_Left.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/04_Reference_ThreeQuarter.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/05_Reference_Clay_Front.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/06_Reference_Wire_Front.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/07_Reference_2_5D.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/08_Reference_Clay_ThreeQuarter.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/09_Reference_Wire_Profile.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/10_Reference_Views.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/Previews/11_Reference_Clay_Wire.png
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/ProtectedBefore.json
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/ProtectionAfter.json
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/ReopenAudit.json
?? Art/Characters/NPCs/Westland/HobbitBase/Review/Retopo_V2/WorkspaceAudit.json
?? Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_Retopo_V2.blend
?? Art/Characters/NPCs/Westland/HobbitBase/Tools/Retopo_V2/FinalizeWorkspace.py
?? Art/Characters/NPCs/Westland/HobbitBase/Tools/Retopo_V2/PrepareWorkspace.py
?? Art/Characters/NPCs/Westland/HobbitBase/Tools/Retopo_V2/ReopenAndAudit.py
?? Art/Characters/NPCs/Westland/HobbitBase/Tools/Retopo_V2/SaveAndRenderReference.py
```

Die `.blend1` ist eine neu entstandene Blender-Sicherung der neuen V2, kein bestehendes Original. Logs, Hashlisten und Review-JSON sind Prüfarbeitsartefakte. Eine vollständige neue Dateiliste folgt in `NewFiles.json`; keine Datei wurde gelöscht.
