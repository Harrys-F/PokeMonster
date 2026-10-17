import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=R/'Art/Characters/NPCs/Ranger/Exports/V2_Protected';P='/Game/Characters/NPCs/RangerV2/Diagnostic';old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH,'create_physics_asset':False,'skeleton':unreal.load_asset('/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1_Skeleton')}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(E/'SK_Ranger_NPC_V2_LOD1.fbx'),'destination_path':P,'destination_name':'SK_Ranger_LOD1_Diagnostic','automated':True,'save':False,'replace_existing':False,'options':ui}.items():t.set_editor_property(k,v)
 assert not unreal.EditorAssetLibrary.does_asset_exist(P+'/SK_Ranger_LOD1_Diagnostic');unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);m=unreal.load_asset(P+'/SK_Ranger_LOD1_Diagnostic');slots=list(m.materials);slots[0].material_interface=unreal.load_asset('/Game/Characters/NPCs/Ranger/Materials/MI_Ranger_V1');m.materials=slots;unreal.EditorAssetLibrary.save_loaded_asset(m,False)
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(old))
