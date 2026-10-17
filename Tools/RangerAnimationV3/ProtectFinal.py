# V5: current required-core guard; historical session algorithm is preserved below.
import os as _evidence_os, sys as _evidence_sys
from pathlib import Path as _EvidencePath
if _evidence_os.environ.get('POKEMONSTER_RUN_HISTORICAL_GUARD') != '1':
    _evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
    _evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
    from evidence import current_guard as _current_guard
    _current_guard()
"""Protect every pre-existing file, including untracked V2 work. No staging."""
import hashlib,json,subprocess,re
from pathlib import Path
R=Path(__file__).resolve().parents[2];S=R/'Saved/RangerAnimationV3';D=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3/Data'
assert (S/'PerformanceComplete.txt').exists()
old=json.loads((S/'ProtectedBefore.json').read_text());changed=[];missing=[]
for p,h in old.items():
 f=R/p
 if not f.is_file():missing.append(p)
 elif hashlib.sha256(f.read_bytes()).hexdigest()!=h:changed.append(p)
raw=subprocess.check_output(['git','ls-files','-co','--exclude-standard','-z'],cwd=R).decode().split('\0')
files=sorted(set(p for p in raw if p and (R/p).is_file()));new=[p for p in files if p not in old]
allowed=['Tools/RangerAnimationV3/','Art/Characters/NPCs/Ranger/Review/AnimationV3/','Art/Characters/NPCs/Ranger/Exports/AnimationV3/','Content/Characters/NPCs/RangerMotionV3/']
exact=['Art/Characters/NPCs/Ranger/Source/Ranger_NPC_AnimationQuality_V3.blend','Content/Maps/Dev_TestMap_NPCMotionV3.umap','Docs/MESHY_RANGER_ANIMATION_QUALITY_V3_PRUEFBERICHT.md']
foreign=[p for p in new if not any(p.startswith(x) for x in allowed) and p not in exact and 'PokeMonsterNPCMotionV3' not in p]
save=R/'Saved/SaveGames/PokeMonster_Dev.sav';expected=json.loads((S/'DevSaveBefore.json').read_text())['sha256'];actual=hashlib.sha256(save.read_bytes()).hexdigest()
assert actual==expected,'Dev save changed outside the guarded test'
git=subprocess.run(['git','diff','--check'],cwd=R,text=True,capture_output=True)
(S/'GitDiffCheck.txt').write_text(git.stdout+git.stderr);assert git.returncode==0,git.stdout+git.stderr
checks=[];suffixes={'.py','.cpp','.h','.md','.swift','.tsv','.json'}
for p in new:
 if (R/p).suffix not in suffixes:continue
 result=subprocess.run(['git','diff','--no-index','--check','/dev/null',p],cwd=R,text=True,capture_output=True)
 assert result.returncode in [0,1] and not result.stdout and not result.stderr,(p,result.stdout,result.stderr)
 checks.append(p)
status=subprocess.check_output(['git','status','--short'],cwd=R,text=True);(S/'GitFinal.txt').write_text(status)
(D/'GitChecks.json').write_text(json.dumps({'tracked_diff_check':'erfolgreich, keine Ausgabe','new_text_files_checked':checks,'method':'git diff --no-index --check /dev/null <specific new text file>','review_csv':'Raw acquisition CSVs preserved; no blanket staging recommendation.'},indent=2))
out={'protected_count':len(old),'modified_existing':changed,'missing_existing':missing,'new_files':new,'foreign_new_files_not_touched':foreign,'dev_save_sha256':actual,'no_commit_push_staging':True}
(D/'ScopeAndFiles.json').write_text(json.dumps(out,indent=2))
assert not changed and not missing,(changed,missing)
print('PROTECTED',len(old),'existing files; new',len(new),'foreign new',foreign)
