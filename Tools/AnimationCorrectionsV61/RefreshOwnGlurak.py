"""Only refine our unpublished V6.1 mesh. Never reimport an original asset."""
import unreal,subprocess,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P='/Game/Characters/Creatures/Glurak/AnimationV61/SK_Glurak_V61';disk='Content/Characters/Creatures/Glurak/AnimationV61/SK_Glurak_V61.uasset';assert not subprocess.check_output(['git','ls-files','--',disk],cwd=R).strip(),'Published asset: use a reviewed explicit update';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();mesh=unreal.load_asset(P);sk=mesh.skeleton;slots=list(mesh.materials);ui=unreal.FbxImportUI()
for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False,skeleton=sk).items():ui.set_editor_property(k,v)
for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
t=unreal.AssetImportTask()
for k,v in dict(filename=str(R/'Art/Characters/Creatures/Glurak/Exports/AnimationV61/Glurak_Idle.fbx'),destination_path=P.rsplit('/',1)[0],destination_name=P.rsplit('/',1)[1],automated=True,save=False,replace_existing=True,options=ui).items():t.set_editor_property(k,v)
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
mesh=unreal.load_asset(P);assert mesh.skeleton==sk;mesh.set_editor_property('materials',slots);assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();unreal.log('V61_UNPUBLISHED_GLURAK_REFINED')
