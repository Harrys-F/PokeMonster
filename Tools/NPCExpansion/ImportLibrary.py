"""Add only missing library assets. Shared original textures/materials remain untouched."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();T=unreal.AssetToolsHelpers.get_asset_tools();P='/Game/Characters/NPCs/Library';results=[]
def task(file,folder,name,ui=None):
 path=P+'/'+folder+'/'+name
 if unreal.EditorAssetLibrary.does_asset_exist(path):return [unreal.load_asset(path)]
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(file),'destination_path':P+'/'+folder,'destination_name':name,'automated':True,'save':False,'replace_existing':False}.items():t.set_editor_property(k,v)
 if ui:t.options=ui
 T.import_asset_tasks([t]);objects=list(t.get_objects());assert objects,(file,t.imported_object_paths);return objects
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
  id=a['id'];C=R/'Art/Characters/NPCs'/id if id!='HobbitBase' else R/'Art/Characters/NPCs/Westland/HobbitBase';exports=C/'Exports/Library';audit=json.loads((O/'AnimationViews'/id/'Audit.json').read_text())
  if id=='HobbitBase':
   textures={}
   for role,suffix in [('BaseColor','BaseColor'),('Normal','Normal'),('MetalRough','ORM')]:
    tex=task(C/'Textures/MeshyBaseV2'/('T_Hobbit_MeshyBase_V2_'+suffix+'.png'),id+'/Textures','T_HobbitBase_'+role)[0];tex.srgb=role=='BaseColor'
    if role=='Normal':tex.compression_settings=unreal.TextureCompressionSettings.TC_NORMALMAP;tex.set_editor_property('flip_green_channel',True)
    elif role=='MetalRough':tex.compression_settings=unreal.TextureCompressionSettings.TC_MASKS
    unreal.EditorAssetLibrary.save_loaded_asset(tex,False);textures[role]=tex
   name='MI_HobbitBase_Original';path=P+'/'+id+'/Materials/'+name
   mi=unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else T.create_asset(name,P+'/'+id+'/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
   unreal.MaterialEditingLibrary.set_material_instance_parent(mi,unreal.load_asset('/Game/Characters/NPCs/Shared/Materials/M_NPC_MeshyBase_V1'))
   for k,v in textures.items():unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi,k,v)
   unreal.MaterialEditingLibrary.update_material_instance(mi);unreal.EditorAssetLibrary.save_loaded_asset(mi,False)
  else:mi=unreal.load_asset('/Game/Characters/NPCs/'+id+'/Materials/MI_'+id+'_V1');assert mi
  if a.get('reuse_mesh'):mesh=unreal.load_asset(a['reuse_mesh'])
  elif id=='SilverLady':mesh=unreal.load_asset('/Game/Characters/NPCs/SilverLady/HealerArtV4/Meshes/SK_WestlandHealer_ArtV4')
  else:
   ui=unreal.FbxImportUI()
   for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH,'create_physics_asset':False}.items():ui.set_editor_property(k,v)
   for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
   mesh=next(x for x in task(exports/('SK_'+id+'_Library.fbx'),id+'/Meshes','SK_'+id+'_Library',ui) if isinstance(x,unreal.SkeletalMesh));slots=list(mesh.materials);assert len(slots)==1;slots[0].material_interface=mi;mesh.materials=slots;unreal.EditorAssetLibrary.save_loaded_asset(mesh.skeleton,False);unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
  skeleton=mesh.skeleton;clips={}
  for clip in audit['clips']:
   ui=unreal.FbxImportUI()
   for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':skeleton,'override_full_name':True}.items():ui.set_editor_property(k,v)
   for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':30,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
   name=clip['name'];anim=next(x for x in task(exports/(name+'.fbx'),id+'/Animations'+('/SharedSkeleton' if a.get('reuse_mesh') else ''),name,ui) if isinstance(x,unreal.AnimSequence));target=P+'/'+id+'/Animations/'+('SharedSkeleton/' if a.get('reuse_mesh') else '')+name
   if anim.get_path_name().split('.')[0]!=target:assert unreal.EditorAssetLibrary.rename_asset(anim.get_path_name().split('.')[0],target)
   anim=unreal.load_asset(target);anim.set_editor_property('enable_root_motion',False);unreal.EditorAssetLibrary.save_loaded_asset(anim,False);clips[clip['role']]=anim
  name='DA_NPC_'+id;path=P+'/Profiles/'+name;profile=unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else T.create_asset(name,P+'/Profiles',unreal.PokeMonsterNPCPresentationData,unreal.DataAssetFactory())
  for k,v in {'technical_id':id,'original_source':audit['source'],'limitations':audit['limitations'],'mesh':mesh,'materials':[mi],'reference_height_cm':a['height']*100,'walk_speed':a['walk'],'run_speed':a['run'],'bFootContacts':not a.get('rooted') and not a.get('simple'),'bAccessoryMotion':a['cape'] and not a.get('simple')}.items():profile.set_editor_property(k,v)
  for k,role in [('idle','Idle'),('walk','Walk'),('run','Run'),('talk','Talk'),('greeting','Greet'),('turn_left','TurnLeft'),('turn_right','TurnRight')]:profile.set_editor_property(k,clips.get(role))
  errors=list(profile.get_validation_errors());assert not errors,(id,errors);unreal.EditorAssetLibrary.save_loaded_asset(profile,False)
  results.append({'id':id,'mesh':mesh.get_path_name(),'profile':profile.get_path_name(),'skeleton':skeleton.get_path_name(),'clips':{k:v.get_path_name() for k,v in clips.items()},'material':mi.get_path_name(),'validation_errors':errors,'height_cm':a['height']*100,'limits':audit['limitations']});(O/'Imported.json').write_text(json.dumps(results,indent=2));unreal.log('PM_NPC_LIBRARY_IMPORTED '+id)
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
