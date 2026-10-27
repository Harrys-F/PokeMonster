# VisualV2 – Grafikartefakte, Performance und Stabilität V1

Stand: 27.10.2026. Ausgangsstand `052c2ab2` auf `main`, zu Beginn und vor der Sicherung identisch mit GitHub `origin/main`.

**Ergebnis:** Ursache der grünen Flächen nachgewiesen und durch drei lokale Materialzuweisungen korrigiert. Der Entwicklungsrecorder beendet sich jetzt beim PIE-/Weltende selbst und verwendet einen begrenzten Pool wiederverwendbarer GPU-Lesepuffer. Die tatsächliche Spielleistung, Aufnahmerate und Videozeitstempel wurden getrennt geprüft. **30-FPS-Aufnahmen sind nicht erreicht. Der frühere Editorstillstand ist nicht reproduziert und nicht als behoben freigegeben.** Der abschließende strenge QA-Wrapper endet wegen bekannter externer Warnungen mit **Exit 1**.

## Ausgangszustand und Schutz

Zu Beginn kein laufender Unreal Editor; vorhandene UnrealEditorServices-/UnrealTraceServer-Prozesse blieben unangetastet. Eigene Sitzungen: PID 35632, 37635 und 40668, jeweils mit absolutem Projektpfad und regulär geschlossen. Kein Prozesssignal und kein Force Quit. Eine frühere Freigabe für PID 23485 wurde nicht wiederverwendet.

Die alten Bilder/Videos waren durch die zuvor ausdrücklich freigegebene Medienbereinigung bereits entfernt. Die damaligen CSVs, Metadaten und der Hang-Sample existieren weiterhin. Alte Videos wurden deshalb nicht erneut dekodiert oder als vorhandene Bildnachweise ausgegeben. Frische Vergleichsaufnahmen entstanden vor der ersten Mapänderung.

Prüfsummen: **3963 von 3964 Originaldateien unverändert**; einzige erlaubte Inhaltsabweichung ist `Content/Maps/Dev_TestMap_VisualV2.umap`. Alle **33 ursprünglichen unversionierten Dateien**, alle **317 vorher vorhandenen `.sav`-Dateien** einschließlich älterer Testslots und beide Vollbackup-Refs bleiben identisch. Keine neue Map, Modelle, Texturen, Projektkopie oder Worktree. Westland, Biom-Testmap, Art und alle gemeinsam genutzten Materialien unverändert. Nachweis: [Prüfsummenprüfung](../Saved/ProjectRefinement/VisualV2StabilityV1/ProtectionFinal.json).

## Sichtkreis-Artefakt: Ursache und Korrektur

Reproduzierbar um Spielerposition ungefähr `(-650, 1000, 110.15)` cm, aus der normalen Kamera: Pitch −50°, Yaw −45°, FOV 35°. Die großen grünen Dreiecke waren **keine Kronenflächen**: Die Sichtfreistellung legte drei ältere begehbare Podeste frei. Diese verwendeten das selbstleuchtende/unbeleuchtete `M_PaintedGround` (`MSM_UNLIT`). Ihre grüne Fläche blieb auch bei deaktivierter Sichtfreistellung bestehen; das getrennte Ausblenden genau dieser Podest-Renderkomponenten ließ sie verschwinden. Kollisionen blieben bei der Diagnose aktiv.

| Objekt | Zentrum in cm | Änderung |
|---|---|---|
| Hill_Step_Low | −1120, 620, 10 | Materialslot 0 → vorhandenes M_EQ3_Ground |
| Hill_Step_Mid | −900, 800, 20 | Materialslot 0 → vorhandenes M_EQ3_Ground |
| Hill_Lookout | −620, 1010, 30 | Materialslot 0 → vorhandenes M_EQ3_Ground |

Das gewählte Material ist bereits der umgebende, weltkoordinatenbasierte VisualV2-Boden. Dadurch passen Farbe, Textur und Beleuchtungsreaktion. Geometrie, Höhen, Kollision, Schattenflags und alle übrigen Actor-Eigenschaften sind laut vollständigem Szenenvergleich identisch. Keine Änderung an Sichtkreisradius, Blattmaterialien, Spieler-Fülllicht, GI, Belichtung oder Tageslicht. Die vorhandenen Podestkanten sind weiterhin Geometrie; es fand kein Landschaftsumbau statt.

Gezielte GPU-Abwägung: Das vollständige Bodenmaterial ist teurer als die alte unbeleuchtete Fläche. Die erste A/B/A-Stichprobe ergab etwa +2,5 ms; kurze, abwechselnd mit alten Kontrollflächen gemessene Schätzungen +2,17 / +5,08 / +6,28 ms. Die einfachere vorhandene Naturgrasvariante zeigte +0,28 bis +3,56 ms, aber deutlichere rechteckige Farb-/Materialgrenzen und wurde verworfen. Bei langen Reihen drifteten die Kontrollwerte stark (in einer frischen Reihe 63,7 → 88,9 ms; in einer langen Sitzung zeitweise über 170 ms). **Kein belastbarer allgemeiner GPU-Gewinn und keine Kostenneutralität behauptet.** Die bessere Bildintegration wurde nur an diesen drei Flächen übernommen; keine pauschale Grafikreduktion.

Nachweise: [gezielte Geometrie-/Materialablation](../Saved/ProjectRefinement/VisualV2StabilityV1/SurfaceAblation01/Result.json), [abwechselnde GPU-Kontrollen](../Saved/ProjectRefinement/VisualV2StabilityV1/InterleavedMaterialAnalysis.json), [begründete Endauswahl](../Saved/ProjectRefinement/VisualV2StabilityV1/SelectedFinalState.json).

## Echte QHD-Vergleiche

Alle sechs Hauptpaare besitzen nach unabhängigem Metadatenvergleich dieselbe Spieler-/Kameraposition (Toleranz <0,01 cm), dieselbe Uhrzeit und FOV. PNGs jeweils **2560×1440**, High=2, 100 %, normale Spielkamera. Bewegte Pokémon/Idle-Posen dürfen zeitlich variieren; Bilder wurden nicht künstlich erzeugt oder umbelichtet.

| Uhrzeit | Vorher | Übernommene Korrektur |
|---|---|---|
| 06:00 | [Original](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproBefore03/Group0600.png) | [Nachher](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproAfter01/Group0600.png) |
| 09:00 | [Original](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproBefore03/Group0900.png) | [Nachher](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproAfter01/Group0900.png) |
| 12:00 | [Original](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproBefore03/Group1200.png) | [Nachher](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproAfter01/Group1200.png) |
| 19:00 | [Original](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproBefore03/Group1900.png) | [Nachher](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproAfter01/Group1900.png) |
| 22:00 | [Original](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproBefore03/Group2200.png) | [Nachher](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproAfter01/Group2200.png) |
| 00:00 | [Original](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproBefore03/Group0000.png) | [Nachher](../Saved/ProjectRefinement/VisualV2StabilityV1/ReproAfter01/Group0000.png) |

Weitere echte Ansichten: [Wiese](../Saved/ProjectRefinement/VisualV2StabilityV1/ViewSites01/Wiese0900.png), [Baumkrone nachts](../Saved/ProjectRefinement/VisualV2StabilityV1/ViewSites01/Krone2200.png), [Waldweg nachts](../Saved/ProjectRefinement/VisualV2StabilityV1/ViewSites01/Waldweg0000.png), [Heilhaus außen](../Saved/ProjectRefinement/VisualV2StabilityV1/ViewSites01/Haus0900.png), [Innenraum nach Laden](../Saved/ProjectRefinement/VisualV2StabilityV1/Gameplay01/InteriorLoaded.png). [Bildgrößen, Prüfsummen und Kameravergleich](../Saved/ProjectRefinement/VisualV2StabilityV1/PhotoPairs.json). Bilder bleiben lokal außerhalb von Git/LFS.

## Tatsächliche Spielleistung

Verwendet wird der bestehende native `pm.EnvPerf2`-Profiler mit `VGB1_`-Kennung, ausdrücklich ohne dessen ältere Qualitäts-Absenkungen. Pro Standardsegment 2 s Aufwärmen + 4 s Messung, drei Wiederholungen. Jeder gemessene Frame wurde auf tatsächliche interne/ausgegebene 2560×1440, High=2, 100 %, TAA2 und Standardkamerawinkel geprüft. Keine Videoaufnahme während der folgenden Zeitmatrix. Uhr läuft normal mit 1×/120 Minuten pro Tag; Kontakte werden nur im isolierten Messaufbau temporär gesperrt.

Erste Referenz am Mittag: Dorf **11,37–11,99 FPS**, GPU-Mittel 73,22 ms, Frame-Mittel 85,12 ms, Game-Thread 11,06 ms; Wald **10,97–11,45 FPS**, GPU 77,59 ms, Frame 88,99 ms, Game-Thread 9,94 ms. Editor wurde mit vorgefundenem Epic=3 geöffnet; das vereinbarte High-Messprofil wurde ausdrücklich temporär gesetzt, keine INI gespeichert.

Zusätzliche Matrix direkt bei der sichtbaren Pokémon-Gruppe. Acht natürliche Rhythmus-Wildinstanzen aus sechs Arten, insgesamt zwölf Wild-Encounter-Actors und 23 Visual-Actors inklusive elf Vorführexemplaren; Encounter- und Visual-Actors sind teilweise dieselben Pokémon und dürfen nicht zu 35 Tieren addiert werden. „Ohne“ pausiert vorübergehend sämtliche Pokémon-Actor-/Component-Ticks und deren Darstellung, zerstört keine Instanzen und restauriert danach die Flags. Nativer Standortname bleibt historisch `Wald`; der QA-Aufbau versetzt nur während des Warmups zur tatsächlichen Gruppenposition, die in jedem Frame mitprotokolliert wird.

| Zeit | Mit: FPS / GPU ms / Frame ms / Game ms | Ohne: FPS / GPU ms / Frame ms / Game ms |
|---|---|---|
| 06:00 | 11.61 / 79.76 / 86.13 / 10.46 | 11.58 / 81.11 / 86.37 / 11.14 |
| 09:00 | 11.01 / 83.59 / 90.81 / 11.37 | 11.45 / 82.30 / 87.37 / 10.16 |
| 12:00 | 11.04 / 83.18 / 90.62 / 11.38 | 11.55 / 81.04 / 86.54 / 9.84 |
| 19:00 | 11.22 / 82.24 / 89.10 / 10.49 | 11.83 / 79.40 / 84.50 / 9.72 |
| 22:00 | 11.40 / 79.45 / 87.72 / 11.62 | 11.93 / 78.62 / 83.79 / 10.13 |
| 00:00 | 11.46 / 80.19 / 87.26 / 10.89 | 11.97 / 78.25 / 83.51 / 10.41 |

Kein unverhältnismäßiger einzelner Nachtzustand in dieser Stichprobe. Absolute Werte verändern sich mit Sitzung/Systemlast; thermischer Einfluss ist möglich, aber nicht separat bewiesen. Kleine Unterschiede sind kein garantierter Optimierungsgewinn. Der native aggregierte RenderThreadTime-Zähler liefert nahezu Null trotz positiver Render-Scopes und ist hier **nicht als gesamte Render-CPU-Zeit verwertbar**. RDG-Teilscope typischerweise etwa 1–3 ms, zusätzlich erhebliche Warteanteile; daraus keine erfundene vollständige Render-Thread-Zeit ableiten. Rohdaten einschließlich Streuung: [sämtliche Einzelmessungen](../Saved/ProjectRefinement/VisualV2StabilityV1/MetricsSummary.json).

Gehen, Sprinten und folgende Kamera, jeweils drei reale Messsegmente; keine freie Kamerarotation:

| Tätigkeit | Ohne Aufnahme: FPS / GPU ms / Game ms | Mit Slate-Aufnahme: FPS / GPU ms / Game ms |
|---|---|---|
| Gehen | 10.98 / 79.58 / 10.74 | 9.70 / 81.43 / 12.05 |
| Sprinten | 10.80 / 80.95 / 11.12 | 9.66 / 80.45 / 12.73 |
| Richtungswechsel/Kamerafolge | 10.49 / 83.52 / 11.37 | 9.59 / 82.46 / 12.19 |

## Aufnahme und Videowiedergabe getrennt

Historischer Clip: 45 Quellframes, 12,0528 s zwischen erstem/letztem Zeitstempel, **44/12,0528 = 3,6506 Hz**. Das ist die Abtastrate der Aufnahme; die alte MP4 fehlt inzwischen und wurde nicht nachträglich als geprüft ausgegeben.

Im erneuten QHD-Vergleich: ursprünglicher Slate-Pfad 4,178 Hz, synchroner Framebuffer-Pfad ohne UMG 6,208 Hz (bremst das Spiel stärker). Nach Poolwiederverwendung Slate etwa 5,378 Hz. Unterschiedliche Sitzungs-/Lastbedingungen verhindern, diesen Unterschied vollständig als kausalen Gewinn der Änderung auszugeben. Sechs statt drei Puffer erreichten nur 5,417 Hz; kein belegter Vorteil, Standard bleibt drei. Tatsächlich wurden im finalen Messclip nur **zwei GPU-Lesepuffer wiederverwendet** statt pro Frame neue Ressourcen anzulegen.

Messcode: je Bild im Mittel etwa 100 ms im Lock-/Lese-/Kopierabschnitt, 31–36 ms JPEG-Aufruf auf einem Worker, 1,5–1,9 ms Dateischreib-Aufruf; letztere können OS-Cache enthalten. Keine Puffer- oder Encoder-Warteschlangenüberläufe. Dies sind Aufruf-/Wartezeiten, keine addierbaren CPU-Prozessorzeiten. Der lokale UE-5.8.2-Quellcode `MetalRenderTarget.cpp`, `FMetalDynamicRHI::RHIMapStagingSurface`, ruft trotz vorheriger Bereitschaftsprüfung `SubmitAndBlockUntilGPUIdle()` auf. Das belegt eine zusätzliche Synchronisationsquelle im vermeintlich asynchronen Texture-Readback. Engine-Dateien wurden nicht verändert.

Alternative native macOS-Aufnahme: Bildschirmaufnahme-Vorabprüfung war `false`; eine Freigabe wurde angefragt, aber keine OS-Berechtigung verändert. ScreenCaptureKit wurde daher nicht als getestete Lösung ausgegeben. Schon ohne Aufnahme liegen die untersuchten QHD/High-Szenen deutlich unter 30 FPS; ein Encoder allein kann dort keine 30 echten neuen Spielbilder erzeugen.

Drei H.264-Dateien mit bestehendem AVFoundation-Encoder, unveränderte Bildfolge und ursprüngliche Abstände, nur gemeinsamer Zeitnullpunkt. Bei Auflösungsübergängen wurde der längste zusammenhängende Lauf gleicher Größe ausgewählt. Der bestehende Encoder rundet ungerade native Dimensionen um ein Pixel ab; Videos sind deshalb **keine QHD-Videoabnahme**. QHD gilt für Renderer-Messungen/Standbilder, der kontinuierliche Clip stammt aus dem normalen eingebetteten PIE-Ausschnitt.

| Video | Dekodierte Frames | Spanne / echte Rate | Dateidauer | Größe |
|---|---|---|---|---|
| [Messclip vorher](../Saved/ProjectRefinement/VisualV2StabilityV1/Videos/CaptureBefore01_Slate.mp4) | 78 | 18.268 s / 4.215 Hz | 18.420 s | 2330x1310 |
| [Messclip Pool 3](../Saved/ProjectRefinement/VisualV2StabilityV1/Videos/CaptureAfter01_Pool3.mp4) | 102 | 18.568 s / 5.439 Hz | 18.855 s | 2330x1310 |
| [Zusammenhängendes Gameplay](../Saved/ProjectRefinement/VisualV2StabilityV1/Videos/GameplayContinuous01.mp4) | 108 | 13.947 s / 7.672 Hz | 14.050 s | 2330x1346 |

Unabhängiger AVAssetReader dekodiert genau so viele Frames wie Quellzeilen, eindeutige Zeitstempel und Abweichung unter einem tatsächlichen 1/600-s-Ausgabequantum (maximal rund 0,85 ms). Keine künstlich vervielfachten/interpolierten Frames. Dekodierung der einzelnen Clips dauerte etwa 0,26–0,31 s; kein zusätzlicher Wiedergabe-Flaschenhals erkennbar. Vorläufiger eigener Videoverifier scheiterte zunächst an unrealistisch engen 50-µs-/Halbquantum-Grenzen; diese Fehlversuche bleiben dokumentiert. Das war kein Unreal-Absturz und keine Änderung der Videodaten.

## Editorstillstand und Regression

Alter Sample von PID 23485: GameThread wartet beim Viewport-Resize auf eine Render-Fence; asynchrone Scene-Extension-Freigabe wartet ebenfalls. Footprint damals 41,4 GB bei 16 GB Hardware. Der Stack bestätigt **nicht** KI-Timer, Partnerreservierungen, Weltuhr, Save/Load oder den Recorder als ursprüngliche Ursache. Vorhandene EndPlay-/Deinitialize-Pfade lösen Partner beidseitig auf, entfernen Uhrdelegates und räumen Timer/Callbacks auf; keine spekulative KI-/Speicheränderung vorgenommen.

Separat reproduzierter Recorderfehler: Nach regulärem PIE-Ende fehlten Complete/Frames.csv, Aufnahmezustand blieb bis zum manuellen Stop bestehen. Korrektur bindet eine schwache Welt-Abbau-Benachrichtigung, stoppt neue Bilder und lässt vorhandene GPU-Lesevorgänge/Worker asynchron auslaufen. Kein blockierendes Flush/Warten im Welt-Abbau hinzugefügt. Nachprüfung: Aufnahme schließt automatisch, 26 Bilder geschrieben, maximal zwei verwendete Lesepuffer.

**Zehn vollständige kontrollierte Start-Stopp-Zyklen bestanden**: normal, aktive Pokémon, Tagesphasenwechsel, Innenraum, Save/Load, Kampf, Bewegung/Controller-Software, laufende Aufnahme und zwei weitere Wiederholungen. Nach jeder Beendigung reagiert die Editor-Queue wieder, kein GameWorld/dirty package; Prüfantwort jeweils ungefähr 0,28–0,30 s. Zusätzlich echte VisualV2 → Dev_TestMap → VisualV2-Reise mit identischer GameInstance/Uhr, Team-Identitäten/KP/AP und genau einem korrekten Begleiter nach Rückkehr bestanden. Alle eigenen Editoren anschließend regulär geschlossen. Im langen zweiten Editor wurden nach dem Test 12,0 GB Footprint / 13,3 GB Peak erfasst; das ist ein anderer Workload und kein Nachweis eines behobenen Lecks.

Echter zusammenhängender Gameplay-Lauf: 63,57 s, 18 Prüfungen für 75°/85°, Menüpause, reale Eingaben, Dämmerung/Mitternacht, Heilhaus-Ein-/Austritt, isoliertes Innenraum-Save/Load und ClassicBattle-Sieg/Steuerungsrückkehr. Separater direkter Tastatur-Fußlauf über CUA: 544,65 cm Positionsänderung, Kamera folgt, Steuerung bleibt aktiv. Acht Richtungen, L3-Toggle, X, L/R, Steuerkreuz und A wurden softwareseitig über bestehende Eingabepfade geprüft; **kein neuer physischer Switch-Pro-Test behauptet**.

KI-Regression: 91,49 s, 172 Stichproben bei acht Instanzen aus sechs Arten. Beobachtet Wander, Idle, Rest, Sleep, Forage und Social; gültige gegenseitige Reservierungen, keine Schlafbewegung/Schlafpartner, Habitatschutz, Zeitwechsel und Pause bestanden. Die Profile und alle Tagesrhythmusdaten blieben unverändert. Fang, EP, Entwicklung, Heilung/Kontrollpunkt und übrige Speicherfälle werden zusätzlich durch die vollständige Automation abgedeckt; kein neuer visueller PIE-Fang-/Entwicklungsdurchlauf behauptet.

Nachweise: [zehn Zyklen](../Saved/ProjectRefinement/VisualV2StabilityV1/Cycles01/Result.json), [Gameplay](../Saved/ProjectRefinement/VisualV2StabilityV1/Gameplay01/Result.json), [Mapwechsel](../Saved/ProjectRefinement/VisualV2StabilityV1/Travel01/Result.json), [KI](../Saved/ProjectRefinement/VisualV2StabilityV1/Rhythm01/Result.json), [Recorderfehler vorher](../Saved/ProjectRefinement/VisualV2StabilityV1/RecorderLifecycleBefore.json). Erster Bewegungs-Prüfaufbau verwendete irrtümlich eine generische X-Taste; korrigiert wurde nur der QA-Aufbau auf das bestehende macOS-Backend, nicht die Spielbelegung. Weitere frühe Python-Prüfaufbaufehler und leere Fehlversuchsordner wurden nicht als bestandene Tests gezählt.

## Build, Automation und Warnungen

| Lauf | Tatsächliches Ergebnis |
|---|---|
| Editor-Build 01 | Exit 0, 29,21 s |
| Automation 01 | 279 sauber erfolgreich, 0 Fehler/Übersprungen/Testwarnungen; Engine/strenger Wrapper 0 |
| Finaler Editor-Build | Exit 0, 3,11 s |
| Finale volle Automation | 276 sauber + 3 erfolgreich mit Warnungen = 279 funktional erfolgreich; 0 Fehler/Übersprungen; Engine 0, **strenger Wrapper 1** |
| Abschließende Map Checks | Alle zwölf bestehenden Maps, je **0 Fehler / 0 Warnungen** |
| Szenen-/Dateischutz | Vollständiger Szenenvergleich und Originalprüfsummen bestanden |

Die drei finalen Warnungstests sind `Creatures.Pipeline.ImportContract`, `MoveEffectsV4.ProtectFlinchConfusionAndSwitchReset` und `ProgressionV1.LearningAndFourSlotLimit`. Je zwei Meldungen betreffen ausschließlich den vorhandenen externen iOS-Helfer `idevice_id` mit „Bad CPU type“ / „Failed to launch Tool“. Die sechs Rohwarnungen bleiben erhalten. Kein Warnungsfilter und kein weiterer Wiederholungslauf nur zum Erzielen von Grün. [genaue Zuordnung](../Saved/ProjectRefinement/VisualV2StabilityV1/QAClassification.json).

Zusätzliche vorbestehende Editor-/Enginebefunde bleiben getrennt: Python-Namenskollision der PresentationAction, generische Startup-Condition-Meldungen, Instancing-/CVar-Prioritäts- und RenderThreadSafe-Hinweise sowie externe HTTP-Shutdown-Warnungen. Der gesamte Editorlog wird nicht als warnungsfrei bezeichnet. Keine neuen funktionalen Projekt-Testfehler und kein neuer Unreal-Stillstand/-Absturz in den durchgeführten Zyklen.

## Offene Grenzen und Git-Sicherung

- 30-FPS-Ziel bleibt offen; Quelle/Spielrenderer sind in den geprüften Szenen zu langsam. Native OS-Aufnahme ohne Engine-Readback mangels Berechtigung nicht geprüft.
- Frühere Editorblockade nicht reproduziert, Ursache weiterhin offen. Recorder-Lebenszyklusfehler separat behoben; keine Gleichsetzung beider Ursachen.
- Materialkorrektur benötigt lokale zusätzliche GPU-Arbeit; keine Performance-Neutralität oder globale Beschleunigung behauptet. Einfachere Alternative wegen sichtbarer Kanten nicht übernommen.
- Volle aggregierte Render-Thread-CPU-Zeit mit dem vorhandenen nativen Summenzähler hier nicht belastbar verfügbar; Teilscope und Wartebefunde separat ausgewiesen.
- Finale strenge QA bleibt Exit 1 wegen externer iOS-Warnungen. Alle 279 Funktionstests erfolgreich, dies ersetzt keinen warnungsfreien Wrapper.

Versioniert werden ausschließlich die drei Map-Materialzuweisungen, die Entwicklungsrecorder-Korrektur, tatsächlich genutzte QA-Quellen und dieser Bericht/Entscheidungsnachtrag. Keine Prüfmedien, Nutzersaves oder ursprünglichen unversionierten Dateien im Commit. Ausgangscommit `052c2ab2`; der Sicherungscommit ist der Commit dieses Berichts (`git log -1 -- Docs/VISUALV2_GRAFIK_PERFORMANCE_STABILITAET_V1.md`). Tatsächlicher Push-/Remote-/LFS-Abgleich wird lokal in `Saved/ProjectRefinement/VisualV2StabilityV1/GitFinal.json` protokolliert und im Abschlusschat mit Commit-ID genannt. Git-LFS-Budget bleibt 0 USD; keine Budget-/Zahlungsänderung, kein Force Push oder Prune.
