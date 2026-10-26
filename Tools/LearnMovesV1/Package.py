"""Exact phase B package, untouched user files/maps/models and approved previous hashes."""
from pathlib import Path
import hashlib,json,subprocess,datetime
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/LearnMovesV1';base=json.loads((R/'Saved/ProjectRefinement/SaveSystemV2/Baseline.json').read_text());prior='dcb8c464b1723c7c959454aa1e153a762dfc3fb2';manifest='Tools/DevelopmentEvidence/CoreFiles.json'
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).strip()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
assert git('branch','--show-current')=='main'and git('rev-parse','HEAD')==prior
for name,v in base['protected'].items():
 p=R/name;assert p.is_file()and p.stat().st_size==v['bytes']and sha(p)==v['sha256'],name
assert not(R/'Saved/SaveGames/PokeMonster_Recovery.sav').exists()
for ref,v in base['backup_refs'].items():assert git('rev-parse',ref)==v
files=set('''Docs/ENTSCHEIDUNGEN.md
Docs/TECHNIK.md
Docs/SPEICHERSYSTEM_V2_LERNATTACKEN_V1_PRUEFBERICHT.md
Source/PokeMonster/Battle/PokeMonsterBattleLibrary.cpp
Source/PokeMonster/Battle/PokeMonsterBattleLibrary.h
Source/PokeMonster/Battle/PokeMonsterBattleSession.cpp
Source/PokeMonster/Battle/PokeMonsterBattleSession.h
Source/PokeMonster/Development/PokeMonsterEvolutionV2Review.cpp
Source/PokeMonster/Development/PokeMonsterMoveEffectsV4Review.cpp
Source/PokeMonster/Development/PokeMonsterLearnMovesV1Review.cpp
Source/PokeMonster/Tests/PokeMonsterLearnMovesV1Test.cpp
Source/PokeMonster/Encounter/PokeMonsterEncounterSubsystem.cpp
Source/PokeMonster/Moves/PokeMonsterMoveData.cpp
Source/PokeMonster/Moves/PokeMonsterMoveEffectComponent.h
Source/PokeMonster/UI/PokeMonsterBattlePresenter.cpp
Tools/GameplayPraxisV1/Guard.py
Tools/GameplayPraxisV1/Run.py'''.splitlines())
for name in ['Bibor','Garados','Habitak','Karpador','Smettbo']:files.add('Content/Data/Creatures/DA_'+name+'.uasset')
for p in(R/'Tools/LearnMovesV1').rglob('*'):
 if p.is_file()and'__pycache__'not in p.parts:assert p.suffix in ['.py','.md','.json'];files.add(str(p.relative_to(R)))
newassets=list((R/'Content/Data/Moves/LearnMovesV1').glob('*.uasset'));assert len(newassets)==15
files.update(str(p.relative_to(R))for p in newassets)
assert set(git('diff','--name-only').splitlines())<=files|{manifest}
old=json.loads(git('show',prior+':'+manifest));core=json.loads((R/manifest).read_text());assert set(core['files'])==set(old['files'])or set(core['files'])-set(old['files'])<=files
for name,v in old['files'].items():
 if name not in files:assert(R/name).is_file()and sha(R/name)==v['sha256'],name
others=set(git('ls-files','--others','--exclude-standard').splitlines());assert set(base['untracked'])<=others;assert others-set(base['untracked'])<=files
for name in sorted(files):
 p=R/name;assert p.is_file();core['files'][name]={'bytes':p.stat().st_size,'sha256':sha(p)}
core['files']=dict(sorted(core['files'].items()));core['generated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();core['snapshot_kind']='save_v2_learning_moves_v1_verified';(R/manifest).write_text(json.dumps(core,indent=2)+'\n');files.add(manifest)
(D/'PackageFiles_B.json').write_text(json.dumps(sorted(files),indent=2)+'\n')
result=dict(passed=True,baseline_commit=prior,protected_files=len(base['protected']),protected_untracked=len(base['untracked']),unchanged_prior_core_files=len(old['files'])-len(set(old['files'])&files),no_map_model_or_animation_change=True,backup_refs=base['backup_refs'],package_files=len(files),lfs_assets=20,lfs_total_bytes=sum((R/p).stat().st_size for p in files if p.endswith('.uasset')))
(D/'Integrity_B.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
