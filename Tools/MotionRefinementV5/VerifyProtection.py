"""Read-only original/protected-file/save/ref validation against this task's local starting inventory."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/MotionRefinementV5';initial=json.loads((D/'InitialState.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();allowed={'Content/Data/Creatures/DA_Glurak.uasset','Content/Data/Creatures/DA_Nebulak.uasset'};changed=[]
for p,h in initial['originals'].items():
 assert(R/p).is_file(),p
 if sha(R/p)!=h:changed.append(p)
assert set(changed)==allowed,changed
for p,h in initial['untracked'].items():assert(R/p).is_file()and sha(R/p)==h,p
save=sha(R/'Saved/SaveGames/PokeMonster_Dev.sav');assert save==initial['save_sha256'];refs={x:subprocess.check_output(['git','rev-parse',x],cwd=R,text=True).strip()for x in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']};assert all(x=='03492bd96b4dba44692f675c19d5f11abfa86b4b'for x in refs.values());assert subprocess.run(['git','merge-base','--is-ancestor',next(iter(refs.values())),'HEAD'],cwd=R).returncode==1
for name,base,auditname in [('Glurak','Art/Characters/Creatures/Glurak','MotionV5_Audit.json'),('Nebulak','Art/Characters/Creatures/Nebulak','MotionV5_Audit.json'),('Player','Art/Characters/YoungTrainer','MotionQualityV3_Audit.json')]:
 a=json.loads((R/base/auditname).read_text());assert sha(R/a['source'])==a['source_sha256']
 for e in a['exports']:assert sha(R/e['path'])==e['sha256']
result=dict(passed=True,protected_untracked_count=len(initial['untracked']),unchanged_original_files=len(initial['originals'])-len(changed),only_changed_originals=changed,save_sha256=save,backup_refs=refs,no_backup_ancestor_of_main=True);(D/'Protection.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
