"""Read-only whole-map signature, authored geometry and required asset availability."""
import unreal,json,sys,math,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldOverhaulV3';sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W.get_name()=='Dev_TestMap_VisualV2';out=scene(W);(D/'SceneFinal.json').write_text(json.dumps(out,indent=2));before=json.loads((D/'SceneBefore.json').read_text());changed=[]
for k,v in before['actors'].items():
 assert k in out['actors'],('Removed original actor',k)
 if v!=out['actors'][k]:
  if v['class']=='/Script/PokeMonster.PokeMonsterRestPoint':
   q=copy.deepcopy(out['actors'][k]);assert len(q['components'])==len(v['components'])
   for old,new in zip(v['components'],q['components']):
    if 'materials'in old:new['materials']=old['materials']
   assert q==v,('Rest point logic/transform changed',k)
  elif v['class']=='/Script/PokeMonster.PokeMonsterInteractionTestActor'and v['label']=='Dev_InteractionMarker_Separat':
   q=copy.deepcopy(out['actors'][k]);proof=json.loads((D/'PlaceholderCrate.json').read_text());q['components']=[c for c in q['components']if c['name']!=proof['new_visual']]
   assert len(q['components'])==len(v['components'])
   for old,new in zip(v['components'],q['components']):
    if old['name']=='Mesh':new['props']['visible']=old['props']['visible']
   assert q==v,('Marker logic, collider or transform changed',k)
  else:assert v['class']in ['/Script/Engine.StaticMeshActor','/Script/Engine.Actor'],('Functional actor changed',k,v['class'])
  changed.append(dict(actor=k,label=v['label']))
assert before['world_settings']==out['world_settings'];added=[v for k,v in out['actors'].items()if k not in before['actors']];assert all(v['label'].startswith('WOV3_')for v in added)
assets=unreal.EditorAssetLibrary.list_assets('/Game/Environment/VisualV2WorldOverhaulV3',True,False);missing=[]
for p in assets:
 a=unreal.load_asset(p);assert a,p
 for d in unreal.EditorAssetLibrary.find_package_referencers_for_asset(p,False):pass
registry=unreal.AssetRegistryHelpers.get_asset_registry();opt=unreal.AssetRegistryDependencyOptions(include_hard_package_references=True,include_soft_package_references=True)
for p in assets:
 for dep in registry.get_dependencies(p.split('.')[0],opt):
  s=str(dep)
  if s.startswith('/Game/')and not unreal.EditorAssetLibrary.does_asset_exist(s):missing.append(dict(asset=p,dependency=s))
assert not missing,missing
(D/'FinalAudit.json').write_text(json.dumps(dict(changed_original_static_actors=changed,unchanged_functional_actors=True,unchanged_world_settings=True,added_own_actors=len(added),own_assets=len(assets),missing_dependencies=missing),indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
