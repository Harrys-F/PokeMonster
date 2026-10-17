# VisualV2 Quality V2 – Außen-Motion-Blur und GPU-Bestandsaufnahme

17.10.2026 · Unreal Engine 5.8.2 · MacBook Air M4 / 16 GB · macOS.

## Ergebnis

Die zentrale `/Game/Maps/Dev_TestMap_VisualV2` verwendet außen jetzt **MotionBlurAmount 0**. Das Heilhaus behält seinen bisherigen Innenraumwert **0,5**. Dies ist die einzige übernommene EnvironmentPerfV1-Maßnahme. Bloom, Schatten, Lumen, Kamera, Figuren, Vegetation und Gameplay wurden nicht überarbeitet.

Vier vollständige Gameplay-Fußläufe (PIE/Standalone jeweils 1280×720 und 2560×1440), Build, 48/48 Projekt-Automationstests, 8/8 Nachweis-Sicherheitstests und Map Check bestanden. 108 reguläre Profilsegmente mit verifizierter Ausgabe-/interner Auflösung und GPU-Zählern ausgewertet. Keine behauptete kausale FPS-Steigerung gegenüber zeitlich getrennten V1-Messungen.

**Nächste Priorität:** den großen noch nicht zugeordneten GPU-Anteil untersuchen, anschließend High-Lumen-Gather und Schattenprojektion gezielt profilieren. Kein weiterer Qualitätsschalter wurde dafür verändert.

## 1. Ausgangsstand, Sicherung und genaue Änderung

Gearbeitet ausschließlich im schlanken Worktree:
`/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`.

Ausgangs-HEAD/remote main: `a4cfd0baeeffbaccf928151552faabd01d41b704`, Branch `codex/slim-backup-v5`. Vorhandene unversionierte V1-Testkarte, Werkzeuge und Prüfbericht erhalten. AGENTS, GRAFIKSTIL und relevante TECHNIK/ENTSCHEIDUNGEN/SPIELIDEE/SPIELREGELN sowie V1-Prüfbericht gelesen. Die zusätzliche Git-/GitHub-Sicherungsanweisung am Ende des Auftrags wird als ausdrückliche Freigabe nach bestandener Prüfung behandelt.

Vor der Änderung externe, SHA-256-geprüfte Kopie der zentralen Map erstellt. Alle 2.807 bisherigen versionierten/unversionierten Slim-Dateien erfasst. Das separate lokale main und `refs/archive/pokemonster/full-backup-03492bd` verbleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; keine Originaldatei des Vollbackups geändert.

Die anfänglich geöffnete Editorsitzung stammte aus dem Vollbackup-Projekt. UI zeigte „Alle gespeichert“, kein PIE aktiv. Regulär geschlossen, kein Speichern-/Verwerfen-Dialog, kein Save All, Discard All oder Force Quit. Im danach gestarteten Slim-Editor saubere Map-/Content-Pakete per API bestätigt.

| Vorhandenes Volume | Feld | Vorher | Nachher |
|---|---|---:|---:|
| V2_OutdoorExposure, unbound, Priority −10 | override_motion_blur_amount | false | true |
| V2_OutdoorExposure | motion_blur_amount | 0,5 | 0 |
| V2_House_HH_Art_InteriorLighting, begrenzt, Priority 0 | override_motion_blur_amount | false | true |

Der Innenwert selbst bleibt 0,5. Sein expliziter Override ist notwendig, damit das höher priorisierte Innenvolume nicht die neue Außen-Abschaltung erbt. Blend-Weight, Blend-Radius, Prioritäten und alle übrigen PP-Felder bleiben gleich.

**Vollständiger Vergleich:** 1.348 Actors samt erfassten Komponenten/Transforms, Mesh-/Material-/HISM-Referenzen, Kollisionen, NPC-/Gameplay-Eigenschaften und WorldSettings; zusätzlich vollständiger exportierter FPostProcessSettings-Text beider Volumes. Exakt die drei genannten Felder geändert. Karte gespeichert, unabhängig erneut geöffnet und danach nochmals verglichen. Keine andere Karte gespeichert. Die neutrale V1-Testkopie bleibt unberührt.

Keine globale Abschaltung: `r.MotionBlurQuality` und `r.DefaultFeature.MotionBlur` bleiben aktiv. In der Medium-Abnahme beispielsweise MotionBlurQuality 3, BloomQuality 4, Lumen-Integration 1, VSM-Rays 4; High verwendet weiter die Stockwerte inklusive 8 VSM-Rays. Kein Bloom-Off, kein Lumen2, kein Gather-Wechsel, kein Raycount2, keine Vegetationsreduktion.

Kamera B unverändert: 2850 cm / Pitch −50° / Yaw −45° / FOV 35°. Player 140 cm, normale Geschwindigkeit 210 cm/s, bestehender Sprint 315 cm/s, Capsule, Animationen, Eingaben und Interaktionen unverändert. Innenkamera und Relocation bleiben die vorhandenen Gebäudefunktionen.

[Map-Sicherung und Prüfsumme](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/MapBackup.json)

[Unabhängiger Änderungsvergleich](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/MapChangeAudit.json)

[Schutzvergleich](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/ProtectionAudit.json)

## 2. Reale Gameplay- und Darstellungsabnahme

Alle vier Durchläufe bewegen den echten Player über Enhanced Input und CharacterMovement, ohne Test-Teleports im Parcours. Dialog-, Menü- und Kampfbedienung nutzt vorhandene öffentliche Spiel-APIs. Keine physische Controllerprüfung und keine kontinuierliche Videoabnahme behauptet. Profiling-Positionswechsel werden davon ausdrücklich getrennt.

| Durchlauf | Schritte | Wegstrecke m | Max. Sprint cm/s | Wildfang | Heilhaus / Save/Load | Ergebnis |
|---|---:|---:|---:|---|---|---|
| VEQ2_PIE_720 | 102 | 275.80 | 315.00 | CAPTURED, Team 3 | bestanden | bestanden |
| VEQ2_PIE_QHD | 102 | 283.41 | 315.00 | CAPTURED, Team 3 | bestanden | bestanden |
| VEQ2_Native_720 | 102 | 273.02 | 315.00 | CAPTURED, Team 3 | bestanden | bestanden |
| VEQ2_Native_QHD | 102 | 286.24 | 315.00 | CAPTURED, Team 3 | bestanden | bestanden |

Tatsächlich geprüft: normales Gehen, alle acht Richtungen, Sprint in acht Richtungen und Loslassen/Abbremsen, unveränderte Kamerafolge, Wanderer-Dialog/Talkblend/Sprite-Fallback, Queststart, Wildfang, Liora-Sieg, Archivabschluss und Rückkehrdialog, Menü-Eingabesperren, Save/Load mit HP-/PP-Erhalt, Heilhaus gerade und diagonal hinein/hinaus, Cutaway/Relocation/Innensteuerung, Heilerin/Heilung und gespeicherter Checkpoint, Brücke, Wald und Kronenfreistellung. Normale Geschwindigkeitsgrenze 210, Sprintspitze 315 cm/s bestätigt.

Vor jedem Durchlauf Dev-Slotzustand gesichert. Es existierte jeweils kein ursprünglicher Slot; die durch den Test erzeugten Saves wurden verlustfrei in ihren Runordner verschoben, ursprünglicher Zustand „kein Slot“ wiederhergestellt. Kein Vollbackup-Spielstand verwendet oder überschrieben.

Visueller Befund aus echten Spielkamera-PNGs und geordneten Bewegungsbildern: außen keine zusätzliche kamerabedingte Bewegungsunschärfe, Innenraumlook und ursprünglicher Motion-Blur-Wert erhalten. Figuren und Umgebung bleiben aus der festen Perspektive unverändert angeordnet. **Vorhandene Probleme bleiben sichtbar:** sehr dunkler Player im Waldschatten, temporale Dither-/Schattenkörnung, teils weiche TSR-/Upscaling-Darstellung, einfache Topfpflanzen und der braune Würfel am Heilhaus. Motion Blur aus beseitigt weder diese Artprobleme noch sämtliche temporale Bildweichheit. Kein neuer vollständiger Animationsqualitätsnachweis.

**QHD Außenansicht – echte Standalone-Aufnahme**

![QHD Außenansicht](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD/Native_Heilhaus00000.png)

[Originaldatei](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD/Native_Heilhaus00000.png)

**QHD Sprint / Kamerafolge – echte Standalone-Aufnahme**

![QHD Sprint / Kamerafolge](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD/Sprint_2_9900000.png)

[Originaldatei](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD/Sprint_2_9900000.png)

**QHD Innenraum in Bewegung – echte Standalone-Aufnahme**

![QHD Innenraum in Bewegung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD/WalkMotion_InteriorAisle_0000000.png)

[Originaldatei](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD/WalkMotion_InteriorAisle_0000000.png)

**QHD Wanderer-Gespräch – echte Standalone-Aufnahme**

![QHD Wanderer-Gespräch](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD/TalkSequence_QuestDialogue_0000000.png)

[Originaldatei](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD/TalkSequence_QuestDialogue_0000000.png)

Zusätzliche visuelle Kampf-/Fangprüfung: kurzer eigenständiger QHD-Standalone-Lauf mit 20 Stationen, 16,87 m, anschließend CAPTURED und Trainer-Sieg bestätigt, Spielstandzustand wiederhergestellt. Echte zeitlich geordnete Bilder der vorhandenen Kampf-UI aufgenommen und geprüft; keine Umstellung auf ein neues In-World-Kampfsystem und keine Performancewerte aus dieser Bildaufnahme abgeleitet.

![Laufender Fangversuch in der bestehenden Kampf-UI](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD_BattleReview/WildCapture_Frame_0300000.png)

![Trainerkampf in der bestehenden Kampf-UI](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Acceptance/VEQ2_Native_QHD_BattleReview/TrainerBattle_Frame_0300000.png)

## 3. Messmatrix und Zuverlässigkeit

Finaler Kartenstand, keine weiteren Einzelfaktor-Abschaltungen und keine neue Vorher-/Nachher-Serie. Historische V1-Werte sind andere Sitzungen und werden nicht zur Berechnung eines neuen Motion-Blur-FPS-Gewinns verwendet.

| Ausgabe | Profil | Screen Percentage | Intern abgeleitet |
|---|---|---:|---|
| 1280×720 | Medium | 75 % | 960×540 |
| 1280×720 | Medium | 100 % | 1280×720 |
| 2560×1440 | Medium / High | 75 % | 1920×1080 |
| 2560×1440 | Medium / High | 100 % | 2560×1440 |

Alle sechs Konfigurationen separat in eingebettetem PIE und Standalone mit Editorbinary `-game` (Development, kein paketierter Shipping-Build). Dorf, dichter Wald und offener Weg jeweils drei Wiederholungen, 5 Sekunden Warm-up und 8 Sekunden Messfenster. 12 Pläne × 9 reguläre Segmente = **108**, alle mit nichtleeren GPU-CSVs. Sechs zusätzliche Standalone-CSVDrain-Abschnitte nur zum Leeren des asynchronen Writers, **nicht ausgewertet**. Kein Renderer-/C++-Umbau.

Feste Player-Capsule-Standorte in cm: Dorf/Heilhaus (−4100,450,50,15), Wald (−4300,1550,50,15), Weg (−36,6,−47,1,50,15). Blickrichtung, FOV und Kameraposition geprüft; je Ort Variation unter 0,2 cm. Keine Gespräche/Kämpfe im Performancefenster; NPCs im vorhandenen Idle. Tatsächliche Viewport-, Render-Target- und unskalierte ViewRect-Größen stimmen mit der deklarieren Ausgabe überein. Interne Größen aus dem konstanten Renderthread-Screen-Percentage-Treiber abgeleitet, **kein direkter SceneColor-Pufferreadback**. Fenster-/DPI-Werte separat in MatrixValidation.

Dynamische Auflösung aus, Secondary Fraction 1, VSync 0, t.MaxFPS 0. rhi.SyncInterval bleibt 1; native 720p/75 ist bei etwa 60 FPS möglicherweise präsentationsbegrenzt. Daraus keine unbegrenzte Leistungsreserve ableiten. PIE-Renderthreadwerte nahe null nicht auswertbar; native Renderthread-Wall-Zeit enthält GPU-/Present-Warten und ist keine reine CPU-Rechenzeit. Fehlende/konstante Nullzähler werden nicht als kostenlose Arbeit ausgegeben, verschachtelte GPU-Pässe nicht addiert.

Tabellen: Median aus drei segmentbezogenen Medianen; FPS = 1000 / Median-Framezeit. P95 ist der Median der drei segmentbezogenen P95-Werte, kein gepooltes Gesamt-P95. Min/Max der drei Framezeitmediane separat erhalten. Kurze Stichproben, keine formale Signifikanz und kein 10–15-minütiger Dauerstabilitätsnachweis dieses Auftrags. Sichtbare Messdrift: insbesondere PIE 720p/75 im Wald etwa 36,27 / 37,06 / 47,26 FPS, daher keine stabile Leistungsangabe aus einem ausgewählten guten Lauf. Native QHD-Runs zeigen ebenfalls Zeitdrift.

Energieabfrage: AC, 100 %. Ab Beginn des Thermikmonitors 214 Statusproben, alle „fair“; keine Grad-/Takt-/Leistungsmessung, keine vollständige Überwachung jeder ersten Setup-/Fußlaufminute. Andere Anwendungen nicht zwangsweise beendet. Keine großen Hash-, Archiv- oder Buildarbeiten während Grafik-Timings.

In keinem der 36 Orts-/Konfigurationssummaries wird ein GPU/MotionBlur-Zähler gemeldet. Das passt zur Außen-Abschaltung bei weiterhin aktivem Quality-Schalter; es ist kein allgemeiner Beweis für null Motion-Vector-/TSR-Kosten. Innenraumdarstellung separat im Fußlauf geprüft.

[108 Messsegmente / Auswertung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/GPUSummary.json)

[Auflösungs- und Kameranachweis](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/MatrixValidation.json)

[Messwerttabelle (CSV)](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/PerformanceSummary.csv)

### Sämtliche Endstand-Messwerte

Zeiten in ms; CPU = Game Thread, RT = Renderthread-Wall-Zeit mit den oben genannten Grenzen. Historische Reihen nicht als Vorherwerte dieser Tabelle behandeln.

| Modus | Ausgabe / Profil / % | Ort | FPS | Frame | P95 | Frame Min…Max | GPU | Game | RT | ShadowProjection | ShadowDepths |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75 | Dorf | 34.78 | 28.75 | 31.76 | 28.40…29.22 | 25.56 | 9.28 | — | 0.58 | 2.63 |
| PIE | 1280×720 / Medium / 75 | Wald | 37.06 | 26.98 | 31.25 | 21.16…27.57 | 23.96 | 8.54 | — | 0.58 | 2.44 |
| PIE | 1280×720 / Medium / 75 | Weg | 46.15 | 21.67 | 27.42 | 21.66…21.91 | 20.37 | 8.28 | — | 0.63 | 1.22 |
| PIE | 1280×720 / Medium / 100 | Dorf | 35.66 | 28.04 | 31.25 | 28.01…28.24 | 26.40 | 7.28 | — | 1.01 | 1.46 |
| PIE | 1280×720 / Medium / 100 | Wald | 36.16 | 27.65 | 30.34 | 27.17…27.83 | 25.58 | 7.09 | — | 1.00 | 1.47 |
| PIE | 1280×720 / Medium / 100 | Weg | 34.66 | 28.85 | 31.24 | 28.59…29.08 | 26.90 | 6.97 | — | 1.07 | 1.33 |
| PIE | 2560×1440 / Medium / 75 | Dorf | 21.23 | 47.11 | 49.69 | 46.52…47.47 | 45.07 | 6.45 | — | 2.50 | 1.81 |
| PIE | 2560×1440 / Medium / 75 | Wald | 21.60 | 46.29 | 48.68 | 46.11…46.47 | 44.44 | 6.31 | — | 3.03 | 1.83 |
| PIE | 2560×1440 / Medium / 75 | Weg | 20.91 | 47.82 | 50.57 | 47.77…48.11 | 45.71 | 6.45 | — | 2.87 | 1.63 |
| PIE | 2560×1440 / Medium / 100 | Dorf | 14.64 | 68.28 | 75.68 | 67.39…68.41 | 66.44 | 7.25 | — | 4.93 | 2.19 |
| PIE | 2560×1440 / Medium / 100 | Wald | 14.62 | 68.41 | 76.36 | 66.53…68.55 | 66.31 | 7.17 | — | 5.28 | 2.38 |
| PIE | 2560×1440 / Medium / 100 | Weg | 14.61 | 68.46 | 74.35 | 67.86…69.38 | 66.30 | 7.27 | — | 5.48 | 2.20 |
| PIE | 2560×1440 / High / 75 | Dorf | 15.63 | 63.98 | 70.47 | 63.67…65.43 | 60.35 | 7.49 | — | 4.38 | 1.89 |
| PIE | 2560×1440 / High / 75 | Wald | 15.54 | 64.37 | 73.07 | 62.92…64.55 | 60.72 | 7.21 | — | 4.78 | 1.86 |
| PIE | 2560×1440 / High / 75 | Weg | 15.14 | 66.04 | 80.20 | 64.89…66.48 | 62.90 | 7.28 | — | 5.24 | 1.62 |
| PIE | 2560×1440 / High / 100 | Dorf | 11.04 | 90.59 | 104.63 | 89.45…92.09 | 87.20 | 8.10 | — | 10.79 | 2.53 |
| PIE | 2560×1440 / High / 100 | Wald | 10.71 | 93.38 | 114.08 | 93.21…93.91 | 89.93 | 8.12 | — | 11.42 | 3.01 |
| PIE | 2560×1440 / High / 100 | Weg | 10.31 | 97.02 | 111.40 | 95.25…99.37 | 93.47 | 8.09 | — | 12.45 | 2.44 |
| Standalone | 1280×720 / Medium / 75 | Dorf | 59.96 | 16.68 | 17.13 | 16.68…16.70 | 12.87 | 1.90 | 16.66 | 0.56 | 1.31 |
| Standalone | 1280×720 / Medium / 75 | Wald | 60.00 | 16.67 | 17.25 | 16.66…16.67 | 12.51 | 1.91 | 16.65 | 0.55 | 1.25 |
| Standalone | 1280×720 / Medium / 75 | Weg | 60.01 | 16.66 | 17.14 | 16.66…16.66 | 12.95 | 1.79 | 16.66 | 0.59 | 1.11 |
| Standalone | 1280×720 / Medium / 100 | Dorf | 56.82 | 17.60 | 20.13 | 17.46…17.76 | 16.36 | 1.66 | 17.60 | 1.02 | 1.42 |
| Standalone | 1280×720 / Medium / 100 | Wald | 55.81 | 17.92 | 20.40 | 17.52…18.25 | 16.77 | 1.76 | 17.89 | 1.02 | 1.47 |
| Standalone | 1280×720 / Medium / 100 | Weg | 51.41 | 19.45 | 22.28 | 19.22…19.45 | 18.04 | 1.89 | 19.44 | 1.15 | 1.38 |
| Standalone | 2560×1440 / Medium / 75 | Dorf | 30.36 | 32.94 | 34.64 | 32.42…33.11 | 31.76 | 1.65 | 32.92 | 2.48 | 1.69 |
| Standalone | 2560×1440 / Medium / 75 | Wald | 30.05 | 33.27 | 36.37 | 32.81…33.43 | 32.37 | 1.58 | 33.28 | 2.52 | 1.85 |
| Standalone | 2560×1440 / Medium / 75 | Weg | 27.76 | 36.03 | 39.61 | 35.84…36.47 | 34.79 | 1.68 | 36.00 | 2.99 | 1.66 |
| Standalone | 2560×1440 / Medium / 100 | Dorf | 20.01 | 49.97 | 55.56 | 49.28…52.49 | 48.34 | 1.92 | 49.95 | 4.83 | 2.19 |
| Standalone | 2560×1440 / Medium / 100 | Wald | 19.81 | 50.48 | 53.34 | 49.77…51.19 | 48.96 | 1.95 | 50.48 | 5.13 | 2.41 |
| Standalone | 2560×1440 / Medium / 100 | Weg | 18.55 | 53.91 | 58.00 | 52.80…54.61 | 52.35 | 1.94 | 53.94 | 5.54 | 2.21 |
| Standalone | 2560×1440 / High / 75 | Dorf | 22.08 | 45.29 | 47.50 | 44.52…46.30 | 43.04 | 1.79 | 45.29 | 4.05 | 1.78 |
| Standalone | 2560×1440 / High / 75 | Wald | 22.03 | 45.39 | 47.65 | 44.89…46.44 | 43.02 | 1.83 | 45.42 | 4.32 | 1.98 |
| Standalone | 2560×1440 / High / 75 | Weg | 20.32 | 49.20 | 54.36 | 49.08…50.38 | 47.02 | 1.85 | 49.25 | 4.98 | 1.81 |
| Standalone | 2560×1440 / High / 100 | Dorf | 14.59 | 68.53 | 73.50 | 68.02…68.85 | 65.98 | 2.09 | 68.52 | 7.42 | 2.27 |
| Standalone | 2560×1440 / High / 100 | Wald | 14.77 | 67.72 | 72.89 | 67.22…68.87 | 65.78 | 2.12 | 67.67 | 7.59 | 2.49 |
| Standalone | 2560×1440 / High / 100 | Weg | 13.47 | 74.22 | 80.95 | 73.32…74.35 | 71.50 | 2.13 | 74.20 | 9.87 | 2.45 |

## 4. Größte tatsächliche GPU-Beiträge und Prioritäten

Repräsentative **Standalone-Waldwerte**, gleiche Ausgabe QHD; Medium/100 und High/100 sind unterschiedliche Gesamtprofile, kein isoliertes Lumen-A/B. GPU-Scopes nicht aufsummieren und nicht automatisch einzelnen Meshfamilien zuschreiben.

| Zähler | QHD Medium/100 ms | QHD High/100 ms | Einordnung |
|---|---:|---:|---|
| GPUTime | 48.96 | 65.78 | Gesamt-GPU-Zeit |
| GPU/Unaccounted | 16.98 | 20.58 | Großer nicht sauber aufgeschlüsselter Anteil, kein benannter Verursacher |
| GPU/LumenScreenProbeGather | — | 12.72 | High-Gather-Pfad |
| GPU/LumenIrradianceFieldGather | 4.43 | — | Medium-Gather-Pfad |
| GPU/ShadowProjection | 5.13 | 7.59 | Deutlich größer als reine Shadow Depths |
| GPU/Basepass | 3.18 | 4.45 | Sichtbare Geometrie/Materialarbeit, keine isolierte Vegetationsmessung |
| GPU/RenderDeferredLighting | 3.30 | 4.42 | Lichtarbeit; Überschneidung mit anderen Scopes möglich |
| GPU/Lights | 4.00 | 4.17 | Keine additive separate Gesamtbudgetposition |
| GPU/ShadowDepths | 2.41 | 2.49 | Zusätzliche Schattenarbeit, nicht mit Projection verwechseln |
| GPU/Postprocessing | 1.29 | 1.45 | Native Schreibweise dieses CSV-Scopes |
| GPU/TemporalSuperResolution | — | 0.22 | Nur gemeldeter Scope, nicht sämtliche temporale Kosten |
| GPU/DistanceFieldShadows | — | 0.48 | Erfasst, hier wesentlich kleiner als ShadowProjection |

**P0 – Messlücke aufschlüsseln.** Etwa 20,58 ms Unaccounted bei QHD/High im nativen Wald sind die größte noch ungeklärte Position. Nächster gezielter Schritt: Metal-/Unreal-GPU-Capture derselben Kamera, Queue-/Present-Warteanteile und nicht erfasste Passbereiche unterscheiden, anschließend wieder mit CSV gegenprüfen. Zunächst keine Qualitätsänderung. Dieser Anteil ist kein Beweis, dass ausschließlich Vegetation oder Lumen die Last verursacht.

**P1 – High-Lumen.** ScreenProbeGather etwa 12,72 ms, Medium verwendet den anderen Gather-Pfad. Trace-, Integrations- und Scene-Update-Anteile getrennt untersuchen. Qualitätsarme Kandidaten zuerst: unnötige Scene-/Lichtaktualisierungen und offscreen wirksame Beiträge des räumlich entfernten Innenraums identifizieren, danach nur nachgewiesene redundante Arbeit entfernen; Eintritt/indirekte Beleuchtung müssen identisch bleiben. Keine bloße Abschaltung indirekten Lichts. IntegrateDownsampleFactor 2 ist aus V1 ein bedingter Kandidat mit möglichen Detailverlusten und bleibt **nicht übernommen**.

**P2 – Schattenprojektion.** Rund 7,59 ms High-Wald gegenüber 2,49 ms Depths. Cache-Invalidierungen und ihre tatsächlichen Auslöser pro Licht/Krone/Revealmaterial messen. Bevorzugt unnötige Invalidierungen/Updates beseitigen und vorhandene statische Wiederverwendung erhalten. Keine Baum-/Blattentfernung, keine pauschal schattenlosen Bäume. V1-Raycount2 erzeugt sichtbar mehr Körnung und bleibt unverändert ausgeschlossen. Die 0,48 ms DistanceFieldShadows sind hier kein vorrangiger Hebel.

**P3 – Basepass und Beleuchtung.** Basepass etwa 4,45 ms, benannte Lighting-Scopes ebenfalls um 4 ms; keine unbewiesene Summierung. Materialkomplexität und Pixelarbeit von Blatt-/Rinden-Reveal, Wegkanten sowie vorhandenen Lichtüberlagerungen gezielt aufschlüsseln. Mögliche bildgleiche Maßnahmen: identische Sampler-/Rechenarbeit zusammenfassen, nachweislich redundante Materialpfade/Updates vermeiden, bereits statische Gruppen gemeinsam rendern. Gain und tatsächliche Familienzuordnung sind noch nicht belegt. Kein weiterer pauschaler Polygonabbau oder Dichteabbau als Abkürzung.

**P4 – übriges Postprocessing erst nachrangig.** Native High-Werte etwa 1,45 ms für den gemeldeten Postprocessing-Scope und 0,22 ms für TSR; keine automatische Gleichsetzung mit allen Postprocesskosten. In PIE High/75 liegt ein PostProcessing-Scope auffällig bei 17,86 ms, während andere Sitzungen den großen Anteil unter Unaccounted führen. Diese Zuschreibung ist nicht stabil genug für eine pauschale Effekt-Abschaltung. Bloom/TSR/Lichtkomposition nicht weiter reduzieren; zuerst den Scope mit einem Capture klären. Motion Blur bleibt die einzige freigegebene Änderung.

Lichtinventar: 15 direkte LightComponents (darunter bewegliche Sonne und Innenfeuer mit CastShadows true; die meisten Zusatzlichter insgesamt ohne Schatten), dazu stationäres Skylight mit Intensität 1,25, **Realtime Capture false**, Cubemap-Auflösung 128. „Realtime Sky aus“ wäre hier keine neue Optimierung. Ein gesetztes Distance-Field-Schattenflag allein beweist keine zusätzlichen Kosten; die tatsächlichen GPU-Zähler sind maßgeblich. Keine einzelnen Lichtkosten ohne Per-Light-Capture behauptet.

**Empfehlung:** als nächsten Auftrag P0 plus begrenzte P1/P2-Diagnose durchführen, weiterhin separate Experimente und identische Bildabnahme. Dieses Paket liefert keine allgemeine QHD-Performancefreigabe: nativer Wald QHD/High/100 etwa 14,77 FPS / 67,72 ms, GPU 65,78 ms gegenüber Game Thread 2,12 ms. Die Last ist dort überwiegend GPU-/Render-seitig; reine NPC-CPU-Animation ist daraus kein priorisierter Hauptverursacher.

## 5. Build, Automation, Map Checks und Grenzen

- Mac Development Editor Build erfolgreich, Exit 0, Target aktuell, 0 Compile-Aktionen. Kein C++ geändert; kein behaupteter Clean-Rebuild.
- Frische vollständige PokeMonster-Automation: **48 Success, 0 Failed, 0 NotRun, 0 InProcess, 0 SuccessWithWarnings**. NullRHI ist keine Bildabnahme.
- Bestehende DevelopmentEvidence-Sicherheitstests: **8/8** erfolgreich.
- Zentrale Map vor/nach Übernahme und nach PIE-Fußläufen erneut geprüft: **Map Check 0 Fehler / 0 Warnungen**.
- 108 reguläre Messsegmente, alle drei Wiederholungen, tatsächliche Auflösungen, feste Kamera und nichtleere GPU-Aufzeichnungen validiert; sechs bewusst ausgeschlossene Drain-Segmente.

Automationlog weiterhin mit bekannten Startmeldungen außerhalb der strukturierten Projekttests: 17 generische Condition-failed-Zeilen bei Frame 0 vor Projekt-Testbeginn, vier idevice_id-/Bad-CPU-Warnungen, MCP-Lizenzhinweis und Editorlayout-Migration (23 Warning-/Error-Zeilen). Nicht unterdrückt; keine Behauptung eines vollständig fehlerfreien Engine-Logs. Ursache der Bootstrap-Conditions nicht Teil dieser reinen Kartenänderung.

Einrichtung: ExecutePythonScript beendete zunächst erwartungsgemäß die Editorsitzung; für die dauerhafte Sitzung wurde ExecCmds/py verwendet. Nach dem ersten erfolgreichen Save/Reload scheiterte nur die Audit-Metadatenausgabe an einem alten, entladenen Volume-Objekt. Das Autorenwerkzeug speichert die Namen jetzt vor Reload; eine unabhängige erneute vollständige Prüfung bestätigte die gespeicherte Karte. Kein unbestätigter Zustand als bestandener Test gewertet. Ein Git-LFS-Diff im eingeschränkten Dateisystem durfte den gemeinsamen temporären LFS-Speicher nicht beschreiben; dieselbe lesende Prüfung mit autorisiertem Zugriff gelang. Keine Gameplay-Testfehlfunktion oder Datei zurückgesetzt.

[Build](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Build.log)

[Automation-Ergebnis](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/AutomationResult.json)

[Unverdeckte Engine-/Automationmeldungen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Automation.log)

[Map-Check- und Editorlog](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/EditorSession.log)

[Sicherheits-Tests](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/EvidenceTests.log)

[Lichtinventar](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/LightingInventory.json)

[Alle Originalnachweise / Kopierprüfsummen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/Manifest.json)

[Rohdatenarchiv](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/Evidence/RawMeasurements.zip)

## 6. Dateien und Git-Sicherungsumfang

Geänderte bestehende Dateien ausschließlich:

- `Content/Maps/Dev_TestMap_VisualV2.umap`
- `Docs/TECHNIK.md`
- `Docs/ENTSCHEIDUNGEN.md`

Neu: dieser Bericht und die expliziten Entwicklungs-/Abnahmewerkzeuge unter `Tools/VisualV2QualityV2/` einschließlich zwölf TSV-Plänen. Keine neue Runtimeklasse, Material-, Textur-, Mesh-, Animations-, Gameplay- oder Konfigurationsdatei.

Der bereits bekannte, kompakte technische V1-Vergleichsbericht wird getrennt gesichert. Dessen neutrale Testkarte und alte Werkzeugkopien bleiben lokal unverändert; sie werden für diesen kleinen Integrationsstand nicht zusätzlich hochgeladen. Große Kontrollbilder, Saves, Roh-CSVs und Archive bleiben außerhalb von Git unter:
`/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17`.

Nach erfolgreichen Prüfungen gezieltes Staging, vollständiger Indexvergleich, `git diff --cached --check`, LFS-Zuordnung und reguläre Pushes ausschließlich vom Slim-HEAD nach `refs/heads/main`; niemals den alten lokalen main pushen. Vollbackup darf nicht Vorfahr der neuen Remotehistorie sein. Kein Force-Push, LFS-Prune, Kauf oder Budgetwechsel. Jeder Remote-Stand und neue LFS-Inhalt wird vor dem nächsten Push geprüft. Commit-Hashes und tatsächliche Push-/LFS-Ergebnisse werden im externen Abschlussnachweis nachgetragen, damit dieser Bericht seinen eigenen Hash nicht selbst referenzieren muss.

Aktuelle GitHub-Grenzen wurden anhand offizieller Dokumentation geprüft: normale Dateien maximal 100 MiB, Pushlimit 2 GiB; hier gilt zusätzlich die Nutzergrenze möglichst 1 GiB neue normale Git-Daten. LFS wird unabhängig geprüft. GitHub Free enthält 10 GiB Storage und Bandbreite; dies ersetzt keine aktuelle Kontoverbrauchsabfrage. Letzte vom Nutzer bestätigte freie Kapazität und bereits bekannte Uploadmenge werden getrennt von neu übertragenen Bytes dokumentiert. Keine neue Kostenfreigabe oder Kontoeinstellung.

[GitHub Repository Limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits); [GitHub LFS Billing](https://docs.github.com/en/billing/concepts/product-billing/git-lfs).

[Abschluss mit Commit-/Push-/LFS-Status](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/GIT_ABSCHLUSS.md).

## 7. Bekannte offene Punkte

Keine generelle Artfreigabe für dunkle Figuren, Schatten-/Ditherflimmern, TSR-Details, einfache Props oder die vollständige Spieler-/NPC-Animation. Keine Kontrolle mit physischem Controller. Keine paketierte Shipping-Abnahme, keine neue thermische Dauerlaufgarantie. Aktuelle GPU-Verursacher sind teils benannt, der große Unaccounted-Anteil bleibt offen. Optimierungsvorschläge sind **Pläne, nicht bereits implementierte Leistungsgewinne**.

Die gewünschte Einzelübernahme – Außen-Motion-Blur aus, bisheriger Innenraumwert erhalten – ist damit technisch und anhand echter Spielkameraaufnahmen abgenommen.
