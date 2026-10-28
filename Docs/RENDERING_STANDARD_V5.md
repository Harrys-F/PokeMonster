# Rendering-Standard V5 – Software-Lumen + IFG

Stand: 28.10.2026. Ausgangsstand main/origin/main a7ef91210164e66b3351a7cecfa5808b83318ae1.

Die Umstellung ist ausdrücklich vom Projektinhaber entschieden. Die technische
Umstellung ist geprüft; eine abschließende temporale Bildfreigabe oder stabile
30 FPS werden damit ausdrücklich nicht behauptet.
Die V4-Messungen sind historische Referenzen, keine neuen V5-Ergebnisse.

Offen bleiben stabile 30 FPS, Framezeitspitzen und die abschließende temporale
Bildprüfung. Hardware-Lumen + SPG bleibt wiederherstellbare Qualitätsreferenz.

## Profile

| Befehl | Lumen HWRT / FinalGatherMethod | Auflösung | VisualV2-VSM-Strahlen |
|---|---|---|---:|
| `pm.Graphics C` (Standard) | 0 / 0 = Software / IFG | QHD / 75 % / TAAU | 4 |
| `pm.Graphics HardwareSPG` | 1 / 1 = Hardware / SPG | QHD / 75 % / TAAU | 4 |
| `pm.Graphics 100` | 1 / 1 = Hardware / SPG | QHD / 100 % / TAA | bisheriger Wert, High 8 |

Alle elf Qualitätsgruppen bleiben High (2). `pm.Graphics status` zeigt tatsächliche
Werte. `-PMGraphicsProfile=HardwareSPG` beziehungsweise `=100` wählen eine Referenz
ab Prozessstart. Auswahl gilt bis zum Prozessende; ein Neustart ohne Argument
beginnt mit C. Live-Umschaltung der beiden getesteten Lumen-CVars benötigt auf
dieser Konfiguration keinen Neustart; globale Raytracing-/Distance-Field-
Unterstützung und Shader bleiben verfügbar. Editor-Vorschau außerhalb PIE bleibt
unverändert und wird nach PIE restauriert. Keine SaveSettings- oder Spielstand-
Schreiboperation. Explizite höher priorisierte Konsolen-Overrides müssen für
einen unverfälschten Profiltest zuvor aufgehoben werden.


## Architektur und Wiederherstellung

Die bestehende nicht tickende `UPokeMonsterGraphicsProfile`-WorldSubsystem bindet
sich an `OnWorldBeginPlay` in Game-/PIE-Welten. `DefaultProfile=VariantC` bleibt
zentral in `DefaultPokeMonsterGraphics.ini`. Dauerhaft ist die Implementierung und
dieser Standard; eine manuell gewählte Referenz gilt nur im jeweiligen Prozess.
Es gibt keinen erforderlichen Start-Pythoncode und keinen manuellen Lumen-Befehl.
Ein bewusst nach dem Start ausgeführter Profilwechsel hat bei Mapreisen Vorrang
vor einem früheren `-PMGraphicsProfile`-Startargument.

Die beiden Lumen-CVars werden wie die übrigen Profilwerte über vorhandene
reversible Overrides mit `SetByCode` gesetzt. Der bisherige Wert und seine
Priorität werden erhalten; eine explizite höher priorisierte Nutzerkonsole bleibt
maßgeblich. `status` gibt den tatsächlich wirksamen Pfad aus und meldet eine
abweichende Anforderung. Am PIE-Ende werden die Werte vor PIE restauriert. Die
reine Editor-Vorschau bleibt deshalb bei ihrem vorherigen Rendering; jeder neue
PIE-Spielstart aktiviert wieder das ausgewählte Spielprofil. Keine Änderung an
`DefaultEngine.ini`, kein automatisches `SaveSettings`, keine neue Speicherdatei.

Auf VisualV2 erhalten C und HardwareSPG vier VSM-Strahlen. `100` behält die alte
native 100-%-Referenz mit High-Standardwert acht. Auf anderen bestehenden Maps
bleibt die frühere map-spezifische VSM-Regel unverändert (High acht); die Lumen-
Profilwahl bleibt beim Reisen erhalten. Keine Änderungen an Map- oder Assetdateien.

## Exakte Rendering-Werte

Die Umstellung verändert gegenüber V4 A ausschließlich HWRT 1→0 und Gather
1→0. Die übrigen Werte entsprechen der in V4 getesteten Konfiguration.
Reflexionen bleiben Lumen; die globale Raytracing-Fähigkeit bleibt eingeschaltet,
damit die Hardware-Referenz zur Laufzeit verfügbar ist. `r.RayTracing=1` bedeutet
somit bei C ausdrücklich nicht, dass Lumen Hardware-Tracing verwendet.

| Einstellung | C: Software/IFG | HardwareSPG: Qualitätsreferenz |
|---|---:|---:|
| `r.DynamicGlobalIlluminationMethod` | 1 | 1 |
| `r.ReflectionMethod` | 1 | 1 |
| `r.RayTracing` | 1 | 1 |
| `r.RayTracing.Enable` | 1 | 1 |
| `r.Lumen.HardwareRayTracing` | 0 | 1 |
| `r.Lumen.FinalGatherMethod` | 0 | 1 |
| `r.Lumen.DiffuseIndirect.Allow` | 1 | 1 |
| `r.Lumen.Reflections.Allow` | 1 | 1 |
| `r.Lumen.Reflections.ScreenTraces` | 1 | 1 |
| `r.Lumen.ScreenProbeGather.ScreenTraces` | 1 | 1 |
| `r.GenerateMeshDistanceFields` | 1 | 1 |
| `r.DistanceFields.SupportEvenIfHardwareRayTracingSupported` | 1 | 1 |
| `r.Lumen.TraceMeshSDFs.Allow` | 0 | 0 |
| `r.Lumen.IrradianceFieldGather.GridResolution` | 64 | 64 |
| `r.Lumen.IrradianceFieldGather.ProbeResolution` | 16 | 16 |
| `r.Lumen.IrradianceFieldGather.NumProbesToTraceBudget` | 100 | 100 |
| `r.Lumen.ScreenProbeGather.DownsampleFactor` | 32 | 32 |
| `r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor` | 1 | 1 |
| `r.Lumen.ScreenProbeGather.TracingOctahedronResolution` | 8 | 8 |
| `r.LumenScene.SurfaceCache.AtlasSize` | 3584 | 3584 |
| `r.LumenScene.DirectLighting.UpdateFactor` | 64 | 64 |
| `r.LumenScene.Radiosity.UpdateFactor` | 128 | 128 |
| `r.Lumen.Reflections.DownsampleFactor` | 2 | 2 |
| `r.Shadow.Virtual.Enable` | 1 | 1 |
| `r.Shadow.Virtual.SMRT.RayCountDirectional` | 4 | 4 |
| `r.Shadow.Virtual.SMRT.SamplesPerRayDirectional` | 4 | 4 |
| `r.Shadow.Virtual.ResolutionLodBiasDirectional` | 0 | 0 |
| `r.DistanceFieldShadowing` | 1 | 1 |
| `r.ScreenPercentage` | 75 | 75 |
| `r.SecondaryScreenPercentage.GameViewport` | 100 | 100 |
| `r.TemporalAA.Upsampling` | 1 | 1 |
| `r.DynamicRes.OperationMode` | 0 | 0 |
| `r.VSync` | 0 | 0 |
| `t.MaxFPS` | 0 | 0 |

Alle elf High-Skalierungsgruppen haben Wert 2. Das aktive Device Profile im
Development-Spielprozess ist MacEditor mit Elternprofil Mac. Keine neuen Device-
Profile- oder Scalability-Dateien und keine PP-Override-Änderungen. PP Final Gather,
Scene Lighting Quality, Scene Detail und beide Update-Speeds bleiben 1;
View Distance 20000, Reflection Quality 1, die zugehörigen Overrides sind aus.
IFG 64/16/100 sind unveränderte, im lokalen UE-5.8.2-Quellcode und zur Laufzeit
geprüfte Engine-Defaults. Der tatsächlich arbeitende IFG-GPU-Scope wird zusätzlich
in jedem Benchmark ausgewertet. Software-Lumen nutzt bei High den Global Distance
Field (Mesh-SDF-Detail-Tracing Allow=0). Kein SSGI und kein GI-off.

Die globale AA-CVar bleibt 4, während die vorhandene VisualV2-Anbindung den
maßgeblichen View auf AA=2 setzt. Der Renderer bestätigt temporales Upsampling=1,
primären Faktor 0,75, sekundär 1 und Ausgabe/Renderziel 2560×1440. Die internen
1920×1080 sind aus tatsächlicher Viewgröße und Renderfraktion abgeleitet, kein
unabhängiger GPU-Allocation-Readback. Keine Grafikqualitätsreduktion gegenüber V4 C.

## Prüfung – Methodik

UE 5.8.2 / CL 56702186, Metal SM6, Apple M4, MacBook Air Mac16,12 mit 16 GB.
Neue Messungen verwenden frische `UnrealEditor -game`-Development-Prozesse, keinen
gepackten Shipping-Build. QHD/High/TAAU75, VSync 0, kein FPS-Limit, keine Aufnahme.
Reguläres Schiggy-/Pikachu-/Glumanda-Team und ein echter aktiver Begleiter aus der
isolierten V4-QA-Fixture. Nutzerspielstände sind kein Schreibziel. 12 Wild-Pokémon,
Weltuhr, Sonnenbewegung und KI bleiben aktiv. `-nosound`: Audio ist nicht geprüft.

Dorf −4100/450/50,15, Wald −4300/1550/50,15, Innenraum 17050/500/50,15 cm.
20 Sekunden Szenen-Warm-up und zwölf Sekunden vor jedem Messfenster. Ortsfeste
Fenster je zehn Sekunden, bewegte Dorf-/Waldschleifen je 75 Sekunden mit normalen
Enhanced-Input-Actions und 15 Sekunden Sprint. Keine Teleports während der
Messfenster. Jeder Frame wird auf Fokus, tatsächliche Auflösung, High, TAAU und
Renderfraktion geprüft; langsame gültige Frames werden nicht entfernt.

FPS = 1000 / mittlere Framezeit je Lauf, Tabellenmittel aus den Läufen. p95/p99
werden aus allen zugehörigen Frames bestimmt, 1-%-Low = 1000 / Mittelwert des
langsamsten aufgerundeten Prozents. CPU-Zähler enthalten Wartezeiten und sind
keine reine Busy-Zeit. GPU-Scopes sind hierarchisch; nicht addieren.

Die neuen Läufe verwenden dieselben C-Renderingwerte wie V4. Abweichungen in den
Messwerten sind kein Nachweis einer zusätzlichen Optimierung durch V5: Hostlast,
Thermik, natürliche KI und Reihenfolge können abweichen. Die V4-Reihe mit 80
Fenstern/64160 Frames bleibt die umfangreichere Vergleichsbasis.

## Technische QA – bisherige Ergebnisse

- Editor-Build02: Exit 0, nach der abschließenden Profilwahlkorrektur.
- Originaler strenger ProjectQA-Lauf Automation01: Engine Exit 0, Wrapper Exit 1;
  279 ohne Warnung und zwei mit Warnungen, keine Fehler, insgesamt 281 Tests.
  Die beiden Testwarnungen betreffen ausschließlich das externe iOS-Hilfsprogramm
  `idevice_id` (Bad CPU type / failed to launch).
- Isolierte Wiederholung Automation02: gleicher vollständiger Testumfang und
  unveränderte strenge Ergebnisprüfung, zusätzlich `-UserDir`/`-nowrite` zum
  Schutz des Projekt-Saved. **281/281 ohne Testwarnung bestanden, Wrapper Exit 0**.
  Keine Warnungsfilterung oder Lockerung der Prüfkriterien.
- Neue Automation prüft beide echten Lumen-CVars, Profilwechsel, exakte
  Wiederherstellung von Werten/Prioritäten und explizite Nutzer-Overrides.

Laufzeit-, PIE-, Map- und Schutzprüfungen sind nachfolgend dokumentiert.


## Neue V5-Performance

20 Hauptfenster, **23243 echte Frames**, davon drei frische Standardprozesse und
ein zusätzlicher HardwareSPG-Kontrollprozess. Je Prozess drei ortsfeste und zwei
bewegte Fenster; insgesamt zwölf Minuten reine Messzeit. Reihenfolge C–Hardware–C–C.
Der einzelne neue Hardwarelauf ersetzt keine fünf gepaarten V4-Wiederholungen.

| Ort | Variante | Läufe | FPS Ø (Spanne) | GPU ms | Game ms | Render ms | Frame-p95 ms | 1-%-Low FPS | Max ms |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| Dorf | C Software/IFG | 3 | 35.28 (31.82–37.09) | 28.11 | 2.50 | 28.39 | 32.89 | 22.66 | 87.25 |
| Wald | C Software/IFG | 3 | 33.76 (29.59–36.64) | 29.52 | 2.35 | 29.88 | 36.39 | 20.10 | 53.21 |
| Innenraum | C Software/IFG | 3 | 48.37 (42.30–52.00) | 20.38 | 1.75 | 20.85 | 24.54 | 35.07 | 40.60 |
| DorfMoving | C Software/IFG | 3 | 33.00 (30.74–36.69) | 30.07 | 2.49 | 30.47 | 35.09 | 21.27 | 80.57 |
| WaldMoving | C Software/IFG | 3 | 32.47 (30.89–34.86) | 30.43 | 2.48 | 30.87 | 35.16 | 22.63 | 51.77 |
| Dorf | Hardware/SPG | 1 | 30.30 (30.30–30.30) | 30.11 | 2.65 | 32.83 | 35.50 | 19.22 | 82.70 |
| Wald | Hardware/SPG | 1 | 30.43 (30.43–30.43) | 31.83 | 2.01 | 32.86 | 34.94 | 26.76 | 38.70 |
| Innenraum | Hardware/SPG | 1 | 40.22 (40.22–40.22) | 23.89 | 2.16 | 24.86 | 26.90 | 35.18 | 31.53 |
| DorfMoving | Hardware/SPG | 1 | 26.23 (26.23–26.23) | 34.51 | 2.31 | 38.11 | 43.39 | 18.91 | 60.51 |
| WaldMoving | Hardware/SPG | 1 | 26.85 (26.85–26.85) | 35.48 | 2.29 | 37.23 | 41.20 | 18.30 | 67.85 |

Bewegter V4-Vergleich: Software/IFG damals Dorf 31,63 / Wald 32,47 FPS, GPU
31,50 / 30,67 ms, p95 34,90 / 34,76 ms. V5 nun **33,00 / 32,47 FPS**, GPU
30,07 / 30,43 ms und p95 **35,09 / 35,16 ms**. Der erwartete Leistungsvorteil
bleibt bestehen; daraus folgt keine Verbesserung der Framezeitstabilität.

Im neuen Hardware-Kontrolllauf bewegen sich Dorf/Wald mit 26,23/26,85 FPS,
GPU 34,51/35,48 ms. IFG-GPU-Scope beim bewegten C: 3,09/3,20 ms,
SPG im Hardwarelauf: 6,44/6,70 ms. Nicht mit anderen GPU-Scopes addieren.

C enthält 11/7424 Dorf- und 5/7305 Wald-Bewegungsframes über 50 ms. Größte
bewegte Spitze 80,57 ms; größte ortsfeste C-Spitze 87,25 ms. Keine Frames über
100 ms in diesen Hauptfenstern. Ursachen der Spitzen sind hier nicht durch
Callstacks isoliert und bleiben ein weiterer Optimierungsauftrag.

**Stabile 30 FPS sind weiterhin nicht nachgewiesen.** Bewegte p95-Werte liegen
über 33,3 ms und 1-%-Lows bei ca. 21–23 FPS. Ein ortsfester Waldlauf fällt auf
29,59 FPS. Keine langsamen Frames oder schwachen Läufe ausgeschlossen.

macOS-Thermalzustände, fünfsekündlich erfasst: C1 35×Nominal/26×Fair,
Hardware 18×Nominal/43×Fair, C2 22×Nominal/39×Fair, C3 61×Fair. AC-Strom,
kein Stromsparmodus. Fair ist kein gemessener GPU-Takt; thermische Drift und
Hostlast sind nicht vollständig eliminiert. Die höheren frühen C-Werte sind
kein zusätzliches Optimierungsversprechen durch die Umstellung.

Rohdaten und vollständige Verteilungen:
`Saved/ProjectRefinement/RenderingStandardV5/PerformanceSummary.json`,
`BenchC1…3/Measurements.json`, `BenchHardware/Measurements.json` sowie die
zugehörigen Frame-/GPU-CSV-Dateien. Keine großen Messdateien in Git.


## Gameplay, PIE und Profilwechsel

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Separates Development-Spiel | FunctionalC01: 67 Schritte bestanden |
| Reguläres Editor-PIE | PIEGameplay03: 67 Schritte bestanden |
| Grafikprofile | Default C → HardwareSPG → 100 → C; vier Zustände und 820 echte Rendererframes geprüft |
| Referenz 100 | interne/äußere Auflösung 2560×1440, HW/SPG 1/1, ursprüngliche VSM8 |
| Referenz HardwareSPG | interne 1920×1080, HW/SPG 1/1, VisualV2-VSM4 |
| Standard C | interne 1920×1080, Software/IFG 0/0, VisualV2-VSM4 |
| Mapwechsel | VisualV2 → vorhandene Dev_TestMap → VisualV2; zwei frische Läufe bestanden |
| CLI-Referenz → C → Mapreise | bewusste neue Profilwahl bleibt erhalten; korrigierter Vorrang nachgewiesen |
| Save/Load | Innenraum, genaue Position, Nachtzeit, unabhängiger Kontrollpunkt, Team/IDs/KP/AP/Repertoire erhalten |
| Kampf und Fang | Bisasam herausfordern/Attacke/Flucht; Myrapla angreifen/fangen; Team wächst auf vier |
| Begleiter und Teamsortierung | echter Schiggy-Begleiter, anschließend Pikachu über Teamplatzwechsel; nach Save/Load korrekt |
| Tag/Nacht | normale Grenzübergänge 04/05/07/18/20 Uhr und Mitternacht/Tag 2; Tageslänge 120 unverändert |
| Controller-Software | acht Richtungen, L3 an/aus, X, Steuerkreuz, L/R, Plus, B bestätigt Team, A schließt und gibt Fokus zurück |
| Finaler PIE-Phasenzyklus | Nachtübergang, gültige soziale Partnerreservierungen und normales Spielerhandeln bestanden |
| Editor-Wiederherstellung | alle 19 erfassten Rendering-/Qualitätswerte wiederhergestellt; keine schmutzigen Maps/Assets |
| Zwölf Map Checks | jeweils ausdrücklich 0 Fehler / 0 Warnungen im MAP-CHECK-Logblock; Originalmap wieder geöffnet |

Native Tests schreiben nur in eigene UserDirs; PIE verwendet einen ausdrücklich
isolierten `PokeMonster_SaveV2_Test_RenderingV5PIE01`-Slot im eigenen UserDir.
Die ursprüngliche V4-QA-Fixture wird nur gelesen. Es gibt keine Kopie eines
Nutzerspielstands als Schreibziel. Die Kontrollzyklen verwenden tatsächliche
Slate-/Enhanced-Input-Verarbeitung, keinen Nachweis der physischen Switch-Tasten.

### Fehlgeschlagene Prüfversuche, unverändert aufbewahrt

- PIEGameplay01 brach nach sieben Schritten ab: `setnopec`-Propertyänderungen
  sind im Editor gesperrt. Der native Ablauf war dafür ungeeignet. Der PIE-Test
  verwendet anschließend die vorhandenen `pm.WorldClock`-Befehle, mit deren
  Minutenpräzision und ausreichender normaler Wartezeit an Phasengrenzen.
- PIEGameplay02 brach vor dem zweiten Kampf ab: der feste Annäherungspunkt
  erlaubte keine normale Interaktion mit Myrapla. PIEGameplay03 nähert sich
  begrenzt von anderen Seiten und ruft unverändert `TryInteract` auf. Myrapla
  wurde beim zweiten normalen Annäherungsversuch akzeptiert. Keine Deaktivierung
  von KI, Kollision oder Sichtprüfung und kein erzwungener Kampfstart.
- Erster zusätzlicher Bewegungszyklus: falsche Erwartung, dass B im Hauptmenü
  sofort fortsetzt. Tatsächlich ist der erste Eintrag Team. Die korrigierte
  Prüfung bestätigt genau dieses vorhandene Verhalten und schließt mit A.

Diese drei Resultate bleiben als fehlgeschlagen gekennzeichnet; sie werden nicht
zu Erfolgen umetikettiert. Danach vollständiger PIE-Durchlauf und beide finalen
Kontrollzyklen bestanden. Insgesamt sechs reguläre PIE-Start-/Stopp-Sitzungen,
keine gewaltsame Beendigung. Die letzten zwei Stopps benötigen einschließlich
fest eingeplanter drei Sekunden Kontrollwartezeit ca. 3,21/3,22 Sekunden.
Der eigene Editor PID 20155 wurde nach sauberer Wiederherstellung regulär
beendet. Ein früherer Editorstillstand wurde nicht erneut beobachtet.

## Visuelle Prüfung und Grenzen

Echte QHD-Spielkamera-Aufnahmen liegen unter
`Saved/ProjectRefinement/RenderingStandardV5/Photos01/`:
Dorf06, Dorf12, Dorf19, Dorf22, Wiese09, Wald12, Wald22, Waldrand19,
Innenraum12 und Innenraum22. `FunctionalC01/` und `PIEGameplay03/` enthalten
zusätzlich tatsächliche ClassicBattle-, Innenraum- und Begleiteraufnahmen;
`Profiles01/` dokumentiert die vier Umschaltzustände. Normale Viewport-Shots,
keine generierten Bilder oder interpolierten Videos. Die 18 nativen Aufnahmen
haben 2560×1440. Die sechs PIE-Aufnahmen mit `-showui` erfassen das Editorfenster
mit 2940×1696 und sind ergänzende UI-Nachweise, keine QHD-Kameravergleiche.
Eine zunächst pauschal auf QHD prüfende Medienvalidierung brach daran ab; die
Dateien wurden weder verändert noch auf QHD umgerechnet.

Stichproben zeigen weiterhin Sonnen-/Vegetationsschatten, lesbare Wege,
Originalfarben von Spielfigur/Pokémon und unveränderte Innenraum-Grundhelligkeit.
Kein offensichtlicher neuer schwerwiegender Bildfehler in diesen geprüften
Szenen. Die 19-Uhr-Waldrandszene liegt unmittelbar neben dem vorhandenen Gebäude;
keine neue freie Kameraperspektive oder Geländeänderung. Vorhandene
Kronenfreistellung und nutzerseitige Debuganzeigen bleiben erhalten.

**Keine abschließende temporale Bildfreigabe.** Die in V4 unzureichende
Aufnahmeleistung und die derzeit nicht verfügbare ScreenCaptureKit-Freigabe
bleiben offene Nachweise. Neue Standbilder beweisen kein fehlendes Ghosting,
GI-Nachziehen oder feines Flimmern. Keine neuen umfangreichen Videos erzeugt.
Die Übernahme erfolgt ausdrücklich aufgrund Harrys V5-Entscheidung; die offene
Bildprüfung und p95-/Spitzenoptimierung bleiben dokumentierte Folgearbeiten.

## Logbefunde

Die erfolgreiche strenge Testauswertung ist keine Behauptung warnungsfreier
Engine-Logs. Externe iOS-Helferwarnungen `idevice_id` treten weiter auf. Native
Prozesse protokollieren je 58 Python-Startfehlerzeilen zu den fehlenden externen
Editor-API-Klassen AgentSkill, ToolsetDefinition und PythonTestRunner. Editor/
Automation zeigen beim Start 17 `LogAutomationTest: Condition failed`-Zeilen;
diese sind bereits in älteren Referenz-Automationlogs vorhanden und liegen vor
der Projekt-Testsession. Sie werden von den 281 erfolgreichen Projekt-Test-
ergebnissen getrennt aufgeführt, nicht gelöscht oder als neue Renderfehler erklärt.

Weitere Meldungen betreffen EditorDataStorageUI, verzögerte Python-Startbefehle,
Bewegungs-Substeps während des Starts und die häufigen CVar-Abfragen des
Diagnoseskripts. Die LeafOak-Material-Usage-Warnung beim ClassicBattle ist schon
in V4 FunctionalA03 und FunctionalC01 vorhanden. Keine entsprechende Asset-
Änderung zum Verbergen der Meldung. Keine beobachteten Fatal-/Assertion-/Metal-
oder RHI-Fehler in den ausgewerteten Laufzeitlogs. Vollständige Kategorien und
Zählungen: lokales `LogAudit.json`; MAP-CHECK-Nachweis: `MapCheckValidation.json`.

## Projektschutz und beobachtetes Unreal-Housekeeping

Die Baseline umfasst 6370 bereits vorhandene Dateien, einschließlich 403 `.sav`
und 34 unversionierter Eingänge. Originale, Karten, Modelle, Animationen,
vorbestehende DefaultEngine.ini-Änderung, unversionierte Eingänge und beide
Vollbackup-Gitverweise werden gegen ihre ursprünglichen Hashes geprüft.

Der erste unveränderte ProjectQA-Runner startet ohne isoliertes UserDir und ohne
`-nowrite`. Dabei wurde die generierte
`Saved/Config/MacEditor/EditorPerProjectUserSettings.ini` neu geschrieben und
30 ältere `Saved/Config/CrashReportClient/UECC-…/CrashReportClient.ini` entfernt.
Die lokale Engine ruft beim Initialisieren `PurgeOldCrashConfig` mit standardmäßig
zwei Tagen Aufbewahrung auf. Das wurde nach der ersten Automation festgestellt,
explizit inventarisiert und nicht als unverändert ausgegeben. Die Baseline
enthält Hashes; keine unbewiesene Sicherung oder exakte Rücksetzung dieser
Generatdateien wird behauptet. Alle folgenden Tests verwenden isolierte UserDirs
und `-nowrite`; die strengen Automationserwartungen wurden dabei nicht gelockert.

Keine manuelle Bereinigung, keine neuen Maps, Worktrees, Projektkopien oder
Vollbackups. Der vorhandene UnrealEditorServices-Prozess blieb unangetastet.
Source-/Dokumentationsänderungen beschränken sich auf die vorhandene
Profilverwaltung, zugehörige Tests, Profilkommentare und Rendering-Dokumentation.


## Endkontrolle und Git-Sicherung

Ein weiterer frischer Development-Spielprozess nach dem regulären Editorende
bestätigt ohne Profilargument und ohne Lumen-Overrides erneut C: HWRT 0, IFG 0,
75 %, TAAU, VSM1/Strahlen4, High und 2560×1440. 293 zusätzliche Rendererframes
validiert; dieses achtsekündige Abschlussfenster ist kein weiterer Nachweis
stabiler Frameraten und nicht in die 20 Hauptfenster eingerechnet.

Die finale Hashkontrolle bestätigt 6332 unveränderte Bestandsdateien,
403/403 vorbestehende `.sav`, 34/34 unversionierte Eingänge, sämtliche erfassten
Map-/Originaldateien, DefaultEngine.ini und beide Backup-Refs unverändert.
Sieben vorhandene Dateien wurden gezielt für V5 angepasst; der neue Bericht
kommt hinzu. Die oben beschriebenen 31 generierten Konfigurations-Nebeneffekte
bleiben separat ausgewiesen. Nach der ersten Automation keine weiteren
unerwarteten Änderungen oder fehlenden Bestandsdateien. Keine neuen Assets
und keine zugehörigen neuen LFS-Objekte.

Lokale Belege: `FinalRuntimeProof.json`, `ProtectionFinalBeforeCommit.json`,
`BuildAndQA.json`, `EditorRestored.json`, `EditorCycles.json`, die jeweiligen
`Result.json` und `LogAudit.json` unter Saved/ProjectRefinement/RenderingStandardV5.
Der frühere V4-Bericht bleibt als unveränderte lokale Referenz erhalten.

Geprüfte Implementierung: **8cfda0502a2d6a891273452eea16a8069478a418**.
Die Rendering-Dokumentation und dieser Prüfbericht werden anschließend als
getrennter Dokumentationscommit gesichert. Bestehende DefaultEngine.ini-
Nutzeränderungen und die 34 unversionierten Eingänge bleiben außerhalb der
Commits. Exakte finale Commit-/Remote-/LFS-Kontrolle steht lokal in
`Saved/ProjectRefinement/RenderingStandardV5/GitFinal.json` und im Abschlusschat.


Lokale Bildbeispiele:
[Dorf 12:00](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/RenderingStandardV5/Photos01/Dorf12.png),
[Wald 22:00](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/RenderingStandardV5/Photos01/Wald22.png),
[Innenraum nachts](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/RenderingStandardV5/Photos01/Innenraum22.png),
[ClassicBattle](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/RenderingStandardV5/FunctionalC01/C_ClassicBattle.png).
