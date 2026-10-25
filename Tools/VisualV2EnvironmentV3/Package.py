"""Exact commit whitelist and complete existing-core integrity check. Never stages files."""
from pathlib import Path
import hashlib,json,subprocess,datetime
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/EnvironmentV3';base=json.loads((D/'Baseline.json').read_text());scope=json.loads((R/'Art/World/VisualV2EnvironmentV3/Scope.json').read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
files={'Content/Maps/Dev_TestMap_VisualV2.umap','Source/PokeMonster/Development/PokeMonsterNPCTestGround.cpp','Docs/TECHNIK.md','Docs/ENTSCHEIDUNGEN.md','Docs/VISUALV2_ENVIRONMENT_QUALITY_V3_PRUEFBERICHT.md'}
for root in ['Tools/VisualV2EnvironmentV3','Art/World/VisualV2EnvironmentV3','Content/Environment/VisualV2EnvironmentV3']:
 for p in (R/root).rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts and p.suffix in ['.py','.md','.json','.blend','.fbx','.uasset']:files.add(str(p.relative_to(R)))
assert not files.intersection(base['untracked']);assert all((R/f).is_file()for f in files)
protected=[]
for rel,v in base['protected'].items():
 if rel=='Content/Maps/Dev_TestMap_VisualV2.umap':continue
 assert(R/rel).is_file()and sha(R/rel)==v['sha256'],('Protected file changed',rel);protected.append(rel)
for ref,v in base['backup_refs'].items():assert subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()==v
old=json.loads(subprocess.check_output(['git','show',base['head']+':Tools/DevelopmentEvidence/CoreFiles.json'],cwd=R,text=True));changed=[]
for rel,v in old['files'].items():
 assert(R/rel).is_file(),('Existing core file missing',rel)
 if sha(R/rel)!=v['sha256']:changed.append(rel)
allowed_existing={'Content/Maps/Dev_TestMap_VisualV2.umap','Source/PokeMonster/Development/PokeMonsterNPCTestGround.cpp','Docs/TECHNIK.md','Docs/ENTSCHEIDUNGEN.md'};assert set(changed)<=allowed_existing,(changed,allowed_existing)
core=json.loads((R/'Tools/DevelopmentEvidence/CoreFiles.json').read_text());assert core['files'].keys()>=old['files'].keys()
for rel in sorted(files):core['files'][rel]={'bytes':(R/rel).stat().st_size,'sha256':sha(R/rel)}
core['files']=dict(sorted(core['files'].items()));core['generated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();core['snapshot_kind']='visualv2_environment_quality_v3_verified';(R/'Tools/DevelopmentEvidence/CoreFiles.json').write_text(json.dumps(core,indent=2)+'\n');files.add('Tools/DevelopmentEvidence/CoreFiles.json')
assert {str(p.relative_to(R))for p in (R/'Content/Environment/VisualV2EnvironmentV3').rglob('*.uasset')}=={'Content/'+p.removeprefix('/Game/')+'.uasset'for p in scope['assets']}
(D/'PackageFiles.json').write_text(json.dumps(sorted(files),indent=2));(D/'Integrity.json').write_text(json.dumps({'passed':True,'prior_core_files':len(old['files']),'unchanged_prior_core_files':len(old['files'])-len(changed),'approved_existing_changes':changed,'protected_untracked':len(base['untracked']),'other_maps_and_saves':True,'backup_refs':base['backup_refs'],'package_files':len(files)},indent=2));print({'files':len(files),'existing_changes':changed,'protected':len(protected)})
