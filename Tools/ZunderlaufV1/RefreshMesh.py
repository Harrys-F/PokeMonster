"""Reimport only our diagnosed eye-normal correction; preserve the existing creature skeleton and materials."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P='/Game/Characters/Creatures/Zunderlauf';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();m=unreal.load_asset(P+'/Meshes/SK_Zunderlauf');sk=m.skeleton;slots=list(m.materials);old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH,'create_physics_asset':False,'skeleton':sk}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(R/'Art/Characters/Creatures/Zunderlauf/Exports/Zunderlauf_Idle.fbx'),'destination_path':P+'/Meshes','destination_name':'SK_Zunderlauf','automated':True,'save':False,'replace_existing':True,'replace_existing_settings':True,'options':ui}.items():t.set_editor_property(k,v)
 unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);m=unreal.load_asset(P+'/Meshes/SK_Zunderlauf');assert m.skeleton==sk;m.materials=slots;assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
 data=unreal.load_asset(P+'/DA_Zunderlauf_Presentation');data.set_editor_property('ground_offset_cm',.71433);assert unreal.EditorAssetLibrary.save_loaded_asset(data,False)
 for a in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
  assert a.get_name().startswith(P),a.get_name()
  if a.get_name()==sk.get_outermost().get_name():assert unreal.EditorAssetLibrary.save_loaded_asset(sk,False)
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
 (R/'Saved/ZunderlaufV1/MeshRefresh.json').write_text(json.dumps({'mesh':m.get_path_name(),'same_skeleton':True,'same_material_slots':True,'changed_only_eye_winding':True,'ground_offset_cm':.71433},indent=2));unreal.log('ZUNDERLAUF_EYE_REIMPORT_PASS')
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(old))
