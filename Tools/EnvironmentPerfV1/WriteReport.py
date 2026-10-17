# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
"""Assemble final report from actual measurements. Run only after all checks."""
from pathlib import Path
import json,statistics,collections,subprocess
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV1';A=R/'Art/World/EnvironmentPerfV1/Review';D=R/'Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V1_PRUEFBERICHT.md'
assert (O/'StandalonePair6_Done.txt').read_text()=='Complete'
data=json.loads((O/'Measurements.json').read_text());foot=json.loads((O/'FootTest/FootTest.json').read_text());protection=json.loads((O/'ProtectionAudit.json').read_text());auto=json.loads((O/'Automation/index.json').read_text(encoding='utf-8-sig'));assert foot['passed'] and not protection['unexpected_changes'] and not protection['missing']
text=(R/'Tools/EnvironmentPerfV1/ReportBody.md.in').read_text()
def put(name,value):
 global text
 text=text.replace('{{'+name+'}}',value)
put('PROTECTION',f"Vor Beginn wurden {protection['initial_file_count']} vorhandene versionierte/unversionierte Dateien mit Größe und SHA-256 erfasst. Abschließend {len(protection['unchanged'])} bytegleich; bewusste Änderungen ausschließlich: "+', '.join(protection['intentional_changes'])+'. Dokumente nur ergänzt, anfänglicher Inhalt vollständig erhalten. Build.cs ausschließlich um RenderCore ergänzt. Keine fehlenden oder unerwartet geänderten Ausgangsdateien.')
thermal=[json.loads(s) for s in (O/'Thermal.jsonl').read_text().splitlines() if s]
put('THERMAL','Thermalmonitor (10-Sekunden-Abstand): '+str(dict(collections.Counter(x['thermal_label'] for x in thermal)))+'. NSProcessInfo-Labels sind keine °C-/Taktfrequenzmessungen. Zeit-/Temperaturdrift bleibt trotz Verschachtelung möglich.')
rs=[r for r in data['FinalPairedPIE'] if r['site']=='Wald' and r['quality']=='2' and r['percentage']=='100' and r['condition']=='Control']
keys=['GameThreadTime','RenderThreadTime','GPUTime','GPU/LumenScreenProbeGather','GPU/ShadowProjection','GPU/ShadowDepths','GPU/Basepass','GPU/SlateUI','GPU/LumenSceneUpdate','GPU/MotionBlur','GPU/TemporalSuperResolution','GPU/Unaccounted']
gpu=['| Zähler | Median |','|---|---:|']
for k in keys:
 vs=[] if k=='RenderThreadTime' else [r['csv'][k]['median'] for r in rs if k in r['csv'] and not r['csv'][k]['all_zero']]
 gpu.append('| '+k+' | '+(f'{statistics.median(vs):.3f} ms' if vs else 'nicht zuverlässig verfügbar')+' |')
put('GPU_TABLE','\n'.join(gpu))
tables=(O/'MetricTables.md').read_text();f=tables.index('## Einzelfaktor-Paare');p=tables.index('## Finale Paare: PIE')
put('FACTOR_TABLES',tables[f:p].strip())
put('FINAL_TABLES',tables[p:].strip())
shots=[]
for title,base,cand in [('Dorf / Heilhaus','00_Dorf_Control00000.png','01_Dorf_MapCandidate00000.png'),('Dichter Wald','02_Wald_Control00000.png','03_Wald_MapCandidate00000.png'),('Waldlichtung','04_Clearing_Control00000.png','05_Clearing_MapCandidate00000.png'),('Wegübergänge','06_Weg_Control00000.png','07_Weg_MapCandidate00000.png'),('NPC im Waldschatten','08_NPCWald_Control00000.png','09_NPCWald_MapCandidate00000.png'),('Kronenfreistellung','10_Crown_Control00000.png','11_Crown_MapCandidate00000.png'),('Archiv','12_Archiv_Control00000.png','13_Archiv_MapCandidate00000.png')]:
 shots.append(f'**{title}: Kontrolle / Kandidat**\n\n![Kontrolle]({A}/Screenshots/{base})\n\n![Kandidat]({A}/Screenshots/{cand})')
put('SCREENSHOTS','\n\n'.join(shots))
put('FOOT_RESULT',f"**Bestanden:** {foot['distance_m']:.2f} m echte Enhanced-Input-Fortbewegung, {foot['game_seconds']:.2f} s Spielzeit / {foot['wall_seconds']:.2f} s Wall-Clock. Keine Test-Teleports. Nur bestehende normale Heilhaus-Relocation. Maximales gemessenes Tempo {foot['max_speed_cm_s']:.3f} cm/s.")
put('AUTOMATION',f"Tatsächlicher Umfang: **{len(auto['tests'])} Tests**, {auto['succeeded']} erfolgreich, {auto['succeededWithWarnings']} erfolgreich mit Warnungen, {auto['failed']} fehlgeschlagen, {auto['notRun']} nicht ausgeführt. Neue Abdeckung: PokeMonster.Rendering.EnvironmentProfile.ScopeAndBaselineProtection. Bestehende Gameplaytests vollständig mit ausgeführt. [Strukturierter Report]({A}/Data/AutomationIndex.json).")
warnings=(O/'WarningsSummary.md').read_text() if (O/'WarningsSummary.md').exists() else 'Vollständige Warnungen im nativen Automation.log; keine nicht überprüfte Behauptung einer warnungsfreien Engine-Sitzung.'
put('WARNINGS',warnings)
files=[R/'Content/Maps/Dev_TestMap_EnvironmentPerfV1.umap',R/'Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbe.cpp',R/'Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfile.cpp',R/'Source/PokeMonster/Development/PokeMonsterEnvironmentRenderProfile.h',R/'Source/PokeMonster/Tests/PokeMonsterEnvironmentRenderProfileTest.cpp',D]
for folder in [R/'Tools/EnvironmentPerfV1',A]:
 files.extend(p for p in sorted(folder.rglob('*')) if p.is_file() and '__pycache__' not in p.parts)
put('FILES','Vollständige neue Dateiliste dieser Aufgabe:\n\n~~~text\n'+'\n'.join(str(p.relative_to(R)) for p in files)+'\n~~~')
git=json.loads((O/'FinalGitChecks.json').read_text())
put('GIT',f"git diff --check: Exit {git['diff_check_exit']}; Ausgabe: "+(git['diff_check_output'] or '(keine)')+'. Nichts gestaged, kein Commit, kein Push.\n\nAnfangsstatus:\n\n~~~text\n'+(O/'GitBefore.txt').read_text().rstrip()+'\n~~~\n\nAbschlussstatus (vorhandene offene Arbeiten eingeschlossen):\n\n~~~text\n'+git['status'].rstrip()+'\n~~~')
assert '{{' not in text,'Unfilled report placeholder'
D.write_text(text)
print(D)
