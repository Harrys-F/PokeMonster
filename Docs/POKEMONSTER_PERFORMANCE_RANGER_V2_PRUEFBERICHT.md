# PokeMonster – Performance & Ranger Quality V2

Stand: 15.10.2026. **Keine Freigabeempfehlung für eine automatische Übernahme in Dev_TestMap_VisualV2.** Der neue Ranger ist ein funktionsfähiger, sichtbar geprüfter Optimierungskandidat. Die Welt wird dadurch nicht wesentlich schneller. Vor dauerhafter Übernahme sollten die automatische LOD-Grenze und die stark schwankenden Standalone-Bedingungen gezielt nachgeprüft werden. Tests ersetzen diese visuelle/zeitliche Abnahme nicht.

## 1. Ausgangszustand und Projektschutz

HEAD: `351a3ef Add YoungTrainer sprint V1 and in-place run animation`. Der Arbeitsbaum war **bereits geändert**, nicht sauber. Insbesondere VisualV2, TECHNIK, ENTSCHEIDUNGEN, der Dialogue-Header und die komplette uncommittete NPC-Integration waren vorhandene Arbeiten. Sie wurden nicht als eigene Änderungen ausgegeben und nicht zurückgesetzt.

```text
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
?? Docs/MESHY_NPC_INTEGRATION_V1_PRUEFBERICHT.md
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.h
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.h
?? Source/PokeMonster/Tests/PokeMonsterNPCPresentationTest.cpp
?? Tools/MeshyNPCIntegrationV1/
```

Abschließender SHA-256-Vergleich: **2328 anfangs erfasste versionierte/unversionierte Projektdateien unverändert**, keine fehlenden Dateien. Darunter alle zehn Incoming-Originale, ursprüngliche Blenderquellen, Ranger V1, Spieler/Animationen, Originalmaps und bestehende Dokumentation. Ignorierte Build-/Log-/Cachedateien sind von dieser Aussage ausgenommen. Der Dev-Spielstand wurde nach den Tests bytegleich wiederhergestellt. [Hash-Nachweis](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/ProtectedAfter.json).

Originalbaseline: `/Game/Maps/Dev_TestMap_VisualV2`. Experiment ausschließlich in **`/Game/Maps/Dev_TestMap_RangerPerfV2`** (`Content/Maps/Dev_TestMap_RangerPerfV2.umap`). Kopie über Editor-API, anschließend explizit die neue Welt geladen und nur diese gespeichert. `save_map` schreibt eine Kopie, benennt die aktuelle Welt aber nicht um; ein deshalb abgewiesener zweiter Speicherversuch wurde korrigiert. Die Originaldatei wurde nicht gespeichert.

Keine Veränderung an Gameplay, Kamera, Playermaßstab, Geschwindigkeit, Input, Playeranimationen, Weltgeometrie, Vegetationspositionen, Dialogdefinitionen oder Speicherlogik. Kein Commit, kein Push, nichts gestaged.

## 2. Tatsächliche Messauflösungen

- **A:** tatsächlicher SceneViewport und dessen Render-Target **1280 × 740**, Medium, 75 % Screen Percentage, VSync 0, `t.MaxFPS=0`, Dynamic Resolution 0.
- **B:** tatsächlicher SceneViewport/Render-Target **2331 × 1346**, sonst identische Vorgaben. Das sind **3,31-mal** so viele Ausgabepixel wie A. Die alten 23–27 FPS werden ausdrücklich nicht als 1280×740 ausgegeben.
- **C:** eigener nativer Development-Prozess mit `-game -windowed -ResX=1280 -ResY=740 -ForceRes -NoVSync -NoSound`. Tatsächlicher SceneViewport/Render-Target ebenfalls **1280 × 740**. **Kein paketierter Shipping-Build.** Unreal CSV meldet Metal SM6 / Apple M4 / MacEditor-DeviceProfile.

Die tatsächliche Ausgabegröße, Render-Target-Größe, Screen Percentage und Kamerapose wurden **pro Frame** erfasst. Alle **218 gültigen Segmente** bestanden die Größen-/75-%-Prüfung. Die 75 % beschreiben die konfigurierte 3D-Skalierung; Ausgabepixel und intern ausgerichtete Renderpass-Texturgrößen sind nicht gleichzusetzen. Keine Behauptung einer separat gemessenen internen SceneColor-Ausrichtung.

Das eingebettete PIE ließ sich mit `r.SetRes` allein nicht verlässlich auf die geforderte Größe bringen. Deshalb wurde ein ausdrücklich gestarteter nativer Development-Prüfbefehl ergänzt, der `FSceneViewport::SetFixedViewportSize` verwendet. Kein autonomer Gameplay-Tick. Editor-Overrides wurden scoped auf PIE-Override 0 / Secondary Percentage 100 gesetzt und abschließend auf die ursprünglichen Werte 1 / 0 zurückgestellt. Keine Projekt-Renderkonfiguration gespeichert.

[1280×740-Bildnachweis](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/ResolutionSmoke_ResolutionProof00000.png); [Validierungsdaten](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/MeasurementValidation.json).

## 3. Messmethode und Grenzen

Pro Standort drei Wiederholungen; Baseline/Finalvergleich **8 s Warm-up + 10 s Messfenster**. Reihenfolge der Standorte gewechselt. Finale V1/V2-Paare zeitlich verschachtelt; zweite Wiederholung mit umgekehrter V1/V2-Reihenfolge. NPC ohne Gespräch in bestehendem Idle, gleiche Quellidentität/Position/Ausrichtung. Die Einzelposen einer laufenden Idle-Animation sind nicht framegenau phasengleich; jedes Fenster umfasst mehrere Zyklen. Für die Standbilder wurde dagegen dieselbe Idle-Position 0,25 s eingefroren.

| Rohdatenname | Spielerposition cm | Bedeutung |
|---|---|---|
| Dorf | −760 / −1410 / 50,15 | NPC-Vorplatz am Beginn des ursprünglichen Mini-Slices; **kein Gebäudestandort** |
| Wald | −746,5 / −718 / 50,15 | Wald-/Trainerweg |
| Weg | −36,6 / −47,1 / 50,15 | Offener Weg |
| DorfBauten | −4100 / 450 / 50,15 | Heilhaus/Vorplatz; zusätzlich aufgenommen, um echte Gebäude abzudecken |

Kamera unverändert **2850 cm / Pitch −50° / Yaw −45° / FOV 35°**. Automatische Heilhaus-Innenkamera im Fußtest unverändert. Profilierungspositionen wurden gezielt gesetzt und sind **kein behaupteter Fußlauf**. Der spätere komplette Fußtest war eine frische PIE-Sitzung mit Enhanced-Input-Bewegung.

Native Framezeiten aus monotoner Echtzeit. FPS = 1000 / Median-Frametime; P95 mit linearer Quantilinterpolation. Tabellenmediane über drei Messläufe, kein verstecktes Wegmitteln langsamer Läufe. Unreal CSV/GPU-Zähler ergänzen die nativen Framezeiten. Game/Render/GPU überlappen; ihre Zeiten nicht summieren. RenderThreadTime im Standalone enthält Wartezeit und ist keine reine CPU-Rechenzeit.

**Zeitdrift vorhanden:** 922 macOS-Thermal-State-Abfragen meldeten durchgehend „nominal“. Das ist weder ein Temperaturmesswert in °C noch ein Beweis konstanter GPU-Taktrate. Kalte/heiße Blöcke unterscheiden sich deutlich. Daher sind die direkt gepaarten Kontrollen aussagekräftiger als Stunden auseinanderliegende V1-/V2-Blöcke. Keine gemessene Takt-/Temperaturursache behauptet.

Standalone schwankte besonders stark (z. B. finaler NPC-Vorplatz 60,35 → 20,52 → 21,79 FPS). Diese Ergebnisse sind real, aber **kein stabiler Standalone-Nachweis einer Optimierung**. Auflösung und 75 % blieben laut Frameprotokoll gleich. Die Ursache der starken Drift wurde nicht eindeutig isoliert; keine nachträgliche Qualitätsänderung vorgenommen.

Pläne: `Tools/PerformanceRangerV2/Plans/`. Frame-Rohdaten: `Saved/PerformanceRangerV2/*_Frames.csv`; Unreal-Zähler: `Saved/Profiling/CSV/RV2_*.csv`. [Auswertung je Messlauf](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/Measurements.json). Roh-CSV-Header am Dateiende berücksichtigt, weil Unreal Zähler dynamisch ergänzt.

## 4. FPS, Framezeiten und isolierte A/B-Tests

**Wichtig:** `AfterA`, `AfterB`, `PairedA`, `PairedB` sowie `Unreal/` und `UnrealFinal/` beziehen sich auf einen später verworfenen Custom-LOD-Import. Sie bleiben als Fehlernachweise erhalten, sind aber **kein Optimierungserfolg**. Gültige V2-Reihen sind `FinalPairedA/B`, `FinalAfterC` und `VillageA/B/C`. V1-Baselines und reine V1-Faktortests bleiben gültig, da vor jedem Plan ausdrücklich V1 als Kontrollmesh gesetzt wurde.

## Gültige Baselines und finale Messungen

A: 1280 × 740; B: 2331 × 1346; C: Standalone 1280 × 740. Medium / 75 %, VSync aus / uncapped. „Dorf“ in den Rohdaten bezeichnet den NPC-Vorplatz; die eigentliche Gebäudemessung heißt „DorfBauten“.

| Reihe | Standort | Mesh | FPS der 3 Läufe | Median FPS | Median ms | Median der 3 P95 ms | Game ms | Render ms | GPU ms |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| BeforeA | Dorf | V1 | 36.38, 42.31, 41.44 | 41.44 | 24.132 | 26.550 | 6.469 | 0.000 | 21.370 |
| BeforeA | Wald | V1 | 40.59, 41.73, 41.65 | 41.65 | 24.009 | 26.438 | 6.594 | 0.000 | 21.256 |
| BeforeA | Weg | V1 | 41.48, 42.27, 42.15 | 42.15 | 23.722 | 26.581 | 6.511 | 0.000 | 20.849 |
| FinalPairedA | Dorf | V1 | 38.75, 40.01, 39.87 | 39.87 | 25.079 | 27.147 | 6.833 | 0.000 | 21.793 |
| FinalPairedA | Dorf | V2 | 39.55, 40.25, 40.00 | 40.00 | 25.003 | 26.709 | 6.835 | 0.000 | 21.641 |
| FinalPairedA | Wald | V1 | 39.80, 40.05, 39.35 | 39.80 | 25.123 | 27.023 | 6.641 | 0.000 | 21.805 |
| FinalPairedA | Wald | V2 | 40.46, 40.24, 39.91 | 40.24 | 24.850 | 26.545 | 6.617 | 0.000 | 21.483 |
| FinalPairedA | Weg | V1 | 41.49, 41.33, 40.47 | 41.33 | 24.195 | 26.441 | 6.707 | 0.000 | 20.831 |
| FinalPairedA | Weg | V2 | 42.01, 41.49, 40.97 | 41.49 | 24.103 | 26.486 | 6.572 | 0.000 | 20.600 |
| BeforeB | Dorf | V1 | 26.42, 26.63, 25.56 | 26.42 | 37.848 | 43.261 | 6.317 | 0.000 | 35.145 |
| BeforeB | Wald | V1 | 26.23, 26.45, 25.52 | 26.23 | 38.125 | 42.690 | 6.159 | 0.000 | 35.570 |
| BeforeB | Weg | V1 | 27.45, 27.47, 25.55 | 27.45 | 36.424 | 41.066 | 6.375 | 0.000 | 33.609 |
| FinalPairedB | Dorf | V1 | 24.64, 22.53, 23.42 | 23.42 | 42.703 | 45.751 | 6.690 | 0.000 | 39.211 |
| FinalPairedB | Dorf | V2 | 24.86, 22.69, 23.82 | 23.82 | 41.979 | 47.114 | 6.646 | 0.000 | 38.979 |
| FinalPairedB | Wald | V1 | 24.55, 22.08, 22.36 | 22.36 | 44.728 | 48.221 | 6.649 | 0.000 | 40.921 |
| FinalPairedB | Wald | V2 | 24.48, 22.56, 22.82 | 22.82 | 43.817 | 46.301 | 6.689 | 0.000 | 40.247 |
| FinalPairedB | Weg | V1 | 25.10, 23.11, 24.13 | 24.13 | 41.439 | 44.213 | 6.521 | 0.000 | 37.859 |
| FinalPairedB | Weg | V2 | 24.89, 24.16, 24.31 | 24.31 | 41.129 | 46.271 | 6.562 | 0.000 | 37.551 |
| BeforeC | Dorf | V1 | 31.45, 33.10, 33.98 | 33.10 | 30.213 | 43.285 | 1.321 | 30.226 | 29.690 |
| BeforeC | Wald | V1 | 31.95, 31.42, 31.89 | 31.89 | 31.354 | 45.603 | 1.306 | 31.373 | 30.241 |
| BeforeC | Weg | V1 | 35.15, 33.25, 32.67 | 33.25 | 30.074 | 39.872 | 1.289 | 29.260 | 28.983 |
| FinalAfterC | Dorf | V2 | 60.35, 20.52, 21.79 | 21.79 | 45.889 | 51.146 | 1.593 | 45.841 | 44.619 |
| FinalAfterC | Wald | V2 | 58.69, 28.90, 22.33 | 28.90 | 34.607 | 44.874 | 1.583 | 34.621 | 33.081 |
| FinalAfterC | Weg | V2 | 57.05, 33.62, 23.96 | 33.62 | 29.741 | 34.846 | 1.570 | 23.625 | 22.994 |
| VillageA | DorfBauten | V1 | 40.20, 39.50, 41.06 | 40.20 | 24.876 | 26.895 | 7.112 | 0.000 | 20.855 |
| VillageA | DorfBauten | V2 | 40.03, 38.61, 41.69 | 40.03 | 24.981 | 27.186 | 7.321 | 0.000 | 20.995 |
| VillageB | DorfBauten | V1 | 25.25, 25.19, 24.95 | 25.19 | 39.693 | 42.512 | 6.417 | 0.000 | 36.585 |
| VillageB | DorfBauten | V2 | 25.26, 25.18, 23.74 | 25.18 | 39.708 | 42.683 | 6.418 | 0.000 | 36.551 |
| VillageC | DorfBauten | V1 | 23.46, 30.06, 32.27 | 30.06 | 33.267 | 46.104 | 1.331 | 33.270 | 31.991 |
| VillageC | DorfBauten | V2 | 29.72, 30.72, 36.17 | 30.72 | 32.549 | 48.214 | 1.285 | 33.102 | 32.092 |

**RenderThreadTime = 0 im PIE ist kein belastbarer Nullkosten-Nachweis; dort nicht interpretieren.** P95 je einzelner Messung steht im Rohdatenaudit `Measurements.json`. Frühere AfterA/AfterB/PairedA/PairedB beziehen sich auf einen verworfenen Import und sind von dieser Auswertung ausgeschlossen.

## Finale zeitlich verschachtelte Paare

Negative Differenz = V2 schneller. Drei Paare sind eine begrenzte Stichprobe, keine Signifikanzgarantie.

| Reihe | Standort | V1 ms | V2 ms | Δ V2−V1 je Paar, ms | Median Δ ms |
|---|---|---:|---:|---|---:|
| FinalPairedA | Dorf | 25.079 | 25.003 | -0.521, -0.146, -0.076 | -0.146 |
| FinalPairedA | Wald | 25.123 | 24.850 | -0.406, -0.118, -0.352 | -0.352 |
| FinalPairedA | Weg | 24.195 | 24.103 | -0.296, -0.091, -0.297 | -0.296 |
| FinalPairedB | Dorf | 42.703 | 41.979 | -0.360, -0.322, -0.724 | -0.360 |
| FinalPairedB | Wald | 44.728 | 43.817 | +0.113, -0.968, -0.911 | -0.911 |
| FinalPairedB | Weg | 41.439 | 41.129 | +0.343, -1.875, -0.310 | -0.310 |
| VillageA | DorfBauten | 24.876 | 24.981 | +0.105, +0.584, -0.367 | +0.105 |
| VillageB | DorfBauten | 39.693 | 39.708 | -0.015, +0.015, +2.046 | +0.015 |
| VillageC | DorfBauten | 33.267 | 32.549 | -8.973, -0.717, -3.340 | -3.340 |

## Einzelfaktoren – V1, jeweils scoped zurückgesetzt

| Standort | Faktor | Kontroll-ms | Varianten-ms | Median Δ ms | Δ der zwei Paare | GPU Δ ms |
|---|---|---:|---:|---:|---|---:|
| Dorf | RangerHidden | 27.873 | 27.320 | -0.553 | -0.356, -0.749 | -0.460 |
| Dorf | RangerNoShadow | 27.692 | 27.282 | -0.410 | -0.753, -0.068 | -0.035 |
| Dorf | RangerNoAnimation | 27.284 | 27.471 | +0.186 | +0.387, -0.014 | -0.004 |
| Dorf | VegetationHidden | 27.333 | 25.336 | -1.996 | -1.692, -2.301 | -2.132 |
| Dorf | VegetationNoShadow | 27.255 | 26.971 | -0.283 | -0.435, -0.131 | -0.178 |
| Dorf | LocalLightsOff | 27.216 | 28.695 | +1.479 | +2.607, +0.351 | +0.578 |
| Dorf | AllDynamicShadowsOff | 27.388 | 24.160 | -3.227 | -3.183, -3.272 | -2.654 |
| Dorf | PostProcessingOff | 27.297 | 23.021 | -4.276 | -4.565, -3.987 | -3.763 |
| Dorf | RangerFlatMaterial | 27.170 | 27.066 | -0.103 | +0.092, -0.299 | +0.092 |
| Wald | RangerHidden | 28.633 | 27.797 | -0.836 | -1.361, -0.311 | -0.573 |
| Wald | RangerNoShadow | 28.502 | 28.151 | -0.351 | -0.946, +0.244 | -0.234 |
| Wald | RangerNoAnimation | 28.583 | 28.380 | -0.203 | -0.150, -0.256 | -0.179 |
| Wald | VegetationHidden | 28.265 | 25.775 | -2.490 | -2.650, -2.330 | -2.351 |
| Wald | VegetationNoShadow | 28.137 | 27.833 | -0.304 | -0.129, -0.480 | -0.312 |
| Wald | LocalLightsOff | 27.938 | 27.886 | -0.052 | +0.245, -0.350 | +0.149 |
| Wald | AllDynamicShadowsOff | 27.622 | 24.869 | -2.753 | -3.251, -2.255 | -2.539 |
| Wald | PostProcessingOff | 27.585 | 23.802 | -3.784 | -3.497, -4.070 | -3.739 |
| Wald | RangerFlatMaterial | 27.745 | 27.855 | +0.110 | +0.728, -0.508 | +0.168 |
| Weg | RangerHidden | 27.253 | 27.461 | +0.208 | -0.439, +0.855 | +0.033 |
| Weg | RangerNoShadow | 27.396 | 27.028 | -0.368 | +0.250, -0.986 | -0.092 |
| Weg | RangerNoAnimation | 27.390 | 27.171 | -0.220 | +0.059, -0.498 | +0.023 |
| Weg | VegetationHidden | 27.602 | 25.652 | -1.950 | -2.456, -1.444 | -2.053 |
| Weg | VegetationNoShadow | 26.985 | 26.935 | -0.050 | -0.228, +0.127 | -0.074 |
| Weg | LocalLightsOff | 26.980 | 27.064 | +0.084 | -0.393, +0.561 | +0.055 |
| Weg | AllDynamicShadowsOff | 27.545 | 24.415 | -3.130 | -3.183, -3.076 | -2.418 |
| Weg | PostProcessingOff | 27.124 | 23.479 | -3.644 | -3.315, -3.974 | -3.467 |
| Weg | RangerFlatMaterial | 27.526 | 27.187 | -0.339 | -1.443, +0.766 | +0.049 |
| DorfBauten | VegetationHidden | 25.074 | 25.103 | +0.029 | -0.018, +0.076 | -0.944 |
| DorfBauten | VegetationNoShadow | 25.357 | 25.508 | +0.151 | +0.273, +0.028 | +0.193 |
| DorfBauten | LocalLightsOff | 25.202 | 25.118 | -0.083 | -0.364, +0.197 | -0.196 |
| DorfBauten | AllDynamicShadowsOff | 25.410 | 23.201 | -2.210 | -1.902, -2.518 | -2.115 |
| DorfBauten | PostProcessingOff | 25.837 | 22.495 | -3.342 | -2.678, -4.006 | -3.264 |

## 5. GPU-/CPU-Analyse und Bedeutung der Faktoren

Die Ergebnisse sprechen für einen überwiegend render-/GPU-begrenzten Ablauf: Game-Thread meist etwa 6–7 ms im PIE, während GPU und Framezeit deutlich höher liegen; steigende Ausgabepixel erhöhen die Zeiten stark. Im Standalone liegt der Game-Thread ungefähr bei 1–2 ms, bei erheblich höheren GPU-/inklusive Renderzeiten. Das ist eine Einordnung, kein lückenloser CPU-/GPU-Scheduler-Nachweis.

Der finale Ranger spart in den gepaarten PIE-Läufen nur ungefähr **0,15–0,91 ms Median-Paardifferenz**, je nach Standort/Auflösung; einzelne Paare haben die Gegenrichtung. Am Gebäudestandort ist er außer Sicht und der Effekt praktisch null. Kein belastbarer großer FPS-Sprung und keine garantierte P95-Verbesserung.

Größere wiederholte Diagnoseeffekte:

- **PostProcessingOff:** ungefähr 3,3–4,3 ms weniger Framezeit. Das ist ein breiter Show-Flag-/Pipeline-Test, kein Beweis für einen einzelnen teuren Effekt; AA/Upscaling/Pipelinefolgen können mit betroffen sein.
- **Alle dynamischen Schatten aus:** etwa 2,2–3,2 ms. Shadow Depths und Shadow Projection sind als GPU-Zähler vorhanden. Die Kategorien können verschachtelt sein; nicht blind addieren.
- **Vegetation unsichtbar:** etwa 2,0–2,5 ms am Wald-/NPC-/Wegstandort; am Heilhaus kein stabiler Framezeitgewinn. Dieser Schalter umfasst Sichtbarkeit und die damit entfallenden Schatten-/Sichtbarkeitsfolgen, nicht ausschließlich Dreiecke.
- **Nur Vegetationsschatten aus:** deutlich kleiner und teils nicht stabil. Daraus folgt nicht, dass alle Schattenkosten von Bäumen stammen.
- **Ranger unsichtbar:** im Wald/Vorplatz etwa 0,55–0,84 ms, auf offenem Weg kein stabiler Gewinn. Enthält auch sichtbarkeitsabhängige Animationsfolgen, nicht reine Geometrie.
- **Ranger ohne Schatten / ohne Animation / konstantes Material:** kleine, teils wechselnde Ergebnisse. Der Flat-Materialtest verändert Normal-/Rauheits-/Texturinputs gemeinsam; keine isolierte Texturbandbreitenmessung.
- **Lokale Punkt-/Spotlichter aus:** kein stabiler Vorteil. Nicht gleichbedeutend mit „sämtliche Beleuchtung kostenlos“; Directional-/Rect-Lichter waren nicht dieser Faktor.

Die Vegetationsauswahl ist exakt im Probe-Code dokumentiert: registrierte StaticMesh-/Instancing-Komponenten mit `SM_WLA_` und Oak/Birch/Bush/Grass/Fern/Flower/Herb, ohne Ruins/Rune/Column. Kein pauschaler Schalter sämtlicher Umgebungsobjekte.

CSV zeigt auch Lumen- und SlateUI-/Unaccounted-Kosten. Das sind auffällige Zähler, keine separat bewiesenen Einzelursachen. **RHI/DrawCalls und passbezogene DrawCall-Zähler lieferten Nullwerte und sind nicht verlässlich auswertbar.** Keine erfundene Draw-Call-Anzahl. Ebenso kein belastbarer quantitativer Overdraw-/Quad-Overdraw-Nachweis. Maskierte/dithernde Vegetation kann Pixelkosten verursachen, obwohl GPU/Translucency 0 meldet. Texture-/Materialslotzahlen sind gemessen; einzelne Texturkosten und NPC-VRAM-Residency nicht isoliert erfasst.

Alle Faktoren nur temporär in der wegwerfbaren PIE-Welt geändert und vor der nächsten Variante zurückgestellt. **Keine abgeschalteten Schatten, Lichter, Vegetation oder Posteffekte in die Testkarte übernommen.**

## 6. Ranger-V2-Blenderquelle und Exporte

Maßgebliche Quelle: `Art/Characters/NPCs/Ranger/Source/Ranger_NPC_V2_Protected.blend`. Vollständig gepackt, in separater Blender-Instanz erneut erfolgreich geöffnet. Drei gepackte 2048×2048-Texturen, ursprüngliche UVMap, ein Materialslot. Live-Blender mit der vorhandenen Hobbit-Retopo-Sitzung nicht ersetzt oder gespeichert.

V1-Runtime: 90.000 Dreiecke / 44.390 geometrische Vertices. Bestehende High-Poly-Referenz und V1-Runtime unverändert als Referenzen behalten. Keine neue Retopologie, kein neues Rig, keine neue Animation. 24 Blender-Bones; in Unreal 25 einschließlich importiertem Armature-Root. Bone-/Restpose-Hash identisch mit V1. Source-Bounds bis etwa 1,80063 m / 180,063 cm; der bestehende etwa 1,80-m-Rangermaßstab und die Fußbasis wurden nicht verändert (Spieler weiterhin 1,40 m).

Reduktion kontrolliert vor dem Armature-Modifier. Kopf/Hände über empirisch geprüfte invertierte Vertex-Group-Gewichtung geschützt. Die erste ungeschützte Reduktion zeigte in Nahaufnahmen unvertretbare Gesichtsschäden und wurde verworfen. Keine Behauptung, ein erfolgreich ausgeführter Decimate-Modifier genüge als Qualitätstest.

| Kandidat | Geometrische Vertices | Dreiecke | Status |
|---|---:|---:|---|
| Geschützt LOD0 | 26.890 | 55.000 | Unreal-Kandidat, Kopf/Hände geschützt |
| Geschützt LOD1 | 11.390 | 24.000 | Unreal-Kandidat; nur mit konsistentem Importpfad |
| Geschützt LOD2 | 4.486 | 10.192 | **Verworfen**: sichtbare Kragen-/Kleidungsschäden; nicht im Runtime-Mesh |

Export: `Art/Characters/NPCs/Ranger/Exports/V2_Protected/SK_Ranger_NPC_V2_LOD0.fbx` und `...LOD1.fbx`. Der zusätzliche LOD2-FBX sowie `Exports/V2/` und `Ranger_NPC_V2.blend` sind erhaltene, verworfene Versuche, keine Alternativfreigaben.

Kopf-/Hand-Quellvertices zur Zieloberfläche: gemessen 0 mm Abweichung in den definierten geschützten Regionen. Globaler P95 etwa 1,00 mm / 3,98 mm für LOD0/1; Maximum etwa 7,90 / 29,50 mm. Das ist ein einseitiger Quellvertex-zu-Oberfläche-Test, **kein vollständiger Hausdorff- oder Qualitätsbeweis**. UVs, normalisierte Gewichte und endliche Normalen/Koordinaten geprüft. Vollständige Blender-Idle-/Talk-Zyklen kontrolliert. Unterkörper-/Umhangdetails werden bei LOD1 etwas kantiger; die Vorlage selbst besitzt bereits Oberflächen-/Gesichtsartefakte.

## 7. Unreal-Assets und tatsächlicher Reimport

**Arbeitskandidat:** `/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean`.

Wiederverwendet:

- `/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1_Skeleton`
- `/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Idle_V1`
- `/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Talk_V1`
- `/Game/Characters/NPCs/Ranger/Materials/MI_Ranger_V1` und bestehende Texturen.

Keine neuen Gameplay-Collider/Physics Assets. Bestehender NPC-Präsentationsactor und dessen sichtbarkeitsabhängige Animation/URO/kurzer Dreh-Tick weiterverwendet. Kein permanenter zusätzlicher NPC-Actor-Tick.

**Aufgedeckter Importfehler:** Der erste Runtime-Import zeigte bei LOD1 eine falsche Arm-/Körperhaltung, obwohl Bone-Namen, Counts und Blender-Bilder korrekt waren. Beide FBX-Dateien wurden in frischem Blender gelesen: Hierarchie, Bindepose, Objekttransformationen und Vertex-Group-Namen identisch. Der 24k-FBX funktionierte als separat importiertes Skeletal Mesh und als frischer Custom-LOD-Import. Ein nachträglicher Reimport über den anderen Importpfad erzeugte die Fehlpose erneut. Am selben Clean-Asset stellte **Legacy-FBX-Reimport** die korrekte Animation wieder her.

Der fehlerhafte Interchange-Pfad meldete ausdrücklich zwei unterschiedliche BindPose-Matrizen aus FbxCluster/FbxPose und eine nicht passende LOD-Namenskonvention. Diese Warnungen wurden nicht unterdrückt.

Daher Erstimport **und** Custom-LOD-Reimport konsistent mit `Interchange.FeatureFlags.Import.FBX=0`, nur scoped während der Operation und anschließend auf den vorherigen Wert 1 zurückgestellt. Tatsächlicher Reimport durchgeführt, gespeichert und danach aus der Spielkamera animiert geprüft. Keine globale Importer-Konfiguration geändert. Ein erneuter Reimport über einen abweichenden Standardpfad bleibt ein konkretes Wartungsrisiko.

Früher hatte ein automatisch angelegtes LOD-Settings-Asset außerdem eine zusätzliche 50-%-Reduktion aktiviert. Die tatsächlichen Renderdaten wurden deshalb nativ geprüft. Der finale Clean-Kandidat verwendet keine solche automatische Reduktions-DataAsset-Zuweisung. Der erste `SK_Ranger_NPC_V2` und `DA_RangerV2_LODSettings` bleiben **verworfene Diagnose**, `M_Ranger_FlatDiagnostic` ist ausschließlich ein A/B-Prüfmaterial. Keine neuen doppelten Texturen oder Animationsclips.

## 8. LODs, Entfernungen und Speicher

Native Renderdaten des finalen Clean-Assets:

| Mesh/LOD | Renderdreiecke | Rendervertices inkl. UV-/Normalensplits | approximative LOD-Renderdaten-Bytes |
|---|---:|---:|---:|
| V1 LOD0 | 90.000 | 76.506 | 3.528.192 |
| V2 LOD0 | 55.000 | 52.476 | 2.638.944 |
| V2 LOD1 | 24.000 | 27.390 | 1.349.160 |

LOD0: **38,9 % weniger Dreiecke**, etwa 31,4 % weniger Rendervertices. LOD1: 73,3 % weniger Dreiecke gegenüber V1. **Beide gespeicherten LOD-Renderdaten zusammen benötigen etwa 13,0 % mehr als V1**, nicht weniger; ein aktives LOD und der gesamte Asset-Speicher sind unterschiedliche Größen. UE-ResourceSizeEx ist kein vollständiger VRAM-/Prozess-Residency-Nachweis. Serialized UAsset: V1 17.471.356 Bytes, finaler V2-Clean-Kandidat 17.853.627 Bytes zum Prüfzeitpunkt. Originaltexturen geteilt.

ScreenSize LOD0 1,0 / LOD1 **0,12**, Hysterese **0,015**. Keine fixe Metergrenze: Bildschirmgröße, Bounds und Sichtbarkeit wirken mit. Vergleichsbilder bei tatsächlichen Kamera-NPC-Distanzen **27,12 / 28,77 / 30,23 m**; Spieler-NPC-Abstand und Kamerapose im Bildmanifest.

Der erste gezielte LOD-Direktweg traf die vorhandene NPC-Collision; keine Welt geändert. Der umgelegte, bereits im vollständigen Fußlauf bewährte Weg wurde erfolgreich mit Enhanced Input abgelaufen (26,85–37,44 m Kamera-NPC-Distanz), **ohne einen automatischen LOD-Wechsel zu erreichen**. Die frühere dicht erfasste Bildsequenz hatte zusätzliche Screenshot-Hitches und blieb ebenfalls bei LOD0. Deshalb **keinen bestandenen natürlichen LOD-Popping-/Schattenwechseltest behaupten**. Beide erzwungenen LOD-Stufen wurden bei identischer Pose visuell verglichen; sichtbare große Sprünge/Defekte dabei nicht festgestellt. Vor Freigabe die automatische Grenze gezielt justieren und erneut mit realer Bewegung prüfen.

## 9. Echte Bildnachweise

36 unbearbeitete Unreal-Spielkamera-Vergleiche in `Art/Characters/NPCs/Ranger/Review/V2/UnrealAccepted/`: Dialogdistanz, typische Entfernung, Wald; jeweils Front, Seite, Dreiviertel und Rücken; V1, V2-LOD0 und erzwungenes V2-LOD1. **2331×1346-Ausgabe**, FOV/Position unverändert. Keine generierten Konzeptbilder.

Blender-Nahaufnahmen in `Review/V2/BlenderProtected/`. Fehlgeschlagene Importe in `Unreal/`, `UnrealFinal/`, `NativeAnim/` nicht mit finalen Nachweisen verwechseln. Korrekt animierter Reimport: `NativeAnim_ConsistentReimport/`.

### V1 – Dialogentfernung, Dreiviertel

![V1 – Dialogentfernung, Dreiviertel](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/UnrealAccepted/Dialog_ThreeQuarter_V100000.png)

### V2 LOD0 – gleiche Spielkamera

![V2 LOD0 – gleiche Spielkamera](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/UnrealAccepted/Dialog_ThreeQuarter_V200000.png)

### V2 LOD1 – erzwungener Vergleich

![V2 LOD1 – erzwungener Vergleich](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/UnrealAccepted/Dialog_ThreeQuarter_V2LOD100000.png)

Die originale dunkle Haut-/Kleidungswirkung im Schatten bleibt teilweise schwer lesbar; keine eigenmächtige Neuinterpretation der Vorlage. Die geschützte Reduktion beseitigt keine schon in V1 vorhandenen Artefakte. Keine finale Künstlerfreigabe behauptet.

## 10. Animation und Gameplay – tatsächlich durchgeführt

Frischer eingebetteter PIE-Lauf in der Testkopie: **263.65 m**, 193.90 s Wandzeit / 177.59 s protokollierte Laufzeit. Enhanced Input für Bewegung; bestehende Interaktions-, Menü- und Battle-Presenter-Funktionen per Prüfsystem ausgelöst. Kein menschlicher Handtest behauptet. **Keine Test-Teleports im vollständigen Rundweg**, nur das reguläre bestehende Heilhaus-Relocation-System.

- Menü geöffnet/geschlossen, Eingabesicherung geprüft.
- Wanderer-Dialog und Queststart; Ranger erhält Conversation-Signal und Alpha >0,5; Blickwendung/Gesprächsbildsequenzen aufgenommen.
- Wildkampf **mit erfolgreichem Fang**, danach drei Teammitglieder.
- Liora besiegt; Trainerstatus bestätigt.
- Vor Archivaktivierung gespeichert, Runtime-Trainerstatus kontrolliert verändert, geladen; Trainer und HP/PP korrekt wiederhergestellt. HUD-Bild nach Load zeigt „Untersuche den Archivstein“.
- Archiv aktiviert, Flag im Save vorhanden; Rückdialog sichtbar geändert („Der Archivstein leuchtet wieder…“), aktive Questanzeige beendet.
- Heilhaus gerade hinein, zur Heilerin, alle HP/PP voll, Save/Checkpoint bestätigt, hinaus und diagonal erneut hinein/hinaus. Cutaway/Relocation/Innenbewegungsbasis korrekt.
- Wald-Rundweg, Kronenfreistellung, alle acht Richtungen und abschließendes Menü geprüft.
- **Sprite-Fallback tatsächlich ein-/ausgeschaltet und Sichtbarkeit überprüft**, danach 3D wiederhergestellt.
- Maximal protokollierte normale Geschwindigkeit 210.000005 cm/s (Float-Toleranz zu 210). Keine neuen Kollisionen oder Abstürze im Rundweg.

Zusätzlicher Python-Direktzugriff auf geschützte Quest-/Save-Felder war nicht möglich; keine Produktions-API dafür aufgebohrt. Der gescheiterte Zusatzprüfer ist dokumentiert, nicht als Erfolg gezählt. Questprüfung hier durch tatsächlichen Ablauf/HUD/Abschlussdialog plus vorhandene Automation. Vollständige Bewegungs-/Interaktionsprotokolle: `Review/V2/FootTest/FootTest.json`, `FootFrames.jsonl`, `FootProgress.json` und Screenshots/Bildsequenzen. `Shot showui` enthält bewusst auch die Editoroberfläche; deren gesamte Bildgröße ist **keine** behauptete Renderauflösung der Performance-Messung.

## 11. Build, Automation und Map Check

- Development Editor Build erfolgreich, letzter Lauf `BuildCleanCandidate.log`, 7,75 s. C++ ausschließlich neues ausdrücklich gestartetes Development-Messwerkzeug; keine bestehenden Gameplaydateien verändert.
- **43/43 Automation erfolgreich**, 0 Fehler, 0 Warnungstests, 0 nicht ausgeführt. Frischer Unreal-Prozess mit NullRHI; reine Suite 0.661 s. NullRHI ersetzt nicht die separat vorgenommenen visuellen PIE-Prüfungen.
- **Map Check der neuen Testkarte: 0 Fehler / 0 Warnungen** (finaler `MAP CHECK`, 09:50 UTC). Der erste Log-Abfrageversuch mit Kategorie MapCheck war technisch nicht verfügbar; anschließende ungekürzte Musterabfrage enthält den tatsächlichen Check.
- Platzierte Actor-Transformationen zur Baseline identisch. Audit zählt in der initialisierten Editorwelt drei zusätzliche Engine-Manager (GameplayDebuggerPlayerManager, AbstractNavData, BuoyancyManager); keine neu platzierten Gameplay-/Geometrieobjekte. Der einzige beabsichtigte Darstellungsunterschied ist das Ranger-Mesh. Präsentationskomponente weiterhin NoCollision, gleicher SourceActor/Idle/Talk/Skeleton. Keine schwebenden PIE-Fenster benutzt.
- Anfängliche Compile-/Python-API-Fehler behoben und ihre Logs erhalten. Zusätzlich im Editor: generische `LogAutomationTest: Condition failed`-Startmeldungen ohne zugeordneten Projekttest, wiederholtes falsches CPU-Format von `idevice_id`, Audio-Samplerate-, MotionVectorSimulation- und MCP-/Socket-/Diagnosewarnungen. Diese sind **nicht** mit den 43 erfolgreichen Projekttests gleichgesetzt oder verschwiegen. Zusätzlich erfasst: Interchange-LOD-Muster-/BindPose-Warnungen im verworfenen Import, eine Warnung über 31 erfolglose ConsoleObject-Lookups für `Shot` (die Screenshotdateien wurden tatsächlich erzeugt und geprüft) sowie EOS-Analytics-Flush-/Heartbeat-Warnungen. Vollständige Logs `EditorWarningsPreRestart.json`, `EditorWarningsFinal.json`, `StartupAutomationMessages.json`, `Automation.log`; keine pauschale Warnungsunterdrückung. Ursache der generischen Startup-Meldungen in diesem Auftrag nicht abschließend ermittelt.

[Automation-Report](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/Automation/index.html) · [Map-Check-Meldungen](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/MapCheckLog.json) · [Map-/Actor-Audit](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/FinalMapAudit.json).

## 12. Verbleibende Probleme und Freigabeempfehlung

**Empfehlung: V2 in der separaten Testkarte belassen; noch nicht für den dauerhaften Austausch in Dev_TestMap_VisualV2 freigeben.**

Begründung: sichtbare Geometrie im geprüften Zustand weitgehend erhalten, weniger aktive Geometrie, Animation/Gameplay im Fußlauf funktionsfähig. Der FPS-Effekt ist jedoch klein, P95 nicht überall besser, Standalone stark driftend, und ein natürlicher automatischer LOD-Wechsel wurde nicht nachgewiesen. Außerdem muss der konsistente Legacy-Reimport als verbindlicher Arbeitsweg abgesichert bleiben. Das ist keine automatische Künstler-/Performancefreigabe allein wegen grüner Tests.

Offen: automatische LOD-Grenze im sichtbaren Spielbereich fein abstimmen und Übergang/Schatten real ablaufen; stabile zeitlich gepaarte Standalone-Reihe bei kontrollierter Vordergrund-/OS-/Leistungssituation; keine verlässlichen Draw Calls, kein quantitatives Overdraw, keine isolierte Texture-/VRAM-Messung. Keine Ursache für die große Zeitdrift erfunden.

## 13. Konkrete nächste Optimierungsschritte

1. Zunächst die größeren Renderkosten fein isolieren: einzelne Post-/AA-/Upscaling-Effekte unter unveränderter Bildqualität gegentesten; breites PostProcessingOff nicht als Lösung übernehmen.
2. Dynamische Schatten: tatsächlich benötigte Reichweite/Caster, Shadow Depths/Projection und entfernte kleine Objekte gezielt prüfen. Keine pauschale Schattenabschaltung.
3. Wald: passende Vegetations-LODs/Culling und maskierte Material-/Pixelkosten getrennt untersuchen; Gebäudevorplatz zeigt andere Kosten als Wald. Vorhandene Reveal-Materialien/Positionen erhalten.
4. Ranger: konservative automatische LOD-Grenze anhand sichtbarer Übergänge nachziehen, Importvertrag Legacy-FBX bewahren; keine weitere aggressive 10k-Reduktion vor Qualitätsnachweis.
5. Standalone-Ausreißer mit zeitnahen V1/V2-Paaren und zusätzlich verifizierter Vordergrund-/Leistungs-/Speichersituation untersuchen. macOS „nominal“ nicht als Taktstabilitätsbeweis verwenden.

## Dateien, Git und Arbeitsartefakte

Neu in diesem Auftrag: zwei Ranger-V2-Blender-Versuchsversionen, getrennte FBX-Kandidaten, neue RangerV2-Unreal-Assets einschließlich Diagnosen, eine neue Performance-Testkarte, ein Development-C++-Messwerkzeug, reproduzierbare Prüfskripte/Pläne, dieser Bericht sowie Review-/Mess-/Bild-/Lognachweise. **Bestehende Projektdateien aus der Eingangsliste inhaltlich unverändert.**

Maßgebliche Dateien:

- `Art/Characters/NPCs/Ranger/Source/Ranger_NPC_V2_Protected.blend`
- `Art/Characters/NPCs/Ranger/Exports/V2_Protected/SK_Ranger_NPC_V2_LOD0.fbx`, `...LOD1.fbx`
- `Content/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean.uasset`
- `Content/Maps/Dev_TestMap_RangerPerfV2.umap`
- `Source/PokeMonster/Development/PokeMonsterPerformanceProbe.cpp`
- `Tools/PerformanceRangerV2/`
- `Art/Characters/NPCs/Ranger/Review/V2/`
- `Docs/POKEMONSTER_PERFORMANCE_RANGER_V2_PRUEFBERICHT.md`

Vollständige neue Dateiliste: `Review/V2/NewFiles.json`. Volatile Job-/Ack-/Slate-Dateien, Logs, verworfene Kandidaten, Save-Backups und Buildausgaben sind Arbeits-/Diagnoseartefakte, keine pauschale Empfehlung, alles zu versionieren. Nichts gelöscht. Rohmessungen unter Saved sind bewusst getrennt von Runtime-Assets.

`git diff --check`: erfolgreich, keine Ausgabe. Abschließendes `git status --short`:

```text
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
```

Die bereits anfangs geänderte `Dev_TestMap_VisualV2.umap` erscheint weiterhin als M; ihr SHA-256 ist gegenüber dem Eingangszustand identisch. Gleicher HEAD, kein Commit, kein Push, nichts gestaged. Temporäre Editorparameter wiederhergestellt; keine schmutzigen Map-/Contentpakete bei Abschluss. Dev-Spielstand bytegleich zurückgesichert.
