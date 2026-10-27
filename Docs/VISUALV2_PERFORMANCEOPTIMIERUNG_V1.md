# VisualV2 – Performanceoptimierung V1

Stand: 27.10.2026. Ausgangscommit `d1509a725ecf88635746942c1bcb6daa9a1dcd15`.

**Ergebnis:** Die GPU ist in den gemessenen Szenen der überwiegende Engpass.
Eine map-spezifische Vorberechnung der statischen Bodenfarbe spart in gepaarten
Wiederholungen messbar GPU-Zeit. **Stabile 30 FPS bei QHD/High/100 % sind nicht
erreicht; 60 FPS ebenfalls nicht.** Im separaten Spielprozess nach Optimierung
etwa 16,8–22,8 FPS, im abschließenden gepaarten PIE etwa 10,5–14,6 FPS.
Diese Werte sind Szenenmittel und keine garantierten Untergrenzen.

Build erfolgreich. Alle 279 Funktionstests erfolgreich; **strenger QA-Wrapper
Exit 1** wegen zweier bekannter externer iOS-Helferwarnungen in einem Test.
Zwölf Map Checks ohne Fehler/Warnungen. Zehn isolierte Gameplay-/Stabilitäts-
Sitzungen regulär beendet. Keine gewaltsame Prozessbeendigung.

## 1. Hardware und Betrieb

Tatsächlich ermittelt: MacBook Air Mac16,12, Apple M4, 10 CPU-Kerne (4 Performance,
6 Effizienz), 10 GPU-Kerne, 16 GB gemeinsamer Speicher, Metal 4. macOS 27.0.1
(26A434). Unreal Engine 5.8.2, CL 56702186, Metal SM6. Eingebautes Display
2560×1664 Retina. Keine Hardwaredaten geschätzt; keine persönlichen Gerätekennungen
in diesen Bericht übernommen. Zu Beginn Netzbetrieb, Low-Power-Modus aus.

Referenz: Ausgabe **2560×1440**, **High = sg.* 2**, **100 % interne Auflösung**,
keine dynamische Auflösung, kein FPS-Limit, keine Videoaufnahme. Ausgabefenster,
Viewport, ViewRect und interne Auflösung wurden anhand realer Frame-Daten geprüft.
Kamera B unverändert: Pitch −50°, Yaw −45°, FOV 35°. Hintergrunddrosselung nur
für die eigene Sitzung deaktiviert und anschließend auf den vorgefundenen Wert
zurückgesetzt. Keine gespeicherten Qualitäts-/Projekt-INI-Änderungen.

PIE läuft im Editor. Der gesonderte Native-Lauf verwendet denselben Editor-Binary
mit `-game`, eigenem `UserDir` und eigener Save-Fixture. **Kein gepackter Shipping-
Build und kein Nachweis der späteren Auslieferungsleistung.** Editor und Spielprozess
werden getrennt ausgewiesen; ihre Differenz ist wegen Sitzungs-/Lastunterschieden
keine exakt isolierte Messung des reinen Editor-Overheads.

## 2. Rendering-Ausgangszustand

Lumen-GI/Reflections, Virtual Shadow Maps, Mesh Distance Fields, Substrate und
Metal SM6 sind konfiguriert. Raytracing ist im Projekt freigegeben und wird im
Native-Startup als dynamisch aktiviert gemeldet; daraus wird keine gemessene
Aufteilung in Hardware-Raytracing-/Bandbreitenkosten abgeleitet.
Tatsächliches AA im Spiel ist durch den bestehenden map-spezifischen Blendable
**TAA = 2**, obwohl der globale AA-CVar 4 enthält. Keine erneute TSR-Umstellung.

High-Referenz unter anderem: VSM-Cache an, Directional RayCount 8, SamplesPerRay 4,
LodBias 0, Shadow.MaxResolution 1024; Lumen ScreenProbeGather DownsampleFactor 32.
Skylight `SkyLight_Dev`: Stationary, Intensität 1,25, Cubemap-Auflösung 128,
**real_time_capture=False**. Der globale Capture-CVar allein wäre kein Beweis
für laufende Sky-Capture-Kosten. Keine neuen Lichter, kein Recapture pro Frame.
Tag-Nacht-System mit 75° Standard/85° Debug bleibt unverändert.

Detailinventare: [Editor](../Saved/ProjectRefinement/VisualV2PerformanceV1/EditorInventory.json),
[Runtime](../Saved/ProjectRefinement/VisualV2PerformanceV1/RuntimeInventory.json),
[Modelle und tatsächliches Skylight](../Saved/ProjectRefinement/VisualV2PerformanceV1/ModelAndSkyAudit.json).

## 3. Messmethode und Vergleichbarkeit

Sechs feste Orte, jeweils drei Wiederholungen. Uhr jeweils auf 12:00 gestellt,
anschließend normaler 1×-Verlauf mit 120 Minuten pro Tag. Keine zweite Uhr.
4 s Warmup, 5 s Messung je PIE-Segment; Native-Paare 4 + 6 s. Zusätzliche
GI-/Schatten- und Qualitätsproben sind gesonderte Diagnosefälle.

Gepaarte Reihenfolge je Ort A/B, B/A, A/B, nur Bodenmaterial verändert. Im
Native-Lauf wird vor jedem Fall dieselbe eigene Noon-Fixture über die bestehende
Save-/Load-Funktion geladen. Im abschließenden PIE werden die vier gebundenen
Materialpfade je Fall zusätzlich protokolliert. Die nicht gemessenen Zeitabschnitte
enthalten Materialwechsel, Laden und Shader-Warmup.

Letzter tatsächlicher PIE-Bestand: 1539 Actors, 12
Wild-Actors, davon 8 mit natürlichen Aktivitäten und
8 mit Tagesrhythmus; 23 CreatureVisual-
Actors in der gesamten Map einschließlich bestehender Testdarstellung, nicht alle
in derselben Kamera. Die Benchmark-Testparty hat kein modelliertes Begleiterexemplar
(0 Companion-Tags); der echte Begleiter wurde mit bestehender
Zunderlauf/Glurak-Fixture separat im Gameplay-/Mapwechsel geprüft. Keine neuen Spawns.
Kontaktauslösung ist nur im isolierten Messaufbau temporär gesperrt; Bewegung,
Aktivitäten und Tagesrhythmen laufen weiter. Regression dagegen mit Originalprofilen.

Tabellen sind Mittel der drei Segmentmittel. FPS werden je Segment aus seiner
realen mittleren Framezeit berechnet und dann gemittelt; deshalb ist der Kehrwert
der gemittelten Framezeit bei streuenden Läufen nicht exakt der tabellierte FPS-Wert.
Rohdaten enthalten Anzahl, Minimum, Maximum, Standardabweichung und p95.
Alle geprüften Standardsegmente melden aktives Fenster, QHD/100 % und TAA 2.

## 4. Frische ursprüngliche PIE-Basis

Diese Werte wurden in diesem Auftrag neu gemessen, nicht aus dem alten Bericht
übernommen. Sie sind eine erste Referenz; spätere absolute Sitzungswerte driften.

| Ort | FPS | Frame ms | GPU ms | Game ms |
| --- | --- | --- | --- | --- |
| Dorf | 12.29 | 81.41 | 70.81 | 8.41 |
| Wiese | 12.76 | 78.39 | 72.57 | 9.26 |
| Wald | 10.68 | 93.61 | 81.84 | 9.55 |
| Waldweg | 11.44 | 87.40 | 76.34 | 9.68 |
| Gewaesser | 11.29 | 88.58 | 82.12 | 9.68 |
| Gruppe | 11.92 | 83.92 | 77.43 | 9.53 |

## 5. Engpass und größte GPU-Kosten

GPU-Zeiten liegen weit über Game-Thread-Zeiten. Im Native-Spielprozess beträgt
Game meist wenige Millisekunden, während die GPU mehrere Dutzend ms benötigt.
Im Editor kommen deutlich höhere und schwankende CPU-/GPU-Lasten hinzu.
**Überwiegend GPU-limitiert** ist damit belegt; reine FPS allein waren nicht
Diagnosegrundlage. Kurzzeitige Game-Thread-Ausreißer werden nicht als konstante
Gameplay-Kosten interpretiert.

Separates echtes `ProfileGPU`-Einzelbild außerhalb der Zeitmatrix:

| GPU-Scope | Inklusive Zeit ms | Einordnung |
| --- | --- | --- |
| BasePass | 22,033 | größte einzelne dargestellte Rendergruppe |
| LumenScreenProbeGather | 14,366 | wichtiger GI-Kostentreiber |
| ShadowProjectionOnOpaque | 11,122 | deutlich teurer als reine ShadowDepths |
| PrePass | 3,151 | Geometrie/Vorpass |
| PostProcessing | 2,971 | kleiner als BasePass/GI/Schatten |
| ShadowDepths | 0,991 | dieses Einzelbild, keine allgemeine Obergrenze |
| Slate Editor + Nachrichtenlog | 2,646 | zusätzlicher Editor-Anteil dieses Profilerbildes |

Keine Summe über überlappende inklusive/exklusive Scopes und keine Rangfolge
aus nur einem Einzelbild. Native-CSV-Nachprüfung bestätigt: Basepass-Median im
kontrollierten Scout rund 23,2 ms mit Original, rund 11,6–11,7 ms mit Farbbake.
Die gemessene Gesamt-GPU-Zeit sinkt dabei von etwa 66 auf 52–53 ms.

Aggregiertes RenderThreadTime ist im ersten PIE-Summenzähler teilweise nahe null
und damit unbrauchbar als vollständige CPU-Zeit. Im Native-Lauf enthält es erhebliche
GPU-/Present-Warteanteile und liegt nahe der Framezeit. **Keine Behauptung, dass
die CPU so lange aktiv rechnet.** Exklusive CSV-Render-Scopes und die GPU-Messung
werden getrennt verwendet. Draw-/Primitive-Zähler liefern hier unbrauchbare Nullen;
kein Nachweis von null Draw Calls oder gemessenem Overdraw. Eine echte GPU-
Bandbreiten-/Takt-/Shader-Kernel-Aufschlüsselung beziehungsweise vollständige
Insights-CPU-Busy-Analyse liegt nicht vor. Lokaler CSV-Profiler und GPU Visualizer
waren die verwendbare Alternative; keine Engine- oder Metal-Treiberänderung.

## 6. Vegetation, Modelle und Materialien

199 Editor-/203 Runtime-StaticMesh-Assets, 111 Materialmaster und 23 SkeletalMesh-
Assets im ursprünglichen Inventar. Die Hauptboden-/Wege-/Wassermaterialien weisen
hohe Shader-Statistikschätzungen auf (Boden 1631, Hauptweg 1647, Nordweg 1735,
Wasser 1517 Pixelinstruktionen). Dies sind **Compiler-Schätzwerte, keine gemessenen
Metal-Kernel-Laufzeiten**. Der originale Boden scannt im statischen Farbteil 118
Wegsegmente und verbindet mehrere prozedurale Farb-/Texturteile.

Bestehende große Eiche: LOD0 12.068 Dreiecke, drei LODs; Busch 3.284, drei LODs.
Bereits vorhanden: Instancing/HISM, unter anderem Grasgruppen mit 1709 / 1162 /
677 Instanzen und 392 / 518 / 434 Dreiecken je LOD0-Mesh. Ältere Grasgruppe 990 ×
1056. Auffällig hohe Platzierungsbudgets: GardenFlowers 225 × 23.516 Dreiecke,
MossCushion 336 × 6624. **Platzierte LOD0-Summen sind nicht die tatsächlich
sichtbaren/gezeichneten Dreiecke.** Culling, Distanz, verdeckte Innenräume und
LOD-Auswahl verhindern eine solche Gleichsetzung.

Repräsentative tatsächlich aus Asset-Registry-Tags gelesene Modellwerte:

| Modell | LOD0-Dreiecke | LODs | Materialslots |
| --- | --- | --- | --- |
| SK_Player_V61 | 47744 | 1 | 1 |
| SK_Glumanda_V11 | 18245 | 1 | 1 |
| SK_Bisasam_Skin | 21545 | 1 | 1 |
| SK_Pikachu_Meshy | 137094 | 1 | 1 |
| SK_Nebulak_V6 | 23527 | 1 | 3 |
| SK_Glurak_V61 | 246066 | 1 | 2 |

Pikachu/Glurak und mehrere NPCs besitzen hohe Einzelbudgets; daraus allein folgt
kein dominanter Frameengpass. Skeletal-Hide-Diagnose ergab keinen überzeugenden
Gesamt-GPU-Gewinn. Originalmodelle, Texturen, Rigs, Animationen und NPC-Bibliothek
wurden nicht verändert. Keine pauschale Entfernung/Reduktion von Gras oder Kronen.
Vegetations- und Schattenablationen liefern keine ausreichend belastbare größere
Verbesserung für eine Produktionseinstellung. Gezielte neue LOD-Varianten und eine
vollständige Masked-Overdraw-Aufschlüsselung bleiben offen. Dichter Bestand bleibt erhalten.

## 7. Isolierte Maßnahmen und Entscheidung

| Maßnahme | Tatsächlicher Befund | Entscheidung / Risiko |
| --- | --- | --- |
| Statische Grundfarbe vorberechnen | beide vollständigen gepaarten Matrizen positiv; siehe Tabellen | übernommen, geringe feine Texturweichzeichnung, erneuter Bake bei Quelländerungen |
| Exakte BVH-Wegsuche im Shader | deutlich weniger CPU-validierte Distanztests, kein entsprechender GPU-Gewinn | verworfen; CPU-Operationszahl ist kein GPU-Nachweis |
| Distanz-/Breitenfeldtextur | geringe/instabile Zeitersparnis, zusätzliche Interpolation | verworfen |
| Einfaches fremdes Grasmaterial | Diagnose-GPU rund 70 ms statt 83–87 ms | sichtbarer Material-/Farbwechsel, verworfen |
| Einfacher Boden inklusive Wege/Wasser | Diagnose-GPU rund 62 ms, hoher CPU-Ausreißer | andere Bildwirkung, keine Produktionsübernahme |
| Kleine Pflanzen aus / ohne Schatten | nur begrenzter Gewinn gegenüber Kontrollen | kein pauschaler Dichte-/Schattenverlust |
| Ganze Vegetation aus | kein überzeugender großer isolierter Gewinn in der Probe | keine Entfernung |
| Skelettmodelle aus | kein überzeugender GPU-Gewinn | keine Modelloptimierung auf Verdacht |
| GI aus | etwa 72 statt 81–82 ms Diagnose-GPU | Beleuchtungsfunktion verloren, nicht übernommen |
| Lumen IntegrateDownsample 2 / GatherDownsample 32 | etwa 81–83 ms Diagnose-GPU | kein belastbarer Vorteil; letzterer war bereits 32 |
| Lumen Gather-Qualität 0,5 / 0,25 | Native-Kontrollen driften, Gesamtframe nicht zuverlässig verbessert | nicht übernommen |
| SSGI statt Lumen | Laufdrift verhindert belastbare Ursachenzuordnung | keine ausreichende gemeinsame visuelle/Innenraumfreigabe, nicht übernommen |
| Alle Schatten aus | etwa 69 statt 83 ms Diagnose-GPU | deutlicher Verlust räumlicher Wirkung, nicht übernommen |
| VSM RayCount 2 / Bias +1 / RayCount 4 | kleine beziehungsweise driftbehaftete Differenzen | kein globaler Qualitätsverlust für unklaren Gewinn |
| Reflections aus / Nanite aus | kein überzeugender Gewinn, etwa 82–83 ms | nicht übernommen |
| Postprocessing aus | etwa 78 statt 82 ms, verändert unter anderem AA | Diagnose, nicht vergleichbare Produktionsqualität |
| Software-Lumen-Umschaltung | GPU nahezu unverändert, Frame verändert | kein belegter kostenloser Gewinn |
| GPU-CSV-/GPU-Statistik aus | Gesamtframe nahezu unverändert in alternierender Kontrollfolge | Instrumentierung erklärt nicht allein die schlechte Leistung |

Die frühen Einzelproben dienen der Eingrenzung, nicht als garantierte kausale
Ersparnis. Aufwendige Inventar-/Shaderstatistik-Abfragen fanden außerhalb der
Messfenster statt. Die deutlich positivere Materiallösung wurde wiederholt und
an allen sechs Orten bestätigt. Keine umfangreichen Gameplay-Refactorings.

## 8. Übernommene Optimierung

Nur vier Materialslots: `V2_Ground`, `Hill_Step_Low`, `Hill_Step_Mid`,
`Hill_Lookout`, jeweils Slot 0. Neues `M_PV1_BakedGroundSRGB` plus
`T_PV1_GroundColorSRGB`; Original `M_EQ3_Ground` bleibt unverändert.

Ein unbeleuchteter Material-Draw berechnet einmalig **ausschließlich statische
BaseColor** über den tatsächlichen Bodenbereich X −6000…3000, Y −3250…3250 cm.
4096², sRGB, BC7, vollständige Mips, eine nicht gestreamte Textur. BC7 mit Mips
belegt rechnerisch ungefähr 21,3 MiB GPU-Speicher; tatsächliche Ressourcenbelegung
ist nicht separat gemessen. Benötigtes PNG etwa 37,8 MiB auf Datenträger.
Keine Schatten, Lichter, Spielfiguren oder Pokémon eingebrannt. Keine Szene als
flaches Hintergrundbild ersetzt. Weltbasierte Normalen, Roughness, Specular,
DefaultLit und bestehende Geometrie bleiben erhalten.

Die gesamte vom bestehenden `AuditScene` erfasste Szene ist vor/nach
Normalisierung dieser vier Slots gleich: Actors, Transformationen, Instanzen,
Kollisionen, Materialslots der übrigen Objekte, Licht- und Postprocess-Eigenschaften.
Keine Landschafts- oder Heilhausgestaltung geändert. [Übernahmekontrolle](../Saved/ProjectRefinement/VisualV2PerformanceV1/Applied.json).

Herkunft/Hash/Weltgrenzen: [Bake.json](../Art/World/VisualV2PerformanceV1/Bake.json).
Bei Änderungen am Quellmaterial, seinen Texturen, eingebetteten Wegverläufen oder
Weltbereich muss erneut gebacken und visuell geprüft werden. Kein automatischer
Reimport und keine Quellenkaschierung. Die einzigen verworfenen Dateien sind acht
**in diesem Auftrag neu erzeugte** Entwürfe; ihre Produktionsreferenzen wurden
vorher geprüft. Kein alter QA-/Arbeitsordner wurde gelöscht.

## 9. Vorher/nachher – separater Spielprozess

`NativeMatrix05`, jeweils drei benachbarte Paare, unverändertes QHD/High/100 %,
normale Beleuchtung und KI. Dieses Ergebnis belegt den Materialgewinn unabhängig
vom normalen Editorfenster. Es ist keine Shipping-Prognose.

| Ort | FPS vorher | FPS nachher | Frame ms vorher → nachher | GPU ms vorher → nachher | Game ms vorher → nachher |
| --- | --- | --- | --- | --- | --- |
| Dorf | 18.43 | 22.01 | 54.29 → 45.56 | 51.36 → 42.46 | 2.53 → 2.71 |
| Wiese | 13.89 | 22.81 | 73.28 → 43.96 | 66.05 → 40.35 | 5.11 → 3.94 |
| Wald | 13.50 | 16.80 | 74.14 → 59.59 | 70.36 → 55.71 | 4.24 → 3.41 |
| Waldweg | 15.43 | 18.58 | 64.81 → 53.84 | 60.71 → 49.77 | 3.56 → 3.30 |
| Gewaesser | 14.17 | 16.93 | 70.56 → 59.07 | 66.41 → 55.06 | 3.35 → 3.10 |
| Gruppe | 15.07 | 19.27 | 66.34 → 51.90 | 62.23 → 47.86 | 3.45 → 3.20 |

Zusätzliche Streuung und der verfügbare Render-Thread-Wandzeitzähler:

| Ort | Original FPS-Spanne | Optimiert FPS-Spanne | Frame p95 ms vorher → nachher | RT-Wandzeit ms vorher → nachher |
| --- | --- | --- | --- | --- |
| Dorf | 17.76–18.92 | 20.38–22.96 | 58.09 → 49.49 | 54.29 → 45.56 |
| Wiese | 11.68–16.17 | 21.21–23.80 | 107.77 → 47.70 | 73.36 → 43.95 |
| Wald | 12.93–13.85 | 16.38–17.55 | 79.20 → 66.35 | 73.84 → 59.56 |
| Waldweg | 15.23–15.57 | 18.45–18.84 | 69.41 → 57.87 | 64.78 → 53.81 |
| Gewaesser | 14.15–14.19 | 16.90–16.95 | 75.52 → 64.10 | 70.53 → 59.07 |
| Gruppe | 15.05–15.11 | 19.21–19.32 | 71.56 → 57.12 | 66.32 → 51.91 |

FPS-Spannen beziehen sich auf die drei Segmentmittel, p95 ist das Mittel der drei
Frame-p95-Werte. RT-Wandzeit enthält GPU-/Present-Warten, **keine CPU-Busy-Zeit**.

Wiese streut besonders: Original-FPS-Einzelmittel 16,17 / 11,68 / 13,81;
optimiert 23,80 / 23,42 / 21,21. Deshalb keine Behauptung einer überall konstanten
prozentualen Beschleunigung. NSProcessInfo-Thermalstatus in dieser Reihe beginnt
nominal und wechselt zu fair (11 beziehungsweise 72 Stichproben), nicht serious/
critical. Das beweist keine konkrete Taktdrosselung oder deren alleinige Ursache.

## 10. Vorher/nachher – frischer gepaarter PIE-Lauf

`PairedPIE02`, drei Paare je Ort. Tatsächlich gebundene Materialien dokumentiert.
Diese Reihe ist für den unmittelbaren Editorvergleich maßgeblich. Sie wird nicht
mit der früheren Sitzung zu einer vermeintlichen Beschleunigung vermischt.

| Ort | FPS vorher | FPS nachher | Frame ms vorher → nachher | GPU ms vorher → nachher | Game ms vorher → nachher |
| --- | --- | --- | --- | --- | --- |
| Dorf | 10.24 | 11.85 | 97.92 → 84.72 | 85.48 → 72.72 | 11.89 → 13.59 |
| Wiese | 9.38 | 14.58 | 107.05 → 68.71 | 94.75 → 61.25 | 23.62 → 23.67 |
| Wald | 8.87 | 10.51 | 112.73 → 95.11 | 99.20 → 81.97 | 14.24 → 17.29 |
| Waldweg | 9.36 | 11.58 | 107.10 → 86.35 | 94.90 → 75.39 | 16.74 → 11.92 |
| Gewaesser | 9.39 | 11.16 | 106.49 → 89.59 | 100.51 → 83.29 | 12.68 → 11.51 |
| Gruppe | 9.95 | 12.46 | 100.55 → 80.28 | 93.31 → 73.16 | 12.06 → 11.79 |

In beiden Betriebsarten ist die Materialänderung positiv. Höhere absolute
Editorzeiten bleiben eine reale Einschränkung. Die optimierte ungepaarte
PIE-Nachmessung war ebenfalls schwankend (etwa 10,5–15 FPS); vollständige Werte
und Ausreißer bleiben im Rohdatensatz. Keine Auswahl nur des schnellsten Laufs.
Native-Lighting-Kontrollen drifteten in einer längeren Reihe beispielsweise von
rund 40 auf 56 ms GPU. Thermik, Speicherlast, Editor-/Shader-/DDC-Aktivität sind
mögliche Beiträge; kein einzelner davon wurde als alleinige Ursache bewiesen.

## 11. Performance nach Tageszeit

Optimierter PIE-Bestand, bestehende Pokémon-Gruppe, drei Messsegmente je Zeit.
Die Uhr läuft innerhalb eines Segments normal weiter; Angabe ist dessen Startzeit.

| Zeit | FPS | Frame ms | GPU ms | Game ms |
| --- | --- | --- | --- | --- |
| 06:00 | 14.29 | 69.97 | 63.91 | 11.12 |
| 09:00 | 14.08 | 71.01 | 64.74 | 12.10 |
| 12:00 | 13.99 | 71.49 | 65.00 | 15.09 |
| 19:00 | 14.23 | 70.28 | 63.93 | 15.27 |
| 22:00 | 14.17 | 70.58 | 64.25 | 16.27 |
| 00:00 | 14.35 | 69.66 | 63.50 | 11.32 |

Kein herausragender zusätzlicher Nachtkostentreiber in dieser Ortsstichprobe.
Alle übrigen Licht-, Sonnen-, Weltuhr- und Tagesrhythmusregeln sind unverändert.

## 12. Getrennte Qualitäts-/Auflösungsalternativen

NativeAlternatives06, jeweils drei Läufe, derselbe zusätzliche Wald-Messpunkt
(−2960, 1700, 50,15 cm), jeweils Farbbake und 12:00. Dieser Punkt ist nicht der
Waldpunkt der Sechs-Orte-Matrix (−4300, 1550). Interleavte Umkehrreihenfolge.
QHD-Ausgabe bleibt, intern 75 % entspricht **1920×1080**, kein unverändertes QHD.

| Getrennte Alternative | FPS Mittel | Frame ms | GPU ms | FPS der drei Läufe: Spanne |
| --- | --- | --- | --- | --- |
| High100 | 20.76 | 48.37 | 45.12 | 19.50–22.66 |
| High75 | 28.41 | 35.24 | 31.81 | 27.41–29.71 |
| Medium100 | 26.65 | 37.59 | 36.39 | 25.27–27.86 |
| Medium75 | 36.60 | 27.37 | 26.20 | 34.53–38.16 |

Nur Medium/75 % liegt hier in allen drei **Segmentmitteln** über 30 FPS. Das
ist keine stabile 30-FPS-Freigabe für alle Orte, Tageszeiten und längere Sitzungen.
High/75 % bleibt im Mittel unter 30. Keine dieser Alternativen ist als Standard
übernommen. Eine solche Qualitätsentscheidung benötigt einen gesonderten,
vollständigen Bild-/Gameplayvergleich. 60 FPS werden auch hier nicht erreicht.

## 13. Echte Bildvergleiche und Qualitätsgrenzen

22 echte QHD-PNGs in elf Paaren. Identische Kamera, Spielerposition, Uhrzeit,
Grafikbedingungen und eingefrorene Weltzeit je Paar maschinell geprüft. Keine
KI-generierten oder künstlich nachgebauten Bilder. Normale Spielkamera.

| Szene/Zeit | Vorher | Nachher |
| --- | --- | --- |
| Dorf | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Dorf_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Dorf_Baked.png) |
| Wiese | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Wiese_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Wiese_Baked.png) |
| Wald | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Wald_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Wald_Baked.png) |
| Waldweg | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Waldweg_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Waldweg_Baked.png) |
| Gewaesser | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gewaesser_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gewaesser_Baked.png) |
| Gruppe | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe_Baked.png) |
| Gruppe06 | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe06_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe06_Baked.png) |
| Gruppe09 | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe09_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe09_Baked.png) |
| Gruppe19 | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe19_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe19_Baked.png) |
| Gruppe22 | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe22_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbPhotos01/Gruppe22_Baked.png) |
| Gruppe00 | [Original](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbLastPair02/Gruppe00_Original.png) | [Optimiert](../Saved/ProjectRefinement/VisualV2PerformanceV1/SrgbLastPair02/Gruppe00_Baked.png) |

Bewertung: dichte Kronen, plastische Gräser, Bodenfarben/Wegeverläufe,
Charaktermaßstab und dynamische Tag-/Nachtwirkung bleiben erhalten. **Feine
Bodenfarbdetails sind etwas weicher.** Das ist der dokumentierte begrenzte
Qualitätskompromiss, keine vollkommen pixelidentische Ausgabe. Wege, 3D-Gras,
Figur und Bäume werden nicht ausgedünnt. Die frühere lineare, ungeeigneter
abgedeckte Bake-Variante wurde zugunsten der sRGB-Variante verworfen.

Der letzte Screenshot einer früheren Schleife wurde vor der verzögerten Aufnahme
zu früh zurückgestellt. Das 00:00-Paar wurde deshalb separat mit zusätzlicher
Renderwartezeit vollständig wiederholt (`SrgbLastPair02`) und ersetzt das alte
Paar. Die übrigen Fehlversuche bleiben als QA-Log erhalten, nicht als Abnahmebild.
Innenraum-Tag/Nacht/Load-Aufnahmen zusätzlich in `Gameplay01`.

## 14. Gameplay und Controller

Echter zusammenhängender PIE-Ablauf `Gameplay01`: 18 bestandene Prüfungen,
Start 09:00, 75°/85°-Umschaltung, Pause/Resume, Hauptmenü, realer vorhandener
Heilhauszugang/-ausgang, Innenraumkamera, Save/Load bei Nacht einschließlich
Teamidentität, KP/AP und unabhängigem Kontrollpunkt, Mitternacht, ClassicBattle-
Sieg und Rückkehr. Kampf löst soziale Reservierungen; anschließend wieder Steuerung.

Zusätzlich echter Tastatur-Fußlauf über native UI-Eingaben mit W/D, Richtungswechsel,
Shift-Sprint und Tab-Menü. Zunächst fehlte Spieleingabefokus: unveränderte Position,
keine bestandene Bewegung behauptet. Nach normaler Fokuswiederherstellung über
bestehende WidgetLibrary bewegte sich die Figur von (−200, −100) auf
(301,21, −236,68); Menü sichtbar geöffnet/geschlossen. Kein Input-Code geändert.

Isolierte Bewegungsprüfung: acht Richtungen, L3-Sprint an/aus, X-Schnellmenü,
D-Pad, L/R, A zurück und Fokuswiederherstellung über vorhandene Eingabesimulation.
Kein neuer physischer Switch-Pro-Hardwaretest behauptet. Die funktionierende
Grundbelegung bleibt unverändert.

Fang, Teamplatz-/Begleiterwechsel, EP, Entwicklung, Heilung/Kontrollpunkt und
weitere Grenzfälle werden zusätzlich durch die vollständige Automation geprüft.
**Kein zusätzlicher visueller PIE-Fang- oder vollständiger Entwicklungsdurchlauf
behauptet.** Dieser Auftrag verändert nur ein Material und keine Gameplaylogik.

## 15. KI-/Tagesrhythmusregression

93.28 s, 165 reale Stichproben bei acht
aktiven Instanzen aus den sechs bestehenden Testarten. Beobachtet: Wander,
Idle, Rest, Sleep, Forage und Social. Gegenseitige Partnerreservierungen,
Habitatschutz, keine Schlafbewegung/Schlafpartner, Pause und direkte Zeitsprünge
wurden in jeder relevanten Stichprobe kontrolliert. Profile, Zeitgewichte und
Artparameter unverändert. Reaktionen/Kontakt-/Fluchtgrenzen zusätzlich Automation.
Keine neuen Arten, Lebensräume, Tageszeit-Spawns oder zentrale KI-Schleife.
[Beobachtungsdaten](../Saved/ProjectRefinement/VisualV2PerformanceV1/Rhythm01/Result.json).

## 16. Stabilität und Reisen

Zehn gezielt protokollierte Sitzungen: Gameplay, Rhythmus, normal, aktive Pokémon,
Bewegung/Menüs, Tagesphasenwechsel, Save/Load, Kampf, Innenraum, Map-Rundlauf.
Alle bestanden; reguläre Stopps 0.202 bis
0.409 s. Dazu die separaten längeren Benchmark-
und Bildprüfsitzungen. Mehrminütige kontinuierliche Läufe erfolgreich; kein
stundenlanger Soak-Test behauptet. Kein Stillstand reproduziert und keine
unbelegte Reparatur des historischen Hängers behauptet.

Realer OpenLevel-Rundlauf VisualV2 → bestehende Dev_TestMap → VisualV2:
identische GameInstance/Weltuhr, Team/KP/AP unverändert, nur auf VisualV2 aktiver
Tag-Nacht-Zyklus, danach genau ein sichtbarer regulärer Begleiter und acht gültige
Wildrhythmen. Kontroll-/Ladezustände und Spielersteuerung wieder aktiv.
[Stopprotokoll](../Saved/ProjectRefinement/VisualV2PerformanceV1/RegressionStops.json),
[Reise](../Saved/ProjectRefinement/VisualV2PerformanceV1/Travel01/Result.json).

## 17. Build, Automation, Map Checks und Warnungen

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Editor-Build Mac Development | Exit 0, 27,93 s einschließlich Editor-Abschlusswarten |
| Vollständige relevante Automation | 278 sauber + 1 mit Warnungen = 279 funktional erfolgreich; 0 fehlgeschlagen/übersprungen |
| Engine-Testprozess | Exit 0 |
| Unveränderter strenger QA-Wrapper | **Exit 1**, nicht vollständig bestanden |
| Zwölf bestehende Map Checks | je 0 Fehler / 0 Warnungen |
| Zehn Gameplay-/Stop-Sitzungen | bestanden, regulär beendet |
| Originalschutz per SHA256 | 3964 von 3965 Originaldateien unverändert; einzig erlaubte VisualV2-Map geändert |

Warnungstest: `PokeMonster.BiomeV11.ProductionMoves.StringShot`, Zustand Success,
zwei `LogHAL`-Warnungen des externen `idevice_id`: Bad CPU type / Failed to launch
Tool. Kein Filter, keine erneute Automation nur zum Erzielen von Grün.
[QA-Klassifikation](../Saved/ProjectRefinement/VisualV2PerformanceV1/QAClassification.json),
[Original-Automation](../Saved/ProjectRefinement/PerformanceV1Automation/Report/index.json),
[Build](../Saved/ProjectRefinement/PerformanceV1Build/Result.json),
[alle Map Checks](../Saved/ProjectRefinement/VisualV2PerformanceV1/MapChecksClassified.json).

Weitere Befunde getrennt: vorbestehende Engine-/Python-Namenskollisionen, generische
Startup-Condition-Meldungen und CVar-/FindConsoleObject-Hinweise. Native `-game`-
Startup lädt experimentelle Engine-Toolset-Pythonmodule, denen Editorklassen
(`ToolsetDefinition`, `AgentSkill`, `PythonTestRunner`) fehlen; die Tracebacks sind
vorhanden, kein stillschweigend warnungsfreier Native-Log behauptet. Sie verhindern
die erfolgreichen Messungen nicht und wurden nicht durch Projektumbauten kaschiert.
Ein CharacterMovement-MaxIterations-Hinweis beim Native-Start liegt außerhalb der
Messfenster. Eigene vorläufige Python-API-/Bildexport-/Parserfehler wurden korrigiert;
sie sind nicht als Gameplay-Testfehler oder Engine-Absturz umgedeutet. Map-Check-
Auswertung berücksichtigt die tatsächliche deutsche Loglokalisierung.

## 18. Schutz und verbleibende Grenzen

Alle 318 ursprünglichen `.sav`-Dateien, sämtliche
ursprünglichen Art-/Content-Quellen außer der erlaubten Map und alle
33 geschützten unversionierten Dateien hashgleich.
Zwölf ursprüngliche Map-Pfade erhalten; Westland/Biom-Map und weitere Maps
unverändert. Beide Vollbackup-Refs weiterhin `03492bd96b4dba44692f675c19d5f11abfa86b4b`.
Kein Backup neu erzeugt, keine neue Map/Projektkopie/Worktree. [Schutznachweis](../Saved/ProjectRefinement/VisualV2PerformanceV1/ProtectionFinal.json).

Keine Gameplay-, Uhr-, KI-, Kamera-, Controller-, NPC-, Modell- oder Animations-
Quellen verändert. Kein LFS-Prune, keine Git-Historienänderung. Eigene isolierte
Testspielstände liegen nur im bestehenden Saved-Prüfbereich/benannten QA-Slots.

30/60 FPS bleiben offen. Nächste sinnvolle, gesondert zu prüfende Kandidaten:
Restkosten der ebenfalls prozeduralen Wege, profilierte GI-/Schattenqualität sowie
gezielte abgeleitete Vegetations-/Modell-LODs. Keine dieser Maßnahmen ist bereits
als erfolgreiche, gleichwertige Lösung freigegeben. Eine pauschale Lumenabschaltung
oder Weltentleerung wäre keine Fortsetzung dieser qualitätserhaltenden Optimierung.

Auf Harrys Freigaberückmeldung wurde die Bildschirmaufnahme-Vorabprüfung erneut
lesend ausgeführt. Im aktuellen Prüfprozess weiterhin `false`; keine OS-Einstellung
geändert und keine native Aufnahme als erfolgreich getestet ausgegeben. Sämtliche
hier angegebenen Leistungsfenster bleiben ohne Aufnahme.

## 19. Reproduktion und lokale Nachweise

[Werkzeugablauf](../Tools/VisualV2PerformanceV1/README.md),
[alle Einzelmessungen einschließlich Streuung/p95](../Saved/ProjectRefinement/VisualV2PerformanceV1/Measurements.json),
[Native-Paare](../Saved/ProjectRefinement/VisualV2PerformanceV1/NativeMatrix05/Result.json),
[PIE-Paare mit tatsächlichen Materialpfaden](../Saved/ProjectRefinement/VisualV2PerformanceV1/PairedPIE02/Result.json),
[Pixel-/Kameraprüfung](../Saved/ProjectRefinement/VisualV2PerformanceV1/ScreenshotValidation.json).
Rohlogs/CSV/Screenshots bleiben lokal unter Saved, wie in AGENTS vorgegeben;
sie werden nicht als Kontrollmedien in Git hochgeladen. Links sind lokal nutzbar.
Keine Medieninterpolation und keine Messung aus der Video-Wiedergaberate.

## 20. Git-Abschluss

Versioniert werden nur die geprüften vier Map-Zuweisungen, zwei neue Unreal-
Assets, erforderliche Farbquelle/Provenienz, exakt begrenzte LFS-Regel, zugehörige
Prüfwerkzeuge und diese Dokumentation. Die 33 ursprünglich unversionierten
Dateien bleiben außerhalb des Commits. Der Anfangsstand ist oben benannt.

Implementierung und geprüfter Ausgangsbericht: [`817e9121`](https://github.com/Harrys-F/PokeMonster/commit/817e9121a4e2e2de5617dbdfc5d74a8c4086a211).
Der normale Push war erfolgreich. Anschließend waren lokales `main`,
`origin/main` und der per `ls-remote` gelesene Serverstand identisch. Alle vier
LFS-Objekte (79.805.847 Bytes) wurden vollständig vom Server gelesen und ihre
SHA-256/Größe gegen den Commit geprüft. Keine ausstehenden LFS-Übertragungen.
Keine zusätzlichen Archiv-/Dateikopien beim Streaming-Download.

Der ergänzende Dokumentationscommit enthält ausschließlich diesen Git-Nachweis
und seine Berichtsvorlage; keine weitere Produktänderung. Der aktuelle abschließende
Branchstand ist zusätzlich im Abschlusschat sowie lokal in
[GitFinal.json](../Saved/ProjectRefinement/VisualV2PerformanceV1/GitFinal.json)
verzeichnet. Kein Force-Push und keine Änderung des bestätigten 0-USD-LFS-Budgets.
Bei Kontingent-/Abrechnungsfehlern wird abgebrochen und kein synchroner Remote
behauptet. Die technische Abnahme ist eine erfolgreiche, begrenzte Optimierungs-
und Analysephase; das Leistungsziel 30 FPS ist ausdrücklich nicht erreicht.
