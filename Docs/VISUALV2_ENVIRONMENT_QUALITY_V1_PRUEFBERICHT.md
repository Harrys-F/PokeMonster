# VisualV2 Environment Quality V1 – Prüfbericht

Datum: 17.10.2026. Unreal Engine 5.8.2, macOS, MacBook Air M4 / 16 GB.

## Ergebnis und Empfehlung

Die vier EnvironmentPerfV1-Maßnahmen wurden **einzeln** auf einer unveränderten VisualV2-Kopie gemessen. 648 vollständige Framezeitsegmente, 144 Einzelfaktorvergleiche, sechs Auflösung/Qualität/Screen-Percentage-Konfigurationen, drei Orte und drei Wiederholungen je Zustand/Ort. PIE und Standalone getrennt. Keine Maßnahme automatisch übernommen.

| Maßnahme | Bewertung | Begründung / Grenze |
|---|---|---|
| Motion Blur aus | **empfehlenswert für Außenbewegung** | Schärfere vorbeiziehende Umgebung; kleiner, nicht überall reproduzierbarer Zeitvorteil. Keine Lösung für dunkle Figuren. Für eine spätere dauerhafte Übernahme außen begrenzen. |
| Bloom aus | **bedingt empfehlenswert** | In den geprüften Tageslichtansichten geringer Bildunterschied und teilweise messbarer Vorteil. Andere Zellen gemischt; globaler Schalter könnte Innenraumglanz verändern. |
| VSM-Richtungslicht: zwei SMRT-Strahlen | **bedingt empfehlenswert** | Schattenprojektion messbar günstiger, aber native QHD-Details zeigen zusätzliche Körnung der weichen Kronenschatten. Keine uneingeschränkte Artfreigabe. |
| Lumen-Integration Faktor 2, High | **bedingt empfehlenswert** | Kleinere Screen-Probe-Kosten und wiederholter Standalone-Vorteil; feinste indirekte Normal-/Kontaktdetails können weicher werden. Kein Gather-Methodenwechsel. |
| Derselbe Lumen-Parameter, Medium | **nicht empfehlenswert als Optimierung** | Medium nutzt bereits Irradiance Field statt Screen Probe. Kleine Differenzen sind hier kein Wirkungsnachweis dieses Parameters. |

Empfohlene erste spätere Umsetzung: nur die Bewegungsunschärfe im Außenbereich deaktivieren und separat abnehmen. Bloom danach getrennt entscheiden. Zwei Schattenstrahlen erst bei akzeptierter Körnung; Lumen-Integration ausschließlich für den tatsächlich aktiven High-Screen-Probe-Pfad. Vor einer Kombination erneut messen: **Einzelgewinne dürfen nicht addiert werden.** Keine dieser kleinen Maßnahmen bringt QHD/High in die Nähe stabiler 60 FPS.

## 1. Arbeitsbasis und Projektschutz

Schlanker Worktree:
`/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`

Branch `codex/slim-backup-v5`, HEAD `a4cfd0baeeffbaccf928151552faabd01d41b704`. Arbeitsbaum zu Beginn sauber; origin/main zu Beginn direkt als derselbe Commit geprüft. Kein Fetch, Branchwechsel, Commit oder Push im Auftrag. Die abschließende erneute Remote-Abfrage scheiterte an DNS-Auflösung von github.com; daraus wird keine Aussage über einen neueren Remote-Stand abgeleitet.

Das ursprüngliche Projekt bleibt auf main / `03492bd96b4dba44692f675c19d5f11abfa86b4b`, ebenso der dauerhafte Ref `refs/archive/pokemonster/full-backup-03492bd`. Der abschließende SHA-256-Vergleich bestätigt **alle 2.769 vorher versionierten Dateien des schlanken Worktrees und alle 11.343 vorher versionierten Dateien des Vollbackups bytegleich, keine fehlend**. Diese Aussage betrifft die erfassten Projektdateien, nicht automatisch jeden ignorierten Editorcache. Kein Save All, Discard All, Force Quit, Reset, Restore, Clean oder Löschen vorhandener Dateien.

Gelesen: AGENTS, GRAFIKSTIL, relevante TECHNIK/ENTSCHEIDUNGEN/SPIELIDEE/SPIELREGELN, EnvironmentPerfV1-Bericht und der externe zentrale Referenzmap-Bericht. Die alte Editorsitzung wurde regulär geschlossen; gearbeitet wurde anschließend im schlanken Worktree.

[Zentrale Referenzmap V1 – Grundlage](/Users/harry/Documents/Codex/PokeMonster_ZentraleReferenzmap_V1_2026-10-17/ZENTRALE_REFERENZMAP_V1_PRUEFBERICHT.md); [Schutzvergleich](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/ProtectionAudit.json).

## 2. Separate Testkarte und exakt erhaltener Szenenstand

**Neue Karte:** `/Game/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1`.

Über `EditorLoadingAndSavingUtils.save_map` unter einem neuen Paketnamen aus `/Game/Maps/Dev_TestMap_VisualV2` erzeugt und explizit geladen. Die Quelle wurde nicht gespeichert. Die neue Karte ist bewusst ein neutraler Kontrollstand; keine Optimierung aktiviert sich beim gewöhnlichen Öffnen automatisch. Die vier Varianten werden explizit über den vorhandenen nativen `pm.EnvPerf.Run`-Probe für die Dauer eines Testsegments gesetzt und danach restauriert.

Vor und nach dem Fußlauf: **1.348 Actors** verglichen; keine fehlenden, zusätzlichen oder abweichenden Einträge. Erfasst wurden Transforms, Mesh-/Materialreferenzen, HISM-Instanztransformationen, Kollisionen, NPC-Quelle und Clips, Postprocess-Volumes und WorldSettings. Beide Karten erben denselben Projekt-GameMode. Keine Vegetationsposition, Dichte, Geometrie, Schattenwerfer-Flags, LOD-Daten oder Gameplay-Identität verändert. Vor dem regulären Editorende keine Dirty-Map-/Content-Pakete.

Kamera unverändert: **2850 cm, Pitch −50°, Yaw −45°, FOV 35°**. Playermaßstab 140 cm, Gehen 210 cm/s, Capsule Radius 28 / halbe Höhe 48 cm unverändert; Innenkamera und Relocation unverändert. Ranger bleibt die bestehende V1-Präsentation, kein MotionV2/V3-Paket eingeschleust.

[Actor-/Komponentenaudit](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/Data/MapCopyAudit.json).

## 3. Tatsächlich geprüfte Parameter und Abgrenzung zu EnvironmentPerfV1

| Variante | Einziger geänderter Faktor |
|---|---|
| MotionBlurOff | `r.MotionBlurQuality=0` |
| BloomOff | `r.BloomQuality=0` |
| VSMRayCount2 | `r.Shadow.Virtual.SMRT.RayCountDirectional=2`, gegenüber Medium 4 / High 8 |
| LumenIntegrate2 | `r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor=2`, gegenüber 1 |

Aktiver Renderer: Metal SM6, Virtual Shadow Maps, TSR. Keine pauschale sg-Absenkung zwischen A und B, kein deaktiviertes Lumen, kein Wechsel auf den EnvironmentPerfV2/V3-Gather-Kandidaten, kein Ambient-Occlusion-/Tonemapping-/Texturabbau. Qualität ist nur die deklarierte Matrixvariable, innerhalb jedes A/B-Vergleichs identisch.

**Wichtige Abgrenzung:** Die Bloom-/Motion-Blur-Tests verwenden vorhandene globale Runtime-Qualitätsschalter. Sie sind keine unveränderte Übernahme der alten, außen begrenzten PP-Volume-Overrides `BloomIntensity=0` / `MotionBlurAmount=0`. Quality-Off kann auch Innenräume betreffen. BloomIntensity=0 verändert darüber hinaus Voraussetzungen weiterer Postprocess-Pfade; deshalb keine Gleichsetzung aller Kosten/Nebenwirkungen. Die gemessenen Werte gelten für die oben genannten CVars. Eine spätere maplokale Umsetzung muss Innenräume explizit schützen und erneut geprüft werden.

Lokaler UE-Quellcode: Motion Blur setzt Quality > 0 und Amount > 0 voraus; BloomQuality 0 deaktiviert Gaussian Bloom. BaseScalability verwendet Medium `r.Lumen.FinalGatherMethod=0`, High `=1`. Medium-Lumen2 wird daher als No-op-/Driftkontrolle behandelt, nicht als nachgewiesene Optimierung.

## 4. Messmethode und verifizierte Auflösungen

| Konfiguration | Ausgabe / Viewport / Target | Qualität | Screen Percentage | Abgeleitete interne Größe |
|---|---|---|---:|---|
| 1 | 1280 × 720 | Medium | 75 % | 960 × 540 |
| 2 | 1280 × 720 | Medium | 100 % | 1280 × 720 |
| 3 | 2560 × 1440 | Medium | 75 % | 1920 × 1080 |
| 4 | 2560 × 1440 | Medium | 100 % | 2560 × 1440 |
| 5 | 2560 × 1440 | High | 75 % | 1920 × 1080 |
| 6 | 2560 × 1440 | High | 100 % | 2560 × 1440 |

Jede Konfiguration in eingebettetem PIE und separatem `UnrealEditor -game`-Prozess. Standalone ist hier **Development mit Editorbinary, kein paketierter Shipping-Build**. Während Standalone kein Editor offen. PIE-Hauptfenster 2940 × 1696 Slate-Pixel / DPI 2, aber der gemessene FSceneViewport, Target und ViewRect sind auf die oben verifizierte Ausgabe festgelegt. Standalone-Fenster entspricht jeweils 1280 × 720 beziehungsweise 2560 × 1440 / DPI 1. Fenstergröße und Rendergröße werden nicht verwechselt.

Die internen Maße stammen vom Renderthread-Screen-Percentage-Treiber mit UE-ceil-Regel; kein direkter SceneColor-Allocation-Readback. Alle 648 Segmente bestehen Extent-, Fraction- und Kameraprüfung. Dynamische Auflösung aus, Secondary Fraction 1. VSync=0, t.MaxFPS=0; `rhi.SyncInterval=1` unverändert. Native 720p/75 läuft häufig bei etwa 16,67 ms/60 FPS trotz niedrigerer GPU-Zeit: mögliche Metal-/Präsentationsbegrenzung, keine behauptete unbegrenzte Reserve. PIE-Renderthreadwerte nahe null sind nicht belastbar und erscheinen als —. Native Renderthread-Wall-Zeit enthält GPU-/Present-Warten und ist keine reine CPU-Rechenzeit.

Orte / Player-Capsule-Zentrum in cm: Dorf/Heilhaus (−4100, 450, 50,15), Wald (−4300, 1550, 50,15), offener Weg (−36,6, −47,1, 50,15). Kamera B und Blickrichtung fest; NPCs im bestehenden Idle, keine Gespräche/Kämpfe im Timingfenster. Kontrollierte Positionswechsel für Profiling sind keine Gameplay-Fußprüfung.

Je Ort/Konfiguration drei Wiederholungen: Kontrolle → vier Einzelfaktoren → Kontrolle. Zweite Wiederholung mit umgekehrter Faktorenfolge. **5 s Warm-up, 8 s Messung pro Segment**. 216 Kontrollen + 432 Kandidatensegmente = 648. Startup-/Ladevorgänge vor den Segmenten; keine Builds, Bildkompositionen oder großen Hashaudits während der GPU-Timings. Kurze Stichproben, kein eigener 10–15-Minuten-Dauerstabilitätstest dieses Auftrags.

Median-FPS = 1000 / Median nativer Wall-Clock-Frameintervalle. P95 linear interpoliert je Segment. Für A wird je Wiederholung das Mittel der flankierenden Kontrollmediane gebildet, danach Median der drei Wiederholungen; B ebenso aus den Kandidatenmedianen. P95 analog, kein gepooltes Gesamt-P95. **Paar-Delta = Median der drei einzelnen B−A-Differenzen; muss nicht der Differenz der separat berichteten A/B-Mediane entsprechen.** Delta-Min/Max und Kontrolldrift bleiben erhalten. Drei Läufe liefern keine formale statistische Signifikanz; kleinste Differenzen nicht überinterpretieren.

Foundation-Thermikmonitor: 1.006 Messpunkte, durchgehend „fair“, Netzbetrieb zu Beginn 100 %. Keine Temperaturgrad-, Leistungs- oder Taktsensordaten; zeitlich weit auseinanderliegende Modi deshalb nicht als isolierter Editor-Overhead-Vergleich interpretieren.

**Zählerlücke:** Alle 648 nativen Framezeitmessungen sind vollständig. GPU-/CSV-Zähler für 642 Segmente vorhanden. Der bestehende Standalone-Probe ruft nach dem letzten `csvprofile stop` unmittelbar `quit` auf; der asynchrone Writer hinterließ in jedem nativen Plan Segment 53 als leere CSV. Deshalb fehlt am offenen Weg jeweils die dritte abschließende GPU-Kontrolle. Strenge Drei-Paar-GPU-/CPU-Zusammenfassungen stehen dort als —; zwei gültige GPU-Paare sind separat mit n=2 ausgewiesen. Keine Werte ersetzt oder nacherfunden. Eine spätere Probe-Verbesserung sollte vor Quit auf den CSV-Schreibabschluss warten; bestehender C++-Code wurde hier nicht verändert.

[Validierte Matrix](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/Data/MatrixValidation.json)

[648 Einzelmessungen (CSV)](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/Data/IndividualMeasurements.csv)

[144 Faktorvergleiche (CSV)](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/Data/FactorSummary.csv)

[GPU-Verfügbarkeit einschließlich expliziter n=2-Paare](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/Data/GPUCounterAvailability.json)

## 5. Kontrollzustand – vollständige Übersicht

Zeiten in ms. Je Zeile drei wiederholte, flankierende Kontrollen. Fehlende strenge Drei-Paar-Zähler am nativen Weg bleiben —. GPU-Pässe können verschachtelt sein und werden nicht addiert.

| Modus | Konfiguration | Ort | FPS | Frame | P95 | GPU | Game | Render | ShadowProjection | ShadowDepths |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75 % | Dorf | 49.72 | 20.11 | 25.65 | 19.30 | 6.56 | — | 0.57 | 1.37 |
| PIE | 1280×720 / Medium / 75 % | Wald | 50.10 | 19.96 | 25.41 | 19.28 | 6.70 | — | 0.58 | 1.36 |
| PIE | 1280×720 / Medium / 75 % | Weg | 45.82 | 21.83 | 27.22 | 21.01 | 7.13 | — | 0.64 | 1.24 |
| PIE | 1280×720 / Medium / 100 % | Dorf | 33.59 | 29.77 | 32.32 | 29.06 | 6.30 | — | 1.06 | 1.48 |
| PIE | 1280×720 / Medium / 100 % | Wald | 33.80 | 29.59 | 32.47 | 28.74 | 6.37 | — | 1.06 | 1.54 |
| PIE | 1280×720 / Medium / 100 % | Weg | 32.52 | 30.75 | 32.98 | 29.95 | 6.31 | — | 1.14 | 1.40 |
| PIE | 2560×1440 / Medium / 75 % | Dorf | 19.93 | 50.17 | 54.42 | 49.30 | 6.56 | — | 2.62 | 1.83 |
| PIE | 2560×1440 / Medium / 75 % | Wald | 19.83 | 50.43 | 55.33 | 49.36 | 6.52 | — | 2.82 | 1.91 |
| PIE | 2560×1440 / Medium / 75 % | Weg | 19.53 | 51.22 | 57.22 | 50.42 | 6.66 | — | 2.94 | 1.75 |
| PIE | 2560×1440 / Medium / 100 % | Dorf | 13.45 | 74.38 | 82.55 | 73.62 | 7.50 | — | 6.60 | 2.34 |
| PIE | 2560×1440 / Medium / 100 % | Wald | 13.32 | 75.06 | 90.21 | 73.24 | 7.56 | — | 6.82 | 2.57 |
| PIE | 2560×1440 / Medium / 100 % | Weg | 13.20 | 75.78 | 81.41 | 74.27 | 7.55 | — | 7.57 | 2.29 |
| PIE | 2560×1440 / High / 75 % | Dorf | 14.75 | 67.81 | 77.51 | 65.63 | 7.39 | — | 4.22 | 2.04 |
| PIE | 2560×1440 / High / 75 % | Wald | 14.89 | 67.18 | 76.09 | 64.91 | 7.27 | — | 5.78 | 2.13 |
| PIE | 2560×1440 / High / 75 % | Weg | 14.52 | 68.89 | 75.43 | 67.10 | 7.46 | — | 7.25 | 1.89 |
| PIE | 2560×1440 / High / 100 % | Dorf | 9.98 | 100.22 | 109.29 | 97.17 | 8.45 | — | 12.50 | 2.51 |
| PIE | 2560×1440 / High / 100 % | Wald | 9.98 | 100.24 | 112.91 | 97.30 | 7.79 | — | 12.76 | 2.70 |
| PIE | 2560×1440 / High / 100 % | Weg | 9.82 | 101.87 | 111.29 | 99.08 | 7.72 | — | 13.36 | 2.39 |
| Standalone | 1280×720 / Medium / 75 % | Dorf | 60.02 | 16.66 | 17.01 | 13.01 | 1.42 | 16.66 | 0.56 | 1.32 |
| Standalone | 1280×720 / Medium / 75 % | Wald | 59.99 | 16.67 | 17.01 | 12.91 | 1.28 | 16.66 | 0.59 | 1.36 |
| Standalone | 1280×720 / Medium / 75 % | Weg | 60.03 | 16.66 | 17.03 | — | — | — | — | — |
| Standalone | 1280×720 / Medium / 100 % | Dorf | 54.50 | 18.35 | 20.42 | 17.24 | 1.64 | 18.34 | 1.11 | 1.49 |
| Standalone | 1280×720 / Medium / 100 % | Wald | 56.95 | 17.56 | 19.40 | 16.65 | 1.55 | 17.55 | 1.10 | 1.54 |
| Standalone | 1280×720 / Medium / 100 % | Weg | 53.61 | 18.65 | 20.61 | — | — | — | — | — |
| Standalone | 2560×1440 / Medium / 75 % | Dorf | 30.71 | 32.56 | 34.30 | 31.33 | 1.54 | 32.57 | 2.62 | 1.87 |
| Standalone | 2560×1440 / Medium / 75 % | Wald | 31.72 | 31.52 | 33.30 | 30.31 | 1.55 | 31.52 | 2.64 | 1.87 |
| Standalone | 2560×1440 / Medium / 75 % | Weg | 30.38 | 32.92 | 35.07 | — | — | — | — | — |
| Standalone | 2560×1440 / Medium / 100 % | Dorf | 20.94 | 47.75 | 49.98 | 46.20 | 1.83 | 47.75 | 4.56 | 2.30 |
| Standalone | 2560×1440 / Medium / 100 % | Wald | 21.51 | 46.49 | 49.06 | 45.08 | 1.85 | 46.48 | 4.56 | 2.50 |
| Standalone | 2560×1440 / Medium / 100 % | Weg | 20.80 | 48.08 | 51.51 | — | — | — | — | — |
| Standalone | 2560×1440 / High / 75 % | Dorf | 23.54 | 42.49 | 44.27 | 40.43 | 1.72 | 42.47 | 3.86 | 1.91 |
| Standalone | 2560×1440 / High / 75 % | Wald | 24.00 | 41.67 | 44.34 | 39.64 | 1.74 | 41.60 | 4.01 | 1.98 |
| Standalone | 2560×1440 / High / 75 % | Weg | 22.87 | 43.73 | 46.71 | — | — | — | — | — |
| Standalone | 2560×1440 / High / 100 % | Dorf | 15.86 | 63.07 | 65.81 | 61.48 | 1.98 | 63.03 | 7.08 | 2.39 |
| Standalone | 2560×1440 / High / 100 % | Wald | 16.06 | 62.27 | 68.22 | 60.71 | 1.96 | 62.26 | 7.16 | 2.61 |
| Standalone | 2560×1440 / High / 100 % | Weg | 15.65 | 63.88 | 68.28 | — | — | — | — | — |

## 6. Einzelfaktoren – QHD High/100 im Wald

Bewusst nur ein gleichartig konfigurierter Standort als lesbares Beispiel; die vollständige Matrix folgt im Anhang. Kein Vergleich mit den früheren 740p- oder 2331×1346-Messungen.

| Modus | Zustand | FPS A → B | Frame A → B | P95 A → B | GPU A → B | ShadowProjection A → B | Gepaarte ΔFrame | Δ Min … Max |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| PIE | MotionBlurOff | 9.98 → 10.19 | 100.24 → 98.12 | 112.91 → 113.06 | 97.30 → 95.19 | 12.76 → 12.64 | -3.26 | -3.45 … 0.88 |
| PIE | BloomOff | 9.98 → 10.22 | 100.24 → 97.85 | 112.91 → 104.47 | 97.30 → 95.47 | 12.76 → 12.60 | -3.53 | -3.60 … 1.08 |
| PIE | VSMRayCount2 | 9.98 → 10.39 | 100.24 → 96.21 | 112.91 → 102.42 | 97.30 → 93.14 | 12.76 → 10.11 | -4.39 | -5.17 … -1.84 |
| PIE | LumenIntegrate2 | 9.98 → 10.34 | 100.24 → 96.67 | 112.91 → 103.32 | 97.30 → 93.82 | 12.76 → 12.61 | -3.58 | -4.09 … -3.05 |
| Standalone | MotionBlurOff | 16.06 → 16.02 | 62.27 → 62.41 | 68.22 → 72.99 | 60.71 → 60.78 | 7.16 → 7.29 | -0.97 | -1.86 … 1.66 |
| Standalone | BloomOff | 16.06 → 16.42 | 62.27 → 60.90 | 68.22 → 65.00 | 60.71 → 59.67 | 7.16 → 6.99 | -1.25 | -1.61 … -0.97 |
| Standalone | VSMRayCount2 | 16.06 → 16.33 | 62.27 → 61.23 | 68.22 → 68.25 | 60.71 → 59.58 | 7.16 → 5.20 | -2.10 | -2.24 … -0.91 |
| Standalone | LumenIntegrate2 | 16.06 → 16.48 | 62.27 → 60.66 | 68.22 → 64.28 | 60.71 → 59.33 | 7.16 → 7.13 | -1.49 | -1.70 … -1.48 |

Einordnung:

- **Motion Blur:** Standalone QHD/High/100 im Wald kein stabiler Gesamtgewinn (Spanne schließt Verschlechterung ein, P95 ebenfalls schlechter). Auf Dorf/Weg und anderen Konfigurationen teils hilfreicher. Die Empfehlung stützt sich vor allem auf schärfere Außenbewegung, nicht auf garantierte FPS.
- **Bloom:** QHD/High/100 im nativen Dorf und Wald alle drei Framezeit-Paare günstiger; am offenen Weg gemischt und schlechteres Kandidaten-P95. Kein universeller Qualitäts-/Performancegewinn.
- **Schatten:** Native Waldprojektion etwa 7,16 → 5,20 ms; ShadowDepths praktisch unverändert. Das passt zur geänderten Abtastung statt entfernter Geometrie. Gesamtframezeit gewinnt weniger als der einzelne Projektionspass; körnigere Halbschatten bleiben sichtbar.
- **Lumen High:** Native Wald-Gatherkosten etwa 11,19 → 9,45 ms; GPU gesamt etwa 60,71 → 59,33 ms. Kontrolliert messbarer Teilgewinn, keine generelle Beleuchtungslösung. Hohe nicht zugeordnete GPU-Anteile bleiben; nicht sämtliche Last den Bäumen oder Lumen zuschreiben.
- **Medium:** Kein kausaler Lumen2-Gewinn, auch wenn einzelne Framezeiten differieren. Schatten-/Postprocess-Ergebnisse variieren nach Auflösung/Ort und stehen vollständig im Anhang.

## 7. Echte Spielkamera-Bildvergleiche

60 native Standbilder: 720p Medium/75, QHD Medium/75, QHD High/100, jeweils Wald, Heilhaus, Weg sowie Player/NPCs, jeweils Kontrolle und vier einzelne Faktoren. 48 vollständige A/B-Anordnungen plus vier NPC-Detailvergleiche. Unskalierte Originalpixel im PNG, Beschriftung außerhalb der Szene; die zusätzlichen JPEG-Vorschauen sind verkleinert. Keine synthetischen Konzeptbilder oder Farbretusche. Alle statischen Vergleichsaufnahmen stammen aus PIE, nicht fälschlich aus Standalone. Kameraposen zwischen A/B auf < 0,02 cm geprüft; Rotation/FOV/Auflösung identisch. Animationen nur für statische Aufnahmen pausiert, danach restauriert.

**Heilhaus – Bloom aus**

![Heilhaus – Bloom aus](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/VEQ1_Review_2560_2_100_Dorf_BloomOff_Vorschau.jpg)

[Datei öffnen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/VEQ1_Review_2560_2_100_Dorf_BloomOff_Vorschau.jpg)

**Wald – zwei Schattenstrahlen**

![Wald – zwei Schattenstrahlen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/VEQ1_Review_2560_2_100_Wald_VSMRayCount2_Vorschau.jpg)

[Datei öffnen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/VEQ1_Review_2560_2_100_Wald_VSMRayCount2_Vorschau.jpg)

**Player und NPCs – Lumen2, native Details**

![Player und NPCs – Lumen2, native Details](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/VEQ1_Review_2560_2_100_NPCWald_LumenIntegrate2_NPC_Detail.png)

[Datei öffnen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/VEQ1_Review_2560_2_100_NPCWald_LumenIntegrate2_NPC_Detail.png)

**Weg – Schatten2**

![Weg – Schatten2](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/VEQ1_Review_2560_1_75_Weg_VSMRayCount2_Vorschau.jpg)

[Datei öffnen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/VEQ1_Review_2560_1_75_Weg_VSMRayCount2_Vorschau.jpg)

**Kronenschatten – native Pixel, sichtbare Körnung**

![Kronenschatten – native Pixel, sichtbare Körnung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/InitialVisualReview/Shadow2_NativeCrop.png)

[Datei öffnen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/InitialVisualReview/Shadow2_NativeCrop.png)

**Gehdetail – Motion Blur an/aus**

![Gehdetail – Motion Blur an/aus](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/InitialVisualReview/MotionBlur_Gehdetail.png)

[Datei öffnen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/InitialVisualReview/MotionBlur_Gehdetail.png)

Zusätzlich je 13 zeitlich geordnete QHD-Gehbilder für Kontrolle und MotionBlurOff. Gleiches Enhanced-Input-Protokoll, aber keine pixelgenauen Posen: im betrachteten Frame etwa 28 cm Positionsabweichung, beide Geschwindigkeiten 210 cm/s. **Keine kontinuierliche Videoabnahme**. Diese Begleit-Probes wurden absichtlich vor dem eigentlichen Timingfenster gestoppt; deren „Cancelled“ ist kein Fehlschlag der 648 regulären Segmente.

Visuelle Bewertung: Bewegungsunschärfe aus verbessert die Schärfe des vorbeiziehenden Bodens. Tageslicht-Bloom aus verändert die Komposition wenig. Lumen2 bleibt makroskopisch nahe der Kontrolle, feinere Normal-/Kontaktdetails können nachlassen. Zwei Schattenstrahlen zeigen in QHD zusätzliche Körnung; Standbilder beweisen keine vollständige Freiheit von temporalem Flimmern. Kronen bleiben dicht, Wege und Gebäudekonturen erhalten. Im geprüften Reveal-Loch bleibt der Player sichtbar, allerdings dunkel; dunkle Figuren im Wald, fleckiger Boden, einfache Topfpflanzen und der braune Würfel am Heilhaus sind bestehende, hier bewusst nicht bearbeitete Qualitätsprobleme.

[Alle 52 Vergleichsanordnungen und Quellpfade](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Comparisons/Comparisons.json); [Unveränderte native Originalbilder und SHA-256-Nachweis](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/EvidenceManifest.json).

## 8. Gameplay-Abnahme und Spielstand

Realer eingebetteter PIE-Fußlauf: **bestanden**, 100 protokollierte Schritte, **264,32 m**, 174,97 Spielsekunden / 195,32 Wall-Sekunden, keine Test-Teleports. Enhanced Input bewegt den echten CharacterMovement-Player; Interaktionen/Kampf/Menü über vorhandene öffentliche Spiel-APIs. Das ist keine Hardware-Controller-Abnahme. Die normale Relocation des Heilhauses wird selbstverständlich weiterhin vom Spiel ausgeführt.

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Acht Richtungen / diagonale Bewegung / Anhalten | bestanden, maximal 210 cm/s, keine neue Kollision im Parcours |
| Wanderer / Dialog / Talkblend / Sprite-Fallback | bestanden, bestehende NPC-Identität und Präsentation erhalten |
| Wildbegegnung / Fang / Team | CAPTURED, anschließend drei Teamkreaturen |
| Liora / Kampf | VICTORY, Trainer-defeated-Flag gesetzt |
| Archiv / Quest / Rückkehrdialog | Abschlussflag und geänderter Dialog bestätigt |
| Menü / Eingabesperre | vor und nach Rundweg korrekt freigegeben |
| Save/Load | HP/PP und Spielfortschritt erhalten |
| Heilhaus / Cutaway / Relocation | gerade und diagonal hinein/hinaus, Dach/Vorderwand aus, außen restauriert |
| Heilerin / Checkpoint | HP/PP voll, Checkpoint VisualV2_HealingHouse gespeichert |
| Wald / Kronenfreistellung / Brücke | durchlaufen, Figur im geprüften Kronenausschnitt sichtbar |
| Sprint / Hardwarecontroller | Sprint im Fußlauf nicht eigens ausgelöst; vorhandene Sprint-Automation separat bestanden. Kein physischer Controller geprüft. |

Vier Renderingfaktoren während dieses Fußlaufs kombiniert, ausschließlich als Funktionsregression. **Keine kombinierte Performance daraus abgeleitet.** Nach Ende alle Laufzeitwerte und Prioritäten restauriert; Editor regulär geschlossen.

Im schlanken Worktree existierte vor Tests kein Dev-Spielstand. Der neu erzeugte Testslot wurde verlustfrei als `Saved/VisualV2EnvironmentQualityV1/DevSaveTestResult.sav` erhalten und aus dem regulären Slotpfad verschoben; vorheriger Zustand „kein Slot“ wiederhergestellt. Kein ursprünglicher Dev-Spielstand überschrieben, kein Zugriff auf den Vollbackup-Slot.

[Fußlaufprotokoll](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/Data/FootTest.json)

[Wiederhergestellter Spielstandzustand](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/Data/SaveRestored.json)

[Innenraumaufnahme](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/FootScreenshots/Native_Innenraum00000.png)

[Kronenfreistellung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/FootScreenshots/Native_CrownReveal_On00000.png)

## 9. Build, Automation und Map Checks

- **Mac Development Editor Build: erfolgreich**, Exit 0. Target aktuell, 0 Compile-Aktionen; kein C++ geändert. Kein behaupteter vollständiger Clean-Rebuild.
- **48/48 PokeMonster-Automationstests erfolgreich**, 0 failed, 0 notRun, 0 inProcess, 0 succeededWithWarnings. Frischer NullRHI-Prozess; Renderingqualität dadurch nicht abgenommen.
- **8/8 DevelopmentEvidence-Sicherheitstests erfolgreich** (fehlende erforderliche/optionale Dateien, beschädigte Archive, Pfadausbruch usw.).
- **Map Check Quelle und neue Karte: 0 Fehler / 0 Warnungen**, vor und nach Fußlauf. Das ist keine Behauptung eines warnungsfreien Engine-Logs.
- Matrixvalidierung: alle 12 Pläne vollständig, 648 Framezeitsegmente, 144 Faktorvergleiche, verifizierte Auflösungen/Kamera und mindestens 20 Samples je Segment.

Im frischen Automationlog stehen 25 externe Bootstrap-/Umgebungsmeldungen: 17 generische „Condition failed“ bei Frame 0 vor Projekt-Testbeginn, sechs idevice_id-/Bad-CPU-Startwarnungen, ein MCP-Lizenzhinweis und eine Layoutmigration. Nicht unterdrückt und nicht als bestandene Fehlerfreiheit ausgegeben; alle strukturierten PokeMonster-Ergebnisse dennoch Success. Die Bootstrap-Ursache wurde nicht in diesem Renderauftrag repariert. Reguläre Laufzeitlogs enthalten zudem bekannte Engine-/Audio-/MotionVector-Hinweise. Einzelne anfängliche MCP-Abfragen liefen in Timeouts; keine fehlgeschlagene Abfrage als bestandenen Audit gewertet. Der abschließende Kartenvergleich ist vollständig erfolgreich.

[Buildlog](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Build.log)

[Automation-Ergebnis](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/AutomationResult.json)

[Automationbericht](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Automation/index.json)

[Automationlog einschließlich Startmeldungen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Automation.log)

[Nachweis-Sicherheitstests](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/EvidenceSafetyTests.log)

[Map-Check-Log](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/EditorLive.log)

## 10. Grenzen und nächste konkrete Schritte

1. Keine automatische Baselinefreigabe. Zunächst Harrys Bildprüfung, insbesondere QHD-Schattenkörnung. Keine Vegetation ausdünnen oder Geometrie ändern, um diese kleinen Gewinne größer erscheinen zu lassen.
2. Motion Blur/Bloom später lokal außen umsetzen, Innenvolumes schützen und neu testen; diese Quality-CVar-Messungen sind keine exakten PP-Volume-Benchmarks.
3. Lumen2 nur bei High aktivem Screen-Probe-Pfad in Betracht ziehen. Keine Übernahme der EnvironmentPerfV2/V3-Gather-/Lichtänderungen.
4. Finale Kombination erneut eigenständig benchmarken, längere thermisch vergleichbare Laufzeiten und möglichst paketierter Development-/Shipping-Stand. Keine 60-FPS-Garantie aus achtsekündigen Samples.
5. Vor künftigen Standalone-Profilings CSV-Schreibabschluss vor Quit absichern. Die sechs fehlenden GPU-Endkontrollen nicht durch Schätzwerte ersetzen.
6. Game-/Render-/GPU-Zeiten sind getrennte Beobachtungen; große Unaccounted-Anteile und mögliches Presentation-Limit erfordern bei weiterer Optimierung einen gezielten Metal-Capture. Keine erfundene Draw-Call-/Overdraw-Kausalanalyse.
7. Dunkle Figuren, einfache Props und Boden-/Blattwiederholung benötigen einen eigenen Artauftrag; dieses Experiment verändert sie nicht.

## 11. Neue Dateien und Nachweisablage

Nur eine neue Map, neue auftragsspezifische Mess-/Reviewwerkzeuge und dieser Bericht im schlanken Worktree. Bestehende Source-, Config-, Docs-, Asset- und Mapdateien bytegleich. Keine Änderungen an TECHNIK oder ENTSCHEIDUNGEN als vermeintliche neue Standardfreigabe.

Große Nachweise außerhalb des Repositorys:
`/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17`.

144 Nachweisdateien SHA-256-verifiziert kopiert, 795 Rohdateneinträge in RawMeasurements.zip; alle Saved-Quelldateien erhalten. Keine Nachweisvideos/Bilder automatisch in Git aufgenommen.

[Rohmessungen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/RawMeasurements.zip); [Vollständige Datentabellen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/Evidence/Data/VOLLSTAENDIGE_MESSWERTE.md).

Neue Projektdateien (vollständige Liste; nichts gestaged):

```text
Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap
Tools/VisualV2EnvironmentQualityV1/AfterFoot.py
Tools/VisualV2EnvironmentQualityV1/Analyze.py
Tools/VisualV2EnvironmentQualityV1/ArchiveEvidence.py
Tools/VisualV2EnvironmentQualityV1/AuditMaps.py
Tools/VisualV2EnvironmentQualityV1/CloseEditor.py
Tools/VisualV2EnvironmentQualityV1/Compose.py
Tools/VisualV2EnvironmentQualityV1/Control.py
Tools/VisualV2EnvironmentQualityV1/FootTest.py
Tools/VisualV2EnvironmentQualityV1/FormatTables.py
Tools/VisualV2EnvironmentQualityV1/MCPClient.py
Tools/VisualV2EnvironmentQualityV1/Monitor.py
Tools/VisualV2EnvironmentQualityV1/MotionReview.py
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_1.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_2.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_3.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_4.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_5.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_6.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_1.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_2.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_3.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_4.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_5.tsv
Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_6.tsv
Tools/VisualV2EnvironmentQualityV1/Preset.py
Tools/VisualV2EnvironmentQualityV1/README.md
Tools/VisualV2EnvironmentQualityV1/ReviewShots.py
Tools/VisualV2EnvironmentQualityV1/RunFoot.py
Tools/VisualV2EnvironmentQualityV1/RunMotionReview.py
Tools/VisualV2EnvironmentQualityV1/RunPIE.py
Tools/VisualV2EnvironmentQualityV1/RunReview.py
Tools/VisualV2EnvironmentQualityV1/RunStandalone.py
Tools/VisualV2EnvironmentQualityV1/StartFoot.py
Tools/VisualV2EnvironmentQualityV1/StartProbe.py
Tools/VisualV2EnvironmentQualityV1/Startup.py
Tools/VisualV2EnvironmentQualityV1/Summarize.py
Docs/VISUALV2_ENVIRONMENT_QUALITY_V1_PRUEFBERICHT.md
```

## 12. Git-Abschluss

HEADs und Backup-Ref unverändert. Vollbackup-Arbeitsbaum sauber. Slim enthält ausschließlich die oben aufgeführten neuen Dateien; keine vorgemerkten Änderungen. `git diff --check` erfolgreich; zusätzlich alle neuen Textdateien separat auf Whitespace geprüft, da unversionierte Dateien vom normalen Diff nicht erfasst werden. Der abschließende vollständige Status liegt beim Bericht. **Kein Commit, kein Push, keine Baseline-Übernahme, keine Datei gelöscht.**

[Finaler Git-/Whitespace-Status](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17/FinalGitCheck.json).

## Anhang – sämtliche Einzelfaktorwerte

Vollständige Einzelfaktor-Ergebnisse

A = Mittel der flankierenden Kontrollmediane pro Wiederholung; B = Einzelmaßnahme. Tabellenwerte sind anschließend Mediane der drei Wiederholungen. Zeiten in ms. Delta-Spanne nennt alle drei Framezeit-Differenzen B−A als Min/Max; negativ ist schneller. P95 ist der Median der wiederholungsbezogenen P95-Werte, kein gepooltes Gesamt-P95. GPU-Pässe nicht addieren. Fehlende bzw. konstante Nullzähler erscheinen als —.

### MotionBlurOff

| Modus | Ausgabe / Qualität / % | Ort | FPS A → B | Frame A → B | P95 A → B | GPU A → B | ShadowProjection A → B | ShadowDepths A → B | ΔFrame Min … Max |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75 | Dorf | 49.72 → 50.77 | 20.11 → 19.70 | 25.65 → 25.41 | 19.30 → 19.02 | 0.57 → 0.57 | 1.37 → 1.36 | -0.45 … 0.10 |
| PIE | 1280×720 / Medium / 75 | Wald | 50.10 → 48.39 | 19.96 → 20.66 | 25.41 → 25.95 | 19.28 → 19.55 | 0.58 → 0.58 | 1.36 → 1.34 | -0.31 … 0.87 |
| PIE | 1280×720 / Medium / 75 | Weg | 45.82 → 46.31 | 21.83 → 21.60 | 27.22 → 26.54 | 21.01 → 20.71 | 0.64 → 0.63 | 1.24 → 1.24 | -0.73 … 0.07 |
| PIE | 1280×720 / Medium / 100 | Dorf | 33.59 → 33.97 | 29.77 → 29.44 | 32.32 → 32.21 | 29.06 → 28.68 | 1.06 → 1.06 | 1.48 → 1.49 | -0.78 … 0.11 |
| PIE | 1280×720 / Medium / 100 | Wald | 33.80 → 34.64 | 29.59 → 28.87 | 32.47 → 32.17 | 28.74 → 28.04 | 1.06 → 1.05 | 1.54 → 1.53 | -0.79 … -0.61 |
| PIE | 1280×720 / Medium / 100 | Weg | 32.52 → 32.95 | 30.75 → 30.35 | 32.98 → 32.47 | 29.95 → 29.59 | 1.14 → 1.14 | 1.40 → 1.39 | -0.47 … -0.40 |
| PIE | 2560×1440 / Medium / 75 | Dorf | 19.93 → 20.39 | 50.17 → 49.03 | 54.42 → 51.02 | 49.30 → 48.11 | 2.62 → 2.54 | 1.83 → 1.83 | -1.45 … -0.64 |
| PIE | 2560×1440 / Medium / 75 | Wald | 19.83 → 20.30 | 50.43 → 49.26 | 55.33 → 51.28 | 49.36 → 48.09 | 2.82 → 2.73 | 1.91 → 1.92 | -1.23 … -0.75 |
| PIE | 2560×1440 / Medium / 75 | Weg | 19.53 → 19.82 | 51.22 → 50.46 | 57.22 → 56.24 | 50.42 → 49.86 | 2.94 → 2.98 | 1.75 → 1.73 | -1.06 … -0.18 |
| PIE | 2560×1440 / Medium / 100 | Dorf | 13.45 → 13.88 | 74.38 → 72.07 | 82.55 → 79.71 | 73.62 → 71.25 | 6.60 → 6.36 | 2.34 → 2.30 | -4.63 … -2.31 |
| PIE | 2560×1440 / Medium / 100 | Wald | 13.32 → 14.00 | 75.06 → 71.41 | 90.21 → 79.38 | 73.24 → 70.68 | 6.82 → 6.90 | 2.57 → 2.54 | -3.65 … -1.46 |
| PIE | 2560×1440 / Medium / 100 | Weg | 13.20 → 13.74 | 75.78 → 72.78 | 81.41 → 79.45 | 74.27 → 71.55 | 7.57 → 7.40 | 2.29 → 2.27 | -4.49 … -3.00 |
| PIE | 2560×1440 / High / 75 | Dorf | 14.75 → 14.96 | 67.81 → 66.86 | 77.51 → 74.37 | 65.63 → 64.59 | 4.22 → 4.07 | 2.04 → 2.03 | -1.64 … 0.12 |
| PIE | 2560×1440 / High / 75 | Wald | 14.89 → 15.07 | 67.18 → 66.34 | 76.09 → 72.77 | 64.91 → 64.10 | 5.78 → 4.31 | 2.13 → 2.12 | -1.58 … -0.24 |
| PIE | 2560×1440 / High / 75 | Weg | 14.52 → 14.55 | 68.89 → 68.75 | 75.43 → 80.70 | 67.10 → 66.87 | 7.25 → 5.08 | 1.89 → 1.91 | -1.94 … 0.13 |
| PIE | 2560×1440 / High / 100 | Dorf | 9.98 → 10.18 | 100.22 → 98.27 | 109.29 → 112.04 | 97.17 → 95.02 | 12.50 → 12.52 | 2.51 → 2.51 | -2.14 … -1.38 |
| PIE | 2560×1440 / High / 100 | Wald | 9.98 → 10.19 | 100.24 → 98.12 | 112.91 → 113.06 | 97.30 → 95.19 | 12.76 → 12.64 | 2.70 → 2.76 | -3.45 … 0.88 |
| PIE | 2560×1440 / High / 100 | Weg | 9.82 → 10.02 | 101.87 → 99.82 | 111.29 → 113.91 | 99.08 → 97.34 | 13.36 → 13.29 | 2.39 → 2.38 | -2.55 … -1.92 |
| Standalone | 1280×720 / Medium / 75 | Dorf | 60.02 → 60.00 | 16.66 → 16.67 | 17.01 → 17.38 | 13.01 → 13.13 | 0.56 → 0.60 | 1.32 → 1.37 | -0.00 … 0.01 |
| Standalone | 1280×720 / Medium / 75 | Wald | 59.99 → 60.02 | 16.67 → 16.66 | 17.01 → 16.97 | 12.91 → 12.96 | 0.59 → 0.59 | 1.36 → 1.38 | -0.01 … -0.00 |
| Standalone | 1280×720 / Medium / 75 | Weg | 60.03 → 60.05 | 16.66 → 16.65 | 17.03 → 17.10 | — → 12.85 | — → 0.59 | — → 1.12 | -0.01 … -0.00 |
| Standalone | 1280×720 / Medium / 100 | Dorf | 54.50 → 54.48 | 18.35 → 18.36 | 20.42 → 20.74 | 17.24 → 17.20 | 1.11 → 1.11 | 1.49 → 1.50 | -0.87 … 0.06 |
| Standalone | 1280×720 / Medium / 100 | Wald | 56.95 → 57.95 | 17.56 → 17.26 | 19.40 → 19.07 | 16.65 → 16.46 | 1.10 → 1.09 | 1.54 → 1.53 | -0.48 … -0.23 |
| Standalone | 1280×720 / Medium / 100 | Weg | 53.61 → 54.56 | 18.65 → 18.33 | 20.61 → 20.31 | — → 17.30 | — → 1.17 | — → 1.39 | -0.37 … -0.17 |
| Standalone | 2560×1440 / Medium / 75 | Dorf | 30.71 → 31.36 | 32.56 → 31.89 | 34.30 → 33.56 | 31.33 → 30.64 | 2.62 → 2.64 | 1.87 → 1.84 | -1.75 … -0.19 |
| Standalone | 2560×1440 / Medium / 75 | Wald | 31.72 → 32.87 | 31.52 → 30.42 | 33.30 → 32.11 | 30.31 → 29.25 | 2.64 → 2.64 | 1.87 → 1.86 | -1.22 … -0.84 |
| Standalone | 2560×1440 / Medium / 75 | Weg | 30.38 → 31.23 | 32.92 → 32.02 | 35.07 → 34.37 | — → 30.74 | — → 2.82 | — → 1.67 | -1.02 … -0.34 |
| Standalone | 2560×1440 / Medium / 100 | Dorf | 20.94 → 21.47 | 47.75 → 46.58 | 49.98 → 49.00 | 46.20 → 45.03 | 4.56 → 4.54 | 2.30 → 2.31 | -1.97 … -1.02 |
| Standalone | 2560×1440 / Medium / 100 | Wald | 21.51 → 22.09 | 46.49 → 45.26 | 49.06 → 47.79 | 45.08 → 43.72 | 4.56 → 4.54 | 2.50 → 2.49 | -1.55 … -1.01 |
| Standalone | 2560×1440 / Medium / 100 | Weg | 20.80 → 21.29 | 48.08 → 46.98 | 51.51 → 48.97 | — → 45.30 | — → 4.76 | — → 2.30 | -1.51 … -0.91 |
| Standalone | 2560×1440 / High / 75 | Dorf | 23.54 → 23.94 | 42.49 → 41.76 | 44.27 → 43.75 | 40.43 → 39.73 | 3.86 → 3.91 | 1.91 → 1.91 | -1.03 … -0.49 |
| Standalone | 2560×1440 / High / 75 | Wald | 24.00 → 24.76 | 41.67 → 40.39 | 44.34 → 42.45 | 39.64 → 38.40 | 4.01 → 3.95 | 1.98 → 1.94 | -1.28 … -0.61 |
| Standalone | 2560×1440 / High / 75 | Weg | 22.87 → 23.39 | 43.73 → 42.75 | 46.71 → 44.71 | — → 40.67 | — → 4.51 | — → 1.75 | -1.30 … -0.38 |
| Standalone | 2560×1440 / High / 100 | Dorf | 15.86 → 16.20 | 63.07 → 61.72 | 65.81 → 65.16 | 61.48 → 60.40 | 7.08 → 7.06 | 2.39 → 2.40 | -2.58 … -1.35 |
| Standalone | 2560×1440 / High / 100 | Wald | 16.06 → 16.02 | 62.27 → 62.41 | 68.22 → 72.99 | 60.71 → 60.78 | 7.16 → 7.29 | 2.61 → 2.65 | -1.86 … 1.66 |
| Standalone | 2560×1440 / High / 100 | Weg | 15.65 → 15.71 | 63.88 → 63.65 | 68.28 → 66.32 | — → 62.26 | — → 7.99 | — → 2.32 | -0.82 … 1.47 |

### BloomOff

| Modus | Ausgabe / Qualität / % | Ort | FPS A → B | Frame A → B | P95 A → B | GPU A → B | ShadowProjection A → B | ShadowDepths A → B | ΔFrame Min … Max |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75 | Dorf | 49.72 → 50.45 | 20.11 → 19.82 | 25.65 → 25.25 | 19.30 → 19.04 | 0.57 → 0.57 | 1.37 → 1.38 | -0.29 … -0.13 |
| PIE | 1280×720 / Medium / 75 | Wald | 50.10 → 49.23 | 19.96 → 20.31 | 25.41 → 25.25 | 19.28 → 19.28 | 0.58 → 0.59 | 1.36 → 1.38 | -0.40 … 0.40 |
| PIE | 1280×720 / Medium / 75 | Weg | 45.82 → 46.08 | 21.83 → 21.70 | 27.22 → 27.00 | 21.01 → 20.61 | 0.64 → 0.65 | 1.24 → 1.24 | -0.62 … 0.02 |
| PIE | 1280×720 / Medium / 100 | Dorf | 33.59 → 33.50 | 29.77 → 29.85 | 32.32 → 32.34 | 29.06 → 29.20 | 1.06 → 1.06 | 1.48 → 1.49 | -0.65 … 0.25 |
| PIE | 1280×720 / Medium / 100 | Wald | 33.80 → 34.42 | 29.59 → 29.05 | 32.47 → 32.28 | 28.74 → 28.26 | 1.06 → 1.06 | 1.54 → 1.54 | -0.55 … -0.46 |
| PIE | 1280×720 / Medium / 100 | Weg | 32.52 → 32.95 | 30.75 → 30.35 | 32.98 → 32.71 | 29.95 → 29.59 | 1.14 → 1.15 | 1.40 → 1.39 | -0.50 … -0.21 |
| PIE | 2560×1440 / Medium / 75 | Dorf | 19.93 → 19.98 | 50.17 → 50.06 | 54.42 → 55.81 | 49.30 → 49.06 | 2.62 → 2.67 | 1.83 → 1.87 | -0.42 … 0.35 |
| PIE | 2560×1440 / Medium / 75 | Wald | 19.83 → 20.07 | 50.43 → 49.83 | 55.33 → 52.17 | 49.36 → 49.04 | 2.82 → 2.82 | 1.91 → 1.88 | -0.77 … 1.09 |
| PIE | 2560×1440 / Medium / 75 | Weg | 19.53 → 19.64 | 51.22 → 50.93 | 57.22 → 57.18 | 50.42 → 50.15 | 2.94 → 2.97 | 1.75 → 1.78 | -0.42 … 0.92 |
| PIE | 2560×1440 / Medium / 100 | Dorf | 13.45 → 13.40 | 74.38 → 74.61 | 82.55 → 80.28 | 73.62 → 73.07 | 6.60 → 6.42 | 2.34 → 2.32 | -3.00 … 1.42 |
| PIE | 2560×1440 / Medium / 100 | Wald | 13.32 → 13.69 | 75.06 → 73.03 | 90.21 → 79.90 | 73.24 → 71.93 | 6.82 → 6.42 | 2.57 → 2.57 | -2.03 … -0.20 |
| PIE | 2560×1440 / Medium / 100 | Weg | 13.20 → 13.31 | 75.78 → 75.11 | 81.41 → 80.84 | 74.27 → 73.29 | 7.57 → 6.79 | 2.29 → 2.28 | -3.05 … -0.16 |
| PIE | 2560×1440 / High / 75 | Dorf | 14.75 → 14.80 | 67.81 → 67.57 | 77.51 → 78.06 | 65.63 → 65.54 | 4.22 → 4.27 | 2.04 → 2.06 | -0.88 … 0.17 |
| PIE | 2560×1440 / High / 75 | Wald | 14.89 → 15.20 | 67.18 → 65.78 | 76.09 → 70.17 | 64.91 → 63.83 | 5.78 → 4.24 | 2.13 → 2.10 | -1.51 … -0.18 |
| PIE | 2560×1440 / High / 75 | Weg | 14.52 → 14.65 | 68.89 → 68.27 | 75.43 → 74.71 | 67.10 → 66.25 | 7.25 → 5.41 | 1.89 → 1.89 | -2.08 … 0.16 |
| PIE | 2560×1440 / High / 100 | Dorf | 9.98 → 10.17 | 100.22 → 98.34 | 109.29 → 107.13 | 97.17 → 95.50 | 12.50 → 12.48 | 2.51 → 2.50 | -2.25 … 0.60 |
| PIE | 2560×1440 / High / 100 | Wald | 9.98 → 10.22 | 100.24 → 97.85 | 112.91 → 104.47 | 97.30 → 95.47 | 12.76 → 12.60 | 2.70 → 2.69 | -3.60 … 1.08 |
| PIE | 2560×1440 / High / 100 | Weg | 9.82 → 9.95 | 101.87 → 100.51 | 111.29 → 106.03 | 99.08 → 97.54 | 13.36 → 13.37 | 2.39 → 2.39 | -2.28 … -1.36 |
| Standalone | 1280×720 / Medium / 75 | Dorf | 60.02 → 60.03 | 16.66 → 16.66 | 17.01 → 17.07 | 13.01 → 15.81 | 0.56 → 0.60 | 1.32 → 1.42 | -0.01 … 0.00 |
| Standalone | 1280×720 / Medium / 75 | Wald | 59.99 → 60.00 | 16.67 → 16.67 | 17.01 → 17.03 | 12.91 → 15.78 | 0.59 → 0.66 | 1.36 → 1.45 | -0.00 … 0.03 |
| Standalone | 1280×720 / Medium / 75 | Weg | 60.03 → 59.99 | 16.66 → 16.67 | 17.03 → 16.99 | — → 15.79 | — → 0.64 | — → 1.23 | 0.00 … 0.02 |
| Standalone | 1280×720 / Medium / 100 | Dorf | 54.50 → 55.39 | 18.35 → 18.05 | 20.42 → 19.67 | 17.24 → 17.05 | 1.11 → 1.12 | 1.49 → 1.51 | -0.76 … -0.18 |
| Standalone | 1280×720 / Medium / 100 | Wald | 56.95 → 58.13 | 17.56 → 17.20 | 19.40 → 18.97 | 16.65 → 16.24 | 1.10 → 1.11 | 1.54 → 1.56 | -0.49 … -0.31 |
| Standalone | 1280×720 / Medium / 100 | Weg | 53.61 → 54.98 | 18.65 → 18.19 | 20.61 → 20.45 | — → 16.98 | — → 1.19 | — → 1.40 | -0.49 … -0.39 |
| Standalone | 2560×1440 / Medium / 75 | Dorf | 30.71 → 31.17 | 32.56 → 32.08 | 34.30 → 34.05 | 31.33 → 30.87 | 2.62 → 2.63 | 1.87 → 1.83 | -1.23 … 0.27 |
| Standalone | 2560×1440 / Medium / 75 | Wald | 31.72 → 32.55 | 31.52 → 30.72 | 33.30 → 32.76 | 30.31 → 29.65 | 2.64 → 2.62 | 1.87 → 1.86 | -0.81 … -0.37 |
| Standalone | 2560×1440 / Medium / 75 | Weg | 30.38 → 30.93 | 32.92 → 32.33 | 35.07 → 34.66 | — → 31.07 | — → 2.74 | — → 1.66 | -0.80 … 0.03 |
| Standalone | 2560×1440 / Medium / 100 | Dorf | 20.94 → 21.19 | 47.75 → 47.19 | 49.98 → 49.02 | 46.20 → 45.63 | 4.56 → 4.53 | 2.30 → 2.30 | -1.11 … -0.56 |
| Standalone | 2560×1440 / Medium / 100 | Wald | 21.51 → 21.90 | 46.49 → 45.67 | 49.06 → 48.13 | 45.08 → 44.20 | 4.56 → 4.50 | 2.50 → 2.50 | -1.13 … 0.03 |
| Standalone | 2560×1440 / Medium / 100 | Weg | 20.80 → 21.09 | 48.08 → 47.41 | 51.51 → 49.57 | — → 45.94 | — → 4.82 | — → 2.26 | -1.03 … -0.06 |
| Standalone | 2560×1440 / High / 75 | Dorf | 23.54 → 24.08 | 42.49 → 41.53 | 44.27 → 44.20 | 40.43 → 39.44 | 3.86 → 3.86 | 1.91 → 1.91 | -1.03 … 0.42 |
| Standalone | 2560×1440 / High / 75 | Wald | 24.00 → 24.14 | 41.67 → 41.42 | 44.34 → 45.18 | 39.64 → 39.26 | 4.01 → 4.19 | 1.98 → 2.02 | -0.50 … 1.78 |
| Standalone | 2560×1440 / High / 75 | Weg | 22.87 → 22.86 | 43.73 → 43.74 | 46.71 → 52.87 | — → 41.49 | — → 4.81 | — → 1.83 | -0.84 … 0.47 |
| Standalone | 2560×1440 / High / 100 | Dorf | 15.86 → 16.19 | 63.07 → 61.75 | 65.81 → 64.49 | 61.48 → 60.52 | 7.08 → 7.03 | 2.39 → 2.41 | -1.45 … -0.88 |
| Standalone | 2560×1440 / High / 100 | Wald | 16.06 → 16.42 | 62.27 → 60.90 | 68.22 → 65.00 | 60.71 → 59.67 | 7.16 → 6.99 | 2.61 → 2.65 | -1.61 … -0.97 |
| Standalone | 2560×1440 / High / 100 | Weg | 15.65 → 15.68 | 63.88 → 63.80 | 68.28 → 85.14 | — → 62.19 | — → 7.92 | — → 2.36 | -0.89 … 0.68 |

### VSMRayCount2

| Modus | Ausgabe / Qualität / % | Ort | FPS A → B | Frame A → B | P95 A → B | GPU A → B | ShadowProjection A → B | ShadowDepths A → B | ΔFrame Min … Max |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75 | Dorf | 49.72 → 50.28 | 20.11 → 19.89 | 25.65 → 25.66 | 19.30 → 19.15 | 0.57 → 0.50 | 1.37 → 1.37 | -0.22 … -0.05 |
| PIE | 1280×720 / Medium / 75 | Wald | 50.10 → 49.69 | 19.96 → 20.12 | 25.41 → 25.21 | 19.28 → 19.22 | 0.58 → 0.50 | 1.36 → 1.36 | -0.13 … 0.35 |
| PIE | 1280×720 / Medium / 75 | Weg | 45.82 → 45.97 | 21.83 → 21.75 | 27.22 → 26.72 | 21.01 → 20.91 | 0.64 → 0.52 | 1.24 → 1.24 | -0.56 … 0.00 |
| PIE | 1280×720 / Medium / 100 | Dorf | 33.59 → 33.68 | 29.77 → 29.69 | 32.32 → 32.15 | 29.06 → 29.00 | 1.06 → 0.93 | 1.48 → 1.49 | -0.40 … 0.61 |
| PIE | 1280×720 / Medium / 100 | Wald | 33.80 → 34.15 | 29.59 → 29.28 | 32.47 → 32.47 | 28.74 → 28.47 | 1.06 → 0.93 | 1.54 → 1.54 | -0.45 … 0.36 |
| PIE | 1280×720 / Medium / 100 | Weg | 32.52 → 32.75 | 30.75 → 30.54 | 32.98 → 32.69 | 29.95 → 29.68 | 1.14 → 0.97 | 1.40 → 1.40 | -0.38 … -0.02 |
| PIE | 2560×1440 / Medium / 75 | Dorf | 19.93 → 20.09 | 50.17 → 49.79 | 54.42 → 52.76 | 49.30 → 49.05 | 2.62 → 2.26 | 1.83 → 1.81 | -0.39 … -0.14 |
| PIE | 2560×1440 / Medium / 75 | Wald | 19.83 → 20.12 | 50.43 → 49.70 | 55.33 → 52.44 | 49.36 → 48.61 | 2.82 → 2.47 | 1.91 → 1.88 | -0.73 … -0.40 |
| PIE | 2560×1440 / Medium / 75 | Weg | 19.53 → 19.75 | 51.22 → 50.63 | 57.22 → 56.88 | 50.42 → 49.74 | 2.94 → 2.56 | 1.75 → 1.72 | -0.72 … -0.56 |
| PIE | 2560×1440 / Medium / 100 | Dorf | 13.45 → 13.24 | 74.38 → 75.54 | 82.55 → 85.61 | 73.62 → 73.16 | 6.60 → 6.08 | 2.34 → 2.38 | 1.15 … 5.03 |
| PIE | 2560×1440 / Medium / 100 | Wald | 13.32 → 13.86 | 75.06 → 72.14 | 90.21 → 80.14 | 73.24 → 70.86 | 6.82 → 6.22 | 2.57 → 2.53 | -2.91 … 0.47 |
| PIE | 2560×1440 / Medium / 100 | Weg | 13.20 → 13.62 | 75.78 → 73.45 | 81.41 → 81.37 | 74.27 → 72.77 | 7.57 → 6.75 | 2.29 → 2.30 | -3.14 … 1.88 |
| PIE | 2560×1440 / High / 75 | Dorf | 14.75 → 15.02 | 67.81 → 66.56 | 77.51 → 74.10 | 65.63 → 64.36 | 4.22 → 2.88 | 2.04 → 2.04 | -1.37 … -1.25 |
| PIE | 2560×1440 / High / 75 | Wald | 14.89 → 15.25 | 67.18 → 65.55 | 76.09 → 69.67 | 64.91 → 63.41 | 5.78 → 2.93 | 2.13 → 2.14 | -1.79 … -0.99 |
| PIE | 2560×1440 / High / 75 | Weg | 14.52 → 14.68 | 68.89 → 68.14 | 75.43 → 77.63 | 67.10 → 66.21 | 7.25 → 3.11 | 1.89 → 1.87 | -1.83 … -0.60 |
| PIE | 2560×1440 / High / 100 | Dorf | 9.98 → 10.20 | 100.22 → 98.05 | 109.29 → 134.01 | 97.17 → 94.11 | 12.50 → 7.61 | 2.51 → 2.51 | -3.51 … 0.66 |
| PIE | 2560×1440 / High / 100 | Wald | 9.98 → 10.39 | 100.24 → 96.21 | 112.91 → 102.42 | 97.30 → 93.14 | 12.76 → 10.11 | 2.70 → 2.68 | -5.17 … -1.84 |
| PIE | 2560×1440 / High / 100 | Weg | 9.82 → 10.25 | 101.87 → 97.60 | 111.29 → 104.89 | 99.08 → 95.58 | 13.36 → 10.57 | 2.39 → 2.41 | -5.22 … -3.61 |
| Standalone | 1280×720 / Medium / 75 | Dorf | 60.02 → 60.01 | 16.66 → 16.66 | 17.01 → 17.08 | 13.01 → 13.05 | 0.56 → 0.50 | 1.32 → 1.34 | -0.00 … 0.01 |
| Standalone | 1280×720 / Medium / 75 | Wald | 59.99 → 60.01 | 16.67 → 16.66 | 17.01 → 16.98 | 12.91 → 13.27 | 0.59 → 0.52 | 1.36 → 1.41 | -0.01 … 0.01 |
| Standalone | 1280×720 / Medium / 75 | Weg | 60.03 → 60.00 | 16.66 → 16.67 | 17.03 → 17.07 | — → 12.92 | — → 0.50 | — → 1.10 | -0.00 … 0.01 |
| Standalone | 1280×720 / Medium / 100 | Dorf | 54.50 → 54.99 | 18.35 → 18.18 | 20.42 → 20.29 | 17.24 → 17.09 | 1.11 → 0.98 | 1.49 → 1.49 | -0.16 … 0.07 |
| Standalone | 1280×720 / Medium / 100 | Wald | 56.95 → 57.36 | 17.56 → 17.43 | 19.40 → 19.41 | 16.65 → 16.39 | 1.10 → 0.98 | 1.54 → 1.54 | -0.30 … 0.14 |
| Standalone | 1280×720 / Medium / 100 | Weg | 53.61 → 54.28 | 18.65 → 18.42 | 20.61 → 20.63 | — → 17.36 | — → 1.01 | — → 1.39 | -0.25 … -0.13 |
| Standalone | 2560×1440 / Medium / 75 | Dorf | 30.71 → 30.52 | 32.56 → 32.76 | 34.30 → 35.00 | 31.33 → 31.59 | 2.62 → 2.47 | 1.87 → 1.94 | -0.14 … 0.43 |
| Standalone | 2560×1440 / Medium / 75 | Wald | 31.72 → 32.05 | 31.52 → 31.20 | 33.30 → 33.92 | 30.31 → 30.02 | 2.64 → 2.40 | 1.87 → 1.88 | -0.48 … -0.30 |
| Standalone | 2560×1440 / Medium / 75 | Weg | 30.38 → 30.36 | 32.92 → 32.94 | 35.07 → 35.30 | — → 31.58 | — → 2.36 | — → 1.71 | -0.51 … 0.27 |
| Standalone | 2560×1440 / Medium / 100 | Dorf | 20.94 → 20.87 | 47.75 → 47.91 | 49.98 → 51.18 | 46.20 → 46.31 | 4.56 → 4.27 | 2.30 → 2.39 | 0.16 … 1.03 |
| Standalone | 2560×1440 / Medium / 100 | Wald | 21.51 → 21.97 | 46.49 → 45.52 | 49.06 → 48.11 | 45.08 → 44.06 | 4.56 → 4.05 | 2.50 → 2.49 | -1.28 … -0.22 |
| Standalone | 2560×1440 / Medium / 100 | Weg | 20.80 → 21.05 | 48.08 → 47.51 | 51.51 → 49.77 | — → 45.92 | — → 4.17 | — → 2.30 | -1.03 … -0.50 |
| Standalone | 2560×1440 / High / 75 | Dorf | 23.54 → 24.04 | 42.49 → 41.59 | 44.27 → 43.14 | 40.43 → 39.55 | 3.86 → 2.69 | 1.91 → 1.92 | -1.02 … 0.09 |
| Standalone | 2560×1440 / High / 75 | Wald | 24.00 → 24.98 | 41.67 → 40.04 | 44.34 → 42.07 | 39.64 → 38.10 | 4.01 → 2.75 | 1.98 → 1.96 | -1.64 … -1.09 |
| Standalone | 2560×1440 / High / 75 | Weg | 22.87 → 23.51 | 43.73 → 42.54 | 46.71 → 46.32 | — → 40.45 | — → 2.94 | — → 1.81 | -1.52 … -0.24 |
| Standalone | 2560×1440 / High / 100 | Dorf | 15.86 → 16.35 | 63.07 → 61.16 | 65.81 → 65.15 | 61.48 → 59.22 | 7.08 → 5.03 | 2.39 → 2.43 | -1.91 … -1.06 |
| Standalone | 2560×1440 / High / 100 | Wald | 16.06 → 16.33 | 62.27 → 61.23 | 68.22 → 68.25 | 60.71 → 59.58 | 7.16 → 5.20 | 2.61 → 2.63 | -2.24 … -0.91 |
| Standalone | 2560×1440 / High / 100 | Weg | 15.65 → 16.10 | 63.88 → 62.10 | 68.28 → 66.65 | — → 60.70 | — → 5.22 | — → 2.36 | -2.44 … -1.08 |

### LumenIntegrate2

| Modus | Ausgabe / Qualität / % | Ort | FPS A → B | Frame A → B | P95 A → B | GPU A → B | ShadowProjection A → B | ShadowDepths A → B | ΔFrame Min … Max |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75 | Dorf | 49.72 → 49.89 | 20.11 → 20.04 | 25.65 → 25.54 | 19.30 → 19.21 | 0.57 → 0.57 | 1.37 → 1.37 | -0.17 … 0.48 |
| PIE | 1280×720 / Medium / 75 | Wald | 50.10 → 49.42 | 19.96 → 20.23 | 25.41 → 25.75 | 19.28 → 19.39 | 0.58 → 0.58 | 1.36 → 1.37 | 0.08 … 0.28 |
| PIE | 1280×720 / Medium / 75 | Weg | 45.82 → 45.71 | 21.83 → 21.88 | 27.22 → 27.06 | 21.01 → 21.01 | 0.64 → 0.64 | 1.24 → 1.24 | 0.05 … 0.33 |
| PIE | 1280×720 / Medium / 100 | Dorf | 33.59 → 33.57 | 29.77 → 29.79 | 32.32 → 32.13 | 29.06 → 29.10 | 1.06 → 1.06 | 1.48 → 1.49 | -0.26 … 0.18 |
| PIE | 1280×720 / Medium / 100 | Wald | 33.80 → 33.78 | 29.59 → 29.60 | 32.47 → 32.88 | 28.74 → 28.85 | 1.06 → 1.05 | 1.54 → 1.54 | -0.28 … 0.11 |
| PIE | 1280×720 / Medium / 100 | Weg | 32.52 → 32.34 | 30.75 → 30.93 | 32.98 → 32.98 | 29.95 → 29.98 | 1.14 → 1.14 | 1.40 → 1.39 | 0.04 … 0.21 |
| PIE | 2560×1440 / Medium / 75 | Dorf | 19.93 → 20.04 | 50.17 → 49.90 | 54.42 → 52.39 | 49.30 → 49.08 | 2.62 → 2.55 | 1.83 → 1.83 | -0.27 … 0.89 |
| PIE | 2560×1440 / Medium / 75 | Wald | 19.83 → 20.04 | 50.43 → 49.90 | 55.33 → 52.99 | 49.36 → 49.03 | 2.82 → 2.80 | 1.91 → 1.87 | -0.53 … 0.25 |
| PIE | 2560×1440 / Medium / 75 | Weg | 19.53 → 19.43 | 51.22 → 51.46 | 57.22 → 58.01 | 50.42 → 50.76 | 2.94 → 3.00 | 1.75 → 1.76 | -0.62 … 0.57 |
| PIE | 2560×1440 / Medium / 100 | Dorf | 13.45 → 13.72 | 74.38 → 72.89 | 82.55 → 80.46 | 73.62 → 72.49 | 6.60 → 6.44 | 2.34 → 2.34 | -4.06 … 1.97 |
| PIE | 2560×1440 / Medium / 100 | Wald | 13.32 → 13.38 | 75.06 → 74.72 | 90.21 → 81.78 | 73.24 → 72.82 | 6.82 → 6.67 | 2.57 → 2.61 | -0.34 … 1.06 |
| PIE | 2560×1440 / Medium / 100 | Weg | 13.20 → 13.10 | 75.78 → 76.35 | 81.41 → 81.86 | 74.27 → 75.01 | 7.57 → 7.44 | 2.29 → 2.31 | -0.23 … 2.10 |
| PIE | 2560×1440 / High / 75 | Dorf | 14.75 → 14.91 | 67.81 → 67.06 | 77.51 → 76.61 | 65.63 → 64.92 | 4.22 → 4.25 | 2.04 → 2.05 | -1.34 … 0.96 |
| PIE | 2560×1440 / High / 75 | Wald | 14.89 → 15.25 | 67.18 → 65.59 | 76.09 → 69.38 | 64.91 → 63.44 | 5.78 → 4.20 | 2.13 → 2.11 | -1.70 … -1.11 |
| PIE | 2560×1440 / High / 75 | Weg | 14.52 → 14.37 | 68.89 → 69.58 | 75.43 → 80.76 | 67.10 → 67.46 | 7.25 → 7.23 | 1.89 → 1.89 | -1.59 … 1.13 |
| PIE | 2560×1440 / High / 100 | Dorf | 9.98 → 10.33 | 100.22 → 96.79 | 109.29 → 100.89 | 97.17 → 93.54 | 12.50 → 12.49 | 2.51 → 2.50 | -3.43 … -2.38 |
| PIE | 2560×1440 / High / 100 | Wald | 9.98 → 10.34 | 100.24 → 96.67 | 112.91 → 103.32 | 97.30 → 93.82 | 12.76 → 12.61 | 2.70 → 2.67 | -4.09 … -3.05 |
| PIE | 2560×1440 / High / 100 | Weg | 9.82 → 10.11 | 101.87 → 98.90 | 111.29 → 107.49 | 99.08 → 97.05 | 13.36 → 13.52 | 2.39 → 2.43 | -3.37 … -2.85 |
| Standalone | 1280×720 / Medium / 75 | Dorf | 60.02 → 60.03 | 16.66 → 16.66 | 17.01 → 17.14 | 13.01 → 12.89 | 0.56 → 0.56 | 1.32 → 1.31 | -0.02 … -0.00 |
| Standalone | 1280×720 / Medium / 75 | Wald | 59.99 → 59.97 | 16.67 → 16.68 | 17.01 → 17.01 | 12.91 → 13.21 | 0.59 → 0.59 | 1.36 → 1.39 | 0.00 … 0.03 |
| Standalone | 1280×720 / Medium / 75 | Weg | 60.03 → 60.00 | 16.66 → 16.67 | 17.03 → 16.99 | — → 13.41 | — → 0.60 | — → 1.12 | 0.00 … 0.01 |
| Standalone | 1280×720 / Medium / 100 | Dorf | 54.50 → 54.67 | 18.35 → 18.29 | 20.42 → 20.33 | 17.24 → 17.20 | 1.11 → 1.10 | 1.49 → 1.49 | -0.10 … 0.09 |
| Standalone | 1280×720 / Medium / 100 | Wald | 56.95 → 56.95 | 17.56 → 17.56 | 19.40 → 19.36 | 16.65 → 16.68 | 1.10 → 1.10 | 1.54 → 1.53 | -0.06 … 0.05 |
| Standalone | 1280×720 / Medium / 100 | Weg | 53.61 → 53.96 | 18.65 → 18.53 | 20.61 → 21.03 | — → 17.57 | — → 1.18 | — → 1.39 | -0.36 … 0.18 |
| Standalone | 2560×1440 / Medium / 75 | Dorf | 30.71 → 30.50 | 32.56 → 32.79 | 34.30 → 34.79 | 31.33 → 31.63 | 2.62 → 2.76 | 1.87 → 1.88 | 0.13 … 0.23 |
| Standalone | 2560×1440 / Medium / 75 | Wald | 31.72 → 31.48 | 31.52 → 31.77 | 33.30 → 33.80 | 30.31 → 30.53 | 2.64 → 2.67 | 1.87 → 1.89 | -0.07 … 0.64 |
| Standalone | 2560×1440 / Medium / 75 | Weg | 30.38 → 30.32 | 32.92 → 32.98 | 35.07 → 35.62 | — → 31.82 | — → 2.95 | — → 1.66 | -0.03 … 0.37 |
| Standalone | 2560×1440 / Medium / 100 | Dorf | 20.94 → 21.16 | 47.75 → 47.25 | 49.98 → 50.00 | 46.20 → 45.98 | 4.56 → 4.54 | 2.30 → 2.28 | -0.50 … 0.89 |
| Standalone | 2560×1440 / Medium / 100 | Wald | 21.51 → 21.82 | 46.49 → 45.83 | 49.06 → 47.98 | 45.08 → 44.34 | 4.56 → 4.48 | 2.50 → 2.47 | -0.97 … -0.51 |
| Standalone | 2560×1440 / Medium / 100 | Weg | 20.80 → 20.81 | 48.08 → 48.04 | 51.51 → 51.17 | — → 46.51 | — → 4.81 | — → 2.29 | -0.34 … 0.57 |
| Standalone | 2560×1440 / High / 75 | Dorf | 23.54 → 24.05 | 42.49 → 41.59 | 44.27 → 43.50 | 40.43 → 39.46 | 3.86 → 3.88 | 1.91 → 1.89 | -1.21 … -0.36 |
| Standalone | 2560×1440 / High / 75 | Wald | 24.00 → 24.64 | 41.67 → 40.59 | 44.34 → 42.65 | 39.64 → 38.63 | 4.01 → 4.04 | 1.98 → 1.97 | -1.55 … -0.37 |
| Standalone | 2560×1440 / High / 75 | Weg | 22.87 → 23.26 | 43.73 → 43.00 | 46.71 → 45.64 | — → 40.81 | — → 4.62 | — → 1.78 | -1.03 … -0.56 |
| Standalone | 2560×1440 / High / 100 | Dorf | 15.86 → 16.41 | 63.07 → 60.93 | 65.81 → 64.46 | 61.48 → 59.54 | 7.08 → 7.03 | 2.39 → 2.40 | -2.39 … -0.65 |
| Standalone | 2560×1440 / High / 100 | Wald | 16.06 → 16.48 | 62.27 → 60.66 | 68.22 → 64.28 | 60.71 → 59.33 | 7.16 → 7.13 | 2.61 → 2.61 | -1.70 … -1.48 |
| Standalone | 2560×1440 / High / 100 | Weg | 15.65 → 16.03 | 63.88 → 62.38 | 68.28 → 65.69 | — → 61.02 | — → 7.83 | — → 2.34 | -1.87 … -1.35 |
