# VisualV2 World Art Quality V6 – Prüfbericht

19.10.2026. **Drei bestehende Musterbereiche und ihre angrenzenden Wege verfeinert, technisch geprüft. Visuelle Freigabe durch Harry offen. Nach diesem Stand stoppen.**

## 1. Ausgangsstand und Schutz

- Schlanker Worktree: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`, Branch `codex/slim-backup-v5`.
- Vor Beginn direkt abgefragtes GitHub-`origin/main` und lokaler HEAD: `8725ca992b8832701da61621799b34cf21f936ff`, gesicherter V5-Stand.
- AGENTS, GRAFIKSTIL, relevante TECHNIK-/ENTSCHEIDUNGEN-Abschnitte, SPIELIDEE, SPIELREGELN und vollständige V4-/V5-Artberichte sowie die tatsächlichen V5-Werkzeuge und Wegquellen gelesen.
- Ausschließlich bestehende Karte `/Game/Maps/Dev_TestMap_VisualV2`, Datei `Content/Maps/Dev_TestMap_VisualV2.umap`. **Keine neue Map.**
- Aktuelle V5-Kartendatei vor jeder Bearbeitung extern gesichert und SHA-256 geprüft: `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V6_2026-10-19/Dev_TestMap_VisualV2_Before.umap`. Hashes aller 17 bestehenden Karten in `InitialState.json` dort.
- Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b`, lokales `main` und `refs/archive/pokemonster/full-backup-03492bd` unverändert; Backup kein Vorfahr des schlanken Zweigs.
- Keine offene Unreal-Sitzung bei Beginn. Fremde Blender-Sitzung unverändert erhalten; keine neuen Blenderdateien nötig. Eigene Editorprozesse sauber geöffnet und ohne offene Pakete regulär geschlossen. Kein Save All, Verwerfen, Reset oder Force Quit.
- Drei bereits vorhandene fremde/unzugeordnete unversionierte Einträge vollständig erhalten und von Staging ausgeschlossen: `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap`, `Tools/VisualV2EnvironmentQualityV1/`, `Tools/VisualV2QualityV2/__pycache__/`.

Die drei V5-Muster sind die gesicherte Ausgangsbasis; dieser V6-Auftrag erlaubt deren Überarbeitung, ist aber keine nachträglich behauptete allgemeine Stilfreigabe. Heilhaus V4 bleibt die vorhandene Qualitätsreferenz und wird nicht umgestaltet.

## 2. Sichtbare Wege verbessern, vorhandene Funktion erhalten

Die vorhandenen kollisionsfreien Wegbänder liegen über dem unveränderten begehbaren Boden. Ihre sichtbare Gestaltung wird mit drei **privaten Materialkopien** verändert, nicht durch Verschieben oder Neuaufbau ihrer Meshes.

- Leicht wechselnde sichtbare Breiten, unregelmäßige Säume und örtlich weiter auslaufender Anschluss an der vorhandenen Wiesenwegkreuzung.
- Laufkern als erkennbare festgetretene Erde; kleine Steine und breitere Materialstrukturen aus der vorhandenen V4-Erdfamilie statt ausschließlich der gleichförmigen feinen Orangefläche.
- Waldweg: gedämpftere Erde mit Laub-/Moosbezug am Rand; Wiesenweg: trockenere, etwas wärmere Erde mit Klee-/Grassäumen; Uferweg: gedeckter, kiesiger und feuchter.
- Zweite gedrehte Texturabfrage, unregelmäßig versetzte Weltkoordinaten und größere Makrovariation reduzieren erkennbare Wiederholung. Kein neues Texture-Set oder zusätzlicher Decal-Stapel.
- Einzelne niedrige Gras-, Moos- und Kleegruppen wachsen in die äußeren Säume hinein. Kleine Kieselgruppen werden stellenweise an der Wegschulter platziert. Der zentrale Laufbereich bleibt frei; keine neue Collision oder Navigationsregel.

### Umsetzung und räumliche Begrenzung

`RouteField.json` leitet sich aus den tatsächlich vorhandenen Punkten und der bestehenden **16-Schritt-Catmull-Rom-Abtastung** in `Tools/ModernizeDevTestMapVisualV2.py` ab. 73 ausgewählte kurze Distanzsegmente: 21 Main, 16 VillageLoop, 36 NorthLoop; Wildpfad nicht neu gestaltet. Maximale gemessene Abweichung der vereinfachten Mittellinie von den ursprünglichen Wegmesh-Samples unter **4 cm**. Das ist ein Autoren-Distanzfeld für Farbe/Opacity, keine veränderte Weggeometrie oder neue Navigation.

Regional begrenzte Masken entsprechen den drei V5-Mustern: Wald etwa 21,6 × 12,8 m, Wiese 16 × 11,4 m, Ufer 19 × 9,6 m. Hinzu kommt nur die unmittelbar angrenzende vorhandene Wiesenwegkreuzung um X/Y **(-1310, -1850) cm**, weich auslaufende Ellipse ungefähr 8 × 6 m. Keine weitere Siedlung oder andere Mapregion bearbeitet. Der direkte Brückenbereich ist ausdrücklich ausgenommen; außerhalb der örtlichen Masken bleiben die vorherigen Materialausgaben Grundlage.

Material-Halbbreiten beginnen bei 112 cm für NorthLoop, 127 cm für VillageLoop und 122 cm für Main, mit örtlicher niederfrequenter Variation und zusätzlicher Aufweitung am Anschluss. Diese Werte beschreiben die **sichtbare Materialmaske**, nicht die unveränderte Boden-/Wegkollision. Keine grundlegende Änderung von Wegeführung oder Laufrichtung.

## 3. Wald, Wiese und Ufer

| Bereich | Tatsächliche Überarbeitung |
|---|---|
| Wald | Farnfamilien und Unterholz stärker in verschieden große Taschen konzentriert; Moos zwischen Gruppen, ruhigere freie Bodenstellen, weniger gleichmäßige Verteilung. Laubkoordinaten verzerrt und verschieden skaliert, Moos-/Erdanteile örtlich variiert; harmonischerer Auslauf zum Waldweg. |
| Wiese | Unterschiedlich hohe und breite Grasbüschel, größere zusammenhängende Pflanzentaschen sowie kleinere Blüten-/Kleeinseln. Bewusst offene Flächen dazwischen; leicht wechselnde Grün-/Gelbtöne. Einige niedrige Ausläufer an der Wegkante. |
| Flussufer | Unterschiedlich dichte Schilf-/Grasgruppen statt gleichmäßiger Säume, offene Kiesbuchten, feuchte Erde und einzelne Steine. Landseitige Materialkontur unregelmäßiger. Vorhandene Wasser-Opacity und tatsächlicher Flussverlauf unverändert. |

Es werden **399 bestehende Instanzen in 16 der 17 V5-HISM-Gruppen neu angeordnet**. Acht vorhandene Wurzelinstanzen bleiben unverändert; insgesamt weiterhin **407 Instanzen**. Kein Baum, Gebäude, NPC oder Gameplayobjekt verschoben. Keine zusätzlichen Akteure und keine entfernten Instanzen.

| Bereich | Erhaltene Gesamtzahl | Neu angeordnet |
|---|---:|---:|
| Wald | 130 | 122; 8 Wurzeln unverändert |
| Wiese | 156 | 156 |
| Flussufer | 121 | 121 |
| Summe | **407** | **399** |

Meshes, Materialbindungen, Komponenten-/Actor-Identitäten, NoCollision, bisherige Schattenflags und Culling bleiben erhalten. Nur Einzeltransformationen der klar getaggten V5-Dekorationsgruppen ändern sich. Größen wurden mit den tatsächlichen V4-/V5-Pflanzenmaßen abgestimmt; keine pauschal mannshohen Grasblätter. Bestehende Interaktionspunkte, Brückenzugang und Bewegungsroute werden bei der Platzierung ausgespart.

## 4. Neue und wiederverwendete Dateien

**Keine neuen Meshes, Texturen oder Blenderquellen.** V4-/V5-Blenderdateien, FBX-Importquellen, Texturen und Originalmaterialien unverändert wiederverwendet. Keine künstlerische Vereinfachung oder Polygonreduktion zur Leistungssteigerung.

Nur drei neue Unreal-Assets:

- `/Game/Environment/VisualV2WorldArtV6/Materials/M_WA6_Ground`
- `/Game/Environment/VisualV2WorldArtV6/Materials/M_WA6_NorthPath`
- `/Game/Environment/VisualV2WorldArtV6/Materials/M_WA6_MainPath`

Reproduzierbare Eingaben unter `Art/World/VisualV2WorldArtV6/`:

- `RouteField.json` und `RouteField.hlsl`: tatsächliche Wegableitung, räumliche Masken und Materialkonturen.
- `SurfaceColor.hlsl`: Oberflächen-/Erdfarbübertragung mit den bestehenden Texturen.
- `AssetManifest.json`: ursprüngliche und neue Custom-Graphen einschließlich Opacity.
- `Scope.json`: vier Materialbindungen und alle neu angeordneten Einzeltransformationen, Mengen und Identitäten.

Autoren-, Aufnahme- und Prüfwerkzeuge mit README unter `Tools/VisualV2WorldArtV6/`. Keine Gameplay-C++-/Blueprint-Änderung. Die Autorenwerkzeuge verweigern ein erneutes Umgestalten der bereits fertigen Karte; Material-Wiederaufnahme nur innerhalb der ausdrücklich markierten eigenen unvollständigen Sitzung. Kein Überschreiben unbekannter Arbeit.

## 5. Erhaltener Projektzustand

- Vorher und nachher **1.374 erfasste Szenenakteure**. Keine hinzugefügt oder gelöscht.
- Genau vier Akteure ändern nur ihre Materialbindung: `V2_Ground`, `V2_Path_Main`, `V2_Path_NorthLoop`, `V2_Path_VillageLoop`.
- Genau 16 V5-Dekorationsakteure ändern nur Instanztransformationen. Die übrigen **1.354 vorhandenen Akteure** stimmen in den erfassten Signaturen vollständig mit V5 überein.
- Alle vorhandenen Wege-Meshes, Bäume, Wasser, Brücke, Gebäude, Boden-/Gameplaykollisionen und Actor-Referenzen unverändert. Keine neue begehbare Höhenstufe.
- Unveränderte Licht-/PP-Einstellungen, Originalschatten, Lumen, Bloom, TAA sowie Kamera B **2850 cm / Pitch -50° / Yaw -45° / FOV 35°**. Keine experimentelle AA- oder Lichtvariante integriert.
- Player 140 cm, Gehen 210 cm/s, Sprint 315 cm/s, Animationen, Steuerung und Spielregeln unverändert.
- Alle **16 anderen Mapdateien SHA-256-identisch**. Keine neue Map und keine Änderung am Vollbackup.
- Gespeicherte VisualV2 frisch geöffnet und gegen den geprüften Szenensnapshot verglichen; identischer Stand. Keine offenen Map-/Contentpakete beim regulären Schließen.

Der Audit prüft die tatsächlich exponierten Actor-/Komponenteneigenschaften und vollständigen Postprocess-Texte; keine Behauptung, jedes interne Enginefeld auszulesen. Git-Dateiprüfung bestätigt zusätzlich keine Änderung an bestehenden gemeinsamen Assets oder Gameplaydateien.

## 6. Echte QHD-Vergleiche

**40 finale Originalaufnahmen**: fünf feste Ansichten × Vorher/Nachher × Medium/High × eingebetteter PIE/nativer Standalone-`-game`-Betrieb. Ausgabe-PNGs und tatsächlicher Spielviewport jeweils **2560 × 1440**, Primary und Secondary Screen Percentage 100 %, DynamicRes 0. Kamera, Rotation, FOV und Playerposition pro Paar aus den tatsächlichen Metadaten verglichen, Toleranz unter 0,02 cm/Grad. Gleiches Qualitätsniveau auf beiden Seiten, keine Lichtänderungen.

| Ansicht | Player X/Y in cm |
|---|---|
| Waldweg / Waldboden | -3300 / 2050 |
| Wiesenweg / Vegetation | -2100 / -1760 |
| Uferweg / Flussufer | -350 / -130 |
| Angrenzende Wegkreuzung | -1640 / -1840 |
| Heilhaus-Kontrolle | -4100 / 450 |

Der erste Kreuzungs-Fotostandpunkt war von einer bestehenden Baumkrone verdeckt. Vor Beginn der Kartengestaltung wurde deshalb seitlich ein besserer Standort gewählt und die komplette finale Vorherreihe neu aufgenommen. **Nur `BeforeFinal2` gegen `AfterFinal`** ist der endgültige Vergleich; vorläufige Serien bleiben als lokale Arbeitsnachweise erhalten, gelten aber nicht als finale Referenz.

- Originale: `Saved/VisualV2WorldArtV6/Photos/{PIE|Standalone}_Q{1|2}_{BeforeFinal2|AfterFinal}_2560_1440/`.
- Dauerhafte bytegleiche Kopie aller Originale und Metadaten außerhalb von Git: `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V6_2026-10-19/Originals/`, Prüfsummen in `OriginalsSHA256.json`.
- **36 Vergleichstafeln**: 20 vollständige Ansichtsvergleiche und 16 Originalpixel-Detailvergleiche. `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V6_2026-10-19/Comparisons/Manifest.json` listet alle Bildpfade, Originale und Ausschnitte.
- Haupttafeln dort: `PIE_Q2_Wald_BeforeAfter.png`, `PIE_Q2_Wiese_BeforeAfter.png`, `PIE_Q2_Flussufer_BeforeAfter.png`, `PIE_Q2_Kreuzung_BeforeAfter.png`; Details jeweils `*_GroundDetail.png`. Medium und Standalone entsprechend ebenfalls vorhanden.

Alle Bilder stammen aus Unreal. Nur Beschriftung, gleichmäßige Bildverkleinerung und unveränderte Originalpixel-Ausschnitte; keine Retusche, Konzeptbilder oder synthetischen Spielnachweise. Foto-Positionssetzung zur Reproduzierbarkeit ist ausdrücklich vom echten Gameplay-Fußlauf ohne Test-Teleports getrennt. Standalone ist nativer Development-`-game`-Start, **kein Shipping-Cook**.

## 7. Tatsächliche Tests

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build / UE 5.8.2 | erfolgreich, Exit 0; kein C++ geändert |
| Vollständige Projekt-Automation | **49/49 erfolgreich**, 0 mit Warnungen, 0 fehlgeschlagen, 0 ausgelassen |
| Map Check nach frischem Laden | **0 Fehler / 0 Warnungen** |
| Persistierter Szenenstand | exakt gleich dem geprüften Nachher-Snapshot |
| Wegfeld-Autorenquelle | aus den vorhandenen Kurven erneut erzeugt, JSON und HLSL bytegleich; externer Nachweis RouteFieldReproduction.json |
| Drei finale Materialgraphen | alle Custom-Eingänge verbunden, wiederverwendete Erdquelle korrekt, gespeicherte Graphen entsprechen Manifest |
| Finale native Shader-/Materialdarstellung | Medium und High ohne neue Kompilierungs-/Fallbackfehler, keine grauen V6-Flächen |
| Vollständiger Gameplay-Fußlauf | **102 Schritte, 284,39 m**, echte Enhanced-Input-Bewegung im gerenderten eingebetteten PIE, keine Test-Teleports |
| Gehen, acht Richtungen, Anhalten, Sprint | erfolgreich; unveränderter maximaler Sprint 315 cm/s |
| Wanderer-/Liora-Dialoge, Quest, Archiv, Menü | erfolgreich |
| Wildkampf, Fang und Trainerkampf | erfolgreich |
| Brücke / neue Wegsäume / Waldpassage | durchlaufen; keine neue Blockade festgestellt |
| Heilhaus / Heilung / PP / Checkpoint | erfolgreich, einschließlich gerader und diagonaler Ein-/Ausgänge sowie Cutaway |
| Save/Load | erfolgreich; vorher kein Dev-Slot, ursprüngliche Abwesenheit wiederhergestellt; Testresultat separat erhalten |
| Kronenfreistellung / NPC-Sprite-Fallback | bestehende Prüfroute erfolgreich |
| QHD Medium/High, PIE/Standalone | reale finale Bildserien vorhanden und verglichen |
| FPS-/GPU-Benchmarks | **nicht durchgeführt**, gemäß Art Quality First |

Fußlauf: 179,11 Spielsekunden / 203,13 Wandsekunden; Ablaufzeiten, keine FPS-Messung. Die routegesteuerte Prüfung ist keine behauptete manuelle Nutzerabnahme. Kein zweiter vollständiger Standalone-Fußlauf, physischer Controllertest oder Shipping-Cook behauptet.

## 8. Aufgetretene Fehler und verbleibende Grenzen

- Der erste private Materialaufbau stoppte an einer Schutzprüfung, weil der Boden-Graph einen anderen finalen Mode-Return als die Weggraphen besitzt. Anschließend wurde ein Unterschied zwischen Unreal-Objektpfad und Paketpfad in der Wiederaufnahmeprüfung abgefangen. Beide Fälle betrafen ausschließlich die neu erstellte eigene Materialkopie; die Karte war dabei noch unverändert. Ursachen gezielt korrigiert, keine Originaldateien verworfen oder zurückgesetzt.
- Während des schrittweisen Aufbaus erschienen vor vollständiger Pin-Verbindung vorübergehend `Custom missing input W6Earth`-/Defaultmaterial-Meldungen. Finale Eingänge sind tatsächlich verbunden. In den anschließend frisch gestarteten nativen Nachherprozessen **0 Material-Kompilierungsfehler**; kein Fehler unterdrückt oder allein auf Basis eines Skript-Exitcodes als behoben erklärt.
- Eine lokale Git-Statusabfrage im eingeschränkten Dateisystem konnte nicht in den gemeinsamen LFS-Temporärordner schreiben. Mit autorisiertem Zugriff erfolgreich wiederholt; kein Pushfehler, keine erneute Übertragung und keine beschädigten Objekte.
- Native Engine-Toolset-Startdiagnosen bleiben wie vorher: je Qualitätsstufe 58 Python-Fehlerzeilen, dieselben 47 normalisierten Fingerprints vor/nach V6 (u. a. experimentelle Toolsets mit fehlender `ToolsetDefinition`/`PythonTestRunner`). Kein neuer Fingerprint. Vorhandene macOS-`idevice_id`-/Audio-/Startdiagnosen bleiben getrennt von den 49 erfolgreichen Projekt-Automationstests dokumentiert.
- Wegvariation ist sichtbar, bleibt aber ein Materialpass auf den vorhandenen Kurven. Keine vollständige individuelle Handmodellierung jedes Wegmeters; einzelne Abschnitte können weiterhin bandartig wirken.
- Die wiederverwendeten Bodenalbedos bleiben gekachelt. Verzerrung und gemischte Skalen reduzieren, beseitigen aber nicht jede erkennbare Wiederholung.
- Dichter Kronenschatten lässt einige Uferpflanzen und Waldpartien weiterhin sehr dunkel erscheinen. Keine Aufhellung, emissiven Pflanzen oder Änderung der Originalschatten vorgenommen.
- Reale Wasser-/Brückengeometrie unverändert; der Fluss bleibt im Grundriss entsprechend gerade. Organische Uferkontur entsteht landseitig durch Kies, Material und Pflanzen. Keine unzutreffende neue Bachmodellierung behauptet.
- Kleine Einzelpflanzen bleiben aus normaler Spielentfernung teilweise zurückhaltend. Einige vorhandene runde Strauchformen und das schlichte Brückenaussehen bleiben Qualitätsgrenzen außerhalb dieses Auftrags.
- Das neue räumliche Materialfeld fügt Rechenarbeit hinzu. Keine Aussage über zusätzliche GPU-Zeit oder einen FPS-Gewinn, keine automatische Performancefreigabe. Auch kein globaler Vegetations-/Schattenabbau.

**Empfehlung:** V6 anhand der vier echten QHD-Vergleiche visuell abnehmen: Waldweg-Laubauslauf, Wiesen-Gruppengrößen, offene Kiesbuchten und unterschiedliche Breiten an der Kreuzung. Nach den drei Mustern stoppen; keine weitere Mapfläche automatisch übernehmen.

## 9. GitHub-Sicherung

Nur neue V6-Materialien, reproduzierbare Autoren-/Prüfwerkzeuge, nötige Konfigurationsdaten, zentrale Karte und bestätigte Dokumentation sichern. **Keine Vergleichsbilder, Videos, Saved-Ausgaben, Renderings oder anderen Kontrollmedien hochladen.** Keine neue LFS-Regel erforderlich; vorhandene `.uasset`-/`.umap`-Regeln gelten.

Zwei logische Sicherungsschritte: (1) drei private Materialassets mit Autorenquellen und Werkzeugen; (2) begrenzter Kartenstand mit Prüfbericht und bestätigter Dokumentation. Vor jedem Commit vollständige explizite Indexliste, `git diff --cached --check`, LFS-Pointer, lokale Objekt-SHA-256 und Dateigrößen kontrollieren. Vor jedem regulären Push `origin/main` direkt prüfen; danach Remote-Commit und alle neu gesicherten LFS-Dateien unabhängig lesen und SHA-256 vergleichen. Bei Fehler stoppen; kein Force-Push, Kauf, Budgetwechsel oder Prune.

[GitHub-Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) und [LFS-Einzeldateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) am 19.10.2026 frisch geprüft: 100 MiB normale Git-Dateigrenze, konservative 2-GB-LFS-Dateiprüfung. Beide normalen Git-Pushes bleiben deutlich unter 1 GiB; LFS-Payload getrennt erfasst. Kein behaupteter Abruf der Kontobilling-Anzeige, keine kostenpflichtige Aktion.

Die tatsächlichen beiden Commit-Hashes, Push-Ergebnisse, unabhängig bestätigte LFS-Objektbytes und der endgültige Git-Status werden nach Abschluss in `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V6_2026-10-19/GIT_ABSCHLUSS.json` festgehalten und in der Abschlussantwort genannt. Keine Push-Behauptung vor dessen Durchführung. Technische Nachweise: `InitialState.json`, `FinalEvidence.json`, `QA/` und `Comparisons/Manifest.json` im selben externen Ergebnisordner.
