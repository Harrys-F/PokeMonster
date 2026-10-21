"""Only new correction assets + explicit species visual bindings; original mesh/profile/rig untouched."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/StarterPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();T=unreal.AssetToolsHelpers.get_asset_tools();w=E.get_editor_world();rows=[];flag=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0')
try:
 for name in ['Zunderlauf','Bisasam']:
  A=R/'Art/Characters/Creatures'/name;audit=json.loads((A/'PolishV2_AnimationAudit.json').read_text());assert hashlib.sha256((R/audit['reference']).read_bytes()).hexdigest()==audit['reference_sha256'];s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);old=s.get_visuals().presentation;sk=old.mesh.skeleton;folder='/Game/Characters/Creatures/'+name+'/PolishV2';isanim=name=='Zunderlauf';assetname='A_Glumanda_Faint'if isanim else'SK_Bisasam_Skin';assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+assetname)
  ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=not isanim,import_as_skeletal=True,import_animations=isanim,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION if isanim else unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
  data=ui.anim_sequence_import_data if isanim else ui.skeletal_mesh_import_data
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.).items():data.set_editor_property(k,v)
  if isanim:
   for k,v in dict(use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():data.set_editor_property(k,v)
  else:
   for k,v in dict(normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,update_skeleton_reference_pose=False,use_t0_as_ref_pose=False).items():data.set_editor_property(k,v)
  task=unreal.AssetImportTask()
  for k,v in dict(filename=str(R/audit['export']),destination_path=folder,destination_name=assetname,automated=True,save=False,replace_existing=False,options=ui).items():task.set_editor_property(k,v)
  T.import_asset_tasks([task]);a=next(x for x in task.get_objects()if isinstance(x,unreal.AnimSequence if isanim else unreal.SkeletalMesh))
  if a.get_path_name().split('.')[0]!=folder+'/'+assetname:assert unreal.EditorAssetLibrary.rename_asset(a.get_path_name().split('.')[0],folder+'/'+assetname);a=unreal.load_asset(folder+'/'+assetname)
  assert(a.get_skeleton()if isanim else a.skeleton)==sk
  if isanim:a.set_editor_property('enable_root_motion',False);assert abs(a.get_play_length()-1.1)<.001
  else:
   slots=list(a.materials);assert len(slots)==len(old.mesh.materials)
   for x,y in zip(slots,old.mesh.materials):x.material_interface=y.material_interface
   a.materials=slots
  assert unreal.EditorAssetLibrary.save_loaded_asset(a,False)
  profile=unreal.EditorAssetLibrary.duplicate_asset(old.get_path_name(),folder+'/DA_'+name+'_Presentation');assert profile
  if isanim:clips=dict(profile.clips);clips[unreal.PokeMonsterCreatureClip.FAINT]=a;profile.set_editor_property('clips',clips)
  else:profile.set_editor_property('mesh',a)
  assert not profile.get_validation_errors();assert unreal.EditorAssetLibrary.save_loaded_asset(profile,False);visual=s.get_visuals();visual.set_editor_property('presentation',profile);s.set_editor_property('visuals',visual);assert unreal.EditorAssetLibrary.save_loaded_asset(s,False);rows.append({'species':name,'original_profile':old.get_path_name(),'profile':profile.get_path_name(),'asset':a.get_path_name(),'skeleton_compatible':True,'original_materials':True,'height_cm':profile.reference_size_cm})
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(flag))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()];(O/'ImportCorrections.json').write_text(json.dumps(rows,indent=2))
