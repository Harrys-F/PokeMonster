"""Only the proven missing HISM usage flag. No map, graph or parameter edits."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2MaterialFixV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
a=json.loads((O/'Before_MaterialAudit.json').read_text());assert a['master_properties']['used_with_instanced_static_meshes']=='False'
m=unreal.load_asset(a['master']);mi=unreal.load_asset(a['instance']);assert mi.parent==m;assert not m.get_editor_property('used_with_instanced_static_meshes')
sys.path.insert(0,str(R/'Tools/VisualV2MaterialFixV1'));from GraphAudit import graph
before_graph=graph(m);(O/'Before_Graph.json').write_text(json.dumps(before_graph,indent=2))
m.set_editor_property('used_with_instanced_static_meshes',True);unreal.MaterialEditingLibrary.recompile_material(m);unreal.MaterialEditingLibrary.update_material_instance(mi)
allowed={m.get_outermost().get_name(),mi.get_outermost().get_name()};dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert all(x.get_name() in allowed for x in dirty),[x.get_name() for x in dirty]
assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
if mi.get_outermost() in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():assert unreal.EditorAssetLibrary.save_loaded_asset(mi,False)
assert m.get_editor_property('used_with_instanced_static_meshes');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert graph(m)==before_graph,'Unexpected connected graph change';(O/'After_Graph.json').write_text(json.dumps(graph(m),indent=2))
(O/'FixApplied.json').write_text(json.dumps({'set_property':'used_with_instanced_static_meshes','before':False,'after':True,'master':m.get_path_name(),'instance_updated':mi.get_path_name(),'saved_dirty_packages':[x.get_name() for x in dirty],'other_settings_edited':False},indent=2));unreal.log('VMF1_FIX_APPLIED')
