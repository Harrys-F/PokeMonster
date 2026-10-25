"""Reimport only this task's private Ranger library mesh after retaining original source density."""
import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();P='/Game/Characters/NPCs/Library/Ranger/Meshes/SK_Ranger_Library';M=unreal.load_asset(P);assert M and '/Library/Ranger/' in M.get_path_name();old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH,'create_physics_asset':False,'skeleton':M.skeleton}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(R/'Art/Characters/NPCs/Ranger/Exports/Library/SK_Ranger_Library.fbx'),'destination_path':P.rsplit('/',1)[0],'destination_name':P.rsplit('/',1)[1],'automated':True,'save':False,'replace_existing':True,'options':ui}.items():t.set_editor_property(k,v)
 unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);M=unreal.load_asset(P);slots=list(M.materials);slots[0].material_interface=unreal.load_asset('/Game/Characters/NPCs/Ranger/Materials/MI_Ranger_V1');M.materials=slots;unreal.EditorAssetLibrary.save_loaded_asset(M,False);unreal.EditorAssetLibrary.save_loaded_asset(M.skeleton,False)
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
