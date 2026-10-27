"""Read-only comparison to the pre-task hashes. Never restores or rewrites originals."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GraphicsVariantC';base=json.loads((D/'Baseline.json').read_text());changes=[]
def digest(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
for name,expected in base['files'].items():
 p=R/name
 if not p.is_file()or p.is_symlink()or p.stat().st_size!=expected['bytes']or digest(p)!=expected['sha256']:changes.append(name)
refs={ref:subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()for ref in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']}
assert all(base['refs'][k]==v for k,v in refs.items())
result={'protected_files':len(base['files']),'original_save_files':sum(n.endswith('.sav')for n in base['files']),'original_untracked':len(base['untracked']),'changed_or_missing':changes,'backup_refs_unchanged':True}
(D/'ProtectionFinal.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not changes
