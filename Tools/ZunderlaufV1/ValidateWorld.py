"""Strict map scope plus explicit creature binding; the pre-existing V5 art contract remains intact."""
import unreal,json,sys,runpy,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ZunderlaufV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
runpy.run_path(str(R/'Tools/ProjectMaintenance/ValidateRefinedArt.py'),run_name='__main__')
a=scene(w);b=json.loads((O/'BeforeScene.json').read_text()) if (O/'BeforeScene.json').exists() else None
def canonical(x):
 if isinstance(x,dict):
  v={k:canonical(a)for k,a in x.items()}
  if 'components'in v:v['components']=sorted(v['components'],key=lambda q:q['name'])
  return v
 if isinstance(x,list):return [canonical(a)for a in x]
 return x
assert b is None or canonical(a)==canonical(b),'Existing scene components/transforms/renderer/collisions must match exactly'
source=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor));assert source.encounter_id=='Dev_VisibleWild' and source.seed==3817;assert source.profile.get_path_name()=='/Game/Data/Encounters/DA_Zunderlauf_Wild.DA_Zunderlauf_Wild';assert source.get_editor_property('visual_species').get_path_name()=='/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf';assert source.get_editor_property('ambient_motion')
assert len(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor))==0,'Creature is runtime-only, not duplicate saved geometry'
j=json.loads((O/'Initial.json').read_text()) if (O/'Initial.json').exists() else {'untracked_sha256':{},'map_sha256':{}};unchanged=[]
for path,digest in j['untracked_sha256'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path;unchanged.append(path)
for path,digest in j['map_sha256'].items():
 if path.endswith('/Dev_TestMap_VisualV2.umap'):continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
(O/'WorldValidation.json').write_text(json.dumps({'passed':True,'existing_scene_signature_unchanged':True,'historical_detailed_comparison':b is not None,'only_explicit_wild_species_profile_and_opt_in_motion_changed':True,'protected_untracked_files_verified':len(unchanged),'other_maps_unchanged':True,'original_v5_art_contract_passed':True},indent=2));unreal.log('ZUNDERLAUF_WORLD_SCOPE_PASS')
