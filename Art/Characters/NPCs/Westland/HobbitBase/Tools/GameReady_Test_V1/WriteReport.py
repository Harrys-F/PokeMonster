from pathlib import Path
import json,subprocess
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');B=R/'Art/Characters/NPCs/Westland/HobbitBase';P=B/'Review/GameReady_Test_V1';A=json.loads((P/'TechnicalAudit.json').read_text());Q=json.loads((P/'RetopoTrial.json').read_text());U=json.loads((P/'UVAndIntersectionAudit.json').read_text());Z=json.loads((P/'ProtectionAfter.json').read_text());F=json.loads((P/'FinalFile.json').read_text());C=json.loads((P/'ComparisonPages.json').read_text());V=json.loads((P/'FixedUV.json').read_text());S=json.loads((P/'RegionAnalysis.json').read_text())
raw=json.loads((P/'SourceVertexCounts.json').read_text())
source_sum=sum(S[x]['source_faces'] for x in ['HeadHair','Torso']);low_sum=A['candidate_total_triangles'];reduction=100*(1-low_sum/source_sum)
t=f'''# Westland Hobbit NPC – Game-Ready Retopologie-Test V1

Prüfdatum: 14.10.2026. Ausgangs-HEAD: `{Z['head']}`. Blender 5.2.2 LTS, vorhandene MCP-Verbindung und getrennte native Blender-Python-Prozesse. Keine externen Modelle, Dienste, neuen Add-ons oder Retopologieprogramme.

## Klare Entscheidung

**Keine Freigabe für eine vollständige Game-Ready-Version mit dem getesteten automatischen Verfahren.** Der begrenzte Test und die Materialübertragung sind abgeschlossen; das Erfolgskriterium einer animationsgeeigneten Zieltopologie ist **nicht erreicht**.

Die automatische QuadriFlow-Retopologie wurde für Kopf/Haare und Oberkörper wegen nicht-manifolder Eingaben abgebrochen. Die verbleibenden Dreiecksmeshes sind ausschließlich **nicht freigegebene Reduktions-/Baking-Vergleichsobjekte**, keine endgültige Retopologie. An dieser Stelle wurde die automatische geometrische Bearbeitung gestoppt. Keine vollständige Figur automatisch reduziert.

Der Baking-Test zeigt nach Korrektur eines UV-Packfehlers, dass Base Color und PBR-/Normalendetails grundsätzlich übertragen werden können. In Nahansicht gehen Lockenrundung sowie Lid-/Mundvolumen verloren; Schnittnahtfehler, Überschneidungen und UV-Überlappungen bleiben. In der erhöhten Ansicht wirken die Unterschiede kleiner, das ersetzt keine Topologie- und Deformationsprüfung.

## Dateien und Schutz

- Unveränderte Quelle: `{B/'Source/Hobbit_NPC_4K_Base_V1.blend'}`.
- Neue eigenständige Testdatei: `{B/'Source/Hobbit_NPC_GameReady_Test_V1.blend'}`.
- Neue Bakes: `{B/'Textures/GameReady_Test_V1'}`.
- Neue Skripte: `{B/'Tools/GameReady_Test_V1'}`.
- Bericht und Nachweise: `{P}`.

Die komplette Highpoly-Referenz liegt unabhängig in der Testdatei; Geometrie, UVs, Custom Normals, ursprüngliche Texturbilddaten und Materialgraph wurden gegen die Quelle geprüft und erhalten. Original-GLB, V1–V4, MeshyBase V1/V2, Spieler, 25-Bone-Rig, Animationen und Unreal-Dateien blieben unverändert. **{Z['checked']} zuvor vorhandene Dateien per SHA-256 geprüft: keine verändert, keine fehlt.** Bereits offene Sprint-/Player-Änderungen wurden nicht zurückgesetzt.

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
| Beide Testbereiche | {source_sum:,} | 1.058.271 | 41.668 | {low_sum:,} | 0 |

Reduktion der ausgewählten Quelldreiecke: **{reduction:.2f} %**. Diese Zahl beweist keine Rigging-Eignung.

Die vollständige Quelle hat 1.466.192 Vertices / 2.652.461 Dreiecke. In der Testdatei liegen vier Charakter-Mesh-Objekte: komplette Highpoly-Referenz, zwei Vergleichsbereiche und unoptimierter Rest. A rendert einen vollständigen Highpoly-Charakter; B rendert drei Meshes mit insgesamt **620.980 Dreiecken**, davon 537.172 unverändertem Kontext. **B ist kein 30.000–50.000-Dreiecke-Gesamtmodell.** Das spätere LOD0-Ziel wurde nicht durch weitere aggressive Reduktion erzwungen.

Materialien: Originalreferenz ein Material, jeder Vergleichsbereich ein eigenes neues Material, unoptimierter Kontext verwendet Originalmaterial. B zeigt damit drei Materialzuweisungen über drei Meshes. Zwei neue PBR-Materialien, jeweils fünf 2K-Bilder; drei ursprüngliche 2K-Bilder bleiben Referenz. Keine Unreal-Material-/Draw-Call-Messung.

Tatsächlich referenzierte originale Vertex-IDs in den Ausschnitten (vor jeder Positionsgleichsetzung): Kopf/Haare **{raw['HeadHair']['source_vertex_ids']:,}**, Oberkörper **{raw['Torso']['source_vertex_ids']:,}**. Überlappende Randvertices werden zwischen den Ausschnitten separat gezählt; ihre Summe ist keine Vertexzahl der gesamten Figur.

## Baking-Test und UV-Korrektur

### Erster Versuch – ausdrücklich verworfen

Smart Project mit Winkel 0,9 rad und `SCALED` Island Margin 0,008 erzeugte sehr viele kleine Charts. Gemessene summierte UV-Fläche: Kopf 0,00068556 (0,069 %), Oberkörper 0,0112558 (1,126 %). Die großzügigen skalierten Abstände ließen die tatsächlichen Inseln extrem schrumpfen. Die Bakes sahen wie einzelne Farbpunkte aus und erzeugten schwarze Dreiecke sowie verlorene Augen-/Mundinformationen. Dies war ein Fehler des Test-UV-Packings, **kein Beweis gegen die Originaltexturen**.

Alle ersten Bakes und ausgewählte erste Renderings sind unter `FirstBakeFailure/` erhalten. Die erste RNA-Abfrage des Cycles-Gerätetyps und eine spätere Diagnoseabfrage verwendeten in Blender 5.2 nicht vorhandene Typ-/Feldnamen; sie wurden im neuen Skript korrigiert. Beide Fehler betrafen nur neue Arbeitsprozesse, nicht die Quelle. Logs bleiben erhalten.

### Korrigierter Versuch – verwendetes Vergleichsmaterial

Nur UVs und Baking-Konfiguration der Testkontrollen angepasst, keine weitere Geometriebearbeitung:

- Smart Project: Winkel 1,15 rad, Area Weight 0,4, Scale To Bounds.
- Margin Method `FRACTION`, 4/2048 = 0,001953125 UV-Abstand.
- Gemessene summierte UV-Fläche: Kopf {V['HeadHair']['uv_area_sum']:.6f}, Oberkörper {V['Torso']['uv_area_sum']:.6f}.
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
| UV-Innenflächen-Pixelüberlappungen bei 2K | {U['HeadHair']['uv_interior_overlapping_texels']:,} | {U['Torso']['uv_interior_overlapping_texels']:,} |
| UV-belegte Atlaspixel | {U['HeadHair']['uv_occupied_texels']:,} | {U['Torso']['uv_occupied_texels']:,} |
| Leere Base-Color-Alpha-Texel innerhalb UV | {U['HeadHair']['base_color_empty_alpha_inside_uv']} | {U['Torso']['base_color_empty_alpha_inside_uv']} |
| Schwarze Texel innerhalb UV | {U['HeadHair']['base_color_black_inside_uv']} | {U['Torso']['base_color_black_inside_uv']} |
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

'''
for c in C:t+=f"- [{Path(c['path']).name}]({c['path']})\n"
t+='\n## Texturdateien\n\n'
for f in sorted((B/'Textures/GameReady_Test_V1').glob('*.png')):t+=f'- [{f.name}]({f})\n'
t+='\n## Git und vollständige neue Dateiliste\n\n`git diff --check`: Exit 0, keine Ausgabe. Keine bestehenden Dateien gelöscht, zurückgesetzt oder überschrieben. Nichts gestaged; kein Commit, kein Push. Neue Dateien ausschließlich im HobbitBase-Arbeitsbereich. Bereits vorhandener Git-Status bleibt bestehen:\n\n```text\n'+Z['git_status']+'```\n\n'
report=P/'PRUEFBERICHT.md';roots=[P,B/'Tools/GameReady_Test_V1',B/'Textures/GameReady_Test_V1'];files=[f for r in roots for f in r.rglob('*') if f.is_file()]+list((B/'Source').glob('Hobbit_NPC_GameReady_Test_V1.blend*'));t+=f'- `{report}`\n'
for f in sorted(files):
 if f!=report:t+=f'- `{f}`\n'
for n in [source_sum,low_sum,raw['HeadHair']['source_vertex_ids'],raw['Torso']['source_vertex_ids']]+[U[x][k] for x in ['HeadHair','Torso'] for k in ['uv_interior_overlapping_texels','uv_occupied_texels']]:
 t=t.replace(f'{n:,}',f'{n:,}'.replace(',','.'))
report.write_text(t);assert all(line==line.rstrip() for line in t.splitlines());print('REPORT_SAVED',len(t))
