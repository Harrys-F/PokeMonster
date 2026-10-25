"""Reuse the three existing suitable humanoid meshes/skeletons; create only new role clips."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0');rows=[]
try:
 for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
  if not a.get('reuse_mesh'):continue
  id=a['id'];C=R/'Art/Characters/NPCs'/id;P='/Game/Characters/NPCs/Library/'+id+'/Animations/SharedSkeleton';mesh=unreal.load_asset(a['reuse_mesh']);skeleton=mesh.skeleton;clips={};audit=json.loads((O/'AnimationViews'/id/'Audit.json').read_text())
  for c in audit['clips']:
   name=c['name'];path=P+'/'+name
   if unreal.EditorAssetLibrary.does_asset_exist(path):anim=unreal.load_asset(path)
   else:
    ui=unreal.FbxImportUI()
    for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':skeleton,'override_full_name':True}.items():ui.set_editor_property(k,v)
    for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':30,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
    t=unreal.AssetImportTask()
    for k,v in {'filename':str(C/'Exports/Library'/(name+'.fbx')),'destination_path':P,'destination_name':name,'automated':True,'save':False,'replace_existing':False,'options':ui}.items():t.set_editor_property(k,v)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);anim=next(x for x in t.get_objects()if isinstance(x,unreal.AnimSequence))
    if anim.get_path_name().split('.')[0]!=path:assert unreal.EditorAssetLibrary.rename_asset(anim.get_path_name().split('.')[0],path)
    anim=unreal.load_asset(path);anim.set_editor_property('enable_root_motion',False);unreal.EditorAssetLibrary.save_loaded_asset(anim,False)
   assert anim.get_editor_property('skeleton')==skeleton,(id,name);clips[c['role']]=anim
  profile=unreal.load_asset('/Game/Characters/NPCs/Library/Profiles/DA_NPC_'+id);profile.set_editor_property('mesh',mesh)
  for prop,role in [('idle','Idle'),('walk','Walk'),('run','Run'),('talk','Talk'),('greeting','Greet'),('turn_left','TurnLeft'),('turn_right','TurnRight')]:profile.set_editor_property(prop,clips.get(role))
  assert not list(profile.get_validation_errors());unreal.EditorAssetLibrary.save_loaded_asset(profile,False);rows.append({'id':id,'existing_mesh':mesh.get_path_name(),'existing_skeleton':skeleton.get_path_name(),'new_clips':{k:v.get_path_name()for k,v in clips.items()}})
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
(O/'SharedSkeletonReuse.json').write_text(json.dumps(rows,indent=2))
