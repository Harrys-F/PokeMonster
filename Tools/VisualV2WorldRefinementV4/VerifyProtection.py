"""Verify original working files/saves against task-start SHA256, without resetting anything."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4'
allowed={'.gitignore','Content/Maps/Dev_TestMap_VisualV2.umap','Docs/ENTSCHEIDUNGEN.md'}
results={}
for name in ['FileBaseline','OriginalAssetBaseline','SaveBaseline']:
 original=json.loads((D/(name+'.json')).read_text());changed=[];missing=[]
 for relative,sha in original.items():
  p=R/relative
  if not p.is_file():missing.append(relative);continue
  h=hashlib.sha256()
  with p.open('rb')as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  if h.hexdigest()!=sha:changed.append(relative)
 unexpected=set(changed)-allowed if name=='FileBaseline'else set(changed);assert not missing and not unexpected,dict(baseline=name,missing=missing,unexpected=sorted(unexpected));results[name]=dict(checked=len(original),changed=changed,missing=missing,unexpected=[])
refs={ref:subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()for ref in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']};assert all(v=='03492bd96b4dba44692f675c19d5f11abfa86b4b'for v in refs.values());results['backup_refs']=refs
results['user_config_sha256']=hashlib.sha256((R/'Config/DefaultEngine.ini').read_bytes()).hexdigest();(D/'ProtectionFinal.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
