"""Candidate-only import. No species/map binding or original reimport."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();A=R/'Art/Characters/Creatures/Zunderlauf';O=R/'Saved/MeshyGlumandaV1';P='/Game/Characters/Creatures/Zunderlauf/MeshyV1';assert not (O/'Import.json').exists();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;created=[]
def save(o):assert o.get_path_name().startswith(P+'/');assert unreal.EditorAssetLibrary.save_loaded_asset(o,False);created.append(o.get_path_name());return o
def task(path,folder,name,options=None):
 dest=P+'/'+folder+'/'+name
 if unreal.EditorAssetLibrary.does_asset_exist(dest):
  a=unreal.load_asset(dest);assert str(path) in a.get_editor_property('asset_import_data').extract_filenames()
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(path),'destination_path':P+'/'+folder,'destination_name':name,'automated':True,'save':False,'replace_existing':unreal.EditorAssetLibrary.does_asset_exist(dest)}.items():t.set_editor_property(k,v)
 if options:t.options=options
 T.import_asset_tasks([t]);return list(t.get_objects())
def node(m,cls,**props):
 n=L.create_material_expression(m,cls)
 for k,v in props.items():n.set_editor_property(k,v)
 return n
def material(name,tex,fire=False):
 m=unreal.load_asset(P+'/Materials/'+name) or T.create_asset(name,P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());L.delete_all_material_expressions(m);m.set_editor_property('two_sided',True);m.set_editor_property('used_with_skeletal_mesh',not fire)
 n={}
 for typ,sampler in [('BaseColor',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR),('Normal',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL),('MetallicRoughness',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)]:n[typ]=node(m,unreal.MaterialExpressionTextureSample,texture=tex[typ],sampler_type=sampler)
 for typ,channel,prop in [('BaseColor','RGB',unreal.MaterialProperty.MP_BASE_COLOR),('Normal','RGB',unreal.MaterialProperty.MP_NORMAL),('MetallicRoughness','G',unreal.MaterialProperty.MP_ROUGHNESS),('MetallicRoughness','B',unreal.MaterialProperty.MP_METALLIC)]:assert L.connect_material_property(n[typ],channel,prop)
 if fire:
  mult=node(m,unreal.MaterialExpressionMultiply,const_b=.65);assert L.connect_material_expressions(n['BaseColor'],'RGB',mult,'A');assert L.connect_material_property(mult,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
  # Existing V1's inexpensive time/sine movement, masked by original flame vertex height baked into vertex color.
  time=node(m,unreal.MaterialExpressionTime);sine=node(m,unreal.MaterialExpressionSine,period=1.8);L.connect_material_expressions(time,'',sine,'')
  direction=node(m,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(.12,.12,0,1));wave=node(m,unreal.MaterialExpressionMultiply);L.connect_material_expressions(sine,'',wave,'A');L.connect_material_expressions(direction,'',wave,'B');color=node(m,unreal.MaterialExpressionVertexColor);masked=node(m,unreal.MaterialExpressionMultiply);L.connect_material_expressions(wave,'',masked,'A');L.connect_material_expressions(color,'R',masked,'B');L.connect_material_property(masked,'',unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
 L.recompile_material(m);return save(m)
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0')
try:
 tex={}
 for typ in ['BaseColor','Normal','MetallicRoughness']:
  a=next(a for a in task(A/'Textures/MeshyV1'/('Glumanda_'+typ+'.jpg'),'Textures','T_Glumanda_'+typ)if isinstance(a,unreal.Texture2D))
  a.set_editor_property('srgb',typ=='BaseColor')
  if typ=='Normal':a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);a.set_editor_property('flip_green_channel',True)
  if typ=='MetallicRoughness':a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
  tex[typ]=save(a)
 mat=material('M_Glumanda',tex);fm=material('M_GlumandaTailFlame',tex,True)
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH,'create_physics_asset':False}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 if unreal.EditorAssetLibrary.does_asset_exist(P+'/Meshes/SK_Glumanda_Meshy'):ui.skeleton=unreal.load_asset(P+'/Meshes/SK_Glumanda_Meshy').skeleton
 mesh=next(a for a in task(A/'Exports/MeshyV1/Glumanda_Idle.fbx','Meshes','SK_Glumanda_Meshy',ui)if isinstance(a,unreal.SkeletalMesh));sk=mesh.skeleton;slots=list(mesh.materials)
 for slot in slots:slot.material_interface=mat
 mesh.materials=slots;save(sk);save(mesh);clips={}
 for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
  ui=unreal.FbxImportUI()
  for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':sk,'override_full_name':True}.items():ui.set_editor_property(k,v)
  for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':30,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
  clip=next(a for a in task(A/'Exports/MeshyV1'/('Glumanda_'+role+'.fbx'),'Animations','A_Glumanda_'+role,ui)if isinstance(a,unreal.AnimSequence));dest=P+'/Animations/A_Glumanda_'+role
  if clip.get_path_name().split('.')[0]!=dest:assert unreal.EditorAssetLibrary.rename_asset(clip.get_path_name().split('.')[0],dest);clip=unreal.load_asset(dest)
  clip.set_editor_property('enable_root_motion',False);clips[getattr(unreal.PokeMonsterCreatureClip,role.upper())]=save(clip)
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_as_skeletal':False,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'auto_generate_collision':False,'vertex_color_import_option':unreal.VertexColorImportOption.REPLACE,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 fire=next(a for a in task(A/'Exports/MeshyV1/Glumanda_TailFlame.fbx','Meshes','SM_GlumandaTailFlame',ui)if isinstance(a,unreal.StaticMesh));save(fire)
 pose=unreal.AnimPoseExtensions.get_reference_pose(sk);transform=unreal.AnimPoseExtensions.get_bone_pose(pose,'tail_socket',unreal.AnimPoseSpaces.WORLD);assert transform.translation.length()>20,transform
 anchor=unreal.PokeMonsterCreatureEffectAnchor();anchor.set_editor_property('id','TailTipFX');anchor.set_editor_property('socket','tail_socket');anchor.set_editor_property('mesh',fire);anchor.set_editor_property('material',fm);anchor.set_editor_property('offset',unreal.Transform(rotation=transform.rotation.inversed().rotator(),scale=unreal.Vector(1/transform.scale3d.x,1/transform.scale3d.y,1/transform.scale3d.z)));anchor.set_editor_property('world_upright',False)
 factory=unreal.DataAssetFactory();factory.set_editor_property('data_asset_class',unreal.PokeMonsterCreaturePresentationData);data=T.create_asset('DA_Glumanda_Presentation',P,unreal.PokeMonsterCreaturePresentationData,factory)
 for k,v in {'mesh':mesh,'clips':clips,'walk_speed':22.,'run_speed':36.,'ground_offset_cm':-.04,'rig_family':unreal.PokeMonsterCreatureRigFamily.BIPED,'reference_size_cm':60.,'size_source':'https://ph.portal-pokemon.com/pokedex/0004/','effect_anchors':[anchor]}.items():data.set_editor_property(k,v)
 assert not data.get_validation_errors(),list(data.get_validation_errors());save(data)
 (O/'Import.json').write_text(json.dumps({'assets':created,'candidate':data.get_path_name(),'skeleton':sk.get_path_name(),'socket_ref_location_cm':transform.translation.to_tuple(),'socket_ref_rotation':str(transform.rotation),'source_texture_channels':'glTF G=Roughness, B=Metallic; normal OpenGL -> flip G','no_species_binding':True,'no_map_save':True},indent=2));unreal.log('MESHY_GLUMANDA_CANDIDATE_IMPORT_PASS')
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(old))
