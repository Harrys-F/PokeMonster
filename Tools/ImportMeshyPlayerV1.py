"""Import the reviewed, rigged Meshy copy into its own player asset folder."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/MeshyPlayerV1';D='/Game/Characters/YoungTrainer/MeshyV1'
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()
T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary
unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
def task(filename,folder,name,options=None):
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(filename),'destination_path':D+'/'+folder,'destination_name':name,'automated':True,'save':False,'replace_existing':True,'replace_existing_settings':True}.items():t.set_editor_property(k,v)
 if options:t.options=options
 T.import_asset_tasks([t]);assert t.imported_object_paths, filename
 return [unreal.load_asset(p) for p in t.imported_object_paths]
textures={}
for label in ['BaseColor','ORM','Normal']:
 n='T_Player_Meshy_'+label;tex=task(R/'Art/Characters/YoungTrainer/Textures/MeshyV1'/(n+'.png'),'Textures',n)[0]
 tex.srgb=label=='BaseColor';tex.max_texture_size=2048
 if label=='Normal':
  tex.compression_settings=unreal.TextureCompressionSettings.TC_NORMALMAP;tex.set_editor_property('flip_green_channel',True)
 elif label=='ORM':tex.compression_settings=unreal.TextureCompressionSettings.TC_MASKS
 textures[label]=tex;unreal.EditorAssetLibrary.save_loaded_asset(tex,False)
m=unreal.load_asset(D+'/Materials/M_Player_Meshy') or T.create_asset('M_Player_Meshy',D+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
if not unreal.EditorAssetLibrary.get_metadata_tag(m,'MeshyV1Ready'):
 for label,prop in [('BaseColor',unreal.MaterialProperty.MP_BASE_COLOR),('Normal',unreal.MaterialProperty.MP_NORMAL)]:
  n=L.create_material_expression(m,unreal.MaterialExpressionTextureSample,-450,0 if label=='BaseColor' else 200);n.texture=textures[label]
  if label=='Normal':n.sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL
  L.connect_material_property(n,'RGB',prop)
 n=L.create_material_expression(m,unreal.MaterialExpressionTextureSample,-450,400);n.texture=textures['ORM'];n.sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_MASKS
 for channel,prop in [('R',unreal.MaterialProperty.MP_AMBIENT_OCCLUSION),('G',unreal.MaterialProperty.MP_ROUGHNESS),('B',unreal.MaterialProperty.MP_METALLIC)]:L.connect_material_property(n,channel,prop)
 L.recompile_material(m);unreal.EditorAssetLibrary.set_metadata_tag(m,'MeshyV1Ready','true')
unreal.EditorAssetLibrary.save_loaded_asset(m,False)
# Calibrate only the new player material for the existing bright Overworld light.
# Source paint stays unchanged; Blender/OpenGL normal green is converted for Unreal.
if not unreal.EditorAssetLibrary.get_metadata_tag(m,'MeshyPaletteCalibration'):
 paint=next(o for o in unreal.ObjectIterator(unreal.MaterialExpressionTextureSample) if o.get_outer()==m and o.texture and o.texture.get_name()=='T_Player_Meshy_BaseColor')
 multiply=L.create_material_expression(m,unreal.MaterialExpressionMultiply,-120,0)
 scale=L.create_material_expression(m,unreal.MaterialExpressionScalarParameter,-450,-150);scale.set_editor_property('parameter_name','AlbedoScale');scale.set_editor_property('default_value',.35)
 L.connect_material_expressions(paint,'RGB',multiply,'A');L.connect_material_expressions(scale,'',multiply,'B');L.connect_material_property(multiply,'',unreal.MaterialProperty.MP_BASE_COLOR)
 L.recompile_material(m);unreal.EditorAssetLibrary.set_metadata_tag(m,'MeshyPaletteCalibration','0.35: player-only palette integration')
 unreal.EditorAssetLibrary.save_loaded_asset(m,False)
ui=unreal.FbxImportUI()
for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'create_physics_asset':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH}.items():ui.set_editor_property(k,v)
for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE,'use_t0_as_ref_pose':False,'update_skeleton_reference_pose':False}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
objects=task(R/'Art/Characters/YoungTrainer/Exports/MeshyV1/SK_Player_Meshy.fbx','Meshes','SK_Player_Meshy',ui)
mesh=next(o for o in objects if isinstance(o,unreal.SkeletalMesh));skeleton=mesh.skeleton
slots=list(mesh.materials);assert len(slots)==1;slots[0].material_interface=m;mesh.materials=slots
unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);unreal.EditorAssetLibrary.save_loaded_asset(skeleton,False)
clips=[]
for n in ['A_Player_Meshy_Idle','A_Player_Meshy_Walk']:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':skeleton,'override_full_name':True}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':30,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
 objects=task(R/'Art/Characters/YoungTrainer/Exports/MeshyV1'/(n+'.fbx'),'Animations',n,ui)
 a=next(o for o in objects if isinstance(o,unreal.AnimSequence));a.set_editor_property('enable_root_motion',False)
 # Normalize importer-generated names for stable native defaults.
 target=D+'/Animations/'+n
 if a.get_path_name().split('.')[0]!=target:
  assert unreal.EditorAssetLibrary.rename_asset(a.get_path_name().split('.')[0],target)
 a=unreal.load_asset(target);unreal.EditorAssetLibrary.save_loaded_asset(a,False)
 clips.append({'path':a.get_path_name(),'seconds':a.get_play_length()})
(O/'ImportAudit.json').write_text(json.dumps({'mesh':mesh.get_path_name(),'skeleton':skeleton.get_path_name(),'clips':clips,'material':m.get_path_name(),'textures':{k:t.get_path_name() for k,t in textures.items()}},indent=2))
unreal.log('MESHY_PLAYER_IMPORT_COMPLETE')
