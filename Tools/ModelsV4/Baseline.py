"""Read-only baseline; writes only new QA evidence, never copies a project or save."""
from pathlib import Path
import hashlib,json,subprocess,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/ModelsV4';D.mkdir(parents=True,exist_ok=True)
assert not(D/'Baseline.json').exists()
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True).strip()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
tracked=git('ls-files','-z').split('\0');untracked=git('ls-files','--others','--exclude-standard','-z').split('\0');files={}
for rel in tracked+untracked:
 p=R/rel
 if rel and p.is_file()and not p.is_symlink():files[rel]={'size':p.stat().st_size,'sha256':sha(p)}
saves={str(p.relative_to(R)):sha(p)for p in R.rglob('*.sav')if not p.is_symlink()and '.git'not in p.parts}
result={'head':git('rev-parse','HEAD'),'status':git('status','--porcelain=v1'),'untracked':[x for x in untracked if x],'files':files,'saves':saves,'backup_refs':{k:git('rev-parse',k)for k in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']}}
(D/'Baseline.json').write_text(json.dumps(result,indent=2));print('Baseline',len(files),'files',len(saves),'saves',len(result['untracked']),'untracked')
