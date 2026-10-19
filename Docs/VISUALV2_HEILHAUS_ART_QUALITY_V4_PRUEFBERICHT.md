# VisualV2 Heilhaus Art Quality V4 – Prüfbericht

Datum: 19.10.2026. **Begrenzter Stand zur visuellen Abnahme. Keine automatische Weltstilfreigabe.**

## 1. Ausgangsstand und Schutz

- Schlanker Worktree `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`, Branch `codex/slim-backup-v5`.
- Ausgangs-HEAD und vor Arbeitsbeginn direkt geprüftes origin/main: `86685a660f3a0b55f90c8d557b8becf136069b7b`.
- AGENTS, GRAFIKSTIL, TECHNIK, ENTSCHEIDUNGEN, SPIELIDEE, SPIELREGELN und V3-Heilhausbericht gelesen.
- Karte: **`/Game/Maps/Dev_TestMap_VisualV2`**, Datei `Content/Maps/Dev_TestMap_VisualV2.umap`.
- **Keine neue Map.** 16 andere vorhandene Maps per SHA-256 unverändert, einschließlich WestlandRegion, WestlandAssetLibrary und aller vorhandenen Performance-/NPC-Testkarten.
- Lokaler main und Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` unverändert; kein Vorfahr des schlanken Zweigs.
- Vorherdatei extern gesichert: `/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/Dev_TestMap_VisualV2_Before.umap`, SHA-256 `d5631233ff719377d966752f7dcf2931886b51e5b91ef6bef6d86cb8fd93429a`.
- Zusätzlich eigener V4-Zwischenstand vor der letzten Fensterkorrektur extern gesichert. Keine Originalquelle überschrieben.
- Bereits unversionierte fremde Arbeit erhalten und von Staging ausgeschlossen: `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap`, `Tools/VisualV2EnvironmentQualityV1/`, `Tools/VisualV2QualityV2/__pycache__/`.
- Geöffnete fremde Blender-Hobbit-Sitzung unverändert; eigene Quellen ausschließlich in separaten Blender-Hintergrundprozessen bearbeitet.

## 2. Tatsächlich verwendete Zielreferenz

Nutzeranlage `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Art/World/VisualV2HealingArtV4/References/Heilhaus_V4_UserTarget.jpg`, unveränderte Kopie der tatsächlich zugänglichen Anlage `1-Foto-1.jpg`.
Die **rechte Bildhälfte** dient als Ziel für größere lesbare Oberflächen, organische Kräuter, reichere Hausmaterialien und dichtere örtliche Details. Diese Illustration ist **kein Unreal-Screenshot**.
Die Lichtstimmung des Konzepts wurde nicht durch neue Licht-/Belichtungswerte nachgebaut.

## 3. Boden und Wegsäume

Fünf bestehende Komponenten erhalten private V4-Graphen: V2_Ground, V2_House_Forecourt, V2_Path_VillageLoop, V2_Path_NorthLoop, V2_House_HH_Q2_OrganicApproach.

- Neue malerische Gras-/Klee- und Erd-Albedos mit deutlich größeren, lesbaren Strukturen statt vorwiegend feinem Korn.
- Neue Motive lokal über ungefähr **255 cm** Weltmaßstab; zusätzlicher gedrehter Grasanteil über 417 cm gegen sichtbare Wiederholung. Bestehende Koordinaten außerhalb des örtlichen Artbereichs bleiben Grundlage.
- Lokale Makrovariation und unregelmäßig versetzter, breiterer Auslauf; Grasanteile an Wegsäumen stärker differenziert.
- Wirkungsbereich ungefähr X −4660…−3530, Y −755…1220 cm einschließlich unregelmäßiger Ausläufe. Keine flächige Übertragung auf die restliche Karte.
- Zusätzliche Kräuter, gekrümmte Grasbüschel, zurückhaltende Blüten und flache unregelmäßige Vorplatzsteine.
- Vier neue HISM-Gruppen: **72 GrassTuft, 18 GardenHerb, 12 GardenFlowers, 45 Flagstone = 147 Instanzen**.
- Bisherige 175 kleinen HISM-Vegetationsinstanzen einschließlich ihrer Transformationen unverändert.
- Geschützter Laufkorridor ungefähr 2,7 m; neue Details NoCollision. Die flachen Steinakzente sind keine neue Treppe und verändern keine Boden-/Wegekollision.
- Keine zusätzlichen Decal-Stapel oder neuen Material-Layer. Der Graph ist ein Qualitätspass, keine nachgewiesene Shaderoptimierung.

## 4. Topfpflanzen und Fensterdekoration

Fünf eigenständige botanische Varianten, vorhandene handgeformte Q3-Keramik erhalten. Ungleiche Blattgrößen/-höhen, gezackte und gefaltete Konturen, sichtbare Verzweigungen, cremefarbene Blüten, violette Blütenähren und rankende Triebe. Vier gemeinsame botanische Materialfamilien. Echte Blattgeometrie statt großflächiger transparenter Blattkarten.

- **26 neuere Außentöpfe**: bestehende Position, Rotation, Skalierung, Actor-Identität, Kollision und Schattenflags erhalten.
- Detailkontrolle fand zusätzlich **acht ältere Fensterpflanzen** mit sichtbaren ovalen Grundkörpern. Ihre reine Dekorationsherkunft ist in `Tools/DressHealingHouseV3.py`, Funktion `pot`, Abschnitt WindowHerb dokumentiert. Alle betroffenen Komponenten waren NoCollision/NoShadow.
- Acht Zylinder-Topf-Actor erhalten vollständige V4-Pflanzen. X/Y-Position bleiben gleich; der neue Bodenursprung wird auf die ursprüngliche Topfunterkante Z=105 cm gesetzt, entsprechend **−6,48 cm** gegenüber dem alten Zylinderzentrum. Einheitliche lokale Skalierung 0,42, damit Topfdurchmesser zum bisherigen Fensterkasten passt.
- **28 alte Blatt-/Blütenteile** verbleiben vollständig als unsichtbare Komponenten in der Karte. Nicht gelöscht; ursprüngliche Bindungen und Transformationen in Scope.json. Keine Gameplay- oder Cutaway-Identität entfernt.
- Zusätzliche echte PIE-Sichtprüfung bestätigt 28 unsichtbare alte Komponenten und acht vorhandene neue Fensterpflanzen. Der Gebäude-Cutaway verändert Actor-Hidden-Zustände, nicht die hier gespeicherte Komponenten-Sichtbarkeit.

## 5. Heilhausmaterialien und Fassade

Private Varianten für **Holz, dunkles Tragholz, Putz, Stein/Sockel und Dach**. Bestehende Gebäude-/Fenster-/Tür-/Sockelmeshes und ihre Form unverändert. Nur örtliche Materialbindungen; Originale bleiben verfügbar. Innenraum-/Floor-/InteriorStone-Objekte ausgenommen.

- Neue gemalte Eichenholzquelle: erkennbare Maserung und Holzfarbvariation für Fensterrahmen, Balken und Türflächen.
- Vorhandene Putz- und Steinbildquellen erneut verwendet, mit breiterer Materialvariation, dezenter Rauheit und zurückhaltender Oberflächenreaktion.
- Dach behält seine echte vorhandene Geometrie; versetzte Fugen, individuelle Ziegelfarbvariation und dezente Moosanteile werden im privaten Material lesbarer.
- Sehr dezente Bump-Reaktion aus der jeweiligen gemalten Oberfläche; kein vollständiges neu gebackenes PBR-Texturset behauptet.
- **14 bisher perlenartige Fassadenranken** erhalten zwei organische Efeu-Sprays. Actor-Position/Rotation/Skalierung bleiben gleich.
- Erste dünne Blätter lagen zu weit hinter der alten Außenkante und waren in bestehendem Licht zu dunkel. Nur eigene Blattgeometrie um unter der vorhandenen Skalierung 3,5 cm nach außen versetzt, Normalen nach außen gerichtet und Blätter nach oben geneigt. Kein Licht aufgehellt, keine emissive Pflanzenlösung.
- Bestehender **HouseCutaway**-Mechanismus und Materialmasken erhalten.

## 6. Quellen, Texturen und tatsächliche Geometrie

Neue Quellen:

- `Art/World/VisualV2HealingArtV4/Source/HealingHouse_PottedPlants_V4.blend`
- `Art/World/VisualV2HealingArtV4/Source/HealingHouse_GardenDetails_V4.blend`
- Elf getrennte benötigte FBX-Importquellen unter `Art/World/VisualV2HealingArtV4/Exports/`.
- Unreal-Varianten ausschließlich unter `/Game/Environment/VisualV2HealingArtV4/`.

Drei neue Albedoquellen Meadow/Earth/Wood, tatsächlich **1254 × 1254 Pixel**. Unreal-Zweierpotenzimport maximal 2048² ist keine native 2K-Quelle. Erzeugt mit eingebautem Imagegen; vollständige Prompts, Herkunft und Modus in `Art/World/VisualV2HealingArtV4/TexturePrompts.json`. Bestehende Terracotta-/Putz-/Steintexturen erhalten. Keine gebackene Studiobeleuchtung beabsichtigt.

| Meshfamilie | Gemessene Dreiecke LOD0 | Abschnitte | Materialslots |
| --- | ---: | ---: | ---: |
| BroadHerb | 9,364 | 4 | 4 |
| NarrowHerb | 34,320 | 4 | 4 |
| LeafPlant | 6,332 | 3 | 3 |
| FlowerPlant | 24,172 | 4 | 4 |
| TrailingHerb | 5,300 | 3 | 3 |
| GardenHerb | 8,708 | 2 | 2 |
| GardenFlowers | 23,516 | 2 | 2 |
| GrassTuft | 1,056 | 1 | 1 |
| IvySprigA | 180 | 1 | 1 |
| IvySprigB | 180 | 1 | 1 |
| Flagstone | 50 | 1 | 1 |

Elf einzigartige Meshes zusammen **113,178 Dreiecke**. Das sind Meshdaten, keine gemessenen GPU-/Draw-Call-Kosten.
Die 34 platzierten Töpfe können zusammen 627.704 Dreiecke bei vollständig dargestelltem LOD0 beanspruchen; neue HISM-Details zusammen 517.218. Kein Sichtbarkeits-/LOD-Abzug und keine Performancebehauptung. Die höhere botanische Detailmenge ist Teil des Art-Auftrags; kein Ressourcenverbrauch als kostenlos dargestellt.

Beide Blenderdateien gespeichert und erneut geöffnet; gepackte benötigte Bildquelle vorhanden. Finale Prüfungen: keine gefundenen Nullflächen, Nullnormalen, nicht endlichen Vertices oder degenerierten UV-Dreiecke. Offene dünne Blattflächen sind beabsichtigt. Unreal-Reimport, Dreieckzahlen, Maße mit <0,05 cm Toleranz, Materialbindung und **0 einfache Kollisionsformen** für alle elf Meshes geprüft. Zwei Efeu-Reimporte betreffen ausschließlich eigene Varianten.

## 7. Geschützter Szenenbestand

- Vorher 1353, nachher 1357 auditierte Actor, vier neue Dekorationsgruppen.
- **116** bestehende Actor gezielt geändert: 80 erste Bindungen und 36 ältere Fensterdekorationsteile.
- **1237** andere Actor-Signaturen vollständig unverändert im verwendeten Audit.
- Keine ursprünglichen Actor gelöscht. Nur geprüfte Bindungen, die acht dekorativen Topfursprünge/-skalierungen sowie Sichtbarkeit der 28 alten Dekorationsteile angepasst.
- Welt-/Postprocess-Signaturen unverändert. Lichtquellen und deren Parameter nicht bearbeitet.
- **Schatten, Lumen, Bloom, TAA und Kamera unverändert.** Kamera B: 2850 cm / Pitch −50° / Yaw −45° / FOV 35°.
- Player 140 cm, Gehen 210 cm/s, Sprint 315 cm/s, Collision Capsule, Eingabe, Animationen, Dialog-/Quest-/Speicherlogik unverändert.
- Alle Zusatzdetails kollisionsfrei, ohne zusätzlichen Schattenwurf und ohne dynamischen Tick. Gebäude-/Originalschattenflags unverändert.
- Der Audit prüft exponierte Actor-/Komponenteneigenschaften und vollständige Postprocess-Texte; er ist keine Behauptung, jedes Engine-interne Feld auszulesen.

## 8. Echte Bildvergleiche

**80 finale Vergleichsaufnahmen**: fünf Fotopositionen × vorher/nachher × 720p/QHD × Medium/High × eingebettetes PIE/eigenständiges `-game`.

- Ausgabe **1280×720 und 2560×1440** anhand realer PNG-Größen und Viewportdaten geprüft.
- Primary **100 %**, Secondary **100 %**, Dynamic Resolution **0** auf beiden Vergleichsseiten.
- Kamera, Rotation, FOV und Playerposition pro Paar abgeglichen; maximal 0,02 cm Abweichung erlaubt.
- Gleiche Qualität je Paar; eine Qualität pro Editorprozess. Mindestens fünf Sekunden Einlauf je Fotoposition. Keine Leistungsmessung während dieser Aufnahmen.
- Rohbilder: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2HealingArtV4/Photos`. Interner letzter Batchname „Approved“ bezeichnet nur diese technische Bildreihe, **keine menschliche Artfreigabe**.
- Kein Shipping-Cook. Standalone bedeutet echter eigenständiger Unreal-`-game`-Prozess.
- Fotopositionierung verwendet Teleports ausschließlich zur Reproduzierbarkeit. Der getrennte Gameplay-Rundweg verwendet keine Testteleports.
- Vergleichsboards beschriften echte Bilder; identisch skaliert oder unveränderte Originalpixel-Ausschnitte. Keine Retusche und keine synthetischen Bilder als Spielnachweis.

Wichtige QHD-High/PIE-Vergleiche:

- [Gesamteindruck](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/Comparisons/PIE_Q2_Heilhaus_BeforeAfter.png)
- [Vorplatz](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/Comparisons/PIE_Q2_Vorplatz_BeforeAfter.png)
- [Wegsaum](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/Comparisons/PIE_Q2_Wegsaum_BeforeAfter.png)
- [Boden – Detail](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/Comparisons/Heilhaus_Boden_Detailvergleich.png)
- [Topfpflanzen – Detail](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/Comparisons/Vorplatz_Topfpflanzen_Detailvergleich.png)
- [Fassade – Detail](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/Comparisons/Heilhaus_Holz,_Detailvergleich.png)

Alle Paar-/Ausschnittmanifeste unter `/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/Comparisons`. Kontrollmedien bleiben lokal und werden nicht hochgeladen.

## 9. Technische und Gameplay-Ergebnisse

| Prüfung am endgültigen Stand | Ergebnis |
| --- | --- |
| Mac Development Editor Build, CompleteBuild | Exit 0 |
| Vollständige Projekt-Automation, CompleteAutomation | **49/49 erfolgreich**, 0 mit Warnungen, 0 fehlgeschlagen, 0 ausgelassen |
| Gespeicherte Karte frisch öffnen / Signatur vergleichen | erfolgreich |
| Map Check, CompleteMapCheck | **0 Fehler / 0 Warnungen** |
| Zwei Blenderquellen erneut öffnen / UV-/Geometrieprüfung | erfolgreich |
| Elf Unreal-Meshes / Maßstab / Materialien / Kollisionsformen | erfolgreich |
| Eingebetteter PIE-Fußlauf | **102 Schritte, 283.75 m**, ohne Testteleports, erfolgreich |
| Laufen / acht Richtungen / Anhalten / Sprint | geprüft; maximal 315 cm/s |
| Wanderer / Liora / Dialog / Quest / Archiv / Menü | vorhandener Testablauf erfolgreich |
| Wildfang und Trainerkampf | erfolgreich |
| Heilhaus, gerade und diagonale Ein-/Austritte / Heilung / Checkpoint | erfolgreich |
| Save/Load | erfolgreich; ursprüngliche Abwesenheit des Dev-Slots wiederhergestellt |
| Kronenfreistellung / NPC-Sprite-Fallback | erfolgreich |
| Alte Fenstergrundkörper in frischem eingebettetem PIE unsichtbar | 28/28, neue Pflanzen 8/8 |
| Medium/High, 720p/QHD, PIE/Standalone | echte finale Bilder geprüft |
| Finaler nativer Material-/Shaderfallback / Normalenwarnungen | kein neuer Material-/Shaderfallback festgestellt |
| FPS-/GPU-Benchmarks | **nicht durchgeführt**, gemäß Art Quality First |
| Physischer Controller / Shipping-Cook | nicht geprüft |

Fußlauf: 181.27 Spielsekunden, 202.17 Wandsekunden. Das sind Ablaufzeiten, keine FPS-Messung. Standalone wurde visuell geprüft; kein zweiter vollständiger Standalone-Gameplay-Rundweg behauptet.

## 10. Fehler, Korrekturen und offene Qualität

- Der erste Materialauslauf war zu gleichmäßig, und das dominante Grasmotiv wiederholte sich sichtbar. Breiteren unregelmäßigen Auslauf und gedrehten zweiten Motivanteil geprüft und übernommen.
- Flache Efeublätter zunächst zu dunkel/zu weit in der Fassade: tatsächliche Geometrie-/Normalenkorrektur, keine Lichtänderung.
- Acht alte Fensterpflanzen erst in den Detailausschnitten erkannt und gezielt korrigiert; abschließende Build-/Automation-/Map-Check-Prüfungen danach erneut durchgeführt.
- Ein ergänzender Sichtprüf-Aufruf traf unmittelbar nach Ende des Fußlaufs auf bereits beendetes PIE und brach ohne Änderung ab. In einer frischen eingebetteten PIE-Sitzung erneut tatsächlich durchgeführt; keine Laufzeitprüfung allein aufgrund dieses fehlgeschlagenen Aufrufs behauptet.
- Ein Git-Diff-Aufruf im eingeschränkten Dateisystem konnte nicht in den gemeinsamen LFS-Temporärspeicher schreiben. Mit autorisiertem Zugriff erfolgreich wiederholt; kein Daten-/Pointerdefekt und kein Reset.
- Bekannte Engine-Toolset-Startfehler bleiben: native Vorher-/Nachher-Logs haben dieselben Python-Fehlersignaturen, keine neue Signatur. Allgemeine vorhandene `Condition failed`-Startmeldungen sind nicht mit den separat exportierten 49 erfolgreichen Projekttests verwechselt.
- Vorhandene macOS-`idevice_id`-/Audio-/MCP-Startwarnungen bleiben. Nicht unterdrückt, vollständige lokale Logs erhalten.
- **Die Konzeptqualität ist noch nicht vollständig erreicht.** Boden ist weiterhin gekachelt; Übergänge können örtlich noch weich wirken. Einzelne vorhandene Grassorten bleiben kartig, einige Blatt-/Stängelaufbauten wirken noch regelmäßig. Die neue Pflanzendetailtiefe ist aus normaler Spielentfernung nur teilweise lesbar.
- Ziegelfugen und Materialvariation sind klarer, aber kein vollständig handbemaltes individuelles Gebäudemodell. Die unveränderte Beleuchtung lässt manche Fassaden-/Figurenpartien weiterhin dunkel erscheinen.
- Keine belastbare Aussage zu zusätzlicher GPU-/FPS-Last. Keine Abnahme für eine großflächige Übertragung.

## 11. GitHub-Sicherung

Zwei logische Schritte: neue private Artquellen/Assets/Werkzeuge und anschließend zentrale Kartenübernahme mit Bericht/bestätigter Dokumentation. Nur explizite Dateiliste, kein pauschales Staging. Die Nutzer-Konzeptreferenz und drei Material-Albedos sind benötigte Quellen; keine Kontrollscreenshots, Videos, temporären Renderings, Rohlogs oder Caches im Sicherungsumfang.

.blend, .fbx, .uasset, .umap sowie ausschließlich die neuen benötigten PNG-/JPG-Quellen werden per Git LFS verwaltet. Pointer, Quell-SHA-256, Größe und lokale Objektverfügbarkeit werden vor jedem Commit geprüft. GitHub-Dateigrenzen frisch gegen [normale Dateien](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) und [LFS-Dateien](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) geprüft. Normale Git-Nutzdaten weit unter 1 GiB je Push.

Art-/Werkzeug-Commit: `ec2ba2a7fe367810dd2e720e58817fbc5948e1ba`.

Die tatsächlichen Commit-Hashes, Push-Ausgänge, unabhängigen Remote-LFS-SHA-Prüfungen und der endgültige Git-Status stehen nach Abschluss in `/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19/GIT_ABSCHLUSS.json` und in der Codex-Abschlussantwort. Ein Commit kann seinen eigenen Hash nicht ohne zirkuläre Änderung enthalten. Keine Käufe/Budgetänderungen, kein Force-Push, kein History-Rewrite oder Prune.

**Empfehlung:** Den begrenzten Heilhausbereich anhand der echten QHD-Vergleiche jetzt visuell abnehmen. Größere lesbare Bodenstrukturen, Kräuterblüten, echte Efeukonturen und die Hausoberflächen sind verbessert; die vollständige Qualität der rechten Konzeptbildhälfte bleibt ein weiterer künstlerischer Maßstab. Nach diesem Stand stoppen. Keine Übertragung auf andere Gebiete ohne Harrys Freigabe.
