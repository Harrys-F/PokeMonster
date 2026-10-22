"""Only the three unpublished V6 player animations; original mesh/skeleton never saved."""
import unreal,json,ast,hashlib,subprocess
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P='/Game/Characters/YoungTrainer/AnimationV6';assert not subprocess.check_output(['git','ls-files','--','Content/Characters/YoungTrainer/AnimationV6'],cwd=R).strip();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert all(x.get_path_name().startswith(P+'/A_Player_')for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();a=json.loads((R/'Art/Characters/YoungTrainer/AnimationCorrectionsV6_Audit.json').read_text());sk=unreal.load_asset('/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2').skeleton;T=unreal.AssetToolsHelpers.get_asset_tools();old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 for x in a['exports']:
  assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'];ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,use_default_sample_rate=False,custom_sample_rate=60,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
  task=unreal.AssetImportTask()
  for k,v in dict(filename=str(R/x['path']),destination_path=P,destination_name='A_Player_'+x['role']+'_V6',automated=True,save=False,replace_existing=True,replace_existing_settings=True,options=ui).items():task.set_editor_property(k,v)
  T.import_asset_tasks([task]);clip=next(v for v in task.get_objects()if isinstance(v,unreal.AnimSequence));assert clip.get_editor_property('skeleton')==sk;clip.set_editor_property('enable_root_motion',False);assert unreal.EditorAssetLibrary.save_loaded_asset(clip,False)
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();unreal.log('V6_PLAYER_POSED_PARENT_ELBOW_CLIPS_IMPORTED')
