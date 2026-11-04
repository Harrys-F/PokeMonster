"""Verify pre-existing files against this task's pre-migration hash manifests."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';allowed={'Content/Maps/Dev_WestlandRegion.umap','Docs/ENTSCHEIDUNGEN.md','Source/PokeMonster/Habitats/PokeMonsterHabitatSubsystem.cpp'}
def digest(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
r={}
for name in ['FileBaseline','AssetBaseline','SaveBaseline']:
 baseline=json.loads((D/(name+'.json')).read_text());missing=[];changed=[]
 for p,v in baseline.items():
  q=Path(p)if Path(p).is_absolute()else R/p
  if not q.is_file():missing.append(p)
  elif digest(q)!=v:changed.append(p)
 r[name]=dict(files=len(baseline),missing=missing,changed=changed,allowed_changes=sorted(set(changed)&allowed))
 assert not missing and not(set(changed)-allowed),(name,missing,changed)
b=json.loads((D/'GitBaseline.json').read_text());r['baseline_untracked_retained']=all((R/p).is_file()for p in b['untracked']);assert r['baseline_untracked_retained'];r['backup_refs']={}
for ref in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']:
 value=subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip();assert value=='03492bd96b4dba44692f675c19d5f11abfa86b4b';r['backup_refs'][ref]=value
r['user_config_sha256']=digest(R/'Config/DefaultEngine.ini');assert r['user_config_sha256']=='f676a51869c678a5820c869165154b6d6e05ae723c77c622d5fb510957799523';r['passed']=True;(D/'ProtectionAudit.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
