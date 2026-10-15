# Westland Hobbit NPC Base V2 – Modell- und Qualitätsprüfung

Stand: 14.10.2026. Ausgangs-HEAD: `3c6dc47 Extend player sight visibility to all test map tree families`.

## Ergebnis und Freigabestatus

Die neue Blender-Arbeitsversion wurde gespeichert, in einem getrennten Blender-5.2.2-LTS-Prozess erneut geöffnet, geprüft und gerendert. **V2 ist ein überarbeiteter Master-Zwischenstand, kein produktionsreifer NPC.** Die geforderte hochwertige erwachsene Fantasy-Charakterqualität ist noch nicht vollständig erreicht. Insbesondere Gesicht, Locken, Kleidung und lokale Hand-/Fußübergänge benötigen weitere sichtbare Modellarbeit; bestandene Geometrieprüfungen ersetzen diese nicht.

- Neue Quelle: [/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_Base_V2.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_Base_V2.blend).
- Ausgangsquelle `Source/Hobbit_NPC_Base_V1.blend` und alle V1-Vorschauen/Berichte bleiben unverändert.
- Kein Meshy, kein externes Charaktermodell, keine neue Abhängigkeit. Modellierung aus eigener V1 und Blender-Python über die bestehende Blender-MCP-Verbindung.
- Noch kein Rig, Skinning, keine Animation, kein Unreal-Export oder Import.
- Keine bestehenden Unreal-, Player-, Sprint-, Map- oder Gameplaydateien geändert.

## Referenzen und Ausgangsprobleme

`AGENTS.md`, die relevanten Abschnitte von `Docs/TECHNIK.md`, `Docs/ENTSCHEIDUNGEN.md`, `Docs/GRAFIKSTIL.md`, `Docs/SPIELIDEE.md` und `Docs/SPIELREGELN.md` wurden gelesen. Als vorhandene gezeichnete Stilreferenzen wurden `Art/Characters/YoungTrainer/Reference/BarefootFinal/Front.png` und `Portrait.png` geprüft. Sie dienen für Farbwelt, stilisierte Haarwirkung und barfüßige Fantasygestaltung. Sie zeigen einen jungen Trainer und sind ausdrücklich **keine erwachsene NPC-Anatomiereferenz**. Eine eigene erwachsene Hobbit-NPC-Referenz wurde nicht gefunden; die Nutzerbeschreibung war dafür maßgeblich.

V1 besaß einen stark vereinfachten Kopf, aufgesetzte Augen-/Mundformen, einfache Lockenvolumen, grobe Hände/Fußübergänge und glatte Kleidungsformen. Die kompakte Körperbasis und T-Pose wurden übernommen; fehlende Qualität wurde durch eigene Formarbeit überarbeitet, nicht durch zusätzliche Accessoires ersetzt.

## Änderungen gegenüber V1

1. **Körper:** Ursprüngliche Schulter-/Arm-/Beinbasis erhalten; Kopf, Hände und Füße lokal neu aufgebaut und zu einer geschlossenen Haut verbunden. Natürlichere Hals-/Kiefer-/Wangen-/Kinnformen, modellierter Nasenrücken mit Spitze und Flügeln sowie angepasste Ohren. Handwurzel und Knöchelübergänge geglättet. Sohlen bleiben bei Z=0.
2. **Gesicht:** Mandelartig verkleinerte Augenöffnung, integrierte Augenhöhlenhaut, Ober-/Unterlider, Brauen, Ohrfalten, dezente Nasenöffnungen und Lippenflächen mit Mundspalt. Ausrichtung beider Augen nach vorne; keine Ausdrucksanimation.
3. **Haare:** Eigenes voluminöses Unterhaar mit braunen, gebogenen, unterschiedlich großen Lockengruppen. Vier zurückhaltende Braunvarianten und längs gerichtete prozedurale Oberflächenstruktur. Unregelmäßige Locken werden paarweise gespiegelt, um die Grundsymmetrie zu erhalten. Dezente einzelne Fußhaare.
4. **Hände:** Je vier Finger und ein eigener Daumen, unterschiedliche Fingerlängen, Handflächen-/Knöchelvolumen und modellierte Nägel. Nach sichtbaren Durchdringungen wurden die Nägel zuletzt als dünne, an die tatsächliche Hautoberfläche angepasste Schalen neu erstellt.
5. **Füße:** Breite barfüßige Form mit Ferse, Spann, Sohlenprofil und je fünf getrennt erkennbaren Zehen. Abgestufte Zehengrößen, Nägel und zurückhaltende Fußbehaarung. Noch kein vollständiges anatomisches Feinsculpting.
6. **Kleidung:** Cremefarbenes Leinenhemd mit geöffnetem Kragen, Knopfleiste, Nähten, gerollten Ärmelabschlüssen und milden Falten. Separat geöffnete braune Weste mit kleinen Knöpfen und Kanten. Olivbraune Kniehose mit Saum und Faltenvariation. Gürtel und Schnalle separat. Nach einem fehlerhaften experimentellen Westenschnitt wurde die stabile eigene V1-Schulterkonstruktion in einer isolierten V2-Kopie überarbeitet.
7. **Materialien:** Eigene zurückhaltende Haut-/Leinen-/Woll-/Leder-/Metall-/Haarfamilien mit prozeduraler Mikrostruktur. Keine geladenen externen Texturen, kein finales Texture Painting, keine gebackenen Runtime-Texturen.

## Organisation und nichtdestruktive Zwischenstände

Aktive Szene: `Hobbit_NPC_Base_V2`. Collections: `HNV2_HOBBIT_BODY`, `HNV2_HOBBIT_CLOTHING`, `HNV2_HOBBIT_FACE`, `HNV2_HOBBIT_HAIR`, getrennte `HNV2_PREVIEW_STAGE` und ausgeblendete `HNV2_ARCHIVE_V1`. Die Archive bewahren eigene vorherige Bauteile; sie zählen nicht als aktive Gliedmaßen und werden nicht gerendert. Körper, Hemd, Weste, Hose, Gürtel und Schnalle bleiben getrennt organisiert. Kopf, Rumpf, Arme, Hände, Beine und Füße gehören zum zusammenhängenden Hautmesh.

`Source/Stages/Hobbit_NPC_Base_V2_*.blend` enthält neue lokale Sicherungsstufen; manche frühere experimentelle Stufen enthalten bekannte Zwischenfehler. **Nur `Source/Hobbit_NPC_Base_V2.blend` ist der geprüfte Endstand dieses Auftrags.** `Tools/V2/` enthält die nachvollziehbaren Blender-Python-Arbeitsschritte, Normalisierung, Audit und Renderer. Es wurden keine vorher vorhandenen Quelldateien überschrieben.

## Maße, Symmetrie und Körperteile

Blender-Einheitensystem `METRIC`, Unit Scale **1,0**; Koordinaten in Metern.

- Gesamthöhe einschließlich Haaren: **1.3200000525 m = 132,000005 cm**. Zielabweichung ca. 0,000005 cm, Float-Rundung.
- Sohlenunterkante: **0.000000 m**. Haaroberkante: **1.3200000525 m**.
- Schädel-/Hautoberkante: **1,288 m**; die Differenz zur Gesamthöhe gehört zu den Haaren.
- Maximale numerische X-Symmetrieabweichung der Haut: **0 m**.
- Gerade, seitlich ausgestreckte Arme in T-Pose auf gleicher Schulterhöhe; ungefähr 1,544 m Handspannweite.
- Schnittprüfungen: ein Kopf, je ein linker/rechter Arm, zwei Beine; je vier Finger plus insgesamt zwei Daumen; zehn getrennte vordere Zehenkonturen. Front-, Rück-, Seiten- und Dreiviertelbilder ergänzen die Schnittprüfungen.
- Genau zwei Arme, zwei Hände, zwei Beine und zwei Füße; keine zusätzlichen aktiven Gliedmaßen.
- Größenvarianten 1,20–1,45 m bleiben ein späterer Ableitungsbereich; keine zusätzlichen Varianten erzeugt.

## Mesh- und Dreieckzahlen

Aus dem tatsächlich erneut geöffneten Endstand, **mit ausgewerteten Modifikatoren**, ohne Studio und ausgeblendete Archive. „Meshes“ bezeichnet sichtbare Mesh-Objekte, nicht zusammenhängende Inseln innerhalb eines Detailobjekts.

| Kategorie | Mesh-Objekte | Vertices | Dreiecke |
| --- | ---: | ---: | ---: |
| Zusammenhängende Haut / Körper | 1 | 13,539 | 27,090 |
| Kleidung einschließlich Gürtel / Schnalle | 5 | 13,416 | 26,756 |
| Separate Augen, Lider, Lippen, Ohren-Details und Nägel | 22 | 9,866 | 19,568 |
| Kopfhaar und Fußbehaarung | 3 | 24,232 | 47,772 |
| **Gesamt** | **31** | **61,053** | **121,186** |

| Kleidungsobjekt | Vertices | Dreiecke |
| --- | ---: | ---: |
| HNV2_Belt | 256 | 512 |
| HNV2_Buckle | 280 | 540 |
| HNV2_Breeches | 3,230 | 6,456 |
| HNV2_Shirt | 6,908 | 13,776 |
| HNV2_Waistcoat | 2,742 | 5,472 |

V1 hatte 88.060 Dreiecke insgesamt. V2 liegt bei 121,186 Dreiecken: mehr als V1, hauptsächlich durch modellierte Locken und Gesichts-/Nageldetails. Die Haut wurde von 33.512 auf 27.090 Dreiecke reduziert; Kleidung stieg von 21.948 auf 26.756 Dreiecke. **Dies ist kein optimierter Crowd-/Runtime-Stand.** Kopf-/Fußhaar kostet allein 47.772 Dreiecke. Diese Kosten müssen vor vielen gleichzeitig sichtbaren NPCs reduziert werden.

## Topologie und Prüfgrenzen

Die gespeicherte Quelle wurde unabhängig erneut geöffnet; `ReopenAudit.json` hält die Rohwerte und die ausgewerteten Objektbounds fest.

- Haut: **eine** zusammenhängende Komponente mit 13.539 Vertices.
- Nicht-manifold Kanten: **0**; offene Kanten: **0**; degenerierte Hautflächen: **0**.
- Hautflächen: **11.362 Quads, 246 Dreiecke, 832 N-Gons**.
- Auswärts gerichtete Hautnormalen nach den Verbindungen neu berechnet.
- Körper-/Kleidungsabstand: Alle Vertices der fünf Kleidungsobjekte gegen die geschlossene Haut abgetastet. Keine negativen Abstände jenseits 0,6 mm. Mindestabstand bei Hemd/Hose ungefähr 1,49 mm, Weste 2,0 mm.

Diese Vertexprüfung ist **kein vollständiger Dreieck-Dreieck-Kollisionstest** und keine Garantie gegen Kleidungsdurchdringungen bei Bewegung. Schulter-/Ellbogen-/Hüft-/Kniebereiche besitzen Grundringe; Boolean-Verbindungen an Händen/Füßen/Ohren und Augenhöhlen sowie 832 N-Gons benötigen gezielte Retopologie. Nicht jede separate Detail- oder Stoffkante ist als einheitliche Deformationstopologie angelegt. Eine geschlossene Haut ist deshalb nicht automatisch animationsbereit.

Nicht durchgeführt: Gewichtung, Gelenkverformung, Facial-Rig, vollständige Selbstüberschneidungsprüfung, Unreal-Import, PIE, Runtime-Performance. Armatures **0**, animierte Objekte **0**. Die übrigen Projekt-Automationstests wurden nicht ausgeführt, weil dieser Auftrag keine Unreal-Dateien verändert.

## Visuelle Abnahme und offene Modellierungsprobleme

Front, beide Seiten, Rückseite, Dreiviertel und schräge Nahansichten wurden anhand tatsächlicher Blender-Ausgaben geprüft. Hobbit-Grundproportionen, große barfüßige Füße, kompakter Rumpf und T-Pose sind erkennbar. Die nähere 2,5D-Ansicht zeigt Kopf-/Haarvolumen und Kleidung deutlich; die 2850-cm-Perspektive ist nur ein technischer Fernvergleich.

**Verbleibende Qualitätsabweichungen:**

- Gesicht: Wangen-/Kinnform und Lidansatz sind verbessert, aber weiterhin sehr glatt und weich. Die erwachsene, charaktervolle Fantasywirkung ist noch nicht überzeugend genug; die Figur behält Anteile einer Puppen-/Spielzeugwirkung. Nase, Mundwinkel, Lidvolumen und Ohranatomie benötigen gezieltes Sculpting, ohne den Kopf kindlicher zu machen.
- Haare: Volumen und Lockenrichtung sind verbessert. Aus der Detailkamera wirken einzelne Gruppen noch wie wiederholte modellierte Klumpen; an Spitzen/Übergängen sind lokale Facetten und Lücken sichtbar. Eine besser zusammenhängende, bewusst komponierte Lockensilhouette und weichere Übergänge fehlen.
- Hände/Füße: Vollständige Anzahl vorhanden; Fingerwurzeln und Zehenansätze wirken teilweise noch kantig. Knöchel, Fingerpolster, Nagelbetten und Zehenansätze sind vor einer Qualitätsfreigabe nachzuarbeiten. Die zuletzt korrigierten Nägel wurden in den finalen Hand-/Fußdetailbildern geprüft: keine früheren fleckigen Hautdurchdringungen mehr sichtbar. Die Schalen sind noch vereinfacht und brauchen natürliche Nagelbetten.
- Kleidung: Kragen und einige Saumkanten sind noch zu hart bzw. unregelmäßig. Hemd und Hose wirken in großen Bereichen zu glatt; Stoffzug und Falten um Achseln, Ellbogen, Schritt und Knie sind noch nicht glaubwürdig genug. Am Hemdsaum ist eine leicht gezackte Linie sichtbar. Die Weste hat eine brauchbare Schulterform, aber noch einen vereinfachten Schnitt.
- Materialien: Prozedurale Mikrostruktur bleibt im Render sehr dezent; die angestrebte handgemalte Materialqualität ist nicht fertig. Noch keine finalen UVs, Texture-Bakes oder gemalten Farbdetails.

**Keine Produktionsfreigabe.** Der Auftrag hat einen sichtbaren und technisch gesicherten V2-Arbeitsstand erzeugt; die volle künstlerische Zielqualität bleibt offen. Die detaillierten Vorschauen sind ausdrücklich zur ehrlichen Sichtprüfung vorgesehen.

## Gemeinsames Hobbit-Rig und Runtime-Plan

Grundsymmetrie, T-Pose, vollständige Gliedmaßen und getrennte Kleidungsobjekte bilden eine brauchbare Ausgangsbasis für ein späteres gemeinsames Rig. **Rig-Eignung wurde noch nicht durch Deformation getestet.** Vorher sind lokale Retopologie mit klaren Gelenkloops, Augen-/Mundloops, saubere Fingerwurzeln und eine engere Abstimmung zwischen Haut und austauschbarer Kleidung nötig.

Blender-Master und zukünftige Unreal-Runtime-Version bleiben getrennt. Die Runtime-Variante wurde noch nicht erzeugt. Vorgesehener separater Pfad: `Art/Characters/NPCs/Westland/HobbitBase/Runtime/`. Ein möglicher späterer Planungsbereich ist ungefähr 18–30k Dreiecke für eine nahe NPC-Stufe, mit reduzierter Haargeometrie, gebackenen Details, Materialzusammenfassung und LODs. **Dies ist ein unverbindlicher Budgetplan, kein getesteter Performancewert oder bereits vorhandenes Asset.**

## Neue Vorschauen

Zwölf echte Blender-Cycles-CPU-Renders, vier Threads, 40 Samples mit Denoising. Front/Rück/Seiten sind orthografisch. 2,5D-Nahansichten sind bewusst enger gefasste orthografische Qualitätsansichten, keine Änderung der Unreal-Kamera. Der technische Fernvergleich verwendet 2850 cm Abstand und 35° horizontales FOV. **Keine dieser Aufnahmen ist ein Unreal-Screenshot.** Kameraparameter wurden nur im Renderprozess verändert; die Quelle wird dabei nicht gespeichert.

1. **Vorderansicht**: [Front](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Front.png)
2. **Rückansicht**: [Back](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Back.png)
3. **Seite −X (V1-Bezeichnung: links)**: [Side_Left](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Side_Left.png)
4. **Seite +X (V1-Bezeichnung: rechts)**: [Side_Right](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Side_Right.png)
5. **Dreiviertel**: [ThreeQuarter](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_ThreeQuarter.png)
6. **Schräg erhöhte 2,5D-Nahansicht**: [Camera_25D_Detail](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Camera_25D_Detail.png)
7. **Technischer 2850-cm-/35°-Vergleich**: [Camera_25D_2850cm](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Camera_25D_2850cm.png)
8. **Gesicht und Haare**: [FaceHair_Detail](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_FaceHair_Detail.png)
9. **Handdetail; Gegenhand symmetrisch**: [Hands_Detail](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Hands_Detail.png)
10. **Beide Füße**: [Feet_Detail](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Feet_Detail.png)
11. **Kleidung**: [Clothing_Detail](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_Clothing_Detail.png)
12. **Zusätzliche gut lesbare 2,5D-Nahansicht**: [25D_Readability](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V2/Previews/Hobbit_V2_25D_Readability.png)

`PreviewPaths.json` listet die tatsächlichen Dateien. Die beiden Seitenbezeichnungen behalten V1s Dateikonvention bei; entscheidend ist die ausdrücklich angegebene Weltseite −X / +X.

## Erhaltungsprüfung und Git

Vorhandene ungesicherte Player-/Sprint-Änderungen waren bereits vor diesem Auftrag vorhanden. Sie wurden weder zurückgesetzt noch bearbeitet. SHA256-Vergleich der **1.511 vor Arbeitsbeginn erfassten Projektdateien**: unverändert, keine fehlenden Dateien. Dazu gehören V1-Quelle, V1-Vorschauen, V1-Bericht, bestehende Blenderquellen, Unreal-Assets und Source-Dateien. Neue Dateien dieses Auftrags liegen ausschließlich im HobbitBase-Arbeitsbereich (`Source/Hobbit_NPC_Base_V2.blend`, `Source/Stages/`, `Tools/V2/`, `Review/V2/`).

`Erhaltungspruefung.json`, `Ausgangsdateien_SHA256.json` und `Neue_Dateien.json` stellen den Vergleich bereit. Review-Logs, Prüfsummen und Zwischenstände sind Arbeits-/Prüfarbeitsdateien und nicht automatisch eine Empfehlung, alles in Git aufzunehmen.

`git diff --check`: erfolgreich, keine Ausgabe. `GitStatus_Before.txt` / `GitStatus_Final.txt` dokumentieren den offenen Arbeitsbaum. Kein Staging, kein Commit, kein Push. Nach künstlerischer Prüfung wäre eine gezielte Sicherung nur der freigegebenen V2-Quelle, reproduzierbaren Modellskripte und des Berichts sinnvoll; kein pauschales `git add .`.

## Abschließender Git-Status

Die folgenden Source-/Sprint-Dateien waren bereits beim Start offen und blieben bytegleich. Der neue V2-Arbeitsbereich steckt in der zusammengefassten untracked Zeile `Art/Characters/NPCs/`.

```text
 M Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.cpp
 M Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.h
 M Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.cpp
 M Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.h
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h
 M Source/PokeMonster/Tests/PokeMonsterMeshyPlayerTest.cpp
 M Source/PokeMonster/Tests/PokeMonsterPlayerFoundationTest.cpp
?? Art/Characters/NPCs/
?? Art/Characters/YoungTrainer/Exports/SprintV1/
?? Art/Characters/YoungTrainer/Review/
?? Art/Characters/YoungTrainer/Source/Player_Meshy_Sprint_V1.blend
?? Content/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Run_V1.uasset
?? Source/PokeMonster/Tests/PokeMonsterPlayerSprintTest.cpp
?? Tools/Blender/CreateMeshySprintV1.py
?? Tools/ImportMeshySprintV1.py
```
