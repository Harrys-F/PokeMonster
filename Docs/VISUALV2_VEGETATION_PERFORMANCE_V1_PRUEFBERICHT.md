# VisualV2 Vegetation Performance V1 – Prüfbericht

## Ergebnis und Übernahmeentscheidung

**Keine breit wirksame, belastbar nachgewiesene Vegetationsoptimierung zur Übernahme empfohlen. VisualV2 bleibt unverändert.**

Die aktuelle TAA-Szene wurde auf der **bereits vorhandenen** `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1` untersucht. **Keine neue Map und keine automatische Übernahme in VisualV2.** Die Tabellen unten sind echte neue Messungen; historische TSR-/andere-Auflösungswerte werden nicht als Vergleich verwendet.

Die Shadervereinfachung und die LOD-Diagnosen sind Versuche, keine automatisch freigegebenen Optimierungen. Eine verringerte Instruktionszahl allein ist kein GPU-Leistungsnachweis. Die konkrete Empfehlung und visuelle Bewertung stehen im Abschlussabschnitt.

## Ausgangszustand und Sicherheit

Schlanker Worktree: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`, Branch `codex/slim-backup-v5`. Ausgangs-HEAD und direkt bestätigter origin/main: `2d2200bccb6f9876b2652323304e3be72ab01553`. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b`, alter lokaler main und Archiv-Ref unverändert; Vollbackup bleibt außerhalb der Remote-Historie.

3060 vorbestehende Dateien SHA-256-geprüft; keine fehlt. Alle 17 vorhandenen Maps bytegleich, einschließlich VisualV2, GPU-Testmap, Westland, NPCMotion und Performance-Testkarten. Keine Modelle, Texturen, Spieler-/NPC-Animationen, Gameplayklassen, Configdateien oder bearbeitbaren Art-Originalquellen verändert. Einzige geänderte bestehende Projektdatei: eng begrenzte Erweiterung des expliziten Development-Performance-Probes.

Vorhandene unversionierte EnvironmentQuality-V1-Testkarte, ihr Werkzeugordner und der lokale Python-Cache bleiben unberührt und uncommittet. Blender war als vorhandener Prozess geöffnet und blieb unangetastet; keine fremde Editorsitzung verworfen. Eigene Unreal-Sitzungen nur bei leeren Dirty-Paketlisten regulär geschlossen.

## Vergleichbarkeit mit dem aktuellen TAA-Stand

Der vollständige Szenevergleich enthält 1348 Actoren auf beiden Maps. Die NPC-Source-Actor-Adresse unterscheidet sich ausschließlich durch den Mapnamen. Sonst unterscheidet sich nur der zentrale native TAA-Blendable-Eintrag. Die GPU-Testmap verwendet während der expliziten Probe temporär `r.AntiAliasingMethod=2`; in VisualV2 bleibt der globale Standard 4 mit map-lokalem TAA-Blendable. Der Renderthread bestätigt in **allen ausgewerteten Abschnitten tatsächlich Methode 2** und dieselben internen Renderer-Fractions. Kein Speichern oder Übertragen des zentralen Blendables in die Testmap.

Lichtquellen, Positionen, Intensitäten, Lichtfarben, GI/Reflexionsverfahren, Bloom, Exposure, Schattenkonfiguration und Kamera B (2850 cm / −50° / −45° / 35°) bleiben gleich. 140-cm-Player, Gehen 210 und Sprint 315 cm/s unverändert. Vollständige Licht-/Schattenflag-/Postprocess-Nachweise pro Bildpaar identisch. Die temporäre LOD-Diagnose beeinflusst die gerenderte Geometrie und damit möglicherweise feine Schattenkonturen; das wird nicht als unveränderter Produktionsschatten freigegeben.

## Vegetationsinventar

Platzierungen und LOD0-Summen sind **keine tatsächlich sichtbaren Instanz-/Dreiecks-/Draw-Call-Zahlen pro Frame**.

| Mesh | Komponenten / Platzierungen | Dreiecke je LOD | Nanite |
|---|---:|---|---|
| SM_WLA_OakAncient_V3 | 41 / 41 | 12068 / 7240 / 3621 | deaktiviert |
| SM_WLA_WildBush_V3_B | 20 / 47 | 3396 / 2038 / 1019 | deaktiviert |
| SM_WLA_WildBush_V3_A | 26 / 55 | 3284 / 1971 / 986 | deaktiviert |
| SM_WLA_Birch_A | 4 / 4 | 28628 / 17177 / 8588 | deaktiviert |
| SM_WLA_Grass_A | 1 / 175 | 576 | deaktiviert |
| SM_WLA_Fern_A | 1 / 46 | 8030 / 4818 / 2409 | deaktiviert |
| SM_WLA_Herb_A | 1 / 55 | 1152 / 634 / 288 | deaktiviert |

Erfasste LOD0-Platzierungssumme: 1.483.072 Dreiecke. Unterwuchs teilweise HISM/ISM, Reveal-Bäume eigene Komponenten. Keine Instanz entfernt oder versetzt, keine neue Culling-Grenze und keine neue Baumgeometrie. Alle erfassten Vegetationsmeshes haben Nanite deaktiviert. Ein globaler Nanite-Schalter würde andere Assets betreffen und wurde deshalb nicht als Vegetationsoptimierung ausgegeben.

## Materialien, Maskierung und Overdraw

V3-Eichen und Sträucher: Masked, Two-Sided, Alpha-Clip 0,45, derselbe Paint-Atlas und Vertexfarbmultiplikation. Kronen-Reveal besitzt zusätzlich den unveränderten Kamera→Player-Korridor und DitherTemporalAA. Birken verwenden Geometrieblätter mit vorhandenen Reveal-Materialien; sie wurden nicht in neue Masked-Karten umgewandelt. Keine neuen Materialslots oder Texturen.

Unreal-Statistik der Originalkronen: 208 Pixelshader-Instruktionen, FullyRough-Kopie 197; Strauchmaster 208 → 198. Dies sind Engine-Statistiken der abgefragten Shaderfamilie, keine pro-Pixel-GPU-Zeiten oder garantierten aktiven Metal-Kernelzahlen. Gemeldete Sampler-Nullwerte sind offensichtlich kein Beleg kostenloser Texturzugriffe. Roughness/Specular-Schattierung wird durch FullyRough vereinfacht; Alpha und Schattenmasken bleiben identisch.

Der Quelatlas hat tatsächlich 1254×1254 Pixel; der bestehende Unreal-Import streckt ihn wie bisher auf 2048×2048. Innerhalb der vorhandenen oktagonalen Karten sind je Atlasfeld etwa 46–65 % der Quellpixel über Alpha 0,45. Das ist **Alpha-Belegung, kein gemessener GPU-Overdraw**. Konservativer Hüllkonturtest mit 32 Quellpixeln Filterrand lässt je Feld etwa 86–100 % der Kartenfläche übrig. Mehr Eckpunkte/Clipping können Geometriekosten erhöhen. Keine neue Geometrie allein aus diesem theoretischen Potential erstellt.

Base Pass ist eine gemessene Gesamtstufe der Szene, nicht die isolierte Zeit aller Blattmaterialien. RHI-/Draw-Call-Nullzähler werden nicht als gültige Draw-Call-Messung verwendet. Qualitative Debugansichten beziehungsweise deren technische Nichtverfügbarkeit werden separat protokolliert; keine erfundenen Overdraw-Pixelzahlen.

## Getrennte Testvarianten

- Control: originale Szene, TAA, unveränderte Vegetation und Schatten.
- FullyRough: genau zwei separate Materialmaster, Graphen unverändert, nur Compile-Flag `fully_rough=true`. Zur Laufzeit 41 Kronen- und 46 Strauchkomponenten, zusammen 87 Slots. Dieselben Texturen/Parameter; originale Reveal-Stärke wird vom bestehenden MID gespiegelt. Zusätzlicher Test-Updateaufwand bleibt in der CPU-Messung enthalten. Kein Ersatz der produktiven Sichtfreistellung.
- TreeLOD1 / BushLOD1: vorhandene LOD1 temporär **erzwingen**, keine neue Topologie. Das ist keine Mindest-LOD-Klemme: weit entfernte Instanzen könnten vorher schon LOD2 verwenden. Deshalb weder ein allgemeiner LOD-Gewinn noch die Wirkung eines fertigen neuen LOD-Konzepts daraus ableiten.

Der Probe restauriert nach jeder Zeile und beim Stoppen Originalmaterialien, Sichtbarkeit, Schattenflags, LOD/Culling-Werte, vollständige Postprocess-Structs und CVars. Alle neuen Pfade sind auf exakte GPU-Testmap und explizite `VGB1_Vegetation_`-Labels begrenzt; Shipping ist ausgeschlossen.

### Erster getrennter Waldvergleich – PIE, QHD High 100 %

| Variante | GPU-Differenzen B−A aus drei Paaren (ms) | Median Δ GPU |
|---|---|---:|
| VegPerf:BushLOD1 | +0.563, -1.045, +0.149 | +0.149 |
| VegPerf:FullyRough | +0.697, -0.479, +2.845 | +0.697 |
| VegPerf:TreeLOD1 | +0.224, -1.319, +0.717 | +0.224 |

## Messmethode

Apple M4 / macOS / UE 5.8.2. Eingebettetes PIE und eigenständiger Development-Prozess (`UnrealEditor -game`) getrennt; kein paketierter Shipping-Build. Editor während nativer Messungen geschlossen.

Acht Konfigurationen je Modus: 1280×720 und 2560×1440, jeweils Medium/High und 75/100 %. Dorf (−4100/450/50,15), Wald (−4300/1550/50,15), Weg (−36,6/−47,1/50,15). Je Ort drei gepaarte Vergleiche, AB/BA/AB, 5 s Warm-up und 4 s Messfenster. Diese kurzen Fenster erlauben Zustandsvergleiche, keine dauerhafte 60-FPS-Garantie. NPC-Idle läuft beim Timing weiter; exakte Animationsphase nicht prozessübergreifend synchronisiert.

Ausgabeviewport, RenderTarget, Renderer-ViewRect, tatsächliche AA-Methode, aktive Fenster, Kamera und tatsächliche Renderer-Fractions geprüft. Intern 960×540 bzw. 1920×1080 bei 75 %, volle Ausgabe bei 100 %. Interne Pixelmaße aus Renderer-Fractions nach UE-Ceil-Regel, keine direkte SceneColor-Allocation-Rücklesung.

VSync=0, t.MaxFPS=0, Dynamic Resolution=0. rhi.SyncInterval bleibt unverändert 1. Engine-Durchsatz ist keine separat gemessene physische Display-Präsentationsrate. RenderThread enthält teilweise Wartezeit und ist nicht reine CPU-Arbeit. Verschachtelte GPU-Stufen nicht addieren. Shader-/Ladezeiten und separate Fotos/Videoaufnahmen nicht in reguläre Performancewerte einbezogen.

Thermische Statusverteilung: {'nominal': 51, 'fair': 529}. Energiezustände: ["Now drawing from 'AC Power'\n -InternalBattery-0 (id=23068771)\t100%; charged; 0:00 remaining present: true"]. NSProcessInfo ist keine Grad-/Taktmessung; Temperaturdrift wird durch benachbarte Paare reduziert, nicht vollständig ausgeschlossen.

Die erste PIE-C1-Gruppe wurde wegen parallel laufender CPU-Atlasanalyse vollständig aus der Endauswertung ausgeschlossen und unter CRecheck1 wiederholt. Keine Vermischung einzelner günstiger Werte. Alle Rohdateien erhalten. Ausgewertet: 288 reguläre Matrixabschnitte + 18 Scoutabschnitte = 306. Fotos und CSV-Auslauf separat.

## Vollständige neue Messmatrix – Control → FullyRough

FPS = 1000 / Median der drei Laufmediane. P95 = Median der drei Lauf-P95; alle Einzelwerte und CPU-/GPU-Stufen im JSON. Keine historischen TSR-Werte als Vorher-Vergleich.

| Modus | Ausgabe / Qualität / SP | Ort | FPS A → B | Bildzeit ms A → B | P95 ms A → B | GPU ms A → B |
|---|---|---|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75% | Dorf | 52.07 → 51.82 | 19.20 → 19.30 | 23.12 → 23.02 | 17.47 → 17.70 |
| PIE | 1280×720 / Medium / 75% | Wald | 54.69 → 54.24 | 18.28 → 18.44 | 23.43 → 22.31 | 16.81 → 16.89 |
| PIE | 1280×720 / Medium / 75% | Weg | 51.04 → 51.62 | 19.59 → 19.37 | 22.77 → 22.26 | 17.91 → 17.69 |
| PIE | 1280×720 / Medium / 100% | Dorf | 47.85 → 47.71 | 20.90 → 20.96 | 24.71 → 24.90 | 19.41 → 19.42 |
| PIE | 1280×720 / Medium / 100% | Wald | 49.65 → 49.84 | 20.14 → 20.06 | 24.26 → 24.49 | 18.94 → 18.79 |
| PIE | 1280×720 / Medium / 100% | Weg | 47.70 → 47.67 | 20.97 → 20.98 | 25.25 → 24.87 | 19.58 → 19.76 |
| PIE | 1280×720 / High / 75% | Dorf | 44.66 → 43.57 | 22.39 → 22.95 | 26.23 → 29.89 | 19.94 → 19.90 |
| PIE | 1280×720 / High / 75% | Wald | 45.73 → 45.52 | 21.87 → 21.97 | 26.77 → 26.88 | 19.24 → 19.39 |
| PIE | 1280×720 / High / 75% | Weg | 44.17 → 44.14 | 22.64 → 22.66 | 26.07 → 26.42 | 20.34 → 20.45 |
| PIE | 1280×720 / High / 100% | Dorf | 38.72 → 38.30 | 25.83 → 26.11 | 29.86 → 29.96 | 23.19 → 23.45 |
| PIE | 1280×720 / High / 100% | Wald | 39.65 → 39.75 | 25.22 → 25.16 | 29.48 → 29.00 | 22.56 → 22.27 |
| PIE | 1280×720 / High / 100% | Weg | 37.64 → 36.80 | 26.57 → 27.18 | 30.27 → 30.10 | 24.12 → 23.96 |
| PIE | 2560×1440 / Medium / 75% | Dorf | 29.72 → 29.94 | 33.65 → 33.40 | 35.34 → 35.04 | 31.98 → 31.80 |
| PIE | 2560×1440 / Medium / 75% | Wald | 30.29 → 30.54 | 33.01 → 32.74 | 35.64 → 35.14 | 31.33 → 31.59 |
| PIE | 2560×1440 / Medium / 75% | Weg | 29.67 → 29.66 | 33.70 → 33.72 | 35.48 → 35.58 | 32.24 → 32.19 |
| PIE | 2560×1440 / Medium / 100% | Dorf | 23.37 → 23.43 | 42.80 → 42.68 | 47.25 → 47.46 | 40.73 → 41.05 |
| PIE | 2560×1440 / Medium / 100% | Wald | 23.95 → 23.81 | 41.76 → 42.00 | 46.45 → 47.28 | 39.86 → 40.65 |
| PIE | 2560×1440 / Medium / 100% | Weg | 23.25 → 23.26 | 43.02 → 42.99 | 48.48 → 47.75 | 41.67 → 41.48 |
| PIE | 2560×1440 / High / 75% | Dorf | 23.96 → 23.81 | 41.73 → 42.00 | 46.70 → 47.25 | 38.97 → 39.12 |
| PIE | 2560×1440 / High / 75% | Wald | 24.64 → 24.93 | 40.58 → 40.11 | 45.61 → 45.63 | 37.93 → 38.14 |
| PIE | 2560×1440 / High / 75% | Weg | 23.07 → 23.61 | 43.34 → 42.36 | 49.06 → 47.14 | 40.91 → 39.55 |
| PIE | 2560×1440 / High / 100% | Dorf | 17.15 → 17.51 | 58.32 → 57.10 | 67.68 → 65.28 | 55.23 → 53.27 |
| PIE | 2560×1440 / High / 100% | Wald | 18.13 → 18.71 | 55.16 → 53.46 | 62.05 → 60.47 | 52.07 → 50.92 |
| PIE | 2560×1440 / High / 100% | Weg | 17.89 → 17.59 | 55.90 → 56.86 | 64.54 → 64.52 | 54.04 → 54.95 |
| Standalone | 1280×720 / Medium / 75% | Dorf | 60.01 → 60.03 | 16.66 → 16.66 | 17.13 → 17.12 | 12.80 → 12.90 |
| Standalone | 1280×720 / Medium / 75% | Wald | 60.03 → 60.05 | 16.66 → 16.65 | 17.12 → 17.14 | 12.79 → 12.69 |
| Standalone | 1280×720 / Medium / 75% | Weg | 60.02 → 59.96 | 16.66 → 16.68 | 17.11 → 17.08 | 12.83 → 12.74 |
| Standalone | 1280×720 / Medium / 100% | Dorf | 60.04 → 60.05 | 16.66 → 16.65 | 17.04 → 17.11 | 13.17 → 13.30 |
| Standalone | 1280×720 / Medium / 100% | Wald | 59.98 → 60.03 | 16.67 → 16.66 | 17.16 → 17.15 | 13.14 → 13.14 |
| Standalone | 1280×720 / Medium / 100% | Weg | 60.04 → 60.01 | 16.66 → 16.66 | 17.03 → 17.05 | 13.28 → 13.24 |
| Standalone | 1280×720 / High / 75% | Dorf | 60.04 → 60.04 | 16.66 → 16.66 | 18.14 → 19.93 | 14.72 → 14.69 |
| Standalone | 1280×720 / High / 75% | Wald | 60.01 → 60.05 | 16.66 → 16.65 | 18.26 → 17.27 | 13.02 → 14.58 |
| Standalone | 1280×720 / High / 75% | Weg | 59.98 → 59.99 | 16.67 → 16.67 | 17.10 → 17.56 | 14.52 → 14.46 |
| Standalone | 1280×720 / High / 100% | Dorf | 52.28 → 51.29 | 19.13 → 19.50 | 21.01 → 21.25 | 17.18 → 17.64 |
| Standalone | 1280×720 / High / 100% | Wald | 54.25 → 53.67 | 18.43 → 18.63 | 20.38 → 20.97 | 16.75 → 16.83 |
| Standalone | 1280×720 / High / 100% | Weg | 50.75 → 50.79 | 19.71 → 19.69 | 21.55 → 21.67 | 17.89 → 17.95 |
| Standalone | 2560×1440 / Medium / 75% | Dorf | 41.29 → 40.83 | 24.22 → 24.49 | 26.01 → 26.13 | 23.79 → 23.86 |
| Standalone | 2560×1440 / Medium / 75% | Wald | 42.59 → 42.53 | 23.48 → 23.51 | 25.30 → 25.54 | 23.02 → 23.01 |
| Standalone | 2560×1440 / Medium / 75% | Weg | 40.60 → 40.79 | 24.63 → 24.52 | 26.42 → 26.86 | 24.14 → 24.15 |
| Standalone | 2560×1440 / Medium / 100% | Dorf | 29.97 → 29.78 | 33.36 → 33.58 | 34.47 → 35.32 | 31.97 → 32.06 |
| Standalone | 2560×1440 / Medium / 100% | Wald | 30.59 → 30.42 | 32.70 → 32.88 | 34.17 → 35.35 | 31.21 → 31.33 |
| Standalone | 2560×1440 / Medium / 100% | Weg | 29.61 → 29.36 | 33.77 → 34.06 | 36.16 → 35.77 | 32.16 → 32.52 |
| Standalone | 2560×1440 / High / 75% | Dorf | 31.64 → 31.82 | 31.61 → 31.43 | 33.64 → 33.69 | 29.75 → 29.54 |
| Standalone | 2560×1440 / High / 75% | Wald | 32.07 → 32.12 | 31.19 → 31.13 | 33.40 → 33.53 | 29.15 → 29.33 |
| Standalone | 2560×1440 / High / 75% | Weg | 30.59 → 30.69 | 32.69 → 32.58 | 34.96 → 34.61 | 30.73 → 30.64 |
| Standalone | 2560×1440 / High / 100% | Dorf | 22.20 → 22.37 | 45.04 → 44.71 | 47.20 → 47.81 | 42.62 → 42.56 |
| Standalone | 2560×1440 / High / 100% | Wald | 22.56 → 22.92 | 44.33 → 43.63 | 47.15 → 45.38 | 42.14 → 41.74 |
| Standalone | 2560×1440 / High / 100% | Weg | 21.82 → 21.92 | 45.83 → 45.61 | 47.78 → 48.40 | 43.69 → 43.50 |

### Tatsächlich gemessene GPU-/CPU-Stufen: Standalone, Wald, QHD High 100 %

| Stufe | Control ms | FullyRough ms |
|---|---:|---:|
| GPUTime | 42.137 | 41.744 |
| GameThreadTime | 2.289 | 2.323 |
| RenderThreadTime | 44.301 | 43.621 |
| RHIThreadTime | 2.781 | 2.821 |
| GPU/Basepass | 4.178 | 4.164 |
| GPU/BeginOcclusionTests | 0.178 | 0.175 |
| GPU/DistanceFieldShadows | 0.674 | 0.655 |
| GPU/HZB | 0.223 | 0.215 |
| GPU/LightFunctionAtlasGeneration | 0.002 | 0.002 |
| GPU/LightGrid | 0.033 | 0.033 |
| GPU/Lights | 2.757 | 2.681 |
| GPU/LumenSceneLighting | 0.981 | 0.953 |
| GPU/LumenSceneUpdate | 0.969 | 1.058 |
| GPU/LumenScreenProbeGather | 11.295 | 11.101 |
| GPU/Postprocessing | 1.640 | 1.635 |
| GPU/Prepass | 0.563 | 0.542 |
| GPU/RayTracingScene | 0.053 | 0.053 |
| GPU/RenderDeferredLighting | 4.218 | 4.056 |
| GPU/RenderVelocities | 0.427 | 0.433 |
| GPU/ShadowDepths | 2.631 | 2.602 |
| GPU/ShadowProjection | 7.175 | 6.939 |
| GPU/TAA | 1.677 | 1.671 |
| GPU/Translucency | 0.129 | 0.127 |
| GPU/TranslucentLighting | 0.033 | 0.033 |
| GPU/Unaccounted | 0.025 | 0.025 |

## Bewegungs- und Gameplayprüfung

Vier reale kurze Input-/Kamerasequenzen: Control/FullyRough jeweils 720p Medium75 und QHD High100. Gehen, Sprint, Anhalten, Diagonalen, Kameranachlauf und NPC-Idle/Talk. Verdichtete reale Bildfolgen; Aufnahmelast ausdrücklich nicht für Timingwerte verwenden. Zwei initialisierte Testpositionen je Kurzsequenz, keine Behauptung eines teleportfreien Rundwegs dafür. Kein WPO in den erfassten Vegetationsmaterialien; echter Windverformungstest deshalb nicht verfügbar und kein neuer Wind hinzugefügt.

Davon getrennt drei vollständige Enhanced-Input-Fußläufe ohne Testteleports im Originalmaterial-/TAA-Kontrollzustand auf der vorhandenen GPU-Testmap. Die Materialvariante wurde in den getrennten kurzen Bewegungsfolgen geprüft; keine vollständige Kandidaten-Produktionsabnahme behauptet:

- Foot_Standalone_720p: bestanden, 267.28 m, maximale Geschwindigkeit 315.00 cm/s.
- Foot_Standalone_QHD: bestanden, 287.19 m, maximale Geschwindigkeit 315.00 cm/s.
- Foot_PIE_QHD: bestanden, 283.34 m, maximale Geschwindigkeit 315.00 cm/s.

Bestehende Prüfung von acht Richtungen, Sprint/Stop, Kollisionen, Menüs, Wanderer-Dialog/Quest, Liora, Wildkampf/Fang/Team, Archivabschluss, Heilhaus mit geradem/diagonalem Ein-/Austritt, Heilung HP/PP/Checkpoint, Sprite-Fallback und Save/Load. Tatsächlicher ursprünglicher Dev-Slot vorher gesichert, danach unverändert restauriert; die genaue anfängliche Existenz/Prüfsumme steht je Lauf in SaveBefore/SaveRestored. Keine physische Controller- oder menschliche Abnahme behauptet.

## Technische Tests und Warnungen

Mac Development Editor Builds erfolgreich (Build1.log und Build2.log). Die Messungen nutzten Build1; nach allen Messungen wurde ausschließlich die Protokollbezeichnung präzisiert: Schatten-Cast-Flags und Quellmeshes bleiben unverändert, ein erzwungener Render-LOD darf nicht als unveränderter LOD-Flag ausgegeben werden. Build2 und erneute vollständige Automation prüfen den finalen Quellstand; keine Zeitfenster oder Renderoperationen verändert. Vollständige Automation: {'succeeded': 48, 'succeededWithWarnings': 1, 'failed': 0, 'notRun': 0, 'inProcess': 0}. Alle 49 Einzeltests haben Status Success; 48 ohne Warnung, ein Test mit zwei erhaltenen vorbestehenden idevice_id/Bad-CPU-Plattformwarnungen. Der strenge Wrapper stoppte deswegen; keine Wiederholung zum Erzielen einer grünen Zusammenfassung, kein Warnungsfilter und keine Änderung der originalen Reports. ClassifyFinalAutomation.py vergleicht exakt diese Meldungen mit der vorbestehenden TAA-Baseline; keine weiteren Testwarnungen oder Fehler zugelassen. Der erste vollständige Lauf vor der reinen Logbezeichnungsänderung war 49/49 ohne Testwarnung. Map Checks von VisualV2, bestehender GPU-Testmap und WestlandAssetLibrary: jeweils 0 Fehler / 0 Warnungen. Keine neue Material-/Shader-/Instancing-Fallback- oder Probe-Steuerungsfehlermeldung in den finalen Renderläufen.

Bekannte native experimentelle Engine-Toolset-Python-Startmeldungen bleiben offen und werden gegen den vorbestehenden vollständigen Meldungs-Fingerprint verglichen. Sie werden nicht unterdrückt und machen daraus keine fehlerfreie Shipping-Abnahme. Allgemeine Engine-/MCP-/Audio-/idevice-Meldungen in Rohlogs erhalten.

Vorbereitungsfehler getrennt dokumentiert: erster Inventarzugriff auf nicht direkt exponiertes Custom-code-Attribut (auf get_editor_property korrigiert); erste Auswertungszuordnung des vor dem Segmentheader geloggten Slotzählers korrigiert; Quellatlasdimension zunächst fälschlich als 2048 statt tatsächlich 1254 angenommen und vor Verwendung vollständig neu berechnet. Diese Skriptbefunde sind keine reparierten Modellfehler. Der zusätzlich belastete erste PIE-C1-Versuch wurde vollständig neu gemessen. Der erste Bewegungsversuch lieferte wegen des erhaltenen Recorder-Ausgabepfadguards nur Telemetrie, keine Bilder; vier neue R2-Aufnahmen wurden im bestehenden zugelassenen Recorderordner vollständig erstellt, ohne den C++-Recorder zu ändern. Erste Debugbilder wurden durch einen zu frühen Moduswechsel falsch zugeordnet; alle Debugansichten unter R2 mit gehaltenem Modus bis zum geschriebenen Bild erneut erstellt.

## Dateipfade und Nachweise

- Neue Shader-Testmaster: `/Game/Environment/VegetationPerfV1/Materials/M_VVP1_CrownFullyRough` und `/Game/Environment/VegetationPerfV1/Materials/M_VVP1_FoliageFullyRough`. Nur Testassets, keine Referenz in VisualV2.
- Diagnosecode: `Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV2.cpp`.
- Reproduzierbare Werkzeuge und statische Messpläne: `Tools/VisualV2VegetationPerfV1/`.
- [Alle Einzelmessungen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/Evidence/Measurements.json)
- [Dreiergruppen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/Evidence/Summary.json)
- [Unabhängige Auswertungsprüfung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/Evidence/Validation.json)
- [Fotometadaten](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/Evidence/Photos.json)
- [Dateischutz](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/ProtectionAudit.json)
- [Warnungsprüfung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/WarningAudit.json)
- [Git-Abschluss](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/GIT_ABSCHLUSS.md)

## Visuelle Bewertung, Empfehlung und offene Grenzen

**Keine allgemeine Übernahme in VisualV2 empfohlen.** Die graphgleiche FullyRough-Variante spart etwa zehn angezeigte Shaderinstruktionen, zeigt aber keinen konsistenten Vorteil über die Matrix. Im nativen QHD-High-100-Wald: 22,56 → 22,92 FPS, Bildzeit 44,33 → 43,63 ms, GPU 42,14 → 41,74 ms. Der Base Pass ist praktisch gleich (4,1785 → 4,1637 ms). Auch unveränderte Schatten-/GI-Stufen schwanken; deshalb ist die gesamte kleine GPU-Differenz kein belegter reiner Materialgewinn. In anderen Konfigurationen sind Unterschiede nahe null oder negativ. Keine bedeutende QHD-Verbesserung und kein 60-FPS-Versprechen.

Der originale Wald ist in QHD High GPU-dominiert: GPU 42,14 ms, Game Thread 2,29 ms, Render Thread 44,30 ms einschließlich Wartezeit. Große tatsächlich gemessene Stufen sind Screen Probe Gather 11,29 ms, Schattenprojektion 7,18 ms, Deferred Lighting 4,22 ms, Base Pass 4,18 ms und Shadow Depths 2,63 ms. Dies sind teils verschachtelte Bereiche, keine addierbare Aufteilung und keine ausschließlich der Vegetation zugewiesenen Zeiten. Licht, GI und Schatten wurden hier nicht verändert.

Bei nativen 720p-Konfigurationen liegen etliche Durchläufe nahe 60 FPS, obwohl VSync=0 und t.MaxFPS=0 sind und GPU-Zeiten teils darunter liegen. Das ist ein Begrenzungsindikator; physische Präsentation beziehungsweise eine verbleibende Metal-/Fensterbegrenzung sind nicht separat aufgelöst. rhi.SyncInterval blieb 1. Gleichbleibende 60 FPS werden nicht als fehlende GPU-Kosten oder erzielter Materialgewinn ausgegeben.

**Visuell:** In den gesichteten Verlustfrei-Vergleichen bleibt die Kronendichte erhalten. Keine auffällige neue graue Fallbackdarstellung, kein zusätzliches dauerhaftes Figuren-Doppelbild und kein deutlich neuer Stilbruch in den begrenzten Bewegungsfolgen. Die Blätter waren bereits sehr rau; die Testvariante entfernt einen kleinen verbleibenden Glanzanteil und ist deshalb nicht mathematisch bildgleich. Bestehende Blatt-/Dither-Unruhe und Weichheit bei 75 % werden dadurch nicht behoben. Die zeitlich geordneten Detailbilder zeigen echte aufeinanderfolgende Frames, keine Zwischenbildsynthese. Vier erfolgreiche R2-Aufnahmen, insgesamt 1267 Frames; deren tatsächliche Renderer-AA wurde zusätzlich in den gleichzeitig erfassten Probe-Frames als 2 überprüft. Aufnahmerate deutlich unter einer 60-FPS-Abnahme; nicht jede sehr kurze Bewegungsanomalie dadurch ausgeschlossen.

Bewegungsabnahme exemplarisch bei 720p Medium75 und QHD High100, nicht als vollständige Videoabnahme sämtlicher Zwischenkonfigurationen ausgeben. Alle 16 Modus-/Auflösungs-/Qualitäts-/SP-Konfigurationen sind dagegen vollständig dreifach gemessen. Die kurzen Routen prüfen vorhandene automatische Übergänge im sichtbaren Ausschnitt, keinen vollständigen Entfernungssweep jedes Baumes. Forced-LOD1 kann Konturen und daraus folgende feine Schattenkonturen verändern; es wird ohne belastbaren Gewinn verworfen. Bestehende LOD-Schwellen und Dichte bleiben erhalten.

Die LOD-Farbansicht bestätigt am gemessenen Waldpunkt nahe Eichen/Birke in LOD0 (weiß), Sträucher überwiegend LOD1 (rot) und einige fernere Pflanzen in LOD2 (grün). Farblegende im lokalen UE-BaseEngine.ini kontrolliert. Eine pauschale Erzwingung von LOD1 kann also teils bereits reduzierte Geometrie wieder vergrößern. Die Shaderkomplexitätsansicht zeigt die Szene überwiegend im grünen Bereich ihrer Skala. Die korrekt wiederholte Quad-Overdraw-Ansicht auf METAL_SM6 ist dagegen gleichmäßig blau ohne auswertbare Blatt-/Szenenstruktur: **kein belastbarer lokaler Overdraw-Zähler**, weder als null Overdraw noch als Qualitätsgewinn interpretieren; exakte Ursache nicht bewiesen. Keine globalen Debug-/Renderoptionen dauerhaft erzwungen.

Die zusätzliche Fade-Parameter-Spiegelung gehört ausschließlich zum Testwrapper und kann eine zusätzliche Frame-Latenz haben. Sie ist keine Produktionsfreigabe eines neuen Reveal-Systems. Eine später gezielt freigegebene reine Compile-Flag-Änderung am Originalmaster bräuchte diese zusätzlichen Test-MIDs nicht. Die vollständigen Gameplay-Fußläufe gelten für den Originalmaterial-/TAA-Kontrollzustand; der Kandidat ist keine umfassend freigegebene Produktionsvariante.

**Empfohlene nächsten Schritte:**

1. Aktuelle TAA-Referenz mit originalen Materialien, automatisch gewählten LODs, Originalschatten und unverändert dichter Vegetation behalten.
2. FullyRough höchstens als kleine optionale Materialvereinfachung nach Sichtfreigabe behandeln; kein prioritäres QHD-Projekt daraus machen. Kein pauschales Erzwingen bestehender LOD1.
3. Falls weitere Vegetationsarbeit gewünscht ist: begrenzter Pilot für konservativ alphaangepasste Blattkarten an genau einer Strauchfamilie, mit Original-UVs, Filter-/Mip-Sicherheitsrand und separater Silhouetten-/Schatten-/GPU-Abnahme. Die gemessene Quellbelegung allein rechtfertigt keine flächige Geometrieänderung. Mehr Dreiecke können die Einsparung umkehren.
4. Vor breitem Umbau einen zuverlässigeren Metal-Overdraw-/Passnachweis anstreben; weder blaue Debugbilder noch null RHI-Zähler als Erfolg verwenden.
5. Größere aktuelle GPU-Stufen sind GI und Schattenprojektion. Deren mögliche Einsparungen benötigen einen getrennten, qualitätsbewahrenden Auftrag; hier keine Änderungen daran. Nanite für die Vegetation nicht ohne eigenen Vergleich aktivieren.

## Direkt zugängliche echte Vergleiche

Links Original-TAA, rechts separate FullyRough-Testvariante. Unveränderte Screenshots lediglich zur Übersicht beschriftet und zusammengestellt; volle Originalauflösungen stehen in Photos.json.

![Native QHD High100 Wald – Original / FullyRough](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/ImageReview/Standalone_2560_Q2_SP100_AB_Wald.png)

[Alle vier nativen QHD-Standorte](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/ImageReview/Standalone_2560_Q2_SP100_AB.png)

![Zeitlich geordnete echte QHD-Blattdetails nach Sprint](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/ImageReview/Motion_2560_Q2_SP100_StopSprint_Leaves.png)

[Spieler, Sprint und Gespräch: Original / Test](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/ImageReview/Motion_2560_Q2_SP100_Player.png)

[Echte lokale Videoaufnahmen – nach den Messungen aus Originalframes kodiert, PIE](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/Videos/Manifest.json)

## GitHub-Grenzen und Sicherungsumfang

Aktuelle offizielle Grenzen geprüft: reguläre Einzeldateien bis 100 MiB, Git-Push bis 2 GiB; die zusätzliche Nutzervorgabe von höchstens 1 GiB normaler neuer Git-Daten wird eingehalten. Die zwei neuen LFS-Materialdateien umfassen zusammen nur 48.693 Bytes. Keine Map, Textur, Aufnahme oder Messrohdatei neu hochladen. GitHub Free enthält laut Dokumentation 10 GiB LFS-Speicher und Download-Bandbreite; live verfügbares Kontokontingent ist nicht zuverlässig auslesbar und wird nicht als gemessene Gesamtbelegung behauptet. Keine Käufe oder Budgetänderungen.

Quellen: [GitHub Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits), [100-MiB-Dateigrenze](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [LFS-Inklusivumfang](https://docs.github.com/en/billing/concepts/product-billing/git-lfs).

Implementierung/Testwerkzeuge und Bericht werden gezielt in getrennten Commits gesichert. Tatsächliche Hashes, Remote-Prüfung, unabhängiger Download-/SHA-256-Nachweis der zwei neuen LFS-Objekte und verbleibender Git-Status stehen nach Abschluss in [GIT_ABSCHLUSS.md](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/GIT_ABSCHLUSS.md). Kein Force-Push und keine Änderung am Vollbackup.


Die vier Videos wurden nach allen Messungen erfolgreich kodiert und zusätzlich unabhängig dekodiert; Auflösungen und Dauer sind in [Videos/Verification.json](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/Videos/Verification.json) geprüft. Der erste zusätzliche Prüfer wollte bereits vom Encoder erzeugte PNG-Vorschauen exklusiv neu anlegen und stoppte; die vorhandenen Bilder blieben geschützt, erneute Prüfung mit neuen Dateinamen. Kein Unreal-Absturz.

Externe Nachweise: 2182 Dateien / 2.459.102.880 Bytes, SHA-256-kontrollierte Kopien und CRC-geprüftes ZIP. Bilder, Videos, Rohdaten und ausführbare lokale Hilfsprogramme bleiben außerhalb Git.

## Verifizierte Implementierungssicherung

Commit `622d79adabac6aea3a27bb95fea24e1616ce0433` (`perf: add isolated TAA vegetation diagnostics`) regulär auf `origin/main` gepusht und Remote direkt bestätigt. 63 gezielt geprüfte Pfade, 137.129 Bytes normaler Dateiinhalte, zwei LFS-Testmaterialien mit zusammen 48.693 Bytes. Beide LFS-Objekte nach dem Push unabhängig heruntergeladen und SHA-256/Bytezahl bestätigt; keine ausstehenden LFS-Uploads. Kein Kartenasset verändert oder hochgeladen.

`git diff --cached --check` stoppte zunächst wegen einer Leerzeichenzeile im neuen NativePhase-Werkzeug. Ausschließlich diese harmlose Leerzeichenzeile korrigiert, exakt denselben Index erneut geprüft; danach ohne Befund committed. Keine bestehenden Nutzerdateien dafür geändert.

Der Bericht wird separat gesichert. Endgültige Bericht-Commit-ID, finale Remote-/LFS- und Arbeitsbaumprüfungen im verlinkten externen Git-Abschluss. Die vorbestehenden lokalen Testdateien sowie lokale Python-Caches bleiben uncommittet; kein Vollbackup-Vorfahr in der neuen Historie.
