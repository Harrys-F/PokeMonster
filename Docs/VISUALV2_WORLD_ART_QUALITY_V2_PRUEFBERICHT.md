# VisualV2 World Art Quality V2 – Prüfbericht

Stand: 19.10.2026. Unreal Engine 5.8.2, Apple M4, 16 GiB, macOS 27.0.1.

## Ergebnis und begrenzte Übernahme

Der bisherige Heilhausbereich in **`/Game/Maps/Dev_TestMap_VisualV2`** besitzt jetzt unterschiedlich große Pflanzentaschen, bewusst freie Bodenflächen und eine dezent weniger gleichförmige Gras-/Erdtextur. Alle **175 Instanzen** und sämtliche vorhandenen Topfpflanzen bleiben erhalten. Keine neue Karte, keine Ausweitung auf den Rest der Welt.

Drei geometrisch unveränderte Gras-/Kräutermeshes teilen sich ein Vertexfarben-Material. Über die sechs Gruppen sinken **echte LOD0-Abschnitte 17→10**, Komponenten-Materialbindungen **19→12**. Das ist ein nachgewiesener struktureller Vorteil, **kein nachgewiesener allgemeiner FPS-Gewinn**. HISM bleibt erhalten; 175 Einzelobjekte, Diagnose-Ausblendung und erzwungenes LOD0 werden nicht übernommen.

Die Ergebnisse schwanken. Insbesondere Standalone Medium/QHD100 liegt V2 im Gruppenmedian etwas hinter V1. Die einzelnen gepaarten Wiederholungen zeigen dort jedoch keine einheitliche Verschlechterung. Daher weder eine Verbesserung noch vollständige Kostenneutralität behauptet. Die gestalterische Änderung und Materialzusammenfassung sind keine Lösung der allgemeinen QHD-Last.

## Ausgangszustand und Schutz

Arbeitsverzeichnis: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`; Branch `codex/slim-backup-v5`. HEAD und direkt geprüftes origin/main zu Beginn: `371190e69776d906288e9772c7fdfcb0d635f4b1`. AGENTS.md, GRAFIKSTIL, SPIELIDEE, SPIELREGELN, TECHNIK, ENTSCHEIDUNGEN und die relevanten bisherigen Art-/Performanceberichte wurden berücksichtigt.

Die unveränderte Ausgangskarte wurde außerhalb des Projekts nach `/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19/Dev_TestMap_VisualV2_V1_Backup.umap` kopiert und per SHA-256 geprüft. Dies ist eine Dateisicherung, keine neue registrierte Unreal-Karte. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b`, lokaler main und Archivref bleiben unverändert; dieser Commit gehört nicht zur schlanken Remote-Historie.

SHA-256-Abschlussprüfung: **3164** vorher erfasste Dateien / **7,190,861,594 Bytes**, keine Originaldatei fehlt. Erlaubte Änderungen ausschließlich an zentraler Map, TECHNIK.md und ENTSCHEIDUNGEN.md. Alle übrigen erfassten Bestandsdateien bleiben identisch, einschließlich Originalassets, Spieler-/NPC-Quellen und anderer Karten. Lokales Prüfprotokoll: `/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19/ProtectionAfter.json`.

Bereits vorhandene fremde/unversionierte Stände bleiben ausgeschlossen: `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap`, `Tools/VisualV2EnvironmentQualityV1/`, `Tools/VisualV2QualityV2/__pycache__/`.

## Gestaltung und Assets

Bearbeitungsgrenze unverändert: X −4620…−3560, Y −720…1190 cm, etwa 10,6×19,1 m. Keine neuen Actors; weiterhin 1354 auditierte Actors. Nur **elf** Actors dürfen sich ändern: sechs vorhandene HISM-Gruppen und fünf Bodenmaterial-Zuweisungen. Die übrigen **1343** Actors und Weltparameter stimmen im Inhaltsvergleich überein.

- Neun unterschiedlich gewichtete, asymmetrische Pflanzentaschen. Größere Kräuter-/Blütengruppen wechseln mit kleinen Akzenten; Farne bevorzugt in Rand-/Schattenlagen. Gruppen variieren in Ausdehnung und Anzahl, ohne Raster. Bestehende zufällige Pflanzenmaßstäbe bleiben erhalten; X/Y und Drehung werden neu angeordnet.
- Freie Korridore vor Eingang und auf dem Rundweg; zusätzliche Abstände zu den vorhandenen Töpfen. Kein neuer Collider, kein Blockieren wichtiger Interaktionspunkte.
- Vier private Bodenmaterialvarianten verschieben ausschließlich lokal die vorhandenen Texturkoordinaten weich und unregelmäßig. Vorhandene drei Gras- und zwei Erdabfragen bleiben erhalten. Keine neue Textur, kein zusätzlicher Texture-Fetch, keine Änderung der ursprünglichen Wegmasken. Zusätzliche Rechenoperationen sind trotzdem nicht kostenlos.
- Drei private Meshvarianten bewahren Dreieckspositionen (geprüft bis 0,00001 cm), UVs und Corner-Normalen. Keine Decimation, keine neue Blattgeometrie, keine entfernten Halme. Konstante vorhandene Materialfarben werden in Vertexfarben übertragen; geringfügige 8-Bit-Farbquantisierung bleibt möglich.

| Gruppe | Instanzen | Dreiecke je Mesh, LOD0 / 1 / 2 | LOD0-Abschnitte V2 | Komponentenbindungen V2 |
|---|---:|---|---:|---:|
| WAQ1_GrassSmall | 54 | 45 | 1 | 1 |
| WAQ1_GrassMedium | 36 | 90 | 1 | 1 |
| WAQ1_MeadowHerbs | 28 | 100 | 1 | 1 |
| WAQ1_Flowers | 18 | 2160 / 1188 / 540 | 5 | 5 |
| WAQ1_Fern | 12 | 8030 / 4818 / 2409 | 1 | 3 |
| WAQ1_Pebbles | 27 | 80 | 1 | 1 |

Maximale Summe bei allen 175 Instanzen in LOD0 weiterhin **145.870 Dreiecke**; das ist keine gemessene sichtbare Dreieckzahl. Zwei historische Farnbindungen sind ungenutzt; sein Mesh hat nur einen Abschnitt. Deshalb dürfen Bindungen und tatsächliche Abschnitte nicht gleichgesetzt werden.

Neue Assets ausschließlich unter `Content/Environment/VisualV2WorldArtV2`: `SM_WAQ2_GrassSmall`, `SM_WAQ2_GrassMedium`, `SM_WAQ2_MeadowHerbs`, `M_WAQ2_PlantVertexColour` sowie `M_WAQ2_HealingMeadow`, `HealingPath`, `HealingForecourt`, `LegacyApproach`. Originale bleiben erhalten. Autoren- und Wiederherstellungsdaten: `Art/World/VisualV2WorldArtV2/{BaselineInstances,MeshCandidates,ArtCandidate}.json`.

Alle sechs Gruppen behalten NoCollision, keinen Schattenwurf, keinen zusätzlichen Distance-Field-/Indirect-Beitrag und Culling4500–6500 cm. Keine Änderung an Bäumen, Topfpflanzen, Lichtquellen, Lichtpositionen/-farben/-intensitäten, Exposure, Bloom, Lumen, Originalschatten, TAA oder Kamera. Kamera weiterhin2850 cm / −50° / −45° /35°, Spieler140 cm, Gehen210 cm/s, Sprint315 cm/s. Bestehendes Kronen-Reveal unverändert.

## Messmethode und echte Auflösung

Acht vollständige Reihen, **396 Segmente**, **132 Gruppen mit je drei FPS-/P95-Läufen**. Die vier Kostenreihen umfassen je15, die vier finalen Reihen je84 Segmente. Pro finalem Segment3 s Warm-up +3 s Messung; Kostenversuch3+4 s. Vor nativen Starts zusätzlich20 s. Faktoren rotieren in der Reihenfolge; Qualitätsstufen werden je in einem frischen Spiel-/PIE-Start gesetzt, nicht über laufende Reveal-MIDs umgeschaltet.

Matrix:1280×720 und2560×1440; Medium/High; SP75/100; Dorf/Wald/Weg; Embedded PIE und native Development-Standalone getrennt. Kein Shipping-Pakettest. Gleiche NPC-Konfiguration ohne aktive Dialoge; normale zyklische Idle-Phasen sind zeitabhängig. Keine Aufnahmen während der Zeitmessung.

Unabhängiger vorhandener Renderer-Beobachter bestätigt in jeder Messzeile tatsächliches Target/View/Viewport, interne Größe und AA-Methode2(TAA). 720p75 intern960×540; QHD75 intern1920×1080;100% jeweils volle Ausgabe. Native Slate-Fenstergröße und DPI werden separat protokolliert und nicht mit Renderpixeln verwechselt. Alle tatsächlichen Größen stehen in [Messmethode.json](Data/VisualV2WorldArtQualityV2/Messmethode.json). VSync-CVar0, MaxFPS0, dynamische Auflösung aus; kein alter EnvironmentPerf-GI-/Schatten-Preset dank Präfix `VGB1_`. Eine Plattform-/Präsentationsbegrenzung nahe60 FPS kann trotz dieser CVars nicht vollständig ausgeschlossen werden.

Messpunkte aus der bestehenden Kamera: Dorf Player−4100/450, Wald−4300/1550, Weg−36,6/−47,1 cm. Dorfkamera ungefähr−5395,3805/1745,3805/2268,3767 cm. Pitch/Yaw/FOV identisch; Fotopositionen sind separat vom echten Fußlauf eingerichtet.

FPS=1000/Median der Wall-Framezeit. Tabellenwert=Median der drei Laufmediane; P95=Spannweite der drei Lauf-P95. Drei Sekunden sind kurze Stichproben, keine Langzeitgarantie. Mac am Netzteil100%, thermische Stichproben: {'nominal': 338} bei 338 Beobachtungen. Normaler thermischer Status schließt Frequenz-/Zeitdrift nicht aus. Unterschiedliche Ausführungsarten und historische Reihen werden nicht zu einem vermeintlich kausalen FPS-Vergleich vermischt.

**Zählergrenzen:** Die tatsächlichen DrawCall-/RHI-Zähler dieser Metal-CSV sind durchgehend null und damit nicht zuverlässig verfügbar, nicht null reale Draw Calls. Vier letzte Standalone-Segmente besitzen wegen des sofortigen normalen Programmendes keine fertig geschriebene zusätzliche Profiler-CSV. Alle Wall-Frames bleiben vollständig. Bei diesen Gruppen beruhen GPU-/CPU-Werte auf zwei statt drei gültigen Zählerläufen; jedes Feld `*_runs` in der CSV weist dies aus. Keine fehlenden Werte ergänzt. Betroffen: natives Cost-Segment14(Individual_LOD0) sowie finales Segment83(Weg/V1/QHD100), jeweils Medium/High. Insgesamt392 zusätzliche gültige Profiler-Segmente.

## Kosten der175 Instanzen: isolierter Vergleich

Dorf, QHD100%, identische vorhandene Kamera, pro Faktor drei Wall-Frame-Läufe. `No175` ist nur eine reversible Diagnose. Die beiden LOD0-Zeilen erzwingen auf beiden Darstellungsarten dieselbe Geometrie, weil automatische HISM-/Einzelobjekt-LOD-Auswahl unterschiedlich sein kann. Die transienten175 Einzelobjekte besitzen keine Kollision, keinen Schatten und keinen Tick; sie werden nicht gespeichert.

| Modus / Qualität | Darstellung | FPS | Frame ms | GPU ms | GPU-Läufe | P95 ms, Spanne |
|---|---|---:|---:|---:|---:|---|
| PIE / Medium | HISM | 29.77 | 33.59 | 32.88 | 3 | 35.44–36.75 |
| PIE / Medium | HISM_LOD0 | 30.45 | 32.84 | 31.11 | 3 | 35.88–36.85 |
| PIE / Medium | Individual | 29.76 | 33.60 | 32.68 | 3 | 34.93–45.15 |
| PIE / Medium | Individual_LOD0 | 30.37 | 32.92 | 31.87 | 3 | 36.19–37.67 |
| PIE / Medium | No175 | 29.80 | 33.55 | 32.68 | 3 | 34.49–35.67 |
| PIE / High | HISM | 19.82 | 50.45 | 47.42 | 3 | 52.35–52.83 |
| PIE / High | HISM_LOD0 | 19.33 | 51.74 | 49.14 | 3 | 53.94–60.98 |
| PIE / High | Individual | 20.00 | 50.00 | 47.52 | 3 | 52.31–56.03 |
| PIE / High | Individual_LOD0 | 19.70 | 50.77 | 48.56 | 3 | 54.03–62.79 |
| PIE / High | No175 | 20.17 | 49.57 | 46.99 | 3 | 53.06–53.69 |
| Standalone / Medium | HISM | 30.35 | 32.94 | 31.98 | 3 | 33.56–35.70 |
| Standalone / Medium | HISM_LOD0 | 30.61 | 32.67 | 31.69 | 3 | 34.46–35.09 |
| Standalone / Medium | Individual | 30.07 | 33.26 | 32.23 | 3 | 34.56–35.25 |
| Standalone / Medium | Individual_LOD0 | 30.78 | 32.49 | 31.48 | 2 | 33.66–34.70 |
| Standalone / Medium | No175 | 30.61 | 32.67 | 31.60 | 3 | 34.27–36.94 |
| Standalone / High | HISM | 28.13 | 35.55 | 33.91 | 3 | 36.76–36.95 |
| Standalone / High | HISM_LOD0 | 27.78 | 36.00 | 34.34 | 3 | 37.03–37.71 |
| Standalone / High | Individual | 28.24 | 35.41 | 33.80 | 3 | 37.00–37.13 |
| Standalone / High | Individual_LOD0 | 27.89 | 35.86 | 34.09 | 2 | 37.06–38.00 |
| Standalone / High | No175 | 28.52 | 35.07 | 33.45 | 3 | 36.38–39.60 |

HISM→No175 spart im jeweiligen GPU-Gruppenmedian ungefähr0,20 ms(PIE Medium),0,43 ms(PIE High),0,38 ms(Standalone Medium) bzw.0,47 ms(Standalone High). Diese kleinen Unterschiede und die Streuung beweisen weder einen exakten isolierten Dauerpreis noch einen Hauptengpass durch die175 Details. Einzelobjekte liefern keinen konsistenten Vorteil. Die frühere sequenzielle V1-Mehrkostenmessung darf nicht vollständig diesen Instanzen zugeschrieben werden; Bodenmaterialien und zeitliche Schwankungen wurden dort nicht getrennt.

## V1 / reine Materialzusammenfassung / vollständigeV2

`Merged`: V1-Positionen und V1-Boden, nur drei Mesh-/Materialvarianten. `V2`: zusätzlich neue Gruppierung und Bodenvariation. Dorf; jeweils drei Wiederholungen.

| Modus / Qualität | Ausgabe / SP | FPS V1 / Merged / V2 | GPU ms V1 / Merged / V2 |
|---|---|---|---|
| PIE / Medium | 1280×720 / 75% | 56.40 / 56.53 / 55.70 | 16.67 / 16.69 / 16.68 |
| PIE / Medium | 1280×720 / 100% | 50.01 / 50.10 / 49.95 | 19.16 / 19.05 / 19.23 |
| PIE / Medium | 2560×1440 / 75% | 31.91 / 32.46 / 32.02 | 30.42 / 30.20 / 30.50 |
| PIE / Medium | 2560×1440 / 100% | 24.85 / 24.74 / 24.76 | 39.13 / 39.48 / 39.12 |
| PIE / High | 1280×720 / 75% | 46.07 / 46.57 / 45.13 | 19.13 / 19.31 / 19.32 |
| PIE / High | 1280×720 / 100% | 38.14 / 37.41 / 37.71 | 23.63 / 23.85 / 23.63 |
| PIE / High | 2560×1440 / 75% | 24.95 / 24.86 / 24.98 | 36.94 / 37.03 / 36.90 |
| PIE / High | 2560×1440 / 100% | 18.80 / 18.80 / 18.68 | 50.99 / 50.19 / 50.77 |
| Standalone / Medium | 1280×720 / 75% | 59.99 / 60.00 / 59.96 | 13.19 / 13.07 / 12.96 |
| Standalone / Medium | 1280×720 / 100% | 59.98 / 60.03 / 59.99 | 13.37 / 13.41 / 13.53 |
| Standalone / Medium | 2560×1440 / 75% | 53.41 / 51.50 / 53.46 | 17.91 / 18.42 / 17.86 |
| Standalone / Medium | 2560×1440 / 100% | 31.53 / 31.51 / 30.56 | 30.61 / 30.94 / 31.55 |
| Standalone / High | 1280×720 / 75% | 59.96 / 60.04 / 60.07 | 12.99 / 12.88 / 12.93 |
| Standalone / High | 1280×720 / 100% | 56.70 / 55.59 / 55.84 | 16.05 / 16.20 / 15.90 |
| Standalone / High | 2560×1440 / 75% | 34.73 / 34.88 / 34.35 | 26.92 / 26.66 / 27.12 |
| Standalone / High | 2560×1440 / 100% | 23.96 / 24.04 / 24.03 | 39.77 / 39.53 / 39.63 |

Kein belegter allgemeiner FPS-Gewinn. Beispiel Standalone Medium/QHD100: GPU30,61→31,55 ms und FPS31,53→30,56 im Gruppenmedian. Die drei gepaarten GPU-Differenzen betragen jedoch−0,74/+1,70/−0,43 ms: kein gleichmäßiger Effekt. High/QHD100 liegt bei39,77→39,63 ms und23,96→24,03 FPS. Keine pauschale Behauptung „kostenlos“ oder „schneller“.

Die Compiler-Vorschaustatistik des neuen Vertexfarben-Materials lautet VS157/PS200, Sampler0, Pixel-Texture-Samples3; alte konstante Grasmaterialien im Inventar VS151/PS197. Weniger Abschnitte bedeutet hier keinen günstigeren einzelnen Pixelshader. Die neuen Grasmaterialien enthalten keine eigenen Texture-Sample-Nodes. Bei den Custom-HLSL-Bodenmaterialien erfassen die Vorschau-Texture-Zähler die expliziten HLSL-Abfragen nicht vollständig; aus einer API-Null folgt keine Nullkostenbehauptung.

Base-Pass-, Game-Thread-, Game-Critical-Path- und Render-Critical-Path-Werte stehen vollständig in [Messwerte.csv](Data/VisualV2WorldArtQualityV2/Messwerte.csv). Render-Critical-Path kann GPU-/Present-Wartezeit enthalten; nicht als reine CPU-Rechenzeit oder unabhängiger CPU-Engpass interpretieren. Die große Szene bleibt besonders in QHD GPU-teuer. Keine weitergehende Environment-Optimierung in diesem Auftrag.

## Vollständige Vorher-/Nachher-Matrix

Je Tabellenzeile drei Wall-Frame-Wiederholungen. Sämtliche Einzelgruppen einschließlich CPU, Base Pass, Counter-Laufzahl und Streuung in der verlinkten CSV.

| Modus | Qualität | Ausgabe / SP | Ort | FPS V1 → V2 | Frame ms V1 → V2 | GPU ms V1 → V2 | P95-Spanne ms V1 / V2 |
|---|---|---|---|---:|---:|---:|---|
| PIE | Medium | 1280×720 / 75% | Dorf | 56.40 → 55.70 | 17.73 → 17.95 | 16.67 → 16.68 | 20.83–21.55 / 21.72–24.34 |
| PIE | Medium | 1280×720 / 75% | Wald | 58.47 → 58.73 | 17.10 → 17.03 | 16.01 → 15.88 | 19.15–21.10 / 20.20–25.41 |
| PIE | Medium | 1280×720 / 75% | Weg | 56.36 → 56.05 | 17.74 → 17.84 | 16.89 → 17.04 | 21.15–21.32 / 20.96–21.55 |
| PIE | Medium | 1280×720 / 100% | Dorf | 50.01 → 49.95 | 19.99 → 20.02 | 19.16 → 19.23 | 24.09–24.68 / 24.13–25.69 |
| PIE | Medium | 1280×720 / 100% | Wald | 51.04 → 51.14 | 19.59 → 19.55 | 18.62 → 18.63 | 23.77–24.03 / 23.75–23.97 |
| PIE | Medium | 1280×720 / 100% | Weg | 48.91 → 48.88 | 20.44 → 20.46 | 19.48 → 19.53 | 24.16–25.30 / 24.44–25.13 |
| PIE | Medium | 2560×1440 / 75% | Dorf | 31.91 → 32.02 | 31.34 → 31.23 | 30.42 → 30.50 | 33.01–33.28 / 32.83–34.12 |
| PIE | Medium | 2560×1440 / 75% | Wald | 33.31 → 32.94 | 30.02 → 30.36 | 29.30 → 29.32 | 32.56–34.16 / 32.36–32.54 |
| PIE | Medium | 2560×1440 / 75% | Weg | 31.64 → 31.24 | 31.60 → 32.01 | 31.07 → 31.36 | 33.60–34.14 / 33.80–34.95 |
| PIE | Medium | 2560×1440 / 100% | Dorf | 24.85 → 24.76 | 40.25 → 40.38 | 39.13 → 39.12 | 44.78–45.85 / 44.77–45.64 |
| PIE | Medium | 2560×1440 / 100% | Wald | 25.45 → 25.61 | 39.30 → 39.05 | 38.49 → 38.29 | 43.34–45.43 / 43.57–44.97 |
| PIE | Medium | 2560×1440 / 100% | Weg | 24.64 → 24.69 | 40.59 → 40.50 | 40.02 → 39.65 | 44.32–48.02 / 45.55–45.77 |
| PIE | High | 1280×720 / 75% | Dorf | 46.07 → 45.13 | 21.71 → 22.16 | 19.13 → 19.32 | 25.84–29.79 / 26.10–31.15 |
| PIE | High | 1280×720 / 75% | Wald | 46.27 → 45.54 | 21.61 → 21.96 | 18.87 → 18.76 | 32.52–61.27 / 27.32–48.95 |
| PIE | High | 1280×720 / 75% | Weg | 44.07 → 43.68 | 22.69 → 22.89 | 20.85 → 20.84 | 26.79–27.25 / 27.68–36.86 |
| PIE | High | 1280×720 / 100% | Dorf | 38.14 → 37.71 | 26.22 → 26.52 | 23.63 → 23.63 | 30.91–31.43 / 30.30–31.26 |
| PIE | High | 1280×720 / 100% | Wald | 39.39 → 38.98 | 25.39 → 25.65 | 22.84 → 23.21 | 29.69–29.92 / 29.36–30.46 |
| PIE | High | 1280×720 / 100% | Weg | 37.98 → 36.98 | 26.33 → 27.04 | 24.15 → 24.56 | 30.62–30.74 / 30.88–32.28 |
| PIE | High | 2560×1440 / 75% | Dorf | 24.95 → 24.98 | 40.08 → 40.03 | 36.94 → 36.90 | 44.90–45.40 / 45.05–45.61 |
| PIE | High | 2560×1440 / 75% | Wald | 26.17 → 26.24 | 38.21 → 38.12 | 36.14 → 36.38 | 45.24–45.57 / 44.92–45.88 |
| PIE | High | 2560×1440 / 75% | Weg | 24.25 → 24.48 | 41.24 → 40.85 | 38.02 → 37.94 | 45.80–47.05 / 46.26–46.75 |
| PIE | High | 2560×1440 / 100% | Dorf | 18.80 → 18.68 | 53.20 → 53.53 | 50.99 → 50.77 | 60.27–61.55 / 60.68–62.01 |
| PIE | High | 2560×1440 / 100% | Wald | 18.99 → 19.32 | 52.66 → 51.76 | 50.20 → 50.36 | 58.30–60.97 / 59.26–60.95 |
| PIE | High | 2560×1440 / 100% | Weg | 17.90 → 18.27 | 55.85 → 54.73 | 52.48 → 52.19 | 61.41–62.90 / 60.15–65.19 |
| Standalone | Medium | 1280×720 / 75% | Dorf | 59.99 → 59.96 | 16.67 → 16.68 | 13.19 → 12.96 | 16.96–17.02 / 17.00–17.07 |
| Standalone | Medium | 1280×720 / 75% | Wald | 60.00 → 60.04 | 16.67 → 16.66 | 12.94 → 12.47 | 16.99–17.10 / 16.99–17.17 |
| Standalone | Medium | 1280×720 / 75% | Weg | 59.98 → 60.01 | 16.67 → 16.66 | 13.11 → 12.93 | 16.95–17.02 / 17.00–17.09 |
| Standalone | Medium | 1280×720 / 100% | Dorf | 59.98 → 59.99 | 16.67 → 16.67 | 13.37 → 13.53 | 16.96–17.03 / 16.96–17.05 |
| Standalone | Medium | 1280×720 / 100% | Wald | 60.04 → 59.99 | 16.66 → 16.67 | 13.18 → 13.32 | 17.07–17.16 / 17.02–17.10 |
| Standalone | Medium | 1280×720 / 100% | Weg | 60.05 → 60.00 | 16.65 → 16.67 | 13.42 → 13.37 | 17.02–17.06 / 16.97–17.02 |
| Standalone | Medium | 2560×1440 / 75% | Dorf | 53.41 → 53.46 | 18.72 → 18.70 | 17.91 → 17.86 | 19.98–20.70 / 19.95–21.23 |
| Standalone | Medium | 2560×1440 / 75% | Wald | 49.27 → 48.04 | 20.30 → 20.82 | 19.46 → 19.98 | 21.89–22.88 / 21.49–24.11 |
| Standalone | Medium | 2560×1440 / 75% | Weg | 44.53 → 44.67 | 22.46 → 22.39 | 21.45 → 21.45 | 24.76–25.20 / 24.03–25.01 |
| Standalone | Medium | 2560×1440 / 100% | Dorf | 31.53 → 30.56 | 31.71 → 32.72 | 30.61 → 31.55 | 33.23–35.77 / 33.12–37.38 |
| Standalone | Medium | 2560×1440 / 100% | Wald | 33.70 → 33.47 | 29.67 → 29.88 | 28.91 → 29.00 | 31.05–33.24 / 31.43–31.76 |
| Standalone | Medium | 2560×1440 / 100% | Weg | 32.24 → 32.05 | 31.02 → 31.20 | 30.28 → 30.24 | 32.14–33.06 / 33.15–34.30 |
| Standalone | High | 1280×720 / 75% | Dorf | 59.96 → 60.07 | 16.68 → 16.65 | 12.99 → 12.93 | 17.05–21.82 / 17.07–26.88 |
| Standalone | High | 1280×720 / 75% | Wald | 59.99 → 60.00 | 16.67 → 16.67 | 11.87 → 12.32 | 17.02–17.65 / 17.05–19.90 |
| Standalone | High | 1280×720 / 75% | Weg | 59.98 → 60.05 | 16.67 → 16.65 | 12.93 → 12.82 | 17.02–17.11 / 16.97–17.00 |
| Standalone | High | 1280×720 / 100% | Dorf | 56.70 → 55.84 | 17.64 → 17.91 | 16.05 → 15.90 | 19.52–19.62 / 19.99–23.35 |
| Standalone | High | 1280×720 / 100% | Wald | 58.84 → 58.79 | 17.00 → 17.01 | 15.61 → 15.48 | 18.54–18.82 / 18.52–35.94 |
| Standalone | High | 1280×720 / 100% | Weg | 55.99 → 56.09 | 17.86 → 17.83 | 16.45 → 16.39 | 19.39–20.36 / 19.19–19.40 |
| Standalone | High | 2560×1440 / 75% | Dorf | 34.73 → 34.35 | 28.79 → 29.11 | 26.92 → 27.12 | 30.56–37.13 / 30.44–31.48 |
| Standalone | High | 2560×1440 / 75% | Wald | 35.78 → 35.41 | 27.95 → 28.24 | 26.05 → 26.31 | 29.60–30.49 / 29.69–43.94 |
| Standalone | High | 2560×1440 / 75% | Weg | 34.26 → 34.13 | 29.19 → 29.30 | 27.48 → 27.52 | 31.29–31.88 / 31.01–31.57 |
| Standalone | High | 2560×1440 / 100% | Dorf | 23.96 → 24.03 | 41.73 → 41.62 | 39.77 → 39.63 | 42.72–45.86 / 42.68–44.20 |
| Standalone | High | 2560×1440 / 100% | Wald | 24.80 → 24.20 | 40.32 → 41.32 | 38.30 → 39.36 | 42.31–43.33 / 42.62–44.00 |
| Standalone | High | 2560×1440 / 100% | Weg | 23.96 → 23.94 | 41.74 → 41.77 | 39.77 → 40.08 | 43.74–44.16 / 43.88–44.64 |

## Echte Bildvergleiche und visuelle Bewertung

**48 neue, echte Vergleichsbilder**: drei Positionen ×V1/V2×720p/QHD×Medium/High×PIE/Standalone. Kamera-/Player-/FOV-Metadaten und PNG-Größen geprüft; Kameratoleranz0,00001 cm. Keine synthetischen Bilder. `ComposeReview.py` beschriftet/verkleinert lediglich die Originale. Nachweis `/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19/MatchedPhotoProof.json`.

- [Heilhaus V1/V2, QHD](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19/Heilhaus_V1_V2_QHD.png)
- [Vorplatz V1/V2, QHD](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19/Vorplatz_V1_V2_QHD.png)
- [Wegsaum V1/V2, QHD](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19/Wegsaum_V1_V2_QHD.png)

Originale unter `Saved/VisualV2WorldArtQualityV2/Photos/<PIE|Standalone>_Q<1|2>_<V1|V2>_<1280_720|2560_1440>/`: jeweils `Heilhaus00000.png`, `Vorplatz00000.png`, `Wegsaum00000.png` plus `Result.json`. Zusätzliche erste Diagnosebilder in `V1`, `Review_Merged`, `Review_V2`. Nur die geprüften Vergleichsgruppen werden als vollständige Matrix ausgegeben. Medien bleiben lokal und sind keine Build-Abhängigkeit.

Erreicht: weniger gleichmäßige Streuung, unterschiedliche Gruppengrößen, größere freie Bodenstellen, weiterhin lesbarer Zugang und zusammenhängende Säume. Die Materialzusammenfassung erhält die sichtbare Form. Die Bodenvariation bleibt zurückhaltend, ihre Texturen sind weiterhin dieselben.

Offen: großflächig ruhige Gras-/Erdflächen können weiterhin wiederholend wirken; der Boden ist überwiegend flach. Alte Topfpflanzen besitzen unverändert einfachere große Blattflächen. Feine bestehende Halme, der vorhandene Grasstreifen am weiterführenden Vorplatz und die Originalschatten wurden nicht umfassend umgestaltet. Vorhandener brauner Testwürfel bleibt unangetastet. Temporales Blatt-/Dither-Flimmern ist nicht durch diesen Pass gelöst. Keine menschliche endgültige Art-Freigabe aus Testzahlen abgeleitet; keine Ausweitung auf andere Gebiete.

## Build, Tests, Gameplay und Persistenz

- Mac Development Editor Build Exit0; zuvor wurde der neue reine Development-Diagnosehelfer tatsächlich kompiliert. Keine Gameplay-C++-Datei geändert.
- **49/49** vollständige Projekt-Automationstests bestanden,0 Fehler/Warnungstests/nicht ausgeführte Tests. `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2WorldArtQualityV2/Automation/Report/index.json`.
- Frischer Editor lädt die gespeicherte Map; Inhaltsvergleich nach eindeutigen Komponentennamen exakt gleich, **Map Check0 Fehler/0 Warnungen**, keine schmutzigen Map-/Contentpakete. `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2WorldArtQualityV2/FinalMapCheck/`.
- **Echter Enhanced-Input-PIE-Fußlauf**: 277.21 m,102 Routenschritte, ohne Testteleports; Sprintmaximum 315.00 cm/s. Acht Richtungen, Anhalten, Kollisionen und Begehbarkeit; Wanderer-Dialog/Quest, Liora, Wildkampf/Fang, Inventarmenü, Brücke/Archiv, Save/Load, Heilhaus-Zugang/-Ausgang einschließlich Diagonalen, Heilung/PP, Checkpoint, Kronenfreistellung und NPC-Sprite-Fallback. `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2WorldArtQualityV2/Acceptance/ArtV2FinalFoot/FootTest.json`.
- Ursprünglicher Dev-Slot gesichert und unverändert wiederhergestellt beziehungsweise seine ursprüngliche Abwesenheit wiederhergestellt; `SaveBefore.json`/`SaveRestored.json`. Keine bleibende Änderung des Speichersystems.
- Zusätzliche tatsächliche Tür-/Innenraum-Bildsequenz lokal unter `Saved/VisualV2TAAIntegrationV1/Recordings/WorldArtV2_Door_ArtV2FinalFoot`; keine Behauptung einer separaten Videoabnahme.

Werkzeugbefunde bleiben nachvollziehbar: Ein normaler nativer Exit0 wurde zunächst von der Teststeuerung zu spät als Fehler behandelt; die vollständigen15 Segmente bleiben erhalten. Eine erste native Matrix startete wegen eines nur im Editor sichtbaren Materialfeldes nicht; keine Messdaten daraus verwendet. Korrigiert durch eine explizite Development-Schnittstelle zur sicheren Materialfreigabe; vorhandene Gameplay-Systeme unverändert. Der Übernahme-Guard stoppte vor dem Speichern wegen HISM-Transform-Rundung(maximal2,04×10⁻⁶ Skalierungsfaktor). Nach exakter Prüfung des eigenen Zwischenstands wurde nur dafür3×10⁻⁶ Toleranz zugelassen, Z-Abweichung0; keine weiter gefasste Kartentoleranz. Ein read-only Materialstatistik-Zugriff wurde auf `get_editor_property` korrigiert. Abschließende Prüfungen verwenden die reparierten Werkzeuge. Logs der verworfenen Starts bleiben außerhalb Git erhalten; keine falsche Erfolgsmeldung aus bloßem Skriptende.

Allgemeine vorhandene Engine-Startmeldungen zu macOS-`idevice_id`(Architektur), Audio und MCP-/experimentellen Python-Plugins werden von tatsächlichen Projekt- und Mapfehlern getrennt; nicht pauschal als null Engine-Warnungen dargestellt. Keine neuen Material-/Shaderkompilierfehler als Erfolg akzeptiert.

## Sicherung und Empfehlung

Nur benötigte private Assets, zentrale Map, Autoren-/Wiederherstellungsdaten, geprüfte Development-Werkzeuge, verdichtete Messwerte und Dokumentation werden gezielt gesichert. Keine Screenshots, Videos, Roh-Frame-CSVs, Caches oder vorher bestehenden unversionierten Experimente. `git diff --check` und tatsächlichen Index vor Commit prüfen; regulärer Push auf origin/main und LFS-Verifikation, kein Force-Push und keine kostenpflichtige Aktion. Endgültige Commit-/Remote-Nachweise stehen im lokalen `/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19/GIT_ABSCHLUSS.json` und in der Abschlussantwort.

GitHub-Grenzen wurden lesend überprüft: normale Dateien100 MiB, Push2 GB, LFS-Einzeldatei im Free-Plan2 GB. Der kleine gezielte Sicherungsumfang muss zusätzlich unter Harrys1-GiB-Regel für normale Git-Daten bleiben. Quellen: [große Dateien](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage), [Repository-Limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits).

**Empfehlung:** Den begrenzten V2-Bereich visuell abnehmen. HISM und vorhandene Detailstufen beibehalten; die Materialabschnitte sind vereinfacht, die Pflanzenzahl ist unverändert. Keine weitergehende Pflanzenreduktion und keine behauptete QHD-Beschleunigung. Größere Art-/Performance-Schritte benötigen einen eigenen Auftrag.
