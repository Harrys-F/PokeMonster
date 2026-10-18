# VisualV2 GPU Bottleneck V1 – tatsächliche Kosten und Diagnosegrenzen

17./18.10.2026 · UE 5.8.2 · MacBook Air M4, 16 GB · macOS/Metal SM6.

## Ergebnis

**Die zentrale Dev_TestMap_VisualV2 bleibt bytegleich. Kein Experiment wurde übernommen.** Separate, unverändert geklonte Diagnosekarte: `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1`.

402 reguläre Messabschnitte, 48 Baseline-Ortskonfigurationen und 129 gepaarte Einzelvergleiche ausgewertet. Alle Ausgaben, internen Renderer-Fractions, Kameraeinstellungen, stock Kontrollwerte und ausgeführten CVar-Eingriffe unabhängig geprüft. Zwei frische vollständige Automationsläufe mit jeweils 48/48 Success; Mac Development Editor Build und Map Checks erfolgreich. Details und Einschränkungen unten.

**Wichtigstes neues Performance-Ergebnis:** Ein wesentlicher Anteil des zuvor als „Unaccounted“ bzw. stark schwankender Postprocessing-Scope sichtbaren Blocks hängt funktional mit dem **TSR-/AA-Pfad** zusammen. TAA statt TSR spart im gepaarten QHD/High/100-Waldvergleich median 16,84 ms native Bildzeit bzw. 17,23 ms in PIE. Die entsprechenden GPU-Deltas sind 17,06/18,27 ms. Das ist keine reine Shader-Disassembly-Zeit und noch keine Qualitätsfreigabe für TAA. Lumen-GI und Schattenprojektion bleiben weitere erhebliche Kostenfaktoren.

**Korrektheitsblocker vor einer visuellen Freigabe:** Zwei HISM-Strauchgruppen mit 58 Instanzen verwenden ein V3-Blattmaterial ohne erforderliches Instancing-Usage-Flag. Standalone meldet den Fehler beim Start, vor jeder Diagnose, und zeigt graue Sträucher; PIE zeigt belaubte Sträucher. Die Originalmaterialien und beide bestehenden Maps wurden dafür nicht verändert. Absolute PIE-/Standalone-Zahlen sind daher getrennte Bestandsmessungen, kein bildgleicher Modusvergleich. Insbesondere native Vegetationskosten dürfen nicht als Budget einer bereits korrekt belaubten Endfassung ausgegeben werden.

**Empfehlung:** zuerst eine eigene Materialvariante mit korrektem Instancing-Support prüfen, danach TAA/TSR bei Bewegung, 75/100 %, Wald, Figuren und Innenraum vergleichen. Keine pauschale Vegetations-, Bloom-, Schatten- oder GI-Abschaltung.

## 1. Ausgangslage, Schutz und Messverfahren

Arbeitsstand: Slim-Worktree /Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree, Branch codex/slim-backup-v5, Ausgangs-HEAD/Remote 9181dbe17d45036f7d5d9ab797b3d0a61eca398c. Das alte lokale main und der Archiv-Ref bleiben auf 03492bd96b4dba44692f675c19d5f11abfa86b4b. Anfangs nur die frühere unversionierte V1-Testkarte und deren Werkzeuge vorhanden. 2.840 vorhandene Slim-Dateien durch SHA-256 erfasst; zentrale Map zusätzlich extern gesichert.

Unreal war anfangs nicht geöffnet. Keine fremde Editorsitzung verworfen, kein Save All oder Discard All. Separate Map ausschließlich über Editor-Save-As erzeugt: /Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1. Nach erneutem Öffnen vollständige Szenensignatur mit 1.348 Actors identisch, nur der Weltpaketname normalisiert. Die zentrale VisualV2 wurde nie gespeichert. Außen-MotionBlur=0 und Innenwert=0,5 bleiben erhalten; keine produktive AA-, GI-, Schatten-, Material-, Geometrie-, Vegetations-, Kamera- oder Gameplayänderung.

## Methodik

1280×720 und 2560×1440, Medium und High, jeweils 75/100 % Screen Percentage. 16 Baselinepläne, je drei Orte und drei Wiederholungen = 144 reguläre Baselineabschnitte. Warm-up 5 s, Messung 8 s. Native Prozesse sind UnrealEditor -game Development, keine paketierten Shipping-Builds. Native Fenster bei geschlossenem Editor; eingebettetes PIE statt schwebender Fenster.

Wald: zwölf Einzelfaktoren, beide Ausführungsarten, je drei zeitnah gepaarte Kontrollen. Mitte der drei Wiederholungen in umgekehrter Reihenfolge. 6 s Warm-up, 8 s Messung. Zusätzlich GI und Schattenverfahren an Dorf/Heilhaus und Weg. Engere native Postprocessing-Tests und AA-/Profiling-Gegenproben, später dieselben wesentlichen AA-Gegenproben in PIE. Die abgeschlossene Auswertung umfasst 402 reguläre Abschnitte und 43 gepaarte Diagnosegruppen.

Feste Player-Capsule-Punkte in cm: Dorf/Heilhaus (-4100,450,50,15), Wald (-4300,1550,50,15), Weg (-36,6,-47,1,50,15). Profiling-Teleports sind Positionskontrolle, kein Fußlauf. Kamera bleibt B: 2850 cm, Pitch -50°, Yaw -45°, FOV 35°. Keine Interaktionen oder Kämpfe im Messfenster, vorhandene NPCs im Idle.

Viewport, RenderTarget, ViewRect, Driver Primary/Secondary und Kamera pro Frame erfasst. Interne Dimensionen über tatsächliche Renderer-Fractions nach UE-Ceil-Regel abgeleitet; kein SceneColor-Allokationsreadback. 75 %: 960×540 bzw. 1920×1080; 100 %: volle Ausgabegröße. Fenster-/DPI-Werte und Aktivierung separat protokolliert. VSync und t.MaxFPS 0, Dynamic Resolution 0, Secondary Fraction 1. rhi.SyncInterval bleibt 1; Metal-Fensterpräsentation kann schnelle 720p-Fälle nahe 60 FPS begrenzen. Daraus keine CPU- oder GPU-Reserve behaupten.

FPS = 1000 / Median der drei Laufmediane. P95 = Median der drei Lauf-P95, kein gepooltes Gesamt-P95. Faktor-Delta = Median der drei gepaarten Differenzen, nicht Differenz unabhängiger Mediane. Einzelunterschiede erhalten; keine formale Signifikanzbehauptung aus kurzen Stichproben. Native Renderthread-Wallzeit enthält GPU-/Present-Warten. Nahe null liegende PIE-Renderthreadwerte und null Draw-Call-/Primitive-Zähler sind nicht als reine CPU-/Geometriekosten interpretierbar.

## Ausdrücklich verworfene und begrenzte Nachweise

Die ersten beiden VGB1_PIE_Base-Läufe verwendeten den historischen EnvPerfV2-Probe. Dieser erzwingt auch für Control das alte V1-Kandidatenprofil (IntegrateDownsampleFactor=2, VSM-Rays=2). Sie sind keine gültige zentrale VisualV2-Baseline und vollständig ausgeschlossen. Rohdaten bleiben erhalten. Der Probe nimmt neue VGB1_-Labels nun explizit von diesem alten Profil aus, ältere Experimentlabels behalten ihren Codepfad. Ausschließlich VGB1_Final_-Messungen auswerten. Kontrollwerte Integration 1, Gather 0/1, Rays 4/8 und AA-Methode 4 werden geprüft.

Initiale Inventur verwendete einen in dieser Python-API nicht exponierten AssetCompilingManager. Der lesende Aufruf wurde abgefangen/optional gemacht und wiederholt; keine Modelle verändert. Frühere Stop-Anforderung traf bereits beendetes PIE, kein erzwungener Editorabbruch. Reguläre saubere Schließungen vor Builds.

Extra Unreal ProfileGPU bei verifizierter QHD/High/100-Waldkamera erfolgreich. Nur einzelner Diagnoseframe, kein Median und kein Teil der Zeitvergleiche. Volle Tabelle im EditorMeasurementSession.log. Metal-Breadcrumbs teilen Stage-Counter; Leafnamen/verschachtelte Scopes nicht als addierbares Shaderbudget interpretieren. Der auffällige VSM-Log-Stats-Marker allein beweist keinen entsprechend teuren Statistikshader.

Metal System Trace: 15 s angefordert, Aufnahme erreichte ihr Zeitlimit, Finalisierung innerhalb 120 s nicht abgeschlossen. Harness beendete das CLI nach Timeout; Unreal selbst blieb bestehen, wurde danach regulär gestoppt/geschlossen. Teilaufzeichnung ca. 1,9 GiB extern erhalten. Kein zweiter Aufnahmeversuch und keine vollständige Hardwarekernel-Auswertung behauptet. Nicht in Git aufnehmen. Der unabhängige Unreal-Capture und die A/B-Messungen sind davon getrennt.

Enginequelle RHI/Private/GPUProfiler.cpp: Unaccounted wird für die WholeQueueStat verwendet; exklusive Zeiten ohne aktiven Stat enthalten Busy und Wait. CSV-Ausgabe erfasst Graphics Queue 0; verschachtelte GPU-/Async-Zähler nicht summieren. MetalProfiler.h löst Stage-Counter-Spannen auf. Funktionszuordnung durch gepaarte Umschaltungen ist tragfähiger als ein isolierter großer Leafwert.

## Bestandsbefunde

163 eindeutige Static Meshes, 1.029 Static-Mesh-Komponenten inventarisiert, kein Nanite-aktiviertes Static-Mesh-Asset. Das ist kein vollständiger Skeletal-/Landscape-Nanite-Audit; die globale Nanite-Abschaltung wird zusätzlich gemessen. Vegetationsgruppe: 41 V3-Eichen, vier Birken, 46 Strauchkomponenten sowie drei kleine HISM-Gruppen = 94 Komponenten. Komponenten sind keine Anzahl tatsächlich sichtbarer Instanzen oder Draw Calls.

LOD-Dreiecke: Eiche 12068/7240/3621; Birke 28628/17177/8588; Strauch A 3284/1971/986; B 3396/2038/1019; Farn 8030/4818/2409. Das sind Assetbestände, keine gemessenen gezogenen Dreiecke. Instanzen/LODs/MinLOD gesondert im Inventar.

Zur Laufzeit nutzen Baumkronen und Rinde Masked-Reveal-Materialien; Editor-Originalmaterialien allein reichen für den Audit nicht aus. Masked/zweiseitige Blattfamilien, keine angeschlossene WPO-Verformung in den untersuchten Graphen. Fünf laufzeitgeprüfte Materialmaster; MaterialEditingLibrary liefert Schätzstatistik (u.a. 205–212 Pixel-Instruktionen, 1–2 Pixel-Textursamples). Samplerzahl 0 nicht als null Texturkosten ausgeben.

VegetationDefaultMaterial ersetzt nur Laufzeit-Zuweisungen der 94 erkannten Komponenten durch Engine-Defaultmaterial. Geometrie/Collision/Position bleiben, aber Maskierung, Textur-/Revealarbeit, Zweiseitigkeit und Lichtantwort ändern sich gemeinsam. Das ist keine reine Overdraw-Messung, keine Retopologie und keine freigegebene Optimierung. Referenzen während des Probes stark gehalten, danach Original-MIDs/Schatten/Sichtbarkeit zurückgegeben; PIE-Signaturen bestätigen Rückgabe.


**Ergänzung zum Materialaudit:** Der konkrete Warnpfad ist `/Game/Environment/WestlandAssetLibrary/QualityV3/Materials/MI_WLA_FoliageGroups_V3`. Die HISM-Gruppen enthalten 30 A- und 28 B-Sträucher; hinzu kommen 44 einzelne Strauchkomponenten. Material- und Material-Instance-Dateien sind laut SHA-256 unverändert. Der PIE-Referenzshot und der native Kontrollshot zeigen den unterschiedlichen effektiven Shaderzustand trotz gleicher gespeicherter Referenzen. Auch der PIE-Materialgetter meldet das Flag false; der Getter allein beweist somit nicht die tatsächlich gerenderte VF-Permutation. Keine automatische Reparatur oder Speicherung vorgenommen.

Die lange Messserie ist ein wechselnder Lasttest, keine dedizierte thermische Dauerschleife je Einstellung. AC/100 % protokolliert; thermische Zustände siehe Telemetrie, keine Celsius-/Taktmessung. Statischer Systemkontext vor der nativen Matrix: 12.902 MB Swap belegt, memory_pressure meldet 74 % frei. Das belegt keine aktive Paging-Ursache. Andere Apps wurden nicht zwangsweise beendet. Keine Builds, Bildverarbeitung oder Archivierung parallel zu vergleichbaren GPU-Timingfenstern.

## 2. Vollständige Baseline

Alle folgenden Zahlen beschreiben die **unveränderte Diagnosekopie**, keine Optimierung. Je Zeile drei Läufe. Native Materialfallbacks wie oben beachten. Game ist gemeldete Game-Thread-Zeit; PIE-Renderthread nahe null unbrauchbar, native Renderthread-Wallzeit enthält GPU-/Present-Warten. Intern abgeleitet: 960×540, 1280×720, 1920×1080 oder 2560×1440.

| Modus | Ausgabe | Profil | SP % | Ort | FPS | Median ms | P95 ms | GPU ms | Game ms | Laufmediane ms |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| PIE | 1280×720 | Medium | 75 | Dorf | 60.01 | 16.66 | 16.95 | 15.00 | 4.51 | 16.67, 16.65, 16.66 |
| PIE | 1280×720 | Medium | 75 | Wald | 60.00 | 16.67 | 16.87 | 14.32 | 5.07 | 16.67, 16.67, 16.67 |
| PIE | 1280×720 | Medium | 75 | Weg | 57.70 | 17.33 | 19.89 | 16.16 | 5.78 | 17.33, 17.10, 17.62 |
| PIE | 1280×720 | Medium | 100 | Dorf | 45.77 | 21.85 | 26.60 | 20.83 | 6.02 | 21.85, 22.05, 21.79 |
| PIE | 1280×720 | Medium | 100 | Wald | 45.96 | 21.76 | 26.14 | 20.61 | 5.84 | 21.76, 21.76, 21.88 |
| PIE | 1280×720 | Medium | 100 | Weg | 45.20 | 22.13 | 27.09 | 21.47 | 6.11 | 22.15, 22.13, 21.81 |
| PIE | 1280×720 | High | 75 | Dorf | 44.71 | 22.37 | 26.86 | 20.82 | 6.53 | 22.14, 22.52, 22.37 |
| PIE | 1280×720 | High | 75 | Wald | 45.95 | 21.76 | 26.06 | 20.15 | 6.16 | 21.76, 21.66, 21.92 |
| PIE | 1280×720 | High | 75 | Weg | 44.10 | 22.67 | 26.96 | 21.28 | 6.20 | 22.76, 22.58, 22.67 |
| PIE | 1280×720 | High | 100 | Dorf | 33.72 | 29.66 | 32.65 | 27.11 | 5.91 | 29.66, 29.53, 29.71 |
| PIE | 1280×720 | High | 100 | Wald | 36.06 | 27.73 | 31.94 | 25.71 | 5.84 | 27.42, 27.88, 27.73 |
| PIE | 1280×720 | High | 100 | Weg | 33.48 | 29.86 | 33.07 | 27.39 | 5.88 | 29.67, 30.12, 29.86 |
| PIE | 2560×1440 | Medium | 75 | Dorf | 26.92 | 37.15 | 42.69 | 36.24 | 5.45 | 36.82, 37.15, 37.44 |
| PIE | 2560×1440 | Medium | 75 | Wald | 28.29 | 35.35 | 41.36 | 34.92 | 5.32 | 35.35, 35.53, 35.30 |
| PIE | 2560×1440 | Medium | 75 | Weg | 26.91 | 37.16 | 42.41 | 36.29 | 5.48 | 37.82, 37.16, 36.72 |
| PIE | 2560×1440 | Medium | 100 | Dorf | 19.29 | 51.83 | 60.71 | 51.56 | 6.33 | 51.83, 53.62, 51.35 |
| PIE | 2560×1440 | Medium | 100 | Wald | 19.78 | 50.56 | 56.74 | 49.75 | 6.28 | 50.56, 50.46, 50.71 |
| PIE | 2560×1440 | Medium | 100 | Weg | 19.15 | 52.21 | 60.81 | 51.52 | 6.43 | 51.71, 52.21, 53.87 |
| PIE | 2560×1440 | High | 75 | Dorf | 20.40 | 49.02 | 54.11 | 47.08 | 6.27 | 50.19, 49.02, 48.95 |
| PIE | 2560×1440 | High | 75 | Wald | 20.38 | 49.07 | 55.64 | 47.00 | 6.22 | 47.13, 49.07, 50.42 |
| PIE | 2560×1440 | High | 75 | Weg | 19.86 | 50.36 | 56.91 | 47.85 | 6.36 | 50.36, 53.50, 50.29 |
| PIE | 2560×1440 | High | 100 | Dorf | 14.20 | 70.41 | 78.95 | 67.66 | 7.06 | 70.18, 70.41, 70.42 |
| PIE | 2560×1440 | High | 100 | Wald | 14.54 | 68.75 | 78.18 | 66.35 | 7.02 | 69.45, 68.75, 68.48 |
| PIE | 2560×1440 | High | 100 | Weg | 13.93 | 71.81 | 81.01 | 69.37 | 7.07 | 71.81, 71.25, 72.56 |
| Standalone | 1280×720 | Medium | 75 | Dorf | 59.99 | 16.67 | 17.09 | 13.83 | 1.10 | 16.65, 16.67, 16.67 |
| Standalone | 1280×720 | Medium | 75 | Wald | 60.02 | 16.66 | 17.09 | 13.32 | 1.18 | 16.65, 16.67, 16.66 |
| Standalone | 1280×720 | Medium | 75 | Weg | 60.03 | 16.66 | 17.06 | 13.86 | 1.02 | 16.66, 16.65, 16.66 |
| Standalone | 1280×720 | Medium | 100 | Dorf | 59.98 | 16.67 | 16.99 | 15.05 | 1.06 | 16.67, 16.67, 16.68 |
| Standalone | 1280×720 | Medium | 100 | Wald | 60.02 | 16.66 | 17.02 | 15.03 | 1.21 | 16.66, 16.66, 16.67 |
| Standalone | 1280×720 | Medium | 100 | Weg | 55.41 | 18.05 | 20.16 | 17.02 | 1.58 | 17.72, 18.05, 18.54 |
| Standalone | 1280×720 | High | 75 | Dorf | 60.00 | 16.67 | 17.01 | 14.95 | 1.48 | 16.68, 16.66, 16.67 |
| Standalone | 1280×720 | High | 75 | Wald | 59.99 | 16.67 | 17.07 | 15.00 | 1.50 | 16.67, 16.66, 16.68 |
| Standalone | 1280×720 | High | 75 | Weg | 56.78 | 17.61 | 19.40 | 16.01 | 1.59 | 17.53, 17.61, 17.88 |
| Standalone | 1280×720 | High | 100 | Dorf | 47.15 | 21.21 | 23.45 | 20.87 | 1.58 | 21.21, 21.20, 21.49 |
| Standalone | 1280×720 | High | 100 | Wald | 45.42 | 22.02 | 23.56 | 20.90 | 1.58 | 21.55, 22.02, 22.17 |
| Standalone | 1280×720 | High | 100 | Weg | 42.80 | 23.36 | 25.81 | 22.88 | 1.58 | 23.23, 23.36, 23.56 |
| Standalone | 2560×1440 | Medium | 75 | Dorf | 34.71 | 28.81 | 30.96 | 27.90 | 1.49 | 28.74, 28.81, 29.79 |
| Standalone | 2560×1440 | Medium | 75 | Wald | 34.04 | 29.37 | 31.35 | 28.32 | 1.52 | 28.65, 29.37, 29.90 |
| Standalone | 2560×1440 | Medium | 75 | Weg | 31.77 | 31.47 | 33.62 | 30.29 | 1.55 | 31.30, 31.47, 32.05 |
| Standalone | 2560×1440 | Medium | 100 | Dorf | 23.48 | 42.60 | 45.19 | 41.42 | 1.86 | 41.99, 42.60, 42.64 |
| Standalone | 2560×1440 | Medium | 100 | Wald | 23.18 | 43.15 | 45.59 | 41.57 | 1.85 | 42.32, 43.15, 43.22 |
| Standalone | 2560×1440 | Medium | 100 | Weg | 21.92 | 45.61 | 48.87 | 44.00 | 1.83 | 45.54, 45.61, 45.79 |
| Standalone | 2560×1440 | High | 75 | Dorf | 26.90 | 37.18 | 39.94 | 35.39 | 1.72 | 37.12, 37.18, 37.48 |
| Standalone | 2560×1440 | High | 75 | Wald | 25.77 | 38.80 | 42.72 | 36.94 | 1.74 | 38.08, 38.80, 39.76 |
| Standalone | 2560×1440 | High | 75 | Weg | 24.11 | 41.48 | 44.25 | 39.34 | 1.74 | 41.48, 41.39, 42.12 |
| Standalone | 2560×1440 | High | 100 | Dorf | 17.27 | 57.91 | 62.83 | 56.25 | 1.97 | 57.76, 57.91, 58.31 |
| Standalone | 2560×1440 | High | 100 | Wald | 17.10 | 58.48 | 63.90 | 56.61 | 1.97 | 58.48, 58.30, 59.19 |
| Standalone | 2560×1440 | High | 100 | Weg | 15.94 | 62.74 | 74.27 | 61.00 | 1.98 | 61.54, 64.37, 62.74 |

## 3. Gemeldete GPU-Renderphasen

QHD/100-Wald, unveränderte Baseline. CSV-Scopes können Busy und Wait enthalten. Postprocessing-Schreibweise variiert je Prozess; die Werte sind nicht mit dem inklusiven ProfileGPU-Baum gleichzusetzen. Keine Addition als präzises Shaderbudget. Vollständige Phasen aller Baselinepunkte zusätzlich in `RenderPhases.csv` und Summary.json.

| Modus / Profil | GPU Frame | GI Gather | Shadow Projection | Shadow Depths | Basepass | Postprocessing-Scope | Unaccounted | Game |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PIE / Medium | 49.75 | 3.69 | 4.20 | 2.23 | 3.10 | 1.34 | 15.51 | 6.28 |
| PIE / High | 66.35 | 13.14 | 6.47 | 2.29 | 3.18 | 21.77 | 0.91 | 7.02 |
| Standalone / Medium | 41.57 | 3.69 | 4.41 | 2.33 | 3.06 | 1.38 | 13.99 | 1.85 |
| Standalone / High | 56.61 | 11.25 | 6.70 | 2.44 | 4.06 | 1.52 | 17.64 | 1.97 |

Zusatzframe `ProfileGPU`, verifizierte QHD/High/100-Waldkamera: Frame 64,778 ms, Lumen ScreenProbeGather inklusiv 14,545 ms, VirtualShadowMapProjection 6,526 ms, ShadowDepths 1,039 ms, BasePass 3,374 ms, benanntes PostProcessing 1,426 ms und Slate 3,082 ms. Ein Einzelbild außerhalb der regulären Statistik. Der Marker „VSM Log Stats And Status“ zeigt 20,757 ms, beweist aber keinen gleich teuren Statistikshader; VSM-CSV-Kategorie war aus. Metal-Stage-Counter-/Scope-Zuordnung bleibt dafür unzureichend.

Die engere A/B-Diagnose ist entscheidend: In der nativen TAA-Gegenprobe fällt der gemeldete Unaccounted-Median von 17,41 auf 0,02 ms, während GI-Gather etwa 10,60/10,91 ms und Schattenprojektion etwa 6,50/6,42 ms bleiben. In PIE fällt stattdessen der große PostProcessing-Scope von 23,23 auf 1,34 ms; GI-Gather bleibt etwa 14,17/14,24 ms. Somit ist der große Block **wesentlich an AA/TSR gebunden**, nicht pauschal als Bloom, reiner Schatten-Stats-Pass oder vollständig unbekannte Vegetationsarbeit zu behandeln. Die vollständige hardwareseitige Busy-/Fence-/Kernel-Aufteilung bleibt wegen der nicht finalisierten Metal-Aufzeichnung offen.

## 4. Alle gepaarten Einzelfaktoren

QHD/High/100. Negative Werte bedeuten weniger Bild-/GPU-Zeit. Median der drei **gepaarten** Differenzen; nicht die Differenz unabhängig gebildeter Kontroll-/Testmediane. Bewusstes Ausschalten einer Funktion misst eine Kette einschließlich Abhängigkeiten, keine frei addierbare Einzelpass-Ersparnis. Stats-off verwendet nur unabhängig gemessene Wall-Bildzeit; GPU-Werte dort absichtlich n/v.

| Modus | Ort | Einzelfaktor | Δ Frame ms | Drei Δ Frame ms | Δ GPU ms |
|---|---|---|---:|---|---:|
| PIE | Dorf | `CV:r.Lumen.DiffuseIndirect.Allow=0` | -11.53 | -9.56, -13.93, -11.53 | -8.58 |
| PIE | Dorf | `CV:r.Shadow.Virtual.Enable=0` | -4.95 | -4.95, -4.43, -5.83 | -5.95 |
| PIE | Wald | `AllShadowsOff` | -9.50 | -9.11, -9.50, -11.60 | -10.68 |
| PIE | Wald | `CV:r.AntiAliasingMethod=0` | -19.21 | -18.44, -19.21, -23.54 | -20.39 |
| PIE | Wald | `CV:r.AntiAliasingMethod=2` | -17.23 | -17.23, -17.22, -19.96 | -18.27 |
| PIE | Wald | `CV:r.GPUCsvStatsEnabled=0` | 1.28 | -3.38, 1.28, 2.26 | n/v |
| PIE | Wald | `CV:r.Lumen.DiffuseIndirect.Allow=0` | -9.79 | -9.41, -9.79, -11.58 | -9.62 |
| PIE | Wald | `CV:r.Lumen.HardwareRayTracing=0` | -1.80 | -1.51, -1.80, -2.30 | -1.66 |
| PIE | Wald | `CV:r.Lumen.Reflections.Allow=0` | 0.84 | -0.61, 2.57, 0.84 | -0.24 |
| PIE | Wald | `CV:r.Nanite=0` | 0.91 | 0.91, -0.15, 1.17 | 0.07 |
| PIE | Wald | `CV:r.Shadow.Virtual.Cache=0` | 2.85 | 1.89, 2.85, 4.10 | 1.32 |
| PIE | Wald | `CV:r.Shadow.Virtual.Enable=0` | -4.21 | -3.04, -6.42, -4.21 | -5.41 |
| PIE | Wald | `CV:r.Shadow.Virtual.SMRT.RayCountDirectional=2` | -1.76 | -3.20, -1.49, -1.76 | -2.78 |
| PIE | Wald | `CV:r.TSR.AsyncCompute=0` | -0.64 | 3.51, -0.64, -1.72 | -0.66 |
| PIE | Wald | `PostProcessingOff` | -21.08 | -20.59, -21.08, -22.43 | -21.06 |
| PIE | Wald | `VegetationDefaultMaterial` | -3.14 | -2.35, -3.14, -4.36 | -3.16 |
| PIE | Wald | `VegetationHidden` | -4.52 | -4.52, -4.95, -3.90 | -4.34 |
| PIE | Wald | `VegetationNoShadow` | -1.31 | -0.09, -1.31, -2.36 | -1.86 |
| PIE | Weg | `CV:r.Lumen.DiffuseIndirect.Allow=0` | -11.27 | -10.07, -12.77, -11.27 | -9.68 |
| PIE | Weg | `CV:r.Shadow.Virtual.Enable=0` | -6.98 | -6.98, -6.20, -9.31 | -6.41 |
| Standalone | Dorf | `CV:r.Lumen.DiffuseIndirect.Allow=0` | -9.83 | -9.33, -12.67, -9.83 | -7.91 |
| Standalone | Dorf | `CV:r.Shadow.Virtual.Enable=0` | -5.45 | -3.53, -5.96, -5.45 | -5.63 |
| Standalone | Wald | `AllShadowsOff` | -9.50 | -10.81, -9.50, -9.10 | -9.58 |
| Standalone | Wald | `BloomOff` | -0.61 | 0.30, -0.61, -1.76 | -0.43 |
| Standalone | Wald | `CV:r.AntiAliasingMethod=0` | -17.47 | -13.30, -17.47, -18.68 | -17.50 |
| Standalone | Wald | `CV:r.AntiAliasingMethod=2` | -16.84 | -16.50, -16.84, -17.49 | -17.06 |
| Standalone | Wald | `CV:r.GPUCsvStatsEnabled=0` | -0.72 | 1.08, -0.72, -1.08 | n/v |
| Standalone | Wald | `CV:r.Lumen.DiffuseIndirect.Allow=0` | -10.10 | -9.11, -10.76, -10.10 | -8.62 |
| Standalone | Wald | `CV:r.Lumen.HardwareRayTracing=0` | -2.22 | -1.81, -2.24, -2.22 | -0.43 |
| Standalone | Wald | `CV:r.Lumen.Reflections.Allow=0` | 0.02 | 1.86, -1.76, 0.02 | 0.12 |
| Standalone | Wald | `CV:r.Nanite=0` | -0.13 | -0.52, 1.12, -0.13 | -0.46 |
| Standalone | Wald | `CV:r.Shadow.Virtual.Cache=0` | 1.73 | 1.10, 1.73, 2.19 | 1.94 |
| Standalone | Wald | `CV:r.Shadow.Virtual.Enable=0` | -5.26 | -5.94, -4.41, -5.26 | -5.49 |
| Standalone | Wald | `CV:r.Shadow.Virtual.SMRT.RayCountDirectional=2` | -1.86 | -0.37, -2.09, -1.86 | -1.95 |
| Standalone | Wald | `CV:r.TSR.AsyncCompute=0` | -0.01 | -0.01, 0.49, -0.47 | -0.03 |
| Standalone | Wald | `DOFOff` | 0.45 | 0.85, -0.38, 0.45 | 0.77 |
| Standalone | Wald | `PostProcessingOff` | -19.92 | -20.63, -19.71, -19.92 | -19.86 |
| Standalone | Wald | `TonemapperFast` | 0.36 | 3.71, -1.85, 0.36 | -0.07 |
| Standalone | Wald | `VegetationDefaultMaterial` | -2.36 | -2.36, -2.24, -2.55 | -2.29 |
| Standalone | Wald | `VegetationHidden` | -3.99 | -3.53, -3.99, -4.77 | -3.87 |
| Standalone | Wald | `VegetationNoShadow` | -2.51 | -1.95, -2.51, -3.18 | -2.62 |
| Standalone | Weg | `CV:r.Lumen.DiffuseIndirect.Allow=0` | -11.21 | -11.21, -11.14, -11.66 | -9.63 |
| Standalone | Weg | `CV:r.Shadow.Virtual.Enable=0` | -5.88 | -5.88, -5.49, -7.44 | -6.14 |

### Interpretation und Prioritäten

1. **Materialkorrektheit zuerst herstellen.** Eigene, korrekt für HISM kompilierte Variante des bestehenden Blattmaterials anlegen, alle ursprünglichen Texture-/Tint-/Maskenwerte übernehmen und ausschließlich auf einer weiteren Testvariante zuweisen. Danach native Vegetations-/Schattenkosten erneut messen. Graue Fallbacks sind kein akzeptierter Performancegewinn. Keine automatische Reparatur dieses Auftrags.
2. **AA/TSR als größten gut isolierten Kandidaten vertiefen.** TAA statt TSR liefert in allen drei Paaren beider Modi einen großen Vorteil. AA komplett aus spart ähnlich, zeigt aber deutliches Körnen/Jagged Edges und ist ungeeignet. TSR-Async aus allein hilft nativ praktisch nicht (−0,006 ms Median; gemischte Einzelwerte), auch in PIE kein stabiler Vorteil. GPU-CSV aus spart nicht annähernd den großen Block: native −0,72 ms bei gemischten Paaren, PIE +1,28 ms. Keine Erklärung ausschließlich durch Statistikaufwand. TAA ist nur Kandidat, keine Freigabe: 75-%-Upscaling, Bewegung, dünne Blätter, Dither-Fade, kleine Figuren und Innenkamera müssen eigens abgenommen werden. Kein AA-Projektdefault geändert.
3. **Lumen-GI ist der zweite große Funktionsblock.** Abschaltung spart native etwa 10,10 ms im Wald, 9,83 ms am Heilhaus und 11,20 ms am Weg. Schattenbereiche werden dunkler/ärmer an indirekter Helligkeit. Deshalb keine einfache GI-Abschaltung. Nächste technische Versuche: ScreenProbe-/Tracing-Arbeit und unnötige Scene-/Card-Updates gezielt untersuchen, mit Kontaktlicht-/Innenraumvergleich. Die früheren Integrations-/Gather-Kandidaten nicht blind übernehmen. Hardware-Lumen aus allein spart viel weniger als GI komplett aus und ersetzt den Pfad; das ist keine kostenlose identische Beleuchtung.
4. **Schattenprojektion vor Schattengeometrie priorisieren.** QHD/High native etwa 6,70 ms Projektion gegenüber 2,44 ms Depths. VSM→Fallback spart etwa 5,26 ms, verändert aber Schattenkanten und Verfahren. Raycount 2 spart etwa 1,86 ms und besitzt Körnungsrisiken. Cache aus kostet zusätzlich 1,73 ms Bildzeit, also Cache erhalten. Vegetationsschatten komplett aus spart etwa 2,51 ms nativ: vereinfachte Kronen können nicht pauschal als Lösung des gesamten GPU-Defizits behauptet werden. Erst tatsächliche Invalidierungen bzw. Projektions-/Filterarbeit isolieren, keine Bäume schattenlos machen.
5. **Vegetationsmaterialien/Overdraw als begrenzten weiteren Hebel messen.** Vegetation unsichtbar spart native etwa 3,99 ms, Defaultmaterial etwa 2,36 ms. Beide verändern viele abhängige Faktoren; Differenzen dieser Tests sind kein reines Geometriebudget. Native Zahlen gelten zudem mit bekanntem Blattfallback. Blattkartenfläche, Maskenabdeckung, Sampler-/Revealarbeit und LODs erst nach Materialkorrektheit getrennt prüfen. Dichte und Silhouette erhalten. Keine quantifizierte Overdraw-Pixelzahl oder verlässlichen Draw Calls verfügbar.
6. **Nanite und Reflexionen sind hier keine nachgewiesenen Haupthebel.** Kein Nanite-aktiviertes Static Mesh im Inventar; Abschaltung ohne konsistenten Bildzeitvorteil. Lumen-Reflexionen aus: native praktisch null, PIE uneinheitlich. Medium hat sie ohnehin aus. Kein allgemeines Urteil über künftige Wasser-/Spiegelszenen oder alle Meshklassen.
7. **Bloom/DOF/Tonemapper nicht pauschal reduzieren.** Kleine bzw. wechselnde Effekte in den engen nativen Tests; sie erklären den großen PP-off-Unterschied nicht. Vollständiges Postprocessing aus spart zwar rund 19,92 ms nativ, zerstört jedoch AA-/Dither-/Farb-/Belichtungswirkung. Der AA-Vergleich grenzt die Hauptursache deutlich besser ein. Eine globale Effektabschaltung ist keine Empfehlung.

Die Last ist bei QHD überwiegend GPU-/Renderpfad-begrenzt: z.B. native High/100-Wald GPU 56,61 ms bei Game 1,97 ms. Renderthread 58,54 ms enthält Warten und ist keine reine CPU-Ausführung. Kein gezielter NPC-CPU- oder Gameplay-Umbau daraus begründet. Weiterhin keine 60-FPS-Garantie; auch TAA allein macht die ganze QHD-Welt nicht automatisch 60-FPS-tauglich.

## 5. Echte Spielkamera-Bilder und sichtbare Nachteile

Alle folgenden Original-PNGs sind echte 2560×1440-Unreal-Aufnahmen, keine Konzepte. Native Bildserie High/100, identische Kamera je Ort, Skeletal-Animationen für diese Standbilder pausiert und danach zurückgegeben. Die separate PIE-Materialaufnahme friert Animation nicht ein und ist kein pixelidentischer Animationsvergleich. Screenshots und Aufzeichnungsaufwand sind aus den Zeitvergleichen ausgeschlossen.

**Native Kontrolle – bekannter grauer Strauchfallback**

![Native Kontrolle – bekannter grauer Strauchfallback](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/00_Wald_0000000.png)

**Nur TAA statt TSR – im Standbild ähnlich, Bewegung offen**

![Nur TAA statt TSR – im Standbild ähnlich, Bewegung offen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/01_Wald_0100000.png)

**AA aus – deutliche Körnung und unruhige Kanten**

![AA aus – deutliche Körnung und unruhige Kanten](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/02_Wald_0200000.png)

**GI aus – tiefere, weniger aufgehellte Schatten**

![GI aus – tiefere, weniger aufgehellte Schatten](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/04_Wald_0400000.png)

**VSM aus / Fallback – veränderte, härtere Schatten**

![VSM aus / Fallback – veränderte, härtere Schatten](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/06_Wald_0600000.png)

**Ersatzmaterial – Blattkonturen, Texturen und Reveal verloren**

![Ersatzmaterial – Blattkonturen, Texturen und Reveal verloren](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/12_Wald_1200000.png)

**Postprocessing aus – deutlich veränderte Farb-/AA-Wirkung**

![Postprocessing aus – deutlich veränderte Farb-/AA-Wirkung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/14_Wald_1400000.png)

**Heilhaus, native Kontrolle**

![Heilhaus, native Kontrolle](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/17_Dorf_0000000.png)

**Weg, native Kontrolle**

![Weg, native Kontrolle](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/22_Weg_0000000.png)

**PIE-Kontrolle – gleiche gespeicherte Strauchreferenzen, belaubte Darstellung**

![PIE-Materialzustand](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/PIE_Baseline/PIE_Original00000.png)

Statische TAA-/TSR-Aufnahmen zeigen keinen großen Stilbruch, TAA wirkt an feinen Konturen teils weicher. Das ersetzt keine bewegte Qualitätsprüfung. Ohne AA sind Boden-/Schatten-/Blattkanten deutlich körniger. GI-off vertieft dunkle Bereiche; VSM-Fallback verändert die Schattencharakteristik. Der Defaultmaterialtest erzeugt grobe graue Kronen und ist optisch unbrauchbar. Bloom/DOF/Tonemapper-Zusatztests besitzen keine eigene vollständige Bildserie und werden nicht visuell freigegeben. Die zwölf Hauptvarianten und TAA/AA liegen in der nativen Serie vor.

Bekannte Grundprobleme bleiben: dunkle Figur in tiefem Waldschatten, temporale Dither-/Schattenartefakte, einfache Props/brauner Würfel am Heilhaus und der konkret nachgewiesene native Strauchfallback. Keine unaufgeforderte Artkorrektur.

### Alle nativen Bilder

| Nr. | Ort | Variante | Originaldatei |
|---:|---|---|---|
| 0 | Wald | `Control` | [00_Wald_0000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/00_Wald_0000000.png) |
| 1 | Wald | `CV:r.AntiAliasingMethod=2` | [01_Wald_0100000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/01_Wald_0100000.png) |
| 2 | Wald | `CV:r.AntiAliasingMethod=0` | [02_Wald_0200000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/02_Wald_0200000.png) |
| 3 | Wald | `CV:r.TSR.AsyncCompute=0` | [03_Wald_0300000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/03_Wald_0300000.png) |
| 4 | Wald | `CV:r.Lumen.DiffuseIndirect.Allow=0` | [04_Wald_0400000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/04_Wald_0400000.png) |
| 5 | Wald | `CV:r.Lumen.Reflections.Allow=0` | [05_Wald_0500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/05_Wald_0500000.png) |
| 6 | Wald | `CV:r.Shadow.Virtual.Enable=0` | [06_Wald_0600000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/06_Wald_0600000.png) |
| 7 | Wald | `CV:r.Shadow.Virtual.SMRT.RayCountDirectional=2` | [07_Wald_0700000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/07_Wald_0700000.png) |
| 8 | Wald | `CV:r.Shadow.Virtual.Cache=0` | [08_Wald_0800000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/08_Wald_0800000.png) |
| 9 | Wald | `AllShadowsOff` | [09_Wald_0900000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/09_Wald_0900000.png) |
| 10 | Wald | `VegetationNoShadow` | [10_Wald_1000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/10_Wald_1000000.png) |
| 11 | Wald | `VegetationHidden` | [11_Wald_1100000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/11_Wald_1100000.png) |
| 12 | Wald | `VegetationDefaultMaterial` | [12_Wald_1200000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/12_Wald_1200000.png) |
| 13 | Wald | `CV:r.Nanite=0` | [13_Wald_1300000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/13_Wald_1300000.png) |
| 14 | Wald | `PostProcessingOff` | [14_Wald_1400000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/14_Wald_1400000.png) |
| 15 | Wald | `CV:r.Lumen.HardwareRayTracing=0` | [15_Wald_1500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/15_Wald_1500000.png) |
| 16 | Wald | `Control` | [16_Wald_1600000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/16_Wald_1600000.png) |
| 17 | Dorf | `Control` | [17_Dorf_0000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/17_Dorf_0000000.png) |
| 18 | Dorf | `CV:r.Lumen.DiffuseIndirect.Allow=0` | [18_Dorf_0100000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/18_Dorf_0100000.png) |
| 19 | Dorf | `CV:r.Shadow.Virtual.Enable=0` | [19_Dorf_0200000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/19_Dorf_0200000.png) |
| 20 | Dorf | `PostProcessingOff` | [20_Dorf_0300000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/20_Dorf_0300000.png) |
| 21 | Dorf | `Control` | [21_Dorf_0400000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/21_Dorf_0400000.png) |
| 22 | Weg | `Control` | [22_Weg_0000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/22_Weg_0000000.png) |
| 23 | Weg | `CV:r.Lumen.DiffuseIndirect.Allow=0` | [23_Weg_0100000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/23_Weg_0100000.png) |
| 24 | Weg | `AllShadowsOff` | [24_Weg_0200000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/24_Weg_0200000.png) |
| 25 | Weg | `PostProcessingOff` | [25_Weg_0300000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/25_Weg_0300000.png) |
| 26 | Weg | `Control` | [26_Weg_0400000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Screenshots/VGB1_Final_Native_Review/26_Weg_0400000.png) |

## 6. Build, Automation, Map Checks und offene Prüfungen

- Der geänderte Development-Probe wurde tatsächlich kompiliert und gelinkt: Build_FinalProbe.log, erfolgreich. Abschlussbuild nach AA-Prüfung erneut erfolgreich, Target aktuell. Kein behaupteter Clean-Rebuild.
- Zwei frische vollständige Projektläufe: jeweils 48 Success, 0 SuccessWithWarnings, 0 Failed, 0 NotRun, 0 InProcess. NullRHI prüft Logik, nicht die Bildqualität. Letzter Lauf: AutomationFinal/index.json.
- Diagnosekopie und zentrale VisualV2 mehrfach lesend geprüft; vollständige Szenensignaturen identisch, keine schmutzigen Map-/Content-Pakete, Map Check 0 Fehler / 0 Warnungen.
- Materialfallback-Warnungen, bekannte Engine-Bootstrap-Condition-Meldungen, idevice_id/Bad-CPU-, MCP-Lizenz- und Shutdown-HTTP-Hinweise in Logs nicht unterdrückt. Strukturierte Projekttests sind erfolgreich; daraus kein vollständig warningfreier Engine-Start und keine Materialfreigabe abgeleitet.
- Keine neue physische Controller-, Gameplay-Fußlauf-, Dialog-, Kampf-/Fang- oder Save/Load-Abnahme dieses reinen GPU-Auftrags. Kein Gameplaycode geändert; bestehende Logiktests ausgeführt. Profiling-Teleports nicht als Fußlauf ausgegeben.
- Keine echte Hardwarekernel-Vollaufteilung wegen Metal-Finalisierungstimeout. Keine belastbaren Overdraw-Pixel-/Draw-Call-Zahlen. Kein Shipping-Build, keine verbindliche Dauer-FPS- oder Artfreigabe.

## 7. Dateien und Sicherung

Einzige geänderte bestehende Projektdatei: `Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV2.cpp`. Neue dauerhafte Dateien: Diagnosekarte, die tatsächlich benötigten Python-Werkzeuge/README und 23 statischen TSV-Pläne unter `Tools/VisualV2GPUBottleneckV1/`, dieser Prüfbericht. Keine .ini-, Material-, Textur-, Mesh-, Animations- oder Gameplay-Assetänderung. Sämtliche vorherigen 2.840 Dateien geprüft; nur die beabsichtigte Probe-Erweiterung abweichend, keine Datei fehlt. Alle vorherigen Maps und Assets bytegleich, Vollbackup unverändert.

Nur neu in diesem Auftrag erzeugte optionale Pläne und Python-Bytecodes wurden mit Prüfsummen nach extern verlegt. Keine vorbestehende Datei verschoben oder gelöscht. Die alte V1-Testkarte und V1-Werkzeuge bleiben unversioniert lokal. Native Review-/Photo-/Capture-Pläne sind reproduzierbare Generierungsprodukte und werden nicht als statische Pläne in Git aufgenommen, damit Wiederholungsguards im frischen Checkout nicht falsch auslösen.

Große Bilder, Rohmessungen, Logs und die etwa 1,9-GiB-Teilaufzeichnung bleiben außerhalb Git. Diagnosecode, benötigte Werkzeuge und die neue Karte sind im Commit `70e98f699f4294e38069a77035ad1ea24a03fcc3` regulär nach origin/main gesichert; Remote-Hash bestätigt. Die eine neue LFS-Datei (3.300.685 Bytes) wurde unabhängig wieder heruntergeladen und per SHA-256 geprüft. Unkomprimierte neue Git-Objekte dieses Pushs: 106.138 Bytes. Der Bericht wird als eigener zweiter Commit gesichert; dessen Hash und die Abschlusszustände stehen im unten verlinkten Git-Abschluss. Kein Force-Push, kein LFS-Prune, keine Käufe oder Budgetänderungen; der alte lokale main wurde nicht gepusht. Aktueller Live-Billingverbrauch ist nicht zugänglich; die Übertragung hatte keinen Quota- oder Kostenfehler.

[Dateischutz/SHA-256](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/ProtectionAudit.json)

[Materialfehler und unveränderte Originalassets](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/MaterialUsageFinding.json)

[Alle Einzelwerte](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Measurements.json)

[Baselines und GPU-Scopes](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Summary.json)

[43 gepaarte Diagnosegruppen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Pairs.json)

[402 Auflösungs-/Kameraprüfungen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Validation.json)

[48 Baselinezeilen CSV](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/Summary.csv)

[Alle Baseline-Renderphasen CSV](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/RenderPhases.csv)

[Map-/Szenenprüfung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/FinalMapAudit.json)

[Letzte Automation](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Evidence/AutomationFinal/index.json)

[Letzter Build](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/Build_AfterAACheck.log)

[Unreal-GPU-Capture](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/EditorMeasurementSession.log)

[Unvollständiger Metal-Trace](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/MetalSystemTrace_Result.json)

[Externe Kopien/SHA/CRC](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/EvidenceManifest.json)

[Rohdatenarchiv](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/RawMeasurements.zip)

[Nicht benötigte neue Generierungsprodukte](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/GeneratedLocalFiles.json)

[Git-/LFS-Abschluss](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17/GIT_ABSCHLUSS.md)

## 8. Empfehlung für den nächsten Auftrag

Eine separate korrigierte HISM-Blattmaterialvariante erstellen und native/PIE-Darstellung angleichen. Danach TAA und TSR bei gleicher Kamera, Dichte, korrekten Materialien, 75/100 %, in Bewegung und im Heilhaus vergleichen. Erst bei bestandener visueller Prüfung und erneuter Messung eine gezielte Übernahme erwägen. GI und Schatten anschließend getrennt optimieren; die geringere Priorität von Nanite, Bloom und pauschalem Geometrieabbau ist für die gemessenen Szenen belegt. Die zentrale VisualV2 bleibt bis dahin unverändert.
