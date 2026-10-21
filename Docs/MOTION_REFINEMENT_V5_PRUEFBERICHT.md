# Glurak, Nebulak und Spielfigur – Bewegungsüberarbeitung V5

Stand: 21.10.2026. Ausgangspunkt `7bc626972dff133de7317ed2738d9982a17705b9`, Branch `main`, ausschließlich `/Users/harry/Developer/PokeMonster`. Die neuen Darstellungen sind im bestehenden System aktiviert. Die künstlerische Abnahme bleibt Harry vorbehalten; insbesondere enge Spielerwendungen und die Gaswirkung sollten anhand der echten Sequenzen beurteilt werden.

## Umfang und Schutz

Keine neue Map, kein Worktree, keine Projektkopie, keine neue Kreatur und keine Habitat-, Kampfregel-, Kamera-, Heilhaus- oder Landschaftsänderung. VisualV2 und sämtliche übrigen Karten bleiben binär unverändert. Originale, V4-Rückfallquellen, ursprüngliche Materialien und die bisherigen Clips bleiben erhalten. Die bestehenden 51 unversionierten Dateien werden einzeln über SHA-256 geschützt. Das Dev-Save wird nach schreibenden Tests exakt restauriert; Referenz-SHA-256 `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt über beide lokalen Backup-Verweise erhalten und gehört nicht zur main-Historie.

## Tatsächlich geändert

### Glurak

- Neue gepackte Quelle `Art/Characters/Creatures/Glurak/Source/Glurak_MotionV5.blend`, zehn FBX unter `Exports/MotionV5`, neue Unreal-Assets unter `/Game/Characters/Creatures/Glurak/MotionV5`.
- Originalgeometrie, UVs, Texturen und Rest-Skelett erhalten; 35.341 gezielt ausgewählte Gewichte neu verteilt. Fälschliche Hand-/Kopf-/Beckeneinflüsse auf die Flügelmembran wurden durch zusammenhängende Flügel-/Brusteinflüsse ersetzt. Keine neue Körperform.
- Neue Flügelkurven für die sieben bisherigen Rollen; zusätzliche Takeoff-, Hover- und Land-Clips. Orange Rückseiten und dunkle Innenseiten bleiben erhalten. Schwanzflamme folgt weiterhin dem vorhandenen Anker.
- Maximal gemessene Flügelkantenverlängerung: Idle 0,53 cm, Walk 0,76 cm, Run 1,06 cm, Attack 2,54 cm; Takeoff/Hover maximal rund 5,22 cm. Das sind geometrische Prüfwerte, keine automatische Aussage anatomischer Perfektion. Die verworfenen ersten Gewichtsversuche wurden nicht als freigegeben gespeichert.
- Bestehende Run-Baucheindringung korrigiert: Becken/Körper 1,3 cm angehoben, beide ursprünglichen Fußtransformationen per IK erhalten; maximaler Fußfehler etwa `6,7e-8 m`. Kleinster Source-Z-Wert danach nur numerisch unter Null (`<0,001 cm`).
- Automatisches bodennahes Schweben: initial nach 6–13 s geeigneten Bedingungen, danach 28–45 s Bodenpause; Takeoff 1,6 s, Hover 7 s, Landung 1,4 s. Sollhöhe 90 cm, sanfte Bewegung 86–94 cm. Nur Visual-Origin/Mesh werden angehoben; Bodenkapsel, Identität und bestehende Wegsuche bleiben erhalten.
- Keine Flugnavigation, kein Überfliegen unpassierbaren Bodens, keine Innenraum-Flüge. Takeoff/Landing halten die Wegbewegung kurz an. Vollständige Freiraumsäule mit drehungsunabhängigem Flügelraum wird vor Abheben und während des Schwebens geprüft; jeder weitere Wegabschnitt verwendet einen kontinuierlichen Sweep. Bestehende kollisionslose Baum-/Felsdekoration wird zusätzlich über ihre Bounds berücksichtigt. Die Prüfung ist bewusst konservativ und kann Schweben in engen Bereichen verhindern.
- ClassicBattle-Visuals erhalten keinen Bewegungskontext und schweben nicht autonom. Verdeckte Oberweltquellen und laufende Kämpfe setzen den Schwebezustand zurück; WorldBattle erhält eine kurze visuelle Rückführung zum Boden.

### Nebulak

- Neue gepackte Quelle `Art/Characters/Creatures/Nebulak/Source/Nebulak_MotionV5.blend`, sieben Rollen plus statischer Hüllenexport; Unreal unter `/Game/Characters/Creatures/Nebulak/MotionV5`.
- Originalmesh, UVs, Gewichte, Kern-/Gesichtsoptik und Originaltexturen erhalten. 14.199 vorhandene Gasflächen erhalten einen eigenen Materialslot; Gesicht/Kern bleiben deckend.
- Eine kombinierte räumliche Zusatzhülle mit 1.290 Vertices/2.520 Dreiecken, ein Mesh und ein Material. Keine volumetrische Simulation, kein Partikelschwarm, keine zusätzlichen Lichtquellen oder Gameplay-Collider.
- Mehrere unterschiedlich schnelle räumliche Strömungen, langsame Dichtevariation und WPO unabhängig vom Clip-Schweben. Violette echte Transparenz und blickwinkelabhängiges Auslaufen an den Außenrändern; frontseitige Gesichtsöffnung über feste Vertexmasken.
- Hülle am bestehenden `head`-Anker: Mesh-Referenzkoordinaten plus inverse **tatsächlich importierte** Unreal-Referenztransformation. Der zunächst falsch angenommene Bone-/FBX-Versatz wurde vor Übernahme korrigiert.
- Im Modellsetup zwei zusätzliche Material-Draws gegenüber der bisherigen Einmaterialdarstellung; keine gemessene GPU-Einsparung behauptet. Keine FPS-Benchmarks durchgeführt. Die leichte Hülle ersetzt keine hochwertige volumetrische Rauchsimulation; in vergrößerten Ansichten bleiben ursprüngliche Gasformen erkennbar.

### Spielfigur

- Neue gepackte Quelle `Art/Characters/YoungTrainer/Source/Player_Meshy_MotionQuality_V3.blend` und drei Exporte; Clips unter `/Game/Characters/YoungTrainer/MotionV3` auf dem **unveränderten vorhandenen Skeleton**. Bestehendes Player-Mesh, Gewichte, UVs, Materialien und Meshy-Erscheinung unverändert.
- Idle mit subtiler Gewichtsverlagerung und entsperrten Knien; Walk/Run mit zusammenhängender Bein-IK, dezenter Abrollbewegung, angepasstem Armschwung und kontinuierlicher Rückführgeschwindigkeit der Füße. Keine unabhängige Verschiebung des Fußknochens zur Bodenreparatur mehr.
- Gepackte Quelle frameweise geprüft: minimaler Sohlenabstand etwa 0,05 cm; größte Knie-/Sprunggelenk-Anschlussabweichung unter 0,00030 cm. Geh-/Sprintreferenz 210/315 cm/s unverändert, Zyklen 0,55/0,45 s.
- Visuelle Drehung mit begrenzter Geschwindigkeit/Beschleunigung statt sofortigem 180°-Sprung. Interaktionsrichtung und Eingaben bleiben unmittelbar. Bewegungsblend über glatte Kurve mit 0,16 s Start/0,24 s Stop; gemeinsame Walk-/Run-Kontaktphase bleibt erhalten. Vorhandene Mantel-/Taschensprings werden weiterverwendet.
- **Kein pauschal nachgewiesener Gewinn beim Fußgleiten:** Die mittlere Standphase war bereits relativ ruhig. Ein korrekt auf beide aufeinanderfolgenden Kontaktphasen begrenzter Knöchelindikator liegt vor/nachher beim Walk bei etwa 0,59/0,89 cm/s und beim Sprint bei 1,65/1,12 cm/s (nur 6–15 geeignete Paare). Unter Videoaufnahme schwankt der Indikator; daraus folgt keine belastbare allgemeine Verbesserung. Frühere Auswertungen mit nur einem geprüften Phasenendpunkt wurden verworfen. Nachgewiesen sind Source-IK-Kohärenz, kontinuierlichere Rückführung und weiche Dreh-/Blendübergänge. Enges Wenden/Starten ist kein vollständiges World-Space-Foot-Locking und kann weiter sichtbares Gleiten zeigen.

## Quellen und echter Reimport

| Quelle | Blender-Bones | Originale Body-Dreiecke | FBX-Rückimporte |
|---|---:|---:|---:|
| Glurak | 24 | 246.066 | 10 |
| Nebulak | 12 | 21.687 | 8, davon eine neue Hülle |
| Player | 25 | 47.744 | 3 |

Alle drei gepackten Dateien erneut geöffnet; benötigte Bilder eingebettet. Alle 21 FBX tatsächlich in Blender zurückimportiert, Knochen-/Meshanzahl, Animation und Prüfsummen geprüft. Unreal hat separate Kreaturen-Skeletons mit identischen Rest-Bones erhalten; Player behält sein bisheriges Skeleton. Nur die zwei Spezies-Präsentationsverweise wurden geändert, keine Spezies-ID, Kampfwerte oder Save-Struktur. Quellen-/Exportprüfdaten liegen dauerhaft in den jeweiligen `MotionV5_Audit.json` beziehungsweise `MotionQualityV3_Audit.json`.

Werkzeuge und Schutzregeln: [Tools/MotionRefinementV5/README.md](../Tools/MotionRefinementV5/README.md). Erstaufbau-/Korrekturskripte verweigern vorhandene beziehungsweise bereits veröffentlichte Kandidaten. Sie sind keine automatischen Reimport-Jobs für freigegebene Assets.

## Echte Bild- und Bewegungsnachweise

Alle folgenden Medien stammen aus Unreal. Sie bleiben absichtlich lokal unter ignoriertem `Saved/` und werden nicht auf GitHub gespeichert. Eine frische Arbeitskopie enthält deshalb die Medien nicht; mit den Reviewwerkzeugen können neue Nachweise erzeugt werden. Vorführbilder zeigen das explizite transiente Pokémon-Testgelände innerhalb der bestehenden VisualV2, keine behauptete natürliche Habitatbegegnung. Echte Begegnungs-/Gameplaytests sind separat aufgeführt.

Ausgabe per tatsächlicher Viewportabfrage und Screenshotgröße 2560 × 1440 verifiziert; `r.ScreenPercentage 100`. Bestehende Spielkamera unverändert. Bei der statischen Spieler-Idle-Paarung beträgt die Kameradifferenz numerisch weniger als `1e-6 cm`; bei bewegten Aufnahmen sind Eingabefolge und Kamera gleich, die Frame-/Phasenzeitpunkte jedoch nicht bitidentisch. Kein unfairer pixelgenauer Bewegungsvergleich behauptet.

| Motiv | Vorher | Nachher |
|---|---|---|
| Glurak, feste Spielkamera | [Original QHD](/Users/harry/Developer/PokeMonster/Saved/CreaturePolishV4/V5GlurakOriginalAligned/Frame4_QHD00000.png) | [V5 QHD](/Users/harry/Developer/PokeMonster/Saved/CreaturePolishV4/V5GlurakNative/Frame4_QHD00000.png) |
| Nebulak frontal | [Original QHD](/Users/harry/Developer/PokeMonster/Saved/CreaturePolishV4/V5NebuOriginalFront/Frame4_QHD00000.png) | [Korrigierte Hülle QHD](/Users/harry/Developer/PokeMonster/Saved/CreaturePolishV4/V5GasAlignedFront01/Frame4_QHD00000.png) |
| Nebulak seitlich | [Original QHD](/Users/harry/Developer/PokeMonster/Saved/CreaturePolishV4/V5NebuOriginalSide/Frame4_QHD00000.png) | [V5 QHD](/Users/harry/Developer/PokeMonster/Saved/CreaturePolishV4/V5NebuFinalSide/Sequence0000600000.png) |
| Nebulak hinten | [Original QHD](/Users/harry/Developer/PokeMonster/Saved/CreaturePolishV4/V5NebuOriginalRear/Frame4_QHD00000.png) | [V5 QHD](/Users/harry/Developer/PokeMonster/Saved/CreaturePolishV4/V5NebuFinalRear/Sequence0000600000.png) |
| Spieler Idle | [V2 QHD](/Users/harry/Developer/PokeMonster/Saved/MotionRefinementV5/PlayerBefore03/Time3_QHD00000.png) | [V3 QHD](/Users/harry/Developer/PokeMonster/Saved/MotionRefinementV5/PlayerAfter01/Time3_QHD00000.png) |
| Spieler Sprint | [V2 QHD](/Users/harry/Developer/PokeMonster/Saved/MotionRefinementV5/PlayerBefore03/Time14_QHD00000.png) | [V3 QHD](/Users/harry/Developer/PokeMonster/Saved/MotionRefinementV5/PlayerAfter01/Time14_QHD00000.png) |

- [Glurak: Abheben, Schweben, Landen, rund 37 s](/Users/harry/Developer/PokeMonster/Saved/VisualV2TAAIntegrationV1/Recordings/V5GlurakNative/Motion.mp4), 261 echte QHD-Frames, tatsächliche Zeitstempel.
- [Spieler: Idle, Gehen, Sprint, Stop und acht Richtungen, rund 50 s](/Users/harry/Developer/PokeMonster/Saved/VisualV2TAAIntegrationV1/Recordings/PlayerNative/Motion.mp4), 478 echte QHD-Frames.
- [Nebulak frontal](/Users/harry/Developer/PokeMonster/Saved/VisualV2TAAIntegrationV1/Recordings/V5NebuNativeFront/Motion.mp4), [seitlich](/Users/harry/Developer/PokeMonster/Saved/VisualV2TAAIntegrationV1/Recordings/V5NebuNativeSide/Motion.mp4), [hinten](/Users/harry/Developer/PokeMonster/Saved/VisualV2TAAIntegrationV1/Recordings/V5NebuNativeRear/Motion.mp4): 51/44/49 echte QHD-Frames, jeweils rund 7 s. [Zusätzlicher kontinuierlicher Überhangnachweis](/Users/harry/Developer/PokeMonster/Saved/VisualV2TAAIntegrationV1/Recordings/V5HoverSweepFinal02/Motion.mp4), 264 QHD-Frames/rund 37 s.
- ClassicBattle: [Glurak hinten](/Users/harry/Developer/PokeMonster/Saved/CreatureExpansionV3/MotionV5GlurakBattle02/Glurak_Battle_0.png), [Nebulak vorne](/Users/harry/Developer/PokeMonster/Saved/CreatureExpansionV3/MotionV5NebulakBattle/Nebulak_Battle_1.png). Die bestehenden Battle-RenderTargets haben korrekt **2560 × 1080**, nicht 2560 × 1440. Separate LiveUI-Aufnahmen enthalten die vollständige QHD-Oberfläche.

Die MP4-Dateien enthalten ausschließlich echte Framebufferbilder mit ihren ursprünglichen relativen Spielzeitabständen, keine interpolierten oder generierten Frames. Aufnahmen bleiben durch Readback/Kompression beeinflusst und ersetzen keinen ungestörten Live-Eindruck. Die langsame erste PNG-Aufnahme wurde nicht als flüssige Videoabnahme ausgegeben.

## Technische und Gameplay-Prüfung

| Prüfung | Tatsächlicher Stand |
|---|---|
| Mac Development Editor Build | Build04 erfolgreich, Prozesscode 0; native Codeänderungen vollständig gebaut |
| Source-Reopen/FBX | 3 gepackte Quellen, 21 erfolgreiche Rückimporte |
| Erstes automatisches Schweben | Grounded → Takeoff → Hover → Landing → Grounded; maximal ca. 94 cm |
| Niedrige Decke | Abheben gesperrt; bleibt Grounded, Freiraumprüfung durchgängig negativ |
| Kontinuierliche Schwebe-Wegeprüfung | Bestanden: derselbe freie Abschnitt vor Hindernis; während Hover mit seitlich-diagonalem Prüfhindernis abgewiesen; nach Landung bei unverändertem Hindernis wieder begehbar |
| Player Enhanced Input | Walk 210, Sprint 315 cm/s; Idle/Stop und alle acht Richtungen; unveränderte Kamera/Spielphysik |
| ClassicBattle Glurak/Nebulak | Beide Perspektiven, Attack/Hit/Happy/Faint und echte Attackenauflösung; keine autonome Battle-Schwebehöhe |
| Team | Tatsächliche Slate-Tastaturbedienung, belegte/freie Plätze, genau ein Begleiter, Kampf-Sperre, Save/Load: bestanden |
| Niederlage wilder Pokémon | Glurak 18,03 m und Nebulak 14,41 m sichtbar geflohen; erst außerhalb des Bildes entfernt, kein sofortiger Respawn |
| Fang | Sieben neuen Spezies nacheinander gefangen; Team/Bestand und ursprünglicher Dev-Save wiederhergestellt |
| Spieler-Niederlage | Rückkehr/Autosave und erneutes Laden bestanden, ursprünglicher Dev-Save wiederhergestellt |
| WorldBattle | Sonderausgang bleibt erhalten, kein automatisches ClassicBattle-Fluchtverhalten |
| Vollständiger erster PIE-Fußlauf | 103 Schritte, 288,23 m; Sprint, Dialog/Quest, Fang/Kampf, Brücke, Heilhaus, Heilung, Menüs, Save/Load bestanden |
| Begleiter im Fußlauf | 630 Stichproben, 51 korrekt im Kampf verborgen, 43 schattenfreie Innenraum-Stichproben, keine Assertion-Fehler. Roher Maximalabstand enthält die bestehende räumlich versetzte Innenraumtechnik und ist kein Nachlauf-Distanznachweis |
| Map Check erster Abschluss | Alle 11 vorhandenen Maps, einschließlich geschützter unversionierter Karte: 0 Fehler, 0 Warnungen |
| Vollständige Automation erster Abschluss | 94 Tests: 93 Success, 1 SuccessWithWarnings, 0 Failed/NotRun/InProcess; ausschließlich bekannte externe idevice_id-Warnungen |
| Abschließende Wiederholung nach kontinuierlichem Sweep | Build04 und Glurak-Battle erneut bestanden; voller Fußlauf 103 Schritte/289,32 m, 636 Begleiter-Stichproben ohne Issues (45 Kampf-/44 Innenraumstichproben); alle 11 Map Checks wieder 0/0; **94/94 Automation Success ohne Testwarnungen**, strenger Runner Code 0 |
| Physischer Switch-Pro-Controller | Offen; nicht durchgeführt und kein Abschlusskriterium |

Lokale Rohprotokolle: `Saved/MotionRefinementV5`, `Saved/ProjectRefinement/MotionV5Build*`, `Saved/ProjectRefinement/MotionV5Automation*`, `Saved/CreatureExpansionV3/MotionV5*`, `Saved/GlumandaV11/Acceptance/MotionV5*`.

## Fehler, verworfene Prüfungen und Warnungen

1. Erste Glurak-Gewichtskandidaten überschritten die Verformungsgrenze und wurden vor Source-Save verworfen. Erste Source-Prüfskript-/IK-Fehler wurden vor erfolgreichem Export korrigiert. Keine Originalquelle überschrieben.
2. Erste Nebulak-Zusatzhülle lag wegen falscher Bone-/FBX-Raumannahme versetzt. Mesh-Space-Export und exakte inverse Unreal-Referenztransformation korrigieren dies; keine Originalassets reimportiert.
3. Erster Hover-Fixtureversuch war durch die unsichtbare Spieler-Kapsel blockiert. Ausschließlich die versteckte Kamera-Dummy-Figur der expliziten Vorführung wird nun temporär kollisionslos/bewegungslos und danach zurückgesetzt. Normales Gameplay bleibt unverändert.
4. Erste schwere PNG-Sequenz endete vor der Landung: die begrenzte Delta-Zeit verzögerte den Zustandsautomaten. Analytische Höhen-/Zustandszeit verwendet jetzt echte Spielzeit. Erfolgreiche vollständige Wiederholung und asynchroner Recorder.
5. Ein isolierter Kampf-Darstellungslauf wurde durch einen Wildkampf unterbrochen. Das Party-Review stellt persistente Zustände wieder her und kann zuvor nur deaktivierte Wildakteure reaktivieren. Die isolierte Präsentationsprüfung entfernt Wildakteure deshalb ausschließlich aus ihrer eigenen PIE-Instanz; die echten Begegnungs-, Fang- und Fußlauftests behalten normale Spawns. Der fehlgeschlagene Lauf bleibt lokal dokumentiert.
6. Der erste Überhangvergleich blockierte bereits die bestehende große Boden-Navigationskapsel und war damit kein isolierter Hover-/Bodenvergleich. Die Wiederholung verwendet eine seitlich-diagonale Prüfanordnung; die Produktions-Kapselmaße werden nicht geändert.
7. **Externe Engine:** `idevice_id` der installierten UE-Version startet auf ARM mit Fehler 86/Bad CPU type. Im ersten vollständigen Automationlauf werden diese zwei Warnungen dem erfolgreichen `PokeMonster.NPC.MotionV3.AnatomicalLegAxes` zugeordnet. Der unveränderte strenge QA-Runner endet deshalb mit Code 1; Rohbericht meldet keinen fehlgeschlagenen Test. Eine zusätzliche Auswertung trennt diesen bekannten externen Befund, unterdrückt keine Meldung und lehnt unbekannte Warnungen/Testfehler weiterhin ab.
8. **Engine-Startmeldungen:** `UE::UnifiedErrorTest` und unmittelbar folgende `LogAutomationTest: Condition failed` beim Start bleiben im Rohlog erhalten; getrennt von der später ausdrücklich gestarteten PokeMonster-Suite dokumentiert.
9. **Vorhandene Projektwarnungen, keine externen Engine-Warnungen:** `MI_WLA_LeafOak` und `MI_WLA_Stone` melden in der bestehenden Battle-Umgebungsinstanzierung fehlendes `InstancedStaticMeshes`-Usage und möglichen Default-Material-Fallback. Diese unveränderten Umweltmaterialien wurden im Animationsauftrag nicht automatisch resaved. Neue V5-Gasmaterialien zeigen keinen Shader-Kompilierungsfehler.
10. **Aufnahmebedingte Hinweise:** Einzelne `CharacterMovement`-MaxSimulationTimeStep-/PSO-Hitches bei Start/Readback; keine daraus erfundenen Leistungswerte. Der vorhandene AVFoundation-Encoder kompiliert mit API-Deprecation-Hinweisen; Videos wurden tatsächlich geschrieben, nicht als fehlend übersprungen.

## Empfehlung und verbleibende Grenzen

Technischer Zwischenstand zur echten visuellen Abnahme: neue Flügelbewegungen mit begrenztem Schweben, freies Nebulak-Gesicht mit dynamischer transparenter Hülle und weichere Spielerübergänge sind aktiv. Keine Produktionsfreigabe allein aufgrund grüner Assertions. Die Filme zeigen die tatsächliche Spielkameradistanz; ihre künstlerische Bewertung liegt beim Nutzer.

Offen bleiben ein vollständiges prozedurales Fuß-Locking bei engen Spielerwendungen, eine vollständige geometrische Selbstkollisionsgarantie jeder Glurak-Zwischenpose, hochwertigere volumetrische Gasillusion in extremen Nahansichten, die genannten bestehenden Battle-Umweltmaterialwarnungen und der physische Switch-Pro-Test. Das neue Schweben bleibt an konservativ geprüfte Bodenwege gebunden. Keine weiteren Pokémon oder Art-Passes automatisch begonnen.

## Abschließender Schutzbefund

`VerifyProtection.py` bestanden: 1.393 inventarisierte Originaldateien unverändert, nur die zwei ausdrücklich übernommenen Spezies-Präsentationsverweise geändert; alle 51 geschützten unversionierten Dateien und der ursprüngliche Dev-Save stimmen exakt per SHA-256. Beide Vollbackup-Verweise sind unverändert. Keine Mapdatei geändert.

## GitHub-Sicherung

Implementierungscommit [`3b4724ca446c0aff17599d8a1d9cdd13a0d996f7`](https://github.com/Harrys-F/PokeMonster/commit/3b4724ca446c0aff17599d8a1d9cdd13a0d996f7), regulär nach `origin/main` gepusht und unmittelbar über `git ls-remote` bestätigt. 96 exakt geprüfte Commitpfade; 55 neue LFS-Objekte mit **108.188.690 Bytes**, normale benötigte Dateien vor Packkompression rund **1,30 MiB**. Keine Map, kein Kontrollbild, Video, Cache oder temporäres Rendering im Commit.

Alle 55 LFS-Objekte wurden nach Upload authentifiziert über Download-Batch, deklarierte Größe und je einen Bytebereich auf tatsächliche Verfügbarkeit geprüft; komplette SHA-256-Prüfung aller lokalen Payloads. Das ist **kein vollständiger Remote-Payload-SHA-256-Download**. Die Quittung liegt lokal unter `Saved/MotionRefinementV5/RemoteFeatureAvailability.json`; frühere Prüfquittungen wurden nicht überschrieben.

Aktuelle [GitHub-Grenzen](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits) und [LFS-Einzeldateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) vor Upload geprüft: keine normale Datei nahe 100 MiB, kein LFS-Objekt nahe 2 GB; normale Daten deutlich unter der Projektvorgabe 1 GiB pro Push. Keine Käufe, Budgetänderungen, Force-Pushes oder Backup-Referenzen übertragen.

Dieser abschließende Dokumentations-/Manifestnachweis wird separat gesichert. Kontrollbilder, Videos, Logs und temporäre Dateien bleiben ausschließlich lokal im ignorierten `Saved/`. Alle zuvor vorhandenen 51 unversionierten Dateien bleiben unverändert; der Git-Status ist deshalb absichtlich nicht vollständig leer.
