# VisualV2 Heilhaus Art Quality V3 – Prüfbericht

Datum: 19.10.2026. **Begrenzter Art-Abnahmestand, keine automatische Stilfreigabe.**

## 1. Ausgangslage und Schutz

- Schlanker Worktree: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`; Branch `codex/slim-backup-v5`.
- Ausgangs-HEAD und unmittelbar geprüfter GitHub-Stand:
  `716d0c3dfc23e9c5ffa95e57c1a1627f8d6d945b`.
- AGENTS, GRAFIKSTIL, TECHNIK, SPIELIDEE, SPIELREGELN, ENTSCHEIDUNGEN,
  World-Art-V2-Bericht und ältere Würfel-/Heilhausbefunde gelesen.
- Bereits vorhandene fremde/unzugeordnete unversionierte Arbeit erhalten und
  nicht aufgenommen: `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap`,
  `Tools/VisualV2EnvironmentQualityV1/`, `Tools/VisualV2QualityV2/__pycache__/`.
- Lokaler `main` und Archiv-Ref stehen weiterhin unverändert auf
  `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Dieser Commit ist kein Vorfahr des
  schlanken Entwicklungszweigs und wird nicht gepusht.
- Bearbeitete Karte: **`/Game/Maps/Dev_TestMap_VisualV2`**,
  Datei `Content/Maps/Dev_TestMap_VisualV2.umap`. Keine neue Content-Map.
- Vorherdatei außerhalb des Projekts gesichert:
  `/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/Dev_TestMap_VisualV2_Before.umap`.
  SHA-256: `e02de70d82ff71ed452d5ebbc45648d091ddb002573a54841b42f86c6df51c09`.
- 16 andere vorhandene Kartendateien sind per SHA-256 unverändert,
  einschließlich WestlandRegion, AssetLibrary und aller bisherigen Testkarten.
- Blender-GUI mit dem fremden Hobbit-Arbeitsstand blieb unberührt. Neue Pflanzen
  ausschließlich in separaten Blender-Hintergrundprozessen bearbeitet.

## 2. Orangefarbener Würfel – tatsächlicher Befund

| Eigenschaft | Ergebnis |
| --- | --- |
| Actor-Label | `V2_House_HH_V3_SupplyCrate` |
| Objektname | `StaticMeshActor_505` |
| Klasse | `/Script/Engine.StaticMeshActor`, kein Gameplay-Blueprint |
| Mesh | `/Engine/BasicShapes/Cube.Cube` |
| Material | `/Game/Environment/HealingHouse/Materials/M_HH_V2_Wood.M_HH_V2_Wood` |
| Weltposition, cm | **−3570, −62, 18** |
| Skalierung | 0,42 / 0,42 / 0,36 |
| Größe | 42 × 42 × 36 cm; Unterkante Z=0, schwebt nicht |
| Kollision / Schatten | NoCollision / kein Schattenwurf |
| Ursprung | `Tools/DressHealingHouseV3.py`, dekorativer Aufruf `SupplyCrate` |
| Tags | HealingHouse_V3, HealingHouse_V3_Decoration, DevVisualV2_HealingHouse |

Aktuelle Actor-Daten als T3D exportiert und auf Verweise auf diese konkrete
Instanz geprüft; Unicode-Exporte korrekt eingelesen. Keine serialisierten
Actor-Verweise gefunden. Zusätzlich native Object-Reference-Suche durchgeführt:
Level-, Python- und Editor-/GC-Verweise sind erwartbare Infrastruktur und allein
kein Gameplay-Nachweis. Quellsuche und Erzeugungscode bestätigen Dekoration;
keine erkannte Interaktions-, Quest-, Speicher-, Kollisions- oder Blueprintfunktion.
Das gemeinsam verwendete Cube-Mesh und das Holzmaterial bleiben erhalten.

**Nur diese Instanz wurde entfernt.** Keine pauschale Entfernung ähnlich benannter
Objekte. Der vollständige Gameplay-Fußlauf bestätigt, dass ihre Entfernung die
geprüften Funktionen nicht beeinträchtigt.

## 3. Boden und Wegübergänge

Fünf vorhandene Komponenten erhalten private Varianten von vier Materialgraphen:

- `V2_Ground`
- `V2_House_Forecourt`
- `V2_Path_VillageLoop`
- `V2_Path_NorthLoop`
- `V2_House_HH_Q2_OrganicApproach`

Neue Albedo-Quellen: `T_HA3_Meadow.png` und `T_HA3_Earth.png`. Malerisch feine
Gras-/Klee- und Bodenstrukturen, zurückhaltende mineralische Details und ruhigere
Farbverteilung. Erzeugt mit dem eingebauten Imagegen; Prompts und tatsächliche
Dateigrößen in `Art/World/VisualV2HealingArtV3/TexturePrompts.json`.
**Quellen tatsächlich 1254 × 1254 Pixel**, nicht native 2048². Unreal verwendet
Zweierpotenz-Import mit maximal 2048²; das ist keine zusätzliche Quelldetailauflösung.
Keine eingebrannte Studiobeleuchtung beabsichtigt, keine Normal-/AO-Bakes erzeugt.

Die bestehenden versetzten/gedrehten Texturkoordinaten und die örtliche Makrovariation
bleiben Grundlage. Zusätzliche feine Variation, dezente Abnutzung in der Wegmitte
und unregelmäßige Grasanteile an den Säumen. Feine zusätzliche Randabweichungen
vermeiden zu gleichmäßige Maskenkanten. Keine neuen Material-Layer oder Decal-Stacks.
Maximal zehn Farbtextur-Abfragen im erweiterten Graphen statt zuvor fünf; alte und
neue Quellen werden zum Schutz des übrigen Geländes lokal gemischt. Das ist ein
Qualitätspass, **keine nachgewiesene Shader- oder Performanceoptimierung**.

Wirkungsbereich ungefähr X −4620…−3560, Y −720…1190 cm, mit weichem Auslauf.
Außerhalb dieses Bereichs bleibt die bisherige Bodenfarbe erhalten; die örtliche
Vorplatzmaske betrifft ausschließlich das vorhandene Vorplatzobjekt. Wegeführung,
Meshpositionen, Höhen und Kollisionsflächen wurden nicht geändert.

## 4. Topfpflanzen

**26 vorhandene Außen-Actor** erhalten fünf wiederverwendbare private Varianten.
18 Fensterkräuter und acht Eingangs-/Vorplatztöpfe. Position, Rotation, Skalierung,
Actor-Identität, Kollision und Schattenflags bleiben erhalten. Innenraumtöpfe und
sonstige Vegetation werden nicht ersetzt.

Die vorhandenen handgeformten Q3-Töpfe wurden übernommen. Neue verzweigte Stängel,
kleinere unterschiedlich große gewölbte Blätter, zentrale Blattform, dezente
Blattadern, sichtbare Erde, kleine cremefarbene Blüten und einzelne rankende Triebe.
Vier gemeinsame Materialfamilien statt separater Materialien je Pflanze;
beidseitige Blattgeometrie ohne große transparente Alpha-Blattkarten.
Bestehender HouseCutaway-Materialmechanismus bleibt in den Blattvarianten erhalten.
Vorhandene Terracotta-Bildquelle wiederverwendet.

| Familie | Platzierungen | Dreiecke je Mesh | Unreal-Vertices | Abschnitte | Quellhöhe cm |
| --- | ---: | ---: | ---: | ---: | ---: |
| BroadHerb | 8 | 8,396 | 6,355 | 3 | 82.92 |
| NarrowHerb | 2 | 9,944 | 7,505 | 3 | 88.59 |
| LeafPlant | 2 | 7,880 | 5,951 | 3 | 79.51 |
| FlowerPlant | 8 | 13,028 | 9,499 | 4 | 79.09 |
| TrailingHerb | 6 | 6,332 | 4,823 | 3 | 43.66 |

Fünf unterschiedliche Meshes zusammen 45.580 Dreiecke. Über alle 26 Platzierungen
245,032 Dreiecke bei vollständig dargestelltem LOD0, ohne Sichtbarkeitsbewertung.
Das ist eine Geometriemenge, kein gemessener GPU-/Draw-Call-Wert. Höhere Blattdetailtiefe
ist hier bewusst Teil des Art-Auftrags; keine Reduktion allein zur FPS-Steigerung.
Die vorhandenen 140-cm-Spielerproportionen wurden nicht verändert.

### Nachgewiesene technische Korrekturen während der Arbeit

1. Erster Spielversuch zeigte zu helle Blätter. Blender-/FBX-Roundtrip und tatsächlich
   eingelesene Unreal-Vertexfarben verglichen. FBX-Farben waren sRGB-codiert,
   der erste Materialgraph behandelte sie als linear. Explizite sRGB→linear-Übertragung
   ausschließlich in den neuen Blatt-/Blütenmaterialien korrigiert; kein Licht geändert.
2. Zusätzlicher UV-Test fand 144 degenerierte UV-Dreiecke an flachen Topfringen des
   übernommenen Pottery-Meshs. Diese Flächen erhalten planare UVs; seitliche
   zylindrische Wand-UVs bleiben erhalten. Finale Prüfung: **0 degenerierte UV-Dreiecke**.
3. Reimportiert nur die fünf eigenen Varianten. Gerenderte Dreieckspositionen vor/nach
   überprüftem Reimport stimmen bis 0,00001 cm überein. Keine Geometrieänderung durch
   diese UV-Reparatur. Keine neue Kollisionsgeometrie.

Neue Quelle: `Art/World/VisualV2HealingArtV3/Source/HealingHouse_PottedPlants_V3.blend`.
Gepackte Textur, erneut geöffnet, fünf vollständige Pflanzenmeshes; keine Nullflächen,
Nullnormalen oder nicht endlichen Vertices. Offene Blattflächen sind beabsichtigt,
kein geschlossenes Manifold-Körpermodell beansprucht. Fünf FBX-Importquellen gespeichert.

## 5. Geschützter Umfang

Der Szenenvergleich erfasst dieselben Actor-/Komponentensignaturen wie die vorhandene
VisualV2-Abnahme. 31 Actor ändern ausschließlich Mesh-/Materialbindungen;
1 dekorative Instanz entfällt; **1322 andere Actor-Signaturen unverändert**.
Alle 175 HISM-Kleinvegetationsinstanzen inklusive Transformationen unverändert.

Keine Änderungen an Gebäudemeshes, Innenraum, übriger Vegetation, Spieler-/NPC-Assets,
Bewegung, Animation, Collision, Eingabe, Dialog-, Quest- oder Speicherlogik.
Lichtquellen, deren Position/Intensität, Originalschatten, Lumen, Bloom, TAA und
Postprocess-Einstellungen unverändert. Kamera weiterhin 2850 cm / −50° / −45° / 35°.
Der Audit ist eine gezielte Signaturprüfung; er wird nicht als vollständige Prüfung
jedes nicht exponierten Engine-internen Feldes ausgegeben.

## 6. Echte Bildvergleiche

80 überprüfte Einzelaufnahmen: vorher/final nachher, jeweils fünf Kamerapositionen,
720p und QHD, Medium und High, eingebettetes PIE und eigenständiges `-game`.
Kein gepackter Shipping-Build. Kamerapositionen, Rotation, Spielerposition und FOV
pro Paar abgeglichen, Ausgabegrößen zusätzlich anhand der PNG-Dateien geprüft.
Fünf Sekunden Wartezeit je Pose; Bilder außerhalb von Leistungsmessungen aufgenommen.
Teleports dienen ausschließlich der reproduzierbaren Fotopositionierung;
der separate Gameplay-Fußlauf verwendet keine Testteleports.

| Modus | Ausgabe | Qualität | Auflösungsskalierung / Nachweis |
| --- | --- | --- | --- |
| PIE, vorher/nachher | 1280×720 und 2560×1440 | Medium und High | Primary 100 %, Secondary 100 %, Ausgabe geprüft |
| Standalone, identische Paare | 1280×720 und 2560×1440 | Medium und High | Primary 100 %, Secondary automatisch/DPI (CVar 0), beide Seiten identisch |
| Standalone, zusätzliche finale Sichtprüfung | 1280×720 und 2560×1440 | Medium und High | Primary und Secondary ausdrücklich 100 %, Dynamic Resolution 0, Ausgabe geprüft |

Die zusätzlichen 20 Standalone-Vollauflösungsbilder werden nicht als vorher/nachher
bei identischer interner Auflösung ausgegeben. Sie bestätigen die finale Darstellung
bei expliziter Vollauflösung. Die skalierungsbereinigte vorher/nachher-QHD-Reihe liegt
in PIE vor. Keine GPU-Allocation-Readbacks oder Laufzeitbenchmarks durchgeführt.

Vergleiche, High/PIE:
- [Heilhaus](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/Comparisons/PIE_Q2_Heilhaus_BeforeAfter.png)
- [Vorplatz](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/Comparisons/PIE_Q2_Vorplatz_BeforeAfter.png)
- [Wegsaum](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/Comparisons/PIE_Q2_Wegsaum_BeforeAfter.png)
- [Kraeutertoepfe](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/Comparisons/PIE_Q2_Kraeutertoepfe_BeforeAfter.png)
- [Grasflaeche](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/Comparisons/PIE_Q2_Grasflaeche_BeforeAfter.png)
- [Topfpflanzen – unveränderte Originalpixel-Ausschnitte](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/Comparisons/PIE_Q2_PotDetail_BeforeAfter.png)

Alle Vergleichsboards: `/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/Comparisons`.
Rohaufnahmen: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2HealingArtV3/Photos`. Tatsächliche Quellen und Rechtecke sind in den
Vergleichsmanifesten verzeichnet. Nur gleiche Skalierung beziehungsweise klar
bezeichnete unveränderte Ausschnitte; keine Retusche, keine synthetischen
Konzeptbilder als Unreal-Nachweis. Keine Kontrollmedien für Git vorgesehen.

## 7. Technische und Gameplay-Abnahme

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Mac Development Editor Build nach letzter UV-Reparatur | erfolgreich, Exit 0 |
| Vollständige PokeMonster-Automation nach letzter Reparatur | **49/49 erfolgreich**, 0 fehlgeschlagen, 0 mit Warnungen, 0 ausgelassen |
| Frischer Editor / gespeicherte Map erneut laden | entspricht der geprüften Szenensignatur |
| Map Check nach letzter Reparatur | **0 Fehler / 0 Warnungen** |
| Blenderquelle erneut öffnen | erfolgreich, Textur gepackt |
| Blender Geometrie und UVs | keine gefundenen Nullflächen/Nullnormalen/nonfinite Vertices/degenerierten UV-Dreiecke |
| Unreal-Reimport / Maße / Materialien | fünf Meshes geprüft, Dreieckzahlen stimmen, Maßabweichung <0,05 cm, 0 einfache Kollisionsformen |
| Echter eingebetteter PIE-Fußlauf | **102 Schritte, 283.56 m**, keine Testteleports, erfolgreich |
| Sprint / Richtungen / Stoppen | bestehender Enhanced-Input-Ablauf, acht Richtungen, maximal 315 cm/s |
| Gespräche / Quest / Menü | Wanderer, Queststart/-abschluss, Liora, Archiv und Menü erfolgreich |
| Kampf / Fang | Wildfang und Trainerkampf erfolgreich |
| Heilhaus | gerader und diagonaler Eintritt/Austritt, Heiler, Heilung/Checkpoint erfolgreich |
| Save/Load | erfolgreich; ursprüngliche Abwesenheit des Dev-Slots wiederhergestellt |
| Baumkronenfreistellung / NPC-Sprite-Fallback | vorhandene Laufzeitprüfungen erfolgreich |
| Material-/Shaderfehler in finalen Renderläufen | keine neuen Fehler, kein grauer Material-Fallback festgestellt |
| Shipping-Cook / physischer Controller | nicht Bestandteil dieser Abnahme, nicht durchgeführt |

Fußlauf: 180.66 Spielsekunden, 203.98 Wandsekunden.
Das sind Ablaufzeiten, keine FPS-Benchmarkwerte. Standalone wurde visuell getestet;
ein zweiter vollständiger Standalone-Gameplay-Rundweg wurde nicht behauptet.

### Fehlermeldungen und Einschränkungen offen benannt

- Anfangs mussten geschützte Unreal-Python-Eigenschaften über die korrekte Editor-API
  angesprochen werden. Autorenskriptfehler und temporäre Meldungen unvollständiger
  Materialgraphen wurden behoben, bevor der finale Stand geprüft/gesichert wurde.
- Eine ältere Prozesswache konnte ihre eigene Shell-Befehlszeile mit einem Editor
  verwechseln. Sie prüft jetzt reale ausführbare Prozesspfade; kein Force Quit.
- Native Engine-Toolset-Initialisierung meldet vor und nach dieser Arbeit jeweils
  **58 Python-Fehlerzeilen / 47 gleiche Fehlersignaturen**. Keine neue Signatur.
  Diese vorhandenen Engine-Startfehler sind nicht als behoben ausgegeben.
- Editor-Startlogs enthalten schon vor der Arbeit und auch im finalen Map-Check- und
  Automation-Start jeweils 17 allgemeine `Condition failed`-Meldungen. Die gesonderte
  Projekt-Automation exportiert trotzdem 49 erfolgreiche Tests ohne Testwarnungen.
- Vorhandene macOS-`idevice_id`-/Audio-/MCP-Startwarnungen bleiben. Keine Warnung
  unterdrückt; vollständige lokale Logs aufbewahrt.
- Noch keine menschliche Freigabe der Artqualität. Einzelne alte Fassadendetails,
  geometrische Bodenformen und vereinfachte Restpflanzen bleiben erkennbar.
- Boden bleibt ein gekacheltes Material mit örtlicher Variation, kein individuell
  durchgemaltes Landschaftsmodell. Randabschnitte können weiter weich/gleichmäßig wirken.
- Feine Kräuterblätter verlieren aus normaler Spielentfernung Details; TAA-Weichheit
  und bestehende dunkle Figuren in Schatten sind nicht Teil dieser Überarbeitung.
- Keine FPS-Benchmarks und kein GPU-Profiling: die abschließende Vorgabe
  **ART QUALITY FIRST** ersetzt die frühere Performanceforderung dieses Auftrags.
  Entsprechend keine FPS-, GPU-Zeit-, Bildzeit- oder Performancegewinnbehauptung.

## 8. Neue Unreal-Assets

- `/Game/Environment/VisualV2HealingArtV3/Textures/T_HA3_Meadow`
- `/Game/Environment/VisualV2HealingArtV3/Textures/T_HA3_Earth`
- `/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_HealingMeadow`
- `/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_HealingPath`
- `/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_HealingForecourt`
- `/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_LegacyApproach`
- `/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_Pot`
- `/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_Foliage`
- `/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_Soil`
- `/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_Blossom`
- `/Game/Environment/VisualV2HealingArtV3/Meshes/SM_HA3_BroadHerb`
- `/Game/Environment/VisualV2HealingArtV3/Meshes/SM_HA3_NarrowHerb`
- `/Game/Environment/VisualV2HealingArtV3/Meshes/SM_HA3_LeafPlant`
- `/Game/Environment/VisualV2HealingArtV3/Meshes/SM_HA3_FlowerPlant`
- `/Game/Environment/VisualV2HealingArtV3/Meshes/SM_HA3_TrailingHerb`

Reproduzierbare Quellen und Anleitung:
`Art/World/VisualV2HealingArtV3/README.md`, `Tools/VisualV2HealingArtV3/README.md`.
Vorherbindungen und Positionen in `Scope.json`; ältere Quellen/Assets bleiben erhalten.

## 9. GitHub-Sicherung und Entscheidung

Zwei logisch getrennte Sicherungsschritte: private Artquellen/Assets/Werkzeuge sowie
zentrale Kartenübernahme mit Bericht. Keine Kontrollbilder, Videos, Renderings,
Rohlogs oder Bytecode im Commit. Nur die beiden benötigten Albedo-PNGs werden als
Bildquellen aufgenommen; .blend/.fbx/.uasset/.umap und diese Texturen über LFS.

Asset-/Werkzeug-Commit: `453b4a1710883b92b3001bff88691683fb5ede60`.
Karten-/Berichts-Commit und Remote-/LFS-Verifikation im abschließenden lokalen
`/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19/GIT_ABSCHLUSS.json` und in der Codex-Abschlussantwort; ein Commit kann seinen
eigenen Hash nicht ohne zirkuläre Änderung enthalten.

Prüfung der GitHub-Grenzen vor Sicherung: normale Dateien <100 MiB, LFS-Free-Dateien
<2 GB; tatsächliche Nutzdaten getrennt im Indexnachweis. Quellen:
[GitHub Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github),
[Git LFS Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage).
Keine Kauf-, Budget-, Force-Push-, History-Rewrite- oder Prune-Aktion.

**Empfehlung:** Diesen begrenzten Heilhausbereich jetzt visuell abnehmen. Die Pflanzen
sind deutlich weniger flächig, Töpfe und Boden differenzierter. Keine automatische
Freigabe als endgültige Weltqualität, keine Performancefreigabe und keine Ausweitung
auf weitere Gebiete. Nach diesem Stand stoppen und Harrys Bewertung abwarten.
