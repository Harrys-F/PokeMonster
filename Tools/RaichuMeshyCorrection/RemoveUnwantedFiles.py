"""Finite authorized removal set. Generic reports/tools and all unrelated files are retained."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/RaichuMeshyCorrection';replacement=json.loads((D/'Replacement.json').read_text());deleted_assets=json.loads((D/'AssetDeletion.json').read_text());assert deleted_assets['count']==16;assert replacement['active_mesh'].startswith('/Game/Characters/Creatures/Raichu/MeshyV1/');source=R/replacement['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==replacement['source_sha256'];assert (R/'Saved/CreatureExpansionV3/RaichuMeshyCorrection03/Result.json').is_file()
plan=json.loads((D/'RemovalPlan.json').read_text());assert len(plan)==32
# These two files were read in full: they exclusively open/import the old Raichu_V4 source/asset.
for name,required in [('ReviseFaint.py','Raichu_V4.blend'),('RefreshOwnFaint.py','/Game/Characters/Creatures/Raichu/V4')]:
 p=R/'Saved/ProjectRefinement/ModelsV4'/name;assert p.is_file()and required in p.read_text();plan.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exclusively_authored_raichu':True})
assert all('WriteReport.py'not in x['path']for x in plan);assert len({x['path']for x in plan})==34
(D/'RemovalPlanFinal.json').write_text(json.dumps(plan,indent=2));results=[]
for row in plan:
 p=R/row['path'];assert not p.is_symlink();assert p.suffix.lower()not in ['.sav','.glb','.ini'];assert '/Incoming/'not in row['path']
 if row['path'].startswith('Content/'):
  assert row['path'].startswith('Content/Characters/Creatures/Raichu/V4/')and not p.exists();method='Unreal guarded batch deletion already verified'
 else:
  assert p.is_file()and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path'];p.unlink();method='Exact hash-checked filesystem unlink'
 assert not p.exists();results.append({'path':row['path'],'action':'deleted','exists_after':False,'method':method,'sha256_before':row['sha256']})
for base in [R/'Art/Characters/Creatures/Raichu/Exports/V4',R/'Content/Characters/Creatures/Raichu/V4']:
 if base.exists():
  for p in sorted(base.rglob('*'),key=lambda p:len(p.parts),reverse=True):
   if p.is_dir()and not any(p.iterdir()):p.rmdir()
  if not any(base.iterdir()):base.rmdir()
(D/'RemovalResults.json').write_text(json.dumps(results,indent=2));assert source.is_file()and hashlib.sha256(source.read_bytes()).hexdigest()==replacement['source_sha256'];print('REMOVED_EXCLUSIVE_RAICHU_FILES',len(results),'Shared WriteReport retained')
