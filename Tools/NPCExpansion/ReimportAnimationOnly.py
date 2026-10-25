"""Reimport only this task's library animations after removing repeated mesh geometry from FBX."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();P='/Game/Characters/NPCs/Library';rows=[];old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
try:
 for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
  id=a['id'];C=R/'Art/Characters/NPCs'/id if id!='HobbitBase' else R/'Art/Characters/NPCs/Westland/HobbitBase';profile=unreal.load_asset(P+'/Profiles/DA_NPC_'+id);model=unreal.load_asset(a['reuse_mesh']) if a.get('reuse_mesh') else profile.mesh;skeleton=model.skeleton;audit=json.loads((R/'Saved/ProjectRefinement/NPCExpansion/AnimationViews'/id/'Audit.json').read_text())
  for c in audit['clips']:
   path=P+'/'+id+'/Animations/'+('SharedSkeleton/' if a.get('reuse_mesh') else '')+c['name'];anim=unreal.load_asset(path);assert anim and path.startswith(P+'/');before=anim.get_play_length();ui=unreal.FbxImportUI()
   for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':skeleton,'override_full_name':True}.items():ui.set_editor_property(k,v)
   for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':30,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
   t=unreal.AssetImportTask()
   for k,v in {'filename':str(C/'Exports/Library'/(c['name']+'.fbx')),'destination_path':path.rsplit('/',1)[0],'destination_name':c['name'],'automated':True,'save':False,'replace_existing':True,'replace_existing_settings':True,'options':ui}.items():t.set_editor_property(k,v)
   unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);assert anim.get_play_length()==before,(id,c['name']);anim.set_editor_property('enable_root_motion',False);unreal.EditorAssetLibrary.save_loaded_asset(anim,False);rows.append({'clip':path,'seconds_before':before,'seconds_after':anim.get_play_length(),'animation_only_source':True})
  profile.set_editor_property('mesh',model);assert not list(profile.get_validation_errors());unreal.EditorAssetLibrary.save_loaded_asset(profile,False)
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
(R/'Saved/ProjectRefinement/NPCExpansion/AnimationOnlyReimport.json').write_text(json.dumps(rows,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
