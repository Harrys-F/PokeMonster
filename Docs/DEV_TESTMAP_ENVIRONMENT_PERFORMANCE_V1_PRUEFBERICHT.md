# PokeMonster – Environment Performance Optimization V1

Stand: 15.10.2026. **Isolierter, messbar schnellerer Rendering-Kandidat. Keine automatische Übernahme in die visuelle Baseline. Die Leistungsziele sind weiterhin nicht durchgehend erreicht.**

Arbeitskarte: **/Game/Maps/Dev_TestMap_EnvironmentPerfV1**. Keine Änderungen an den ursprünglichen Testkarten, kein Commit, kein Push.

## 1. Ausgangsstand und Schutz

HEAD: **351a3ef Add YoungTrainer sprint V1 and in-place run animation**. Der Arbeitsbaum war bereits verändert. Die offene NPC-Integration, Incoming-Originale, der Ranger-V2-Versuch und die bestehende VisualV2-Map gehörten zum Ausgangsstand. Sie wurden weder verworfen noch als eigene neue Ergebnisse beansprucht.

Gelesen: AGENTS, relevante TECHNIK/ENTSCHEIDUNGEN/GRAFIKSTIL/SPIELIDEE/SPIELREGELN, VisualV2-, NPC-Integrations-, Ranger-Performance-V2-, V3-Asset- und Kronenfreistellungsberichte sowie tatsächliche Implementierungen. Blender blieb unberührt; keine vorhandene Quelle wurde neu erzeugt oder überschrieben.

Vor Beginn wurden 2717 vorhandene versionierte/unversionierte Dateien mit Größe und SHA-256 erfasst. Abschließend 2714 bytegleich; bewusste Änderungen ausschließlich: Docs/ENTSCHEIDUNGEN.md, Docs/TECHNIK.md, Source/PokeMonster/PokeMonster.Build.cs. Dokumente nur ergänzt, anfänglicher Inhalt vollständig erhalten. Build.cs ausschließlich um RenderCore ergänzt. Keine fehlenden oder unerwartet geänderten Ausgangsdateien.

Original-Testkarten einschließlich VisualV2 und RangerPerfV2, Ranger-V1/V2-Assets, alle Incoming-Modelle, Blenderquellen und Playerdateien sind gegenüber Aufgabenbeginn bytegleich. Das bedeutet nicht sauber gegenüber HEAD: Vorher offene Änderungen bleiben offen.

Die neue Karte entstand über die Unreal-Editor-API: save_map unter neuem Pfad, danach explizites Laden. Das Original wurde nicht gespeichert. Der Actor-/Komponentenvergleich findet **keine geänderten bestehenden Positionen, Rotationen, Skalierungen, Meshes, Materialzuweisungen, Instanztransformationen oder Kollisionen**. Hinzu kommt genau ein tick- und kollisionsfreier Rendering-Infoactor. Drei automatisch erzeugte Editor-Manager (Buoyancy, GameplayDebugger, AbstractNavData) und WorldSettings wurden beim persistenten Actorvergleich ausdrücklich ausgeklammert.

## 2. Messmethode und tatsächliche Auflösungen

MacBook Air M4, 16 GB gemeinsamer Speicher, macOS, UE 5.8.2, Metal. Kamera unverändert: **2850 cm / Pitch −50° / Yaw −45° / FOV 35°**. Player 140 cm, normale Bewegung 210 cm/s. Alle Grafik-Scalability-Gruppen jeweils 1 (Medium) oder 2 (High). VSync=0, t.MaxFPS=0, DynamicRes.OperationMode=0, sekundäre Auflösung=100%, PIE-Auflösungsüberschreibung=0. Keine gespeicherten globalen Grafik-/Projekt-Configänderungen.

Der verbindliche Standard wurde zusätzlich in TECHNIK festgehalten:

| Ausgabe | Qualität | Screen Percentage | Interne Bildgröße laut konstantem Renderer-Treiber |
|---|---|---|---|
| 1280×740 | Medium | 75% | 960×555 |
| 1280×740 | Medium | 100% | 1280×740 |
| 2560×1440 | Medium | 75% | 1920×1080 |
| 2560×1440 | Medium | 100% | 2560×1440 |
| 2560×1440 | High | 75% | 1920×1080 |
| 2560×1440 | High | 100% | 2560×1440 |

Fenster, Spiel-Viewport, Render-Target und tatsächliches unskaliertes ViewRect werden getrennt geloggt. Das eingebettete Editorfenster hat 2940×1696 Slate-Pixel, DPI 2; **das sind nicht die Spielmessauflösungen**. FSceneViewport::SetFixedViewportSize setzt den tatsächlichen Game-Viewport/Render-Target auf die Tabellenauflösung. Native Fenstermaße und alle pro Segment beobachteten Größen stehen in MeasurementValidation.json.

Die internen Größen sind **abgeleitet** aus dem auf dem Renderthread gelesenen konstanten Screen-Percentage-Treiber und der UE-5.8-ceil-Regel bei deaktivierter dynamischer Auflösung. Keine direkte SceneColor-Allocation-Readback-Messung. Pufferpadding und einzelne Passauflösungen sind nicht erfasst. Fenster- oder r.SetRes-Angaben allein werden nicht als Nachweis benutzt.

Drei Messorte (Player-Capsule-Zentrum in cm):

- Dorf am tatsächlichen Heilhausvorplatz: (−4100, 450, 50.15).
- Dichter nördlicher Wald: (−4300, 1550, 50.15).
- Offener Weg: (−36.6, −47.1, 50.15).

Die Kameraposen werden pro Frame protokolliert. Ranger V1 bleibt in der Karte, NPCs im Idle, keine Gespräche/Kämpfe während Performancefenstern. Je finaler Einzelmessung 5 Sekunden Warm-up und 6 Sekunden Messung, je Ort/Konfiguration drei benachbarte Kontrolle/Kandidat-Paare. Reihenfolge in Wiederholung 2 umgedreht. Die frühere unoptimierte Baselinereihe verwendet 5/8 Sekunden und ist separat enthalten; wegen Zeitdrift wird sie nicht allein als kausaler Vorhervergleich benutzt. Einzelfaktorserien: dokumentierte 3/5- oder 4/6-Sekunden-Fenster; zusätzlicher Lumen-Test 5/8 Sekunden. Pläne und UTC-Zeiten liegen bei.

Median-FPS = 1000 / Median der nativen Wall-Clock-Frameintervalle. P95 = linear interpoliertes 95. Perzentil derselben Einzelmessung. Die Zusammenfassung zeigt den Median aus drei Laufmedianen bzw. **Median der drei Lauf-P95**, kein aus allen Frames gemischtes P95. Einzelwerte und CPU-/GPU-Zähler bleiben in Measurements.json. Null gemeldete DrawCall-/RHI-/PIE-Renderthread-Zähler gelten als nicht auswertbar, nicht als kostenlose Arbeit. GPU-Pässe können überlappen und dürfen nicht addiert werden.

Editor während Standalone geschlossen. Keine parallelen Builds, Blender-Renderings oder Hashaudits während der GPU-Messungen. Standalone ist ein nativer Development-Prozess mit dem Editorbinary und -game, **kein paketierter Shipping-Build**. Identische angeforderte Grafikwerte, gleiche Messorte und gleiche Faktoren. Modusvergleiche separat, Optimierungsnachweis innerhalb desselben Modus. Im Standalone wird die unveränderte VisualV2 geladen und nur der reversible Runtime-Kandidat appliziert; keine Baseline-Datei gespeichert.

Thermalmonitor (10-Sekunden-Abstand): {'fair': 830, 'nominal': 73}. NSProcessInfo-Labels sind keine °C-/Taktfrequenzmessungen. Zeit-/Temperaturdrift bleibt trotz Verschachtelung möglich.

Sechs Sekunden sind kurze reproduzierbare Stichproben, kein Langzeit-Stabilitätsnachweis für 60 FPS. Keine fremden Apps oder Systemeinstellungen wurden zur FPS-Steigerung beendet/geändert.

## 3. Vegetation, Schatten und Postprocessing

41 V3-Alteichen, vier Birken, 102 V3-Buschinstanzen (55 A/47 B, teilweise HISM). Dies sind platzierte Instanzen, **keine** exakten pro Kamerabild sichtbaren GPU-Instanzen.

| Familie | LOD-Dreiecke | Abschnitte / Hinweise |
|---|---|---|
| V3-Alteiche | 12068 / 7240 / 3621 | 2 Abschnitte; Screen Sizes 1 / .34 / .13 |
| V3-Busch A | 3284 / 1971 / 986 | 2 Abschnitte |
| V3-Busch B | 3396 / 2038 / 1019 | 2 Abschnitte |
| Birke | 28628 / 17177 / 8588 | 2 verwendete Abschnitte, 4 Materialslots |
| Farn | 8030 / 4818 / 2409 | 46 Instanzen, 1 Abschnitt, 3 Slots |
| Gras | 576 pro LOD0-Objekt | 175 erfasste Instanzen |
| Wildblumen | 2160 pro LOD0-Objekt | 63 erfasste Instanzen |
| Kräuter | 1152 pro LOD0-Objekt | 55 erfasste Instanzen |

Weitere NaturalGround-/Heilhausgruppen stehen im Audit. Die Inventarsumme von 922 Instanzen enthält auch Dorf-/Ruinen-/Landschaftsprops; sie ist keine sichtbare Vegetationsanzahl. Alle LOD0-Instanzen dieses Audits summieren sich theoretisch auf 1.732.692 Dreiecke: obere Inventarsumme, kein gemessener Drawn-Triangle-Wert.

HISM/ISM, bestehende LODs und Sichtweiten sind bereits vorhanden. Kleine Vegetation/Büsche werfen überwiegend schon keine Schatten. HISM-Unterwuchs cullt meist 4500–6500 cm, Heilhausunterwuchs 3200–4300 cm. Keine massenhafte Entfernung, keine versetzten Bäume und keine neuen Material-/Meshvarianten wurden nötig.

Blätter verwenden zweiseitige Masked-Atlasmaterialien, bei V3 eine gemeinsame Blattatlas-Abtastung; Reveal-Rinde ist ebenfalls Masked. Masked-Overdraw wurde nicht quantitativ isoliert. Ein null gemeldeter Translucency-Pass beweist keine kostenlosen Blätter. Keine zuverlässigen Materialinstruction-/sichtbaren Instanz-/DrawCall-Zahlen verfügbar. Material- und Texturfamilien unverändert.

Aktive Schattenmethode: **Virtual Shadow Maps**, r.Shadow.Virtual.Enable=1. Schattenprojektion kostet deutlich mehr als allein Shadow Depths; ein CSM-Distanz-CVar ist deshalb kein vollständiger Nachweis einer VSM-Reichweitenoptimierung. Keine neuen dynamischen Lichter.

Beispiel Wald-Kontrolle QHD/High/100%, Median aus drei finalen PIE-Läufen:

| Zähler | Median |
|---|---:|
| GameThreadTime | 7.540 ms |
| RenderThreadTime | nicht zuverlässig verfügbar |
| GPUTime | 73.895 ms |
| GPU/LumenScreenProbeGather | 13.874 ms |
| GPU/ShadowProjection | 7.518 ms |
| GPU/ShadowDepths | 2.693 ms |
| GPU/Basepass | 3.290 ms |
| GPU/SlateUI | 3.485 ms |
| GPU/LumenSceneUpdate | 1.598 ms |
| GPU/MotionBlur | 0.769 ms |
| GPU/TemporalSuperResolution | 0.239 ms |
| GPU/Unaccounted | 23.220 ms |

Lumen Screen Probe Gather ist bei High ein großer klar benannter Pass. Daneben bleiben Schattenprojektion, Basepass, Slate/Editor und ein erheblicher nicht eindeutig zugeordneter GPU-Anteil. **Nicht bewiesen**, dass Vegetation, Ranger oder Lumen allein die gesamte GPU-Last erklären. Auflösungsabhängige GPU-Zeiten und kleinere Game-Thread-Zeiten sprechen bei QHD für ein GPU-Limit. PIE-Renderthreadwerte liegen nahe null und werden als nicht verwertbar markiert. Native Renderthread-Wall-Zeiten enthalten Wartezeit auf GPU/Present; sie sind kein Nachweis reiner CPU-Rechenarbeit. Keine vollständige CPU-Kausalanalyse.

AA bleibt TSR (r.AntiAliasingMethod=4). Der alte r.PostProcessAAQuality-CVar ist in UE 5.8 entfernt; eine anfängliche Nullabfrage wird nicht als abgeschaltetes AA interpretiert. Tonemapper, TSR und Texturqualität werden nicht abgesenkt. Keine zusätzlichen Postprocess-Blendable-Materialien in den zwei Volumes. Klassisches AOOff ist kein vollständiger Schalter für Lumens Short-Range-AO.

## 4. Kontrollierte A/B-Versuche

Alle drei Einzelfaktor-Paare, Mediane und GPU-Differenzen stehen in der folgenden Tabelle. Je Paar nur ein Faktor; anschließend Komponentensichtbarkeit, Schatten, ForcedLOD, Culling, Volumes und CVar-Werte/Prioritäten restauriert.

- Bäume ohne Schatten: kleiner konsistenter Vorteil im Wald, aber Verlust natürlicher Waldbeleuchtung; nicht übernommen.
- Sämtliche Schatten aus: deutlicher diagnostischer Vorteil, erheblicher Bildverlust; nicht übernommen.
- Vegetation unsichtbar: diagnostischer Vorteil, keine akzeptable Maßnahme; niemals gespeichert.
- Schatten-MaxResolution=1024: bei High bereits 1024, somit No-op/Driftkontrolle statt echter Einsparung. Nicht als Erfolg gewertet.
- Halbe Shadow.DistanceScale und gröberer VSM-LOD-Bias: kein konsistenter Vorteil; nicht übernommen.
- **VSM-Richtungslicht 2 SMRT-Rays statt High 8 / Medium 4**: konsistenter Nutzen in Wald-/Dorf-/Weg-Paaren. Samples pro Ray und Reichweite erhalten. Feines Schattenrauschen bleibt eine Abnahmegrenze.
- AOOff, halbe Reflection-/FinalGather-Qualität: gemischte Ergebnisse; keine pauschale GI-/AO-/Reflexionsabsenkung übernommen.
- Forced TreeLOD1, FernLOD1 und kürzeres SmallFoliageCull: kein stabiler Vorteil; keine Geometrie-/LOD-/Cullingänderung übernommen.
- **BloomIntensity=0 außen**: kleiner, weitgehend konsistenter Vorteil; statische QHD-Paare zeigen kaum veränderte Komposition.
- **MotionBlurAmount=0 außen**: überwiegend kleiner Nutzen, einzelne verrauschte Paare. Der finale kombinierte Kandidat wird eigenständig gemessen. Außenbewegung ist schärfer, Animationstempo unverändert.
- **Lumen ScreenProbeGather IntegrateDownsampleFactor=2 statt 1**: zusätzlicher High-Test. GPU-SPG-Kosten sinken in allen neun Ortspaaren, Gesamtframezeit in acht von neun. Laut lokalem Engine-Quellkommentar verwischt dies feinere indirekte Normaldetails. QHD-Standbilder geprüft. Medium verwendet eine andere Gather-Methode; dort wird kein Lumen-Gewinn vorausgesetzt.

## Einzelfaktor-Paare

Negative Differenzen bedeuten kürzere Framezeit. Drei benachbarte Paare, umgekehrte Reihenfolge in Wiederholung 2. QHD/High/75%.

| Serie/Ort | Faktor | Δ Frame ms je Paar | Median Δ Frame ms | Median Δ GPU ms |
|---|---|---|---:|---:|
| FactorsWald/Wald | TreeNoShadow | -0.664, -1.332, -0.745 | -0.745 | -0.417 |
| FactorsWald/Wald | ShadowRes1024 | +2.147, +0.189, +1.081 | +1.081 | +1.130 |
| FactorsWald/Wald | ShadowDistanceHalf | +1.513, +0.095, -1.092 | +0.095 | +0.457 |
| FactorsWald/Wald | VSMBiasPlus1 | +3.327, +0.630, -0.407 | +0.630 | +0.853 |
| FactorsWald/Wald | VSMRayCount2 | -1.331, -0.666, -1.741 | -1.331 | -1.016 |
| FactorsWald/Wald | AOOff | -1.734, +1.579, -0.068 | -0.068 | +0.347 |
| FactorsWald/Wald | BloomOff | -1.383, -1.007, -0.742 | -1.007 | -0.868 |
| FactorsWald/Wald | MotionBlurOff | +5.316, -1.379, -2.118 | -1.379 | -0.887 |
| FactorsWald/Wald | GIFinalGatherHalf | -2.259, +0.325, +0.151 | +0.151 | -0.234 |
| FactorsWald/Wald | ReflectionHalf | -1.287, +0.159, +0.516 | +0.159 | -0.308 |
| FactorsWald/Wald | SmallFoliageCull | +2.918, -0.642, +0.060 | +0.060 | +0.217 |
| FactorsWald/Wald | TreeLOD1 | -0.385, -0.160, +0.111 | -0.160 | +0.020 |
| FactorsWald/Wald | FernLOD1 | +1.669, +0.099, -0.271 | +0.099 | +0.387 |
| FactorsDorfWeg/Dorf | VSMRayCount2 | -3.081, -0.745, -1.302 | -1.302 | -1.115 |
| FactorsDorfWeg/Dorf | BloomOff | -0.589, -1.129, -1.812 | -1.129 | -0.891 |
| FactorsDorfWeg/Dorf | MotionBlurOff | +1.972, -1.356, -2.044 | -1.356 | -1.017 |
| FactorsDorfWeg/Dorf | GIFinalGatherHalf | -1.618, -1.344, -0.544 | -1.344 | -0.406 |
| FactorsDorfWeg/Weg | VSMRayCount2 | -0.132, -1.243, -1.593 | -1.243 | -1.147 |
| FactorsDorfWeg/Weg | BloomOff | -0.803, -2.283, +0.375 | -0.803 | -0.544 |
| FactorsDorfWeg/Weg | MotionBlurOff | -0.598, -1.432, -4.113 | -1.432 | -0.922 |
| FactorsDorfWeg/Weg | GIFinalGatherHalf | -0.191, +0.415, +0.363 | +0.363 | +0.441 |
| IntegrationAB/Dorf | LumenIntegrate2 | -0.447, -1.420, -0.482 | -0.482 | -0.334 |
| IntegrationAB/Wald | LumenIntegrate2 | -1.701, +0.119, -0.805 | -0.805 | -0.968 |
| IntegrationAB/Weg | LumenIntegrate2 | -3.557, -0.563, -0.749 | -0.749 | -1.133 |
| VegetationAB/Dorf | VegetationHidden | -6.145, -3.031, -3.396 | -3.396 | -2.773 |
| VegetationAB/Wald | VegetationHidden | -3.316, -3.275, -1.013 | -3.275 | -3.228 |
| VegetationAB/Weg | VegetationHidden | -5.453, -4.121, -5.621 | -5.453 | -5.070 |
| VegetationAB/Wald | AllShadowsOff | -7.469, -8.284, -6.550 | -7.469 | -7.422 |

Keine akzeptierte Maßnahme beruht allein auf theoretischen Polygon-/FPS-Zahlen. Kombinierte Effekte sind nicht additiv.

## 5. Umgesetzter separater Kandidat

Nur in Dev_TestMap_EnvironmentPerfV1:

1. Neuer APokeMonsterEnvironmentRenderProfile ohne Tick, Collision oder Gameplayreferenzen. Exakter Levelnamen-Guard, keine Aktivierung in Baselines. BeginPlay setzt zwei Renderer-CVars reversibel, EndPlay restauriert Werte/Prioritäten. Höher priorisierte manuelle Nutzerwerte werden respektiert; parallele experimentelle World bekommt keinen zweiten Besitzer.
2. r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor=2.
3. r.Shadow.Virtual.SMRT.RayCountDirectional=2.
4. Unbound-Außenvolume: BloomIntensity=0, MotionBlurAmount=0, jeweilige Overrides an.
5. Bounded-Heilhaus-Innenvolume: ursprüngliche Werte .675/.5 explizit erhalten, um sie gegen die Außenvolume-Overrides zu schützen. Keine neue Lichtstimmung.

Die beiden Renderer-CVars sind engineweit wirksam, **aber nur während der Laufzeit dieser Testworld**, keine echten per-Volume-CVars. Keine Config wird geschrieben. Deshalb keine allgemeine Lösung für mehrere gleichzeitig gerenderte Welten oder Split-Screen. Scope-/Baseline-Ausschluss hat einen eigenen Test. In echter PIE sind 2/2 bei Aktivierung sowie 1/8 nach Ende nachgewiesen.

Build.cs erhält RenderCore für die Auflösungsbeobachtung. Der Messprobe ist opt-in und in Shipping deaktiviert; er startet keine automatischen Benchmarks. Keine neue Vegetation, keine verschobenen Instanzen, keine neuen LODs, keine geänderten Blatt-/Reveal-Materialien. Player/NPC-Animationen, Kamera, Reveal-Fade 0,25 s und Spielregeln unverändert.

## 6. Finale reproduzierbare Messwerte

Jede Zeile: drei Kontrolle/Kandidat-Paare. P95-Spalte: Median aus den drei Lauf-P95. CPU/GPU in ms. Einzel-P95 und weitere Pässe in Measurements.json.

## Finale Paare: PIE

| Ausgabe | Qualität | SP | Ort | Kontrolle FPS | Kandidat FPS | Kontrolle Frame ms | Kandidat Frame ms | Δ ms je Paar | Median Δ ms | Kontrolle/Kandidat P95 ms | Kontrolle/Kandidat Game ms | Kontrolle/Kandidat Render ms | Kontrolle/Kandidat Render CriticalPath ms | Kontrolle/Kandidat GPU ms |
|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|---|
| 1280×740 | Medium | 75% | Dorf | 45.48 | 46.50 | 21.990 | 21.507 | -0.612, +0.027, -0.569 | -0.569 | 27.140/25.855 | 8.568/8.622 | n/v/n/v | n/v/n/v | 20.517/20.006 |
| 1280×740 | Medium | 75% | Wald | 46.36 | 47.98 | 21.572 | 20.840 | -0.779, -0.453, -0.718 | -0.718 | 25.834/25.187 | 8.516/8.355 | n/v/n/v | n/v/n/v | 19.948/19.370 |
| 1280×740 | Medium | 75% | Weg | 45.00 | 46.86 | 22.223 | 21.338 | -1.210, -0.362, -0.364 | -0.364 | 26.568/26.000 | 8.834/8.829 | n/v/n/v | n/v/n/v | 20.414/19.937 |
| 1280×740 | Medium | 100% | Dorf | 36.60 | 37.90 | 27.320 | 26.383 | -0.937, -3.017, -0.667 | -0.937 | 30.517/30.274 | 8.437/8.415 | n/v/n/v | n/v/n/v | 25.259/24.683 |
| 1280×740 | Medium | 100% | Wald | 36.95 | 39.18 | 27.065 | 25.525 | -0.932, -1.540, -0.228 | -0.932 | 30.434/29.690 | 7.862/8.842 | n/v/n/v | n/v/n/v | 24.508/23.756 |
| 1280×740 | Medium | 100% | Weg | 35.26 | 37.36 | 28.364 | 26.765 | -2.334, +0.145, -1.253 | -1.253 | 33.579/30.658 | 13.737/8.506 | n/v/n/v | n/v/n/v | 25.976/24.808 |
| 2560×1440 | Medium | 75% | Dorf | 23.72 | 24.72 | 42.166 | 40.459 | -3.413, -1.707, -1.591 | -1.707 | 47.729/46.288 | 6.638/6.365 | n/v/n/v | n/v/n/v | 40.792/39.279 |
| 2560×1440 | Medium | 75% | Wald | 23.87 | 25.36 | 41.896 | 39.437 | -3.201, -1.477, -2.258 | -2.258 | 46.769/45.198 | 6.300/6.408 | n/v/n/v | n/v/n/v | 40.282/36.923 |
| 2560×1440 | Medium | 75% | Weg | 22.73 | 24.05 | 43.989 | 41.585 | -1.249, -2.405, -1.533 | -1.533 | 48.885/46.901 | 6.582/6.799 | n/v/n/v | n/v/n/v | 42.320/39.587 |
| 2560×1440 | Medium | 100% | Dorf | 16.66 | 17.30 | 60.021 | 57.805 | -4.500, -0.523, -3.292 | -3.292 | 66.490/64.408 | 6.811/7.063 | n/v/n/v | n/v/n/v | 57.724/54.639 |
| 2560×1440 | Medium | 100% | Wald | 17.21 | 17.84 | 58.095 | 56.067 | -2.302, -2.027, -2.868 | -2.302 | 65.224/61.348 | 6.743/6.671 | n/v/n/v | n/v/n/v | 55.824/53.913 |
| 2560×1440 | Medium | 100% | Weg | 16.81 | 17.61 | 59.480 | 56.791 | -1.860, -2.435, -2.818 | -2.435 | 65.028/63.662 | 6.833/6.740 | n/v/n/v | n/v/n/v | 56.775/54.931 |
| 2560×1440 | High | 75% | Dorf | 18.92 | 19.57 | 52.852 | 51.099 | -2.587, -0.861, -1.753 | -1.753 | 59.180/58.817 | 6.563/7.003 | n/v/n/v | n/v/n/v | 50.108/48.324 |
| 2560×1440 | High | 75% | Wald | 18.63 | 20.39 | 53.668 | 49.055 | -3.804, -4.739, -4.433 | -4.433 | 58.244/53.286 | 7.256/6.710 | n/v/n/v | n/v/n/v | 50.554/46.369 |
| 2560×1440 | High | 75% | Weg | 17.83 | 19.63 | 56.084 | 50.950 | -3.713, -3.890, -5.133 | -3.890 | 63.150/55.720 | 6.958/6.504 | n/v/n/v | n/v/n/v | 53.680/48.365 |
| 2560×1440 | High | 100% | Dorf | 13.09 | 14.19 | 76.403 | 70.459 | -4.156, -7.917, -6.340 | -6.340 | 83.763/78.943 | 7.644/7.417 | n/v/n/v | n/v/n/v | 73.525/67.922 |
| 2560×1440 | High | 100% | Wald | 13.09 | 14.45 | 76.388 | 69.214 | -7.317, -7.174, -7.068 | -7.174 | 101.649/76.862 | 7.540/7.251 | n/v/n/v | n/v/n/v | 73.895/66.518 |
| 2560×1440 | High | 100% | Weg | 12.64 | 14.13 | 79.096 | 70.749 | -5.812, -8.347, -6.979 | -6.979 | 85.476/78.205 | 7.718/7.429 | n/v/n/v | n/v/n/v | 76.217/68.785 |

## Finale Paare: Standalone

| Ausgabe | Qualität | SP | Ort | Kontrolle FPS | Kandidat FPS | Kontrolle Frame ms | Kandidat Frame ms | Δ ms je Paar | Median Δ ms | Kontrolle/Kandidat P95 ms | Kontrolle/Kandidat Game ms | Kontrolle/Kandidat Render ms | Kontrolle/Kandidat Render CriticalPath ms | Kontrolle/Kandidat GPU ms |
|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|---|
| 1280×740 | Medium | 75% | Dorf | 60.01 | 59.98 | 16.664 | 16.673 | -0.003, +0.009, +0.002 | +0.002 | 16.998/17.031 | 1.070/1.126 | 16.665/16.666 | 16.665/16.666 | 13.561/15.796 |
| 1280×740 | Medium | 75% | Wald | 60.02 | 59.99 | 16.662 | 16.670 | +0.014, +0.013, -0.006 | +0.013 | 17.007/17.006 | 1.118/1.225 | 16.661/16.668 | 16.661/16.668 | 13.380/15.807 |
| 1280×740 | Medium | 75% | Weg | 60.03 | 60.02 | 16.659 | 16.660 | +0.003, +0.004, -0.019 | +0.003 | 16.979/17.019 | 1.049/1.162 | 16.657/16.665 | 16.657/16.665 | 13.687/15.778 |
| 1280×740 | Medium | 100% | Dorf | 53.82 | 55.98 | 18.581 | 17.864 | -0.702, -0.760, -0.661 | -0.702 | 20.394/19.729 | 1.553/1.634 | 18.556/17.850 | 18.556/17.850 | 17.538/16.917 |
| 1280×740 | Medium | 100% | Wald | 55.25 | 58.85 | 18.099 | 16.992 | -0.850, -0.334, -1.953 | -0.850 | 20.087/18.560 | 1.529/1.506 | 18.087/17.027 | 18.087/17.027 | 17.151/16.145 |
| 1280×740 | Medium | 100% | Weg | 53.24 | 54.43 | 18.783 | 18.371 | -0.412, -0.754, -0.640 | -0.640 | 21.044/20.553 | 1.501/1.612 | 18.788/18.386 | 18.788/18.386 | 17.820/17.263 |
| 2560×1440 | Medium | 75% | Dorf | 29.88 | 30.88 | 33.464 | 32.383 | -1.082, -1.777, -1.262 | -1.262 | 36.131/33.977 | 1.504/1.523 | 33.456/32.378 | 33.456/32.378 | 32.266/31.108 |
| 2560×1440 | Medium | 75% | Wald | 30.28 | 31.81 | 33.024 | 31.441 | -1.434, -1.583, -1.333 | -1.434 | 34.618/33.304 | 1.475/1.547 | 33.050/31.397 | 33.050/31.397 | 31.920/30.263 |
| 2560×1440 | Medium | 75% | Weg | 29.85 | 30.56 | 33.504 | 32.723 | -0.146, -1.480, -1.383 | -1.383 | 35.690/34.407 | 1.527/1.570 | 33.492/33.042 | 33.492/33.042 | 32.149/31.682 |
| 2560×1440 | Medium | 100% | Dorf | 19.86 | 20.78 | 50.365 | 48.134 | -2.230, -1.732, -2.468 | -2.230 | 52.687/50.837 | 1.859/1.844 | 50.349/48.120 | 50.357/48.120 | 49.603/47.255 |
| 2560×1440 | Medium | 100% | Wald | 19.93 | 21.28 | 50.165 | 46.983 | -3.413, -3.886, -3.181 | -3.413 | 55.902/49.232 | 1.799/1.895 | 50.148/47.011 | 50.148/47.011 | 49.455/46.417 |
| 2560×1440 | Medium | 100% | Weg | 19.57 | 20.77 | 51.094 | 48.136 | -3.684, -1.927, -2.292 | -2.292 | 54.327/51.541 | 1.828/1.895 | 51.144/47.986 | 51.144/47.986 | 50.473/47.301 |
| 2560×1440 | High | 75% | Dorf | 22.81 | 25.13 | 43.839 | 39.790 | -3.743, -4.016, -4.165 | -4.016 | 47.560/43.244 | 1.731/1.752 | 43.810/39.801 | 43.810/39.801 | 42.139/38.181 |
| 2560×1440 | High | 75% | Wald | 22.97 | 25.42 | 43.526 | 39.341 | -3.119, -4.415, -4.733 | -4.415 | 47.065/42.798 | 1.809/1.791 | 43.505/39.348 | 43.505/39.348 | 41.754/37.521 |
| 2560×1440 | High | 75% | Weg | 22.41 | 24.29 | 44.624 | 41.162 | -4.603, -4.057, -3.025 | -4.057 | 47.193/44.667 | 1.833/1.809 | 44.596/40.833 | 44.596/40.833 | 42.506/38.964 |
| 2560×1440 | High | 100% | Dorf | 15.17 | 16.40 | 65.919 | 60.958 | -4.784, -4.610, -5.224 | -4.784 | 69.858/65.039 | 1.855/1.875 | 65.960/60.929 | 65.960/60.929 | 63.857/58.684 |
| 2560×1440 | High | 100% | Wald | 15.29 | 16.86 | 65.413 | 59.308 | -5.693, -7.658, -5.958 | -5.958 | 69.900/63.292 | 1.815/1.862 | 65.435/59.337 | 65.435/59.337 | 63.088/57.106 |
| 2560×1440 | High | 100% | Weg | 14.95 | 16.38 | 66.888 | 61.040 | -4.924, -5.848, -5.731 | -5.731 | 71.860/66.196 | 1.836/1.771 | 66.874/61.739 | 66.874/61.739 | 64.890/59.348 |

Standalone Standard/75% zeigt praktisch 60-Hz-Taktung in beiden Zuständen, trotz VSync=0 und t.MaxFPS=0. Dort kein nachgewiesener FPS-Gewinn; GPUTime steigt sogar von etwa 13,4–13,7 auf 15,8 ms. Der größte Zuwachs liegt im nicht zugeordneten GPU-Anteil, während Postprocessing günstiger wird. Ursache (Present-/Pacing-/Taktverhalten oder andere GPU-Arbeit) nicht bewiesen. Kein Beleg für bessere GPU-Effizienz in dieser Konfiguration; vor Baselineübernahme gezielt nachprüfen.

Die Ziele 60 FPS Standard/Medium, 60 FPS QHD/Medium und zunächst mindestens 30 FPS QHD/High bleiben Richtwerte. Dieser Kandidat ist keine ausreichende Gesamtoptimierung für alle Ziele. QHD/100% bleibt deutlich zu langsam. Ein Editor-/Standalone-Unterschied enthält auch Slate-/Prozessbedingungen und wird nicht allein als Optimierungserfolg ausgegeben.

## 7. Visuelle Prüfung und echte Screenshots

14 finale native Gameplay-Screenshots, jeweils echte **2560×1440**, gleiche Kamera/Qualität (High/100%), Position und Beleuchtung. Dorf, Wald, Waldlichtung, Wegübergang, NPC im Waldschatten, Kronenfreistellung, Archiv. Skeletal-Pose für statische A/B-Bilder angehalten und anschließend restauriert. Kontrollierte Fotopositionen sind kein Fußlaufnachweis.

**Dorf / Heilhaus: Kontrolle / Kandidat**

![Kontrolle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/00_Dorf_Control00000.png)

![Kandidat](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/01_Dorf_MapCandidate00000.png)

**Dichter Wald: Kontrolle / Kandidat**

![Kontrolle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/02_Wald_Control00000.png)

![Kandidat](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/03_Wald_MapCandidate00000.png)

**Waldlichtung: Kontrolle / Kandidat**

![Kontrolle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/04_Clearing_Control00000.png)

![Kandidat](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/05_Clearing_MapCandidate00000.png)

**Wegübergänge: Kontrolle / Kandidat**

![Kontrolle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/06_Weg_Control00000.png)

![Kandidat](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/07_Weg_MapCandidate00000.png)

**NPC im Waldschatten: Kontrolle / Kandidat**

![Kontrolle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/08_NPCWald_Control00000.png)

![Kandidat](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/09_NPCWald_MapCandidate00000.png)

**Kronenfreistellung: Kontrolle / Kandidat**

![Kontrolle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/10_Crown_Control00000.png)

![Kandidat](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/11_Crown_MapCandidate00000.png)

**Archiv: Kontrolle / Kandidat**

![Kontrolle](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/12_Archiv_Control00000.png)

![Kandidat](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Screenshots/13_Archiv_MapCandidate00000.png)

Sichtbefund: Dichte Kronen, Baumpositionen, Wege und Gebäudekonturen bleiben erhalten. Keine durch diese Arbeit eingeführte fehlende Vegetation oder neue LOD-Sprünge in geprüften Ansichten. Lumen2 macht feinste indirekte Details etwas weicher, weniger Bloom verändert Leuchtglanz geringfügig. Außenbewegung ohne Motion Blur schärfer. Standbilder beweisen keine vollständige Freiheit von temporalem Schattenrauschen/Ditherflimmern.

Die Figur bleibt im tiefen Waldschatten dunkel. Vereinzelte kantige Hintergrund-/Vegetationsflächen sind bereits in der Kontrolle vorhanden. Diese Art-/Materialgrenzen werden nicht als behoben ausgegeben. Kronenfreistellung im aktiven Lauf sichtbar; Gebäude behalten ihre Darstellung. Der zusätzliche FootTest-Screenshot CrownReveal_Off ist **kein verlässlicher deaktivierter Referenzzustand** wegen laufender Runtime-MID-Anbindung und wird nicht als Material-/Performancebeweis verwendet.

## 8. Gameplay-Fußlauf und Save/Load

**Bestanden:** 263.51 m echte Enhanced-Input-Fortbewegung, 177.43 s Spielzeit / 198.09 s Wall-Clock. Keine Test-Teleports. Nur bestehende normale Heilhaus-Relocation. Maximales gemessenes Tempo 210.000 cm/s.

Route: Start/Menu → Wanderer/Questdialog → Wildabzweigung/Fang → Liora/Trainerkampf → Brücke/offener Weg → Save/Load vor Archiv → Archivabschluss → Rückweg/veränderter Wandererdialog → Dorf/Heilhaus → gerader Eintritt → Heilerin/Heal/PP/Checkpoint/Save → Ausgang → diagonaler Wiederein-/Austritt → dichter Wald/Kronen → alle acht Richtungen → Menü.

Geprüft durch echte Runtime-Aufrufe/Assertions: Dialog-/Battle-Inputlock, Ranger-Idle/Gesprächsblend, NPC-PaperSprite-Fallback ein/aus und restauriert, Trainer besiegt, Trainerzustand nach kontrolliertem Reset und Load restauriert, Party-HP/PP beim Load unverändert, Archivflag im Save, volle HP/PP nach Heilerin, Heilhaus-Checkpoint gespeichert, Innen-/Außenbewegungsbasis und Cutaway korrekt, kein unerwartetes Fallen/Blockieren.

Richtungsbilder und Gesprächsbildsequenzen vorhanden. Kein Controller-Handtest, kein neuer Langzeit-/Multiplayer-Test. Kein kontinuierliches Video.

Der Dev-Slot wurde vorher gesichert. Das Test-Save ist ebenfalls erhalten. Anschließend Original bei passender Test-SHA bytegleich restauriert. SHA-256: 626d58c2f512b3c63f90a18537fd646f611adecb76d52827428a67f578bbd21e. Keine Speichersystemänderung.

Fußlaufbilder unter Art/World/EnvironmentPerfV1/Review/FootTest. UI-Aufnahmen After_*, Direction_* und TalkSequence_* enthalten den 2940×1696-Editorrahmen; Native_* sind 2560×1440-Spielbilder. UI-Ansichten werden nicht als QHD-Performancebeweis benutzt.

## 9. Build, Automation und Map Check

Development Editor Build erfolgreich (Build_FinalProfile.log). Keine Gameplay-C++-Änderung.

Tatsächlicher Umfang: **44 Tests**, 44 erfolgreich, 0 erfolgreich mit Warnungen, 0 fehlgeschlagen, 0 nicht ausgeführt. Neue Abdeckung: PokeMonster.Rendering.EnvironmentProfile.ScopeAndBaselineProtection. Bestehende Gameplaytests vollständig mit ausgeführt. [Strukturierter Report](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV1/Review/Data/AutomationIndex.json).

Map Check: **0 Fehler / 0 Warnungen**, native Logeinträge 15.10.2026 12:47:37 UTC und nach erneutem Öffnen 13:16:54 UTC. Persistenter Komponentenvergleich fehlerfrei. Profile-EndPlay-Restaurierung in echter PIE bestätigt.

Der frische Automationprozess enthält 23 Warning-/Error-Zeilen außerhalb der strukturierten Projektresultate: 17 generische "Condition failed" bei Frame 0 vor Engine-Initialisierung und vor dem ersten PokeMonster-Test, vier idevice_id-Startwarnungen (Bad CPU type), einen MCP-Lizenzhinweis und eine Editorlayout-Migrationswarnung. Die genaue Ursache der 17 Bootstrap-Conditions ist hier nicht weiter aufgelöst; keine Behauptung einer vollständig fehlerfreien Engine-Sitzung. Alle 44 PokeMonster-Tests sind Success, mit 0 zugeordneten Testwarnungen/-fehlern. Keine dieser Meldungen unterdrückt. Runtime-Sitzungen enthalten außerdem die bekannten AudioSampleRate-/MotionVectorSafety-Hinweise.

Vollständige Automation-Warning-/Error-Zeilen:

~~~text
[2026.10.15-13.11.44:860][  0]LogHAL: Warning: FMacPlatformProcess::CreateProc: posix_spawn("/Users/Shared/Epic Games/UE_5.8/Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id") failed (86, Bad CPU type in executable)
[2026.10.15-13.11.44:860][  0]LogHAL: Warning: Failed to launch Tool. (/Users/Shared/Epic Games/UE_5.8/Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id)
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.52:364][  0]LogAutomationTest: Error: Condition failed
[2026.10.15-13.11.53:255][  0]LogModelContextProtocol: Warning: Data transmitted via this plugin to your connected LLM service is Licensed Technology under the UE EULA. You are responsible for ensuring your LLM provider does not use it as training input. See Section 6(e) of the UE EULA for full terms.
[2026.10.15-13.11.54:859][  0]LogHAL: Warning: FMacPlatformProcess::CreateProc: posix_spawn("/Users/Shared/Epic Games/UE_5.8/Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id") failed (86, Bad CPU type in executable)
[2026.10.15-13.11.54:859][  0]LogHAL: Warning: Failed to launch Tool. (/Users/Shared/Epic Games/UE_5.8/Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id)
[2026.10.15-13.11.55:717][  0]LogLayoutService: Warning: While key "UnrealEd_Layout_v1.5" was not found, and older version exists (key "UnrealEd_Layout_v1.6"). This means section "EditorLayouts" was created with a previous version of UE and is no longer compatible. The old key has been removed and updated with the new one.
~~~


Initiale Compile-/API-Anpassungen und MCP-Port-/Editorstartprobleme wurden gelöst; aktueller Build erfolgreich. Kein schwebendes PIE-Fenster verwendet, dessen bekannter Schließabsturz nicht provoziert.

## 10. Empfehlung

**Nicht automatisch in VisualV2 übernehmen.** Separater Kandidat ist funktionsfähig und messbar verbessert, aber keine endgültige Qualitäts-/Leistungsfreigabe. Vor Übernahme: Harry prüft besonders Schattenrauschen in Bewegung und indirekte Details an Gesicht/Vegetation; längere thermisch stabile Messungen, möglichst paketierter Development/Shipping und zusätzliche Licht-/NPC-Schattenfälle.

Nächster technischer Schritt: gezielter Metal-GPU-Capture für den großen noch unaufgeschlüsselten Anteil. Danach Lumen-Integration, Schattenprojektion und Masked-Foliage-Pixelkosten einzeln untersuchen. Kein weiterer pauschaler Polygonabbau: aktuelle ForcedLOD-/Cull-Tests belegen keinen stabilen Nutzen. Vegetationsschatten gruppen-/distanzweise mit Sichtprüfung behandeln, statt Waldschatten komplett zu entfernen. Ergebnisse rechtfertigen keine globale Qualitätsabsenkung.

## 11. Dateien und Nachweise

Bewusst bestehend geändert:

- Docs/TECHNIK.md: angehängter verbindlicher Teststandard.
- Docs/ENTSCHEIDUNGEN.md: bestätigter Teststandard / isolierter Kandidat, keine Baselinefreigabe.
- Source/PokeMonster/PokeMonster.Build.cs: nur private RenderCore-Abhängigkeit.

Vollständige neue Dateiliste dieser Aufgabe:

~~~text
Content/Maps/Dev_TestMap_EnvironmentPerfV1.umap
Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbe.cpp
Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfile.cpp
Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfile.h
Source/PokeMonster/Tests/PokeMonsterEnvironmentRenderProfileTest.cpp
Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V1_PRUEFBERICHT.md
Tools/EnvironmentPerfV1/AfterFoot.py
Tools/EnvironmentPerfV1/AppendDecision.py
Tools/EnvironmentPerfV1/ArchiveEvidence.py
Tools/EnvironmentPerfV1/AuditEditor.py
Tools/EnvironmentPerfV1/AuditVegetation.py
Tools/EnvironmentPerfV1/BeforeFoot.py
Tools/EnvironmentPerfV1/BuildAndLaunch.py
Tools/EnvironmentPerfV1/CloseForBuild.py
Tools/EnvironmentPerfV1/Control.py
Tools/EnvironmentPerfV1/CreateTestMap.py
Tools/EnvironmentPerfV1/FinalEditorCleanup.py
Tools/EnvironmentPerfV1/FinalMapAudit.py
Tools/EnvironmentPerfV1/FootTest.py
Tools/EnvironmentPerfV1/InspectMeshAPI.py
Tools/EnvironmentPerfV1/LoadBaseline.py
Tools/EnvironmentPerfV1/LoadTestMap.py
Tools/EnvironmentPerfV1/MCPClient.py
Tools/EnvironmentPerfV1/PersistCandidate.py
Tools/EnvironmentPerfV1/Plans/BaselinePIE.tsv
Tools/EnvironmentPerfV1/Plans/FactorsDorf.tsv
Tools/EnvironmentPerfV1/Plans/FactorsDorfWeg.tsv
Tools/EnvironmentPerfV1/Plans/FactorsWald.tsv
Tools/EnvironmentPerfV1/Plans/FactorsWeg.tsv
Tools/EnvironmentPerfV1/Plans/FinalPairedPIE.tsv
Tools/EnvironmentPerfV1/Plans/IntegrationAB.tsv
Tools/EnvironmentPerfV1/Plans/QHD_CandidateReview.tsv
Tools/EnvironmentPerfV1/Plans/QHD_FinalComparison.tsv
Tools/EnvironmentPerfV1/Plans/QHD_LumenReview.tsv
Tools/EnvironmentPerfV1/Plans/ResolutionSmoke.tsv
Tools/EnvironmentPerfV1/Plans/StandalonePair1.tsv
Tools/EnvironmentPerfV1/Plans/StandalonePair2.tsv
Tools/EnvironmentPerfV1/Plans/StandalonePair3.tsv
Tools/EnvironmentPerfV1/Plans/StandalonePair4.tsv
Tools/EnvironmentPerfV1/Plans/StandalonePair5.tsv
Tools/EnvironmentPerfV1/Plans/StandalonePair6.tsv
Tools/EnvironmentPerfV1/Plans/VegetationAB.tsv
Tools/EnvironmentPerfV1/PrepareEditor.py
Tools/EnvironmentPerfV1/ProtectionAudit.py
Tools/EnvironmentPerfV1/Queue.py
Tools/EnvironmentPerfV1/README.md
Tools/EnvironmentPerfV1/RefreshFinalEvidence.py
Tools/EnvironmentPerfV1/ReopenFinalEditor.py
Tools/EnvironmentPerfV1/ReportBody.md.in
Tools/EnvironmentPerfV1/RestoreDevSave.py
Tools/EnvironmentPerfV1/ReviewShots.py
Tools/EnvironmentPerfV1/RunAutomation.py
Tools/EnvironmentPerfV1/RunInEditor.py
Tools/EnvironmentPerfV1/RunStandalone.py
Tools/EnvironmentPerfV1/RuntimeMonitor.py
Tools/EnvironmentPerfV1/SceneFactorController.py
Tools/EnvironmentPerfV1/StartFoot.py
Tools/EnvironmentPerfV1/StartProbe.py
Tools/EnvironmentPerfV1/StrictValidation.py
Tools/EnvironmentPerfV1/Summarize.py
Tools/EnvironmentPerfV1/ThermalMonitor.py
Tools/EnvironmentPerfV1/WriteReport.py
Tools/EnvironmentPerfV1/WriteTables.py
Art/World/EnvironmentPerfV1/Review/Data/AutomationExit.json
Art/World/EnvironmentPerfV1/Review/Data/AutomationIndex.json
Art/World/EnvironmentPerfV1/Review/Data/Build_FinalProfile.log
Art/World/EnvironmentPerfV1/Review/Data/DevSaveRestored.json
Art/World/EnvironmentPerfV1/Review/Data/EditorAudit.json
Art/World/EnvironmentPerfV1/Review/Data/FactorPairs.json
Art/World/EnvironmentPerfV1/Review/Data/FinalEditorState.json
Art/World/EnvironmentPerfV1/Review/Data/FinalGitChecks.json
Art/World/EnvironmentPerfV1/Review/Data/FinalMapAudit.json
Art/World/EnvironmentPerfV1/Review/Data/FootProfileActive.json
Art/World/EnvironmentPerfV1/Review/Data/FootSessionAfter.json
Art/World/EnvironmentPerfV1/Review/Data/FootSessionBefore.json
Art/World/EnvironmentPerfV1/Review/Data/MapCheckLog.json
Art/World/EnvironmentPerfV1/Review/Data/MapCheckLog_Reopened.json
Art/World/EnvironmentPerfV1/Review/Data/MeasurementValidation.json
Art/World/EnvironmentPerfV1/Review/Data/Measurements.json
Art/World/EnvironmentPerfV1/Review/Data/MetricTables.md
Art/World/EnvironmentPerfV1/Review/Data/PersistedCandidate.json
Art/World/EnvironmentPerfV1/Review/Data/ProtectionAudit.json
Art/World/EnvironmentPerfV1/Review/Data/RawMeasurements.zip
Art/World/EnvironmentPerfV1/Review/Data/StrictValidation.json
Art/World/EnvironmentPerfV1/Review/Data/Thermal.jsonl
Art/World/EnvironmentPerfV1/Review/Data/VegetationAudit.json
Art/World/EnvironmentPerfV1/Review/Data/WarningsSummary.md
Art/World/EnvironmentPerfV1/Review/EvidenceManifest.json
Art/World/EnvironmentPerfV1/Review/FootTest/After_BachBruecke00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_CrownReveal_Off00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_CrownReveal_On00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_DichterWald00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_Dorf00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_Final00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_Heilhaus00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_Innenraum00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_OffenerWeg00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_Ruinen00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_Wald00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/After_WildBranch00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Direction_000000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Direction_100000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Direction_200000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Direction_300000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Direction_400000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Direction_500000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Direction_600000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Direction_700000.png
Art/World/EnvironmentPerfV1/Review/FootTest/FootProgress.json
Art/World/EnvironmentPerfV1/Review/FootTest/FootTest.json
Art/World/EnvironmentPerfV1/Review/FootTest/Native_BachBruecke00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_CrownReveal_Off00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_CrownReveal_On00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_DichterWald00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_Dorf00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_Final00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_Heilhaus00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_Innenraum00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_OffenerWeg00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_Ruinen00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_Wald00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Native_WildBranch00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/Ranger_Conversation00000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_CompletedDialogue_0000000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_CompletedDialogue_0100000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_CompletedDialogue_0200000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_QuestDialogue_0000000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_QuestDialogue_0100000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_QuestDialogue_0200000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_QuestDialogue_0300000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_QuestDialogue_0400000.png
Art/World/EnvironmentPerfV1/Review/FootTest/TalkSequence_QuestDialogue_0500000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/00_Dorf_Control00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/01_Dorf_MapCandidate00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/02_Wald_Control00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/03_Wald_MapCandidate00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/04_Clearing_Control00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/05_Clearing_MapCandidate00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/06_Weg_Control00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/07_Weg_MapCandidate00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/08_NPCWald_Control00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/09_NPCWald_MapCandidate00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/10_Crown_Control00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/11_Crown_MapCandidate00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/12_Archiv_Control00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/13_Archiv_MapCandidate00000.png
Art/World/EnvironmentPerfV1/Review/Screenshots/Review.json
~~~

Ausführliche Mess-/Prüfnachweise (rund 406 MiB einschließlich unverkleinerter QHD-PNGs und Rohdatenarchiv) unter Art/World/EnvironmentPerfV1/Review. Vollständige rohe Frames, Unreal-CSV-Pässe, Editor-/Native-Logs, weitere diagnostische Screenshotserien und Save-Backups bleiben zusätzlich unter ignoriertem Saved/EnvironmentPerfV1 und Saved/Profiling/CSV/ENV1_* erhalten. Keine Arbeitsartefakte bestehender Aufgaben gelöscht.

## 12. Git-Abschluss

git diff --check: Exit 0; Ausgabe: (keine). Nichts gestaged, kein Commit, kein Push.

Anfangsstatus:

~~~text
 M Content/Maps/Dev_TestMap_VisualV2.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Dialogue/PokeMonsterDialogueSubsystem.h
?? Art/Characters/NPCs/CrouchedCreature/
?? Art/Characters/NPCs/DarkArmored/
?? Art/Characters/NPCs/DwarfWarrior/
?? Art/Characters/NPCs/ElvenArcher/
?? Art/Characters/NPCs/ElvenScholar/
?? Art/Characters/NPCs/Incoming/
?? Art/Characters/NPCs/IntegrationV1/
?? Art/Characters/NPCs/Ranger/
?? Art/Characters/NPCs/SilverLady/
?? Art/Characters/NPCs/TreeBeing/
?? Art/Characters/NPCs/WhiteHairedWarrior/
?? Art/Characters/NPCs/Wizard/
?? Content/Characters/NPCs/
?? Content/Maps/Dev_TestMap_RangerPerfV2.umap
?? Docs/MESHY_NPC_INTEGRATION_V1_PRUEFBERICHT.md
?? Docs/POKEMONSTER_PERFORMANCE_RANGER_V2_PRUEFBERICHT.md
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.h
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.h
?? Source/PokeMonster/Development/
?? Source/PokeMonster/Tests/PokeMonsterNPCPresentationTest.cpp
?? Tools/MeshyNPCIntegrationV1/
?? Tools/PerformanceRangerV2/
~~~

Abschlussstatus (vorhandene offene Arbeiten eingeschlossen):

~~~text
 M Content/Maps/Dev_TestMap_VisualV2.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Dialogue/PokeMonsterDialogueSubsystem.h
 M Source/PokeMonster/PokeMonster.Build.cs
?? Art/Characters/NPCs/CrouchedCreature/
?? Art/Characters/NPCs/DarkArmored/
?? Art/Characters/NPCs/DwarfWarrior/
?? Art/Characters/NPCs/ElvenArcher/
?? Art/Characters/NPCs/ElvenScholar/
?? Art/Characters/NPCs/Incoming/
?? Art/Characters/NPCs/IntegrationV1/
?? Art/Characters/NPCs/Ranger/
?? Art/Characters/NPCs/SilverLady/
?? Art/Characters/NPCs/TreeBeing/
?? Art/Characters/NPCs/WhiteHairedWarrior/
?? Art/Characters/NPCs/Wizard/
?? Art/World/EnvironmentPerfV1/
?? Content/Characters/NPCs/
?? Content/Maps/Dev_TestMap_EnvironmentPerfV1.umap
?? Content/Maps/Dev_TestMap_RangerPerfV2.umap
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V1_PRUEFBERICHT.md
?? Docs/MESHY_NPC_INTEGRATION_V1_PRUEFBERICHT.md
?? Docs/POKEMONSTER_PERFORMANCE_RANGER_V2_PRUEFBERICHT.md
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.h
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.h
?? Source/PokeMonster/Development/
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentRenderProfileTest.cpp
?? Source/PokeMonster/Tests/PokeMonsterNPCPresentationTest.cpp
?? Tools/EnvironmentPerfV1/
?? Tools/MeshyNPCIntegrationV1/
?? Tools/PerformanceRangerV2/
~~~
