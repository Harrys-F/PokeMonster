"""Read-only map/content check after material fix. Never saves a map."""
import unreal,json,sys,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2MaterialFixV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
before=json.loads((O/'Before_MaterialAudit.json').read_text());after=json.loads((O/'After_MaterialAudit.json').read_text())
def clean(x):return re.sub(r'0x[0-9a-fA-F]+','<address>',json.dumps(x,sort_keys=True))
p=before['master_properties'].copy();p['used_with_instanced_static_meshes']='True';assert after['master_properties']==p
for key in ['instance_parameters','instance_properties','parent','components']:assert clean(before[key])==clean(after[key]),key
assert json.loads((O/'Before_Graph.json').read_text())==json.loads((O/'After_Graph.json').read_text())
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');assert scene(E.get_editor_world())==json.loads((O/'Before_Scene.json').read_text())
checks=[]
for name in ['Dev_TestMap_VisualV2','Dev_TestMap_VisualV2GPUBottleneckV1','Dev_WestlandAssetLibrary']:
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/'+name)
 unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'MAP CHECK');checks.append(name)
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2')
assert unreal.load_asset(before['master']).get_editor_property('used_with_instanced_static_meshes')
(O/'FinalAudit.json').write_text(json.dumps({'master_property_only_usage_changed':True,'connected_graph_identical':True,'parameters_textures_references_identical':True,'central_scene_identical':True,'maps_checked':checks,'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]},indent=2))
