"""Read-only project protection checks; writes only an ignored receipt under Saved."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];assert R==Path('/Users/harry/Developer/PokeMonster');O=R/'Saved/WildEncountersV2';initial=json.loads((O/'Initial.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).strip()
for name,h in initial['untracked'].items():assert (R/name).is_file()and sha(R/name)==h,('Protected file changed',name)
maps={p.relative_to(R).as_posix():sha(p)for p in (R/'Content/Maps').glob('*.umap')};assert maps.keys()==initial['maps'].keys()
for name,h in initial['maps'].items():
 if name!='Content/Maps/Dev_TestMap_VisualV2.umap':assert maps[name]==h,('Protected map changed',name)
assert json.loads((O/'GroupSavePreflight.json').read_text())['serialized_nontransient_properties_equal_except_exact_bisasam_group_size']
assert sha(R/'Saved/SaveGames/PokeMonster_Dev.sav')==initial['save'],'Original developer save not restored'
backup='03492bd96b4dba44692f675c19d5f11abfa86b4b'
for ref in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']:assert git('rev-parse',ref)==backup
assert subprocess.run(['git','merge-base','--is-ancestor',backup,'HEAD'],cwd=R).returncode==1,'Backup must not enter main history'
assert git('branch','--show-current')=='main';assert len(git('worktree','list','--porcelain').split('worktree '))-1==1
untracked=[p for p in subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=R).decode().split('\0')if p]
allowed_new={'Source/PokeMonster/Tests/PokeMonsterWildEncountersV2Test.cpp','Docs/WILDE_POKEMON_BEGEGNUNGEN_V2_PRUEFBERICHT.md'}
unknown=[p for p in untracked if p not in initial['untracked']and p not in allowed_new and not p.startswith('Tools/WildEncountersV2/')];assert not unknown,unknown
receipt={'passed':True,'protected_untracked_files':len(initial['untracked']),'protected_other_maps':len(maps)-1,'existing_map_count':len(maps),'backup_ref':backup,'backup_not_in_main_history':True,'worktree_count':1,'original_dev_save_sha256':initial['save'],'head':git('rev-parse','HEAD'),'branch':'main','remote':git('remote','get-url','origin'),'visualv2_intended_change':'Only verified Bisasam GroupSize 1 -> 3; no landscape/light/material/transform changes'};(O/'FinalSafety.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
