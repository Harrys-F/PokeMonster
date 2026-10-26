"""Read-only protection and explicit change-set audit. Does not stage or commit."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/PokemonAIV2';base=json.loads((D/'Baseline.json').read_text())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).strip()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(4194304),b''):h.update(b)
 return h.hexdigest()
assert git('branch','--show-current')=='main'
assert git('remote','get-url','origin')=='git@github.com:Harrys-F/PokeMonster.git'
for name,old in base['protected'].items():
 p=R/name;assert p.is_file()and p.stat().st_size==old['bytes']and sha(p)==old['sha256'],name
for ref,value in base['backup_refs'].items():assert git('rev-parse',ref)==value
assert not(R/'Saved/SaveGames/PokeMonster_Recovery.sav').exists()
fixed='''Docs/ENTSCHEIDUNGEN.md
Docs/TECHNIK.md
Docs/POKEMON_KI_V2_PRUEFBERICHT.md
Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureBehavior.h
Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h
Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureRoamingComponent.cpp
Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureActivities.h
Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureActivities.cpp
Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureRoamingActivities.cpp
Source/PokeMonster/Tests/PokeMonsterNaturalActivitiesTest.cpp
Source/PokeMonster/Development/PokeMonsterSaveV2Review.cpp'''.splitlines()
files=sorted(set(fixed+[str(p.relative_to(R))for p in (R/'Tools/PokemonAIV2').iterdir()if p.is_file()and p.suffix in ['.py','.md']]))
assert all((R/p).is_file()for p in files)
untracked=git('ls-files','--others','--exclude-standard').splitlines();assert set(untracked)-set(files)==set(base['untracked']),'Unrelated untracked files changed'
tracked=set(git('diff','--name-only',base['head']).splitlines());assert tracked<=set(files),('Unrelated tracked changes',tracked-set(files))
subprocess.run(['git','diff','--check'],cwd=R,check=True)
result={'protected_file_count':len(base['protected']),'protected_files_identical':True,'untracked_originals_unchanged':len(base['untracked']),'backup_refs_identical':True,'canonical_recovery_save_not_created':True,'allowed_files':files,'changed_tracked':sorted(tracked),'no_assets_maps_animations_or_saves_in_package':True}
(D/'Protection.json').write_text(json.dumps(result,indent=2));print('PROTECTION_PASS',len(base['protected']),'protected,',len(files),'explicit package paths')
