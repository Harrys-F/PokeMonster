"""Read-only guard of the actual pre-task originals, maps, save and local backup refs."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];O=R/'Saved/MeshyGlumandaV1';j=json.loads((O/'Initial.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for section in ['untracked_sha256','map_sha256']:
 for p,h in j[section].items():assert (R/p).is_file() and sha(R/p)==h,p
assert sha(R/'Saved/SaveGames/PokeMonster_Dev.sav')==j['save_sha256'],'Original save changed'
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True).strip()
full='03492bd96b4dba44692f675c19d5f11abfa86b4b'
for ref in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']:assert git('rev-parse',ref)==full
assert subprocess.run(['git','merge-base','--is-ancestor',full,'HEAD'],cwd=R).returncode==1
worktrees=git('worktree','list','--porcelain');assert worktrees.count('worktree ')==1
r={'passed':True,'original_files_unchanged':len(j['untracked_sha256']),'maps_unchanged':len(j['map_sha256']),'original_save_sha256':j['save_sha256'],'full_backup_preserved':full,'worktrees':1,'map_paths':list(j['map_sha256'])};(O/'ScopeValidation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
