# PokeMonster – QHD Performance Investigation V2

Stand 15.10.2026. Experiment abgeschlossen, **keine automatische Übernahme in VisualV2 und keine Produktionsfreigabe**.

## Ergebnis

Neue Karte: **`/Game/Maps/Dev_TestMap_EnvironmentPerfV2`**, gespeichert unter `Content/Maps/Dev_TestMap_EnvironmentPerfV2.umap`.
Ausgangs-HEAD: `351a3ef Add YoungTrainer sprint V1 and in-place run animation`.

Die gezielte Lumen-Alternative verbessert vor allem High. Nativer Waldvergleich: QHD/75 % **23,74 → 27,19 FPS**, QHD/100 % **17,76 → 20,82 FPS**. PIE: **15,94 → 18,52** beziehungsweise **11,14 → 12,43 FPS**. Medium profitiert wesentlich weniger und nicht durchgehend. Die Ziele stabile 60 FPS bei QHD/Medium und mindestens 30 FPS bei QHD/High werden weiterhin nicht erreicht.

Im untersuchten Umfang wurde keine wesentlich größere weitere Verbesserung bei gleichzeitig weitgehend unverändertem Bild nachgewiesen. Das beweist kein allgemeines Hardwarelimit. Komplette Beleuchtung, Vegetation oder Postprocessing abzuschalten ist keine übernommene Optimierung.

## 1. Schutz und Änderungen

Der Arbeitsbaum war bereits verändert: NPC-Integration, Ranger V2 und EnvironmentPerfV1 waren offene Vorarbeiten. Ihr Anfangsstatus ist unten dokumentiert. **Alle 2863 anfangs erfassten versionierten und unversionierten Projektdateien sind abschließend bytegleich**, keine entfernt. Das umfasst alle bisherigen Karten, Player/Animationen, Originalassets und bereits geänderte Dokumente/C++-Dateien. Der während des Auftrags hinzugekommene Ordner `Art/Characters/MiniHobbit/` ist fremde parallele Arbeit und wurde nicht angefasst.

Die neue Karte wurde über die Unreal-Editor-API aus EnvironmentPerfV1 gespeichert und anschließend unter ihrem neuen Pfad geladen. Die Originalkarte wurde nicht gespeichert. Levelaudit: **1351 statt 1350 relevante Akteure**, ausschließlich ein neuer `EnvironmentPerfV2_RenderOnly` ohne Tick/Collision. Alle bestehenden Actor-Transforms, Static Meshes, Materialien, Collision-Einstellungen und Instanzen unverändert. Die gespeicherten Rendererwerte nach erneutem Laden geprüft.

Nur neue V2-Dateien: die Arbeitskarte, drei Development-C++-Dateien, ein Automationstest, `Tools/EnvironmentPerfV2/`, das Reviewpaket und dieser Bericht. Keine neue Blenderquelle, kein Mesh, kein Material, keine Textur, kein Plugin. Kamera außen **2850 cm / Pitch −50° / Yaw −45° / FOV 35°**, Player 140 cm, Normalgeschwindigkeit 210 cm/s und Gameplay unverändert. Keine neue verbindliche Baseline-Entscheidung: TECHNIK.md und ENTSCHEIDUNGEN.md bleiben gegenüber Auftragsbeginn bytegleich.

## 2. Messmethode und echte Auflösung

Installierte UE 5.8.2, Apple M4, 16 GiB gemeinsamer Speicher. Eingebettetes Editor-PIE und native Development-`-game`-Prozesse, **kein verpackter Shipping-Build**. Während nativer Zeitmessungen Editor geschlossen. Keine Builds, Blender-Renders, Bildverarbeitung oder zweite Unreal-Instanz gleichzeitig mit GPU-Zeitmessungen.

Vollständige Matrix in beiden Modi: 1280×740 Medium bei 75/100 %, QHD 2560×1440 Medium und High jeweils bei 75/100 %. Je Kombination Dorf, Wald, Weg und drei benachbarte Kontroll-/Kandidatenpaare; umgekehrte Reihenfolge in Wiederholung 2. **108 ausgewählte Abschnitte je Modus, 216 insgesamt**. Fünf Sekunden Warm-up und sechs Sekunden Messung pro Abschnitt. Die kurzen Paarfenster liefern keine formalen Konfidenzintervalle; zusätzlich zwölfminütiger Dauertest.

Kontrolle ist der tatsächliche **EnvironmentPerfV1-Renderstand**, einschließlich Integration-Downsample 2, gerichteter SMRT-RayCount 2 und dessen Außen-Postprocessing. Keine künstlich langsamere VisualV2-Kontrolle. Native Prozesse laden die erhaltene V1-Karte und schalten den Kandidaten temporär über den Probe; der gespeicherte V2-Profilakteur kann so keine Kontrollzeile verfälschen. Geometrische Gleichheit durch Audit belegt.

Ein Render-Thread-Observer erfasst Spiel-ViewFamily/ViewRect und tatsächliche Screen-Percentage-Driver. Zusätzlich je Frame: GameViewport, RenderTarget, Fenstergröße/DPI/Aktivierung, Kamerapose und UTC. Die interne Auflösung wird aus dem beobachteten Driver-Faktor berechnet, **nicht aus GPU-Texture-Allocations zurückgelesen**.

| Renderer-Ausgabe | SP | interne Szene |
|---|---:|---|
| 1280×740 | 75 % | 960×555 |
| 1280×740 | 100 % | 1280×740 |
| 2560×1440 | 75 % | 1920×1080 |
| 2560×1440 | 100 % | 2560×1440 |

Sekundärfaktor 1,0; dynamische Auflösung aus. Ausgewählte native Fenster entsprechen der Sollgröße, DPI 1. Editorfenster 2940×1696 bei DPI 2; dessen Renderer wird separat auf die dokumentierte Größe gesetzt. **2331×1346 wird nicht als 1280×740 ausgegeben.** Alle ausgewählten Samples: aktives Fenster, stabile Auflösungen/Faktoren und Kamera. Fensterextents und Kameraposen sind innerhalb jedes Paars gleich.

Player-Messpunkte in cm: Dorf (−4100,450,50,15), Wald (−4300,1550,50,15), Weg (−36,6,−47,1,50,15). Exakte Kamera-XYZ in den Daten. NPCs im normalen Idle ohne Dialog/Laufen; Animationen laufen während Timing weiter. Für Bildpaare werden Skeletal-Posen vorübergehend eingefroren und danach wiederhergestellt. Kontrollierte Benchmark-/Bildpositionierung wird niemals als Fußlauf ausgegeben.

### Abgelehnte Daten und vollständige Wiederholungen

Strenge Prüfung fand Vordergrundverlust im ursprünglichen QHD-PIE-Block, wechselnde native Fenstergrößen in den beiden Standardserien und Vordergrundverlust in einer QHD-High-Dorfzeile. Rohdaten erhalten, betroffene Gruppen nicht als Abnahme gezählt:

- `RepairPIEQHD`: alle vier QHD-PIE-Konfigurationen, 72 Abschnitte.
- `RepairNative1/2`: beide Standardkonfigurationen vollständig, je 18 Abschnitte.
- `RepairNativeHighDorf`: alle drei Dorfpaare QHD High/100, sechs Abschnitte.
- Beibehalten: 36 gültige Standard-PIE-Abschnitte und übrige gültige native Gruppen.

Das Diagnosewerkzeug bereitet native Fenstergröße/Vordergrund **vor dem Warm-up** vor. Editorhauptfenster über native UI angehoben. Keine Auswahl einzelner günstiger Frames. `MeasurementsResolved.json` enthält Ursprungsserie/-segment, `MeasurementSelection.json` dokumentiert die Auswahl. Abschließende Abnahme aller 216 ausgewählten Abschnitte bestanden.

### Messgrenzen

Früher Host-Snapshot 15:19 UTC: Akku/86 %. Abschließender Snapshot: Netzbetrieb/99 %. Wechselzeitpunkt nicht kontinuierlich erfasst. **Keine Behauptung identischer Energiebedingungen über den Gesamtauftrag** und keine absoluten Vergleiche zwischen verschiedenen Uhrzeiten/Modi. Benachbarte A/B-Paare und umgekehrte Reihenfolge reduzieren Drift, schließen fremde Systemlast und Leistungsregelung nicht aus. Parallele Nutzerarbeit wurde nicht beendet. Für eine verbindliche Leistungsfreigabe ruhige Netzbetriebsserie wiederholen.

Sieben native Abschlusssegmente besitzen keinen vollständig geschriebenen Profiler-CSV-Satz nach automatischem Prozessende. Eigenständig gespeicherte Framezeiten/Auflösungen vollständig. CPU-/GPU-Aggregate verwenden nur vorhandene Zähler; fehlende Werte werden nicht erfunden. StrictValidation nennt die sieben Segmente. PIE-RenderThread-Zähler hier unzuverlässig: n/v. Native RenderThread-Werte enthalten Wartezeit, keine reine CPU-Ausführungszeit. RHI-/Draw-Call-Zähler null/unverfügbar, **kein Nachweis von null Draw Calls**.

## 3. 60-FPS-Grenze

r.VSync=0, r.VSyncEditor=0, t.MaxFPS=0; Engine-Smoothing und FixedFrameRate aus. Native GameUserSettings: FrameRateLimit 0, bUseVSync false. Fenster-Pacingläufe: **60,03 / 60,01 / 59,96 FPS**. Angeforderter Vollbildgegenversuch: **59,29 / 59,89 / 59,97 FPS**. Sicher unlimitierter exklusiver Modus nicht nachgewiesen; GameUserSettings FullscreenMode blieb 1.

Lokale Primärquelle: `Engine/Source/Runtime/Apple/MetalRHI/Private/MetalViewport.cpp:1101`. Metal erzwingt außerhalb des echten Game-Fullscreen-Pfads Display-Synchronisierung unabhängig von r.VSync=0. rhi.SyncInterval war 1. Der beobachtete Deckel belegt keine freie GPU-Leistungsreserve. Pacingdiagnose hatte andere Fensterextents und ist kein Optimierungsvergleich. Hauptmatrix mit gleichen Fenstern; QHD liegt deutlich unter dem Deckel.

## 4. GPU-Analyse und gespeicherter Kandidat

Gesonderter ProfileGPU-Frame **innerhalb** verifizierter QHD/High/100-Scope, Proof mit Viewport und CVars gesichert. Ein zuvor verspäteter Capture zeigte 2331×1346 und wird ausdrücklich nicht als QHD-Nachweis benutzt.

| Ereignis, inklusive Metal-Zeit | ms |
|---|---:|
| gesamter Profiling-Frame | 94,273 |
| SceneRender | 89,322 |
| BasePassParallel | 4,567 |
| Lumen ScreenProbeGather | 15,849 |
| darin WorldRadianceCaches | 11,761 |
| ShadowDepths | 1,587 |
| VSM Projection | 5,997 |
| PostProcessing | 2,607 |
| darin Tonemap | 2,118 |
| TSR-Marker | 0,261 |
| VSM Log Stats And Status | 31,393 |

**Kein addierbares präzises Shaderbudget:** Metal-Breadcrumbs teilen Stage-Counter-Zeitspannen; Leaf-Zuordnung grob, teils null. Der VSM-Stats-Marker beweist keinen 31-ms-Statistik-Shader. VSM-CSV-Kanal war nachweislich aus, Stats.Visible bereits 0. Erneutes Setzen und Abschalten von GPU-CSV-Statistik sparen nicht entsprechend Zeit. Primärquelle: MetalProfiler.h ab Zeile 94. Draws/Dispatches-Zähler unbrauchbar.

Wiederholte Einzelfaktoren sind entscheidender: Gather-Wechsel spart im QHD-High-Wald median **7,505 ms**, allein Hardware-Lumen aus **4,126 ms** mit großem Ausreißer. GI ganz aus spart 12,743 ms, Beleuchtung ganz aus 31,211 ms; nicht übernommen. PostProcessing-ShowFlag aus spart 23,444 ms, ist aber ein zusammengesetzter Diagnoseeingriff, kein isolierter Tonemapper-Befund.

VSM→CSM spart median 4,474 ms, uneinheitliches erstes Paar: keine Bestätigung des riesigen Stats-Leafwerts. Weniger SMRT-Samples/ein Strahl kein stabiler Vorteil. Vegetation unsichtbar spart hier 2,941 ms, keine allgemeine Entwarnung für Blatt-Overdraw. Materials-ShowFlag aus spart 2,881 ms mit Streuung. Keine Bäume entfernt oder ausgedünnt, keine Materialvereinfachung ohne tragfähige Qualitätsabnahme übernommen.

Nativer QHD-High/100-Wald: Game Thread ca. 1,98/1,94 ms, GPU 54,42/47,64 ms. PIE ca. 8,02/7,53 ms und GPU 85,78/79,34 ms. Zusammen mit Auflösungsskalierung spricht das für einen **GPU-/Renderpfad-Schwerpunkt**, nicht primär Spiellogik. Feinere GPU-Auflösung, reiner Render-CPU-Aufwand, Overdraw-Pixelzahlen und exakte Draw Calls nicht hinreichend messbar.

| CVar | Kontrolle V1 | Kandidat V2 |
|---|---|---|
| r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor | 2 | 2 |
| r.Shadow.Virtual.SMRT.RayCountDirectional | 2 | 2 |
| r.Lumen.FinalGatherMethod | Medium 0, High 1 | 0 |
| r.Lumen.HardwareRayTracing | 1 | 0 |

Enginequelle Lumen.cpp:55 beschreibt Gather 0 ausdrücklich als schnellere, **qualitativ einfachere** Irradiance-Field-GI. High bleibt als Gruppe High, erhält aber gezielt einen anderen GI-Pfad: keine Behauptung pixelidentischer High-Qualität. Medium verwendet Gather 0 ohnehin. Neue AInfo-Scope wirkt nur in EnvironmentPerfV2, respektiert höhere CVar-Prioritäten und stellt bei EndPlay zurück. Kein dauerhaftes globales INI-Tuning. V1-Postprocessing und Schattenverfahren/-dichte bleiben erhalten.

Baked/static GI nicht umgesetzt: r.AllowStaticLighting=False in DefaultEngine.ini. Änderung wäre globaler Projekt-/Shader-Eingriff. GI-None/ScreenSpace-Vergleiche sind keine geprüfte Ersatzbeleuchtung. Vollständige Einzelpaare und finale Matrix folgen im Messanhang.

## 5. Visuelle Prüfung und Kiste

Echte unveränderte Unreal-Spielkamera-Captures: sieben direkte QHD-High/100-Bildpaare Dorf/Gebäude, Wald, NPC im Waldschatten, Kronenfreistellung, Weg/Brücke, Lichtung, Archiv. Zusätzlich passender Innenraumvergleich während echtem Fußlauf und Gameplaybilder. Keine synthetischen Konzepte.

Sichtprüfung: Kronendichte, Silhouetten, Wege, Gebäude, direkte Schatten und Figurengröße bleiben erhalten. Einzelne Steine/Props sowie indirekte Helligkeits-/Kontaktverläufe ändern sich sichtbar. Innenraum bleibt warm und lesbar, feine Boden-/Kontaktschatten unterscheiden sich. Player im tiefen Waldschatten weiterhin dunkel wie in V1. Nicht alle Tageszeiten, dynamische GI und dünne Kleidungs-/Blattdetails endgültig abgenommen. Keine neuen LODs, damit keine durch diese Arbeit eingeführten LOD-Wechsel. Bestehende Kronenfreistellung im Bildpaar und Fußlauf wirksam.

Brauner Würfel: **V2_House_HH_V3_SupplyCrate**, dekorativer Engine-Cube aus Tools/DressHealingHouseV3.py:175. 42×42×36 cm, Position (−3570,−62,18), NoCollision. Unterkante Z=0, echter Trace auf V2_Ground trifft Z=0, Abstand **0 cm**. Schwebt nicht. Einfacher Blockout und schwacher Kontakt können den Eindruck erzeugen. Nicht entfernt oder versetzt.

## 6. Gameplay und Tests

Echter eingebetteter PIE-Fußlauf über Enhanced Input; Interaktionen/Kampfentscheidungen über bestehende APIs. **Keine Test-Teleports**. Nur normale vorhandene Gebäuderelocation. Kontrollierte Benchmarkpositionen zählen nicht als Fußlauf.

Bestanden: **263,00 m**, **103 protokollierte Schritte**, **209,91 s** reale Laufzeit, maximal 210,00000 cm/s.

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Acht Richtungen, Stoppen, Collision, Fallprüfung, Kamera | bestanden, 210 cm/s |
| Wanderer, Dialogsperre, Questdialog, Ranger-Talk | bestanden, Conversation-Blend aktiv und Bildsequenz |
| Wildbegegnung/Fang | CAPTURED, Party danach drei |
| Liora | VICTORY, Trainerflag gesetzt |
| Save/Load vor Archiv | gespeichert, Runtime-Trainerliste geleert, geladen; Trainerstatus und HP/PP wiederhergestellt |
| Archiv und Rückweg | Archivflag gespeichert, Folgegespräch mit Wanderer durchlaufen |
| Menüs | vor/nach Rundweg; während Dialog/Kampf gesperrt |
| Heilhaus gerade/diagonal hinein/hinaus | Relocation, Innensteuerungsbasis, Dach-/Front-Cutaway korrekt |
| Heilerin | HP/PP vollständig, Checkpoint VisualV2_HealingHouse gespeichert |
| NPC-Sprite-Fallback | aktiviert, geprüft, auf Ranger zurückgestellt |
| Wald und Reveal | Rundweg und Materialvergleich, danach wiederhergestellt |

Originaler Dev-Save bytegleich wiederhergestellt, SHA256 **626d58c2f512b3c63f90a18537fd646f611adecb76d52827428a67f578bbd21e**. Testspielstand zusätzlich unter Saved erhalten. Runtime-Save/Load, kein vollständiger Neustart-/Shipping-Save-Test.

Build Development Editor erfolgreich: Profilbuild 14,16 s, letzter Diagnosefenster-Build **6,34 s**. Erstversuch des Fenster-Patches hatte Compilefehler (`GetWindow` liefert void-Pointer), auf `FindWindow` korrigiert; beide Logs erhalten. Keine Gameplay-C++-Datei geändert.

Vollständige Automation zweimal ausgeführt, nach letztem C++-Build erneut: **45 erfolgreich / 0 mit Testwarnungen / 0 fehlgeschlagen / 0 nicht ausgeführt**, Exit 0. Neuer Test EnvironmentProfileV2.IndependentExperiment prüft Levelbegrenzung, NoTick/NoCollision und V1-Ausgangswerte. Nicht aus früheren Chatangaben abgeleitet.

Map Check nach erneutem Laden und Abschluss: **0 Fehler / 0 Warnungen**. Persistierte vier CVarwerte bestätigt. Am Ende keine dirty Maps/Content-Packages, PIE gestoppt. Session-CVars/Throttling und MCP-Port 8000 wiederhergestellt, eigene Callbacks entfernt.

### Warnungen und offene Prüfgrenzen

- Vor Projektinitialisierung im Automation-Startlog: **17 generische LogAutomationTest: Error: Condition failed**, Frame 0. Nicht den 45 Projekttests zugeordnet, deren Fehlerzahl null ist. Ursache nicht abschließend ermittelt, nicht unterdrückt; kein vollständig fehlerfreies Engine-Startlog behauptet.
- idevice_id: Bad CPU type / nicht gestartetes iOS-Hilfsprogramm, je zwei Meldungen; Ziel bleibt macOS. Zusätzlich MCP-EULA-Hinweis und Editorlayout-Migrationswarnung.
- Speicherhinweis im Editor; einmalige Systemabfrage 23 % frei. Automatische Freigabeprüfung lehnte „Verwerfen“ wegen möglichen Verlusts ungesicherter Editorzustände ab. Nicht umgangen, Hinweis unangetastet; Tests ohne Schließen möglich, Dirty-Package-Prüfung bestanden.
- Geschützte HitResult-Properties/angenommener Python-Break-Aufruf nicht verfügbar; anschließend Bodenhöhe erfolgreich über Native-Break-to_tuple ermittelt. Keine Geometrieänderung.
- Sieben native Abschluss-Profiler-CSV-Sätze fehlen. Draw Calls und feine Metal-Leafkosten unverlässlich. Fehlende Werte bleiben fehlend.
- Kurze Paarfenster, P95 ausreißerempfindlich. Energiezustand wechselte; fremde Hintergrundarbeit nicht vollständig kontrolliert. Keine pauschale Stabilitätsgarantie.

## 7. Empfehlung

**Getrennten experimentellen Kandidaten behalten, VisualV2 nicht automatisch übernehmen.** High zeigt wiederholten Framezeitvorteil bei weitgehend erhaltener Makroansicht. Medium keine durchgehend belastbare Verbesserung, z. B. langsamerer PIE-Wald bei QHD/100. Eine allgemeine Standardumschaltung ist nicht ausreichend begründet. Harrys Bildfreigabe und zusätzliche indirekte Detailprüfung fehlen.

Nächste Schritte: ruhige durchgehende Netzbetriebsserie; feinere Metal-Capture-Zuordnung und Trennung von Präsentations-/GPU-Zeit. Danach gezielter Ersatz teurer indirekter Beleuchtung in weiterer separater Karte mit Innenraum-/Dünnflächenvergleich. Baked GI erfordert wegen deaktivierter statischer Beleuchtung einen ausdrücklich separaten Projekt-/Shader-Versuch. Lokale Licht-/Schattenkosten weiter isolieren, bevor Vegetationsqualität geopfert wird. Bloße Ranger-Polygonreduktion erklärt die QHD-Lücke nicht hinreichend.

## 8. QHD-Dauertest

Ein nativer Prozess, Editor geschlossen, High/100 %. Neun Abschnitte mit je fünf Sekunden Warm-up und 75 Sekunden Messung, drei Runden Dorf → Wald → Weg. **721,375 s** Messstrecke einschließlich Warm-up, gut zwölf Minuten. Bereits warmer Rechner, kein Kaltstartvergleich.

| Ort | FPS Runde 1/2/3 | Frame ms 1/2/3 | P95 ms 1/2/3 | Frameänderung letzte/erste |
|---|---|---|---|---:|
| Dorf | 19.208 / 21.822 / 20.682 | 52.062 / 45.825 / 48.350 | 61.115 / 56.694 / 52.629 | -7.13 % |
| Wald | 21.384 / 21.673 / 20.694 | 46.765 / 46.141 / 48.324 | 51.459 / 51.083 / 57.074 | +3.33 % |
| Weg | 21.452 / 21.752 / 21.552 | 46.616 / 45.972 / 46.399 | 52.024 / 48.784 / 51.059 | -0.46 % |

Alle 72 Thermal-Samples nominal. Wald +3,33 % Framezeit, Dorf schneller, Weg fast gleich. Kein eindeutiger fortschreitender thermischer Einbruch nachgewiesen. Keine Temperatur-/Frequenz-/Energieaufnahmeauslesung: kein Nachweis unveränderter GPU-Takte und keine Kausalbehauptung über Throttling.

## 9. Vollständige Messwerte

FPS = 1000/Median-Framezeit je Lauf. Gruppentabellen verwenden Median der drei Laufmediane und Median der Lauf-P95; Einzelwerte in MeasurementsResolved.json. Median der Paardifferenzen muss nicht gleich Differenz der separat aggregierten Mediane sein.

## Einzelfaktor-Paare

Negative Differenzen bedeuten kürzere Framezeit. Drei benachbarte Paare, umgekehrte Reihenfolge in Wiederholung 2. QHD/High/100%.

| Serie/Ort | Faktor | Δ Frame ms je Paar | Median Δ Frame ms | Median Δ GPU ms |
|---|---|---|---:|---:|
| FactorsQHD/Wald | GI:0 | -12.743, -13.511, -12.070 | -12.743 | -10.416 |
| FactorsQHD/Wald | GI:2 | -7.259, -6.731, -6.591 | -6.731 | -1.961 |
| FactorsQHD/Wald | CV:r.Lumen.FinalGatherMethod=0 | -9.725, -7.505, -7.259 | -7.505 | -6.463 |
| FactorsQHD/Wald | CV:r.Lumen.ScreenProbeGather.ShortRangeAO.DownsampleFactor=4 | -0.378, +0.926, +2.564 | +0.926 | +0.993 |
| FactorsQHD/Wald | CV:r.Lumen.ScreenProbeGather.ShortRangeAO=0 | -0.509, -2.145, -1.838 | -1.838 | -0.380 |
| FactorsQHD/Wald | CV:r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor=4 | -3.342, -4.164, -2.618 | -3.342 | -2.014 |
| FactorsQHD/Wald | CV:r.Shadow.Virtual.SMRT.SamplesPerRayDirectional=2 | +0.427, +0.050, +0.254 | +0.254 | -0.102 |
| FactorsQHD/Wald | CV:r.Shadow.Virtual.Enable=0 | +0.796, -5.235, -4.474 | -4.474 | -3.594 |
| FactorsQHD/Wald | CV:r.DistanceFieldShadowing=0 | -0.760, -3.499, -1.023 | -1.023 | -0.477 |
| FactorsQHD/Wald | CV:ShowFlag.Materials=0 | -0.343, -4.305, -2.881 | -2.881 | -2.309 |
| FactorsQHD/Wald | CV:ShowFlag.PostProcessing=0 | -23.444, -23.865, -22.971 | -23.444 | -22.569 |
| FactorsQHD/Wald | CV:ShowFlag.Lighting=0 | -33.583, -31.211, -28.210 | -31.211 | -29.359 |
| FactorsQHD/Wald | VegetationHidden | -2.629, -3.445, -2.941 | -2.941 | -2.574 |
| FactorsFollowup/Wald | CV:r.Lumen.HardwareRayTracing=0 | -2.192, -18.210, -4.126 | -4.126 | -1.253 |
| FactorsFollowup/Wald | CV:r.Lumen.HardwareRayTracing=0|r.Shadow.Virtual.Enable=0 | -7.898, -7.498, -5.067 | -7.498 | -4.682 |
| FactorsFollowup/Wald | CV:r.Shadow.Virtual.Stats.Visible=0 | +1.205, -2.069, +2.985 | +1.205 | +0.839 |
| FactorsFollowup/Wald | CV:r.GPUCsvStatsEnabled=0 | -0.912, +1.130, +3.589 | +1.130 | +1.224 |
| FactorsFollowup/Wald | CV:r.Shadow.Virtual.SMRT.RayCountDirectional=1 | +2.048, +0.501, +0.925 | +0.925 | +0.240 |

## Finale Paare: PIE

| Ausgabe | Qualität | SP | Ort | Kontrolle FPS | Kandidat FPS | Kontrolle Frame ms | Kandidat Frame ms | Δ ms je Paar | Median Δ ms | Kontrolle/Kandidat P95 ms | Kontrolle/Kandidat Game ms | Kontrolle/Kandidat Render ms | Kontrolle/Kandidat Render CriticalPath ms | Kontrolle/Kandidat GPU ms |
|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|---|
| 1280×740 | Medium | 75% | Dorf | 39.40 | 41.82 | 25.383 | 23.910 | +0.842, -0.354, -1.473 | -0.354 | 30.236/30.796 | 9.679/11.574 | n/v/n/v | n/v/n/v | 23.319/22.122 |
| 1280×740 | Medium | 75% | Wald | 39.28 | 41.42 | 25.456 | 24.141 | +1.746, -0.775, -2.700 | -0.775 | 30.047/29.665 | 9.739/13.886 | n/v/n/v | n/v/n/v | 22.550/22.735 |
| 1280×740 | Medium | 75% | Weg | 35.51 | 36.46 | 28.163 | 27.426 | -0.831, -0.737, -1.627 | -0.831 | 36.589/33.778 | 10.886/9.740 | n/v/n/v | n/v/n/v | 25.393/26.234 |
| 1280×740 | Medium | 100% | Dorf | 35.82 | 38.78 | 27.919 | 25.784 | +5.394, -2.135, -2.965 | -2.135 | 30.889/28.506 | 9.318/8.484 | n/v/n/v | n/v/n/v | 26.810/24.382 |
| 1280×740 | Medium | 100% | Wald | 39.63 | 39.25 | 25.233 | 25.476 | -2.509, +0.243, -0.305 | -0.305 | 35.778/32.408 | 8.471/8.340 | n/v/n/v | n/v/n/v | 23.553/24.690 |
| 1280×740 | Medium | 100% | Weg | 32.49 | 37.40 | 30.780 | 26.739 | +1.121, -4.041, -1.583 | -1.583 | 34.549/51.539 | 8.463/9.604 | n/v/n/v | n/v/n/v | 25.536/25.428 |
| 2560×1440 | Medium | 75% | Dorf | 19.76 | 20.26 | 50.615 | 49.365 | -0.769, -1.250, +0.316 | -0.769 | 57.642/52.561 | 8.349/7.392 | n/v/n/v | n/v/n/v | 48.782/48.197 |
| 2560×1440 | Medium | 75% | Wald | 20.13 | 20.66 | 49.672 | 48.394 | -1.324, -1.234, -1.282 | -1.282 | 53.538/51.251 | 7.637/7.756 | n/v/n/v | n/v/n/v | 47.592/47.258 |
| 2560×1440 | Medium | 75% | Weg | 19.98 | 20.26 | 50.060 | 49.348 | -0.364, -0.806, -0.543 | -0.543 | 54.485/51.450 | 7.276/7.739 | n/v/n/v | n/v/n/v | 47.976/48.246 |
| 2560×1440 | Medium | 100% | Dorf | 13.85 | 14.23 | 72.218 | 70.276 | -1.823, -1.935, -3.250 | -1.935 | 78.938/78.535 | 7.389/7.064 | n/v/n/v | n/v/n/v | 70.097/68.980 |
| 2560×1440 | Medium | 100% | Wald | 13.93 | 13.28 | 71.803 | 75.314 | +2.172, -1.502, +4.697 | +2.172 | 79.688/79.668 | 7.419/7.059 | n/v/n/v | n/v/n/v | 69.674/72.988 |
| 2560×1440 | Medium | 100% | Weg | 13.76 | 13.82 | 72.684 | 72.344 | -4.320, -0.858, +3.045 | -0.858 | 80.738/87.650 | 7.465/7.209 | n/v/n/v | n/v/n/v | 71.644/71.445 |
| 2560×1440 | High | 75% | Dorf | 15.48 | 18.15 | 64.602 | 55.100 | -9.249, -8.792, -9.804 | -9.249 | 67.361/61.570 | 7.610/6.996 | n/v/n/v | n/v/n/v | 60.630/54.233 |
| 2560×1440 | High | 75% | Wald | 15.94 | 18.52 | 62.734 | 53.996 | -11.020, -8.881, -8.591 | -8.881 | 66.424/60.541 | 7.804/7.066 | n/v/n/v | n/v/n/v | 58.825/52.968 |
| 2560×1440 | High | 75% | Weg | 15.57 | 18.13 | 64.235 | 55.166 | -9.069, -8.657, -7.273 | -8.657 | 67.064/60.583 | 7.457/6.659 | n/v/n/v | n/v/n/v | 60.069/54.245 |
| 2560×1440 | High | 100% | Dorf | 10.71 | 12.20 | 93.386 | 81.975 | -7.945, -14.497, -11.411 | -11.411 | 99.673/85.859 | 7.968/7.677 | n/v/n/v | n/v/n/v | 88.434/80.935 |
| 2560×1440 | High | 100% | Wald | 11.14 | 12.43 | 89.770 | 80.481 | -7.954, -13.252, -9.288 | -9.288 | 98.059/82.968 | 8.017/7.525 | n/v/n/v | n/v/n/v | 85.777/79.336 |
| 2560×1440 | High | 100% | Weg | 10.77 | 12.12 | 92.844 | 82.530 | -6.697, -15.352, -10.314 | -10.314 | 98.228/84.801 | 8.075/7.532 | n/v/n/v | n/v/n/v | 87.844/80.687 |

## Finale Paare: Standalone

| Ausgabe | Qualität | SP | Ort | Kontrolle FPS | Kandidat FPS | Kontrolle Frame ms | Kandidat Frame ms | Δ ms je Paar | Median Δ ms | Kontrolle/Kandidat P95 ms | Kontrolle/Kandidat Game ms | Kontrolle/Kandidat Render ms | Kontrolle/Kandidat Render CriticalPath ms | Kontrolle/Kandidat GPU ms |
|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|---|
| 1280×740 | Medium | 75% | Dorf | 60.01 | 60.02 | 16.665 | 16.660 | -0.011, -0.014, +0.006 | -0.011 | 17.054/17.111 | 1.276/1.506 | 16.661/16.663 | 16.661/16.663 | 15.768/16.351 |
| 1280×740 | Medium | 75% | Wald | 60.00 | 60.01 | 16.666 | 16.664 | -0.010, -0.003, +0.010 | -0.003 | 17.127/17.048 | 1.363/1.526 | 16.658/16.667 | 16.660/16.667 | 15.780/16.341 |
| 1280×740 | Medium | 75% | Weg | 60.05 | 60.01 | 16.654 | 16.665 | +0.003, +0.007, +0.013 | +0.007 | 17.022/17.118 | 1.294/1.545 | 16.661/16.656 | 16.661/16.656 | 15.721/16.375 |
| 1280×740 | Medium | 100% | Dorf | 60.03 | 60.05 | 16.659 | 16.654 | +0.004, -0.001, -0.006 | -0.001 | 17.056/17.118 | 1.274/1.361 | 16.662/16.651 | 16.662/16.651 | 15.908/16.387 |
| 1280×740 | Medium | 100% | Wald | 60.02 | 60.02 | 16.662 | 16.660 | -0.009, +0.003, -0.013 | -0.009 | 17.075/17.201 | 1.307/1.506 | 16.659/16.652 | 16.659/16.652 | 15.890/16.399 |
| 1280×740 | Medium | 100% | Weg | 60.01 | 60.03 | 16.665 | 16.659 | -0.019, -0.000, -0.007 | -0.007 | 17.056/17.054 | 1.309/1.376 | 16.657/16.663 | 16.657/16.663 | 15.837/16.403 |
| 2560×1440 | Medium | 75% | Dorf | 30.76 | 31.37 | 32.511 | 31.874 | -0.992, -0.743, -0.172 | -0.743 | 34.810/33.334 | 1.581/1.370 | 32.481/31.885 | 32.481/31.885 | 31.267/31.383 |
| 2560×1440 | Medium | 75% | Wald | 30.73 | 32.23 | 32.539 | 31.030 | -1.204, -1.510, -2.123 | -1.510 | 35.833/33.335 | 1.596/1.387 | 32.538/31.050 | 32.538/31.050 | 31.481/30.655 |
| 2560×1440 | Medium | 75% | Weg | 30.56 | 31.21 | 32.720 | 32.041 | -1.268, -0.679, -0.905 | -0.905 | 34.763/34.267 | 1.645/1.319 | 32.714/32.331 | 32.714/32.331 | 31.452/31.969 |
| 2560×1440 | Medium | 100% | Dorf | 18.99 | 20.30 | 52.671 | 49.258 | -0.503, -3.413, -2.040 | -2.040 | 62.730/51.865 | 1.913/1.697 | 52.554/49.229 | 52.554/49.229 | 50.982/48.756 |
| 2560×1440 | Medium | 100% | Wald | 20.85 | 20.78 | 47.957 | 48.114 | +0.729, +2.111, -0.288 | +0.729 | 58.358/55.957 | 1.873/1.804 | 47.954/48.109 | 47.954/48.109 | 46.718/47.929 |
| 2560×1440 | Medium | 100% | Weg | 19.68 | 19.66 | 50.818 | 50.855 | -1.448, +0.126, +0.037 | +0.037 | 59.356/55.831 | 1.919/1.691 | 50.758/49.292 | 50.758/49.292 | 49.669/48.647 |
| 2560×1440 | High | 75% | Dorf | 23.65 | 26.68 | 42.278 | 37.488 | -3.483, -5.545, -4.790 | -4.790 | 46.090/40.650 | 1.839/1.597 | 42.301/37.466 | 42.301/37.466 | 39.980/37.092 |
| 2560×1440 | High | 75% | Wald | 23.74 | 27.19 | 42.121 | 36.782 | -3.753, -6.102, -5.339 | -5.339 | 46.571/42.111 | 1.804/1.529 | 42.106/36.795 | 42.106/36.795 | 40.010/36.169 |
| 2560×1440 | High | 75% | Weg | 23.38 | 27.34 | 42.779 | 36.577 | -6.348, -5.525, -6.812 | -6.348 | 47.845/39.150 | 1.835/1.516 | 42.816/37.395 | 42.816/37.395 | 40.210/36.722 |
| 2560×1440 | High | 100% | Wald | 17.76 | 20.82 | 56.310 | 48.032 | -5.477, -8.324, -5.910 | -5.910 | 63.961/53.419 | 1.976/1.940 | 56.280/48.028 | 56.280/48.028 | 54.422/47.642 |
| 2560×1440 | High | 100% | Weg | 17.79 | 18.89 | 56.202 | 52.934 | -4.191, -3.262, -7.803 | -4.191 | 60.094/63.440 | 1.998/1.866 | 56.198/54.170 | 56.198/54.170 | 54.675/53.734 |
| 2560×1440 | High | 100% | Dorf | 23.26 | 26.84 | 42.992 | 37.257 | -5.342, -5.735, -3.850 | -5.342 | 44.298/38.321 | 1.908/1.909 | 42.997/36.856 | 42.997/36.856 | 41.501/36.573 |

## 10. Bilder und Datennachweise

Alle folgenden PNGs sind echte 2560×1440-Unreal-Captures. Clientdarstellung kann kleiner sein.

- [FootTest_Interior_V1_QHD00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Interior_V1_QHD00000.png)
- [FootTest_Interior_V2_QHD00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Interior_V2_QHD00000.png)
- [FootTest_Native_BachBruecke00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Native_BachBruecke00000.png)
- [FootTest_Native_CrownReveal_On00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Native_CrownReveal_On00000.png)
- [FootTest_Native_DichterWald00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Native_DichterWald00000.png)
- [FootTest_Native_Dorf00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Native_Dorf00000.png)
- [FootTest_Native_Heilhaus00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Native_Heilhaus00000.png)
- [FootTest_Native_Ruinen00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Native_Ruinen00000.png)
- [FootTest_Ranger_Conversation00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FootTest_Ranger_Conversation00000.png)
- [FinalExteriorQHD_00_Weg_V100000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FinalExteriorQHD_00_Weg_V100000.png)
- [FinalExteriorQHD_01_Weg_V200000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FinalExteriorQHD_01_Weg_V200000.png)
- [FinalExteriorQHD_02_Clearing_V100000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FinalExteriorQHD_02_Clearing_V100000.png)
- [FinalExteriorQHD_03_Clearing_V200000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FinalExteriorQHD_03_Clearing_V200000.png)
- [FinalExteriorQHD_04_Archiv_V100000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FinalExteriorQHD_04_Archiv_V100000.png)
- [FinalExteriorQHD_05_Archiv_V200000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/FinalExteriorQHD_05_Archiv_V200000.png)
- [LightingCandidatesQHD_00_Dorf_V100000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/LightingCandidatesQHD_00_Dorf_V100000.png)
- [LightingCandidatesQHD_03_Dorf_IrradianceSoftware00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/LightingCandidatesQHD_03_Dorf_IrradianceSoftware00000.png)
- [LightingCandidatesQHD_04_Wald_V100000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/LightingCandidatesQHD_04_Wald_V100000.png)
- [LightingCandidatesQHD_07_Wald_IrradianceSoftware00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/LightingCandidatesQHD_07_Wald_IrradianceSoftware00000.png)
- [LightingCandidatesQHD_08_NPCWald_V100000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/LightingCandidatesQHD_08_NPCWald_V100000.png)
- [LightingCandidatesQHD_11_NPCWald_IrradianceSoftware00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/LightingCandidatesQHD_11_NPCWald_IrradianceSoftware00000.png)
- [LightingCandidatesQHD_12_Crown_V100000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/LightingCandidatesQHD_12_Crown_V100000.png)
- [LightingCandidatesQHD_15_Crown_IrradianceSoftware00000.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/Screenshots/LightingCandidatesQHD_15_Crown_IrradianceSoftware00000.png)

Nachweise:

- [MeasurementsResolved.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/MeasurementsResolved.json)
- [MeasurementSelection.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/MeasurementSelection.json)
- [StrictValidation.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/StrictValidation.json)
- [SustainedAnalysis.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/SustainedAnalysis.json)
- [FootTest.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/FootTest.json)
- [FinalMapAudit.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/FinalMapAudit.json)
- [MapCheck.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/MapCheck.json)
- [GPUProfile_QHD_Verified.txt](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/GPUProfile_QHD_Verified.txt)
- [WarningsSummary.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/WarningsSummary.json)
- [ProtectedFinal.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/ProtectedFinal.json)
- [FinalEditorState.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/FinalEditorState.json)
- [EvidenceManifest.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/EvidenceManifest.json)
- [RawMeasurements.zip](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/EnvironmentPerfV2/Review/RawMeasurements.zip)

## 11. Neue Dateien und Git

Neue Karte und Development-C++/Testdateien:

- [Content/Maps/Dev_TestMap_EnvironmentPerfV2.umap](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Content/Maps/Dev_TestMap_EnvironmentPerfV2.umap)
- [Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV2.cpp](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV2.cpp)
- [Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfileV2.cpp](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfileV2.cpp)
- [Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfileV2.h](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfileV2.h)
- [Source/PokeMonster/Tests/PokeMonsterEnvironmentProfileV2Test.cpp](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Source/PokeMonster/Tests/PokeMonsterEnvironmentProfileV2Test.cpp)
- [Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V2_PRUEFBERICHT.md](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V2_PRUEFBERICHT.md)

Neue Werkzeuge/Pläne:

- [Tools/EnvironmentPerfV2/AfterFoot.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/AfterFoot.py)
- [Tools/EnvironmentPerfV2/AnalyzeSustained.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/AnalyzeSustained.py)
- [Tools/EnvironmentPerfV2/AuditScene.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/AuditScene.py)
- [Tools/EnvironmentPerfV2/BeforeFoot.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/BeforeFoot.py)
- [Tools/EnvironmentPerfV2/BuildAndLaunch.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/BuildAndLaunch.py)
- [Tools/EnvironmentPerfV2/CaptureGPU.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/CaptureGPU.py)
- [Tools/EnvironmentPerfV2/CloseForBuild.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/CloseForBuild.py)
- [Tools/EnvironmentPerfV2/Control.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Control.py)
- [Tools/EnvironmentPerfV2/CreateTestMap.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/CreateTestMap.py)
- [Tools/EnvironmentPerfV2/CubeGroundAudit.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/CubeGroundAudit.py)
- [Tools/EnvironmentPerfV2/FinalEditorCleanup.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/FinalEditorCleanup.py)
- [Tools/EnvironmentPerfV2/FinalMapAudit.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/FinalMapAudit.py)
- [Tools/EnvironmentPerfV2/FootTest.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/FootTest.py)
- [Tools/EnvironmentPerfV2/GPUCaptureVerified.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/GPUCaptureVerified.py)
- [Tools/EnvironmentPerfV2/InspectRuntime.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/InspectRuntime.py)
- [Tools/EnvironmentPerfV2/MCPClient.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/MCPClient.py)
- [Tools/EnvironmentPerfV2/PackageEvidence.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/PackageEvidence.py)
- [Tools/EnvironmentPerfV2/PersistCandidate.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/PersistCandidate.py)
- [Tools/EnvironmentPerfV2/Plans/FactorsFollowup.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/FactorsFollowup.tsv)
- [Tools/EnvironmentPerfV2/Plans/FactorsQHD.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/FactorsQHD.tsv)
- [Tools/EnvironmentPerfV2/Plans/FinalExteriorQHD.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/FinalExteriorQHD.tsv)
- [Tools/EnvironmentPerfV2/Plans/FinalPairedPIE.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/FinalPairedPIE.tsv)
- [Tools/EnvironmentPerfV2/Plans/GPUCapture.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/GPUCapture.tsv)
- [Tools/EnvironmentPerfV2/Plans/GPUCaptureFinal.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/GPUCaptureFinal.tsv)
- [Tools/EnvironmentPerfV2/Plans/GPUCaptureVerified.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/GPUCaptureVerified.tsv)
- [Tools/EnvironmentPerfV2/Plans/LightingCandidatesQHD.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/LightingCandidatesQHD.tsv)
- [Tools/EnvironmentPerfV2/Plans/PacingFullscreen.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/PacingFullscreen.tsv)
- [Tools/EnvironmentPerfV2/Plans/PacingWindowed.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/PacingWindowed.tsv)
- [Tools/EnvironmentPerfV2/Plans/RepairNative1.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/RepairNative1.tsv)
- [Tools/EnvironmentPerfV2/Plans/RepairNative2.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/RepairNative2.tsv)
- [Tools/EnvironmentPerfV2/Plans/RepairNativeHighDorf.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/RepairNativeHighDorf.tsv)
- [Tools/EnvironmentPerfV2/Plans/RepairPIEQHD.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/RepairPIEQHD.tsv)
- [Tools/EnvironmentPerfV2/Plans/StandalonePair1.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/StandalonePair1.tsv)
- [Tools/EnvironmentPerfV2/Plans/StandalonePair2.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/StandalonePair2.tsv)
- [Tools/EnvironmentPerfV2/Plans/StandalonePair3.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/StandalonePair3.tsv)
- [Tools/EnvironmentPerfV2/Plans/StandalonePair4.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/StandalonePair4.tsv)
- [Tools/EnvironmentPerfV2/Plans/StandalonePair5.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/StandalonePair5.tsv)
- [Tools/EnvironmentPerfV2/Plans/StandalonePair6.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/StandalonePair6.tsv)
- [Tools/EnvironmentPerfV2/Plans/SustainedQHD.tsv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Plans/SustainedQHD.tsv)
- [Tools/EnvironmentPerfV2/PrepareEditor.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/PrepareEditor.py)
- [Tools/EnvironmentPerfV2/Queue.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Queue.py)
- [Tools/EnvironmentPerfV2/README.md](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/README.md)
- [Tools/EnvironmentPerfV2/ReadFrameLimits.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/ReadFrameLimits.py)
- [Tools/EnvironmentPerfV2/ReopenFinalEditor.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/ReopenFinalEditor.py)
- [Tools/EnvironmentPerfV2/ResolveMeasurements.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/ResolveMeasurements.py)
- [Tools/EnvironmentPerfV2/RestoreDevSave.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/RestoreDevSave.py)
- [Tools/EnvironmentPerfV2/ReviewShots.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/ReviewShots.py)
- [Tools/EnvironmentPerfV2/RunAutomation.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/RunAutomation.py)
- [Tools/EnvironmentPerfV2/RunInEditor.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/RunInEditor.py)
- [Tools/EnvironmentPerfV2/RunStandalone.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/RunStandalone.py)
- [Tools/EnvironmentPerfV2/RuntimeMonitor.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/RuntimeMonitor.py)
- [Tools/EnvironmentPerfV2/StartFoot.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/StartFoot.py)
- [Tools/EnvironmentPerfV2/StartProbe.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/StartProbe.py)
- [Tools/EnvironmentPerfV2/StrictValidation.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/StrictValidation.py)
- [Tools/EnvironmentPerfV2/Summarize.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/Summarize.py)
- [Tools/EnvironmentPerfV2/ThermalMonitor.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/ThermalMonitor.py)
- [Tools/EnvironmentPerfV2/VerifyPreservation.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/VerifyPreservation.py)
- [Tools/EnvironmentPerfV2/WriteTables.py](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Tools/EnvironmentPerfV2/WriteTables.py)

Reviewpaket: Art/World/EnvironmentPerfV2/Review/, vollständige Einzeldateien mit SHA256 in EvidenceManifest.json. Rohdaten zusätzlich unter Saved/EnvironmentPerfV2; nichts davon gelöscht. Vorhandene modifizierte Dateien im Git-Status gehören zu den bytegleich erhaltenen Vorarbeiten. Keine Zuordnung fremder Dateien zum V2-Auftrag. Kein Commit, kein Push, nichts gestaged.

git diff --check: bestanden, Exit 0, keine Ausgabe.

Anfangsstatus:

```text
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
```

Abschließendes git status --short:

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
?? Content/Characters/NPCs/
?? Content/Maps/Dev_TestMap_EnvironmentPerfV1.umap
?? Content/Maps/Dev_TestMap_EnvironmentPerfV2.umap
?? Content/Maps/Dev_TestMap_RangerPerfV2.umap
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V1_PRUEFBERICHT.md
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V2_PRUEFBERICHT.md
?? Docs/MESHY_NPC_INTEGRATION_V1_PRUEFBERICHT.md
?? Docs/POKEMONSTER_PERFORMANCE_RANGER_V2_PRUEFBERICHT.md
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.h
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.h
?? Source/PokeMonster/Development/
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentProfileV2Test.cpp
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentRenderProfileTest.cpp
?? Source/PokeMonster/Tests/PokeMonsterNPCPresentationTest.cpp
?? Tools/EnvironmentPerfV1/
?? Tools/EnvironmentPerfV2/
?? Tools/MeshyNPCIntegrationV1/
?? Tools/PerformanceRangerV2/
```
