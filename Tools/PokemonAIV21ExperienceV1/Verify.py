"""Read-only project protection, native QA and exact map-check evidence audit.
Writes only task-owned Saved evidence; never repairs or deletes protected data.
"""
from pathlib import Path
import json,hashlib,subprocess,re,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/PokemonAIV21ExperienceV1';b=json.loads((D/'Baseline.json').read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True).strip()
changed=[f for f,h in b['files'].items()if not(R/f).is_file()or hashlib.sha256((R/f).read_bytes()).hexdigest()!=h]
assert not changed,changed
assert all(git('rev-parse',r)==h for r,h in b['refs'].items())
assert not(R/'Saved/SaveGames/PokeMonster_Recovery.sav').exists()
u=set(git('ls-files','--others','--exclude-standard').splitlines());assert set(b['untracked'])<=u
qa=json.loads((R/'Saved/ProjectRefinement/PokemonAIV21ExperienceAutomation02/Report/index.json').read_text(encoding='utf-8-sig'))
assert qa['failed']==qa['notRun']==qa['inProcess']==0 and qa['succeeded']+qa['succeededWithWarnings']==261
warnings=[]
for t in qa['tests']:
 for e in t.get('entries',[]):
  v=e['event']
  if v['type']=='Warning':
   assert 'idevice_id'in v['message']or'Failed to launch Tool'in v['message'],v
   warnings.append({'test':t['fullTestPath'],'warning':v['message']})
text=(D/'EditorFinal01.log').read_text(errors='replace');checks=[]
for part in text.split('AIV21_FINAL_MAPCHECK_BEGIN ')[1:]:
 name=part.splitlines()[0].strip();body=part.split('AIV21_FINAL_MAPCHECK_END ')[0]
 result=[x for x in body.splitlines()if'Kartenprüfung abgeschlossen'in x]
 assert len(result)==1 and '0 Fehler, 0 Warnung(en)'in result[0],(name,result)
 checks.append({'map':name,'result':result[0]})
assert len(checks)==12
for label in ['SpontaneousSocial01','SpontaneousSocial02','SpontaneousSocial03','StandardProfileClearing02','ExperiencePIE03','ConnectedPIEFinal01']:
 assert json.loads((D/label/'Result.json').read_text())['passed'],label
for label in ['AIV21TerritorialVictory','AIV21CuriousFlee','AIV21ShyCapture']:
 assert json.loads((R/'Saved/ProjectRefinement/GameplayPraxisV1/wild'/label/'Result.json').read_text())['passed'],label
for n in ['StatusBefore','BattleBefore','LevelUp','StatusAfter','AfterLoad','OtherPokemon','Maximum']:
 p=R/'Saved/GlumandaV11/LiveUI'/('AIV21ExperiencePIE03'+n)/'LivePIEViewportQHD.png'
 assert struct.unpack('>II',p.read_bytes()[16:24])==(2560,1440)
critical=[x for x in text.splitlines()if re.search(r'Fatal error:|Assertion failed:|Ensure condition failed:|Unhandled Exception|Blueprint Runtime Error|LogLinker: Error:',x)]
assert not critical,critical
r={'protected_files_unchanged':len(b['files']),'original_untracked_preserved':len(b['untracked']),'backup_refs_unchanged':b['refs'],'canonical_recovery_created':False,'automation':{k:qa[k]for k in ['succeeded','succeededWithWarnings','failed','notRun','inProcess']},'native_engine_exit':0,'strict_wrapper_exit':1,'external_warnings':warnings,'map_checks':checks,'qhd_images_verified':7,'critical_patterns':critical,'head':git('rev-parse','HEAD')}
(D/'FinalVerification.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items()if k not in ['map_checks','external_warnings','backup_refs_unchanged']},indent=2))
