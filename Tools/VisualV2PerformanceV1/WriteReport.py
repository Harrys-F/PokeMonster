"""Report only measured results; local raw evidence is intentionally not published."""
from pathlib import Path
import json,statistics as st,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1'
def read(n):return json.loads((D/n).read_text())
rows=read('Measurements.json')['segments'];protection=read('ProtectionFinal.json');maps=read('MapChecksClassified.json');qa=read('QAClassification.json');runtime=read('FinalRuntimeAudit.json');assert protection['passed']and maps['passed']and qa['summary']['failed']==0
sites=['Dorf','Wiese','Wald','Waldweg','Gewaesser','Gruppe']
def subset(batch,site=None,action=None,name=None):return [r for r in rows if r['batch']==batch and(site is None or r['case']['site']=='S_'+site)and(action is None or r['case'].get('action','Control')==action)and(name is None or r['case']['name']==name)]
def mean(v,k):
 return st.mean(r['fps']if k=='fps'else r['frame_ms']['mean']if k=='frame'else r['stats'][k]['mean']for r in v)
def f(v,k):return f'{mean(v,k):.2f}'
def table(headers,body):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,r))+' |'for r in body])
def paired(batch,original):
 out=[]
 for site in sites:
  a=subset(batch,site,original);b=subset(batch,site,'BakedSRGB');assert len(a)==len(b)==3
  out.append([site,f(a,'fps'),f(b,'fps'),f(a,'frame')+' → '+f(b,'frame'),f(a,'GPUTime')+' → '+f(b,'GPUTime'),f(a,'GameThreadTime')+' → '+f(b,'GameThreadTime')])
 return table(['Ort','FPS vorher','FPS nachher','Frame ms vorher → nachher','GPU ms vorher → nachher','Game ms vorher → nachher'],out)
baseline=table(['Ort','FPS','Frame ms','GPU ms','Game ms'],[[n,*[f(subset('Baseline01',name=n),k)for k in ['fps','frame','GPUTime','GameThreadTime']]]for n in sites])
days=table(['Zeit','FPS','Frame ms','GPU ms','Game ms'],[[f'{h:02d}:00',*[f(subset('OptimizedPIE01',name='Gruppe'if h==12 else'Gruppe'+str(h)),k)for k in ['fps','frame','GPUTime','GameThreadTime']]]for h in [6,9,12,19,22,0]])
alt=[]
for n in ['High100','High75','Medium100','Medium75']:
 a=[r for r in subset('NativeAlternatives06')if r['case']['name'].startswith(n)];assert len(a)==3
 alt.append([n,f(a,'fps'),f(a,'frame'),f(a,'GPUTime'),f"{min(r['fps']for r in a):.2f}–{max(r['fps']for r in a):.2f}"])
alt=table(['Getrennte Alternative','FPS Mittel','Frame ms','GPU ms','FPS der drei Läufe: Spanne'],alt)
rhythm=read('Rhythm01/Result.json');stops=read('RegressionStops.json');assert len(stops)==10 and all(r['result']['passed']for r in stops)
shots=[]
for folder in ['SrgbPhotos01','SrgbLastPair02']:
 r=read(folder+'/Result.json');assert r['passed'];ss=r['shots']
 for i in range(0,len(ss),2):
  a,b=ss[i:i+2]
  if folder=='SrgbPhotos01'and a['name']=='Gruppe00':continue
  for k in ['clock','world_seconds','player','rotation','fov','world_paused']:assert a[k]==b[k],(a['name'],k)
  assert all(abs(x-y)<1e-5 for x,y in zip(a['camera'],b['camera']))
  for x in [a,b]:
   with(R/x['file']).open('rb')as file:head=file.read(24)
   assert head[:8]==b'\x89PNG\r\n\x1a\n'and struct.unpack('>II',head[16:24])==(2560,1440)
  shots.append([a['name'],f"[Original](../{a['file']})",f"[Optimiert](../{b['file']})"])
assert len(shots)==11
(D/'ScreenshotValidation.json').write_text(json.dumps({'pairs':11,'images':22,'qhd':True,'same_camera_and_clock':True,'final_midnight_pair':'SrgbLastPair02'},indent=2))
scene=read('Applied.json');assert scene['only_four_material_slots'];models=read('ModelAndSkyAudit.json');modelrows=[]
for row in models['skeletal']:
 p=row['asset'];tags=row['registry_LOD0']
 if any(n in p for n in ['YoungTrainer','SK_Glumanda','SK_Bisasam','SK_Pikachu','SK_Glurak','SK_Nebulak']):modelrows.append([p.rsplit('/',1)[-1].split('.')[0],tags['Triangles'],tags['LODs'],row['material_slots']])
scope=read('DiscardedOwnedDrafts.json');assert scope['original_files_removed']==0
report=f'''# VisualV2 – Performanceoptimierung V1

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

Letzter tatsächlicher PIE-Bestand: {runtime['actor_count']} Actors, {runtime['wild_actors']}
Wild-Actors, davon {runtime['active_wild_activities']} mit natürlichen Aktivitäten und
{runtime['wild_rhythms']} mit Tagesrhythmus; {runtime['creature_visuals']} CreatureVisual-
Actors in der gesamten Map einschließlich bestehender Testdarstellung, nicht alle
in derselben Kamera. Die Benchmark-Testparty hat kein modelliertes Begleiterexemplar
({runtime['companions']} Companion-Tags); der echte Begleiter wurde mit bestehender
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

{baseline}

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

{table(['Modell','LOD0-Dreiecke','LODs','Materialslots'],modelrows)}

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

{paired('NativeMatrix05','Control')}

Zusätzliche Streuung und der verfügbare Render-Thread-Wandzeitzähler:

{table(['Ort','Original FPS-Spanne','Optimiert FPS-Spanne','Frame p95 ms vorher → nachher','RT-Wandzeit ms vorher → nachher'],[[n,f"{min(x['fps']for x in subset('NativeMatrix05',n,'Control')):.2f}–{max(x['fps']for x in subset('NativeMatrix05',n,'Control')):.2f}",f"{min(x['fps']for x in subset('NativeMatrix05',n,'BakedSRGB')):.2f}–{max(x['fps']for x in subset('NativeMatrix05',n,'BakedSRGB')):.2f}",f"{st.mean(x['frame_ms']['p95']for x in subset('NativeMatrix05',n,'Control')):.2f} → {st.mean(x['frame_ms']['p95']for x in subset('NativeMatrix05',n,'BakedSRGB')):.2f}",f(subset('NativeMatrix05',n,'Control'),'RenderThreadTime')+' → '+f(subset('NativeMatrix05',n,'BakedSRGB'),'RenderThreadTime')]for n in sites])}

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

{paired('PairedPIE02','OriginalGround')}

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

{days}

Kein herausragender zusätzlicher Nachtkostentreiber in dieser Ortsstichprobe.
Alle übrigen Licht-, Sonnen-, Weltuhr- und Tagesrhythmusregeln sind unverändert.

## 12. Getrennte Qualitäts-/Auflösungsalternativen

NativeAlternatives06, jeweils drei Läufe, derselbe zusätzliche Wald-Messpunkt
(−2960, 1700, 50,15 cm), jeweils Farbbake und 12:00. Dieser Punkt ist nicht der
Waldpunkt der Sechs-Orte-Matrix (−4300, 1550). Interleavte Umkehrreihenfolge.
QHD-Ausgabe bleibt, intern 75 % entspricht **1920×1080**, kein unverändertes QHD.

{alt}

Nur Medium/75 % liegt hier in allen drei **Segmentmitteln** über 30 FPS. Das
ist keine stabile 30-FPS-Freigabe für alle Orte, Tageszeiten und längere Sitzungen.
High/75 % bleibt im Mittel unter 30. Keine dieser Alternativen ist als Standard
übernommen. Eine solche Qualitätsentscheidung benötigt einen gesonderten,
vollständigen Bild-/Gameplayvergleich. 60 FPS werden auch hier nicht erreicht.

## 13. Echte Bildvergleiche und Qualitätsgrenzen

22 echte QHD-PNGs in elf Paaren. Identische Kamera, Spielerposition, Uhrzeit,
Grafikbedingungen und eingefrorene Weltzeit je Paar maschinell geprüft. Keine
KI-generierten oder künstlich nachgebauten Bilder. Normale Spielkamera.

{table(['Szene/Zeit','Vorher','Nachher'],shots)}

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

{rhythm['elapsed']:.2f} s, {len(rhythm['samples'])} reale Stichproben bei acht
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
Alle bestanden; reguläre Stopps {min(x['stop_seconds']for x in stops):.3f} bis
{max(x['stop_seconds']for x in stops):.3f} s. Dazu die separaten längeren Benchmark-
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

Alle {protection['original_saves']} ursprünglichen `.sav`-Dateien, sämtliche
ursprünglichen Art-/Content-Quellen außer der erlaubten Map und alle
{protection['original_untracked']} geschützten unversionierten Dateien hashgleich.
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

Der konkrete abschließende Commit, tatsächlicher Remote-Stand und LFS-Nachweis
werden nach Erstellung und regulärem Push im Abschlusschat sowie lokal in
[GitFinal.json](../Saved/ProjectRefinement/VisualV2PerformanceV1/GitFinal.json)
angegeben. Kein Force-Push und keine Änderung des bestätigten 0-USD-LFS-Budgets.
Bei Kontingent-/Abrechnungsfehlern wird abgebrochen und kein synchroner Remote
behauptet. Die technische Abnahme ist eine erfolgreiche, begrenzte Optimierungs-
und Analysephase; das Leistungsziel 30 FPS ist ausdrücklich nicht erreicht.
'''
(R/'Docs/VISUALV2_PERFORMANCEOPTIMIERUNG_V1.md').write_text(report)
print('Report written:',len(report),'characters; 11 QHD pairs verified')
