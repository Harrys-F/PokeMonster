# European Beech Forest V1 – Prüfbericht

Stand: 01.11.2026. Ausgangscommit `94f7d476598c03be7cf84bf0af5068f9758c2516`, Projekt `/Users/harry/Developer/PokeMonster`, Zielmap `/Game/Maps/Dev_TestMap_VisualV2`. Neue Waldsektion auf derselben Map. Keine neue Map, keine neuen Pflanzenmodelle, keine Gameplay-, Kamera- oder Renderingänderungen.

## Ergebnis und Zugang

Der neue Buchenwald ist am Nordrand über den bestehenden Nordweg erreichbar: vom Heilhausbereich über X≈−4300/Y≈1550 zum bisherigen Wegpunkt X≈−3300/Y≈2050 cm, dann **nach Norden** über X=−3300/Y=2350..3400 cm. Dort beginnt der sichtbare Erdweg.

Eigene Bodenfläche: **120 × 120 m**, X=−7500..4500, Y=3000..15000 cm. Der vorhandene Boden endet ungefähr bei Y=3250 cm; deshalb erhält der Zusatzbereich einen eigenen Boden mit 250 cm Überlappung und nur 0,2 cm Höhenversatz. Bestehende Bodenfläche, Wege, Gebäude und Lebensräume bleiben erhalten. Die ausgelagerten Innenräume um X≈16900/Y≈500 liegen außerhalb dieses Bereichs.

Der Wald enthält einen lockereren Waldrand, unregelmäßig verteilte größere Buchen und junge Bäume, einen geschwungenen Rundweg mit etwa **280 cm Breite**, eine kleine Lichtung bei X≈−400/Y≈8500 cm und einen Seitenpfad zum Totholzbereich bei X≈−5500/Y≈12100 cm. Keine neuen Spawns, NPCs oder Quests. Die äußeren Ränder bleiben die endlichen Ränder eines Testgeländes; keine neue großräumige Landschaft oder unsichtbare Randbarriere behauptet.

## Tatsächlicher Assetbestand

Originalpaket `/Game/Fab/EuropeanBeech`: **258 Dateien / 7.370.419.025 Bytes**. Enthalten sind 34 Static Meshes, 34 Foliage-Typen, 89 Materialinstanzen, 100 Texturen und eine bereits mitgelieferte Asset-Zoo-Map. Letztere wurde weder verwendet noch verändert und ist keine hier neu erstellte Testmap.

Zugehörige Materialbibliothek `/Game/MSPresets/MS_Foliage_Material`: 58 registrierte Assets, darunter 39 Materialfunktionen, 4 Materialien, 6 Materialinstanzen, 4 Editor-Icon-Meshes, 2 Texturen, 1 Parameter Collection, 1 Blueprint und 1 Redirector. Hinzu kommt die lokale Datenbank `Content/MSPresets/MSAssets.db`.

17 tatsächliche Baumformen liegen jeweils als SimpleWind- und PivotPainter-Version vor. SimpleWind unter `/Game/Fab/EuropeanBeech/Geometry/SimpleWind/`; PivotPainter unter `Geometry/PivotPainter/` mit Suffix `_PP`. Die Maße stammen aus Meshbounds einschließlich Blattkarten-/LOD-Rändern, nicht aus angenommenen botanischen Normgrößen.

| Mesh | Höhe der Bounds | LODs | Nanite konfiguriert |
|---|---:|---:|---|
| `SM_EuropeanBeech_Field_01` | 23.92m | 7 | ja |
| `SM_EuropeanBeech_Forest_01` | 48.47m | 7 | ja |
| `SM_EuropeanBeech_Forest_02` | 44.89m | 7 | ja |
| `SM_EuropeanBeech_Forest_03` | 32.80m | 7 | ja |
| `SM_EuropeanBeech_Forest_04` | 31.73m | 7 | ja |
| `SM_EuropeanBeech_Forest_05` | 25.30m | 7 | ja |
| `SM_EuropeanBeech_Forest_06` | 15.32m | 7 | ja |
| `SM_EuropeanBeech_Forest_07` | 14.31m | 7 | ja |
| `SM_EuropeanBeech_Forest_08` | 7.62m | 7 | ja |
| `SM_EuropeanBeech_Sapling_01` | 3.18m | 4 | ja |
| `SM_EuropeanBeech_Sapling_02` | 3.02m | 4 | ja |
| `SM_EuropeanBeech_Sapling_03` | 2.61m | 4 | ja |
| `SM_EuropeanBeech_Sapling_04` | 2.08m | 4 | ja |
| `SM_EuropeanBeech_Seedling_01` | 1.04m | 4 | ja |
| `SM_EuropeanBeech_Seedling_02` | 1.20m | 4 | ja |
| `SM_EuropeanBeech_Seedling_03` | 0.83m | 4 | ja |
| `SM_EuropeanBeech_Seedling_04` | 0.24m | 4 | ja |

Die vorhandenen Nanite-Einstellungen, LODs, UVs, Texturen und Kollisionskörper wurden unverändert übernommen. Nanite und Masked-Nanite waren im Prüfeditor per CVar eingeschaltet; Asset-Einstellung und tatsächliche einzelne GPU-Ausführung sind dennoch getrennte Aussagen. Keine vollständige per-Mesh-Nanite-Profilierung durchgeführt.

Die Materialien besitzen Windunterstützung, unter anderem den vorhandenen Parameter `Wind Animation Strength`, sowie Saison-/Gesundheitsparameter und Impostorvarianten. Verwendet wird SimpleWind mit den Originalmaterialen; kein neuer globaler Wind-Actor oder Wettermechanismus. Keine unabhängige Abnahme jeder Wind-/Saisonvariante oder temporaler Feinqualität aus Standbildern behauptet.

Der vollständige lesende Bestand liegt lokal in `Saved/ProjectRefinement/EuropeanBeechV1/AssetInventoryV2.json`: 34 Mesh-, 89 Material- und 34 Foliage-Datensätze, 0 Auslesefehler. Der erste Inventar-Callback reenterte während Assetkompilierung und erzeugte Duplikate; er wurde gestoppt und mit Busy-Sperre vollständig wiederholt. Die erste `AssetInventory.json` ist deshalb ausdrücklich nicht maßgeblich.

## Verwendete Modelle, Materialien und Platzierung

**2.493 Instanzen in 61 HISM-Gruppen**, dazu Boden und Anschlussweg: insgesamt **63 neue Actors**. Gruppen befinden sich im Editor unter `VisualV2/EuropeanBeechV1`, Labels beginnen mit `EBF1_`; aufgeteilt in Edge, Inner, West und Deadwood. Ein fester Seed und getrennte Gruppen erlauben nachvollziehbare spätere Anpassungen.

| Inhalt | Instanzen | Tatsächliche Quelle |
|---|---:|---|
| Größere/jüngere Waldbäume | 194 | Forest_01, 02, 04–08 und Field_01 aus SimpleWind |
| Junge Buchen | 136 | Sapling_01–04 |
| Setzlinge | 220 | Seedling_01–04 |
| Farne | 800 | vorhandene `SM_WA7_Fern_A/B` |
| Woodland-Gras | 850 | vorhandenes `SM_EQ3_GrassWoodland` |
| Moospolster | 260 | vorhandenes `SM_WA5_MossCushion` |
| Gefallene Äste | 24 | vorhandenes `SM_HH4_FallenBranch` |
| Stümpfe | 9 | vorhandene `SM_WLA_Stump_A/B` |

Das Quixel-Paket enthält keine separaten Totholzstämme oder unabhängigen Bodenpflanzenmeshes. Diese Ergänzungen stammen daher aus dem vorhandenen Projekt. Deren stilisierte Geometrie bleibt sichtbar einfacher als die gescannten Buchen; keine nicht vorhandenen Quixel-Totholzassets oder hochwertigeren Ersatzmodelle behauptet.

194 größere Waldbäume mit mindestens etwa 6 m Stammabstand, unregelmäßigen Rotationen und moderaten Skalierungen. Kleinere Pflanzen bilden unterschiedlich dichte Gruppen. Keine Rasteranordnung. Freihaltung gegenüber dem Weg je nach Pflanzenart; die freie Wegmittellinie wurde tatsächlich abgelaufen. Dichte Bodenpflanzen werfen keine zusätzlichen eigenen Schatten, Baum- und Jungbaumgruppen verwenden ihre Originalschatten und Originalkollision. Kein globales Abschalten von Vegetationsschatten.

Originalmeshes und Materialslots werden direkt referenziert. Beispiel Forest_04: Originalinstanzen `MI_EuropeanBeech_TwoSided`, `MI_EuropeanBeech_Tileable`, `MI_EuropeanBeech_Trunk_04`, `MI_EuropeanBeech_Decoration` sowie der Originalimpostor. Keine Originalmaterialien umgeschrieben.

Nur drei eigene neue Bodenassets unter `/Game/Environment/EuropeanBeechV1`: `Textures/T_EBF_PathMask`, `Materials/M_EBF_ForestGround` und `Materials/M_EBF_Connector`. Sie referenzieren bestehende Projekttexturen `T_WA5_ForestFloor`, `T_HA4_Earth` und `T_HA4_Meadow`. Die eigene numerische Wegmaske stammt aus `Art/World/EuropeanBeechV1/PathMask.png`. Der neue Boden ist beleuchtet und rau, nicht selbstleuchtend. Sanfte Boden-/Wegränder, Moos, Gras und Totholz schaffen Variation; keine ausgeformte Hügellandschaft auf der ebenen Testfläche.

Bestehende HISM-/Nanite-/LOD-Technik, keine neue Foliage-Architektur. Sichtweiten pro Gruppe: größere Bäume 130–180 m, kleinere Gruppen 60–85 m. Das sind lokale Komponenteneinstellungen. Bei weit entfernten Luftaufnahmen können Gruppen ausgeblendet werden; die erste Übersicht `08_Gesamtstruktur.png` zeigt diesen Effekt und ist kein Vollbestandsnachweis. Die näher zentrierte `09_Gesamtstruktur.png` zeigt die Hauptstruktur des Walds.

Eigene Quellen: `Tools/EuropeanBeechV1/Layout.py`, `Layout.json`, `Build.py`, `Snapshot.py`, `AssetReferences.json` und `README.md`. Build ist ein einmaliges, geschütztes Authoringwerkzeug für den Ausgangsstand; es lehnt bereits vorhandene EBF1-Gruppen ab. Nicht erneut über die ausgelieferte Map laufen lassen. Vorhandene HISM-Gruppen können anschließend normal im Editor bearbeitet werden.

## Spielbarkeit und Kamera

Die Produktionskamera blieb vollständig erhalten: Third Person, 350 cm Standardabstand, tatsächlicher View-Pitch −12°, ausschließlich horizontaler Orbit. Gemessene Kamerahöhe im frischen Spielprozess auf dem neuen Boden **172,35 cm über Welt-Z=0**, also etwa **172,15 cm über dem lokalen Boden**. Zoom 200/600 cm, Wechsel 2D→ThirdPerson und vorhandene Kollisionskorrektur wurden geprüft; keine Kameraquelldatei geändert.

Echte Enhanced-Input-Bewegung in PIE:

- `PIEWalk02`: 159 protokollierte Schritte, 215,01 s, 310,31 m Bewegungsprotokoll. Waldrand, Rundweg, Lichtung und Totholzpfad durchlaufen; Save/Load und Zoom bestanden. Der Lauf endet mit einer fehlgeschlagenen zu strengen Stammtestannahme, ist deshalb **kein vollständig bestandener Gesamtlauf**.
- Diagnose `TrunkProbe.json`: direkte Traces in 50/100/172 cm Höhe treffen den Originalstamm. Der echte Spieler-Kapselsweep wird am Original-HISM blockiert. Beim ersten Laufversuch war die Figur seitlich am runden Stamm vorbeigeglitten; daraus folgt kein fehlender Collider.
- `PIEReturn03`: **bestanden**, 83,99 s, weitere 178,68 m. Kapselsweep, echte SpringArm-Verkürzung am Originalstamm, Rückweg über den Seitenpfad und Waldweg bis X≈−3300/Y≈2350. Sprint 315 cm/s, Gehen 210 cm/s, unverändertes Grafikprofil.

Die Bewegungsprotokolle ergeben rund 489 m; darin enthalten ist etwa 1,1 m Positionskorrektur durch den separaten Save/Load-Test. Rund 488 m tatsächliche Fortbewegung. Kontrollierte Ausgangs- und Kollisionsprobe-Positionierungen sind kein lückenlos gelaufener Anweg vom ursprünglichen Spielerstart. Der Anschluss vom bestehenden Nordweg in den Wald und zurück wurde physisch gelaufen.

Der erste kurze Prüfskriptlauf `PIEWalk01` scheiterte an falsch verwendeten Positionsargumenten von `unreal.Rotator`; dadurch wurde im Test die vertikale statt der horizontalen Drehung gesetzt. Auf benannte Yaw-Argumente korrigiert und wiederholt. Keine Produktionskamera oder Map dafür geändert, keinen fehlgeschlagenen Prüflauf als bestanden gewertet.

## Save/Load und Neustart

PIE ausschließlich eigener Slot `PokeMonster_SaveV2_Test_EuropeanBeechV1` im eigenen Editor-UserDir. Der erste Prüfskriptentwurf wurde vor Ausführung durch die automatische Freigabeprüfung wegen fehlender erneuter expliziter Slot-Auswahl blockiert. Sichere Ausführung erst nach neuem PIE-Start, ausdrücklicher Testslot-Auswahl und exakter UserDir-Prüfung.

An der Lichtung über die vorhandenen Menü-/SaveGame-Dienste gespeichert, Position im Test verändert und wieder geladen: gespeicherte Position und sämtliche serialisierten Teamfelder exakt wiederhergestellt. Bestehende Erfahrung, AP, Attacken und Identitäten werden nicht separat neu verwaltet.

`Native01`: frischer separater Development-Spielprozess mit eigener UserDir und ausschließlich Kopie dieses QA-Spielstands. **4 Prüfgruppen bestanden, Prozess Exit 0**, 64,00 s Laufzeit: genaue Waldposition und vollständiges Team geladen, alle 63 neuen Actors vorhanden, echte anschließende Bewegung, unveränderte Grafikwerte. Der reguläre Enton-Begleiter war aktiv; Garados/Glurak blieben im isolierten Team. Kein Nutzerspielstand geladen oder überschrieben.

Nach regulärem PIE-Ende wiederholter Actor-Abgleich: **1.482 vorbestehende Editorwelt-Actors unverändert**, einschließlich temporärer Engine-/Preview-Actors. Die erste reine Karteninventur enthielt 1.475 Szenen-Actors. Referenzabschluss: **23 verwendete Meshpfade, 157 Abhängigkeitspakete, 0 fehlende lokale Abhängigkeiten**.

## Kurze Performance-Stichproben – deutliche Einschränkung

Keine neue Optimierungsphase und keine Reduktion von Grafikqualität, Auflösung oder Renderingprofil. Im frischen Development-Prozess drei stationäre Stichproben von jeweils etwa 8 s nach jeweils 6 s Standort-Warm-up, ohne Videoaufnahme, mit Weltuhr/Beleuchtung und Begleiter aktiv. QHD-Viewport auf 2560×1440 gesetzt; Profil C unverändert mit 75 % Screen Percentage, TAAU, Software-Lumen/IFG, VSM4. Interne 1920×1080 ist daraus abgeleitet, keine neue GPU-Allokationsauslese behauptet. Engine-CSV, keine aus Aufnahme-FPS abgeleitete Spielleistung.

| Blickpunkt | Frames | FPS | Frame Ø | GPU Ø | Game Thread Ø | Render Thread Ø | Frame p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Lichtung | 134 | 16.73 | 59.77 ms | 59.28 ms | 5.39 ms | 58.05 ms | 63.42 ms |
| Waldrand | 94 | 11.69 | 85.52 ms | 84.03 ms | 3.79 ms | 85.54 ms | 92.35 ms |
| Waldweg | 150 | 18.70 | 53.48 ms | 53.89 ms | 2.66 ms | 53.49 ms | 58.18 ms |

Die Werte sind kurze aktuelle Stichproben, kein wiederholter Vorher-/Nachher-Benchmark. Threadzeiten einschließlich Warteanteilen nicht als voneinander unabhängige Kosten addieren. Einzelspitzen bis etwa 282 ms; Shader-/PSO-Hitches wurden beim Aufwärmen und insbesondere bei der großen Editorübersicht beobachtet. Ihre genaue Zuordnung zu jeder Framezeitspitze wurde nicht profiliert.

**Keine stabilen 30 FPS nachgewiesen.** Die neuen Originalbuchen sind in diesen Blickrichtungen deutlich GPU-aufwendig. Trotz Instancing bleibt die Spielbarkeit hinsichtlich Flüssigkeit eingeschränkt. Das ist ein offener Punkt für eine spätere, gesondert beauftragte Prüfung nach Harrys visueller Beurteilung. Keine pauschalen LOD-/Schatten-/Materialkürzungen oder Änderung der Originalassets vorgenommen, um eine bessere Zahl vorzutäuschen. Die langsame Editor-Luftansicht ist außerdem nicht mit normaler Spieleransicht gleichzusetzen.

## Technische Prüfungen

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build | `Build01`, Exit 0, 23,50 s einschließlich Wrapper; Engine meldet Succeeded |
| Vollständige PokeMonster-Automation | `Automation01`: **317 bestanden, 0 mit Warnungsstatus, 0 fehlgeschlagen, 0 nicht ausgeführt** |
| Strenger QA-Wrapper | **Exit 0**, Engine Exit 0; bestehender strenger Reportvertrag, isolierte UserDir |
| Zwölf bestehende Root-Maps | jeweils **0 Fehler / 0 Warnungen**, ausschließlich geladen/geprüft |
| VisualV2-PIE | tatsächliche Bewegung, Screenshots, Zoom, Kollision, Save/Load und Rückweg wie oben einzeln abgegrenzt |
| Separater Spielprozess / Neustart | Native01 bestanden, eigene Testkopie, kontrolliertes Spielende |
| Original-/Nutzerdateien | Hashvergleich bestanden, siehe Projektschutz |

Map-Checks über alle zwölf vorhandenen `Content/Maps/*.umap`, anschließend VisualV2 wieder geladen. Keine fremde Map gespeichert. Exakte Liste in `MapChecks.json`, Nullergebnisse innerhalb `EUROPEAN_BEECH_MAPCHECK_BEGIN/END` im Editorlog.

Engine-/Plugin-Startmeldungen (UnifiedError/Condition failed, Python-Namenskollision, Layout-/Pluginhinweise) sowie vereinzelte HTTP-Zeitüberschreitungen getrennt vom vollständig erfolgreichen Testreport betrachten. Die Meldung `idevice_id: Bad CPU type in executable` wurde in diesen abschließenden Logs nicht beobachtet; keine iOS-/Engine-Helferänderung. Der QA-Exit 0 bedeutet nicht, dass der gesamte Engine-Start meldungsfrei ist.

Ein unerwartet als geändert markiertes `MI_WLA_Timber` blockierte zunächst den PIE-Schutzcheck. Die Festplattendatei entsprach nachweislich dem Anfangshash. Automatische Freigabeprüfung lehnte das Verwerfen des Speicherzustands ab; erst nach ausdrücklicher Zustimmung für Material und eigenen Editor PID19235 wurde ausschließlich dieses Material von der unveränderten Datei neu geladen. Keine Materialdatei gespeichert. Danach keine ungespeicherten Pakete, eigener Editor regulär geschlossen. Kein Force Quit und keine fremde Sitzung beendet.

Keine neue physische Controllerprüfung behauptet. Bewegung und Zoom wurden über die bestehenden Enhanced-Input-Aktionen im echten Spiel automatisiert geprüft. Keine Gameplay-, Kampf-, Pokémon- oder Animationsänderung; die vorhandenen Systeme sind zusätzlich durch die 317 Tests abgedeckt, nicht alle Gameplayaktionen wurden für diesen reinen Waldauftrag erneut manuell durchgespielt.

## Echte QHD-Aufnahmen

Alle folgenden Nachweise lokal unter `Saved/ProjectRefinement/EuropeanBeechV1/`, echte Unreal-Aufnahmen 2560×1440:

1. `PIEWalk02/01_Waldrand.png` – Anschluss und Blick in den Wald.
2. `PIEWalk02/02_Waldweg.png` – geschwungener Waldweg und Vegetation.
3. `PIEWalk02/03_UnterKronen.png` – normale Spielansicht unter dem Kronendach.
4. `PIEWalk02/04_Lichtung.png` – kleine offene Lichtung.
5. `PIEWalk02/05_ZwischenBaeumen.png` – Third-Person-Spielansicht im Wald.
6. `PIEWalk02/06_Totholz.png` – Seitenpfad und vorhandenes Totholz mit Enton.
7. `PIEReturn03/07_StammKamerakollision.png` – reale Stamm-/Kameraprobe.
8. `09_Gesamtstruktur.png` – separate Editor-Luftansicht der Hauptstruktur; ausschließlich Editoransicht bewegt und anschließend wiederhergestellt.

Aufnahmen visuell angesehen. Keine KI-generierten Nachweise, keine künstliche Video-Framerate. Kein zusätzliches Rundgangvideo erstellt; die Aufnahmen ersetzen keine vollständige temporale Blatt-/Windabnahme. Große Medien und Rohinventare werden nicht ins öffentliche Repository aufgenommen.

## Lizenz und öffentlicher Git-Umfang

Tatsächliches Origin `git@github.com:Harrys-F/PokeMonster.git`, GitHub-API bestätigt öffentliches Repository. Harrys ausdrückliche Entscheidung: **nur eigene Map-/Werkzeug-/Dokumentationsänderungen pushen; Fab-Assets lokal behalten**. Die eigenen Boden-/Maskenassets gehören zur Mapgestaltung und enthalten keine kopierten Quixel-Texturen oder Meshdaten.

Enge Ignore-Regeln für `/Content/Fab/EuropeanBeech/`, `/Content/MSPresets/MS_Foliage_Material/` und `/Content/MSPresets/MSAssets.db`. Keine dieser Originaldateien stagen oder pushen. Eigenes Referenzverzeichnis dokumentiert die Importabhängigkeiten. **Ein frischer öffentlicher Checkout allein enthält die Buchen nicht**; erforderlich ist ein eigener lizenzierter Import an denselben Pfaden.

Offizielle Quellen: [European Beech auf Fab](https://www.fab.com/listings/d11cc01d-9422-41b7-950f-416c9ce79caf?lang=en), [Fab-Lizenz](https://www.fab.com/eula?lang=en). Lokaler Assetbestand eigenständig geprüft. Der konkrete Erwerbsbeleg des Nutzerkontos wurde nicht ausgelesen; kein allgemeines Weiterverteilungsrecht oder private Asset-Sicherung behauptet.

## Projektschutz und Git-Abschluss

Anfangsbestand: 6.021 versionierte Dateien, 663 vorhandene Save-Dateien und 351 unversionierte Dateien, darin die 317 Fab-/MSPresets-Dateien und 34 zuvor geschützte Nutzer-/Arbeitsdateien. `ProtectionCheck.json` bestätigt sämtliche ursprünglichen Save- und unversionierten Dateihashes unverändert. Die vorhandene lokale Änderung an `Config/DefaultEngine.ini` bleibt erhalten und außerhalb dieses Commits. Beide Vollbackup-Verweise bleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`.

Unter den vorher versionierten Dateien ausschließlich VisualV2, diese Entscheidungsergänzung und enge Ignore-Regeln geändert. Neu nur eigene Bodenassets, eigene Wegmaskenquelle, Authoringwerkzeuge und dieser Bericht. Keine Änderungen an Westland, Biom-Testmap, Originalen, Pokémon, Gameplay, Kamera oder Grafikprofilen. Keine Projektkopie, kein Worktree, kein LFS-Prune und keine destruktive Git-Operation.

Git-Sicherung ausschließlich der 14 eigenen Map-/Boden-/Masken-/Werkzeug-/Dokumentationsdateien. Normaler Commit auf main und normaler Push auf origin/main; konkrete Commit-SHA über `git log -1 -- Docs/EUROPEAN_BEECH_FOREST_V1.md`. Abschließende Remote-/LFS-Nachweise werden lokal in `Saved/ProjectRefinement/EuropeanBeechV1/GitFinal.json` protokolliert und im Chat gemeldet. Keine Kontrollmedien oder privaten Quellen einschließen. Danach **keine weitere Wald-/Kameraänderung vor Harrys eigener Erkundung und Beurteilung**.
