# VisualV2 TAA/TSR & Soft Shadows V1 – Prüfbericht

## Ergebnis und Freigabegrenze

**TAA (B) ist der bevorzugte Kandidat für eine spätere gezielte Übernahmeprüfung. Die pauschalen Baum-Bodenprojektionen (C) und die Kombination (D) werden vorerst nicht für die zentrale Map empfohlen.** TAA spart besonders bei QHD deutlich GPU-Zeit. Weiche Flecken funktionieren technisch, ersetzen aber die Eigen-/Umgebungsverschattung großer Bäume nicht gleichwertig. Unveränderte Lichtparameter beweisen keine identische Lichtwirkung. VisualV2 bleibt unverändert; Harrys visuelle Freigabe wird nicht vorweggenommen.

Es wurde **keine neue Map erstellt und keine vorhandene Map gespeichert**. Versuche ausschließlich zur Laufzeit in `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1`. Die zentrale VisualV2 bleibt unverändert auf TSR und Originalschatten. Keine automatische Übernahme. Sonnen-/Skylight-Werte, Belichtung, Lumen, Bloom, Nebel und Innenraumbeleuchtung wurden nicht als Optimierung geändert.

## Ausgangslage und Schutz

Slim-Worktree: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`. Ausgangs-HEAD und direkt geprüfter origin/main: `a87b7b07111f6b13fe68d6e1e1fe7588067685e3`. Branch `codex/slim-backup-v5`. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt auf altem main und Archiv-Ref erhalten und wird nicht in die Remote-Historie aufgenommen.

Vorgefundene unversionierte Arbeiten `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap` und `Tools/VisualV2EnvironmentQualityV1/` bleiben unangetastet und ausgeschlossen. Vorher-SHA-Inventar: 2945 Dateien. Vollständige Schutzprüfung: [ProtectionAudit](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/ProtectionAudit.json).

Vorhandene Karten wurden geprüft; die gespeicherte GPU-Diagnosekarte entspricht nach Normalisierung des Paketnamens der aktuellen VisualV2-Szene. EnvironmentPerf-Varianten enthalten andere Versuchsbedingungen und wurden nicht als vermeintlich gleichwertige Ausgangsbasis übernommen. TreeShadowProxyV1 bleibt ein begrenztes, nicht allgemein freigegebenes früheres Experiment. Die aktuelle Strauch-Instancing-Materialkorrektur ist enthalten.

## Varianten und technische Umsetzung

| Variante | AA | Schatten |
|---|---|---|
| A | TSR, Methode 4 | Original |
| B | TAA, Methode 2 | Original |
| C | TSR | weiche Bodenprojektionen |
| D | TAA | weiche Bodenprojektionen |

Neue Assets ausschließlich unter `/Game/Development/VisualV2AASoftShadowsV1`: `M_SoftGroundBlob`, `MI_TreeBlob`, `MI_FigureBlob`. Gemeinsamer texturloser Deferred-Decal-Master, schwarze Base Color mit weich fallender, leicht gelappter Deckkraft. Dichte 0,45 für Bäume und 0,50 für Figuren. Keine Blatt-/Astkonturen. Nur Color/Opacity angeschlossen; keine Normal-/Roughness-/Specular-/Metallic-Eingänge. Der lokale Renderer `DecalRenderingCommon.cpp` leitet die tatsächlich geschriebenen Kanäle aus angeschlossenen Materialeigenschaften ab. Bestehende Empfängermaterialien werden nicht geändert.

45 sichtbare Eichen-/Birkenkomponenten und fünf Figuren ergeben im aktuellen Versuch 50 Projektoren, nicht 50 zwingend gleichzeitig sichtbare Draw Calls. Frustum-/Screen-Size-Culling bleibt wirksam. 46 Strauch- und vier kleine Pflanzenkomponenten erhalten keine zusätzlichen Flecken; ihre Einzelschatten werden in C/D deaktiviert, soweit vorher vorhanden. Dynamische Schatten bleiben an Gebäuden und nicht ausgewählten Objekten erhalten. Keine pauschale DirectionalLight-Abschaltung.

Der opt-in Development-Befehl `pm.SoftShadows.Test` ist auf diese vorhandene Testwelt begrenzt. Er speichert ursprüngliche CastShadow-Werte, erzeugt nur Runtime-Helfer ohne Kollision und stellt alle Werte beim Stop wieder her. Kein Start beim Laden einer Map. Figuren folgen pro Frame; WorldStatic-Bodenabfrage höchstens alle 0,05 s und unmittelbare Neuabfrage bei großem Ortswechsel. Zwischen Abfragen lokale Bodenebene. Verdeckte/deaktivierte aktuelle Quellfiguren werden berücksichtigt. Später neu gespawnte Figuren werden in diesem begrenzten Prototyp noch nicht automatisch registriert.

Rückgabeprüfung: 47 tatsächlich umgeschaltete Schattenkomponenten; 18 Lichtkomponenten und 2 vollständige Postprocess-Volumes unverändert. Originale Komponenten-/Material-/Transform-/Collision-Zustände nach Stop exakt zurückgegeben. [Runtime-Invarianten](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/RuntimeInvariant.json).

Kamera B 2850 cm / −50° / −45° / FOV 35°, Playerhöhe 140 cm, Gehen 210 und Sprint 315 cm/s sowie Eingaben, Kollisionen, NPC-/Quest-/Kampflogik bleiben unverändert.

## Messmethode und Auflösungen

1280×720 und 2560×1440, jeweils Medium/High und 75/100 %, PIE und Standalone getrennt. Acht feste Konfigurationen pro Modus. Drei Orte: Dorf/Heilhaus (-4100,450,50,15), Wald (-4300,1550,50,15), Weg (-36,6,-47,1,50,15) cm. Drei Wiederholungen; A/B/D/C beziehungsweise umgekehrte Reihenfolge interleavt. Pro Segment 3 s Warm-up + 3 s Messung. 576 reguläre Segmente, 192 Drei-Lauf-Zusammenfassungen. Fotos und Drainzeilen außerhalb der Timingwertung.

FPS = 1000 / Median der drei Laufmediane. P95 = Median der drei Lauf-P95, kein gepooltes Gesamt-P95. Kurze Fenster begrenzen kleine Unterschiede und sind keine Dauer-FPS-Garantie. Alle bislang verlangten Auflösungskombinationen wurden anhand von Viewport, Target, ViewRect und fortlaufenden Renderer-Beobachtungen geprüft. Interne Größen: 960×540/1280×720 beziehungsweise 1920×1080/2560×1440. Interne Maße sind aus dem Renderer-Screen-Percentage-Treiber abgeleitet, kein direkter Pufferreadback. Fenster-/DPI-Daten separat im Rohdatensatz; Renderausgabe nicht mit logischer macOS-Fenstergröße verwechseln.

Scalability vor frischem PIE gesetzt; keine High→Medium-Umschaltung mit lebenden Reveal-MIDs. Zwischen Qualitätsprofilen gelten die originalen Scalability-Vorgaben, innerhalb eines Profils sind Lumen/Reflections/VSM/Bloom identisch für A–D. VSync=0, t.MaxFPS=0, Dynamic Resolution=0. `rhi.SyncInterval=1` blieb bestehen; Fälle nahe 60 FPS können präsentationsbegrenzt sein. Keine künstliche FPS-Verbesserung aus unterschiedlichen Renderauflösungen.

Standalone ist UnrealEditor Development `-game` bei geschlossenem Editor, kein paketierter Shipping-Build. GPU-Zeit aus verfügbaren Unreal-CSV-Zählern. Game-/Renderthread-Scopes enthalten Wartezeiten beziehungsweise teils Nullwerte; Null-Draw-Call-Zähler sind keine Messung kostenloser Arbeit. Verschachtelte GPU-Scopes nicht addieren. Begleitende thermische Stichproben: {'fair': 596, 'nominal': 134}; Netzbetrieb laut Energieprotokoll. Kein Temperatur-/Takt-Sensorbeweis. Leichte Auswertungs-/Steuerprozesse und mögliche Zeitdrift begrenzen kleine Submillisekunden-Schlüsse.

## Vollständige Ergebnistabelle

Zeiten in ms. GPU/ShadowProjection und GPU/ShadowDepths sind verfügbare CSV-Scopes; keine vollständige Summe aller Schattenarbeit.

| Modus | Ausgabe | Profil/SP | Ort | Variante | FPS | Median | P95 | GPU | Game | Render | Schattenprojektion | Schattentiefe |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PIE | 1280×720 | Medium/75 % | Dorf | A | 55.19 | 18.12 | 21.54 | 17.08 | 7.10 | 0.00 | 0.55 | 1.36 |
| PIE | 1280×720 | Medium/75 % | Dorf | B | 59.83 | 16.71 | 20.42 | 15.59 | 7.66 | 0.00 | 0.55 | 1.33 |
| PIE | 1280×720 | Medium/75 % | Dorf | C | 55.04 | 18.17 | 21.63 | 17.02 | 7.10 | 0.00 | 0.44 | 1.27 |
| PIE | 1280×720 | Medium/75 % | Dorf | D | 59.91 | 16.69 | 20.20 | 15.45 | 7.53 | 0.00 | 0.44 | 1.27 |
| PIE | 1280×720 | Medium/75 % | Wald | A | 56.57 | 17.68 | 21.77 | 16.74 | 7.23 | 0.00 | 0.57 | 1.31 |
| PIE | 1280×720 | Medium/75 % | Wald | B | 60.03 | 16.66 | 17.06 | 14.93 | 7.38 | 0.00 | 0.53 | 1.24 |
| PIE | 1280×720 | Medium/75 % | Wald | C | 55.59 | 17.99 | 21.66 | 16.79 | 7.11 | 0.00 | 0.46 | 1.27 |
| PIE | 1280×720 | Medium/75 % | Wald | D | 60.00 | 16.67 | 16.99 | 15.37 | 7.46 | 0.00 | 0.45 | 1.22 |
| PIE | 1280×720 | Medium/75 % | Weg | A | 53.78 | 18.59 | 22.76 | 17.67 | 6.89 | 0.00 | 0.59 | 1.16 |
| PIE | 1280×720 | Medium/75 % | Weg | B | 58.57 | 17.07 | 19.81 | 15.88 | 7.40 | 0.00 | 0.60 | 1.17 |
| PIE | 1280×720 | Medium/75 % | Weg | C | 53.84 | 18.57 | 22.86 | 17.67 | 7.28 | 0.00 | 0.44 | 1.15 |
| PIE | 1280×720 | Medium/75 % | Weg | D | 59.26 | 16.88 | 19.64 | 15.67 | 7.35 | 0.00 | 0.45 | 1.14 |
| PIE | 1280×720 | Medium/100 % | Dorf | A | 44.89 | 22.28 | 26.51 | 21.38 | 6.05 | 0.00 | 0.99 | 1.43 |
| PIE | 1280×720 | Medium/100 % | Dorf | B | 52.96 | 18.88 | 22.69 | 18.02 | 7.18 | 0.00 | 0.95 | 1.40 |
| PIE | 1280×720 | Medium/100 % | Dorf | C | 45.21 | 22.12 | 26.46 | 21.38 | 6.53 | 0.00 | 0.80 | 1.39 |
| PIE | 1280×720 | Medium/100 % | Dorf | D | 53.56 | 18.67 | 23.09 | 17.86 | 7.48 | 0.00 | 0.76 | 1.38 |
| PIE | 1280×720 | Medium/100 % | Wald | A | 45.66 | 21.90 | 26.27 | 20.93 | 5.99 | 0.00 | 0.98 | 1.46 |
| PIE | 1280×720 | Medium/100 % | Wald | B | 54.61 | 18.31 | 22.55 | 17.42 | 6.44 | 0.00 | 0.94 | 1.44 |
| PIE | 1280×720 | Medium/100 % | Wald | C | 46.53 | 21.49 | 25.94 | 20.59 | 5.98 | 0.00 | 0.78 | 1.42 |
| PIE | 1280×720 | Medium/100 % | Wald | D | 55.08 | 18.16 | 22.55 | 17.24 | 6.64 | 0.00 | 0.77 | 1.41 |
| PIE | 1280×720 | Medium/100 % | Weg | A | 45.44 | 22.01 | 26.16 | 21.34 | 5.91 | 0.00 | 1.02 | 1.30 |
| PIE | 1280×720 | Medium/100 % | Weg | B | 52.93 | 18.89 | 23.08 | 17.97 | 6.62 | 0.00 | 1.00 | 1.28 |
| PIE | 1280×720 | Medium/100 % | Weg | C | 45.84 | 21.81 | 26.33 | 20.98 | 6.57 | 0.00 | 0.77 | 1.27 |
| PIE | 1280×720 | Medium/100 % | Weg | D | 53.37 | 18.74 | 22.69 | 17.83 | 7.39 | 0.00 | 0.77 | 1.26 |
| PIE | 1280×720 | High/75 % | Dorf | A | 45.03 | 22.21 | 26.83 | 20.71 | 7.19 | 0.00 | 0.91 | 1.40 |
| PIE | 1280×720 | High/75 % | Dorf | B | 48.69 | 20.54 | 29.22 | 18.50 | 7.71 | 0.00 | 0.88 | 1.39 |
| PIE | 1280×720 | High/75 % | Dorf | C | 45.59 | 21.93 | 26.64 | 20.62 | 7.54 | 0.00 | 0.58 | 1.32 |
| PIE | 1280×720 | High/75 % | Dorf | D | 50.84 | 19.67 | 24.02 | 18.08 | 7.67 | 0.00 | 0.58 | 1.31 |
| PIE | 1280×720 | High/75 % | Wald | A | 45.66 | 21.90 | 25.98 | 20.21 | 6.72 | 0.00 | 0.90 | 1.34 |
| PIE | 1280×720 | High/75 % | Wald | B | 51.13 | 19.56 | 23.19 | 17.75 | 7.28 | 0.00 | 0.87 | 1.34 |
| PIE | 1280×720 | High/75 % | Wald | C | 48.04 | 20.82 | 25.06 | 19.74 | 6.63 | 0.00 | 0.53 | 1.31 |
| PIE | 1280×720 | High/75 % | Wald | D | 54.99 | 18.19 | 22.53 | 17.11 | 7.29 | 0.00 | 0.52 | 1.31 |
| PIE | 1280×720 | High/75 % | Weg | A | 44.44 | 22.50 | 26.60 | 21.35 | 6.58 | 0.00 | 1.02 | 1.20 |
| PIE | 1280×720 | High/75 % | Weg | B | 48.67 | 20.55 | 24.48 | 18.88 | 7.11 | 0.00 | 1.04 | 1.19 |
| PIE | 1280×720 | High/75 % | Weg | C | 45.50 | 21.98 | 26.63 | 20.60 | 6.56 | 0.00 | 0.53 | 1.18 |
| PIE | 1280×720 | High/75 % | Weg | D | 50.65 | 19.74 | 24.16 | 18.16 | 7.48 | 0.00 | 0.52 | 1.17 |
| PIE | 1280×720 | High/100 % | Dorf | A | 33.74 | 29.64 | 32.09 | 26.97 | 6.01 | 0.00 | 1.66 | 1.45 |
| PIE | 1280×720 | High/100 % | Dorf | B | 43.04 | 23.23 | 27.31 | 21.59 | 7.28 | 0.00 | 1.61 | 1.44 |
| PIE | 1280×720 | High/100 % | Dorf | C | 35.58 | 28.11 | 31.20 | 26.17 | 6.66 | 0.00 | 1.04 | 1.41 |
| PIE | 1280×720 | High/100 % | Dorf | D | 45.75 | 21.86 | 26.71 | 21.11 | 6.69 | 0.00 | 1.03 | 1.39 |
| PIE | 1280×720 | High/100 % | Wald | A | 36.64 | 27.29 | 31.16 | 25.47 | 6.18 | 0.00 | 1.59 | 1.48 |
| PIE | 1280×720 | High/100 % | Wald | B | 43.70 | 22.88 | 27.19 | 21.07 | 6.57 | 0.00 | 1.58 | 1.47 |
| PIE | 1280×720 | High/100 % | Wald | C | 36.30 | 27.55 | 31.10 | 26.21 | 6.10 | 0.00 | 0.99 | 1.45 |
| PIE | 1280×720 | High/100 % | Wald | D | 46.17 | 21.66 | 26.07 | 20.54 | 6.50 | 0.00 | 0.98 | 1.43 |
| PIE | 1280×720 | High/100 % | Weg | A | 34.42 | 29.05 | 31.92 | 26.77 | 6.02 | 0.00 | 1.82 | 1.32 |
| PIE | 1280×720 | High/100 % | Weg | B | 42.39 | 23.59 | 27.99 | 22.15 | 6.64 | 0.00 | 1.82 | 1.32 |
| PIE | 1280×720 | High/100 % | Weg | C | 34.63 | 28.88 | 31.26 | 28.05 | 6.13 | 0.00 | 0.97 | 1.30 |
| PIE | 1280×720 | High/100 % | Weg | D | 43.52 | 22.98 | 26.58 | 22.16 | 6.85 | 0.00 | 0.97 | 1.29 |
| PIE | 2560×1440 | Medium/75 % | Dorf | A | 28.39 | 35.23 | 42.22 | 34.03 | 5.51 | 0.00 | 2.43 | 1.74 |
| PIE | 2560×1440 | Medium/75 % | Dorf | B | 32.66 | 30.62 | 32.84 | 29.61 | 6.09 | 0.00 | 2.45 | 1.70 |
| PIE | 2560×1440 | Medium/75 % | Dorf | C | 28.60 | 34.97 | 41.58 | 33.82 | 6.13 | 0.00 | 1.97 | 1.67 |
| PIE | 2560×1440 | Medium/75 % | Dorf | D | 33.16 | 30.16 | 32.94 | 29.40 | 6.60 | 0.00 | 2.02 | 1.66 |
| PIE | 2560×1440 | Medium/75 % | Wald | A | 29.37 | 34.04 | 40.65 | 33.14 | 5.47 | 0.00 | 2.37 | 1.76 |
| PIE | 2560×1440 | Medium/75 % | Wald | B | 34.23 | 29.21 | 32.41 | 28.27 | 5.74 | 0.00 | 2.48 | 1.72 |
| PIE | 2560×1440 | Medium/75 % | Wald | C | 29.55 | 33.84 | 40.74 | 32.90 | 5.38 | 0.00 | 2.01 | 1.69 |
| PIE | 2560×1440 | Medium/75 % | Wald | D | 34.17 | 29.27 | 32.24 | 27.95 | 5.95 | 0.00 | 1.98 | 1.68 |
| PIE | 2560×1440 | Medium/75 % | Weg | A | 28.55 | 35.03 | 43.15 | 33.96 | 5.55 | 0.00 | 2.63 | 1.58 |
| PIE | 2560×1440 | Medium/75 % | Weg | B | 32.59 | 30.69 | 32.98 | 29.94 | 6.05 | 0.00 | 2.61 | 1.56 |
| PIE | 2560×1440 | Medium/75 % | Weg | C | 28.99 | 34.49 | 40.95 | 33.72 | 5.59 | 0.00 | 1.96 | 1.58 |
| PIE | 2560×1440 | Medium/75 % | Weg | D | 33.23 | 30.09 | 32.18 | 29.55 | 5.89 | 0.00 | 2.00 | 1.53 |
| PIE | 2560×1440 | Medium/100 % | Dorf | A | 19.24 | 51.97 | 61.31 | 50.76 | 6.53 | 0.00 | 4.29 | 2.14 |
| PIE | 2560×1440 | Medium/100 % | Dorf | B | 25.54 | 39.15 | 45.51 | 37.28 | 6.02 | 0.00 | 4.36 | 2.06 |
| PIE | 2560×1440 | Medium/100 % | Dorf | C | 19.14 | 52.26 | 57.90 | 51.06 | 6.61 | 0.00 | 3.52 | 2.06 |
| PIE | 2560×1440 | Medium/100 % | Dorf | D | 25.17 | 39.72 | 44.51 | 39.18 | 6.12 | 0.00 | 3.61 | 2.10 |
| PIE | 2560×1440 | Medium/100 % | Wald | A | 19.17 | 52.16 | 57.72 | 50.77 | 6.58 | 0.00 | 4.37 | 2.31 |
| PIE | 2560×1440 | Medium/100 % | Wald | B | 25.99 | 38.48 | 46.36 | 37.21 | 6.12 | 0.00 | 4.43 | 2.34 |
| PIE | 2560×1440 | Medium/100 % | Wald | C | 19.55 | 51.16 | 60.51 | 49.74 | 6.80 | 0.00 | 3.63 | 2.28 |
| PIE | 2560×1440 | Medium/100 % | Wald | D | 26.44 | 37.83 | 45.63 | 36.60 | 6.83 | 0.00 | 3.63 | 2.23 |
| PIE | 2560×1440 | Medium/100 % | Weg | A | 19.17 | 52.15 | 60.45 | 51.34 | 6.48 | 0.00 | 4.57 | 2.00 |
| PIE | 2560×1440 | Medium/100 % | Weg | B | 26.02 | 38.43 | 44.32 | 36.99 | 6.00 | 0.00 | 4.56 | 1.99 |
| PIE | 2560×1440 | Medium/100 % | Weg | C | 19.02 | 52.58 | 61.25 | 51.42 | 6.84 | 0.00 | 3.60 | 1.99 |
| PIE | 2560×1440 | Medium/100 % | Weg | D | 25.44 | 39.30 | 45.19 | 38.15 | 6.16 | 0.00 | 3.64 | 2.08 |
| PIE | 2560×1440 | High/75 % | Dorf | A | 20.59 | 48.56 | 54.28 | 46.50 | 6.34 | 0.00 | 3.67 | 1.78 |
| PIE | 2560×1440 | High/75 % | Dorf | B | 25.39 | 39.39 | 45.75 | 36.71 | 5.93 | 0.00 | 3.74 | 1.77 |
| PIE | 2560×1440 | High/75 % | Dorf | C | 21.12 | 47.34 | 53.94 | 45.83 | 6.40 | 0.00 | 2.46 | 1.72 |
| PIE | 2560×1440 | High/75 % | Dorf | D | 27.32 | 36.61 | 44.94 | 34.73 | 6.49 | 0.00 | 2.45 | 1.78 |
| PIE | 2560×1440 | High/75 % | Wald | A | 20.73 | 48.24 | 52.96 | 45.70 | 6.24 | 0.00 | 3.77 | 1.79 |
| PIE | 2560×1440 | High/75 % | Wald | B | 25.96 | 38.52 | 47.10 | 36.09 | 6.73 | 0.00 | 3.88 | 1.93 |
| PIE | 2560×1440 | High/75 % | Wald | C | 21.44 | 46.64 | 52.87 | 45.06 | 6.18 | 0.00 | 2.42 | 1.76 |
| PIE | 2560×1440 | High/75 % | Wald | D | 28.82 | 34.70 | 42.56 | 32.71 | 6.19 | 0.00 | 2.40 | 1.76 |
| PIE | 2560×1440 | High/75 % | Weg | A | 20.01 | 49.98 | 57.25 | 47.88 | 6.36 | 0.00 | 4.32 | 1.61 |
| PIE | 2560×1440 | High/75 % | Weg | B | 25.17 | 39.74 | 45.82 | 36.19 | 6.00 | 0.00 | 4.30 | 1.62 |
| PIE | 2560×1440 | High/75 % | Weg | C | 20.98 | 47.67 | 53.45 | 45.56 | 6.41 | 0.00 | 2.37 | 1.58 |
| PIE | 2560×1440 | High/75 % | Weg | D | 27.71 | 36.09 | 44.33 | 34.25 | 6.16 | 0.00 | 2.39 | 1.54 |
| PIE | 2560×1440 | High/100 % | Dorf | A | 14.55 | 68.73 | 78.03 | 67.00 | 7.09 | 0.00 | 6.45 | 2.17 |
| PIE | 2560×1440 | High/100 % | Dorf | B | 19.39 | 51.58 | 58.93 | 48.19 | 6.73 | 0.00 | 6.52 | 2.16 |
| PIE | 2560×1440 | High/100 % | Dorf | C | 14.89 | 67.16 | 78.41 | 65.72 | 7.25 | 0.00 | 4.36 | 2.01 |
| PIE | 2560×1440 | High/100 % | Dorf | D | 19.96 | 50.10 | 55.52 | 47.23 | 6.71 | 0.00 | 4.31 | 2.07 |
| PIE | 2560×1440 | High/100 % | Wald | A | 14.55 | 68.74 | 82.40 | 66.45 | 7.12 | 0.00 | 6.57 | 2.34 |
| PIE | 2560×1440 | High/100 % | Wald | B | 19.86 | 50.35 | 57.72 | 47.78 | 6.65 | 0.00 | 6.53 | 2.39 |
| PIE | 2560×1440 | High/100 % | Wald | C | 14.93 | 66.97 | 75.12 | 64.69 | 7.08 | 0.00 | 4.31 | 2.16 |
| PIE | 2560×1440 | High/100 % | Wald | D | 20.92 | 47.79 | 54.85 | 45.97 | 6.54 | 0.00 | 4.28 | 2.28 |
| PIE | 2560×1440 | High/100 % | Weg | A | 14.12 | 70.83 | 82.22 | 67.20 | 7.33 | 0.00 | 7.35 | 2.10 |
| PIE | 2560×1440 | High/100 % | Weg | B | 18.87 | 52.98 | 61.29 | 50.40 | 6.86 | 0.00 | 7.29 | 2.09 |
| PIE | 2560×1440 | High/100 % | Weg | C | 14.80 | 67.57 | 78.49 | 64.10 | 7.46 | 0.00 | 4.25 | 1.94 |
| PIE | 2560×1440 | High/100 % | Weg | D | 19.90 | 50.24 | 55.94 | 47.82 | 6.77 | 0.00 | 4.26 | 2.04 |
| Standalone | 1280×720 | Medium/75 % | Dorf | A | 60.04 | 16.65 | 17.13 | 14.16 | 1.30 | 16.66 | 0.52 | 1.24 |
| Standalone | 1280×720 | Medium/75 % | Dorf | B | 60.03 | 16.66 | 17.08 | 13.86 | 1.43 | 16.65 | 0.57 | 1.34 |
| Standalone | 1280×720 | Medium/75 % | Dorf | C | 60.02 | 16.66 | 17.05 | 14.03 | 1.28 | 16.64 | 0.43 | 1.18 |
| Standalone | 1280×720 | Medium/75 % | Dorf | D | 60.02 | 16.66 | 17.00 | 13.86 | 1.37 | 16.65 | 0.46 | 1.35 |
| Standalone | 1280×720 | Medium/75 % | Wald | A | 60.03 | 16.66 | 17.08 | 13.31 | 1.33 | 16.65 | 0.53 | 1.21 |
| Standalone | 1280×720 | Medium/75 % | Wald | B | 60.03 | 16.66 | 17.07 | 12.80 | 1.48 | 16.66 | 0.64 | 1.41 |
| Standalone | 1280×720 | Medium/75 % | Wald | C | 60.11 | 16.64 | 17.07 | 13.88 | 1.38 | 16.65 | 0.42 | 1.19 |
| Standalone | 1280×720 | Medium/75 % | Wald | D | 60.01 | 16.66 | 17.07 | 12.80 | 1.42 | 16.66 | 0.50 | 1.38 |
| Standalone | 1280×720 | Medium/75 % | Weg | A | 60.00 | 16.67 | 17.08 | 14.20 | 1.27 | 16.67 | 0.53 | 1.04 |
| Standalone | 1280×720 | Medium/75 % | Weg | B | 60.02 | 16.66 | 17.09 | 13.93 | 1.32 | 16.66 | 0.62 | 1.14 |
| Standalone | 1280×720 | Medium/75 % | Weg | C | 60.01 | 16.66 | 17.04 | 14.02 | 1.28 | 16.66 | 0.41 | 1.04 |
| Standalone | 1280×720 | Medium/75 % | Weg | D | 59.99 | 16.67 | 17.01 | 14.18 | 1.39 | 16.66 | 0.45 | 1.14 |
| Standalone | 1280×720 | Medium/100 % | Dorf | A | 57.30 | 17.45 | 19.34 | 16.51 | 1.93 | 17.44 | 0.99 | 1.43 |
| Standalone | 1280×720 | Medium/100 % | Dorf | B | 60.00 | 16.67 | 17.10 | 13.22 | 1.72 | 16.66 | 0.91 | 1.31 |
| Standalone | 1280×720 | Medium/100 % | Dorf | C | 58.90 | 16.98 | 18.15 | 16.08 | 1.86 | 16.97 | 0.80 | 1.38 |
| Standalone | 1280×720 | Medium/100 % | Dorf | D | 60.04 | 16.66 | 17.06 | 12.82 | 1.49 | 16.66 | 0.71 | 1.27 |
| Standalone | 1280×720 | Medium/100 % | Wald | A | 59.48 | 16.81 | 18.60 | 16.04 | 1.89 | 16.79 | 0.98 | 1.45 |
| Standalone | 1280×720 | Medium/100 % | Wald | B | 60.00 | 16.67 | 17.18 | 12.75 | 1.42 | 16.66 | 0.91 | 1.39 |
| Standalone | 1280×720 | Medium/100 % | Wald | C | 58.57 | 17.07 | 18.48 | 16.23 | 1.66 | 17.06 | 0.79 | 1.43 |
| Standalone | 1280×720 | Medium/100 % | Wald | D | 60.03 | 16.66 | 17.13 | 12.72 | 1.44 | 16.65 | 0.73 | 1.35 |
| Standalone | 1280×720 | Medium/100 % | Weg | A | 58.68 | 17.04 | 18.61 | 16.17 | 1.93 | 17.05 | 1.05 | 1.31 |
| Standalone | 1280×720 | Medium/100 % | Weg | B | 60.06 | 16.65 | 17.08 | 13.42 | 1.86 | 16.66 | 0.96 | 1.20 |
| Standalone | 1280×720 | Medium/100 % | Weg | C | 56.90 | 17.57 | 19.95 | 16.79 | 2.00 | 17.55 | 0.78 | 1.29 |
| Standalone | 1280×720 | Medium/100 % | Weg | D | 60.04 | 16.65 | 17.09 | 13.06 | 1.79 | 16.65 | 0.71 | 1.18 |
| Standalone | 1280×720 | High/75 % | Dorf | A | 59.31 | 16.86 | 18.46 | 15.31 | 2.03 | 16.92 | 0.94 | 1.40 |
| Standalone | 1280×720 | High/75 % | Dorf | B | 60.05 | 16.65 | 17.16 | 12.32 | 1.98 | 16.65 | 0.85 | 1.30 |
| Standalone | 1280×720 | High/75 % | Dorf | C | 59.89 | 16.70 | 17.39 | 15.08 | 2.23 | 16.66 | 0.59 | 1.26 |
| Standalone | 1280×720 | High/75 % | Dorf | D | 60.06 | 16.65 | 19.40 | 12.73 | 2.56 | 16.65 | 0.54 | 1.21 |
| Standalone | 1280×720 | High/75 % | Wald | A | 60.01 | 16.66 | 17.22 | 14.99 | 1.98 | 16.66 | 0.94 | 1.31 |
| Standalone | 1280×720 | High/75 % | Wald | B | 60.00 | 16.67 | 17.03 | 12.38 | 1.82 | 16.66 | 0.86 | 1.26 |
| Standalone | 1280×720 | High/75 % | Wald | C | 59.99 | 16.67 | 17.02 | 14.18 | 1.80 | 16.66 | 0.53 | 1.26 |
| Standalone | 1280×720 | High/75 % | Wald | D | 60.05 | 16.65 | 17.15 | 12.51 | 1.36 | 16.65 | 0.51 | 1.22 |
| Standalone | 1280×720 | High/75 % | Weg | A | 57.90 | 17.27 | 19.06 | 15.92 | 1.99 | 17.29 | 1.08 | 1.20 |
| Standalone | 1280×720 | High/75 % | Weg | B | 59.97 | 16.68 | 17.10 | 12.77 | 1.81 | 16.65 | 0.97 | 1.13 |
| Standalone | 1280×720 | High/75 % | Weg | C | 59.29 | 16.86 | 18.44 | 15.44 | 2.00 | 16.88 | 0.56 | 1.18 |
| Standalone | 1280×720 | High/75 % | Weg | D | 60.02 | 16.66 | 17.04 | 12.27 | 1.85 | 16.65 | 0.50 | 1.09 |
| Standalone | 1280×720 | High/100 % | Dorf | A | 44.60 | 22.42 | 24.13 | 20.56 | 2.01 | 22.43 | 1.63 | 1.43 |
| Standalone | 1280×720 | High/100 % | Dorf | B | 55.45 | 18.04 | 19.59 | 16.32 | 2.14 | 17.98 | 1.63 | 1.43 |
| Standalone | 1280×720 | High/100 % | Dorf | C | 47.35 | 21.12 | 23.18 | 19.94 | 1.90 | 21.13 | 1.03 | 1.40 |
| Standalone | 1280×720 | High/100 % | Dorf | D | 58.13 | 17.20 | 18.64 | 15.97 | 2.10 | 17.21 | 1.03 | 1.38 |
| Standalone | 1280×720 | High/100 % | Wald | A | 45.82 | 21.82 | 23.61 | 20.20 | 1.98 | 21.82 | 1.59 | 1.47 |
| Standalone | 1280×720 | High/100 % | Wald | B | 56.80 | 17.61 | 19.13 | 15.65 | 2.06 | 17.64 | 1.59 | 1.46 |
| Standalone | 1280×720 | High/100 % | Wald | C | 48.07 | 20.80 | 23.36 | 19.58 | 2.05 | 20.79 | 0.99 | 1.44 |
| Standalone | 1280×720 | High/100 % | Wald | D | 59.84 | 16.71 | 17.86 | 15.52 | 2.18 | 16.68 | 0.99 | 1.40 |
| Standalone | 1280×720 | High/100 % | Weg | A | 43.27 | 23.11 | 24.15 | 21.27 | 2.00 | 23.10 | 1.84 | 1.32 |
| Standalone | 1280×720 | High/100 % | Weg | B | 53.62 | 18.65 | 20.14 | 16.96 | 2.12 | 18.66 | 1.84 | 1.31 |
| Standalone | 1280×720 | High/100 % | Weg | C | 45.57 | 21.95 | 23.95 | 20.18 | 1.98 | 21.93 | 0.99 | 1.29 |
| Standalone | 1280×720 | High/100 % | Weg | D | 56.25 | 17.78 | 19.32 | 16.25 | 2.12 | 17.74 | 0.98 | 1.28 |
| Standalone | 2560×1440 | Medium/75 % | Dorf | A | 32.65 | 30.62 | 32.46 | 29.73 | 1.90 | 30.60 | 2.48 | 1.79 |
| Standalone | 2560×1440 | Medium/75 % | Dorf | B | 42.31 | 23.64 | 25.29 | 22.69 | 1.93 | 23.67 | 2.48 | 1.79 |
| Standalone | 2560×1440 | Medium/75 % | Dorf | C | 33.08 | 30.23 | 32.55 | 29.25 | 1.92 | 30.26 | 2.03 | 1.74 |
| Standalone | 2560×1440 | Medium/75 % | Dorf | D | 43.14 | 23.18 | 24.65 | 22.02 | 1.97 | 23.17 | 2.03 | 1.73 |
| Standalone | 2560×1440 | Medium/75 % | Wald | A | 32.98 | 30.32 | 32.16 | 29.31 | 1.85 | 30.30 | 2.53 | 1.84 |
| Standalone | 2560×1440 | Medium/75 % | Wald | B | 44.20 | 22.63 | 24.68 | 21.82 | 1.86 | 22.61 | 2.53 | 1.82 |
| Standalone | 2560×1440 | Medium/75 % | Wald | C | 33.84 | 29.55 | 31.34 | 28.48 | 1.89 | 29.56 | 2.06 | 1.78 |
| Standalone | 2560×1440 | Medium/75 % | Wald | D | 44.72 | 22.36 | 24.97 | 21.49 | 1.92 | 22.36 | 2.07 | 1.77 |
| Standalone | 2560×1440 | Medium/75 % | Weg | A | 32.59 | 30.69 | 33.11 | 29.86 | 1.96 | 30.67 | 2.67 | 1.63 |
| Standalone | 2560×1440 | Medium/75 % | Weg | B | 41.11 | 24.32 | 26.55 | 23.27 | 1.99 | 24.35 | 2.70 | 1.64 |
| Standalone | 2560×1440 | Medium/75 % | Weg | C | 32.91 | 30.39 | 32.86 | 29.37 | 1.98 | 30.40 | 2.05 | 1.59 |
| Standalone | 2560×1440 | Medium/75 % | Weg | D | 42.86 | 23.33 | 25.90 | 22.33 | 2.02 | 23.31 | 2.05 | 1.59 |
| Standalone | 2560×1440 | Medium/100 % | Dorf | A | 22.72 | 44.02 | 46.08 | 42.57 | 2.26 | 44.07 | 4.43 | 2.21 |
| Standalone | 2560×1440 | Medium/100 % | Dorf | B | 30.48 | 32.81 | 34.15 | 31.27 | 2.21 | 32.81 | 4.69 | 2.29 |
| Standalone | 2560×1440 | Medium/100 % | Dorf | C | 22.31 | 44.82 | 46.59 | 43.30 | 2.26 | 44.87 | 3.71 | 2.18 |
| Standalone | 2560×1440 | Medium/100 % | Dorf | D | 31.10 | 32.16 | 33.43 | 30.61 | 2.13 | 32.14 | 3.79 | 2.21 |
| Standalone | 2560×1440 | Medium/100 % | Wald | A | 23.00 | 43.48 | 46.24 | 41.98 | 2.18 | 43.45 | 4.44 | 2.44 |
| Standalone | 2560×1440 | Medium/100 % | Wald | B | 31.88 | 31.36 | 32.39 | 29.81 | 2.20 | 31.37 | 4.49 | 2.46 |
| Standalone | 2560×1440 | Medium/100 % | Wald | C | 23.42 | 42.70 | 44.23 | 41.26 | 2.21 | 42.71 | 3.66 | 2.36 |
| Standalone | 2560×1440 | Medium/100 % | Wald | D | 32.29 | 30.97 | 32.39 | 29.42 | 2.20 | 30.97 | 3.67 | 2.38 |
| Standalone | 2560×1440 | Medium/100 % | Weg | A | 22.53 | 44.39 | 46.75 | 43.00 | 2.24 | 44.37 | 4.69 | 2.17 |
| Standalone | 2560×1440 | Medium/100 % | Weg | B | 30.42 | 32.88 | 34.89 | 31.60 | 2.19 | 32.88 | 4.92 | 2.25 |
| Standalone | 2560×1440 | Medium/100 % | Weg | C | 22.85 | 43.77 | 45.72 | 42.40 | 2.29 | 43.75 | 3.65 | 2.13 |
| Standalone | 2560×1440 | Medium/100 % | Weg | D | 31.19 | 32.06 | 33.77 | 30.58 | 2.20 | 32.03 | 3.67 | 2.16 |
| Standalone | 2560×1440 | High/75 % | Dorf | A | 25.12 | 39.81 | 41.83 | 38.02 | 2.12 | 39.81 | 3.87 | 1.79 |
| Standalone | 2560×1440 | High/75 % | Dorf | B | 31.90 | 31.35 | 32.98 | 29.38 | 2.08 | 31.35 | 3.89 | 1.82 |
| Standalone | 2560×1440 | High/75 % | Dorf | C | 26.02 | 38.43 | 40.40 | 37.18 | 2.06 | 38.45 | 2.55 | 1.74 |
| Standalone | 2560×1440 | High/75 % | Dorf | D | 33.86 | 29.53 | 31.49 | 28.04 | 2.04 | 29.52 | 2.57 | 1.75 |
| Standalone | 2560×1440 | High/75 % | Wald | A | 25.36 | 39.43 | 41.47 | 37.67 | 2.13 | 39.50 | 3.98 | 1.85 |
| Standalone | 2560×1440 | High/75 % | Wald | B | 32.83 | 30.46 | 31.68 | 28.41 | 2.03 | 30.43 | 3.98 | 1.87 |
| Standalone | 2560×1440 | High/75 % | Wald | C | 26.39 | 37.90 | 39.63 | 36.45 | 2.08 | 37.90 | 2.53 | 1.79 |
| Standalone | 2560×1440 | High/75 % | Wald | D | 34.68 | 28.83 | 30.63 | 27.39 | 1.99 | 28.83 | 2.54 | 1.80 |
| Standalone | 2560×1440 | High/75 % | Weg | A | 24.30 | 41.16 | 42.82 | 38.96 | 2.16 | 41.09 | 4.49 | 1.68 |
| Standalone | 2560×1440 | High/75 % | Weg | B | 31.40 | 31.85 | 33.52 | 29.90 | 2.08 | 31.86 | 4.47 | 1.67 |
| Standalone | 2560×1440 | High/75 % | Weg | C | 25.87 | 38.65 | 40.74 | 36.86 | 2.16 | 38.64 | 2.48 | 1.60 |
| Standalone | 2560×1440 | High/75 % | Weg | D | 33.43 | 29.91 | 31.88 | 28.02 | 2.09 | 29.87 | 2.49 | 1.61 |
| Standalone | 2560×1440 | High/100 % | Dorf | A | 17.01 | 58.79 | 60.60 | 57.19 | 2.41 | 58.73 | 6.62 | 2.27 |
| Standalone | 2560×1440 | High/100 % | Dorf | B | 23.30 | 42.92 | 45.22 | 41.45 | 2.35 | 42.86 | 6.61 | 2.26 |
| Standalone | 2560×1440 | High/100 % | Dorf | C | 17.44 | 57.33 | 59.75 | 56.44 | 2.36 | 57.34 | 4.37 | 2.18 |
| Standalone | 2560×1440 | High/100 % | Dorf | D | 24.01 | 41.64 | 43.62 | 40.56 | 2.24 | 41.63 | 4.39 | 2.25 |
| Standalone | 2560×1440 | High/100 % | Wald | A | 16.81 | 59.50 | 66.68 | 57.90 | 2.53 | 59.52 | 6.74 | 2.46 |
| Standalone | 2560×1440 | High/100 % | Wald | B | 23.47 | 42.61 | 44.31 | 41.17 | 2.27 | 42.59 | 6.67 | 2.47 |
| Standalone | 2560×1440 | High/100 % | Wald | C | 17.80 | 56.19 | 58.44 | 55.11 | 2.34 | 56.16 | 4.32 | 2.37 |
| Standalone | 2560×1440 | High/100 % | Wald | D | 24.69 | 40.50 | 42.20 | 39.46 | 2.26 | 40.44 | 4.33 | 2.42 |
| Standalone | 2560×1440 | High/100 % | Weg | A | 16.38 | 61.03 | 63.43 | 59.55 | 2.52 | 61.03 | 7.50 | 2.20 |
| Standalone | 2560×1440 | High/100 % | Weg | B | 21.96 | 45.54 | 47.52 | 43.99 | 2.35 | 45.53 | 7.67 | 2.25 |
| Standalone | 2560×1440 | High/100 % | Weg | C | 17.36 | 57.60 | 60.00 | 56.21 | 2.44 | 57.60 | 4.27 | 2.14 |
| Standalone | 2560×1440 | High/100 % | Weg | D | 23.77 | 42.07 | 44.24 | 40.58 | 2.35 | 42.05 | 4.28 | 2.22 |

## Isolierte Kosten der Bodenprojektionen

Zusatzvergleich QHD/High/100 %, drei Paare: exakt dieselben deaktivierten Objektschatten und dieselbe AA-Methode, nur sichtbare gegenüber unsichtbaren Decal-Helfern. Registrierungs-/Nachführungsaufwand bleibt in beiden Fällen bestehen; Differenz umfasst Raster-/Compositing-Effekte und Messrauschen, keinen isolierten Hardware-Kernel.

| Modus | GPU sichtbar | GPU unsichtbar | Differenz | Bildzeit sichtbar | Bildzeit unsichtbar | Differenz |
|---|---:|---:|---:|---:|---:|---:|
| PIE | 49.471 | 49.354 | +0.117 | 50.982 | 50.750 | +0.232 |
| Standalone | 55.586 | 56.202 | -0.616 | 56.873 | 57.185 | -0.312 |

PIE-Differenz der Mediane +0,117 ms GPU, native Differenz −0,616 ms; einzelne Paare wechseln das Vorzeichen. Damit kein zuverlässiger Submillisekunden-Nachweis aus Gesamttimings und insbesondere keine negative reale Renderkost behauptet. Einzelne ProfileGPU-Frames zeigen DeferredDecals BeforeBasePass mit 0,293 ms in PIE beziehungsweise 0,321 ms nativ, jeweils fünf relevante von 50 registrierten Decals. Das sind Momentaufnahmen, keine Drei-Lauf-Mediane. Die weiterhin benötigte Schattenprojektion für Gebäude/übrige Objekte bleibt ein Kostenfaktor. Die PIE-Zusatzsitzung hat ein anderes absolutes Gesamtbudget als die Hauptmatrix; diese Sitzungen nicht als direkte Vorher/Nachher-Paare verrechnen.

## Visuelle Prüfung und Bewegung

Vier beschriftete Übersichten aller 64 tatsächlich erzeugten Standbilder, QHD-Originalpixelausschnitte sowie zeitlich geordnete Sprint-, Wald-, Gesprächs- und Innenraumframes wurden geprüft. Keine generierten Konzeptbilder.

| Maßnahme | Sichtbarer Befund | Empfehlung |
|---|---|---|
| B – TAA | Bei 100 % kleine Standbildunterschiede, etwas weicher; bei 75 % feine Blatt-/Gras-/Haarmerkmale weniger präzise. Deutlicher QHD-GPU-Vorteil. | Bevorzugter nächster Kandidat; Detail-/Bewegungsabnahme vor Übernahme. |
| C – einfache Schatten | Ruhige weiche Flecken ohne Blatt-/Astkonturen; Gebäudeschatten erhalten. Wald/Stämme deutlich heller und flacher durch fehlende echte Eigen-/Umgebungsschatten. Kleine Gewinne, teils Mehrkosten. | Nicht pauschal übernehmen. Figurenkontaktflecken gegebenenfalls separat untersuchen. |
| D – Kombination | Höchste QHD-FPS der Hauptmatrix, aber gleiche Tiefenverluste wie C; kein stabiles 30-/60-FPS-Versprechen. | Vorerst nicht übernehmen. |

Bei Sprint/Kamerafahrt sind körnige Dither-Ränder und wechselnde Kronenfreistellung in beiden AA-Verfahren sichtbar. Kein Nachweis vollständiger Ghosting- oder Flimmerfreiheit. Die geprüften Einzelbilder zeigen keine neuen langen dauerhaften Doppelkonturen, schließen kurze temporale Artefakte aber nicht aus. Die Spielfigur bleibt bei Originalschatten teilweise sehr dunkel. C/D verbessert dort ihre Helligkeit, verändert zugleich die Waldwirkung. Das bestehende Reveal-System blieb unverändert. Keine neue Windanimation eingerichtet: Kamerafahrt/Parallaxe und vorhandene Animationen geprüft, keine separat angeregte Winddeformation.

451 tatsächlich gespeicherte zusätzliche Bewegungsframes aus 497 Requests: A 112, B 113, C 115, D 111. Zeitstempel in MotionActualFrames.json. Gleichzeitige Richtungs-/Dialogscreenshots haben einige Requests im selben Unreal-Frame ersetzt; die fehlenden Requests werden ausgewiesen und nicht als vorhandene Bilder gezählt. Bildfolgen, kein 30-/60-FPS-Video und keine menschliche Videoabnahme. Gleiches Bewegungsskript und gleiche Wegpunkte, aber wegen Framerate, Aufnahmestalls und Zielpunkttoleranzen keine pixelidentischen Bewegungspose-Zeitpunkte zwischen Varianten. Im Innenraum blieb Motion Blur 0,5 erhalten; dessen Weichheit nicht allein TAA zuschreiben.

Der erste Rampentest entdeckte eine reale verzögerte Schattennachführung: CoreTicker lag nach der Viewport-Abgabe. Korrektur über OnWorldPostActorTick; Bodenabfrage weiter maximal 20 Hz mit ebener Fortführung pro Frame. Fehlversuch erhalten: maximal 84,278 cm XY-Abstand unter Aufnahmestall. Finaler 8°-Test: 221 Stichproben, maximal 0,278 cm. Freier zweiter Rampentest ebenfalls bestanden (162 Stichproben). Temporäre Kollisionsfläche jeweils entfernt. Im freien Test wurde die Startposition vorbereitend teleportiert; dies gehört nicht zu den teleportfreien vollständigen Fußläufen. C/D-Motion-Stichproben auf flachen Laufwegen: Abstand zum nächsten sichtbaren Figurendecal praktisch 0 cm. Keine auffälligen neuen Z-Fighting-/Doppelschattenbefunde der Flecken in den geprüften Bildern. Steile Kanten, viele überlappende Projektoren und beliebige spätere Geländeformen bleiben ungeprüft.

**Versionstrennung:** Die vollständige statische 576-Segment-Matrix entstand vor der Korrektur des Nachführungszeitpunkts. Materialien, AA-/Lichtwerte und stationäre Schattenanordnung wurden nicht geändert. Die finale Fassung erhielt zusätzlich 24 reguläre QHD/High/100%-Kontrollsegmente mit drei Läufen pro A–D und Modus sowie acht Standbilder. Keine zweite vollständige 16-Konfigurationen-Matrix. Unterschiedliche Sitzungen/thermische Zustände nicht als Verbesserungsbeleg der Nachführung verrechnen. Finale Bewegungstests C/D und Rampen verwenden die korrigierte Fassung.

| Finale QHD/High/100%-Kontrolle | Variante | FPS | Median ms | GPU ms | P95 ms |
|---|---|---:|---:|---:|---:|
| PIE | A | 13.73 | 72.83 | 70.87 | 85.22 |
| PIE | B | 18.08 | 55.30 | 52.15 | 64.04 |
| PIE | C | 14.32 | 69.81 | 67.99 | 82.18 |
| PIE | D | 18.39 | 54.39 | 52.14 | 69.83 |
| Standalone | A | 16.88 | 59.25 | 57.45 | 61.66 |
| Standalone | B | 22.81 | 43.85 | 41.98 | 48.38 |
| Standalone | C | 17.86 | 56.00 | 54.45 | 58.26 |
| Standalone | D | 24.88 | 40.19 | 38.84 | 42.47 |

## Tatsächliche Gameplay- und technische Tests

- Variante A: Enhanced-Input-Fußlauf **313.17 m**, 231.8 s, Maximalgeschwindigkeit 315.00 cm/s. Bestanden; kein Testteleport.
- Variante B: Enhanced-Input-Fußlauf **317.25 m**, 229.0 s, Maximalgeschwindigkeit 315.00 cm/s. Bestanden; kein Testteleport.
- Variante C: Enhanced-Input-Fußlauf **318.80 m**, 232.2 s, Maximalgeschwindigkeit 315.00 cm/s. Bestanden; kein Testteleport.
- Variante D: Enhanced-Input-Fußlauf **317.26 m**, 228.9 s, Maximalgeschwindigkeit 315.00 cm/s. Bestanden; kein Testteleport.

102-Schritt-Rundweg je Variante mit echten Character-Movement-/Enhanced-Input-Bewegungen und bestehenden Interaktions-/Presenter-/Save-APIs: acht Richtungen, Anhalten, Sprint, Kollisionen, Wanderer/Liora, Quest/Archiv, Wildfang und Trainerkampf, Menü, Heilhaus gerade/diagonal hinein und hinaus, Heilung HP/PP, Checkpoint sowie Save/Load. NPC-Sprite-Fallback per bestehender Präsentations-API geprüft. Keine physische Controller- oder menschliche Eingabeabnahme behauptet. Alle vier Läufe besaßen anfangs keinen Dev-Slot; Testdateien gesichert und ursprüngliche Abwesenheit wiederhergestellt. Originaler Projekt-Worktree sauber und Vollbackup unverändert.

Mac Development Editor Build erfolgreich (Logs Build1–5; letzte Fassung Build5). Vollständige Projekt-Automation: {'succeeded': 48, 'succeededWithWarnings': 0, 'failed': 0, 'notRun': 0, 'inProcess': 0}. Map Checks: zentrale VisualV2, bestehende GPU-Testkarte und WestlandAssetLibrary, Ergebnisse in den verlinkten Logs. Ein gezielter Cook der neuen Materialien wird getrennt dokumentiert; kein Shipping-Spieltest behauptet.

## Fehlversuche und Grenzen

Ein erster Prozessstart war durch die Prozess-Sandbox nicht ausführbar; anschließend regulär autorisierter Start. Früher Einrichtungsversuch: MassEntity/pthread_rwlock-Assertion nach Kartenwechsel; getrennt erhalten, keine Map gespeichert. Weiterer Prototyp: SIGSEGV beim Aktivieren; fehlenden Owner-Gültigkeitscheck ergänzt, danach stabile Messsitzungen. Der Stack erlaubt keine weitergehende eindeutige Ursachenbehauptung. Vorbereitungs-Python-API-Anpassungen, fehlendes Screenshot-Unterverzeichnis und ein Abschlussmanifest-Rennen bei nativen Plänen ohne Fotozeilen korrigiert; keine Bilder erfunden. Nicht verfügbare Python-Spawn-API durch transienten Development-Testbefehl ersetzt. Erster Nachführungstest fehlgeschlagen und nach Scheduling-Korrektur erfolgreich wiederholt. A/B-Fußläufe unberührt; C/D bewusst bis zum Neubau zurückgestellt.

Zehn finale native Startlogs geprüft: acht Matrixstarts, Kosten- und finale Kontrollsitzung, keine Materialkompilierungs-/Instancing-Fallback-/Fatalfehler. Allgemeine vorhandene Bootstrap-Condition-, MCP-Lizenz-/HTTP-, Audio-/idevice_id-/Shutdown-Meldungen bleiben in Logs und WarningAudit erhalten. Strukturierte letzte Automation 48/48 ohne Testwarnungen. Keine paketierte Shipping-Abnahme, keine unabhängige Metal-Kernel-/vollständige Overdrawanalyse, keine exakten thermischen Sensorwerte und keine Live-Abrechnungsbestätigung. Keine globale Grafikabsenkung oder Beleuchtungsreparatur zum Kaschieren der Schattenwirkung.

## Dateien und lokale Nachweise

- Neuer Code: `Source/PokeMonster/Development/PokeMonsterSoftShadowTest.h/.cpp`; eng begrenzte Erweiterung des vorhandenen Performance-Probes.
- Neue Materialien: die drei oben genannten Development-Assets. Keine vorhandene Material-/Textur-/Meshdatei geändert.
- Werkzeuge und 16 reproduzierbare Messpläne: `Tools/VisualV2AASoftShadowsV1/`.
- [Alle Drei-Lauf-Ergebnisse](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/Summary.json), [alle A/B/C/D-Vergleiche](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/Comparison.csv), [Auflösungs-/Kamera-/Lichtprüfung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/Validation.json), [isolierte Kosten](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/CostSummary.json).
- [Fotoverzeichnis](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/Screenshots), [Rohdatenarchiv](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/RawMeasurements.zip), [SHA-geprüftes Nachweismanifest](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/EvidenceManifest.json).
- [Automation](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/Automation/Result.json), [Map Checks](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/MapChecks), [Fußläufe und Bildfolgen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/Evidence/Acceptance).

**QHD Standalone: A/B/C/D, Dorf/Wald/Weg/NPC – echte Aufnahmen**

![QHD Standalone: A/B/C/D, Dorf/Wald/Weg/NPC – echte Aufnahmen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/ImageReview/Standalone_C8_ActualScreens_Overview.jpg)

**TSR/TAA bei QHD100 – unvergrößerte Originalpixel**

![TSR/TAA bei QHD100 – unvergrößerte Originalpixel](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/ImageReview/PIE_QHD_High_100_A_B_Originalpixel.png)

**Sprint – zeitlich geordnete Originalpixelausschnitte, keine identischen Posen**

![Sprint – zeitlich geordnete Originalpixelausschnitte, keine identischen Posen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/ImageReview/Motion_SprintEight_ABCD_OriginalPixels.png)

## Git-Sicherung

Feature-/Werkzeug-Commit: `a79594d34d585dbd764cd98cfef0c8785531f71c`. 54 geprüfte Projekt-/Werkzeugpfade gezielt gesichert und regulär auf origin/main übertragen; Remote-Commit bestätigt. Keine Videos, Kontrollbilder, Rohmessungen, Cachedateien oder verworfenen Prototypskripte hochgeladen. Dieser Bericht wird in einem separaten Dokumentationscommit gesichert. Vollbackup bleibt unverändert. Remote/LFS-Abschluss im [Git-Nachweis](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18/GIT_ABSCHLUSS.md) und in der Abschlussantwort. Keine automatische Übernahme in VisualV2.

Git-Status vor Sicherung:

```text
?? Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap
?? Docs/VISUALV2_TAA_TSR_SOFT_SHADOWS_V1_PRUEFBERICHT.md
?? Tools/VisualV2EnvironmentQualityV1/
```

### Uploadumfang und Grenzen

Der Werkzeugcommit enthält 129.853 Byte normale Dateiinhalte und drei neue LFS-Objekte mit zusammen **24.543 Byte**. Der Push bestätigte 3/3 LFS-Uploads. Die direkte Remote-Prüfung wird extern mit OID, Bytezahl und SHA-256 festgehalten. Der Berichtscommit enthält ausschließlich diese Markdown-Datei.

Die am Prüftag eingesehenen [GitHub-Repository-Grenzen](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits) nennen 2 GB pro Push und 100 MB pro normalem Git-Objekt; die strengere Projektregel von höchstens 1 GiB normaler neuer Git-Daten wird deutlich eingehalten. Laut [GitHub-LFS-Abrechnung](https://docs.github.com/en/billing/concepts/product-billing/git-lfs) enthalten Free/Pro 10 GiB Speicher und Downloadbandbreite. Ein früher vom Nutzer bestätigter Kontostand war 0,2 GB/10 GB vor der schlanken Sicherung von etwa 4,26 GiB. Der aktuelle kontoweite Verbrauch und eine Live-Kostenabrechnung sind hier nicht direkt zugänglich und werden nicht als unabhängig bestätigt ausgegeben. Der neue Upload ist lediglich 24.543 Byte; keine Käufe, Budgetänderungen oder kostenpflichtigen Aktionen vorgenommen. Keine Quota-Fehlermeldung.
