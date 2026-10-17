"""Run only after measurement/encoding are complete. No commit or staging."""
import json,subprocess,shutil,re,statistics,collections,hashlib
from pathlib import Path
from MCPClient import rpc
from Control import job
R=Path(__file__).resolve().parents[2];S=R/'Saved/RangerAnimationV3';D=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3/Data'
assert (S/'PerformanceComplete.txt').exists()
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'NPCMotionV3','version':'1'}})
job('FinalMapAudit.py');job('FinalEditorState.py')
for src,name in [(S/'FootTest/FootTest.json','GameplayFootTest.json'),(S/'DevSaveRestored.json','DevSaveRestored.json'),(S/'FinalEditorState.json','FinalEditorState.json'),(S/'FinalMapAudit.json','FinalMapAudit.json')]:shutil.copy2(src,D/name)
a=json.loads((S/'AutomationFinal/index.json').read_text(encoding='utf-8-sig'))
summary={k:a.get(k) for k in ['succeeded','succeededWithWarnings','failed','notRun','totalDuration']}
summary['tests']=[{'path':t['fullTestPath'],'state':t['state'],'entries':t.get('entries',[])} for t in a['tests']]
(D/'AutomationSummary.json').write_text(json.dumps(summary,indent=2))
thermal=[json.loads(x) for x in (S/'Thermal.jsonl').read_text().splitlines() if x]
summary={'samples':len(thermal),'states':dict(collections.Counter(x['thermal_label'] for x in thermal)),'all_on_AC':all("'AC Power'" in x['power'] for x in thermal),'range_utc':[thermal[0]['utc'],thermal[-1]['utc']],'not_measured':'No CPU clock, die temperature, power draw or hard thermal isolation.'}
(D/'ThermalSummary.json').write_text(json.dumps(summary,indent=2))
logs=[S/'EditorSession.log',S/'AutomationFinal.log']+sorted(S.glob('NativeMatrix*.log'))
warning_groups={};mapchecks=[]
for p in logs:
 text=p.read_text(errors='replace')
 groups=collections.Counter()
 for line in text.splitlines():
  if 'MapCheck:' in line:mapchecks.append({'file':str(p),'line':line})
  if 'Warning:' not in line and 'Error:' not in line:continue
  message=re.sub(r'^\[[^]]+\]\[[^]]+\]','',line)
  message=re.sub(r'0x[0-9a-fA-F]+','0xPTR',message)
  if any(n in message for n in ['MachineId','LoginId','UserId','ClientId']):message='<private process metadata omitted; raw local log retained>'
  groups[message]+=1
 warning_groups[p.name]=[{'message':m,'count':n} for m,n in groups.items()]
(D/'Warnings.json').write_text(json.dumps({'raw_logs':[str(p) for p in logs],'groups':warning_groups,'map_check_lines':mapchecks,'project_test_warnings':a['succeededWithWarnings'],'note':'Generic Engine bootstrap Condition failed output precedes PokeMonster tests; raw errors are retained, not suppressed. idevice_id is a known incompatible engine helper, not a project test pass.'},indent=2))
assert mapchecks and all('0 Fehler, 0 Warnung(en)' in x['line'] for x in mapchecks if 'abgeschlossen:' in x['line'])
for name in ['BuildCertified.log','NativeLODAudit.txt']:shutil.copy2(S/name,D/name)
def run(n):subprocess.run(['/usr/bin/python3',str(R/'Tools/RangerAnimationV3'/n)],cwd=R,check=True)
run('ProtectFinal.py');run('WriteReport.py');run('ProtectFinal.py')
p=R/'Docs/MESHY_RANGER_ANIMATION_QUALITY_V3_PRUEFBERICHT.md';text=p.read_text();head,tail=text.rsplit('```text\n',1);assert tail.rstrip().endswith('```');p.write_text(head+'```text\n'+(S/'GitFinal.txt').read_text().rstrip()+'\n```\n')
subprocess.run(['git','diff','--check'],cwd=R,check=True)
check=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],cwd=R,text=True,capture_output=True);assert check.returncode in [0,1] and not check.stdout and not check.stderr
(S/'Finalized.txt').write_text('Complete');print('FINALIZED',p)
