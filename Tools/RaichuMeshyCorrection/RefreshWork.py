"""Refresh ONLY this run's uncommitted Raichu candidate, after final weight smoothing."""
import unreal,json,subprocess,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/RaichuMeshyCorrection';assert not subprocess.check_output(['git','ls-files','--','Content/Characters/Creatures/Raichu/MeshyV1'],cwd=R).strip();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();w=E.get_editor_world();P='/Game/Characters/Creatures/Raichu/MeshyV1';profile=unreal.load_asset(P+'/DA_Raichu_Meshy_Presentation');mesh=profile.mesh;sk=mesh.skeleton;A=R/'Art/Characters/Creatures/Raichu/Exports/MeshyV1';T=unreal.AssetToolsHelpers.get_asset_tools();old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0');rows=[]
try:
 for role in ['Mesh','Idle','Walk','Run','Attack','Hit','Faint','Happy']:
  obj=mesh if role=='Mesh'else profile.clips[getattr(unreal.PokeMonsterCreatureClip,role.upper())];path=obj.get_path_name().split('.')[0];source=A/('Raichu_'+('Idle'if role=='Mesh'else role)+'.fbx');ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=role=='Mesh',import_as_skeletal=True,import_animations=role!='Mesh',import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH if role=='Mesh'else unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,create_physics_asset=False,override_full_name=True).items():ui.set_editor_property(k,v)
  data=ui.skeletal_mesh_import_data if role=='Mesh'else ui.anim_sequence_import_data
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.).items():data.set_editor_property(k,v)
  if role=='Mesh':
   data.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS;data.set_editor_property('update_skeleton_reference_pose',True);data.set_editor_property('use_t0_as_ref_pose',False)
  else:
   data.set_editor_property('use_default_sample_rate',False);data.set_editor_property('custom_sample_rate',30);data.set_editor_property('animation_length',unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
  task=unreal.AssetImportTask()
  for k,v in dict(filename=str(source),destination_path=path.rsplit('/',1)[0],destination_name=path.rsplit('/',1)[1],options=ui,replace_existing=True,automated=True,save=False).items():task.set_editor_property(k,v)
  T.import_asset_tasks([task]);assets=list(task.get_objects());assert obj in assets,(role,[x.get_path_name()for x in assets]);assert unreal.EditorAssetLibrary.save_loaded_asset(obj,False);rows.append({'role':role,'path':path,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
 slots=list(mesh.materials)
 for slot in slots:slot.material_interface=unreal.load_asset(P+'/Materials/M_Raichu_Meshy')
 mesh.materials=slots;assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
 assert unreal.EditorAssetLibrary.save_loaded_asset(sk,False);assert not profile.get_validation_errors();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(O/'RaichuFinalRefresh.json').write_text(json.dumps(rows,indent=2))
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(old))
