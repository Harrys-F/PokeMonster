# Projektbereinigung und Grafikverbesserung V2 – Prüfbericht

Stand: 19.10.2026. Aktives Projekt ausschließlich `/Users/harry/Developer/PokeMonster`.

## Ergebnis

17 → **11 Karten**. Sechs vollständig entkoppelte Kategorie-B-Karten entfernt, zwei Kategorie-B-Karten bewusst behalten. Keine neue Map, Projektkopie oder zusätzlicher Worktree. VisualV2 wurde direkt weitergestaltet. Technisch geprüft; die künstlerische Endabnahme bleibt Harry vorbehalten.

## Sicherheit und Kartenbereinigung

Ausgangspunkt `8cc96f91fdcffd40965989d6c2d4af159668625d`, Branch `main`, bestehendes GitHub-Repository. Alle **53 zuvor unversionierten Dateien** wurden anhand ihrer ursprünglichen SHA-256-Prüfsummen erneut geprüft und unverändert erhalten; dazu gehören die vier Kreaturen-GLBs und `Dev_TestMap_VisualV2EnvironmentQualityV1`. Sie werden nicht mit diesem Auftrag committed. Das Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt unter beiden bestehenden Backup-Refs erhalten. Kein Reset, Clean, History-Rewrite oder LFS-Prune.

Entfernt wurden ausschließlich:

| Assetpfad | Behandlung der Abhängigkeiten |
|---|---|
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV1` | Historische Testwerkzeuge explizit archiviert |
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV2` | Historische Testwerkzeuge explizit archiviert |
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV3` | Historische Testwerkzeuge explizit archiviert |
| `/Game/Maps/Dev_TestMap_RangerPerfV2` | Historische Testwerkzeuge explizit archiviert |
| `/Game/Maps/Dev_TestMap_TreeShadowProxyV1` | Historische Testwerkzeuge explizit archiviert |
| `/Game/Maps/Dev_TestMap_NPCMotionV2` | Aktuelle V3-Regression verwendet geprüfte unveränderliche V2-Akteurssignaturen |

69 historische Python-Einstiegspunkte wurden einzeln nach Entfernung aufgerufen: jeweils Exit 2 mit `HISTORICAL_MAP_REVIEW_NOT_EXECUTED`. Das ist ausdrücklich **kein erfolgreicher historischer Grafiktest**. Fehlende Archivkarten erzeugen keine Ersatzmaps. Fünf neue Python-Sicherheitstests des Map-Lifecycle bestanden. Die aktuelle NPCMotionV3-Prüfung besteht weiterhin gegen die erforderliche, SHA-256-gebundene Baseline von 1.351 ursprünglichen V2-Akteuren. Sie ignoriert keine unerwarteten Änderungen.

Der Pflichtdatei-Vertrag enthält die aktuellen Quellen und Tests weiterhin streng. Wiederherstellung der sechs historischen Karten ist anhand von `Tools/ProjectMaintenance/MapLifecycle.json`, Commit `8cc96f9` und erhaltenen LFS-Objekten möglich. Andere Assets wurden nicht gelöscht.

**Weiterhin behalten:** VisualV2, WestlandRegion, WestlandAssetLibrary, ursprüngliche Dev_TestMap, BuildingKitTestMap, HealingHouseTestMap, NPCMotionV3, VisualV2GPUBottleneckV1 und die geschützte unversionierte EnvironmentQualityV1. Zusätzlich bleiben **Dev_WestlandVillage** (eigenständige Mehrgebäude-/Cutaway-Prüfung) und **Dev_BattleTestMap** (separater Kampf-GameMode/UI-Test) bestehen. Ihre Testabdeckung wurde nicht nachweislich ersetzt; deshalb wäre ihre Löschung hier nicht gerechtfertigt. Startmap-Konfiguration unverändert.

## Tatsächliche grafische Bestandsaufnahme

Echte QHD-Spielkameraaufnahmen vor Bearbeitung: Wald, Wiese, Flussufer, Uferabzweig, Heilhaus, Fassade, Innenraum, Empfang, Heilbereich. Die vorhandene Welt war bereits dicht ausgestaltet; ein vollständiger Neubau wäre weder erforderlich noch angemessen gewesen.

Sichtbare Schwächen: gleichmäßige orange Erdflächen, sehr kleinteilige Waldbodenmotive, dünne Pflanzensäume, wiederholtes zweimetriges Innenbodenraster, wenig ausgearbeitete Stoffwirkung und harte Helligkeitsunterschiede im Heilraum. Architektur und Einrichtung waren funktional und wurden als Grundlage erhalten.

## Landschaft und Atmosphäre

- Vorhandene gemalte Gras-/Laubtexturen mit größerer, aus der Spielkamera besser erkennbarer Struktur; Waldboden-Skalierung 169 → 238 cm, sekundäre Stichprobe 281 → 379 cm, Wiesenstichprobe 240 → 296 cm.
- Erdwege mit zurückhaltender kühlerer Farbvariation, schwachen Tritt-/Verschleißbändern und unregelmäßigen Makroflächen. Vorhandene Wegmasken, Geometrie und Kollisionen unverändert.
- **563 zusätzliche Instanzen in 14 HISM-Gruppen**: ungleich gewichtete Wald-, Wiesen-, Ufer- und Eingangsinseln; bestehende Gras-, Farn-, Moos-, Klee-, Blumen-, Kräuter-, Schilf- und Kiesassets wiederverwendet. Freie Lichtungen, Interaktionsabstände und zentrale Gehbereiche werden ausgespart. Keine bestehenden Bäume oder Pflanzeninstanzen verschoben oder entfernt.
- Wasser: dezente animierte Flussbänder und seichte Farbvariation; vorhandene Ufermaske, Wasserfläche, Brücke und Kollision unverändert. Keine neue Wassersimulation.
- Bestehendes Beleuchtungssystem erhalten. Der vorhandene schattenlose Himmelsfüllanteil wurde maßvoll von 0,50 auf 0,65 erhöht. Das ist eine reale Beleuchtungsänderung dieses ausdrücklich erweiterten Auftrags, keine behauptete isolierte Schattenaufhellung. Sonnenrichtung/-intensität, Skylight, Lumen, TAA, Belichtung, Bloom und Kamerakonfiguration wurden nicht verändert. Keine FPS-/GPU-Benchmarkreihen.

## Heilhaus außen

Das bestehende Heilhaus V4 mit seinen vorhandenen Formen, Proportionen, Fenstern, Eingang und Dach bleibt die Grundlage. Keine zusätzliche Gebäudeversion.

- Private Materialvarianten für Holz, Fachwerk, Stein, Putz und Dach. Gemalte Oberflächen, Maserung, zurückhaltende Putzvariation sowie unterschiedliche Ziegel-/Mooswirkung verfeinert.
- Vorhandene `HouseCutaway`-Graphen und Parameter erhalten; Originalmaterialien als Referenz unverändert.
- Zwei kleine gebogene Holzstreben am bestehenden Vordach ergänzt und nach tatsächlichen Vordachabmessungen positioniert. Keine Änderung der Gebäudekollision oder Türöffnung.
- Weitere ungleichmäßige Gräser-/Blumen-/Kräutergruppen verbinden Vorplatz und bestehende Fassade.
- Keine pauschale Architekturvergrößerung: Die bereits brauchbaren Proportionen und Dachüberstände wurden bewusst erhalten.

## Heilhaus innen

Der vorhandene 12 × 10-m-Heilraum bleibt in derselben Map. Raumaufteilung, Möbelstandorte, Empfang, Betten, Türübergang, Kollisionen sowie Dach-/Wandfreistellung und Innenkamera erhalten.

- Alle 30 vorhandenen Bodenmodule mit einer gemeinsamen, weltbezogenen Dielenoberfläche: versetzte Brettstöße, dezente Brettfarbvariation und vorhandene gemalte Holztextur. Die geometrischen Modulnähte sind weiterhin vorhanden.
- Holz, Fachwerk, Putz, salbeifarbene Textilien und Leinen über private Materialvarianten harmonisiert. Tatsächlich vorhandene Holz-/Stofftexturen wiederverwendet.
- Neue Blender-Arbeitssets am Empfang, Kräutertisch und Wartetisch: glasierte Heilmittelgefäße, Korken, Papierschilder, Kräuterschale, Mörser und Stößel. Zwei bestehende hochwertige Topfpflanzen zusätzlich im Raum verwendet. Heilbereich über bestehende Betten, Kräuter und verständliche Materialakzente erhalten; kein neues Heilsystem.
- Fünf vorhandene warme Innenlichter in Intensität/Reichweite abgestimmt; sechs bestehende Fensterlichter von 5 auf 6 angehoben. Keine Lichtposition verändert, keine neuen Lichtquellen oder moderne Krankenhausausstattung. Exakte Werte stehen in `Art/HealingHouse/Refinement.json`.
- Die vorhandene Decken-/Dachkonstruktion wurde erhalten. Keine undurchsichtigen neuen Deckenbalken in die freigestellte Innenkamera gesetzt.

## Neue Quellen und Assets

Blender: `Art/HealingHouse/Source/HealingHouse_ApothecaryDetails.blend`, gespeichert und erneut geöffnet. Drei separate Detailobjekte, metrische Einheiten, UVs, ein gemeinsames opakes Vertexfarbenmaterial; kein Rig.

| Detail | Vertices | Dreiecke |
|---|---:|---:|
| HerbalRemedyTray | 1.897 | 3.624 |
| HerbalMortar | 468 | 760 |
| PorchCorbel | 160 | 316 |

Gesamt 4.700 Dreiecke für die drei Quelldetails, nicht für alle platzierten Instanzen. Bei der eigenen Geometrieprüfung wurden 40 kollabierte Blattspitzenflächen des neuen Arbeitssets erkannt und korrigiert. Die bereinigten FBX wurden tatsächlich erneut importiert; Unreal-Dreieckzahlen stimmen mit Blender überein, keine einfache Kollision erzeugt.

Drei FBX unter `Art/HealingHouse/Exports/SM_HH_*.fbx`. 16 private Materialassets und drei Meshassets unter `/Game/Environment/VisualV2HealingArtV4/{Materials,Meshes}`. Keine Originalassets überschrieben. Quellen, Materialgraphen und Zuordnungen: `Art/HealingHouse/{ApothecaryDetails.json,Refinement.json,RefinedGraphs.json}`. Pflanzenanordnung: `Art/World/VisualV2WorldArtV7/RefinedPlanting.json`.

## Visuelle Prüfung und Grenzen

Die erste eigene Materialfassung wurde **nicht** als fertiges Ergebnis übernommen: unruhige Bodenmaserung und zu flache Stoffe wurden anhand echter Aufnahmen erkannt und mit den vorhandenen gemalten Texturen korrigiert. Die neue Strebenposition wurde ebenfalls überprüft. Die fertige Aufnahme zeigt ruhigere Dielen, erkennbare Stoffstruktur, zusätzliche Arbeitsdetails und ungleichmäßigere Pflanzeninseln.

Das Ergebnis ist eine gezielte sichtbare Weiterentwicklung, kein vollständiger Neuaufbau oder Beweis für bereits erreichte finale AAA-Artqualität. Weiterhin sichtbar: teilweise breite, recht gleichmäßige Erdwege; starke Sonnenkontraste; einzelne ältere Farne und Pflanzen wirken flacher als die besten V4-Pflanzen; Innenboden-Modulnähte und einfache Teppichsilhouetten bleiben erkennbar. Wasser erhält nur einen zurückhaltenden Materialpass. Es wurde keine neue Flussgeometrie, Fensterarchitektur oder Decke erfunden. Kleine Heilmittel sind aus normaler Spielentfernung Akzente, keine groß lesbaren Hauptobjekte. Eine eigenständige manuelle Bewegungs-/Flimmerabnahme durch Harry bleibt sinnvoll.

## Technische Prüfungen

- Phase 1: Mac Development Editor Build bestanden, **49/49** Automationstests ohne Testwarnung/Fehlschlag/Skip; alle damaligen 17 Map Checks 0 Fehler/0 Warnungen.
- Nach Kartenentfernung: Build bestanden, erneut **49/49**; alle elf verbleibenden Map Checks 0/0. NPCMotionV3-Vergleich gegen ursprüngliche V2-Signaturen bestanden.
- Abschluss nach Art-Änderung: Mac Development Editor Build bestanden; **49/49** ohne Testwarnung/Fehlschlag/Skip; alle **elf** verbliebenen Karten erfolgreich geladen und jeweils Map Check 0 Fehler/0 Warnungen. Keine andere Map gespeichert.
- Strenge Szenenprüfung: 1.397 ursprüngliche Szenenakteure erhalten; bestehende Positionen, Meshgeometrien, Instanzdaten, Kollisionen, Gameplay-Properties, Kameras und WorldSettings unverändert. Nur dokumentierte Materialbindungen und Lichtwerte geändert. 22 neue rein visuelle Akteure, davon 14 HISM-Gruppen; alle ohne Kollision.
- Vollständiger echter eingebetteter PIE-Fußlauf: **102 Schritte**, **286,27 m**, 178,13 s Spielzeit / 209,93 s Wandzeit. Enhanced-Input-Bewegung ohne Testteleports. Menü, Wanderer-Dialog/Quest, Wildkampf/Fang, Liora, Archiv, Brücke, Heilhaus, gerader/diagonaler Eintritt und Austritt, Heilung/Checkpoint/Save/Load, alle acht Richtungen, Kronenfreistellung, NPC-Sprite-Fallback und Sprint geprüft. Gehgeschwindigkeit 210 cm/s, maximaler Sprint 315 cm/s; FOV 35°. Ursprünglicher Dev-Spielstand anschließend SHA-256-identisch restauriert.
- Neun Vorher/Nachher-Paare: tatsächlicher Game-Viewport **2560 × 1440**, High, 100 % Screen Percentage, eingebetteter PIE. Kameraposition/-rotation pro Paar numerisch geprüft. Foto-Positionierungen sind ausdrücklich keine Fußlaufprüfung; der Fußlauf erfolgte separat ohne Teleports.
- Kein neuer Standalone-/720p-Test und keine Performanceverbesserung behauptet. Keine Benchmarkreihe durchgeführt.

Es gab während der Werkzeugentwicklung korrigierte Python-API-/Sitzungsfehler (Vertexfarben-Pin, fehlender Import im Fortsetzungsskript, relativer Projektpfad, Eigenschaftenabfrage, leere Registry-Rückgabe). Sie sind keine bestandenen Tests; die korrigierten Prüfungen wurden erfolgreich erneut ausgeführt. Der zusätzliche Headless-Registry-Wrapper meldete trotz abgeschlossener Referenzprüfung Exit 1; dieselbe Prüfung wurde deshalb im regulären frischen Editor erfolgreich wiederholt. Der ausführliche Editorlog enthält außerdem bekannte macOS-/Engine-Meldungen zu nicht ausführbarem `idevice_id`, Audio-Samplerate, Netzwerk-/EOS-/Telemetrie und Engine-Startup-Selbsttests. Daher wird ausdrücklich kein vollständig warnungsfreier Editorlog behauptet. Der Build-/Projekt-Automationserfolg und die Map-Check-Zahlen beruhen auf den jeweiligen tatsächlichen Ergebnisdateien.

## Nachweise und Bildvergleiche

Lokale, optionale Kontrollmedien werden nicht auf GitHub hochgeladen. Sie sind für Build, Gameplay oder Wiederherstellung nicht erforderlich.

- **Wald:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Wald00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Wald00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Wald.jpg).
- **Wiese:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Wiese00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Wiese00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Wiese.jpg).
- **Flussufer:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Flussufer00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Flussufer00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Flussufer.jpg).
- **Uferabzweig:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Uferabzweig00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Uferabzweig00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Uferabzweig.jpg).
- **Heilhaus:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Heilhaus00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Heilhaus00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Heilhaus.jpg).
- **Fassade:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Fassade00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Fassade00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Fassade.jpg).
- **Innenraum:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Innenraum00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Innenraum00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Innenraum.jpg).
- **Empfang:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Empfang00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Empfang00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Empfang.jpg).
- **Heilbereich:** [QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Before/Heilbereich00000.png), [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/After/Heilbereich00000.png), [direkter Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/Comparisons/Heilbereich.jpg).

Die erforderliche aktuelle Szenensignatur wird in `Tools/ProjectMaintenance/ArtSignatures.json` versioniert. Dadurch hängt die spätere strenge Zustandsprüfung nicht von optionalen Kontrollbildern oder `Saved/BeforeScene.json` ab; die ursprüngliche detaillierte Vorher-Nachher-Prüfung ist lokal nachvollziehbar. Maschinenlesbare zusammengefasste Prüfergebnisse werden unter `Tools/ProjectMaintenance/Acceptance.json` versioniert. Detaillierte lokale Logs und Ergebnisse stehen unter `Saved/ProjectRefinement/`: `FinalBuild/Result.json`, `FinalAutomation/Report/index.json`, `FinalMapQA.json`, `FinalReferences.json`, `ArtValidation.json`, `PhotoValidation.json`, `Acceptance/Final/FootTest.json`, `Acceptance/Final/SaveRestored.json` und `ProtectedValidation.json`.

## GitHub-Sicherung

1. `34e8bca0f9d14a817920800e52672f194ece4154` – aktuelle Prüfungen von historischen Map-Fixtures entkoppelt; regulär gepusht, Remote verifiziert.
2. `702201ea39ae7f078238d571d9ff32214eb48ed5` – sechs geprüfte Altkarten entfernt; regulär gepusht, Remote verifiziert.
3. Das erfolgreich geprüfte Art-Paket und dieser Bericht werden gemeinsam gezielt gesichert. Der konkrete abschließende Commit-Hash wird in der Abschlussmeldung genannt; so entsteht keine zirkuläre Selbstreferenz dieses Berichts. Vor Commit: exakter Index, LFS-Zuordnung und `git diff --cached --check`. Nach Push: Remote-Commit und tatsächliche SHA-256-Verfügbarkeit der neuen LFS-Dateien unabhängig prüfen.

Keine Kontrollbilder, Videos, Caches, Builds oder Spielstände werden gestaged. Die unveränderten 53 fremden unversionierten Dateien bleiben lokal. Keine automatische weitere Bereinigung oder Ausweitung nach diesem Auftrag. Empfehlung: diesen Stand anhand der neun Bildpaare visuell abnehmen; Village/BattleTest erst nach expliziter Ersatz-Testabdeckung erneut zur Entfernung bewerten.
