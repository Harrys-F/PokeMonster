"""Import only the derived Garados water rig; retain the original land/battle mesh and all seven clips."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosWaterV2';A=R/'Art/Characters/Creatures/Garados';P='/Game/Characters/Creatures/Garados/WaterV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not unreal.EditorAssetLibrary.does_directory_exist(P)
assert hashlib.sha256((R/'Art/Characters/Creatures/Incoming/Garados.glb').read_bytes()).hexdigest()=='ce0661729d56dfa628a3232f4296bd5ae3bd51a914f417e8e82426e33133f5b9'
profile=unreal.load_asset('/Game/Characters/Creatures/Garados/MeshyV1/DA_Garados_Presentation');original=profile.mesh;original_clips={str(k):v.get_path_name()for k,v in profile.clips.items()};T=unreal.AssetToolsHelpers.get_asset_tools();W=E.get_editor_world();created=[]
def save(a):assert a.get_path_name().startswith(P+'/');assert unreal.EditorAssetLibrary.save_loaded_asset(a,False);created.append(a.get_path_name());return a
def task(src,folder,name,ui):
 assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name);t=unreal.AssetImportTask()
 for k,v in dict(filename=str(src),destination_path=folder,destination_name=name,automated=True,save=False,replace_existing=False,options=ui).items():t.set_editor_property(k,v)
 T.import_asset_tasks([t]);return list(t.get_objects())
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False).items():ui.set_editor_property(k,v)
 for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 mesh=next(x for x in task(A/'Exports/WaterV2/Garados_SwimIdle_V2.fbx',P+'/Meshes','SK_Garados_Water_V2',ui)if isinstance(x,unreal.SkeletalMesh));sk=mesh.skeleton;slots=list(mesh.materials);assert len(slots)==len(original.materials)
 for slot,ref in zip(slots,original.materials):slot.material_interface=ref.material_interface
 mesh.materials=slots
 # All full poses, including observation, must remain renderable at any heading.
 # Enlarged culling bounds have no collision or world-size effect.
 mesh.set_editor_property('positive_bounds_extension',unreal.Vector(45,180,230));mesh.set_editor_property('negative_bounds_extension',unreal.Vector(45,180,35));save(sk);save(mesh);clips={}
 for role in ['SwimIdle','SwimSlow','SwimNormal','SwimFast','SwimTurnLeft','SwimTurnRight','SwimObserve','SwimAttack','SwimHit','SwimFaint','SwimHappy']:
  ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
  clip=next(x for x in task(A/'Exports/WaterV2'/('Garados_'+role+'_V2.fbx'),P+'/Animations','A_Garados_'+role+'_V2',ui)if isinstance(x,unreal.AnimSequence));dest=P+'/Animations/A_Garados_'+role+'_V2'
  if clip.get_path_name().split('.')[0]!=dest:assert unreal.EditorAssetLibrary.rename_asset(clip.get_path_name().split('.')[0],dest);clip=unreal.load_asset(dest)
  clip.set_editor_property('enable_root_motion',False);clips[role]=save(clip)
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
for k,v in dict(swim_mesh=mesh,swim_idle_clip=clips['SwimIdle'],swim_clip=clips['SwimNormal'],swim_slow_clip=clips['SwimSlow'],swim_fast_clip=clips['SwimFast'],swim_observe_clip=clips['SwimObserve'],swim_turn_left_clip=clips['SwimTurnLeft'],swim_turn_right_clip=clips['SwimTurnRight'],swim_reactions={getattr(unreal.PokeMonsterCreatureClip,n.upper()):clips['Swim'+n]for n in ['Attack','Hit','Faint','Happy']},swim_reference_speed=70.,swim_slow_speed=35.,swim_fast_speed=125.,swim_clearance_radius_cm=400.,swim_submerged_depth_cm=130.,swim_turn_degrees_per_second=35.,swim_observe_blend_seconds=2.5,swim_preview_offset_cm=100.).items():profile.set_editor_property(k,v)
assert profile.mesh==original and {str(k):v.get_path_name()for k,v in profile.clips.items()}==original_clips;assert not profile.get_validation_errors(),profile.get_validation_errors();assert unreal.EditorAssetLibrary.save_loaded_asset(profile,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(D/'Import.json').write_text(json.dumps({'created':created,'presentation':profile.get_path_name(),'unchanged_primary_mesh':original.get_path_name(),'unchanged_primary_clips':original_clips,'water_mesh':mesh.get_path_name(),'water_skeleton':sk.get_path_name(),'bounds':str(mesh.get_bounds().export_text())},indent=2));print('GARADOS_WATER_IMPORTED',len(created))
