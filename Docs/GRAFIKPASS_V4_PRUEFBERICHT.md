# Grafikpass V4 – Heilhaus, Heilerin und Landschaft

Stand: 20.10.2026. Aktives Projekt: `/Users/harry/Developer/PokeMonster/PokeMonster.uproject`. Zielkarte: `/Game/Maps/Dev_TestMap_VisualV2`.

## Ergebnis und Freigabegrenze

Die vorhandene VisualV2 wurde tatsächlich in Unreal erweitert: gemischter Holz-/Steinboden, größerer grüner Läufer, Kamin, Arzneischrank, Kräuterborde, Bettgestelle mit Sichtschutz, neues Pflanzenbanner, grün-cremefarbene Heilerin mit dezenter Idle-Animation sowie reichere Weg- und Waldränder. Die Vergleiche stammen aus der echten Spielkamera. Keine neue Map, Bildkulisse, Projektkopie oder zusätzlicher Worktree.

**Technische Prüfung bestanden; künstlerische Endfreigabe steht aus.** Der Innenraum ist erkennbar reichhaltiger, die Waldränder sind stärker gestaffelt. Die Konzeptvorlage ist noch nicht vollständig erreicht: Kamin und einige Möbel wirken einfacher, Steinflächen haben noch einen recht regelmäßigen äußeren Abschluss, große Wand-/Bodenflächen und die eigentliche Wegmitte bleiben schlichter als das Zielbild. Die Heilerin hat neue Kleidungsmaterialien und Idle, jedoch kein neu ausgearbeitetes Gesicht oder Haar. Keine automatische Aussage „publikationsfertig“.

## Ausgangslage und Schutz

- Ausgangs-HEAD und direkt geprüftes origin/main: `24843e8b970ed68e60137720dbc887ff63b35b10` auf `main`.
- AGENTS sowie GRAFIKSTIL, TECHNIK, SPIELIDEE, SPIELREGELN, ENTSCHEIDUNGEN und Art-Pass-V3-Ergebnisse gelesen. Vorhandener Blender-/Unreal-Workflow verwendet.
- 53 bereits vorhandene unversionierte Dateien einzeln per SHA-256 erhalten; keine davon gestaged. Darunter vier Kreaturen-GLBs, die unversionierte EnvironmentQualityV1-Karte, frühere Bereinigungsunterlagen und vorhandene Prüfwerkzeuge.
- Alle zehn anderen vorhandenen Mapdateien bytegleich zum Anfang erhalten. Nur VisualV2 gespeichert.
- Vollbackup unverändert unter `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd`: `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Kein Vorfahr der hochgeladenen schlanken Historie.
- Bestehende Blenderquellen, GLB-Originale, Player, Ranger-Animationen und Gameplay-C++ unverändert. Keine Datei gelöscht, keine History umgeschrieben, kein Reset/Clean/Prune, keine kostenpflichtige Aktion.
- Nur eigene saubere Editor-Sitzungen normal geschlossen; kein Save All, Discard All oder Force Quit. Nach Speicherung in frischem Editor erneut geladen und streng geprüft.

## Heilhaus: tatsächliche Umsetzung

### Boden und Einrichtung

`M_HH4_OakFloor` verwendet die vorhandene gemalte Holztextur mit weltbasierter, unterschiedlich breiter Dielenaufteilung, versetzten Fugen, Farbwechseln, Abnutzung und matter Oberfläche. Weltkoordinaten verhindern einen Neustart des Materialmusters je alter Bodenplatte. Die vorhandenen großen Plattenabschlüsse sind damit nicht vollständig als Geometrie entfernt.

Eine neue flache, dreidimensionale Natursteinfläche mit versetzten und unterschiedlich breiten, abgeschrägten Steinen ergänzt den Hauptbereich. Der zentrale grüne Läufer und der vorhandene Wartebereich nutzen ein neues flaches Stoffmesh mit sauberem UV-Rechteck, goldenen Einfassungen und einem selbst erstellten sechsblättrigen Naturmotiv. Die zunächst problematischen UVs am Solidify-Rand wurden lokal korrigiert; zuletzt null flächige UV-Degenerationen. Neue Teppiche sind keine erhöhten Blöcke und haben keine neuen Collider.

Empfang bleibt hinten, Wartebereich links, beide bisherigen Heilbetten rechts. Neue Holzrahmen und gefaltete rückseitige Stoffbahnen werten die Betten auf. An der Rückwand stehen der neue Natursteinkamin mit echtem offenem Feuerraum und der bestückte Arzneischrank; neue Kräuterborde und das reliefierte Naturbanner ergänzen vorhandene Einrichtung. Der vorhandene linke Kräuterschrank wurde mitsamt seinem bisherigen Kollisionsobjekt und sämtlichem Regalinhalt um 280 cm in X versetzt, damit er den Kamin nicht verdeckt. Empfangs-/Heilinteraktion und Raummitte bleiben erreichbar.

Kamin und Arzneischrank haben je eine einfache Boxkollision; dekorative Borde, Stoff, Teppiche und Außenkleinteile keine neue Kollision. Die verschobene ursprüngliche Möbelkollision wurde mitgenommen, nicht abgeschaltet. Gebäudehülle, Öffnungen, Innenraumgrenze und Kamera unverändert.

Finale Positionen (Unreal cm; keine neuen Gameplay-Anker):

| Objekt | Position | Hinweis |
|---|---|---|
| Kamin + Feuer | 17342 / 60 / 0 | gemeinsame Position, Yaw 90° |
| Arzneischrank | 17342 / 660 / 0 | Rückwand, Yaw 90° |
| Hauptläufer | 16825 / 500 / 1,9 | flacher Stoff, bestehender Actor |
| Heilerin-Visual | 17230 / 420 / 0,25 | bestehende RestPoint-Identität, Ursprung unverändert |
| Steinfläche | 16950 / 500 / 0,2 | oberhalb bisherigem Boden, bestehender Bodencollider |

`ArtV4_Interior.json` beschreibt den ersten Umsetzungsschritt; `ArtV4_FinalLayout.json`, `ArtV4_HearthPlacement.json` und `ArtV4_FurnitureMoves.json` dokumentieren die finale Komposition und ihre Überlagerung früherer Positionen.

### Innenlicht und Schatten

Nur das vorhandene diffuse Innenraumlicht `V2_House_InteriorDiffuse` wurde von 550 auf 800 lm und von 650×500 auf 900×800 cm erweitert. Lichtfarbe/5000 K bleiben erhalten; ausschließlich Lichtkanal 1, kein Schattenwurf und kein zusätzlicher GI-Eintrag. Die größeren weichen Flächen verbessern die Gleichmäßigkeit. Kaminflammen verwenden eine zurückhaltende warme unbeleuchtete Emission (linear RGB 0,60 / 0,105 / 0,012), keine neue Punktlichtquelle. Randabfall ist weiterhin sichtbar; nicht als vollkommen flache oder schattenlose Gesamtbeleuchtung bezeichnet.

Innen werfen die betroffenen Gebäude-/Möbel-/Figurenkomponenten keine direkten Schlagschatten; räumliche Materialwirkung bleibt bestehen. Die tatsächliche Raumlogik wurde beim Gehen an den Übergängen überprüft. Außen bleiben Lichtquellen, Lichtpositionen, Intensitäten, Schatten, Lumen, Bloom, Exposure und TAA erhalten. Keine globale Schattenabschaltung und kein globaler Helligkeitstrick.

### Fensterflackern: nicht als behoben erklärt

78 tatsächliche 1280×720-Prüfbilder in vier zeitlich geordneten Sequenzen: Innenraum still, Bewegung im Innenraum, außen Annäherung, außen Rückweg. Innen nutzt das Spiel eine feste Kamera; Außenbewegung führt die normale Kamera mit. Die Fenster waren in den geprüften sichtbaren Abschnitten stabil. Nicht alle Außenrückweg-Bilder zeigen noch das Fenster.

Das sporadische Flackern wurde **nicht zuverlässig reproduziert**. Daher keine bestätigte neue Fehlerursache und keine belastbare endgültige Behebung. Bestehende Fenstergeometrie/-materialien, TAA und Lumen wurden nicht auf Verdacht umgebaut. Frühere V3-Befunde zu opaken Fenstern ersetzen keinen neuen Ursachenbeweis. Dichte Bildfolge statt Video; keine Videoabnahme behauptet. Bei erneuter Sichtung sind genaue Position/Zeit und ein zeitlich dichtes Originalvideo erforderlich, um zwischen Kanten-/Temporal-Artefakt, Geometrieüberlagerung und Beleuchtung zu unterscheiden.

## SilverLady / Westland-Heilerin

Die vorhandene gebackene Heilpose dient als geometrische Grundlage. Neue unabhängige Quelle `Art/Characters/NPCs/SilverLady/Source/Westland_Healer_ArtV4.blend`; originale SilverLady-Quellen und V3-Pose bleiben erhalten.

- 149.999 Dreiecke; ein Materialslot. Keine pauschale Neumodellierung oder Polygonreduktion.
- Material: maskierte grüne äußere Gewandteile, cremefarbenes Leinen innen, dezente goldene Saum-/Stichstruktur; bisherige Haut-, Haar-, Normal- und Roughness-Informationen bleiben Grundlage.
- Neues kleines Rig: `root`, `chest`, `head`; FBX-Helper `Westland_Healer_Idle` ergibt vier Unreal-Bones. Vier Sekunden in-place Idle bei 30 fps, dezente Oberkörper-/Kopfbewegung. Kein vollständiges Walk-/Handgesten-/Cloth-Rig.
- Bestehende Skalierung 0,905, rund 1,72 m; keine pauschale Anpassung an Spielerhöhe. Spieler weiter 1,40 m. Füße und Gesamtfigur im tatsächlichen Kameraausschnitt geprüft.
- Neues Skeletal Mesh ohne Physics Asset oder zusätzlichen Gameplay-Collider; bestehendes NPC-Präsentationssystem verwendet. Keine C++-Erweiterung erforderlich.
- Vorwärtsausrichtung für Skeletal-Präsentation korrigiert (Offset 0°, Initial-Yaw 180°); bestehende Blickwendung im Gespräch funktioniert. RestPoint `PokeMonsterRestPoint_1`, Heilung, Speicherung und ursprüngliche Position bleiben erhalten.
- 20 echte QHD-Idle-Prüfbilder über rund zehn Sekunden sowie Runtime-Bone-Sampling: Kopf/Oberkörper verändern sich, Actor-Position bleibt fest. Vollständiger Gesprächs-/Heiltest und Sprite-Fallback bestanden.

**Offen:** Gesicht und Haare sind nicht grundlegend individualisiert; eine grün-cremefarbene Garderobe allein beweist noch keine eigenständige, veröffentlichungsreife Fantasy-Person. Die ursprüngliche Arwen-Anmutung muss vor Veröffentlichung gezielt künstlerisch geprüft und gegebenenfalls weiter verändert werden. Eine vollwertige Gesprächsgestik oder komplexe Gewandverformung wurde nicht erreicht.

## Wege und Waldränder

Drei bestehende private VisualV2-HealingArtV4-Bodenmaterialien gezielt erweitert: mehrere Erdtöne, langsam wechselnde Breite innerhalb der bisherigen Randvariation, festgetretene Struktur, eingebettete abgerundete Steinsplitter und kleine Wurzel-/Laubflecken. Bestehende Wegmittellinien, Abzweige, Brückenmasken, Wasser und Bodenkollisionen bleiben erhalten. Zusätzliche Breitenvariation bleibt bei ungefähr 11–15 cm, damit die Steuerungs-/Navigationsrichtungen nicht verändert werden.

727 zusätzliche Instanzen in zehn HISM-Gruppen: 180 Grasbüschel, 110 Klee, 85 Wildblumen, 55 Farne, 23 Sträucher, 75 Moospolster, 160 Kiesel, 12 Wurzelelemente, 15 Äste und 12 kleine Felsgruppen. Dazu zwei niedrige dekorative Zaunelemente außerhalb des Laufwegs. Ungleiche Gruppen, unterschiedliche Höhen und bewusste Lücken; vorhandene Bäume und Vegetation nicht verschoben oder entfernt. Die 23 neuen Strauchgruppen wurden in der Sichtprüfung noch auf 60 % bzw. 86 % ihrer ersten Größe differenziert, damit keine durchgehende Hecke entsteht. Die finalen Skalierungen stehen im Landschaftsmanifest.

Neue kleine Instanzen sind dekorativ, ohne Kollision und ohne zusätzliche Einzelschatten; bestehende Baum-/Vegetationsschatten bleiben unverändert. Das ist keine neue globale Schattenvariante. Neue Geometrie ergänzt echte räumliche Staffeln; keine flachen Konzeptbild-Ebenen.

Die Sichtprüfung zeigt eine größere Verbesserung an den Wegsäumen und am Unterholz als in der Wegmitte. Der Erdweg ist noch deutlich schlichter als der Referenzweg mit seinen dicht gemalten, unregelmäßigen Kies-/Bodenschichten. Keine Behauptung, die Konzeptqualität sei bereits vollständig erreicht.

## Neue Quellen und Assets

Alle unter dem bestehenden Projekt; frühere Quellen erhalten. Quellen in Metern, Unreal in cm.

- `Art/HealingHouse/Source/HealingHouse_ArtV4.blend`
- `Art/HealingHouse/Exports/SM_HH4_*.fbx`
- `Art/Characters/NPCs/SilverLady/Source/Westland_Healer_ArtV4.blend`
- `Art/Characters/NPCs/SilverLady/Exports/SK_WestlandHealer_ArtV4.fbx`
- `Art/Characters/NPCs/SilverLady/Exports/A_WestlandHealer_Idle.fbx`
- `/Game/Environment/HealingHouse/ArtV4/Meshes/SM_HH4_*`
- `/Game/Environment/HealingHouse/ArtV4/Materials/M_HH4_*`
- `/Game/Characters/NPCs/SilverLady/HealerArtV4/Meshes/SK_WestlandHealer_ArtV4` und zugehöriges Skeleton
- `/Game/Characters/NPCs/SilverLady/HealerArtV4/Animations/A_WestlandHealer_Idle`
- `/Game/Characters/NPCs/SilverLady/HealerArtV4/Materials/M_WestlandHealer_HerbalLinen`

Die vom Nutzer gelieferte Konzeptdatei liegt unverändert als **künstlerische Quelldatei**, ausdrücklich nicht als Unreal-Nachweis, unter `Art/HealingHouse/References/ArtV4_UserConcept.jpg`. Keine fremden 3D-Modelle hinzugekauft oder generiert.

| Eigenes Prop | Vertices | Dreiecke |
|---|---:|---:|
| FlagstoneApron | 7000 | 13500 |
| Hearth | 968 | 1820 |
| HearthFlames | 35 | 21 |
| RemedyCabinet | 4708 | 7824 |
| BedCanopy | 771 | 1328 |
| HerbalBanner | 349 | 592 |
| HerbalWindowShelf | 859 | 1184 |
| FallenBranch | 120 | 228 |
| WovenRug | 1650 | 3296 |

Beide neuen Blenderdateien separat erneut geöffnet: keine fehlenden Texturbilder, fünf gepackte Bilder in der Heilerquelle, keine Änderung durch die Prüfung. Neun Propmeshes ohne gemessene Nullflächen. FBX-Reimport des korrigierten Teppichs ohne neue Tangenten-/Binormalwarnungen. Keine finale Runtime- oder vollumfängliche Manifold-Freigabe aus diesen Prüfungen abgeleitet.

## Reales Qualitätsreview und Bildnachweise

Neun Bildpaare, **2560×1440 Pixel**, High, 100 % Screen Percentage, echte bestehende Gameplay-Kamera, FOV 35°. Positionen/Rotationen/Spielerpositionen in den gepaarten Metadaten maximal unter 0,001 cm/Grad auseinander. Außen Pitch −50°/Yaw −45°, innen die unveränderte feste Innenkamera. Fotopositionierung erfolgt diagnostisch; der getrennte Gameplay-Fußlauf verwendet keine Testteleports.

Die JPG-Vergleichstafeln sind lediglich nebeneinander gesetzte, verkleinerte echte QHD-Aufnahmen, links vorher/rechts nachher. Originale PNGs bleiben für volle Detailprüfung lokal. Keine generierten Konzeptbilder als Umsetzung ausgegeben. Nur die Quellenreferenz wird versioniert; Kontrollbilder und Videos bleiben unter ignoriertem Saved.

### Wald

![Wald vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Wald.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Wald00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalReview/Wald00000.png)

### Wiese

![Wiese vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Wiese.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Wiese00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalReview/Wiese00000.png)

### Flussufer

![Flussufer vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Flussufer.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Flussufer00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalReview/Flussufer00000.png)

### Uferabzweig

![Uferabzweig vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Uferabzweig.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Uferabzweig00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalReview/Uferabzweig00000.png)

### Heilhaus

![Heilhaus vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Heilhaus.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Heilhaus00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalReview/Heilhaus00000.png)

### Fassade

![Fassade vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Fassade.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Fassade00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalReview/Fassade00000.png)

### Innenraum

![Innenraum vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Innenraum.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Innenraum00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalLight/Innenraum00000.png)

### Empfang

![Empfang vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Empfang.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Empfang00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalLight/Empfang00000.png)

### Heilbereich

![Heilbereich vorher / nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Comparisons/Heilbereich.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/Before/Heilbereich00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV4/FinalLight/Heilbereich00000.png)

### Künstlerische Bewertung

| Kriterium | Bewertung |
|---|---|
| Nähe zur Vorlage | Sichtbarer Schritt, noch keine gleichwertige Detaildichte und malerische Ausarbeitung. |
| Materialqualität | Neue matte Holz-/Stein-/Stoffvariation, besser lesbarer grüner Läufer; einige Flächen weiterhin zu einfach/regelmäßig. |
| Natürlichkeit | Lebendigere Vegetationsgruppen; Wegmitte und einzelne neue Propformen benötigen weiteren Feinschliff. |
| Raumwirkung | Kamin, gestaffelte Regale, Bettgestelle und Steinzone schaffen mehr Tiefe; freier Hauptlaufweg erhalten. |
| Maßstab | Bestehender 1,40-m-Player erhalten; neue Einrichtung im Spiel geprüft, Heilerin etwa 1,72 m. |
| Beleuchtung | Innen heller/gleichmäßiger ohne neue direkte Schlagschatten; Außenlicht/-schatten geschützt. |
| Spielbarkeit | Echter Rundweg, Interaktionen und beide neue Möbelkollisionen bestanden. |

## Technische Prüfungen

| Prüfung | Tatsächlich ausgeführt / Ergebnis |
|---|---|
| Mac Development Editor Build | Exit 0, 27,47 s; kein C++ geändert. |
| Vollständige Projekt-Automation | **50/50**, 0 Warnungstests, 0 fehlgeschlagen, 0 übersprungen; Exit 0, 31,93 s. |
| Map Check | Alle elf vorhandenen Karten geladen, je 0 Fehler/0 Warnungen; keine fremde Karte gespeichert. |
| Ranger-V3-Regression | Bestehender FinalMapAudit unverändert aufgerufen; bestanden. |
| Frischer Editor / gespeicherte Map | VisualV2 neu geladen, Actor-Vertrag und zulässiger Änderungsumfang bestanden. |
| Vollständiger Enhanced-Input-Fußlauf | 102 Schritte, 285,93 m, 177,61 Spielsekunden, **ohne Testteleports**, bestanden. |
| Spieler / Kamera | Außen/innen, acht Richtungen, Sprint bis 315 cm/s, normales Gehen 210 cm/s, Menu-Locks geprüft. |
| Gameplay | Wanderer-Dialog/Quest, Liora, Archivabschluss, Brücke, Wildkampf, Fang, Heilhaus rein/raus gerade+diagonal, Heilung/Checkpoint, Save/Load bestanden. |
| Heilerin | Mesh sichtbar, Gesprächsblickwendung, Heilung, Idle, Sprite-Fallback, keine neue Colliderstörung. |
| Live Schatten-/Raumgrenzenaudit | 319 Innen-/2079 Außenframes, 38 Heilerin-Gesprächsframes, keine Auditfehler. |
| Neue Möbelkollisionen | Nach Diagnose-Startposition echter Input gegen Kamin/Schrank und zurück, beide blockieren, kein Durchfallen. |
| Originaler Dev-Spielstand | Nach vollständigem Test bytegenau restauriert; SHA-256 siehe unten. |
| Pflichtdateien | 3654 Dateien im Art-Commit-Snapshot vollständig per SHA-256; spätere Berichtsdokumente separat ergänzt. |
| Python-Werkzeugtests | 8/8 DevelopmentEvidence; bestehende MapLifecycle-Tests 5/5. |
| Git-Diffs / Index | `git diff --check` und `git diff --cached --check` bestanden; ausschließlich explizite eigene Pfadliste. |

Originalsave `Saved/SaveGames/PokeMonster_Dev.sav` wiederhergestellt auf SHA-256 `a0ad009a7b3c6f883d1413b0f96df5b25bc7ab953d0154e29ae50f35ad48bf0a`. Der im FootTest festgehaltene Save-Hash innerhalb des Tests ist nicht der restaurierte Originalhash; separate Restore-/Schutzprüfung bestätigt die Rückgabe.

Kein FPS-Benchmark, kein umfangreiches GPU-Profiling, kein Cook-/Pakettest und keine neue Standalone-Gameplay-Abnahme in diesem Durchgang. Keine erfundenen Performance- oder Plattformgarantien.

### Diagnosen, Fehlversuche und Warnungen

- Neuer Heilerin-Materialimport verwendete zunächst einen unpassenden LinearColor-Sampler für die vorhandene Masken-/Roughness-Textur. Echter Metal-Materialkompilierungsfehler mit grauer Ersatzdarstellung. Auf den korrekten Mask-Sampler geändert; frische finale Sitzung ohne diesen Kompilierungsfehler. Ursprüngliche Textur unverändert.
- Teppichrand hatte zunächst UV-Probleme und FBX-Tangentenwarnungen. Rand-UVs gezielt korrigiert; abschließender eigener Reimport ohne diese Warnungen. Anfangslogs nicht als erfolgreicher Endstand ausgegeben.
- Materialinstanz `MI_WLA_MossStone` wurde durch neue HISM-Verwendung automatisch als InstancedStaticMesh-tauglich markiert. Live-/Disk-Fingerprints zeigen gleiche Nodes, Links, Parent, Texturen und Werte; nur Usage-Bit 128 kam hinzu. Deshalb genau diese Änderung erhalten und gespeichert. **Das Asset ist byteweise geändert**, seine optischen Einstellungen nicht. Kein unnötiges Duplikat.
- Ein vorgeschlagenes automatisches Paket-Reload wurde von der automatischen Sicherheitsprüfung wegen möglichem Verlust ungesicherten Editorzustands abgelehnt. Es wurde nicht ausgeführt. Anschließend vollständiger read-only Vergleich; sichere Speicherung des erhaltenen Usage-Zustands, ohne Reload/Verwerfen. Keine verbleibende Datenverlustblockade.
- Erste Diagnose-Commandlet-Aufrufe mit relativem Projektpfad scheiterten am Descriptor; auf absoluten Pfad korrigiert. Read-only Materialfingerprint wurde ausgegeben; jener parallele Commandlet-Prozess beendete sich wegen belegtem MCP-Port 8000 mit Exit 1. **Nicht als bestandener QA-Lauf gezählt.** Separater vollständiger QA-Lauf bei geschlossenem Editor bestand.
- Erste Idle-Diagnose benutzte nicht exponierte Python-Bone-APIs. Diagnose auf `get_bone_name`/`get_socket_location` korrigiert; finale echte Bild-/Bonesampling-Prüfung bestanden.
- Frisch geladenes Szenen-JSON unterschied sich nur durch exakt gleichwertige vorzeichenbehaftete Null und den normalerweise nicht persistierten, ungenutzten NPCStaticVisual ohne Mesh. Genau diese zwei Darstellungsunterschiede kanonisiert, keine Geometrie-/Positionsabweichung toleriert und keine aktive Komponente ignoriert. Strenger erneuter Vergleich bestanden.
- Engine-Logs sind nicht vollkommen fehler-/warnungsfrei: bekannte 17 generische `LogAutomationTest: Condition failed` bei Frame 0 vor den Projekttests, inkompatibles `idevice_id`-Hilfsprogramm (Bad CPU type), Audio-Samplerate-, MotionVectorSimulation-, MCP-Hinweis- und Telemetrie-Shutdown-Meldungen. Nicht unterdrückt. Die 50/50 beziehen sich auf die strukturierten PokeMonster-Testergebnisse, nicht auf ein warnungsfreies gesamtes Engine-Startlog.

## Nachvollziehbare lokale Ergebnisse

- `Saved/ProjectRefinement/ArtV4Build/Result.json` und Buildlog
- `Saved/ProjectRefinement/ArtV4Automation/Report/index.json`, Result.json und Engine.log
- `Saved/ProjectRefinement/ArtV4AcceptanceEditor.log`
- `Saved/ArtPassV4/MapCheckResults.json`, FinalMapAudit.json
- `Saved/ArtPassV4/ScopeValidation.json`, ReopenEquivalence.json, ProtectionFinal.json
- `Saved/ArtPassV4/Acceptance/Final/FootTest.json`, RuntimeAudit.json, SaveRestored.json
- `Saved/ArtPassV4/FurnitureCollision.json`
- `Saved/ArtPassV4/BlenderReopen.json`
- `Saved/ArtPassV4/IdleFinal/Result.json` und echte QHD-Einzelbilder
- `Saved/ArtPassV4/WindowFinal/Result.json` und 78 echte 720p-Einzelbilder
- `Saved/ArtPassV4/PhotoValidation.json` und neun Vergleichstafeln
- `Saved/ArtPassV4/IndexAudit.json` und Remote-LFS-Prüfung

Diese optionalen lokalen Nachweise werden nicht zu Pflichtdateien eines Clones gemacht. Versionierter kompakter Prüfstand: `Tools/ProjectMaintenance/ArtV4Acceptance.json`. Alle Umsetzungs-/Diagnoseskripte sowie Quell-/Assetmanifeste liegen im bestehenden Projekt. Keine automatisierte künstlerische Qualitätsfreigabe aus Hashes/Tests abgeleitet.

## GitHub-Sicherung

- Art-Commit: `b859e5757e1b37f80f753059655b352baaf61308` – `art: enrich VisualV2 healing house and forest edges`.
- Regulärer Push `24843e8..b859e57` nach origin/main erfolgreich; Remote-Hash direkt mit `git ls-remote` bestätigt.
- 78 explizit geprüfte Commitpfade; 1.690.481 Bytes normale Git-Inhalte unkomprimiert, 36 LFS-Objekte mit 115.335.237 Bytes.
- **Alle 36 Remote-LFS-Dateien tatsächlich heruntergeladen und SHA-256/Größe gegen Index und lokale Quellen verifiziert.** Keine Zugangsdaten oder Download-URLs im Bericht gespeichert.
- Nach den letzten Materialkorrekturen vollständige Automation erneut: **50/50, 0 fehlgeschlagen/übersprungen/Warnungstests**, Exit 0, 24,66 s. Ergebnis unter `Saved/ProjectRefinement/ArtV4FinalAutomation/Result.json`.
- Tracked-Arbeitsbaum nach Art-Commit sauber; die 53 ursprünglichen unversionierten Dateien bleiben geschützt. Anschließender Dokumentationscommit enthält nur diesen Bericht, TECHNIK, ENTSCHEIDUNGEN und die zwei zugehörigen Prüfmanifeste.

Der Bericht mit diesen Prüfergebnissen wird anschließend separat auf main gesichert; sein eigener Hash steht im Git-Log und in der Abschlussantwort, nicht als unmöglicher selbstreferenzieller Dateihash. Keine Kontrollmedien hochgeladen; nur die tatsächliche Nutzer-Konzeptreferenz ist benötigte künstlerische Quelle. Unversionierte Ausgangsdateien bleiben unberührt.

## Empfehlung / nächste Freigabe

Diesen Stand als technisch geprüften **Zwischenstand zur visuellen Abnahme** ansehen. Keine automatische Ausweitung auf andere Maps. Nächster künstlerischer Schwerpunkt wäre die weniger regelmäßige Stein-/Holzübergangszone, stärker ausgearbeitete Kamin-/Schrankoberflächen und eine eigenständige Gesicht-/Haarüberarbeitung der Heilerin. Für die Wege zuerst die Wegmitte detaillierter und organischer ausarbeiten, statt nur mehr Randinstanzen hinzuzufügen. Das sporadische Fensterproblem bleibt bis zu einer reproduzierten Sichtung offen.
