"""Explicit package scope; protect pre-existing untracked files and all unrelated core files."""
from pathlib import Path
import json,hashlib,datetime,subprocess
R=Path(__file__).resolve().parents[2];O=R/'Saved/ProjectRefinement/NPCExpansion';base=json.loads((O/'Baseline.json').read_text());profiles=json.loads((O/'FinalProfiles.json').read_text());configs=json.loads((R/'Tools/NPCExpansion/Library.json').read_text());files=set();required_assets=set()
def asset(p):
 if p and p.startswith('/Game/Characters/NPCs/Library/'):
  required_assets.add('Content/'+p.split('.')[0].removeprefix('/Game/')+'.uasset')
for p in profiles:
 for f in ['profile','mesh','skeleton']:asset(p[f])
 for v in p['clips'].values():asset(v)
 for v in p['materials']:asset(v)
for name in ['BaseColor','Normal','MetalRough']:required_assets.add('Content/Characters/NPCs/Library/HobbitBase/Textures/T_HobbitBase_'+name+'.uasset')
actual={str(p.relative_to(R))for p in (R/'Content/Characters/NPCs/Library').rglob('*.uasset')};assert required_assets==actual,{'missing':sorted(required_assets-actual),'unexpected':sorted(actual-required_assets)};files|=actual
for a in configs:
 id=a['id'];C=R/'Art/Characters/NPCs'/id if id!='HobbitBase' else R/'Art/Characters/NPCs/Westland/HobbitBase';files.add(str((C/'Source'/(id+'_NPCLibrary.blend')).relative_to(R)))
 for p in (C/'Exports/Library').glob('*.fbx'):files.add(str(p.relative_to(R)))
for p in (R/'Tools/NPCExpansion').iterdir():
 if p.is_file() and p.suffix in ['.py','.json','.md']:files.add(str(p.relative_to(R)))
source=['Characters/PokeMonsterNPCAnimInstance.cpp','Characters/PokeMonsterNPCAnimInstance.h','Characters/PokeMonsterNPCVisualActor.cpp','Characters/PokeMonsterNPCVisualActor.h','Characters/PokeMonsterNPCPresentationData.cpp','Characters/PokeMonsterNPCPresentationData.h','Development/PokeMonsterNPCTestGround.cpp','Development/PokeMonsterNPCTestGround.h','Tests/PokeMonsterNPCLibraryTest.cpp']
files|={'Source/PokeMonster/'+x for x in source};files|={'Content/Maps/Dev_TestMap_VisualV2.umap','Docs/NPC_AUSBAU_MESHY_PRUEFBERICHT.md','Docs/ENTSCHEIDUNGEN.md','Docs/TECHNIK.md'}
assert not files.intersection(base['untracked']);assert all((R/p).is_file()for p in files)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
for p,h in base['protected'].items():
 if p=='Content/Maps/Dev_TestMap_VisualV2.umap':continue
 assert (R/p).is_file() and sha(R/p)==h,('Protected file changed',p)
p=R/'Tools/DevelopmentEvidence/CoreFiles.json';core=json.loads(p.read_text());changed=[]
original=json.loads(subprocess.check_output(['git','show',base['head']+':Tools/DevelopmentEvidence/CoreFiles.json'],cwd=R,text=True));original_changed=[rel for rel,v in original['files'].items()if (R/rel).is_file() and sha(R/rel)!=v['sha256']];assert set(original_changed)<=files
for rel,v in core['files'].items():
 assert (R/rel).is_file(),('Existing core file missing',rel)
 if sha(R/rel)!=v['sha256']:changed.append(rel)
assert set(changed)<=files,('Unrelated changes',sorted(set(changed)-files))
for rel in sorted(files):core['files'][rel]={'bytes':(R/rel).stat().st_size,'sha256':sha(R/rel)}
core['files']=dict(sorted(core['files'].items()));core['generated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();core['snapshot_kind']='npc_expansion_final_verification';p.write_text(json.dumps(core,indent=2)+'\n');files.add(str(p.relative_to(R)))
(O/'PackageFiles.json').write_text(json.dumps(sorted(files),indent=2));(O/'ProtectionVerification.json').write_text(json.dumps({'pre_existing_untracked_files':len(base['untracked']),'protected_files_verified':len(base['protected'])-1,'original_core_files_checked':len(original['files']),'unchanged_original_core_files_verified':len(original['files'])-len(original_changed),'expected_changed_existing_core_files':original_changed,'new_library_assets':len(actual),'package_files':len(files),'backup_ref':subprocess.check_output(['git','rev-parse','backup/full-03492bd'],cwd=R,text=True).strip()},indent=2));print(json.dumps({'assets':len(actual),'package_files':len(files),'existing_changes':changed,'protected_untracked':len(base['untracked'])}))
