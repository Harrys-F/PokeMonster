# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
from pathlib import Path
import json,statistics,collections,subprocess
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';D=R/'Art/World/EnvironmentPerfV3/Review';P=R/'Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V3_PRUEFBERICHT.md';assert not P.exists()
def load(n):return json.loads((O/n).read_text(encoding='utf-8-sig'))
v=load('MatrixValidation.json');assert len(v)==12 and all(x['all_segment_csv_present'] for x in v.values())
f=load('FootTest/FootTest.json');assert f['passed'];a=load('Automation/index.json');assert a['failed']==a['notRun']==0
s=load('ProtectedFinal.json');assert s['all_initial_versionable_files_byte_identical'];mc=load('MapCheck.json');assert mc['errors']==mc['warnings']==0
thermal=[json.loads(l) for l in (O/'Thermal.jsonl').read_text().splitlines()];tc=dict(collections.Counter(x['thermal_label'] for x in thermal));power=list(dict.fromkeys(x['power'] for x in thermal))
body=f'''# Environment Performance V3 – Prüfbericht

Stand 15.10.2026. **Keine neue Vegetationsoptimierung zur Übernahme in VisualV2 empfohlen.**

## Ergebnis

Die separate Karte `/Game/Maps/Dev_TestMap_EnvironmentPerfV3` ist gespeichert und geprüft. Ein deutlicher, reproduzierbarer neuer QHD-Gewinn gegenüber V2 wurde nicht erreicht. Daher wurden erzwungene Baum-LODs, zusätzliche Culling-Grenzen und vereinfachte Blattmaterialien **nicht dauerhaft übernommen**. V3 erhält den erneut geprüften V2-Renderzustand. Die Messmatrix zeigt diesen Zustand **A** gegen den anschließend verworfenen Mindest-LOD-Versuch **B**; B ist nicht die ausgelieferte V3-Konfiguration.

Die Irradiance-Field-Alternative bleibt schneller als Screen Probe Gather, aber ihre indirekte Helligkeit und Kontaktschatten entsprechen weiterhin nicht vollständig V1. Die getesteten Korrekturen lösen das nicht überzeugend. Empfehlung: V2 vorerst als bisherigen Performance-Versuch behalten, V3 als nachvollziehbare Untersuchungs-/Reviewgrundlage. Keine automatische Übernahme in VisualV2. Kein Commit, kein Push.

## Sicherheit und Editorzustand

HEAD: `{(O/'InitialHEAD.txt').read_text().strip()}`; Branch `{subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()}`. Der Arbeitsbaum war bereits umfangreich geändert/unversioniert. {s['checked_initial_versionable_files']} vorhandene, von Git erfasste oder nicht ignorierte Projektdateien vor/nachher SHA-256-geprüft: alle bytegleich. Build-, Saved- und DDC-Artefakte sind davon getrennt. Keine Resets, Löschungen, Restores, Staging oder fremden Änderungen.

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
'''
for path,x in load('VegetationLightingAudit.json')['meshes'].items():
 body+='| '+path.split('.')[-1]+' | '+str(sum(c['instances'] for c in x['components']))+' | '+str(len(x['components']))+' | '+' / '.join(str(l['triangles']) for l in x['lods'])+' |\n'
body+='''
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
'''
body+=f'\nThermik: {len(thermal)} Abfragen; Zustände {tc}. Energiezustände: {power}. NSProcessInfo ist keine Grad-/Taktmessung; konkretes Throttling wird daraus nicht behauptet. Zeitnahe A/B-Paare reduzieren Drift, schließen Hintergrundlast/Temperaturdrift nicht vollständig aus.\n'
body+='\n## Vollständiger Vorher-/Nachher-Versuch\n\nA = V2-Renderzustand auf identischer V3-Kopie, entspricht dem gespeicherten V3-Zustand. B = ausschließlich Baum-Mindest-LOD 1, **verworfen**. Keine neue FPS-Verbesserung des ausgelieferten Zustands behauptet.\n\n'+(O/'MetricTables.md').read_text()
body+='\n### GPU-Stufen am QHD-High-100-Waldpunkt\n\nMediane der drei Wiederholungen; verschachtelte Stufen nicht aufsummieren. RenderThread im Standalone enthält Wartezeit.\n\n| Modus | Stufe | A ms | B ms (verworfen) |\n|---|---|---:|---:|\n'
for mode,label in [('Standalone','NativeMatrix6'),('PIE','PIEMatrix6')]:
 row=next(x for x in load('PairedMetrics.json') if x['label']==label and x['site']=='Wald');aa,bb=row['state'].values()
 for stage in ['GPU/Unaccounted','GPU/ShadowProjection','GPU/LumenIrradianceFieldGather','GPU/Basepass','GPU/ShadowDepths','GPU/LumenSceneLighting','GPU/Postprocessing','GPU/PostProcessing','GPU/SlateUI']:
  av=aa['gpu_stages_ms'].get(stage);bv=bb['gpu_stages_ms'].get(stage)
  if av is not None and bv is not None:body+=f'| {mode} | {stage} | {av:.3f} | {bv:.3f} |\n'
body+='\n## Isolierte Faktoren\n\nDiscovery: Wald, PIE QHD High 100 %, sieben Sekunden Warm-up/sieben Sekunden Messung. Negative Δms ist schneller.\n\n| Faktor | Drei Δms B−A | Median Δms |\n|---|---|---:|\n'
for name,rows in load('DiscoveryPairs.json').items():
 ds=[r['delta_ms'] for r in rows];body+='| '+name+' | '+', '.join(f'{x:+.3f}' for x in ds)+' | '+f'{statistics.median(ds):+.3f}'+' |\n'
rs=load('Measurements.json')['NativeCulling'];groups={}
for i in range(0,len(rs),2):
 x,y=rs[i:i+2];c=x if x['condition']=='Control' else y;b=y if x['condition']=='Control' else x;groups.setdefault(b['site']+' / '+b['condition'],[]).append(b['median_ms']-c['median_ms'])
body+='\nNative Nachprüfung QHD High 100 %, fünf Sekunden Warm-up/sechs Sekunden Messung:\n\n'
for k,ds in groups.items():body+='- '+k+': '+', '.join(f'{x:+.3f}' for x in ds)+' ms; Median '+f'{statistics.median(ds):+.3f}'+' ms.\n'
body+='''
**Belegt:** Screen Probe Gather statt V2-Irradiance Field kostet hier rund 4,5–4,6 ms zusätzlich, Hardware-RT-Schalter dabei identisch. GPU-/Präsentationszeit erheblich größer als Game Thread. Schattenprojektion, indirekte Beleuchtung und Base Pass sind messbare Stufen. Der große Unaccounted-Anteil bleibt ungeklärt; keine Behauptung, alles sei Vegetation.

**Nicht belegt:** Robuste Gesamteinsparung durch Vegetation verstecken, Schatten abschalten, Busch-/Farn-LODs oder zusätzliche Culling-Grenzen. Verstecken verändert auch GI/Occlusion und sichtbare Bodenflächen; keine reine Vegetationszeit. Baum-LOD 1 zeigt kleine lokale Vorteile, aber keinen konsistenten Gewinn, insbesondere nicht im nativen QHD High 100. Deshalb kein dauerhafter Qualitätswechsel. Keine großflächige Vegetationsentfernung akzeptiert.

## Beleuchtung und Sichtprüfung

Adaptive Probe-Platzierung, OcclusionBias 0,5, AO-Radius 48 und InterpolateDownsampleFactor 4 einzeln geprüft und in echten QHD-Bildern verglichen. Keine überzeugende Wiederherstellung der V1-Kontaktschatten ohne Nachteile. Größerer AO-Radius kostet Zeit; gröbere Interpolation kein zuverlässiger Gewinn. Keine Übernahme, globale Abdunklung oder zusätzliche Lichter als Kompensation.

Kronen, Boden/Wege, NPC-Lesbarkeit, Gebäude/Heilhaus und Player-Reveal betrachtet. V3 wahrt V2-Materialien, Licht und Geometrie. Abweichende indirekte Schattierung zu V1 bleibt ein bekannter V2-Kompromiss. Mindest-LOD kann feine Stamm-/Ast-/Blattkonturen vereinfachen; ohne überzeugenden Gewinn verworfen. Gespeicherte V3 hat keine neuen LOD-Schwellen/Culling-Übergänge. Keine pauschale Freigabe vorhandener Masked-/LOD-Kanten als flimmerfrei.

## Echte Bildvergleiche

Actual saved Source-Maps VisualV2, EnvironmentPerfV1, V2 und V3 separat ohne Source-Map-Save aufgenommen, High/QHD100 und gleiche Spielkamera. Keine generierten Konzeptbilder. Beschriftete Layouts sind ausschließlich Zusammenstellungen echter Aufnahmen. Review-Metadaten halten Map, Bedingung, Position, Kamera und Viewport fest. Originalbilder 2560×1440 im Reviewordner, weitere Versuchsbilder unter Saved.

'''
for x in json.loads((D/'Screenshots.json').read_text()):body+=f"- [{Path(x['review']).name}](../{x['review']}) — Quelle `{x['source']}`.\n"
body+=f'''
## Funktion, Build und Tests

- Development Editor Build erfolgreich, `Build_Initial.log` und `Build_MinLOD.log`. Nur neue isolierte Entwicklungs-/Profilingdateien und ein Isolationstest; bestehende C++-/Gameplay-Dateien unverändert.
- Projekt-Automation **{a['succeeded']}/{a['succeeded']+a['failed']+a['notRun']} erfolgreich**, {a['failed']} fehlgeschlagen, {a['notRun']} nicht ausgeführt. Aktuell 46 einschließlich neuem V3-Test. Bekannte generische Engine-Startup-„Condition failed“-Meldungen vor der Testsitzung sowie `idevice_id`-macOS-Warnungen getrennt davon; kein komplett warnungsfreier Engine-Startup behauptet. Testdetails im Automation-JSON.
- Finaler Map Check: **{mc['errors']} Fehler / {mc['warnings']} Warnungen**; Lognachweis in MapCheck.json.
- Eingebetteter PIE-Fußlauf **{f['distance_m']:.2f} m**, ohne Test-Teleports, bestanden. EnhancedInput-Bewegung, bestehende Interaktions-/Battle-Presenter-APIs für Aktionen; kein behaupteter manueller Hardware-/Maus-UI-Test.
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

## Dateien und Git

Neu: V3-Karte, vier V3-C++-/Testdateien, Tools/EnvironmentPerfV3, Art/World/EnvironmentPerfV3/Review und dieser Bericht. Art-Dateien sind Mess-/Bildbelege, keine neuen Original-Blender-/Vegetationsassets. README erläutert Befehle, Guards und die konservative Endkonfiguration.

Keine bestehende versionierbare Datei inhaltlich verändert; fremde offene Arbeiten bleiben offen. Abschließender `git diff --check`-Nachweis in GitDiffCheck.json und Abschlussmeldung. Kein Commit, kein Push.
'''
P.write_text(body)
initial=load('InitialHashes.json');names=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines();owned=[]
for n in names:
 if n in initial:continue
 if n.startswith(('Tools/EnvironmentPerfV3/','Art/World/EnvironmentPerfV3/')) or n in ['Content/Maps/Dev_TestMap_EnvironmentPerfV3.umap','Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V3_PRUEFBERICHT.md'] or (n.startswith('Source/PokeMonster/') and 'V3' in Path(n).name):owned.append(n)
owned=sorted(set(owned+['Art/World/EnvironmentPerfV3/Review/NewFiles.json']));(D/'NewFiles.json').write_text(json.dumps(owned,indent=2));body+='\n### Neue Dateien dieses Auftrags\n\n'+''.join('- `'+n+'`\n' for n in owned)
status=subprocess.check_output(['git','status','--short'],cwd=R,text=True);(O/'FinalGitStatus.txt').write_text(status);body+='\n### git status --short\n\n```text\n'+status+'```\n';P.write_text(body);print(P)
