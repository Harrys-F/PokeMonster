"""Hashes only: preserve existing user originals, maps, save slots and backup refs."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/SaveSystemV2';D.mkdir(exist_ok=True)
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).strip()
def digest(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return {'bytes':p.stat().st_size,'sha256':h.hexdigest()}
p=D/'Baseline.json';assert not p.exists()
others=[x for x in git('ls-files','--others','--exclude-standard').splitlines()if not x.startswith('Tools/SaveSystemV2/')]
paths=sorted(set(others+[str(x.relative_to(R))for x in(R/'Content/Maps').glob('*.umap')]+[str(x.relative_to(R))for x in(R/'Saved/SaveGames').glob('*')if x.is_file()]))
v={'head':git('rev-parse','HEAD'),'untracked':others,'protected':{x:digest(R/x)for x in paths},'backup_refs':{x:git('rev-parse',x)for x in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']}}
p.write_text(json.dumps(v,indent=2)+'\n');print('BASELINE',v['head'],len(paths),'protected originals')
