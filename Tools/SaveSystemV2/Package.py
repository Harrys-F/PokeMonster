"""Hash-protected exact package; never stage, copy saves or alter references."""
from pathlib import Path
import hashlib,json,subprocess,datetime,re
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/SaveSystemV2';base=json.loads((D/'Baseline.json').read_text());manifest='Tools/DevelopmentEvidence/CoreFiles.json'
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).strip()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
assert git('branch','--show-current')=='main';assert git('remote','get-url','origin')=='git@github.com:Harrys-F/PokeMonster.git'
for name,v in base['protected'].items():
 p=R/name;assert p.is_file()and p.stat().st_size==v['bytes']and sha(p)==v['sha256'],name
assert not(R/'Saved/SaveGames/PokeMonster_Recovery.sav').exists()
for ref,v in base['backup_refs'].items():assert git('rev-parse',ref)==v
approved=set('''Docs/ENTSCHEIDUNGEN.md
Docs/SPIELREGELN.md
Docs/TECHNIK.md
Docs/SPEICHERSYSTEM_V2_LERNATTACKEN_V1_PRUEFBERICHT.md
Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp
Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h
Source/PokeMonster/Checkpoint/PokeMonsterCheckpointSubsystem.cpp
Source/PokeMonster/Checkpoint/PokeMonsterCheckpointSubsystem.h
Source/PokeMonster/Development/PokeMonsterMoveManagementV2Review.cpp
Source/PokeMonster/Development/PokeMonsterSwitchProInputReview.cpp
Source/PokeMonster/Encounter/PokeMonsterEncounterSubsystem.cpp
Source/PokeMonster/Interaction/PokeMonsterRestPoint.cpp
Source/PokeMonster/Save/PokeMonsterSaveGame.h
Source/PokeMonster/Save/PokeMonsterSaveSubsystem.cpp
Source/PokeMonster/Save/PokeMonsterSaveSubsystem.h
Source/PokeMonster/UI/PokeMonsterOverworldPlayerController.cpp
Source/PokeMonster/UI/PokeMonsterOverworldWidget.cpp
Source/PokeMonster/UI/PokeMonsterOverworldWidget.h
Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp
Source/PokeMonster/World/PokeMonsterBuildingCutaway.h
Tools/GlutexoEvolutionV2/ReviewEvolution.py
Tools/GlutexoEvolutionV2/ReviewManualEvolution.py
Tools/MoveManagementV2/Review.py
Tools/MoveManagementV2/RunReview.py
Source/PokeMonster/Development/PokeMonsterSaveV2Review.cpp
Source/PokeMonster/Tests/PokeMonsterSaveV2Test.cpp'''.splitlines())
for p in(R/'Tools/SaveSystemV2').rglob('*'):
 if p.is_file()and'__pycache__'not in p.parts:assert p.suffix in ['.py','.md','.json'];approved.add(str(p.relative_to(R)))
old=json.loads(git('show',base['head']+':'+manifest));core=json.loads((R/manifest).read_text());assert set(core['files'])-set(old['files'])<=approved
for name,v in old['files'].items():
 if name not in approved:assert sha(R/name)==v['sha256'],name
others=set(git('ls-files','--others','--exclude-standard').splitlines());assert set(base['untracked'])<=others
# Separately prepared phase B tools are not part of this milestone.
assert all(x in approved or x in base['untracked']or x.startswith('Tools/LearnMovesV1/')for x in others)
assert set(git('diff','--name-only').splitlines())<=approved|{manifest}
for name in approved:
 p=R/name;assert p.is_file();core['files'][name]={'bytes':p.stat().st_size,'sha256':sha(p)}
core['files']=dict(sorted(core['files'].items()));core['generated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();core['snapshot_kind']='save_system_v2_phase_a_verified';(R/manifest).write_text(json.dumps(core,indent=2)+'\n')
(D/'PackageFiles_A.json').write_text(json.dumps(sorted(approved|{manifest}),indent=2)+'\n')
(D/'Integrity_A.json').write_text(json.dumps(dict(passed=True,protected_files=len(base['protected']),protected_untracked=len(base['untracked']),unchanged_prior_core_files=len(old['files'])-len(set(old['files'])&approved),backup_refs=base['backup_refs']),indent=2))
print('VERIFIED_PACKAGE',len(approved)+1)
