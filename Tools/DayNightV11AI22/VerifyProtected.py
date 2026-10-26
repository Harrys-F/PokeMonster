"""Verify pre-existing protected content without changing or copying it."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/DayNightV11AI22';b=json.loads((D/'Baseline.json').read_text());errors=[]
for n,h in b['hashes'].items():
 p=R/n
 if not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=h:errors.append(n)
for ref,h in b['refs'].items():
 if subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()!=h:errors.append(ref)
assert not errors,errors
r={'protected_files_unchanged':len(b['hashes']),'original_untracked_preserved':len(b['untracked']),'backup_refs_unchanged':True};(D/'Protected.json').write_text(json.dumps(r,indent=2));print(r)
