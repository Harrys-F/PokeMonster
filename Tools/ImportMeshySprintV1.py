"""Import only a new animation onto the existing unchanged Meshy V2 skeleton."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/Sprint_20261014'
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()
mesh=unreal.load_asset('/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2');assert mesh
name='A_Player_Meshy_Run_V1';D='/Game/Characters/YoungTrainer/MeshyV2/Animations';assert not unreal.EditorAssetLibrary.does_asset_exist(D+'/'+name)
ui=unreal.FbxImportUI()
for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':mesh.skeleton,'override_full_name':True}.items():ui.set_editor_property(k,v)
for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':60,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
t=unreal.AssetImportTask()
for k,v in {'filename':str(R/'Art/Characters/YoungTrainer/Exports/SprintV1'/ (name+'.fbx')),'destination_path':D,'destination_name':name,'automated':True,'save':False,'replace_existing':False}.items():t.set_editor_property(k,v)
t.options=ui;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);assert t.imported_object_paths
a=next(unreal.load_asset(p) for p in t.imported_object_paths if isinstance(unreal.load_asset(p),unreal.AnimSequence))
if a.get_path_name().split('.')[0]!=D+'/'+name:assert unreal.EditorAssetLibrary.rename_asset(a.get_path_name().split('.')[0],D+'/'+name)
a=unreal.load_asset(D+'/'+name);a.set_editor_property('enable_root_motion',False);assert a.get_editor_property('skeleton')==mesh.skeleton
assert abs(a.get_play_length()-.45)<.01;unreal.EditorAssetLibrary.save_loaded_asset(a,False)
(O/'ImportAudit.json').write_text(json.dumps({'clip':a.get_path_name(),'seconds':a.get_play_length(),'skeleton':mesh.skeleton.get_path_name(),'dirty_content': [p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()]},indent=2))
unreal.log('SPRINT_RUN_IMPORT_COMPLETE')
