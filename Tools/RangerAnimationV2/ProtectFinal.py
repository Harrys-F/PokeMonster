# V5: current required-core guard; historical session algorithm is preserved below.
import os as _evidence_os, sys as _evidence_sys
from pathlib import Path as _EvidencePath
if _evidence_os.environ.get('POKEMONSTER_RUN_HISTORICAL_GUARD') != '1':
    _evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
    _evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
    from evidence import current_guard as _current_guard
    _current_guard()
"""Read-only original-file verification. Never restore/reset a changed file."""
from pathlib import Path
import json,hashlib,subprocess,difflib
R=Path(__file__).resolve().parents[2];S=R/'Saved/RangerAnimationV2';O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data';before=json.loads((S/'ProtectedBefore.json').read_text());changed=[];missing=[]
for name,old in before.items():
 p=R/name
 if not p.exists():missing.append(name)
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=old:changed.append(name)
allowed={'Source/PokeMonster/Characters/'+x for x in ['PokeMonsterNPCAnimInstance.h','PokeMonsterNPCAnimInstance.cpp','PokeMonsterNPCVisualActor.h','PokeMonsterNPCVisualActor.cpp']}
assert not missing,missing;assert set(changed)<=allowed,changed
patch=''
for path in sorted(changed):patch+=''.join(difflib.unified_diff((S/Path(path).name).read_text().splitlines(True),(R/path).read_text().splitlines(True),fromfile='before/'+path,tofile='after/'+path))
(O/'NPCPresentationChanges.patch').write_text(patch)
p=R/'Saved/SaveGames/PokeMonster_Dev.sav';save_before=hashlib.sha256((S/'PokeMonster_Dev_before.sav').read_bytes()).hexdigest();save_after=hashlib.sha256(p.read_bytes()).hexdigest();assert save_before==save_after
scope=O/'ScopeAndFiles.json';scope.write_text('{}')
files=sorted(set(x for x in subprocess.check_output(['git','ls-files','-co','--exclude-standard','-z'],cwd=R).decode().split('\0') if x and (R/x).is_file()));new=[x for x in files if x not in before]
def ours(x):return x.startswith(('Art/Characters/NPCs/Ranger/Review/AnimationV2/','Art/Characters/NPCs/Ranger/Exports/AnimationV2/','Tools/RangerAnimationV2/','Content/Characters/NPCs/RangerMotionV2/','Source/PokeMonster/Development/PokeMonsterNPCMotion')) or x in ['Art/Characters/NPCs/Ranger/Source/Ranger_NPC_AnimationQuality_V2.blend','Content/Maps/Dev_TestMap_NPCMotionV2.umap','Docs/MESHY_RANGER_ANIMATION_QUALITY_V2_PRUEFBERICHT.md','Source/PokeMonster/Tests/PokeMonsterNPCMotionV2Test.cpp']
a={'protected_initial_files':len(before),'unchanged_initial_files':len(before)-len(changed),'intentionally_extended_existing_files':changed,'missing_initial_files':missing,'unexpected_initial_changes':sorted(set(changed)-allowed),'new_task_files':[x for x in new if ours(x)],'other_new_files_not_claimed':[x for x in new if not ours(x)],'dev_save_sha256_before':save_before,'dev_save_sha256_after':save_after,'git_head':subprocess.check_output(['git','log','-1','--oneline'],cwd=R).decode().strip(),'git_status_short':subprocess.check_output(['git','status','--short'],cwd=R).decode()}
scope.write_text(json.dumps(a,indent=2));print('Protected',a['unchanged_initial_files'],'unchanged;',len(changed),'intentional C++ extensions;',len(a['new_task_files']),'new task files; foreign additions:',len(a['other_new_files_not_claimed']))
