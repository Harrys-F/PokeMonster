# Westland Environment Polish V2

Stand: 02.11.2026. Ausgangscommit `1c711b4ac6c528889f15376452fa3c683628cc60`. Bestehendes Projekt `/Users/harry/Developer/PokeMonster`; ausschließlich vorhandene Zielmap `/Game/Maps/Dev_WestlandRegion`. Tatsächlich installierte Engine 5.8.4/CL58902052, Apple M4 / 16 GB, Metal. Keine Engineinstallation oder neuen Abhängigkeiten.

## Ergebnis und verwendete Referenzen

Der Auftrag ist eine sichtbare Verdichtung und Überarbeitung der bestehenden Fantasy-Region. Die vier bereitgestellten Bilder dienen als gestalterische Referenz für geschichteten Wald, Blumenwiesen, klares Flusswasser und eingebettete Felsen. Sie wurden weder als Spieltexturen importiert noch als Unreal-Nachweis ausgegeben. Bestehender Hobbit-Dorfaufbau und Third-Person-Kamera bleiben erhalten. Keine neuen Pokémon-/Vegetations-/Felsmodelle erzeugt, keine Downloads und keine Wiederherstellung des verworfenen Buchenwalds.

Die Überarbeitung verwendet vorhandene Projektassets, 32 zusätzliche instanzierte Gruppen und ausschließlich Westland-eigene Material-/Geländederivate. Die offene Region erhält dichtere Teilbereiche und blühende Wiesen, keine gleichmäßige flächendeckende Waldwand. Die künstlerische Abnahme erfolgt anschließend durch Harry im Spiel; keine Behauptung, die fotografischen Referenzen vollständig erreicht zu haben.

## Tatsächlicher Ausgangszustand

Bestandsaufnahme beider Maps im Editor: `Inventory.json`, `Assets.json`, `AssetDetails.json`, `Dev_WestlandRegion_Before.json`, `Dev_TestMap_VisualV2_Before.json` unter `Saved/ProjectRefinement/WestlandEnvironmentPolishV2/`.

Westland bestand aus 80 separaten statischen Gelände-Meshkacheln mit 2 m-Raster, **keinem Unreal-Landscape-Actor**. Vorhanden waren1.710 3D-Bäume,6.668 3D-Büsche,18.167 umgebundene Grasinstanzen,21.613 V1-Detailgrasinstanzen,6.394 Wiesenkräuter und nur vereinzelte Farne/Moos/Wurzeln.503 grobe 80-Dreiecks-Felsgruppen prägten unter anderem die Ufer. Das bisherige Wasser war ein gewöhnliches transluzentes Lit-Material mit einer zu schmalen Oberfläche gegenüber dem tatsächlichen Bett und teilweise zu hoch liegendem oberen Flussniveau gegenüber angrenzendem Land.

Der Grundverlauf, Wasserhöhen, Dorf, Wege, Gebäude und16 Lebensräume waren vorhanden. Diese Struktur wird erweitert, nicht durch eine neue Region ersetzt.

## Vegetationsdichte und Waldaufbau

| Inhalt | Vorher | Ergänzung | Final |
|---|---:|---:|---:|
|Größere Bäume|1.710|1.061|2.771|
|Junge Bäume/Saplings aus vorhandenen Baumvarianten|0 zusätzliche|583|583 zusätzliche|
|Bäume insgesamt|1.710|1.644|**3.354**|
|Buschgruppen|6.668|1.233|**7.901**|
|Farne|189|601+3.524|**4.314**|
|Neue Wildblumengruppen|0|12.369|**12.369**|
|Vorhandene Wiesenkräuter|6.394|0|6.394|
|Zusätzliche neue Grasgruppen in V2|0|39.795+983 Ufergras|40.778|
|Zusätzliches Moos|0 zusätzliche|706|706 zusätzliche|
|Zusätzliches Ufer-Schilf|154 vorhanden|487|641|

Die V2-Grassumme39.795 umfasst37.249 Wiesen-,1.134 Wald- und1.412 Waldtaschen-Instanzen. Vorhandene V1-Grasbestände bleiben zusätzlich erhalten. Instanzzahlen zählen vollständige Tufts/Pflanzengruppen, nicht einzelne Halme/Blätter. Sie sind keine Behauptung einer überall gleich hohen optischen Dichte.

Verwendete Bäume: vorhandene `SM_WLA_OakAncient_V3`, `SM_WLA_OakYoung_A/B`, `SM_WLA_Birch_A/B`; vorhandene Obstbäume aus V1 bleiben erhalten. Neue Baumgruppen liegen vorwiegend im östlichen Wald und am vorhandenen westlichen Waldsaum. Unterschiedliche Größen und Abstände, überlappende Kronen, junge Bäume, niedrigere Buschgruppen, Farne/Moos und Gras schaffen mehrere Höhenstufen. Die ursprünglichen1.710 Standorte bleiben erhalten; zusätzliche Bäume sind eigenständige HISM-Instanzen.

Neue Unterholzmeshes: `SM_WLA_WildBush_V3_A/B`; Farne: `SM_WLA_Fern_A/B`; Gras: `SM_EQ3_GrassShort/Meadow/Woodland`. Pfade, Hausumfelder, NPC-/Fundstellen, bedeutende Ortsplätze und die bestehende Lichtung werden ausgespart. Ausschließlich die bereits importierten einfachen Stammhüllen blockieren Player/Kamera; Blätter, Büsche, Blumen und Bodenpflanzen sind keine neuen Bewegungshindernisse. Kein globales Schatten-/LOD-/Renderingprofil verändert. Kleinvegetation hat begrenzte Sichtweiten und keine zusätzlichen feinen Schatten.

Waldmaterialien verwenden vorhandene gemalte Texturen und eine weichere Waldbodenmischung. Dichte wurde anhand echter Third-Person-Aufnahmen nachjustiert: Zusätzliche Farn-/Moostaschengruppen schließen sichtbare Lücken am Waldboden, statt lediglich eine große Zielzahl zu behaupten.

## Blumenwiesen

Ausschließlich das vorhandene Mesh `SM_WLA_Wildflowers_A` unter `/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/`,2.160 Dreiecke, fünf vorhandene Materialbereiche. Keine Topfpflanzen aus dem Heilhaus als Wiesen-Ersatz. Map-eigene Materialinstanzen variieren ausschließlich vorhandene Blüten-Tints: Creme/Weiß, Gelb, Blau, Violett, Rot und Rosa. Blatt-/Stängelmaterialien bleiben erhalten.

Verteilung: zusammenhängende blühende Abschnitte an der Wildwiese, kleinere unregelmäßige Gruppen am Hof/Dorf, freie Wieseninseln, Wegränder und sonnige Lichtungsbereiche; unterschiedliche Höhen und lokale Farbschwerpunkte. Keine identischen Farbraster. **Keine botanisch eigenständigen Mohn-, Kornblumen-, Butterblumen- oder Glockenblumenmodelle nachgewiesen.** Die sechs Farben sind Varianten desselben vorhandenen generischen Wildblumenmodells und werden nicht als sechs neue Arten ausgegeben.

## Wasseroberfläche und Flussgeometrie

Neue lokale Ableitung `M_WEP_FlowingRiver`: Unreals **Single Layer Water**, opaque Oberflächenpfad mit tatsächlicher Volumen-Transmission statt gewöhnlicher Alpha-Fläche. Ausgangspunkt ist die vorhandene regionale Wasserableitung; die ursprünglichen V1- und VisualV2-Materialien bleiben unverändert. Vorhandene gerichtete zeitabhängige Normalwellen führen den Fluss optisch; keine neue Wasserphysik oder Änderung des globalen Renderprofils.

Finale Materialwerte: Opacity/Surface-Volume-Mix 0,32, Roughness 0,11, Specular 0,5; Scattering(0,001/0,0025/0,0018), Absorption(0,0045/0,0019/0,0011), PhaseG 0,35, ColorScaleBehindWater(0,92/0,98/0,94). Diese Opacity ist bei Single Layer Water kein gewöhnlicher Alpha-Transparenzwert. Die neue Oberfläche lässt Kies und Bett durchscheinen, färbt tiefere Bereiche grünlich/blau und reflektiert die Umgebung blickabhängig. Tatsächlicher Metal-Pfad durch Shaderkompilierung, Spielansicht und gemessenen `GPU/SingleLayerWater`-Pass belegt; nicht lediglich über eine Projekteinstellung angenommen.

Die vorhandene `SM_WR_River` bleibt als Original erhalten. Nur die in Westland gebundene Ableitung `SM_WEP_River` wird bearbeitet: gleiche Topologie, UVs und ursprüngliche Wasserhöhen, begrenzte Variation von Verlauf/Breite. Die äußeren Oberflächenränder werden gegen tatsächliche Terrain-Schnittpunkte geprüft und in die Böschung geführt. Gemessene Breiten der geprüften Reihen ungefähr5,8–14,55 m; durch asymmetrische Ufer können lokale Oberflächenmittelpunkte verschoben werden. Der grundsätzliche Flussverlauf bleibt erkennbar, **keine Behauptung einer exakt unveränderten Mittellinie**.

Der ursprüngliche obere Fluss lag teilweise höher als seine Ufer. Dafür sind innerhalb eines begrenzten Uferkorridors zusätzliche weiche Geländeübergänge notwendig: zehn vorhandene Kachelableitungen, maximal 9,68 m lokale Anhebung am oberen Fluss. Die Fläche wird nicht einfach breit über flaches Land gelegt. Wege, Brückenanschlüsse und Gebäudepads sind von diesem Eingriff ausgeschlossen. Außerhalb der vorhandenen Terrainabdeckung am äußersten Wasserende bleibt die alte Kulissenbegrenzung erhalten; keine neue Hauptweltfläche.

Flussbett: vorhandene gemalte Erde mit feuchterer Färbung und3.485 tatsächlichen `SM_WL_NG_PebbleSmall/Cluster`-Instanzen. Keine neue Kieselmodelle oder künstliches regelmäßiges Punktmuster: Ein solches zunächst getestetes Shader-Muster wurde nach Sichtprüfung entfernt. Felsen,487 zusätzliche Schilf- und983 Ufergrasgruppen ergänzen unregelmäßige Ränder. Keine neue Planar-Reflection, globalen Wasser-CVars oder Wasser-Plugininstallation.

16 Habitat-Actors einschließlich drei flacher Wasserabschnitte, Spielerbarrieren und Brücken bleiben erhalten. Wasser-Kollision bleibt beim vorhandenen System; kein neuer Schwimm-/Unterwasser-Controller. Kein Garados-Spawn oder Änderung an Garados V4: Die vorhandenen Habitatfreiräume und Tiefen reichen weiterhin nicht für seine konservative Körperhülle.

## Gelände und Felsen

80 map-eigene Ableitungen der existierenden Gelände-Kacheln, keine neu erfundene Ersatzlandschaft. Vertices werden begrenzt verändert, Topologie/UVs und jeweils 5.000 Dreiecke erhalten; zusammen 400.000 Geländedreiecke. Kleinere unregelmäßige Höhen, weichere Übergänge an den bestehenden drei Erhebungen und weniger gleichmäßige äußere Höhenkulissen. Fernkulissen im 100 m-Rand dürfen stärker verändert werden; größte ursprüngliche Vertexverschiebung vor Uferkorrektur 37,26 m am äußeren Hintergrund, kein pauschaler37m-Eingriff im Dorf.

Eine gemeinsame ortsabhängige Gewichtung spart Wege, Gebäudeflächen und wichtige Pads aus. Numerischer Endabgleich: **0 cm Kachelrandabweichung**, **0m Höhenänderung auf den geschützten gesampelten Wegmittellinien**. Vegetation wird nach Gelände- und Uferbearbeitung erneut auf die tatsächlichen Meshflächen projiziert. Keine Actor-Versetzung von Häusern, NPCs, Quests, Gegenständen oder Habitaten.

Die503 alten groben Crag-Instanzen sind durch1.509 vorhandene `SM_WLA_Boulder_A/B` ersetzt, jeweils1.280 Dreiecke, in zusammenhängenden Dreiergruppen, variiert in Rotation/Proportion und teilweise eingebettet. Die alte HISM-Gruppe bleibt leer und ohne doppelte Kollision. Neue Felsen verwenden die vorhandenen einfachen konvexen Hüllen sowie das bereits vorhandene `MI_EQ3_MossStoneInstanced`. Keine neu modellierten Felsen oder bearbeiteten Bibliotheksoriginale.

## Reproduzierbare Performance

Echte PIE-Messung im selben eigenen Editor, QHD2560×1440, ProfilC/High,75%TAAU, Software-Lumen/IFG, vier VSM-Strahlen. Keine Videoaufnahme. Fünf definierte Standorte, jeweils drei Durchläufe mit 3 s Standort-Warm-up und 6 s Messfenster. 12:00 Uhr angehalten für vergleichbare Licht-/Schattenbedingungen, kein deaktiviertes GI-/Schatten-/Vegetationsfeature. Die laufende Welt wird separat im nativen Rundgang geprüft.

Die Positionen werden gleich angefordert, Blickrichtung/FOV/Kameraarchitektur bleiben gleich. Wo Gelände verändert ist, folgt die reale Kamera der neuen Bodenhöhe; deshalb sind nicht alle Kameraweltpositionen pixelgenau identisch. Die Messungen bilden den tatsächlichen vorherigen bzw. neuen Spielausschnitt ab, keine isolierte Material-A/B-Kostenermittlung. Reihenfolge erst vorher, dann nachher, drei Wiederholungen; thermische Drift und Fensterfokus wurden nicht separat instrumentiert. Rohwerte und CSV-Aufschlüsselung: `PerformanceResolved.json`.

|Ort|FPS vorher|FPS final|GPU vorher ms|GPU final ms|Finale Frame-p95 ms*|Final Game Thread ms|
|---|---:|---:|---:|---:|---:|---:|
|Dorf|32,66|31,52|29,01|30,36|35,28|9,00|
|Blumenwiese|30,78|27,45|30,16|34,80|38,44|9,70|
|Waldweg|32,12|26,45|29,87|36,31|40,32|9,14|
|Dichter Wald|30,82|28,14|31,20|34,21|38,50|8,89|
|Fluss|30,59|28,78|31,49|33,42|36,92|9,03|

*FPS/GPU/Game Thread sind Mittel der drei Fensterwerte; p95 ist hier ebenfalls der Mittelwert der drei Fenster-p95, kein gemeinsam gepooltes Perzentil. Ein allgemeiner stabiler 30 FPS-Nachweis liegt nicht vor. Die Dichte wurde nicht zur stillen Erfüllung eines Leistungsziels wieder reduziert.

Base Pass: Dorf5,38→5,38 ms, Wiese6,49→8,37 ms, Waldweg5,62→9,10 ms, dichter Wald6,42→7,18 ms, Fluss6,33→6,51 ms. Der aufwendigere sichtbare Pflanzenbestand erhöht nachweislich unter anderem diesen Pass; die gesamte GPU-Differenz wird nicht allein ihm zugeschrieben. ShadowDepths bleiben in diesen pausierten Mittagsfenstern ungefähr1,7–1,9 ms. SingleLayerWater ist im finalen Flussfenster tatsächlich messbar, beispielsweise1,08 ms im dritten Fenster. Überlappende GPU-Passbereiche wurden nicht ungeprüft addiert.

RenderThreadTime meldet in der Vorher-Reihe nur etwa0,001 ms und ist dort offensichtlich kein belastbarer Arbeitszeitwert. Die finale Reihe meldet einschließlich Warte-/Synchronisationsanteilen etwa31–37 ms. Daraus wird **keine**31 ms-Render-Thread-Regression abgeleitet. Game-Thread-Mittel liegen ungefähr8–11 ms vorher bzw.9–10 ms final. Keine globale Performanceoptimierung, Qualitätsabsenkung oder neue FPS-Garantie.

## Technische und Gameplay-Prüfung

- Editor-Build `BuildFinal`: Exit0,17,37s. Nur vorhandener gespeicherter Art-Regressionstest an den neuen zulässigen River-Derivat-/SingleLayerWater-Vertrag angepasst; kein Gameplay-C++ geändert.
- `AutomationFinal`: **325/325 erfolgreich**,0 Warnungstests,0 Fehler,0 Skips;49,64s; Engine0 und **strenger QA-Wrapper Exit0**. Derselbe vollständige Projekt-Test-/Report-Vertrag mit isoliertem UserDir, keine abgesenkten Erfolgsschwellen.
- Zwölf bestehende Map Checks: jeweils0 Fehler/0 Warnungen, `MapCheckParsed.json`. Keine Referenzmap gespeichert.
- `SceneAudit.json`:3.130 ursprüngliche beobachtete Actors→3.162, genau32 neue Instanzgruppen. Alle ursprünglichen Actor-Transformationen und geschützten Gameplay-/Lichtsignaturen erhalten; Änderungen an ursprünglichen visuellen Komponenten eng begrenzt. Weltsettings gleich, keine zusätzliche Karte.
- `PIERegressionFinal`: bestanden. Ursprüngliche vier NPC-Interaktionen, natürliche Begegnung, reguläre ClassicBattle-Attacke/AP-Verbrauch und Fang, Team/Begleiter, Heilhaus hinein/heraus, Heilung/Checkpoint, eigener Menü-Save/Load mit vollständigem Daten-/Zeit-/Positionsvergleich, alle drei Funde und deren Persistenz sowie Tageszeitproben06/12/19/22. Die diagnostische Standortwahl dieses kurzen Laufs ist kein Fußrundgang.

- **Vollständiger separater Rundgang `NativeTour03`: bestanden**,3.382,22m echte Enhanced-Input-Bewegung,667,08s Wandzeit. Dorf, Wildwiesen, Uferpfad, Mühle, Holzbrücke, Hof, Gasthausfront, Heilhaus innen/außen, Nordrunde/Steinkreis, Steinbrücke, Waldruinen und Regionsausgang. Keine Testteleports; genau zwei große Positionswechsel durch den regulären ausgelagerten Heilhaus-Ein-/Ausgang. Faktor3 außen, ausdrücklich Faktor1 am Türübergang; vor eigenem regulären Menü-Save wieder1. Prozess normal mit0 beendet.
- `NativeSpeed01`: bestanden,44,33s. Zwölf tatsächliche Geschwindigkeitskombinationen aus Software-WASD/Stickaktion, Faktoren1/2/3 und Gehen/Sprinten. Faktor3 weiterhin630/945 cm/s, Status und Rückstellung geprüft. Keine Kapselüberlappung am Stamm; Kamerakollision251,15 cm und Rückkehr350 cm.49 unabhängige Rayproben gegen die tatsächlich gekochte neue Geländekollision stimmen mit den erwarteten Höhen überein, maximale Abweichung0,00027 cm. Keine bloße Prüfung des sichtbaren Meshs.
- Frischer Laufzeitwert-Nachweis `NativeSpeed01/Graphics.json`:75%, TAAU1, Software-Lumen0/IFG0, VSM1/vier Strahlen; überprüfte Scalability-Werte jeweils2(High). Keine stille Reduzierung der Grafikqualität.

- `NativeWater02`: bestanden,80,83s.16 tatsächliche einfache Stamm-/Boulderhüllensweeps, vorhandene Flussbarriere hält Faktor3-Sprint;74 natürliche Karpador-Proben bei0–26,25 cm/s innerhalb gültiger Wasserhabitate, Idle/Rest/Wander beobachtet, maximal6 aktive Pokémon. Keine Spawn-/KI-Overrides. Kamera für den natürlichen Offscreen-Spawn zunächst vom Wasser weg, danach zum Fisch.
- Zusätzliche native Bankprüfung: 118 Stichproben zwischen den bearbeiteten Wasserreihen sind durch die tatsächlich gekochte Terrainkollision überdeckt; keine positiv über dem Ufer liegende Kante an diesen Proben. Das ist eine Stichprobe, kein lückenloser Test jedes Oberflächenpixels.
- `NativeRestart01`: bestanden,13,50s. Neuer Prozess lädt ausschließlich den eigenen erfolgreichen Tour03-Save; exakte individuelle Pokémon-/AP-/Positions-/Weltzeitdaten und Begleiter bleiben erhalten. Echter OpenLevel-Wechsel nach unverändertem VisualV2 und normales Laden zurück nach Westland funktionieren. Neuer Pawn/Fresh Start wieder Testfaktor1. Beide Prozesse regulär mit0 beendet.

Der lange native Rundgang liefert18.397 Frameintervallproben:27,58 FPS Mittel,31,68msMedian,61,86msFrame-p95. Diese Werte enthalten13 Screenshots, Menü, Regionen-/Innenraumwege und wechselnde Beleuchtung. Kein sauber isolierter GPU-Benchmark; die Spitzen wurden nicht kausal vollständig profiliert. **Auch dieser reguläre laufende Weltzustand beweist keine stabilen30 FPS.**

### Bestehende Einschränkung des beschleunigten Türübergangs

Der erste vollständige `NativeTour02` bei durchgehend Faktor3 ist nach2.087,13m fehlgeschlagen: Nach dem Heilhausausgang blieb die Figur räumlich beim ausgelagerten Raum, obwohl das Zustandsflag später bereits Außenraum signalisierte, und lief über dessen Bodenrand. Der Lauf gilt nicht als bestanden.

Gezielte native Kontrollen `NativeDoor03/04`: Faktor1 funktioniert. Faktor3 scheitert mit und ohne Sprint; die Kontrolle mit **ursprünglichen Terrain-Meshes und deaktivierten neuen WEP-Zusatzkollisionen** reproduziert es ebenfalls. Die Diagnose zeichnet tatsächliche Positionen, Tür-Fade, absolute Zielposition und überlappende Komponenten auf. Beim schnellen Herauslaufen ist die Figur vor der räumlichen Umsetzung bereits etwas unter Bodenhöhe; die Zielkapsel überlappt dann `Ground` und `WR_Terrain_01_05`. Die unveränderte vorhandene Relocation lehnt das Ziel folgerichtig ab. Diese Kontrolle ist keine Behauptung eines vollständig auf den historischen Gitstand zurückgesetzten Renderings.

Keine Änderung an der ausdrücklich geschützten Tür-, Kamera-, Innenraum- oder `pm.Speed`-Produktionslogik. Die Einschränkung bleibt als eigener bestehender Hochgeschwindigkeits-Grenzfall offen. Der erfolgreiche vollständige Rundgang verwendet deshalb normal dokumentiert Faktor1 am Heilhaus und Faktor3 außerhalb. Sein Prüfhelfer verlangt zusätzlich die tatsächliche richtige Raumseite statt nur das Relocation-Flag. Damit wird weder der erste Fehlversuch umbenannt noch eine uneingeschränkte Faktor3-Innenraumfreigabe behauptet.

Die ersten zwei Tür-Diagnoseaufbauten scheiterten an einer nicht vorhandenen Python-Vektormethode bzw. am erwarteten Listenwert bei leerem Overlap. Korrigiert wurden die Prüfhelfer; diese Aufbauten werden nicht als Gameplaykontrollen gewertet. NativeWater01 endete ebenfalls bereits im Prüfaufbau: Der alte150 cm-hohe Sweep ging über den kleinen Sapling-Hüllen vorbei. Die Probe verwendet jetzt die tatsächliche Spieler-Kapselhöhe50,15 cm statt einen pauschalen hohen Baum-Messpunkt. Keine Stammhüllen verkleinert oder deaktiviert.

Nachweise verwenden ausschließlich eigene isolierte Test-UserDirs/Slots. Die echte physische Gamepad-Hardware wurde nicht als geprüft ausgegeben; vorhandene Software-WASD/Stick-/L3-Tests sind davon getrennt. Kamera bleibt Third Person V3: ungefähr1,72m freie Bodenhöhe,−12°,350 cm freier Abstand, ausschließlich horizontaler Orbit. Weltuhr120 reale Minuten/Tag, Mittag75°, erhaltene85°Debugoption und bestehendes Renderingprofil unverändert.

## Echte QHD-Bildpaare

Alle nachfolgenden Dateien liegen unter `/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/WestlandEnvironmentPolishV2/`. Jeweils echte Westland-PIE-Aufnahmen, keine Referenzfotos oder generierten Nachweise.18 Dateien mit tatsächlich2560×1440 geprüft (`MediaAudit.json`).

|Motiv|Vorher|Final|
|---|---|---|
|Dichter Wald|`Before/DichterWald.png`|`AfterFinalBanks/DichterWald.png`|
|Waldrand|`Before/Waldrand.png`|`AfterFinalBanks/Waldrand.png`|
|Blumenwiese|`Before/Blumenwiese.png`|`AfterFinalBanks/Blumenwiese.png`|
|Waldweg|`Before/Waldweg.png`|`AfterFinalBanks/Waldweg.png`|
|Flussoberfläche|`Before/Flussoberflaeche.png`|`AfterFinalBanks/Flussoberflaeche.png`|
|Flussufer|`Before/Flussufer.png`|`AfterFinalBanks/Flussufer.png`|
|Hügel/Gelände|`Before/Huegelland.png`|`AfterFinalBanks/Huegelland.png`|
|Felsformation|`Before/Felsformation.png`|`AfterFinalBanks/Felsformation.png`|
|Hobbit-Dorf|`Before/Dorf.png`|`AfterFinalBanks/Dorf.png`|

Kameraabgleich `PairedCameraAudit.json`: sechs Paare bis auf Rundung identische Weltkamera. Am Waldrand rund29 cm, im dichten Wald108 cm und am Flussufer32 cm Abweichung durch geänderte Bodenhöhe/Kollision; Blickwinkel/FOV/Ausgabe gleich. Kein Eingriff in die Kamera, um diese Abweichungen zu kaschieren. Bewegliche Pokémon, Flammen und Wasserphasen sind nicht pixelidentisch eingefroren.

## Warnungen, Zwischenversuche und Grenzen

Die installierte Engine erzeugt weiterhin eigene Startmeldungen, darunter17 generische `LogAutomationTest: Error: Condition failed` vor der eigentlichen Projekt-Testreihe. Der Projekt-Report weist trotzdem0 Fehlertests aus. Native `-game`-Starts können experimentelle Engine-Toolset-Python-Fehler zu fehlenden `ToolsetDefinition`/`AgentSkill`/`PythonTestRunner`-Typen sowie Editor-Widget-Registrierungswarnungen melden. Kein global warnungsfreies Rohlog behauptet; keine Engine-/Pluginreparatur in diesem Auftrag. Die extern bekannte iOS-Helfermeldung `idevice_id: Bad CPU type in executable` trat in den ausgewerteten finalen Logs nicht auf und wurde hier nicht repariert. `LogClassification.json` weist diese Befunde getrennt aus. Alle vier finalen nativen Läufe enthalten0 Fatal-/Assertion- oder Material-Fallback-Meldungen, aber jeweils sieben genannte Engine-Toolset-Initialisierungsfehler.

Zwischenzeitliche Wasser-Compile-Warnungen entstanden beim Aufbau des Graphen, bevor Opaque-Blend und SingleLayerWater-Ausgabeknoten vollständig verbunden waren. Der fertige Pfad ist in den frischen nativen Logs ohne Material-Compile-/Default-Fallback geprüft. Ein unnatürliches regelmäßiges Kies-Shader-Muster wurde verworfen. Der erste Ufer-Schnittlauf erreichte das außerhalb des Terrains liegende äußerste Wasserende bzw. eine zu niedrige vorhandene obere Böschung; keine ungeprüfte Breitenvergrößerung übernommen. Die anschließende begrenzte Böschungskorrektur und der finale Schnittlauf sind separat dokumentiert. Ein reentrant aufgerufener Authoring-Generator wurde mit Busy-Guard korrigiert und aus unveränderten Ausgangsmeshes reproduzierbar neu ausgeführt; kein Editor-Force-Quit oder beschädigtes Original.

Die Region bleibt stilisiert. Die vorhandenen gemalten Texturen, einfachen Hintergründe und einzelne deutlich erkennbare Pflanzen-/Felswiederholungen sind nicht plötzlich fotorealistisch. Spezielle botanische Blumenmodelle fehlen. Wasserreflexionen bleiben blickabhängig und können nahe Felsen deutliche Wellenverzerrungen zeigen; keine endgültige künstlerische Wasserfreigabe behauptet. Einzelne durchscheinende Uferpflanzen, dunkle Unterseiten vorhandener Baumkronen, stellenweise noch deutlich abgegrenzte Wege und grobe Geländeübergänge bleiben mögliche Nacharbeit. Dorfplätze bleiben bewusst freier als Wald und Blumenwiese; nicht jede freie Fläche wurde vollständig bepflanzt. Kein vollständiges Unterwasser-/Erosions-/Flusssimulationssystem und keine globale Landschaftsneuerstellung.

Die gewünschte höhere Dichte kostet auf dem M4 messbar Leistung; insbesondere der Waldweg liegt im aktuellen Vergleich unter30 FPS. Eine spätere gezielte Vegetations-/Materialanalyse wäre ein eigener Auftrag. Kein heimliches Ausdünnen, Skalierungs-/Lumenwechsel oder Wiederherstellen des Buchenwalds. Nutzer entscheidet anschließend über die optische Wirkung.

## Schutz und Git-Abschluss

Vor Änderungen wurden6.122 versionierte Dateien,351 geschützte/unversionierte Dateien und692 bestehende Save-Dateien gehasht. Vor Abschlussdokumentation sind nur die beauftragte Map und der vorhandene zugehörige Art-Test verändert; alle351 geschützten Dateien und692 bestehenden Saves bytegleich. Die bereits lokal geänderte `Config/DefaultEngine.ini` ist gegen den lokalen Ausgangsstand unverändert und bleibt außerhalb des Commits. VisualV2, alle übrigen Maps, Originalmodelle/-animationen/-Blenderdateien, Fab-/Quixel-Dateien und sämtliche Gameplay-Quellen bleiben unverändert.

Gesicherte Produktionsinhalte sollen nur die geprüfte Westland-Map, neue regionale Derivate unter `Content/Environment/WestlandEnvironmentPolishV2`, zugehörigen Art-Test, Autoren-/QA-Werkzeuge und Dokumentation umfassen. Keine Saved-Medien oder bestehenden fremden unversionierten Dateien. Der ursprüngliche Westland-Stand bleibt im Ausgangscommit/LFS erhalten; vorhandene Vollbackup-Refs unverändert, keine zusätzliche Kopie oder neuer Worktree. Die nativen Abschlussprüfungen sind bis auf den getrennt dokumentierten vorhandenen Faktor3-Türgrenzfall bestanden. Regulärer Commit/Push und Remote-/LFS-Nachweis werden lokal unter `GitFinalVerification.json` erfasst; konkreter Commit im Abschlusschat. Danach keine weitere Bearbeitung vor Harrys Erkundung.
