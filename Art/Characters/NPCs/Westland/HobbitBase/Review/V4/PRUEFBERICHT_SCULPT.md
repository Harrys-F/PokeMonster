# Westland Hobbit NPC V4 – Kopf-Sculpt-Prüfbericht

14.10.2026 · Ausgangs-HEAD `3c6dc47` · Blender 5.2.2 LTS.

## Ergebnis und bewusster Stopp

**Eine separate, bearbeitbare Sculpt-Sitzung und ein begrenzter reversibler Kopf-Formpass wurden erstellt. Die geforderte hochwertige, erwachsene Gesichtsqualität ist noch nicht erreicht.** Die sichtbare Verbesserung ist klein; insbesondere Augenpartie, Nase und Ohr-Anatomie überzeugen noch nicht. Keine künstlerische Freigabe und kein produktionsreifes Mesh.

Gemäß der ausdrücklich vorgesehenen Grenze der Automation wurde die automatische Formarbeit nach der Sichtprüfung gestoppt. Keine weitere Polygonverdichtung als Ersatz für Qualität. Die Arbeitsdatei ist für gezielte manuelle Bearbeitung vorbereitet; konkrete Werkzeuge und Startwerte stehen in der [manuellen Anleitung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/MANUELLER_SCULPT_WORKFLOW.md). Diese Anleitung ist außerdem als Textblock im Master gespeichert.

Master: [Hobbit_NPC_V4_HeadSculpt.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/SculptV4/Hobbit_NPC_V4_HeadSculpt.blend).

## Tatsächliche Ausgangsdatei und Referenzen

Ausgangspunkt war die gespeicherte [V3-Körperquelle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Source/Hobbit_NPC_Base_V3_Body.blend), nicht eine neue vollständige Körpergenerierung. Die Datei wurde in eine eigene V4-Szene angehängt. Eigenständige Meshdaten und eine unangetastete, standardmäßig verborgene V3-Vergleichskopie befinden sich in der V4. Bestehende offene Blender-Szenen wurden nicht durch `open_mainfile` ersetzt.

AGENTS.md und die relevanten Projektunterlagen wurden gelesen. Zunächst waren nur jugendliche Trainerreferenzen unter `Art/Characters/YoungTrainer/Reference/` und technische V1–V3-Vorschauen verfügbar. Eine passende erwachsene Westland-Hobbit-Gesichtsvorlage wurde angefragt.

Harry hat daraufhin tatsächlich [1-Foto-1.jpg](/tmp/codex-remote-attachments/01a0ac33-17a2-7000-a83d-bf800bb4af2e/60BAE6A8-D0BA-42CF-8136-7BD58A60B4F6/1-Foto-1.jpg) nachgereicht. Eine unveränderte Kopie liegt als [AdultHobbit_ArtTarget.jpg](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/ReferenceViews/AdultHobbit_ArtTarget.jpg) vor und ist in Blender gepackt. Das linke erwachsene Porträt ist die künstlerische Zielvorlage. Die rechte Körperabbildung löst in diesem Kopfauftrag keine Körperänderung aus. Die Referenz kam **nach** dem begrenzten Formpass und wurde anschließend für dessen kritische Bewertung sowie die manuelle Arbeitsanleitung verwendet. Keine Behauptung, die vorhandenen Formen bereits genau nach dieser Vorlage modelliert zu haben.

Keine zusätzliche erwachsene orthografische Front-/Profil-/Dreiviertelserie oder gesondertes Westland-Hobbit-Sheet gefunden. Das nachgereichte Bild ist eine leicht perspektivische Stilvorlage, kein maßhaltiger Turnaround. Keine fremden 3D-Modelle und kein Meshy verwendet.

Referenz-Collection: `HNV4_REFERENCE_IMAGES_TECHNICAL_V3`. Vier V3-Image-Empties decken Front-Kopf, rechtes Kopfprofil, linkes Ganzkörperprofil und Dreiviertel-Kopf ab. Transparenz 35 %, Transformationssperren, nicht auswählbar, standardmäßig verborgen und nicht renderbar. Ein fünftes Image Empty enthält Harrys neue Zielvorlage mit 45 % Transparenz. Die V3-Bilder sind technische Ausgangsvergleiche, keine gewünschte Gesichtsqualität.

## Arbeitsplatz und ausgeführte Operationen

- Eigene Sicherung `Source/SculptV4/Hobbit_NPC_V4_00_V3Copy.blend` vor V4-Geometrieänderungen; V3 bleibt zusätzlich unverändert verfügbar.
- Eine lokale BMesh-Kantenunterteilung mit einem Schnitt, Grid Fill und **Smooth 0** ausschließlich oberhalb Z=1,067 m und innerhalb des Kopfbereichs. Keine globale Subdivision, kein Remesh und keine neue Körpergenerierung.
- Reversibler Shape Key `V4_LimitedHeadFormPass` auf `Basis_V3_LocalDensity`. Wert 1 zeigt die Korrektur; Wert 0 zeigt die unveränderten Formen auf dem lokal verdichteten Netz. Original-V3-Geometrie bleibt in der separaten Vergleichskopie.
- Lokale proportionale Vertexkorrekturen an Wangen, Kinn, Mundwinkeln, oberem Lippenprofil, Nasenflügelregion, orbitalem Übergang und Ohrkontur. Kompakte räumliche Einflussbereiche, bilateral gleich angewandt.
- **4.811 Kopfvertices** versetzt, maximale Verschiebung **3,626 mm**. Wangen/Kinn leicht aufgebaut; erhöhte Mundwinkel reduziert; Lippenprojektion leicht zurückgenommen; Alarregion etwas aufgebaut und nach unten versetzt; Ohrkonturen minimal verändert.
- `.sculpt_mask` schützt sämtliche übrigen Körperregionen. Ein 10-mm-Halsübergang ist abgestuft maskiert. X-Symmetrie an, Y/Z aus. Aktiver Shape Key für weitere Bearbeitung ausgewählt.
- Sculpt Mode, orthografische Kopf-Vorderansicht und eigener Arbeitsplatz. Native mitgelieferte Blender-Brushes vorbereitet: Grab, Clay Strips, Draw Sharp, Smooth, Inflate/Deflate, Crease Polish und Mask. Grab aktiv, Radius 65 px, Strength 0,20, Front Faces Only.
- Vier benannte orthografische Kopf-Review-Kameras, vorhandene neutrale V3-Studiobeleuchtung und Haut-/Augenmaterialien erhalten.

**Wichtige Unterscheidung:** Die tatsächlich ausgeführte Formkorrektur besteht aus Blender-Python-/BMesh-/Shape-Key-Operationen. **Keine interaktiven oder simulierten Sculpt-Brush-Strokes wurden ausgeführt.** Die Pinsel sind für die manuelle Fortsetzung eingerichtet. Es wurden keine neuen Gesichtselemente als Primitive angeklebt und keine Materialien zur Kaschierung fehlender Form verändert.

## Vorher–Nachher und künstlerische Grenzen

Alle neun Vergleichsaufnahmen wurden aus der gespeicherten V4-Datei mit Cycles CPU, vier Threads, 32 Samples und Denoising erzeugt. Einzelne V3/V4-Paare haben identische Kameras, Maßstab, Auflösung, Materialien und Studiolichter. Im gemeinsamen Bild steht V3 links und V4 rechts; beide haben denselben Maßstab und Kamerawinkel. Durch die seitlichen Positionen im selben Studio kann der Lichteinfall geringfügig abweichen; die Einzelpaare sind der genauere Formvergleich.

Kleine nachvollziehbare Änderungen: ruhigere Mundlinie, etwas mehr untere Wangen-/Kinnmasse und geringfügig verändertes Lippenprofil. **Kein überzeugender Sprung zu einem erwachsenen hochwertigen Fantasygesicht.** Die zusätzliche Geometrie verbessert die Bearbeitbarkeit, beweist aber keine Art-Verbesserung. Stirn und orbitale Übergänge zeigen weiterhin unnatürliche Formstufen; teils werden diese durch die veränderte lokale Tessellierung deutlicher sichtbar.

Gegenüber Harrys neuer Zielvorlage bestehen große Abweichungen:

- Kopf-/Gesichtsebenen bleiben zu breit, glatt und schematisch; Jochbein, erwachsene Kieferform und Wangenmasse sind nicht überzeugend gestaltet.
- Kleine, starr wirkende Augenöffnungen mit gleichförmigen Lidwülsten; freundlich-neutraler Blick nicht sicher erreicht. Ein nur technisch eingebetteter Augapfel reicht nicht.
- Nasenrücken und Spitze noch vereinfacht. Die zwei frontal sichtbaren Öffnungen haben weiterhin eckige Umfeldflächen; der Pass behebt dies nicht vollständig.
- Lippen und Mundwinkel noch zu gleichförmig, im Profil teilweise schnabelförmig. Kinn-/Unterlippenübergang benötigt größere bewusste Formarbeit.
- Ohrmuscheln bleiben einfache ovale Vertiefungen; Helix, Antihelix, Tragus und Lobulus brauchen manuelle anatomische Ausarbeitung.

**Einschätzung der Methode:** Vorteil gegenüber V3 ist die geschützte, reversible und lokal besser bearbeitbare Sculpt-Basis. Der künstlerische Vorteil dieses ersten automatisierten Passes ist gering und reicht nicht für Freigabe. Die neu eingetroffene Referenz verbessert die Zielklarheit, ersetzt jedoch keine kontrollierte organische Modellierung.

## Technische Prüfung aus erneut geöffneter Datei

[Rohprüfung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/ReopenAudit.json):

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Blender speichern / separat öffnen | Erfolgreich, Blender 5.2.2 LTS |
| Einheit | METRIC, Unit Scale 1,0 |
| Körperhöhe ohne Haare | 1,281999946 m = 128,20 cm |
| Sohlenminimum | Z=0 |
| Reserve bis 1,32 m einschließlich späterer Haare | 3,80 cm; Haare existieren nicht |
| Maximaler bilateraler Vertexabstand | 0,000000137 m; innerhalb 1-µm-Toleranz |
| Ursprüngliche geschützte Körpervertices | 6.295, Positionsabweichung 0 m |
| Geschützte Regionen | Maskenwert 1,0 |
| Beide Augäpfel | Vertexzahlen, Vertexpositionen und Transformationen unverändert |
| Körperkomponenten | 1 zusammenhängende Haut |
| Offene / Non-Manifold-Kanten | 0 / 0 |
| Lose / degenerierte Geometrie | 0 / 0 |
| Doppelte Vertexpaare innerhalb 0,1 µm | 0 |
| Normalen / gemeinsame Kantenorientierung | Keine erkannten Fehler |
| Erkannte eigentliche nicht benachbarte Dreieckkreuzungen | 0 |
| Anatomische Schnittkontrollen | 1 Kopf, 2 Beine, je 1 Arm, je 4 Finger + Daumen, insgesamt 10 Zehen |
| Rig / Actions / Deformationstest | Keine / keine / nicht durchgeführt |

Der Kreuzungstest schließt gemeinsame Vertexpaare, koplanare Überlappungen und tangentiale Kontakte aus; er ist kein vollständiger mathematischer Beweis. Augapfel-/Haut-Einbettung ist beabsichtigt. Sichtprüfung: Front, Profil, Dreiviertel und Ganzkörper sind konsistent; keine neuen offensichtlich fehlenden oder zusätzlichen Gliedmaßen. Keine Animationsprüfung.

### Tatsächliche Geometriezahlen

Ohne Studio, Referenzbilder oder verborgene Vergleichskopie:

| Mesh | Vertices | Flächen | Dreiecke |
| --- | ---: | ---: | ---: |
| V4 Körper einschließlich lokal verdichtetem Kopf | 23.012 | 23.688 | 46.020 |
| Augapfel links | 1.298 | 1.344 | 2.592 |
| Augapfel rechts | 1.298 | 1.344 | 2.592 |
| Gesamt | 25.608 | 26.376 | 51.204 |

Körper: 22.140 Quads, 1.452 Dreiecke, **96 N-Gons an der lokalen Auflösungsgrenze**. Diese Übergänge sind ein dokumentiertes Sculpt-Zwischenstadium. Trotz geschlossener Geometrie **keine finale Manifold-/Runtime-/Animationsfreigabe**: Gesichtsschleifen, Pole und Auflösungsübergang benötigen später gezielte Retopologie. Der Restkörper wurde nicht verdichtet; neue Vertices liegen nur im Kopf bzw. dessen Auflösungsgrenze.

## Erforderliche manuelle Schritte

Die [vollständige Anleitung mit konkreten Brush-Einstellungen](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/MANUELLER_SCULPT_WORKFLOW.md) benennt Arbeitsreihenfolge und Abbruchkriterien:

1. Größere Stirn-/Schläfen-/Wangen-/Kieferebenen anhand der erwachsenen Porträtvorlage ausformen, bevor Details hinzukommen.
2. Lidformen und Augenwinkel um die vorhandenen Augäpfel neu balancieren.
3. Nasenspitze und Alarvolumen zusammenhängend modellieren; die Öffnungsränder lokal bearbeiten und nach unten ausrichten.
4. Lippenvolumen, neutrale Mundwinkel und Kinn-/Unterlippenübergang korrigieren.
5. Ohrkonturen und innere Falten anatomisch aufbauen.
6. Nach jedem Bereich Front, beide Profile und Dreiviertel unter gleichem Licht prüfen. Keine Haare, Kleidung, Körperarbeit, Retopologie oder Rigging anschließen.

## Neun echte Blender-Renderings

1. [V3 Kopf vorne](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_01_V3_Head_Front.png)
2. [V4 Kopf vorne](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_02_V4_Head_Front.png)
3. [V3 Kopf Profil](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_03_V3_Head_Profile.png)
4. [V4 Kopf Profil](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_04_V4_Head_Profile.png)
5. [V3 Kopf Dreiviertel](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_05_V3_Head_ThreeQuarter.png)
6. [V4 Kopf Dreiviertel](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_06_V4_Head_ThreeQuarter.png)
7. [Direktvergleich, V3 links / V4 rechts](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_07_Compare_V3_V4.png)
8. [V4 Gesamtfigur vorne](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_08_V4_Body_Front.png)
9. [V4 schräg erhöhte 2,5D-Nahansicht](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Previews/Hobbit_V4_09_V4_Body_Camera25D.png)

Alle PNG-Dateien auf Existenz, Abmessungen und Chunk-CRC geprüft. Keine generierten Konzeptbilder als Modellrender ausgegeben. Beim ersten Renderlauf wurde ein Fehler im ausschließlich temporären Render-Skript gefunden: Augenpositionen wurden beim Umschalten zwischen Versionen auf X=0 gesetzt. Das Skript wurde korrigiert und **alle neun Bilder neu erzeugt**. Die gespeicherten Augen und Geometrie waren davon nicht betroffen.

## Erhaltung und Dateien

Die [SHA256-Erhaltungsprüfung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/Preservation.json) erfasst **1.596 vor Beginn vorhandene Dateien**: keine verändert, keine fehlend. Darunter V1–V3 und die bereits offenen Player-/Sprint-Arbeiten. Neue V4-Dateien ausschließlich unter HobbitBase: `Source/SculptV4/`, `Review/V4/`, `Tools/V4/`. Automatische `.blend1`-Backups bleiben erhalten; keine fremden Dateien gelöscht.

Keine Änderungen an Unreal, Maps, Player, Sprint, Gameplay oder Haupt-Projektdokumentation. Keine Unreal-Builds oder Automationstests für diesen reinen Blender-Auftrag ausgeführt. Blender-Mesh-, Erhaltungs-, Reopen- und Renderprüfungen wurden tatsächlich durchgeführt. `git diff --check` ohne Ausgabe; zusätzlicher Whitespace-Check der neuen Markdown-Dateien erfolgreich. [Finaler Git-Status](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/GitStatus_Final.txt), [neue V4-Dateien](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/V4/NewFiles.json).

Kein Commit, kein Push. Stopp nach Kopfversuch, manueller Sculpt-Vorbereitung und Vergleichsbildern. Keine automatische Freigabe für weitere Entwicklungsphasen.
