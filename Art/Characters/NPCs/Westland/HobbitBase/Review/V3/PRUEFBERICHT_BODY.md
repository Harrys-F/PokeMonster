# Westland Hobbit NPC Base V3 – Körper-Prüfbericht

14.10.2026 · Phase 1 · Ausgangs-HEAD `3c6dc47`.

## Ergebnis

Eine neue, gespeicherte Körper- und Gesichtsstruktur wurde aufgebaut. **Das angestrebte hochwertige erwachsene Fantasy-Charakterdesign ist noch nicht erreicht. Keine künstlerische oder Produktionsfreigabe.** Die technische Neustrukturierung ist überprüft; die sichtbaren anatomischen und gestalterischen Schwächen bleiben unten ausdrücklich benannt.

Master: [Hobbit_NPC_Base_V3_Body.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_Base_V3_Body.blend). Die Datei wurde in einem separaten Blender-5.2.2-LTS-Prozess erneut geöffnet und geprüft. V1 und V2 bleiben unverändert. Keine externen Modelle, kein Meshy, kein Unreal-Import.

## Referenzen und Aufbau

[AGENTS.md](/Users/harry/Developer/PokeMonster/Game/PokeMonster/AGENTS.md) und relevante Projektunterlagen wurden gelesen. Vorhandene [Front.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer/Reference/BarefootFinal/Front.png) und [Portrait.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer/Reference/BarefootFinal/Portrait.png) dienen ausschließlich als gezeichnete Stil-/Farbreferenzen. **Keine eigene erwachsene Hobbit-NPC-Anatomiereferenz gefunden.** Der erwachsene Körperentwurf folgt der Nutzerbeschreibung. V1/V2 dienten nur der Größen-/Proportionskontrolle; keine Körpervertices oder Topologie daraus übernommen.

Die Haut wurde aus eigenen Querschnitten und explizit verbundenen Quad-Patches vollständig neu konstruiert. Kopf, Hals, Rumpf, Arme, Hände, Becken, Beine, Füße und Zehen bilden **ein** Mesh. Es gab keine Boolean-Union, kein Remesh, keine Subdivision und keine bloße Glättung der V2. Augenhöhlen, Lidkonturen, Nasenöffnungen, Lippen und Ohrmuscheln sind in der Haut verbunden. Zwei separate, geschlossene Augäpfel sitzen in den Höhlen; keine aufgeklebten Iris-/Lippenscheiben.

Während der Sichtprüfung korrigiert: zu kleiner erster Kopf, vorstehende Augen, dominante rechteckige Ohransätze, vier lokal kreuzende Dreieckpaare am unteren Ohransatz, kantige Fersen und ein harter Absatz am Fußrücken. Querschnittsformen und lokale Formkontrollen wurden dafür geändert; keine zusätzlichen Körper-Primitive gestapelt. Eigene Sicherungsstufen 01–09 liegen in `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/StagesV3/`. Frühere Stufen sind **ungeprüfte Zwischenstände**, keine freigegebenen Alternativen.

Collections: eigene BODY-, EYES- und STUDIO-Collections mit `HNV3_`-Präfix. Der Quellmaster enthält drei Modell-Meshes; Studioboden, Kamera und drei Flächenlichter werden nicht als Körperteile gezählt. Noch keine Haare, Kleidung, Nägel oder Fußbehaarung. Keine Armature, keine Actions, kein Skinning.

## Maße und Pose

Meter, METRIC, Unit Scale **1,0**. Sohlenkontakte bei **Z=0**. Die Fußunterseite besitzt eine kleine mediale Wölbung.

- Aktuelle Höhe ohne Haare: **1,281999946 m = 128,20 cm**.
- Vorgesehene zusätzliche Haarhöhe: **3,80 cm** bis zur späteren Gesamthöhe **1,32 m**. Diese Haare existieren noch nicht.
- Bilaterale Hautabweichung: **0 m** im gemessenen Vertexvergleich.
- T-Pose mit geraden horizontalen Armachsen auf ungefähr **1,003 m**; Handflächen nach unten, Daumen seitlich/vorne abgespreizt.
- Ein Kopf, zwei Arme, zwei Hände, zwei Beine, zwei Füße; je vier Finger plus Daumen und je fünf Zehen. Schnittprüfungen und Ganzkörperbilder bestätigen die Anzahl.
- Varianten zwischen 1,20–1,45 m sind weiterhin nur spätere Ableitungen, keine zusätzlich erzeugten Modelle.

## Tatsächliche Geometriezahlen

Ohne Studio, ohne Vergleichs-V2. Keine aktiven Körper-Modifikatoren.

| Mesh | Vertices | Flächen | Dreiecke |
| --- | ---: | ---: | ---: |
| HNV3_Body | 10.499 | 10.776 | 20.994 |
| HNV3_Eyeball_L | 1.298 | 1.344 | 2.592 |
| HNV3_Eyeball_R | 1.298 | 1.344 | 2.592 |
| **Gesamt: 3 Meshes** | **13.095** | **13.464** | **26.178** |

Haut: **10.218 Quads, 558 Dreiecke, 0 N-Gons**; etwa **94,8 %** der Flächen sind Quads. Dreieckfans dienen überwiegend distalen Verschlüssen und vertieften Gesichtskonturen; am Hals existiert der geordnete Übergang zwischen 48er Körper- und 96er Kopfring. Die Arm-/Ellbogenringe haben 20, Bein-/Knieringe 32 Punkte; Finger besitzen acht, Daumen zehn Punkte im Umfang.

Vergleichbare Hautzahl: V2 **27.090** → V3 **20.994 Dreiecke**, etwa **22,5 % weniger**. V2s Gesamtzahl 121.186 enthält Haare, Kleidung und weitere Details und ist kein direkter Runtime-Vergleich. V3 ist noch keine optimierte Unreal-Variante; keine Performancebehauptung.

## Technische Prüfung

Ergebnis aus der erneut geöffneten Quelle: eine Hautkomponente; **0 offene Kanten, 0 Non-Manifold-Kanten, 0 lose Vertices, 0 degenerierte Flächen und 0 doppelte Vertexpaare innerhalb 0,1 µm**. Euler-Charakteristik **2**. Konsistent berechnete Normalen und positives orientiertes Volumen; 0 Fehler in der gemeinsamen Kantenorientierung und 0 ungültige Flächennormalen.

Keine erkannten eigentlichen Kreuzungen nicht benachbarter Hautdreiecke im BVH-/Segment-Test des Endstands. **Grenzen:** Der Test schließt gemeinsame Vertexpaare, koplanare Überlappungen und tangentiale Kontakte aus. Er ist kein vollständiger mathematischer Beweis. Die separate Augapfel-/Haut-Einbettung ist beabsichtigt. Selbstüberschneidungen bei Verformung wurden nicht geprüft.

Gelenk- und Gesichtsschleifen sind angelegt. Pole, Fingerwurzelübergänge, Halsauflösung und Lippen-/Lidschleifen benötigen vor einem gemeinsamen Hobbit-Rig eine weitere fachliche Prüfung. Geschlossene Topologie allein beweist keine Deformationsqualität. **Kein Rigging, keine Gewichte und keine Deformationstests durchgeführt.**

## Sichtprüfung und offene Qualität

Front, Profil und Dreiviertel stellen denselben Körper konsistent dar. Der kompakte Körper, kürzere Beinanteil, kräftigere Schulterpartie und große breite Füße sind erkennbar. Lid-/Lippen-/Ohrkonturen und Nasenöffnungen sind geometrisch eingebettet. Die Haut hat ein eigenes neutrales Material: Roughness **0,72**, Specular IOR Level **0,20**, sehr zurückhaltende Farbvariation. Keine fertigen Textursets.

**Nicht ausreichend überzeugend:**

- Gesicht weiterhin schematisch und teilweise puppenhaft; die erwachsene, freundliche Persönlichkeit ist nicht sicher erreicht. Eine deutliche künstlerische Verbesserung des Gesichtes gegenüber V2 ist nicht ausreichend belegt.
- Stirn-/Wangen-/Kieferflächen und Lippenprofil benötigen bewussteres Sculpting. Augenwinkel und Lidvolumen wirken noch zu gleichförmig; die Nase ist noch vereinfacht. An den Nasenöffnungen bleiben im Nahbild eckige Übergänge sichtbar.
- Ohren besitzen verbundene Rand-/Innenkonturen, aber noch keine voll überzeugende Ohr-Anatomie.
- Schulter-/Achsel-, Becken- und Rückenformen sind noch zu vereinfacht. Die geplante Gelenkstruktur ist brauchbarer als zufällige Verbindungen, jedoch noch nicht animationsgeprüft.
- Handflächen, Fingerwurzeln, Knöchel und Zehenpolster zeigen lokale kantige Übergänge. Die Fußrückenlinie wurde korrigiert; anatomische Feinmodellierung bleibt offen.

**Grenze der bisherigen rein prozeduralen Modellierung:** Der neue Ring-/Patchaufbau verbessert die technische Grundlage, erreicht hier bisher aber nicht die geforderte hohe künstlerische Qualität. Zusätzliche Polygonzahl oder Subdivision wäre dafür kein ausreichender Ersatz. Vor der Freigabe sind gezielte Formarbeit und erneute Sichtprüfung erforderlich.

## Zwölf echte Blender-Vorschauen

Cycles CPU, vier Threads, 40 Samples, Denoising, eigene neutrale Studiobeleuchtung mit weichen Schatten. Ganzkörperansichten vollständig eingerahmt. Die 2,5D-Aufnahme ist eine gut lesbare schräge **Blender-Nahansicht**, keine Änderung der Unreal-Kamera und kein Unreal-Screenshot.

Der Vergleich zeigt V2-Haut/Gesicht ohne Haare/Kleidung links und V3 rechts, im selben Bild mit identischer orthografischer Kamera, Beleuchtung und neutralisiertem Hautmaterial. Die V2 wird dafür nur in einem temporären Renderprozess lesend angehängt; keine Vergleichskopie im Master gespeichert.

1. [Vorderansicht, ganzer Körper](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_01_Front.png)
2. [Rückansicht, ganzer Körper](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_02_Back.png)
3. [Seite −X / links nach bisheriger Dateikonvention](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_03_Side_Left.png)
4. [Seite +X / rechts nach bisheriger Dateikonvention](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_04_Side_Right.png)
5. [Dreiviertelansicht, ganzer Körper](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_05_ThreeQuarter.png)
6. [Gesicht von vorne](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_06_Face_Front.png)
7. [Gesicht im Dreiviertelprofil](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_07_Face_ThreeQuarter.png)
8. [Gesicht von der Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_08_Face_Profile.png)
9. [Handdetail; Gegenhand symmetrisch](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_09_Hands.png)
10. [Beide Füße als Detail](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_10_Feet.png)
11. [Schräg erhöhte 2,5D-Nahansicht](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_11_Camera25D.png)
12. [V2–V3-Vergleich, gleiche orthografische Kamera](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Previews/Hobbit_V3_12_Compare_V2_V3.png)

## Erhaltung, Dateien und Stopp

SHA256-Vergleich der **1.551 vor Arbeitsbeginn erfassten Dateien**: unverändert, keine fehlenden Dateien. Darunter V1, V2 und deren Vorschauen/Berichte sowie bestehende Player-/Sprint-Arbeiten. Neue Dateien ausschließlich in `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase`: V3-Master, `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/StagesV3/`, `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V3/`, `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/`. [Dateiliste](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/NewFiles.json), [Rohprüfung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/ReopenAudit.json), [Erhaltungsprüfung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/Preservation.json), [Git-Status](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V3/GitStatus_Final.txt).

`git diff --check`: erfolgreich, ohne Ausgabe. Unreal-Build, PIE und Unreal-Automation wurden nicht ausgeführt, weil keinerlei Unreal-Dateien geändert wurden. Kein Staging, Commit oder Push. Review-Logs und Blender-Backups sind Arbeitsartefakte und nicht pauschal versionierungswürdig.

**Entwicklung nach dieser Körperphase gestoppt.** Haare, Kleidung, Rigging, Skinning und Animationen werden erst nach Harrys ausdrücklicher Körper-/Gesichtsfreigabe begonnen. Keine Freigabe aus bestandenen Geometrieprüfungen abgeleitet.
