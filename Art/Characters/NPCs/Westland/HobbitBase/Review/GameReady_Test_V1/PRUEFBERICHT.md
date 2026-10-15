# Westland Hobbit NPC – Game-Ready Retopologie-Test V1

Prüfdatum: 14.10.2026. Ausgangs-HEAD: `3c6dc47 Extend player sight visibility to all test map tree families`. Blender 5.2.2 LTS, vorhandene MCP-Verbindung und getrennte native Blender-Python-Prozesse. Keine externen Modelle, Dienste, neuen Add-ons oder Retopologieprogramme.

## Klare Entscheidung

**Keine Freigabe für eine vollständige Game-Ready-Version mit dem getesteten automatischen Verfahren.** Der begrenzte Test und die Materialübertragung sind abgeschlossen; das Erfolgskriterium einer animationsgeeigneten Zieltopologie ist **nicht erreicht**.

Die automatische QuadriFlow-Retopologie wurde für Kopf/Haare und Oberkörper wegen nicht-manifolder Eingaben abgebrochen. Die verbleibenden Dreiecksmeshes sind ausschließlich **nicht freigegebene Reduktions-/Baking-Vergleichsobjekte**, keine endgültige Retopologie. An dieser Stelle wurde die automatische geometrische Bearbeitung gestoppt. Keine vollständige Figur automatisch reduziert.

Der Baking-Test zeigt nach Korrektur eines UV-Packfehlers, dass Base Color und PBR-/Normalendetails grundsätzlich übertragen werden können. In Nahansicht gehen Lockenrundung sowie Lid-/Mundvolumen verloren; Schnittnahtfehler, Überschneidungen und UV-Überlappungen bleiben. In der erhöhten Ansicht wirken die Unterschiede kleiner, das ersetzt keine Topologie- und Deformationsprüfung.

## Dateien und Schutz

- Unveränderte Quelle: `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_4K_Base_V1.blend`.
- Neue eigenständige Testdatei: `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_GameReady_Test_V1.blend`.
- Neue Bakes: `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1`.
- Neue Skripte: `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1`.
- Bericht und Nachweise: `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1`.

Die komplette Highpoly-Referenz liegt unabhängig in der Testdatei; Geometrie, UVs, Custom Normals, ursprüngliche Texturbilddaten und Materialgraph wurden gegen die Quelle geprüft und erhalten. Original-GLB, V1–V4, MeshyBase V1/V2, Spieler, 25-Bone-Rig, Animationen und Unreal-Dateien blieben unverändert. **1858 zuvor vorhandene Dateien per SHA-256 geprüft: keine verändert, keine fehlt.** Bereits offene Sprint-/Player-Änderungen wurden nicht zurückgesetzt.

## Tatsächlich untersuchte Bereiche

Die Quelle ist eine zusammenhängende sichtbare Gesamtoberfläche mit einem Material und einem 2K-Atlas; UV-/Normalennähte erzeugen viele importierte Inseln. Virtuelle Gleichsetzung exakt gleicher Positionen ergibt im vollständigen Modell eine Komponente. Hemd, Weste, Haut, Haare und Umhang sind damit keine zuverlässig automatisch austauschbaren Module.

Für diesen Test wurden nur zwei räumliche Ausschnitte über Dreiecksschwerpunkte gewählt:

1. **Kopf einschließlich Haare:** Z ≥ 1,105 m. 1.552.988 Quelldreiecke. Enthält Gesicht, Ohren und sämtliche Locken; keine behauptete saubere Hair-/Head-Modultrennung.
2. **Oberkörper:** 0,62 ≤ Z < 1,105 m und |X| ≤ 0,36 m. 562.301 Quelldreiecke. Enthält Hemd, Weste, Schulter-/Ärmelansätze und angeschlossene Kragen-/Umhang-/Zubehörflächen. Kein isoliertes Kleidungsstück und keine ganze Armretopologie.

537.172 Dreiecke außerhalb dieser Ausschnitte wurden als unveränderter Kontext erhalten. Hände, Beine und Füße wurden nicht optimiert. Die Ausschnittgrenzen sind offene Testgrenzen; sie dürfen nicht mit finalen Modularitätsnähten verwechselt werden. Kopf und Oberkörper wurden unabhängig reduziert, wodurch an der Schnittgrenze ein sichtbarer Spalt entsteht.

### Haar-, Gesichts- und Gelenkstruktur

Die Locken sind vielfach verschlungene Volumengeometrie, keine Hair Cards und keine separaten Strähnenobjekte. Ihre feinen Querschnitte, Spitzen und Zwischenräume reagieren empfindlich auf Edge Collapse. Augen-, Mund- und Nasenbereiche besitzen dense, ungerichtete Dreiecke statt geplanter Deformationsloops. Gemalte Augeninformationen liefern einen großen Anteil der Optik; sie ersetzen keine geometrisch geeigneten Lider für Blinzeln. Das Original besitzt weder Gewichte noch getrennte Augäpfel oder Rig.

Schulter-/Hemd-/Westenübergänge sind modellierte gemeinsame Oberflächen. Nähe allein reicht nicht aus, um sie automatisch in unabhängige Kleidung und Körper zu zerlegen. Neue Skin Weights wären in jedem Fall notwendig; keine Gewichte angelegt oder getestet.

## Verfahren und tatsächlicher QuadriFlow-Abbruch

1. Exakte Positionsgleichsetzung **nur an neu erzeugten Ausschnitt-Proxies**, um importierte UV-/Normalen-Splits aus dem numerischen Solver-Eingang zu entfernen. Quelle unangetastet.
2. Bounded Decimate als Solver-Vorbereitung: Kopf/Haare Ratio 0,025, Oberkörper 0,08. Keine globale Decimation und keine Freigabe als Endlösung.
3. QuadriFlow: Ziel Kopf 6.000 Faces, Oberkörper 5.000 Faces; Symmetrie aus (Quelle/Kleidung nicht exakt symmetrisch), Boundary Preserve an, Sharp Preserve aus, neue Attribute, Seed 42.
4. Beide Aufrufe geben `CANCELLED` zurück: „The mesh needs to be manifold and have face normals that point in a consistent direction“. Im vorbereiteten Kopf verbleiben 57 Kanten mit mehr als zwei Flächen, im Oberkörper zwei. Ausschnittgrenzen sind zudem offen. Die Warnung wurde nicht unterdrückt und nicht als erfolgreicher Remesh ausgegeben.
5. Keine weiteren blinden Remesh-/Repair-/Smooth-Schritte. Kein globaler Voxel-Remesh. Die automatischen Quad-Kandidaten existieren daher **nicht**. Geplante Shrinkwrap-Reprojektion nach QuadriFlow wurde mangels Quad-Ergebnis nicht ausgeführt.
6. Die vorbereiteten Dreieckskontrollen wurden ausschließlich für einen getrennten Baking-/Qualitätsverlusttest behalten. Es entstanden keine anatomischen Augen-/Mundringe oder Schulterloops.

## Gemessene Geometriezahlen

| Bereich | Quelle Dreiecke | Proxy-Vertices nach exakter Positionsgleichsetzung | Vergleich Vertices | Vergleich Dreiecke | Quads |
| --- | ---: | ---: | ---: | ---: | ---: |
| Kopf + Haare | 1.552.988 | 775.321 | 17.671 | 38.824 | 0 |
| Oberkörper | 562.301 | 282.950 | 23.997 | 44.984 | 0 |
| Beide Testbereiche | 2.115.289 | 1.058.271 | 41.668 | 83.808 | 0 |

Reduktion der ausgewählten Quelldreiecke: **96.04 %**. Diese Zahl beweist keine Rigging-Eignung.

Die vollständige Quelle hat 1.466.192 Vertices / 2.652.461 Dreiecke. In der Testdatei liegen vier Charakter-Mesh-Objekte: komplette Highpoly-Referenz, zwei Vergleichsbereiche und unoptimierter Rest. A rendert einen vollständigen Highpoly-Charakter; B rendert drei Meshes mit insgesamt **620.980 Dreiecken**, davon 537.172 unverändertem Kontext. **B ist kein 30.000–50.000-Dreiecke-Gesamtmodell.** Das spätere LOD0-Ziel wurde nicht durch weitere aggressive Reduktion erzwungen.

Materialien: Originalreferenz ein Material, jeder Vergleichsbereich ein eigenes neues Material, unoptimierter Kontext verwendet Originalmaterial. B zeigt damit drei Materialzuweisungen über drei Meshes. Zwei neue PBR-Materialien, jeweils fünf 2K-Bilder; drei ursprüngliche 2K-Bilder bleiben Referenz. Keine Unreal-Material-/Draw-Call-Messung.

Tatsächlich referenzierte originale Vertex-IDs in den Ausschnitten (vor jeder Positionsgleichsetzung): Kopf/Haare **881.083**, Oberkörper **302.541**. Überlappende Randvertices werden zwischen den Ausschnitten separat gezählt; ihre Summe ist keine Vertexzahl der gesamten Figur.

## Baking-Test und UV-Korrektur

### Erster Versuch – ausdrücklich verworfen

Smart Project mit Winkel 0,9 rad und `SCALED` Island Margin 0,008 erzeugte sehr viele kleine Charts. Gemessene summierte UV-Fläche: Kopf 0,00068556 (0,069 %), Oberkörper 0,0112558 (1,126 %). Die großzügigen skalierten Abstände ließen die tatsächlichen Inseln extrem schrumpfen. Die Bakes sahen wie einzelne Farbpunkte aus und erzeugten schwarze Dreiecke sowie verlorene Augen-/Mundinformationen. Dies war ein Fehler des Test-UV-Packings, **kein Beweis gegen die Originaltexturen**.

Alle ersten Bakes und ausgewählte erste Renderings sind unter `FirstBakeFailure/` erhalten. Die erste RNA-Abfrage des Cycles-Gerätetyps und eine spätere Diagnoseabfrage verwendeten in Blender 5.2 nicht vorhandene Typ-/Feldnamen; sie wurden im neuen Skript korrigiert. Beide Fehler betrafen nur neue Arbeitsprozesse, nicht die Quelle. Logs bleiben erhalten.

### Korrigierter Versuch – verwendetes Vergleichsmaterial

Nur UVs und Baking-Konfiguration der Testkontrollen angepasst, keine weitere Geometriebearbeitung:

- Smart Project: Winkel 1,15 rad, Area Weight 0,4, Scale To Bounds.
- Margin Method `FRACTION`, 4/2048 = 0,001953125 UV-Abstand.
- Gemessene summierte UV-Fläche: Kopf 0.119972, Oberkörper 0.261021.
- Cycles Selected to Active; CPU, drei Threads, 16 Samples.
- Automatisch extrudierter Cage **an**, kein manuell gestalteter Cage.
- Kopf: Extrusion 0,002 m / Max Ray Distance 0,015 m.
- Oberkörper: Extrusion 0,004 m / Max Ray Distance 0,025 m.
- Bake Margin zwei Pixel, Clear an, Auflösung 2048 × 2048 pro Bild, PNG/RGBA 8 Bit pro Kanal.
- Base Color: `DIFFUSE`, nur `COLOR`-Pass; kein Direct-/Indirect-Studiolicht übertragen. Bereits im Meshy-Albedo enthaltene gemalte Schattierung wird nicht entfernt.
- Normal: Tangent Space / OpenGL +Y. Blender-Material über Normal-Map-Node angebunden. Unreal-Normalenkonvention später ausdrücklich prüfen.
- Roughness und Metallic: Originalshader-Eingänge über eigene temporäre Emission-Materialkopien übertragen; Originalmaterial unverändert.
- AO: separate Diagnosemap; weder ins Albedo eingebrannt noch mit Base Color multipliziert. Keine Studioleuchten in AO.
- Base Color sRGB; Normal/Roughness/Metallic/AO Non-Color. Alpha des Base-Color-Bildes ist nur Hintergrund des Atlas, nicht an Shader-Alpha gebunden; Charakter bleibt opak.
- Zehn neue Bilder extern gesichert und in der Testdatei gepackt. Kein Textur-Upres.

Ergebnis: Augenfarbe, Haut, Kleidungsfarbübergänge, Westenknöpfe, Stoffmuster und viele Normalendetails bleiben in den neuen Bakes erkennbar. Die ersten großen schwarzen Fehler verschwinden überwiegend. Das ist eine positive Materialübertragungsprobe, **keine Freigabe** für UVs, Geometrie oder Animationen.

## Technische Restprobleme

| Messung | Kopf + Haare | Oberkörper |
| --- | ---: | ---: |
| Boundary-Kanten (einschließlich Testzuschnitt) | 538 | 3.338 |
| Kanten mit mehr als zwei Flächen | 57 | 2 |
| Lose Vertices | 7 | 1 |
| Flächen unter 1e−12 m² | 0 | 0 |
| UV-Innenflächen-Pixelüberlappungen bei 2K | 842 | 13.777 |
| UV-belegte Atlaspixel | 502.489 | 1.081.150 |
| Leere Base-Color-Alpha-Texel innerhalb UV | 23 | 2 |
| Schwarze Texel innerhalb UV | 22 | 1 |
| Bestätigte nicht benachbarte Dreieckspaar-Kreuzungen | 326 | 9 |

Keine nicht endlichen UV-/Bildwerte. UV-Überlappungen wurden durch Rasterisierung der Dreiecksinnenflächen bei Pixelzentren gemessen, nicht durch Betrachten leerer Atlasbereiche. Kopf etwa 11,98 %, Oberkörper etwa 25,78 % Atlasbelegung; weiterhin ineffizient. Die summierte Dreiecks-UV-Fläche ist aufgrund von Überlappungen nicht exakt identisch mit der Rasterbelegung. Ein manuelles Unwrap ist erforderlich. Die Alpha-Statistik des gesamten Bildes allein wäre keine Fehlerquote.

Selbstüberschneidungen: BVH plus Segment-Dreieck-Test, Ausschluss benachbarter Dreiecke und Endpunktkontakte, Ausgangspose. Dreieckspaare sind keine Anzahl eigenständiger sichtbarer Defekte. Die reduzierte Geometrie besitzt unerwünschte Kreuzungen an Strähnen/Übergängen. Auch die Quelle hat bekannte Kreuzungen; wegen veränderter Triangulierung sind Paarzahlen nicht unmittelbar als Anzahl neu hinzugekommener Defekte vergleichbar. Kein mathematisch vollständiger Nachweis gegen alle Toleranz-/Berührungsfälle, keine Deformationsprüfung.

### Gemessene Oberflächenabweichung

Je Bereich 8.000 flächengewichtet zufällige baryzentrische Quellpunkte mit Seed 42, Abstand zur Vergleichsoberfläche. Zusätzlich bis zu 8.000 Vergleichs-Dreiecksschwerpunkte zur Quelle. Dies ist eine Stichprobe, kein garantierter Hausdorff-Maximalfehler und kein Ersatz für Silhouettenprüfung.

| Quelle → Vergleich | Mittel | 95. Perzentil | Maximal in Stichprobe |
| --- | ---: | ---: | ---: |
| Kopf/Haare | 0,356 mm | 0,936 mm | 2,087 mm |
| Oberkörper | 0,115 mm | 0,289 mm | 0,593 mm |

Umgekehrt Kopf 0,367 mm Mittel / 1,858 mm Stichprobenmaximum, Oberkörper 0,119 mm / 0,708 mm. Kleine metrische Fehler verdecken die Bedeutung sehr dünner Locken und Lider: Millimeter können dort die gesamte Form ausmachen.

Quellhöhe unverändert 1,399999857 m. Vergleichs-Haarmaximum 1,399672270 m, rund 0,328 mm niedriger durch Vereinfachung; kein Skalierungseingriff. Fußsohlen und Maßstab des ungetesteten unteren Kontexts unverändert. Kein Versuch, einen späteren 1,32-m-Master festzulegen.

## Visuelle A/B-Bewertung

14 Vergleichswinkel/Modi, jeweils A/B unter identischer Kamera, Studiolicht, Projektion und Bildgröße: Gesicht vorne/Dreiviertel/Profil, Haare vorne/seitlich/hinten, Oberkörper, Kopf- und Oberkörper-Clay, Kopf- und Oberkörper-Wireframe, vergrößerter Augen-/Mund-Wireframe, Westen-Detail und erhöhte 2,5D-Ansicht. 28 echte Cycles-Renderings, 1000 × 1000, zwölf Samples/Denoising, CPU; daraus 14 unveränderte A/B-Pixeltafeln. Die ursprüngliche zu enge Profilrahmung wurde für beide Versionen korrigiert, Nase und Kopftiefe bleiben im finalen Vergleich sichtbar. Keine generierten Konzeptbilder. Kamera-/Lichtwerte pro Ansicht stehen in `RenderSettings.json`.

- **Gesicht:** Farbe und Ausdruck im Texturbild weitgehend wiedererkennbar, aber Lid- und Lippengeometrie im Clay abgeschwächt. Kleine sichtbare Risse an Nase/Kinn sowie der unabhängigen Test-Schnittgrenze. Gemalte Augen dürfen die verlorene Deformationstopologie nicht kaschieren.
- **Haare:** Hauptsilhouette bleibt ähnlich, Lockenquerschnitte und Spitzen werden deutlich kantiger. Schmale Strähnen und Zwischenräume verändern sich, zusätzliche Kreuzungen. Normalmap kann äußere Konturen nicht reparieren.
- **Kleidung:** Westenfarbe, Knöpfe, Gürtel-/Riemendetails und viele Stofffalten gut übertragbar. Vergrößerte Aufnahme zeigt kleine schwarze Naht-/Baking-Stellen, unter anderem am Riemen, sowie Material-/Normalenunruhe. Quelle und Körper/Kleidung wurden nicht sauber modular getrennt.
- **Wireframe:** komplett dreieckig und ungerichtet; keine verlässlichen Augen-/Mundringe und keine Schulterdeformationsloops. Das Verfahren ist nicht für zuverlässige neue Skin Weights freigegeben.
- **2,5D:** Unterschiede fallen im größeren Gesamtbild weniger auf; dies reicht nicht, um Nahaufnahme-, Topologie- und Rigging-Probleme zu akzeptieren. Ansicht ist eine Blender-Nahprüfung bei ungefähr 50° Neigung, kein Unreal-/PIE-Screenshot. Projektkamera unverändert.

Nicht geprüft: zeitliches Flimmern in Unreal, Animationsverformungen, Root Motion, GPU-/Draw-Call-/NPC-Performance und LOD-Umschaltungen. Keine Behauptung eines animations- oder enginefertigen Ergebnisses.

## Antworten auf die fünf Entscheidungsfragen

1. **Ist das Verfahren für die gesamte Figur geeignet?** Nein als automatische Endlösung. Die Materialübertragung ist brauchbar, die getestete Topologie nicht.
2. **Welche Qualität geht verloren?** Lockenrundung/Spitzen, feine Gesichtsvolumina und saubere Anschlüsse; Restfehler und neue Überschneidungen. Die 2K-Quelle begrenzt die erreichbare Texturauflösung; zwei zusätzliche Atlanten erzeugen keine neuen Originaldetails.
3. **Was braucht manuelle Retopologie?** Gesicht mit Lid-/Augen-/Mund-/Nasenloops, Hals/Kieferanschluss, Schultern/Achseln/Ärmeln und gezielte Lockenbündel. Kleidungsschnitt-/UV-Grenzen müssen bewusst gewählt werden. Ein automatischer Solver kann später auf kontrolliert manifold vorbereiteten einfachen Flächen erneut getestet werden, nicht blind auf dem gesamten importierten Mesh.
4. **Bleibt Highpoly eine zuverlässige Baking-Quelle?** Ja als erhaltene künstlerische Quelle mit bekannten lokalen Defekten; der korrigierte Test bestätigt Textur-/PBR-Übertragung. Für kritische Locken-/Kontaktbereiche sind getrennte Source-Gruppen und handgeprüfte Cages nötig. Kein pauschales Zertifikat der Fehlerfreiheit.
5. **Soll jetzt die ganze Game-Ready-Version so erstellt werden?** Nein. Erst gezielter manueller Kopf-/Schulter-Retopotest, saubere UVs, kontrollierte Cages und erneute Nahvergleiche. Das vollständige 30.000–50.000-LOD0-Ziel bleibt vorläufig; nicht durch ungeprüfte weitere Decimation erzwingen.

Empfohlener nächster freizugebender Schritt: einen kleinen sauberen, quad-orientierten Gesicht-/Hals-/Schulterkäfig erstellen, auf die unveränderte Highpoly-Referenz projizieren, separate Lockenbündel mit kontrollierten Querschnitten planen und UVs mit klaren Chartgrenzen anlegen. Original-Highpoly als Bake-/Silhouettenquelle behalten. Erst nach Deformationstests und späterer Unreal-Performanceprüfung über die gesamte Figur und LODs entscheiden. Dieser Schritt wurde **nicht** begonnen.

## Wiederöffnungsprüfung und Bedienung der Testdatei

Die gespeicherte Testdatei wurde in einem unabhängigen Blender-Prozess erneut geöffnet. Quell-Positions-/Index-/UV-/Normalenhashes stimmen, Originalmaterialgraph und Originaltexturbilddaten stimmen, alle zehn neuen Bakes gepackt und extern auffindbar. Kein Rig und keine Animationsdaten hinzugefügt. `GameReady_approved = false` ist in Szene und Vergleichsobjekten hinterlegt.

Default zeigt A, die komplette Highpoly-Referenz. Für B im Outliner Highpoly-Referenz ausblenden und `GRT_HeadHair`, `GRT_Torso`, `GRT_UnmodifiedContext` einschalten, jeweils Auge für Viewport und Kamera für Render. Die beiden Vergleichsobjekte sind als nicht freigegeben gekennzeichnet, nicht gegen Bearbeitung gesperrt. Neu gespeicherter Renderpfad zeigt ausschließlich auf den neuen Reviewordner.

Keine Unreal-Dateien betroffen; deshalb kein Unreal-Build, kein Gameplay-/Automationstest oder Unreal-Import in diesem begrenzten Blender-Auftrag. Dateischutz-, Geometrie-, UV-, Bake- und Renderprüfungen sind die tatsächlich ausgeführten Tests.

## Vergleichsbilder

In jeder Tafel: links A (Highpoly), rechts B (nicht freigegebene Dreieckskontrolle mit übertragenen Materialien; in Gesamtansicht ungetesteter Rest weiterhin Highpoly).

- [01_FaceFront_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/01_FaceFront_A_vs_B.png)
- [02_FaceThreeQuarter_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/02_FaceThreeQuarter_A_vs_B.png)
- [03_FaceProfile_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/03_FaceProfile_A_vs_B.png)
- [04_HairFront_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/04_HairFront_A_vs_B.png)
- [05_HairSide_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/05_HairSide_A_vs_B.png)
- [06_HairBack_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/06_HairBack_A_vs_B.png)
- [07_Torso_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/07_Torso_A_vs_B.png)
- [08_HeadClay_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/08_HeadClay_A_vs_B.png)
- [09_HeadWire_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/09_HeadWire_A_vs_B.png)
- [10_TorsoClay_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/10_TorsoClay_A_vs_B.png)
- [11_TorsoWire_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/11_TorsoWire_A_vs_B.png)
- [12_2_5D_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/12_2_5D_A_vs_B.png)
- [13_EyeMouthWire_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/13_EyeMouthWire_A_vs_B.png)
- [14_VestDetail_A_vs_B.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/14_VestDetail_A_vs_B.png)

## Texturdateien

- [GRT_HeadHair_AO.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_AO.png)
- [GRT_HeadHair_BaseColor.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_BaseColor.png)
- [GRT_HeadHair_Metallic.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_Metallic.png)
- [GRT_HeadHair_Normal.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_Normal.png)
- [GRT_HeadHair_Roughness.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_Roughness.png)
- [GRT_Torso_AO.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_AO.png)
- [GRT_Torso_BaseColor.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_BaseColor.png)
- [GRT_Torso_Metallic.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_Metallic.png)
- [GRT_Torso_Normal.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_Normal.png)
- [GRT_Torso_Roughness.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_Roughness.png)

## Git und vollständige neue Dateiliste

`git diff --check`: Exit 0, keine Ausgabe. Keine bestehenden Dateien gelöscht, zurückgesetzt oder überschrieben. Nichts gestaged; kein Commit, kein Push. Neue Dateien ausschließlich im HobbitBase-Arbeitsbereich. Bereits vorhandener Git-Status bleibt bestehen:

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

- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/PRUEFBERICHT.md`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Audit.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/AuditFinal.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Bake.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/BakeDiagnosis.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/BakeDiagnosis.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/BakeDiagnosisRetry.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/BakeFixedUV.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/BakeRetry.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/BakeTrial.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/ComparisonPages.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Compose.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FinalFile.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Finalize.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FinalizeSafePath.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/01_FaceFront_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/01_FaceFront_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/07_Torso_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/07_Torso_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/08_HeadClay_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/08_HeadClay_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/BakeDiagnosis.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/BakeTrial.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_HeadHair_AO.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_HeadHair_BaseColor.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_HeadHair_Metallic.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_HeadHair_Normal.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_HeadHair_Roughness.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_Torso_AO.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_Torso_BaseColor.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_Torso_Metallic.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_Torso_Normal.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/GRT_Torso_Roughness.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FirstBakeFailure/TechnicalAudit.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FixUV.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/FixedUV.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/01_FaceFront_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/01_FaceFront_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/01_FaceFront_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/02_FaceThreeQuarter_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/02_FaceThreeQuarter_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/02_FaceThreeQuarter_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/03_FaceProfile_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/03_FaceProfile_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/03_FaceProfile_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/04_HairFront_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/04_HairFront_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/04_HairFront_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/05_HairSide_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/05_HairSide_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/05_HairSide_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/06_HairBack_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/06_HairBack_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/06_HairBack_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/07_Torso_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/07_Torso_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/07_Torso_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/08_HeadClay_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/08_HeadClay_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/08_HeadClay_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/09_HeadWire_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/09_HeadWire_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/09_HeadWire_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/10_TorsoClay_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/10_TorsoClay_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/10_TorsoClay_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/11_TorsoWire_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/11_TorsoWire_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/11_TorsoWire_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/12_2_5D_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/12_2_5D_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/12_2_5D_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/13_EyeMouthWire_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/13_EyeMouthWire_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/13_EyeMouthWire_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/14_VestDetail_A_HP.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/14_VestDetail_A_vs_B.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Previews/14_VestDetail_B_TriangleControl.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/ProtectedBefore.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/ProtectionAfter.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/RegionAnalysis.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Region_HeadHair.npz`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Region_Torso.npz`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/RenderClayDiagnostic.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/RenderFinal.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/RenderFirst.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/RenderProfileFit.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/RenderSettings.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Reopen.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/ReopenFinal.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/Retopo.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/RetopoTrial.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/SourceVertexCounts.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/SourceVertexCounts.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/TechnicalAudit.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/UVAndIntersectionAudit.json`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/GameReady_Test_V1/UVIntersection.log`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_GameReady_Test_V1.blend`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_GameReady_Test_V1.blend1`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_AO.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_BaseColor.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_Metallic.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_Normal.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_HeadHair_Roughness.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_AO.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_BaseColor.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_Metallic.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_Normal.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Textures/GameReady_Test_V1/GRT_Torso_Roughness.png`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/AuditTrial.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/BakeTrial.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/ComposeComparisons.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/CountSourceVertices.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/DiagnoseBake.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/FinalizeTestFile.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/FixBakeUV.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/PrepareRegions.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/RenderComparisons.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/ReopenFinal.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/RetopoTrial.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/UVAndIntersectionAudit.py`
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/GameReady_Test_V1/WriteReport.py`
