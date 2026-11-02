"""Read-only Fab and target-map inventory. Never saves imported packages."""
import unreal,json,sys,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
(D/'SceneBefore.json').write_text(json.dumps(scene(W),indent=2))
reg=unreal.AssetRegistryHelpers.get_asset_registry(); roots=['Jayant_Chakradhari_Assets','Megaplant_Library','Pack_Bonus','RockEnv_Pack','SimpleRocks','StyleHex_Studio','Fab'];out={}
for root in roots:
 rows=[]
 for d in reg.get_assets_by_path('/Game/'+root,recursive=True):
  cls=str(d.asset_class_path.asset_name);v=dict(path=str(d.package_name),type=cls)
  if cls in ['StaticMesh','Material','MaterialInstanceConstant','Texture2D']:
   a=d.get_asset()
   if cls=='StaticMesh':
    b=a.get_bounding_box();v.update(min=b.min.to_tuple(),max=b.max.to_tuple(),lods=a.get_num_lods(),triangles=[a.get_num_triangles(i) for i in range(a.get_num_lods())],materials=[m.material_interface.get_path_name() if m.material_interface else None for m in a.static_materials],nanite=str(a.get_editor_property('nanite_settings')),collision=str(a.get_editor_property('body_setup').get_editor_property('collision_trace_flag')) if a.get_editor_property('body_setup') else None)
   elif cls=='Texture2D':v.update(width=a.blueprint_get_size_x(),height=a.blueprint_get_size_y())
   elif cls=='Material':v.update(blend=str(a.get_editor_property('blend_mode')),two_sided=a.get_editor_property('two_sided'),instancing=a.get_editor_property('used_with_instanced_static_meshes'))
   else:v.update(parent=a.parent.get_path_name() if a.parent else None,scalar=str(a.scalar_parameter_values),vector=str(a.vector_parameter_values))
  rows.append(v)
 out[root]=rows
(D/'FabInventory.json').write_text(json.dumps(out,indent=2));(D/'InventoryDirty.json').write_text(json.dumps(dict(maps=[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],content=[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]),indent=2));unreal.log('FAB_INVENTORY_DONE')
