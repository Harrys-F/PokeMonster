"""Read-only protection inventory; contains hashes, never copies project/save files."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2]; D=R/'Saved/ProjectRefinement/GameplayPraxisV1';D.mkdir(exist_ok=True)
def git(*a):return subprocess.check_output(['git',*a],cwd=R).decode().strip()
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return {'bytes':p.stat().st_size,'sha256':h.hexdigest()}
p=D/'Baseline.json';assert not p.exists(),'Existing baseline must not be overwritten'
untracked=[x for x in git('ls-files','--others','--exclude-standard').splitlines() if not x.startswith('Tools/GameplayPraxisV1/')]
protected=sorted(set(untracked+[str(x.relative_to(R)) for x in (R/'Content/Maps').glob('*.umap')]+[str(x.relative_to(R))for x in (R/'Saved/SaveGames').glob('*') if x.is_file()]))
v={'head':git('rev-parse','HEAD'),'status':git('status','--porcelain'),'untracked':untracked,'protected':{x:digest(R/x)for x in protected},'backup_refs':{x:git('rev-parse',x)for x in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']}}
p.write_text(json.dumps(v,indent=2));print({'protected':len(protected),'untracked':len(untracked),'head':v['head']})
