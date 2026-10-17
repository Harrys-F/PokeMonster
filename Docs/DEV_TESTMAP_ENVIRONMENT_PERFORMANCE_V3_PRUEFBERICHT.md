# Environment Performance V3 – Prüfbericht

Stand 15.10.2026. **Keine neue Vegetationsoptimierung zur Übernahme in VisualV2 empfohlen.**

## Ergebnis

Die separate Karte `/Game/Maps/Dev_TestMap_EnvironmentPerfV3` ist gespeichert und geprüft. Ein deutlicher, reproduzierbarer neuer QHD-Gewinn gegenüber V2 wurde nicht erreicht. Daher wurden erzwungene Baum-LODs, zusätzliche Culling-Grenzen und vereinfachte Blattmaterialien **nicht dauerhaft übernommen**. V3 erhält den erneut geprüften V2-Renderzustand. Die Messmatrix zeigt diesen Zustand **A** gegen den anschließend verworfenen Mindest-LOD-Versuch **B**; B ist nicht die ausgelieferte V3-Konfiguration.

Die Irradiance-Field-Alternative bleibt schneller als Screen Probe Gather, aber ihre indirekte Helligkeit und Kontaktschatten entsprechen weiterhin nicht vollständig V1. Die getesteten Korrekturen lösen das nicht überzeugend. Empfehlung: V2 vorerst als bisherigen Performance-Versuch behalten, V3 als nachvollziehbare Untersuchungs-/Reviewgrundlage. Keine automatische Übernahme in VisualV2. Kein Commit, kein Push.

## Sicherheit und Editorzustand

HEAD: `351a3ef Add YoungTrainer sprint V1 and in-place run animation`; Branch `main`. Der Arbeitsbaum war bereits umfangreich geändert/unversioniert. 3068 vorhandene, von Git erfasste oder nicht ignorierte Projektdateien vor/nachher SHA-256-geprüft: alle bytegleich. Build-, Saved- und DDC-Artefakte sind davon getrennt. Keine Resets, Löschungen, Restores, Staging oder fremden Änderungen.

Anfangs geöffnet: TreeShadowProxyV1, kein PIE. **0 Dirty-Map- und 0 Dirty-Content-Pakete.** Actor-/Komponententransformationen, Mesh-/Materialzuweisungen, Schattenzustände und Instanzzahlen stimmen nach sicherem erneutem Laden mit der gespeicherten Datei überein. Flüchtige Python-Struct-Adressen wurden beim Vergleich ignoriert. Keine beabsichtigten ungesicherten Pakete zu retten.

Die frühere Sperre war laut V2-Bericht eine Ablehnung der automatischen Aktionsprüfung, kein nachgewiesenes Unreal-Paketproblem. „Verwerfen“ gehört zur **Speicherdruck-KPI-Meldung**: `Engine/Plugins/Experimental/EditorPerformance/Source/EditorPerformance/Private/SEditorPerformanceStatusBar.cpp:275` bindet „Dismiss“ an `ExpireAndFadeout()` und Bestätigung der Meldung, nicht an Paketverwerfen. `EditorPerformanceModule.cpp:317` liefert die Speicherdruckerklärung. Der Button blieb unangetastet. Kein Save All, Discard All oder Force Quit; reguläre Editor-Schließungen nur nach leeren Dirty-Listen.

Quelle der neuen Karte: EnvironmentPerfV2. Erstellung mit `EditorLoadingAndSavingUtils.save_map` an neuem Pfad, danach explizit geladen. Exakte Datei: `Content/Maps/Dev_TestMap_EnvironmentPerfV3.umap`. Keine bestehende Source-Map gespeichert. VisualV2, EnvPerfV1/V2, RangerPerfV2, TreeShadowProxyV1, WestlandRegion, WestlandAssetLibrary und Dev_TestMap unverändert.

## Gespeicherte V3

Die kopierten V1/V2-Profilactoren sind aufgrund exakter Levelnamen-Guards in V3 inaktiv. Ein neuer kollisionsloser Actor ohne Tick stellt ausschließlich in V3 dieselben vier V2-Werte her und setzt sie bei EndPlay zurück:

| Variable | Wert |
|---|---:|
| r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor | 2 |
| r.Shadow.Virtual.SMRT.RayCountDirectional | 2 |
| r.Lumen.FinalGatherMethod | 0 |
| r.Lumen.HardwareRayTracing | 0 |

Keine globale INI-Änderung. Exterior-Bloom/MotionBlur, Geometrie und Beleuchtung wie in V2. FinalMapAudit vergleicht mit dem gespeicherten V2-World-Asset: ein neuer Profilactor; keine fehlenden Actoren oder Unterschiede bestehender Transformationen, Meshes, Materialien, Collision, LOD-/Instanzdaten, Lichtintensitäten und Postprocess-Einstellungen. Keine Vegetationsverschiebung oder Dichteänderung. Die separaten Schattenproxy-Versuche wurden nicht übernommen.

## Vegetations- und Materialinventar

Gezählte Platzierungen, nicht behauptete pro Frame sichtbare Instanzen/Draw Calls:

| Mesh | Instanzen | Komponenten | Dreiecke LOD0 / 1 / 2 |
|---|---:|---:|---|
| SM_WLA_OakAncient_V3 | 41 | 41 | 12068 / 7240 / 3621 |
| SM_WLA_WildBush_V3_B | 47 | 20 | 3396 / 2038 / 1019 |
| SM_WLA_WildBush_V3_A | 55 | 26 | 3284 / 1971 / 986 |
| SM_WLA_Birch_A | 4 | 4 | 28628 / 17177 / 8588 |
| SM_WLA_Grass_A | 175 | 1 | 576 |
| SM_WLA_Fern_A | 46 | 1 | 8030 / 4818 / 2409 |
| SM_WLA_Herb_A | 55 | 1 | 1152 / 634 / 288 |

V3-Eichen/Büsche verwenden Masked-Blattflächen mit Atlas und zweiseitigen Blättern; Birken erhalten zur Laufzeit die bestehenden Reveal-Materialien. Unterwuchs weitgehend instanziert, Reveal-Bäume mit eigenen Komponenten. Keine Materialduplikate oder zusätzlichen Slots. Bestehende LODs, Culling und Schattenwurf geprüft; kleine Vegetation wirft bereits größtenteils keine Schatten.

RuntimeMaterialAudit enthält die tatsächlichen Materialfamilien, Masken-/Zweiseitigkeitswerte, Texturauflösungen und verfügbare kompilierte Statistiken. Diese Abfrage erfolgte nach dem Timing, da sie Shaderkompilierung abschließen kann. Null-/nicht unterstützte Instruktionswerte sind kein Beweis kostenloser Shader. Sampler-/Instruktionsangaben sind keine gemessenen Passzeiten. In den geprüften Baum-/Buschmaterialien kein WPO; tatsächlich animierter Wind ist deshalb nicht abgenommen.

Keine verlässlichen quantitativen Overdraw-/Draw-Call-Zähler verfügbar. Nullwerte aus RHI-/Draw-Zählern gelten als n/v. Masken-/Blattüberlagerung visuell und strukturell untersucht. Der Materials-Showflag betrifft die gesamte Szene und isoliert nicht Blattshader. Ohne belegten CPU-/Draw-Engpass keine Instancing-Neuentwicklung.

## Messstandard und Grenzen

UE 5.8.2, Apple M4, macOS 27.0.1, vorhandener 16-GB-Mac. Native Standalone: Development `UnrealEditor -game`, **kein Shipping-Build**; Editor dabei geschlossen. PIE ausschließlich eingebettet. Keine schwebenden PIE-Fenster.

| Ort | Playerposition cm |
|---|---|
| Dorf | −4100 / 450 / 50,15 |
| Wald | −4300 / 1550 / 50,15 |
| Weg | −36,6 / −47,1 / 50,15 |

Außenkamera 2850 cm / Pitch −50° / Yaw −45° / FOV 35°. Gleiche unbewegte Messpunkte und Idle-Zustände, keine NPC-Gameplaywechsel. Animationen laufen im Timing weiter; exakter Animationsphasentimestamp nicht fixiert. Nur für Bilder temporär pausiert.

Je Modus sechs Konfigurationen: 1280×740 Medium 75/100 %, 2560×1440 Medium 75/100 %, 2560×1440 High 75/100 %. Je Ort/Zustand drei Durchläufe, benachbarte AB/BA/AB-Paare, Ortsreihenfolge im zweiten Durchlauf umgekehrt. Fünf Sekunden Warm-up, sechs Sekunden Messung. Qualität vor PIE gesetzt; kein High→Medium-Wechsel im laufenden PIE. Eine native Prozessinstanz je Konfiguration. Screenshot-/Statistikzeiten ausgeschlossen.

**216 Hauptsegmente**, alle Wiederholungen, Kamera, aktives Fenster, Viewport/RenderTarget/Renderer-ViewRect und CSV-Dateien vollständig validiert. Vor nativem Beenden fünf Sekunden Ausschreibzeit, dadurch keine fehlenden Abschluss-CSV-Dateien wie in V2.

Interne Auflösung aus tatsächlichen Renderer-ResolutionFractions nach UE-Ceil-Regel: 960×555, 1280×740, 1920×1080 oder 2560×1440; keine direkte GPU-Allocation-Rücklesung. Rohe Slate-Fenstergröße samt DPI zusätzlich gespeichert, nicht als Spielauflösung ausgegeben. Historische 2331×1346-Werte und alte Energiezustände sind kein Vergleichsmaßstab.

r.VSync/r.VSyncEditor 0, t.MaxFPS 0, Dynamic Resolution aus, Engine-Framerate-Glättung/Fixframerate aus, GameUser-Limit 0. **rhi.SyncInterval bleibt 1**; Metal-Fensterpräsentation kann nahe 60 FPS deckeln. Dort keine Reserve aus identischen FPS ableiten. Native RenderThread-Zeit enthält Wartezeit, PIE-RenderThread hier n/v. GPU-Stufen können verschachtelt sein, nicht aufsummieren. Unaccounted nicht willkürlich einem Shader zuschreiben.

Tabellen: Median der drei Laufmediane; FPS = 1000 / Median-Bildzeit. P95 = Median der drei Lauf-P95. Δms sind drei gepaarte Differenzen, nicht zwingend die Differenz separat gebildeter Mediane. JSON enthält alle Einzelmediane, FPS-Spannen, Auflösungen und GPU-Stufen.

Thermik: 498 Abfragen; Zustände {'fair': 470, 'nominal': 28}. Energiezustände: ["Now drawing from 'AC Power'\n -InternalBattery-0 (id=23068771)\t100%; charged; 0:00 remaining present: true"]. NSProcessInfo ist keine Grad-/Taktmessung; konkretes Throttling wird daraus nicht behauptet. Zeitnahe A/B-Paare reduzieren Drift, schließen Hintergrundlast/Temperaturdrift nicht vollständig aus.

## Vollständiger Vorher-/Nachher-Versuch

A = V2-Renderzustand auf identischer V3-Kopie, entspricht dem gespeicherten V3-Zustand. B = ausschließlich Baum-Mindest-LOD 1, **verworfen**. Keine neue FPS-Verbesserung des ausgelieferten Zustands behauptet.

| Modus | Ausgabe / Qualität / SP | Ort | FPS A → B | Median ms A → B | P95 ms A → B | GPU ms A → B | Game ms A → B | Render ms A → B | Δms B−A, drei Paare |
|---|---|---|---|---|---|---|---|---|---|
| Standalone | 1280×740 / Medium / 75 % | Dorf | 60.03 → 60.01 | 16.66 → 16.66 | 17.13 → 17.15 | 16.34 → 16.36 | 1.35 → 1.41 | 16.67 → 16.66 | +0.00, +0.01, -0.00 |
| Standalone | 1280×740 / Medium / 75 % | Wald | 59.99 → 60.00 | 16.67 → 16.67 | 17.18 → 17.20 | 16.33 → 16.35 | 1.40 → 1.43 | 16.65 → 16.66 | -0.02, -0.00, +0.02 |
| Standalone | 1280×740 / Medium / 75 % | Weg | 59.96 → 60.02 | 16.68 → 16.66 | 17.15 → 17.13 | 16.37 → 16.36 | 1.45 → 1.43 | 16.66 → 16.65 | +0.01, -0.04, -0.02 |
| Standalone | 1280×740 / Medium / 100 % | Dorf | 60.02 → 60.01 | 16.66 → 16.66 | 17.18 → 17.35 | 16.30 → 16.28 | 1.37 → 1.34 | 16.66 → 16.65 | +0.00, -0.01, -0.03 |
| Standalone | 1280×740 / Medium / 100 % | Wald | 59.99 → 60.01 | 16.67 → 16.66 | 17.15 → 17.10 | 16.36 → 16.30 | 1.32 → 1.35 | 16.66 → 16.66 | -0.02, -0.04, -0.01 |
| Standalone | 1280×740 / Medium / 100 % | Weg | 60.01 → 60.05 | 16.66 → 16.65 | 17.44 → 17.04 | 16.37 → 16.36 | 1.46 → 1.27 | 16.66 → 16.65 | -0.02, -0.08, +0.03 |
| Standalone | 2560×1440 / Medium / 75 % | Dorf | 35.00 → 35.42 | 28.57 → 28.24 | 29.90 → 29.56 | 28.12 → 27.98 | 1.33 → 1.31 | 28.56 → 28.23 | -0.03, -0.34, -0.03 |
| Standalone | 2560×1440 / Medium / 75 % | Wald | 36.02 → 36.53 | 27.76 → 27.37 | 29.12 → 28.35 | 27.35 → 27.02 | 1.34 → 1.30 | 27.75 → 27.39 | -0.03, -0.93, -0.39 |
| Standalone | 2560×1440 / Medium / 75 % | Weg | 35.57 → 35.49 | 28.11 → 28.18 | 29.00 → 28.81 | 27.83 → 27.85 | 1.27 → 1.24 | 28.12 → 28.17 | -0.17, +0.08, -0.13 |
| Standalone | 2560×1440 / Medium / 100 % | Dorf | 23.51 → 23.44 | 42.54 → 42.67 | 43.58 → 44.10 | 42.02 → 42.32 | 1.62 → 1.61 | 42.54 → 42.64 | -0.30, +0.41, +0.23 |
| Standalone | 2560×1440 / Medium / 100 % | Wald | 23.73 → 24.02 | 42.15 → 41.63 | 43.93 → 43.39 | 41.66 → 41.13 | 1.66 → 1.75 | 42.06 → 41.62 | -0.51, -0.73, +0.20 |
| Standalone | 2560×1440 / Medium / 100 % | Weg | 22.98 → 23.30 | 43.51 → 42.93 | 47.12 → 44.16 | 43.08 → 42.64 | 1.60 → 1.53 | 43.51 → 42.94 | -0.58, -0.11, -0.21 |
| Standalone | 2560×1440 / High / 75 % | Dorf | 31.00 → 30.57 | 32.26 → 32.71 | 33.86 → 35.14 | 31.66 → 32.06 | 1.53 → 1.55 | 32.26 → 32.73 | +1.21, +0.45, -0.04 |
| Standalone | 2560×1440 / High / 75 % | Wald | 31.25 → 31.91 | 32.00 → 31.34 | 33.28 → 32.60 | 31.32 → 30.69 | 1.39 → 1.40 | 31.97 → 31.33 | +0.08, -0.45, -0.77 |
| Standalone | 2560×1440 / High / 75 % | Weg | 30.30 → 30.64 | 33.01 → 32.64 | 34.32 → 33.97 | 32.41 → 32.04 | 1.40 → 1.35 | 33.00 → 32.65 | -0.37, +0.11, -1.04 |
| Standalone | 2560×1440 / High / 100 % | Dorf | 20.77 → 20.57 | 48.14 → 48.61 | 50.15 → 51.00 | 47.63 → 48.12 | 1.87 → 1.83 | 48.20 → 48.58 | -1.03, -0.39, +0.46 |
| Standalone | 2560×1440 / High / 100 % | Wald | 21.37 → 21.25 | 46.80 → 47.05 | 50.07 → 52.31 | 46.32 → 46.45 | 1.84 → 1.82 | 46.77 → 47.05 | +0.88, +0.34, -0.24 |
| Standalone | 2560×1440 / High / 100 % | Weg | 20.78 → 20.63 | 48.13 → 48.47 | 49.80 → 49.83 | 47.72 → 47.90 | 1.77 → 1.73 | 48.11 → 48.45 | +0.30, +0.35, -0.15 |
| PIE | 1280×740 / Medium / 75 % | Dorf | 44.12 → 44.14 | 22.67 → 22.65 | 24.49 → 25.77 | 19.57 → 19.31 | 7.22 → 8.49 | n/v → n/v | -0.14, -0.11, +1.03 |
| PIE | 1280×740 / Medium / 75 % | Wald | 45.19 → 44.85 | 22.13 → 22.30 | 23.89 → 24.28 | 18.71 → 18.78 | 7.46 → 7.51 | n/v → n/v | -0.14, +0.30, -0.04 |
| PIE | 1280×740 / Medium / 75 % | Weg | 43.56 → 43.89 | 22.96 → 22.79 | 25.03 → 24.87 | 19.48 → 19.53 | 7.16 → 7.19 | n/v → n/v | -0.36, +0.08, +0.07 |
| PIE | 1280×740 / Medium / 100 % | Dorf | 37.37 → 37.54 | 26.76 → 26.64 | 30.36 → 30.12 | 23.86 → 23.75 | 6.83 → 6.86 | n/v → n/v | +0.70, -0.22, -0.18 |
| PIE | 1280×740 / Medium / 100 % | Wald | 38.31 → 37.87 | 26.10 → 26.41 | 29.62 → 30.14 | 23.00 → 23.06 | 6.96 → 7.45 | n/v → n/v | +0.87, +0.37, -1.26 |
| PIE | 1280×740 / Medium / 100 % | Weg | 37.28 → 37.40 | 26.83 → 26.73 | 30.69 → 30.21 | 23.82 → 23.78 | 6.84 → 6.65 | n/v → n/v | +0.04, -0.21, -0.09 |
| PIE | 2560×1440 / Medium / 75 % | Dorf | 24.41 → 24.72 | 40.97 → 40.45 | 46.07 → 44.95 | 38.52 → 37.93 | 6.38 → 6.33 | n/v → n/v | -1.27, +0.40, -1.51 |
| PIE | 2560×1440 / Medium / 75 % | Wald | 25.01 → 25.12 | 39.98 → 39.81 | 43.93 → 44.24 | 37.22 → 36.98 | 6.61 → 6.66 | n/v → n/v | +2.37, -1.10, -0.17 |
| PIE | 2560×1440 / Medium / 75 % | Weg | 24.49 → 25.23 | 40.83 → 39.64 | 45.22 → 44.29 | 38.19 → 37.01 | 6.37 → 6.29 | n/v → n/v | +0.83, -1.80, -1.19 |
| PIE | 2560×1440 / Medium / 100 % | Dorf | 18.26 → 18.03 | 54.78 → 55.45 | 60.56 → 62.71 | 52.02 → 52.63 | 7.17 → 7.28 | n/v → n/v | +0.58, +0.24, +0.74 |
| PIE | 2560×1440 / Medium / 100 % | Wald | 18.40 → 18.83 | 54.34 → 53.11 | 63.07 → 60.51 | 51.34 → 50.69 | 7.66 → 7.69 | n/v → n/v | -0.64, -1.42, -5.03 |
| PIE | 2560×1440 / Medium / 100 % | Weg | 18.23 → 17.98 | 54.85 → 55.63 | 62.69 → 63.96 | 51.88 → 52.75 | 7.34 → 7.18 | n/v → n/v | -3.56, +0.73, +5.32 |
| PIE | 2560×1440 / High / 75 % | Dorf | 22.47 → 22.75 | 44.51 → 43.95 | 49.34 → 49.17 | 41.41 → 41.29 | 6.41 → 6.45 | n/v → n/v | -0.56, +0.05, -0.74 |
| PIE | 2560×1440 / High / 75 % | Wald | 22.44 → 23.36 | 44.57 → 42.80 | 50.65 → 48.07 | 41.66 → 40.38 | 6.81 → 6.91 | n/v → n/v | -0.51, -0.31, -2.28 |
| PIE | 2560×1440 / High / 75 % | Weg | 22.46 → 22.36 | 44.53 → 44.73 | 50.06 → 51.28 | 41.62 → 42.31 | 6.50 → 6.52 | n/v → n/v | -0.78, +2.22, -0.13 |
| PIE | 2560×1440 / High / 100 % | Dorf | 16.57 → 16.34 | 60.33 → 61.21 | 68.83 → 69.74 | 57.84 → 58.49 | 7.43 → 7.37 | n/v → n/v | -0.35, -0.51, +3.76 |
| PIE | 2560×1440 / High / 100 % | Wald | 16.31 → 16.14 | 61.32 → 61.95 | 67.60 → 70.07 | 58.59 → 58.29 | 7.82 → 7.78 | n/v → n/v | -3.05, +1.46, +1.21 |
| PIE | 2560×1440 / High / 100 % | Weg | 16.07 → 16.49 | 62.24 → 60.65 | 71.80 → 68.56 | 59.30 → 57.95 | 7.55 → 7.54 | n/v → n/v | -5.66, -1.59, +2.29 |

### GPU-Stufen am QHD-High-100-Waldpunkt

Mediane der drei Wiederholungen; verschachtelte Stufen nicht aufsummieren. RenderThread im Standalone enthält Wartezeit.

| Modus | Stufe | A ms | B ms (verworfen) |
|---|---|---:|---:|
| Standalone | GPU/Unaccounted | 17.445 | 17.533 |
| Standalone | GPU/ShadowProjection | 4.915 | 4.949 |
| Standalone | GPU/LumenIrradianceFieldGather | 4.584 | 4.560 |
| Standalone | GPU/Basepass | 3.063 | 3.002 |
| Standalone | GPU/ShadowDepths | 2.435 | 2.435 |
| Standalone | GPU/LumenSceneLighting | 1.599 | 1.609 |
| Standalone | GPU/Postprocessing | 0.893 | 0.899 |
| PIE | GPU/Unaccounted | 2.238 | 2.243 |
| PIE | GPU/ShadowProjection | 4.704 | 4.702 |
| PIE | GPU/LumenIrradianceFieldGather | 4.415 | 4.505 |
| PIE | GPU/Basepass | 3.041 | 2.981 |
| PIE | GPU/ShadowDepths | 2.414 | 2.454 |
| PIE | GPU/LumenSceneLighting | 0.792 | 0.791 |
| PIE | GPU/PostProcessing | 19.281 | 18.929 |
| PIE | GPU/SlateUI | 3.845 | 3.859 |

## Isolierte Faktoren

Discovery: Wald, PIE QHD High 100 %, sieben Sekunden Warm-up/sieben Sekunden Messung. Negative Δms ist schneller.

| Faktor | Drei Δms B−A | Median Δms |
|---|---|---:|
| VegetationHidden | +5.370, -2.186, +1.383 | +1.383 |
| VegetationNoShadow | +1.450, -0.655, -0.313 | -0.313 |
| TreeLOD1 | -2.343, -1.390, +1.029 | -1.390 |
| BushLOD1 | -0.460, +3.357, +0.524 | +0.524 |
| FernLOD1 | -1.380, +0.720, +1.412 | +0.720 |
| CV:ShowFlag.Materials=0 | -3.373, -2.831, -1.597 | -2.831 |
| CV:r.Lumen.IrradianceFieldGather.InterpolateDownsampleFactor=4 | -0.455, +2.012, +1.697 | +1.697 |
| CV:r.Lumen.IrradianceFieldGather.AdaptivePlacement=1 | +0.312, +0.232, -1.414 | +0.232 |
| CV:r.Lumen.IrradianceFieldGather.ShortRangeAORadius=48 | +0.325, +1.953, +1.578 | +1.578 |
| CV:r.Lumen.IrradianceFieldGather.ProbeOcclusionBias=0.5 | +0.340, +0.505, -1.294 | +0.340 |

Native Nachprüfung QHD High 100 %, fünf Sekunden Warm-up/sechs Sekunden Messung:

- Wald / SmallFoliageCull: +0.334, +0.117, -0.313 ms; Median +0.117 ms.
- Dorf / CV:r.Lumen.FinalGatherMethod=1: +3.985, +4.847, +4.514 ms; Median +4.514 ms.
- Wald / CV:r.Lumen.FinalGatherMethod=1: +5.847, +4.373, +4.601 ms; Median +4.601 ms.

**Belegt:** Screen Probe Gather statt V2-Irradiance Field kostet hier rund 4,5–4,6 ms zusätzlich, Hardware-RT-Schalter dabei identisch. GPU-/Präsentationszeit erheblich größer als Game Thread. Schattenprojektion, indirekte Beleuchtung und Base Pass sind messbare Stufen. Der große Unaccounted-Anteil bleibt ungeklärt; keine Behauptung, alles sei Vegetation.

**Nicht belegt:** Robuste Gesamteinsparung durch Vegetation verstecken, Schatten abschalten, Busch-/Farn-LODs oder zusätzliche Culling-Grenzen. Verstecken verändert auch GI/Occlusion und sichtbare Bodenflächen; keine reine Vegetationszeit. Baum-LOD 1 zeigt kleine lokale Vorteile, aber keinen konsistenten Gewinn, insbesondere nicht im nativen QHD High 100. Deshalb kein dauerhafter Qualitätswechsel. Keine großflächige Vegetationsentfernung akzeptiert.

## Beleuchtung und Sichtprüfung

Adaptive Probe-Platzierung, OcclusionBias 0,5, AO-Radius 48 und InterpolateDownsampleFactor 4 einzeln geprüft und in echten QHD-Bildern verglichen. Keine überzeugende Wiederherstellung der V1-Kontaktschatten ohne Nachteile. Größerer AO-Radius kostet Zeit; gröbere Interpolation kein zuverlässiger Gewinn. Keine Übernahme, globale Abdunklung oder zusätzliche Lichter als Kompensation.

Kronen, Boden/Wege, NPC-Lesbarkeit, Gebäude/Heilhaus und Player-Reveal betrachtet. V3 wahrt V2-Materialien, Licht und Geometrie. Abweichende indirekte Schattierung zu V1 bleibt ein bekannter V2-Kompromiss. Mindest-LOD kann feine Stamm-/Ast-/Blattkonturen vereinfachen; ohne überzeugenden Gewinn verworfen. Gespeicherte V3 hat keine neuen LOD-Schwellen/Culling-Übergänge. Keine pauschale Freigabe vorhandener Masked-/LOD-Kanten als flimmerfrei.

## Echte Bildvergleiche

Actual saved Source-Maps VisualV2, EnvironmentPerfV1, V2 und V3 separat ohne Source-Map-Save aufgenommen, High/QHD100 und gleiche Spielkamera. Keine generierten Konzeptbilder. Beschriftete Layouts sind ausschließlich Zusammenstellungen echter Aufnahmen. Review-Metadaten halten Map, Bedingung, Position, Kamera und Viewport fest. Originalbilder 2560×1440 im Reviewordner, weitere Versuchsbilder unter Saved.

- [FootTest_Interior_V1_QHD00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Interior_V1_QHD00000.png) — Quelle `Saved/EnvironmentPerfV3/FootTest/Interior_V1_QHD00000.png`.
- [FootTest_Interior_V3_QHD00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Interior_V3_QHD00000.png) — Quelle `Saved/EnvironmentPerfV3/FootTest/Interior_V3_QHD00000.png`.
- [FootTest_Native_CrownReveal_On00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Native_CrownReveal_On00000.png) — Quelle `Saved/EnvironmentPerfV3/FootTest/Native_CrownReveal_On00000.png`.
- [FootTest_Native_DichterWald00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Native_DichterWald00000.png) — Quelle `Saved/EnvironmentPerfV3/FootTest/Native_DichterWald00000.png`.
- [FootTest_Native_Dorf00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Native_Dorf00000.png) — Quelle `Saved/EnvironmentPerfV3/FootTest/Native_Dorf00000.png`.
- [FootTest_Native_Heilhaus00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Native_Heilhaus00000.png) — Quelle `Saved/EnvironmentPerfV3/FootTest/Native_Heilhaus00000.png`.
- [Baseline_EnvironmentPerfV1_QHD_00_Dorf_EnvironmentPerfV100000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV1_QHD_00_Dorf_EnvironmentPerfV100000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV1_QHD/00_Dorf_EnvironmentPerfV100000.png`.
- [Baseline_EnvironmentPerfV1_QHD_01_Wald_EnvironmentPerfV100000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV1_QHD_01_Wald_EnvironmentPerfV100000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV1_QHD/01_Wald_EnvironmentPerfV100000.png`.
- [Baseline_EnvironmentPerfV1_QHD_02_Weg_EnvironmentPerfV100000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV1_QHD_02_Weg_EnvironmentPerfV100000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV1_QHD/02_Weg_EnvironmentPerfV100000.png`.
- [Baseline_EnvironmentPerfV2_QHD_00_Dorf_EnvironmentPerfV200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV2_QHD_00_Dorf_EnvironmentPerfV200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV2_QHD/00_Dorf_EnvironmentPerfV200000.png`.
- [Baseline_EnvironmentPerfV2_QHD_01_Wald_EnvironmentPerfV200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV2_QHD_01_Wald_EnvironmentPerfV200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV2_QHD/01_Wald_EnvironmentPerfV200000.png`.
- [Baseline_EnvironmentPerfV2_QHD_02_Weg_EnvironmentPerfV200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV2_QHD_02_Weg_EnvironmentPerfV200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV2_QHD/02_Weg_EnvironmentPerfV200000.png`.
- [Baseline_EnvironmentPerfV3_QHD_00_Dorf_EnvironmentPerfV300000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_00_Dorf_EnvironmentPerfV300000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV3_QHD/00_Dorf_EnvironmentPerfV300000.png`.
- [Baseline_EnvironmentPerfV3_QHD_01_Wald_EnvironmentPerfV300000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_01_Wald_EnvironmentPerfV300000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV3_QHD/01_Wald_EnvironmentPerfV300000.png`.
- [Baseline_EnvironmentPerfV3_QHD_02_Weg_EnvironmentPerfV300000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_02_Weg_EnvironmentPerfV300000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV3_QHD/02_Weg_EnvironmentPerfV300000.png`.
- [Baseline_EnvironmentPerfV3_QHD_03_NPCWald_EnvironmentPerfV300000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_03_NPCWald_EnvironmentPerfV300000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV3_QHD/03_NPCWald_EnvironmentPerfV300000.png`.
- [Baseline_EnvironmentPerfV3_QHD_04_Crown_EnvironmentPerfV300000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_04_Crown_EnvironmentPerfV300000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_EnvironmentPerfV3_QHD/04_Crown_EnvironmentPerfV300000.png`.
- [Baseline_VisualV2_QHD_00_Dorf_VisualV200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_VisualV2_QHD_00_Dorf_VisualV200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_VisualV2_QHD/00_Dorf_VisualV200000.png`.
- [Baseline_VisualV2_QHD_01_Wald_VisualV200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_VisualV2_QHD_01_Wald_VisualV200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_VisualV2_QHD/01_Wald_VisualV200000.png`.
- [Baseline_VisualV2_QHD_02_Weg_VisualV200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_VisualV2_QHD_02_Weg_VisualV200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/Baseline_VisualV2_QHD/02_Weg_VisualV200000.png`.
- [CandidatesQHD_00_Dorf_V200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_00_Dorf_V200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/00_Dorf_V200000.png`.
- [CandidatesQHD_02_Dorf_TreeLOD100000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_02_Dorf_TreeLOD100000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/02_Dorf_TreeLOD100000.png`.
- [CandidatesQHD_03_Dorf_AO4800000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_03_Dorf_AO4800000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/03_Dorf_AO4800000.png`.
- [CandidatesQHD_04_Dorf_Bias0500000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_04_Dorf_Bias0500000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/04_Dorf_Bias0500000.png`.
- [CandidatesQHD_05_Dorf_Adaptive00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_05_Dorf_Adaptive00000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/05_Dorf_Adaptive00000.png`.
- [CandidatesQHD_07_Wald_V200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_07_Wald_V200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/07_Wald_V200000.png`.
- [CandidatesQHD_09_Wald_TreeLOD100000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_09_Wald_TreeLOD100000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/09_Wald_TreeLOD100000.png`.
- [CandidatesQHD_10_Wald_AO4800000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_10_Wald_AO4800000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/10_Wald_AO4800000.png`.
- [CandidatesQHD_11_Wald_Bias0500000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_11_Wald_Bias0500000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/11_Wald_Bias0500000.png`.
- [CandidatesQHD_12_Wald_Adaptive00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_12_Wald_Adaptive00000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/12_Wald_Adaptive00000.png`.
- [CandidatesQHD_14_NPCWald_V200000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_14_NPCWald_V200000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/14_NPCWald_V200000.png`.
- [CandidatesQHD_16_NPCWald_TreeLOD100000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_16_NPCWald_TreeLOD100000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/16_NPCWald_TreeLOD100000.png`.
- [CandidatesQHD_17_NPCWald_AO4800000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_17_NPCWald_AO4800000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/17_NPCWald_AO4800000.png`.
- [CandidatesQHD_18_NPCWald_Bias0500000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_18_NPCWald_Bias0500000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/18_NPCWald_Bias0500000.png`.
- [CandidatesQHD_19_NPCWald_Adaptive00000.png](../Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_19_NPCWald_Adaptive00000.png) — Quelle `Saved/EnvironmentPerfV3/Screenshots/CandidatesQHD/19_NPCWald_Adaptive00000.png`.

## Funktion, Build und Tests

- Development Editor Build erfolgreich, `Build_Initial.log` und `Build_MinLOD.log`. Nur neue isolierte Entwicklungs-/Profilingdateien und ein Isolationstest; bestehende C++-/Gameplay-Dateien unverändert.
- Projekt-Automation **46/46 erfolgreich**, 0 fehlgeschlagen, 0 nicht ausgeführt. Aktuell 46 einschließlich neuem V3-Test. Bekannte generische Engine-Startup-„Condition failed“-Meldungen vor der Testsitzung sowie `idevice_id`-macOS-Warnungen getrennt davon; kein komplett warnungsfreier Engine-Startup behauptet. Testdetails im Automation-JSON.
- Finaler Map Check: **0 Fehler / 0 Warnungen**; Lognachweis in MapCheck.json.
- Eingebetteter PIE-Fußlauf **263.10 m**, ohne Test-Teleports, bestanden. EnhancedInput-Bewegung, bestehende Interaktions-/Battle-Presenter-APIs für Aktionen; kein behaupteter manueller Hardware-/Maus-UI-Test.
- Route: Wanderer/Dialog → Wildkampf/Fangen → Liora → Brücke/Weg → Archiv mit Save/Load → Abschlussdialog → Heilhaus/Innenraum/Heilerin/Heal/Checkpoint → diagonal hinaus/hinein → dichter Wald/Player-Reveal → acht Richtungen/Menü. Tatsächliche Einzelbestätigungen in FootProgress.json und FootTest.json.
- Save/Load im selben PIE mit kontrolliert zurückgesetztem Trainerstatus, HP/PP erhalten; kein Save/Load-Prozessneustart. Ursprünglicher Dev-Spielstand SHA-geprüft bytegleich wiederhergestellt, eigener Teststand separat nur unter Saved erhalten.
- Ranger-Idle/Talk, Blickwendung/Dialogbindung und NPC-Sprite-Fallback im Fußtest geprüft. Keine Spieler-/Sprint-/Animationsdatei verändert, keine neue Eingabearchitektur; Hardware-Controller nicht erneut geprüft.
- Kamera, 140-cm-Spielermaßstab, 210 cm/s, Sprint, Collision und Gameplay erhalten. Keine neuen Kollisionen oder verschobenen Interaktionspunkte. Heilhaus-Relocation ist bestehende Funktion, kein Test-Teleport. Reveal mit 0,25 s unverändert; keine neue Gebäudeausblendung.

## Offene Grenzen / Empfehlung

1. Keine deutliche neue QHD-Verbesserung. 60 FPS QHD Medium bzw. durchgehend 30 FPS QHD High nicht erreicht; nahe 60 FPS teilweise Präsentationsdeckel. Keine FPS-Garantie.
2. Nicht zugeordneten Metal-/Präsentationsanteil mit gezielter nativer GPU-Capture untersuchen, bevor weitere Assets umgebaut werden. Keine reine Shader-/Bandbreitenursache aus diesen Zählern bewiesen.
3. Irradiance Field bleibt Qualitätskompromiss. Konsistente indirekte Beleuchtung/Kontaktschatten nicht in diesem Pass gelöst.
4. Enger zugeschnittene Blattkarten könnten theoretisch Overdraw reduzieren; erst separater Pilot mit Qualitäts- und Performancenachweis. Keine unbewiesene globale Material-/Geometrieänderung.
5. Drei kurze Läufe erlauben keinen Signifikanznachweis kleinster Sub-ms-Gewinne. Thermik-/Hintergrunddrift, fehlende verlässliche Draw-/Overdraw-Zähler, kein animierter Wind, kein Shipping-/Controller-Test bleiben ausdrücklich offen.
6. V3 nicht automatisch in VisualV2 übernehmen. Referenzkarten und Originalassets erhalten; keine reine Qualitätsreduktion als Erfolg verkaufen.

### Zusätzliche GPU-Capture und technische Restgrenzen

Nach Abschluss von Matrix und Fußlauf wurde eine separate, nicht als FPS-Messung verwendete PIE-GPU-Capture bei verifiziertem QHD High 100 % aufgenommen (`GPUCaptureProof.json`, `GPUCapture.txt`). Einzelframe 53,04 ms; unter anderem BasePass 2,792 ms, IrradianceFieldGather 7,353 ms und ShadowProjectionOnOpaque 4,935 ms. Der Marker „VSM Log Stats And Status“ trägt 15,841 ms. Das ist **kein ausreichender Nachweis**, dass eingeschaltete sichtbare Statistiken oder dieser einzelne Shader allein die Ursache sind. Draw-/Dispatch-Zähler dieser Ausgabe stehen durchgehend auf null; Warte-/Barrieren-/Synchronisationsanteile sind damit nicht sauber abgegrenzt. Die wiederholten CSV-/A/B-Daten bleiben die primäre Leistungsbewertung. Dieser große Anteil bleibt für eine gezielte Metal-Capture offen; kein Engine-Shader oder globales Schattenverfahren wurde auf Verdacht geändert.

Die Ablaufsteuerung hielt beim frühen Editorstart sicher an, solange das Konsolenfeld noch fehlte; der neue Helper wartet nun auf die tatsächliche Slate-Oberfläche. Im neuen Szenenaudit wurde eine übernommene V2-Klassenreferenz korrigiert, ebenso im neuen Fußtest für den V3-Profilactor. Danach Szenenaudit und Fußlauf vollständig erfolgreich. Diese Prüfskriptkorrekturen betrafen keine bestehenden Spiel-/Assetdateien. `FinalEditorState.json` bestätigt V3 geöffnet, kein PIE, keine Dirty-Pakete, ursprüngliche Editor-/Capturewerte und Dev-Spielstand wiederhergestellt; die temporäre Automationsqueue wurde entfernt.

### Direkte Vergleichslayouts

Die folgenden Layouts enthalten unveränderte echte QHD-Bilder nebeneinander; keine generierten Szenenpixel:

- [Wald: V2 / verworfener LOD-Test](../Art/World/EnvironmentPerfV3/Review/Comparisons/Wald_V2_vs_LOD1_verworfen_QHD.png)
- [Dorf: V1 / V3 mit erhaltenem V2-Renderer](../Art/World/EnvironmentPerfV3/Review/Comparisons/Dorf_V1_vs_V3_QHD.png)
- [Wald: V2 / finaler V3-Endstand](../Art/World/EnvironmentPerfV3/Review/Comparisons/Wald_V2_vs_final_V3_QHD.png)
- [Stamm-/Laubdetail in Originalpixeln](../Art/World/EnvironmentPerfV3/Review/Comparisons/Wald_Contour_Detail_Originalpixels.png)

## Dateien und Git

Neu: V3-Karte, vier V3-C++-/Testdateien, Tools/EnvironmentPerfV3, Art/World/EnvironmentPerfV3/Review und dieser Bericht. Art-Dateien sind Mess-/Bildbelege, keine neuen Original-Blender-/Vegetationsassets. README erläutert Befehle, Guards und die konservative Endkonfiguration.

Keine bestehende versionierbare Datei inhaltlich verändert; fremde offene Arbeiten bleiben offen. Abschließender `git diff --check`-Nachweis in GitDiffCheck.json und Abschlussmeldung. Kein Commit, kein Push.

### Neue Dateien dieses Auftrags

- `Art/World/EnvironmentPerfV3/Review/Automation.json`
- `Art/World/EnvironmentPerfV3/Review/AutomationExit.json`
- `Art/World/EnvironmentPerfV3/Review/Comparisons.json`
- `Art/World/EnvironmentPerfV3/Review/Comparisons/Dorf_V1_vs_V3_QHD.png`
- `Art/World/EnvironmentPerfV3/Review/Comparisons/Wald_Contour_Detail_Originalpixels.png`
- `Art/World/EnvironmentPerfV3/Review/Comparisons/Wald_V2_vs_LOD1_verworfen_QHD.png`
- `Art/World/EnvironmentPerfV3/Review/Comparisons/Wald_V2_vs_final_V3_QHD.png`
- `Art/World/EnvironmentPerfV3/Review/DevSaveRestored.json`
- `Art/World/EnvironmentPerfV3/Review/DiscoveryPairs.json`
- `Art/World/EnvironmentPerfV3/Review/EditorDiskComparison.json`
- `Art/World/EnvironmentPerfV3/Review/EvidenceManifest.json`
- `Art/World/EnvironmentPerfV3/Review/FinalEditorState.json`
- `Art/World/EnvironmentPerfV3/Review/FinalMapAudit.json`
- `Art/World/EnvironmentPerfV3/Review/FootProfileActive.json`
- `Art/World/EnvironmentPerfV3/Review/FootProgress.json`
- `Art/World/EnvironmentPerfV3/Review/FootSessionAfter.json`
- `Art/World/EnvironmentPerfV3/Review/FootTest.json`
- `Art/World/EnvironmentPerfV3/Review/GPUCapture.txt`
- `Art/World/EnvironmentPerfV3/Review/GPUCaptureProof.json`
- `Art/World/EnvironmentPerfV3/Review/GitDiffCheck.json`
- `Art/World/EnvironmentPerfV3/Review/InitialHEAD.txt`
- `Art/World/EnvironmentPerfV3/Review/InitialStatus.txt`
- `Art/World/EnvironmentPerfV3/Review/MapCheck.json`
- `Art/World/EnvironmentPerfV3/Review/MapCopy.json`
- `Art/World/EnvironmentPerfV3/Review/MatrixValidation.json`
- `Art/World/EnvironmentPerfV3/Review/Measurements.json`
- `Art/World/EnvironmentPerfV3/Review/MetricTables.md`
- `Art/World/EnvironmentPerfV3/Review/NewFiles.json`
- `Art/World/EnvironmentPerfV3/Review/PairedMetrics.json`
- `Art/World/EnvironmentPerfV3/Review/PersistedState.json`
- `Art/World/EnvironmentPerfV3/Review/ProtectedFinal.json`
- `Art/World/EnvironmentPerfV3/Review/RawMeasurements.zip`
- `Art/World/EnvironmentPerfV3/Review/RuntimeMaterialAudit.json`
- `Art/World/EnvironmentPerfV3/Review/Screenshots.json`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV1_QHD_00_Dorf_EnvironmentPerfV100000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV1_QHD_01_Wald_EnvironmentPerfV100000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV1_QHD_02_Weg_EnvironmentPerfV100000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV2_QHD_00_Dorf_EnvironmentPerfV200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV2_QHD_01_Wald_EnvironmentPerfV200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV2_QHD_02_Weg_EnvironmentPerfV200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_00_Dorf_EnvironmentPerfV300000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_01_Wald_EnvironmentPerfV300000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_02_Weg_EnvironmentPerfV300000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_03_NPCWald_EnvironmentPerfV300000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_EnvironmentPerfV3_QHD_04_Crown_EnvironmentPerfV300000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_VisualV2_QHD_00_Dorf_VisualV200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_VisualV2_QHD_01_Wald_VisualV200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/Baseline_VisualV2_QHD_02_Weg_VisualV200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_00_Dorf_V200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_02_Dorf_TreeLOD100000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_03_Dorf_AO4800000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_04_Dorf_Bias0500000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_05_Dorf_Adaptive00000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_07_Wald_V200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_09_Wald_TreeLOD100000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_10_Wald_AO4800000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_11_Wald_Bias0500000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_12_Wald_Adaptive00000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_14_NPCWald_V200000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_16_NPCWald_TreeLOD100000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_17_NPCWald_AO4800000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_18_NPCWald_Bias0500000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/CandidatesQHD_19_NPCWald_Adaptive00000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Interior_V1_QHD00000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Interior_V3_QHD00000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Native_CrownReveal_On00000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Native_DichterWald00000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Native_Dorf00000.png`
- `Art/World/EnvironmentPerfV3/Review/Screenshots/FootTest_Native_Heilhaus00000.png`
- `Art/World/EnvironmentPerfV3/Review/VegetationLightingAudit.json`
- `Content/Maps/Dev_TestMap_EnvironmentPerfV3.umap`
- `Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V3_PRUEFBERICHT.md`
- `Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV3.cpp`
- `Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfileV3.cpp`
- `Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfileV3.h`
- `Source/PokeMonster/Tests/PokeMonsterEnvironmentProfileV3Test.cpp`
- `Tools/EnvironmentPerfV3/AfterFoot.py`
- `Tools/EnvironmentPerfV3/AnalyzeDiscovery.py`
- `Tools/EnvironmentPerfV3/AuditInitial.py`
- `Tools/EnvironmentPerfV3/AuditRuntimeMaterials.py`
- `Tools/EnvironmentPerfV3/AuditVegetation.py`
- `Tools/EnvironmentPerfV3/BeforeFoot.py`
- `Tools/EnvironmentPerfV3/CloseForBuild.py`
- `Tools/EnvironmentPerfV3/CompareAndCopy.py`
- `Tools/EnvironmentPerfV3/ComposeComparisons.py`
- `Tools/EnvironmentPerfV3/ContinueMatrix.py`
- `Tools/EnvironmentPerfV3/Control.py`
- `Tools/EnvironmentPerfV3/FinalEditorState.py`
- `Tools/EnvironmentPerfV3/FinalMapAudit.py`
- `Tools/EnvironmentPerfV3/FinishReviewAndFoot.py`
- `Tools/EnvironmentPerfV3/FootTest.py`
- `Tools/EnvironmentPerfV3/GPUCapture.py`
- `Tools/EnvironmentPerfV3/GPUCapturePrepare.py`
- `Tools/EnvironmentPerfV3/LoadReviewMap.py`
- `Tools/EnvironmentPerfV3/MCPClient.py`
- `Tools/EnvironmentPerfV3/MetricTables.py`
- `Tools/EnvironmentPerfV3/PackageEvidence.py`
- `Tools/EnvironmentPerfV3/PersistControl.py`
- `Tools/EnvironmentPerfV3/Plans/Baseline_EnvironmentPerfV1_QHD.tsv`
- `Tools/EnvironmentPerfV3/Plans/Baseline_EnvironmentPerfV2_QHD.tsv`
- `Tools/EnvironmentPerfV3/Plans/Baseline_EnvironmentPerfV3_QHD.tsv`
- `Tools/EnvironmentPerfV3/Plans/Baseline_VisualV2_QHD.tsv`
- `Tools/EnvironmentPerfV3/Plans/CandidatesQHD.tsv`
- `Tools/EnvironmentPerfV3/Plans/DiscoveryQHD.tsv`
- `Tools/EnvironmentPerfV3/Plans/NativeCulling.tsv`
- `Tools/EnvironmentPerfV3/Plans/NativeMatrix1.tsv`
- `Tools/EnvironmentPerfV3/Plans/NativeMatrix2.tsv`
- `Tools/EnvironmentPerfV3/Plans/NativeMatrix3.tsv`
- `Tools/EnvironmentPerfV3/Plans/NativeMatrix4.tsv`
- `Tools/EnvironmentPerfV3/Plans/NativeMatrix5.tsv`
- `Tools/EnvironmentPerfV3/Plans/NativeMatrix6.tsv`
- `Tools/EnvironmentPerfV3/Plans/PIEMatrix1.tsv`
- `Tools/EnvironmentPerfV3/Plans/PIEMatrix2.tsv`
- `Tools/EnvironmentPerfV3/Plans/PIEMatrix3.tsv`
- `Tools/EnvironmentPerfV3/Plans/PIEMatrix4.tsv`
- `Tools/EnvironmentPerfV3/Plans/PIEMatrix5.tsv`
- `Tools/EnvironmentPerfV3/Plans/PIEMatrix6.tsv`
- `Tools/EnvironmentPerfV3/PrepareEditor.py`
- `Tools/EnvironmentPerfV3/PresetBeforePIE.py`
- `Tools/EnvironmentPerfV3/ProtectFinal.py`
- `Tools/EnvironmentPerfV3/Queue.py`
- `Tools/EnvironmentPerfV3/README.md`
- `Tools/EnvironmentPerfV3/ReopenEditor.py`
- `Tools/EnvironmentPerfV3/RestoreDevSave.py`
- `Tools/EnvironmentPerfV3/ReviewShots.py`
- `Tools/EnvironmentPerfV3/RunAutomation.py`
- `Tools/EnvironmentPerfV3/RunBaselineReviews.py`
- `Tools/EnvironmentPerfV3/RunCandidateReview.py`
- `Tools/EnvironmentPerfV3/RunFootOnly.py`
- `Tools/EnvironmentPerfV3/RunInEditor.py`
- `Tools/EnvironmentPerfV3/RunPIEPlans.py`
- `Tools/EnvironmentPerfV3/RunReview.py`
- `Tools/EnvironmentPerfV3/RunStandalone.py`
- `Tools/EnvironmentPerfV3/SetupFootViewport.py`
- `Tools/EnvironmentPerfV3/ShutdownQueue.py`
- `Tools/EnvironmentPerfV3/StartProbe.py`
- `Tools/EnvironmentPerfV3/Summarize.py`
- `Tools/EnvironmentPerfV3/ThermalMonitor.py`
- `Tools/EnvironmentPerfV3/ValidateMeasurements.py`
- `Tools/EnvironmentPerfV3/WriteReport.py`

### git status --short

```text
 M Content/Maps/Dev_TestMap_VisualV2.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Dialogue/PokeMonsterDialogueSubsystem.h
 M Source/PokeMonster/PokeMonster.Build.cs
?? Art/Characters/MiniHobbit/
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
?? Art/World/EnvironmentPerfV2/
?? Art/World/EnvironmentPerfV3/
?? Art/World/TreeShadowProxyV1/
?? Content/Characters/NPCs/
?? Content/Environment/TreeShadowProxyV1/
?? Content/Maps/Dev_TestMap_EnvironmentPerfV1.umap
?? Content/Maps/Dev_TestMap_EnvironmentPerfV2.umap
?? Content/Maps/Dev_TestMap_EnvironmentPerfV3.umap
?? Content/Maps/Dev_TestMap_RangerPerfV2.umap
?? Content/Maps/Dev_TestMap_TreeShadowProxyV1.umap
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V1_PRUEFBERICHT.md
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V2_PRUEFBERICHT.md
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V3_PRUEFBERICHT.md
?? Docs/MESHY_NPC_INTEGRATION_V1_PRUEFBERICHT.md
?? Docs/POKEMONSTER_PERFORMANCE_RANGER_V2_PRUEFBERICHT.md
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.h
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.h
?? Source/PokeMonster/Development/
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentProfileV2Test.cpp
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentProfileV3Test.cpp
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentRenderProfileTest.cpp
?? Source/PokeMonster/Tests/PokeMonsterNPCPresentationTest.cpp
?? Tools/EnvironmentPerfV1/
?? Tools/EnvironmentPerfV2/
?? Tools/EnvironmentPerfV3/
?? Tools/MeshyNPCIntegrationV1/
?? Tools/PerformanceRangerV2/
?? Tools/TreeShadowProxyV1/
```
