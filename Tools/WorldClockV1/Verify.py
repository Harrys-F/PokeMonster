"""Read-only final evidence/protection audit. Writes only this task's Saved result."""
from pathlib import Path
import json,hashlib,subprocess,re,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/WorldClockV1';b=json.loads((D/'Baseline.json').read_text())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).strip()
changed=[x for x,h in b['hashes'].items()if not(R/x).is_file()or hashlib.sha256((R/x).read_bytes()).hexdigest()!=h];assert not changed,changed
for ref in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']:assert git('rev-parse',ref)==b['refs'][ref]
assert not(R/'Saved/SaveGames/PokeMonster_Recovery.sav').exists()
u=set(git('ls-files','--others','--exclude-standard').splitlines());assert set(b['untracked'])<=u
qa=json.loads((R/'Saved/ProjectRefinement/WorldClockV1Automation02/Report/index.json').read_text(encoding='utf-8-sig'));assert qa['succeeded']==267 and all(qa[k]==0 for k in ['succeededWithWarnings','failed','notRun','inProcess'])
wrapper=json.loads((R/'Saved/ProjectRefinement/WorldClockV1Automation02/Result.json').read_text());assert wrapper['exit']==0
for n in ['PIE01','PIE02','PIE03','PIE04','Restart01','Defeat01','Debug01','Travel02','Travel06']:
 assert json.loads((D/n/'Result.json').read_text())['passed'],n
checks=[];log=(D/'Editor04.log').read_text(errors='replace')
for part in log.split('WORLD_CLOCK_FINAL_MAPCHECK_BEGIN ')[1:]:
 name=part.splitlines()[0].strip();body=part.split('WORLD_CLOCK_FINAL_MAPCHECK_END ')[0];lines=[x for x in body.splitlines()if'Kartenprüfung abgeschlossen'in x];assert len(lines)==1 and'0 Fehler, 0 Warnung(en)'in lines[0],(name,lines);checks.append({'map':name,'result':lines[0]})
assert len(checks)==12
critical=[x for x in log.splitlines()if re.search(r'Fatal error:|Assertion failed:|Ensure condition failed:|Unhandled Exception|Blueprint Runtime Error|LogLinker: Error:|=== Critical error:',x)];assert not critical,critical
images=[]
for n in ['Start0900','Later1642','InteriorLoaded','DawnBoundary','DayRollover','NightLoaded']:
 p=R/'Saved/GlumandaV11/LiveUI'/('WorldClockPIE04'+n)/'LivePIEViewportQHD.png';assert struct.unpack('>II',p.read_bytes()[16:24])==(2560,1440);assert p.with_name('ActualSlateViewport.png').is_file();images.append(str(p.relative_to(R)))
assert json.loads((D/'ScenePreserved.json').read_text())['identical']
r={'protected_files_unchanged':len(b['hashes']),'original_untracked_preserved':len(b['untracked']),'map_checks':checks,'automation':wrapper,'qhd_images':images,'critical_errors_final_editor':critical,'prior_failed_runs_preserved':['WorldClockV1Build01 (missing include)','WorldClockV1Automation01 (bad phase config/test bounds)','Editor01/02/03 Travel01/03/04 (GC crash after retained completed Python test contexts); corrected PIE04 + Travel06 passed'],'head':git('rev-parse','HEAD')}
(D/'FinalVerification.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items()if k not in ['map_checks','qhd_images','prior_failed_runs_preserved']},indent=2))
