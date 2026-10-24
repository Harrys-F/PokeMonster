"""Add one swim clip/profile to a new namespace; current species, mesh and battle clips untouched."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and all(x.get_path_name().startswith('/Game/Characters/Creatures/Schiggy/BiomeV11/')for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
species=unreal.load_asset('/Game/Data/Creatures/DA_Schiggy');original=species.get_visuals().presentation;P='/Game/Characters/Creatures/Schiggy/BiomeV11';assert not unreal.EditorAssetLibrary.does_asset_exist(P+'/DA_Schiggy_SwimPresentation')
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=original.mesh.skeleton,override_full_name=True).items():ui.set_editor_property(k,v)
 for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask()
 for k,v in dict(filename=str(R/'Art/Characters/Creatures/Schiggy/Exports/BiomeV11/Schiggy_Swim.fbx'),destination_path=P,destination_name='A_Schiggy_Swim',automated=True,save=False,replace_existing=False,options=ui).items():t.set_editor_property(k,v)
 existing=[unreal.load_asset(x)for x in unreal.EditorAssetLibrary.list_assets(P,recursive=True,include_folder=False)];clips=[x for x in existing if isinstance(x,unreal.AnimSequence)];assert len(clips)<=1
 if clips:clip=clips[0]
 else:
  unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);clip=next(x for x in t.get_objects()if isinstance(x,unreal.AnimSequence))
 clip.set_editor_property('enable_root_motion',False);assert clip.get_editor_property('skeleton')==original.mesh.skeleton;assert unreal.EditorAssetLibrary.save_loaded_asset(clip,False)
 profile=unreal.EditorAssetLibrary.duplicate_asset(original.get_path_name(),P+'/DA_Schiggy_SwimPresentation');profile.set_editor_property('swim_idle_clip',clip);profile.set_editor_property('swim_clip',clip);profile.set_editor_property('swim_reference_speed',original.walk_speed)
 assert not profile.get_validation_errors();assert profile.mesh==original.mesh and dict(profile.clips)==dict(original.clips);assert unreal.EditorAssetLibrary.save_loaded_asset(profile,False)
 assert species.get_visuals().presentation==original
 (R/'Saved/BiomeTestV11/ImportSchiggySwim.json').write_text(json.dumps({'profile':profile.get_path_name(),'clip':clip.get_path_name(),'original_profile':original.get_path_name(),'original_mesh_clips_and_species_unchanged':True},indent=2))
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
