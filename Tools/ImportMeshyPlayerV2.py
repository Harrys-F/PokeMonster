"""Import V2 mesh/clips; reuse unchanged V1 textures and material, preserve V1 assets."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/MeshyPlayerMotionV2';D='/Game/Characters/YoungTrainer/MeshyV2'
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()
T=unreal.AssetToolsHelpers.get_asset_tools()
m=unreal.load_asset('/Game/Characters/YoungTrainer/MeshyV1/Materials/M_Player_Meshy');assert m
unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
def task(filename,folder,name,options):
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(filename),'destination_path':D+'/'+folder,'destination_name':name,'automated':True,'save':False,'replace_existing':True,'replace_existing_settings':True}.items():t.set_editor_property(k,v)
 t.options=options;T.import_asset_tasks([t]);assert t.imported_object_paths,filename
 return [unreal.load_asset(p) for p in t.imported_object_paths]
ui=unreal.FbxImportUI()
for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'create_physics_asset':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH}.items():ui.set_editor_property(k,v)
for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE,'use_t0_as_ref_pose':False,'update_skeleton_reference_pose':False}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
objects=task(R/'Art/Characters/YoungTrainer/Exports/MeshyV2/SK_Player_Meshy_V2.fbx','Meshes','SK_Player_Meshy_V2',ui)
mesh=next(o for o in objects if isinstance(o,unreal.SkeletalMesh));skeleton=mesh.skeleton
slots=list(mesh.materials);assert len(slots)==1;slots[0].material_interface=m;mesh.materials=slots
unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);unreal.EditorAssetLibrary.save_loaded_asset(skeleton,False)
clips=[]
for n in ['A_Player_Meshy_Idle_V2','A_Player_Meshy_Walk_V2']:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':skeleton,'override_full_name':True}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':60,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
 objects=task(R/'Art/Characters/YoungTrainer/Exports/MeshyV2'/(n+'.fbx'),'Animations',n,ui)
 a=next(o for o in objects if isinstance(o,unreal.AnimSequence));a.set_editor_property('enable_root_motion',False)
 # Normalize importer-generated names for stable native defaults.
 target=D+'/Animations/'+n
 if a.get_path_name().split('.')[0]!=target:
  assert unreal.EditorAssetLibrary.rename_asset(a.get_path_name().split('.')[0],target)
 a=unreal.load_asset(target);unreal.EditorAssetLibrary.save_loaded_asset(a,False)
 clips.append({'path':a.get_path_name(),'seconds':a.get_play_length()})
(O/'ImportAudit.json').write_text(json.dumps({'mesh':mesh.get_path_name(),'skeleton':skeleton.get_path_name(),'clips':clips,'material':m.get_path_name()},indent=2))
unreal.log('MESHY_V2_IMPORT_COMPLETE')
