"""Protect original inputs and save slots without copying them. Explicit host-side QA only."""
from pathlib import Path
import json,hashlib,subprocess,os,time
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/TSRComparisonC75';D.mkdir(exist_ok=True)
def digest(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=R,text=True).split('\0');untracked=[p for p in untracked if p and not p.startswith('Tools/TSRComparisonC75/')]
paths=[R/p for p in untracked]+list((R/'Saved').rglob('*.sav'))+list((R/'Art').rglob('*'))+list((R/'Content').rglob('*'))+[R/'Config/DefaultEngine.ini']
files={str(p.relative_to(R)):{'bytes':p.stat().st_size,'sha256':digest(p)}for p in paths if p.is_file()and not p.is_symlink()}
refs={ref:subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()for ref in ['HEAD','origin/main','backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']}
p=D/'Baseline.json';assert not p.exists(),'Never overwrite an existing baseline';p.write_text(json.dumps({'created':time.time(),'untracked':untracked,'files':files,'refs':refs},indent=2));print(json.dumps({'protected_files':len(files),'untracked':len(untracked),'refs':refs}),flush=True)
