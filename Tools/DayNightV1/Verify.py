"""Acceptance/protection audit: native results, no edits beyond owned evidence."""
from pathlib import Path
import hashlib,json,subprocess,re,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/DayNightV1';b=json.loads((D/'Baseline.json').read_text())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).strip()
changed=[p for p,h in b['hashes'].items()if not(R/p).is_file()or hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not changed,changed
for ref,h in b['refs'].items():assert git('rev-parse',ref)==h
assert not(R/'Saved/SaveGames/PokeMonster_Recovery.sav').exists()
u=set(git('ls-files','--others','--exclude-standard').splitlines());assert set(b['untracked'])<=u
assert json.loads((D/'ScenePreserved.json').read_text())['identical']
assert json.loads((R/'Saved/ProjectRefinement/DayNightV1Build09/Result.json').read_text())['exit']==0
qa=json.loads((R/'Saved/ProjectRefinement/DayNightV1Automation08/Report/index.json').read_text(encoding='utf-8-sig'));assert qa['succeeded']+qa['succeededWithWarnings']==272 and all(qa[k]==0 for k in ['failed','notRun','inProcess'])
warnings=[]
for t in qa['tests']:
 for e in t['entries']:
  if e['event']['type']=='Warning':
   msg=e['event']['message'];assert 'idevice_id'in msg or'Failed to launch Tool'in msg,msg;warnings.append({'test':t['fullTestPath'],'message':msg})
assert json.loads((D/'Before/Result.json').read_text())['passed']
for n in ['Gameplay01','Travel02','Sky05','PerformanceSeries02']:assert json.loads((D/n/'Result.json').read_text())['passed'],n
assert json.loads((D/'ComparisonValidation02.json').read_text())['passed']
log=(D/'EditorCycle06.log').read_text(errors='replace');checks=[]
for part in log.split('DAYNIGHT_MAPCHECK_BEGIN ')[1:]:
 name=part.splitlines()[0].strip();body=part.split('DAYNIGHT_MAPCHECK_END ')[0];lines=[x for x in body.splitlines()if'Kartenprüfung abgeschlossen'in x];assert len(lines)==1 and'0 Fehler, 0 Warnung(en)'in lines[0],(name,lines);checks.append({'map':name,'result':lines[0]})
assert len(checks)==12
critical=[x for x in log.splitlines()if re.search(r'Fatal error:|Assertion failed:|Ensure condition failed:|Unhandled Exception|Blueprint Runtime Error|not initialized properly|LogLinker: Error:|=== Critical error:',x)];assert not critical,critical
images=[]
for path in [*list((D/'Before').glob('*.png')),*list((D/'Comparison02').rglob('*.png')),*list((D/'Sky05').glob('*.png')),*list((D/'Gameplay01').glob('*.png'))]:
 assert struct.unpack('>II',path.read_bytes()[16:24])==(2560,1440);images.append(str(path.relative_to(R)))
perf=json.loads((D/'PerformanceSummary.json').read_text());assert len(perf['segments'])==48
r={'protected_files_unchanged':len(b['hashes']),'original_untracked_preserved':len(b['untracked']),'backup_refs_unchanged':True,'map_checks':checks,'automation':{k:qa[k]for k in ['succeeded','succeededWithWarnings','failed','notRun','inProcess']},'automation_warning_entries':warnings,'strict_wrapper_exit':1 if qa['succeededWithWarnings']else 0,'qhd_images':images,'critical_errors_final_editor':critical,'performance_segments':len(perf['segments']),'head_before_commit':git('rev-parse','HEAD')};(D/'FinalVerification.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items()if k not in ['map_checks','qhd_images']},indent=2))
