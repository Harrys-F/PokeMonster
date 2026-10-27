"""Read-only final identity/hash audit. No restores, staging or deletion."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';b=json.loads((D/'Baseline.json').read_text());changed=[];missing=[]
def digest(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
for path,old in b['files'].items():
 p=R/path
 if not p.is_file():missing.append(path)
 elif p.stat().st_size!=old['bytes']or digest(p)!=old['sha256']:changed.append(path)
refs={n:subprocess.check_output(['git','rev-parse',n],cwd=R,text=True).strip()for n in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']};assert refs=={n:b['refs'][n]for n in refs};allowed=['Content/Maps/Dev_TestMap_VisualV2.umap'];original_maps={p for p in b['files']if p.startswith('Content/Maps/')and p.endswith('.umap')};actual_maps={str(p.relative_to(R))for p in (R/'Content/Maps').glob('*.umap')};untracked_unchanged=all((R/p).is_file()and digest(R/p)==b['files'][p]['sha256']for p in b['untracked']);result={'passed':not missing and set(changed)==set(allowed)and original_maps==actual_maps and untracked_unchanged,'original_files':len(b['files']),'unchanged_original_files':len(b['files'])-len(changed)-len(missing),'changed':changed,'missing':missing,'original_untracked':len(b['untracked']),'original_untracked_unchanged':untracked_unchanged,'original_saves':sum(p.lower().endswith('.sav')for p in b['files']),'maps_same_paths':sorted(actual_maps),'backup_refs_unchanged':refs};(D/'ProtectionFinal.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert result['passed']
