import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();I=R/'Art/Characters/NPCs/IntegrationV1';req=json.loads((I/'ImportRequest.json').read_text());id=req['id'];kind=req['kind'];C=R/'Art/Characters/NPCs'/id;D='/Game/Characters/NPCs/'+id
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary
old_interchange=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
def task(filename,folder,name,options=None):
 path=D+'/'+folder+'/'+name
 if unreal.EditorAssetLibrary.does_asset_exist(path):return [unreal.load_asset(path)]
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(filename),'destination_path':D+'/'+folder,'destination_name':name,'automated':True,'save':False,'replace_existing':False}.items():t.set_editor_property(k,v)
 if options:t.options=options
 T.import_asset_tasks([t]);assert t.imported_object_paths,str(filename)
 return [unreal.load_asset(p) for p in t.imported_object_paths]
bind=json.loads((I/(id+'_MaterialBindings.json')).read_text());tex={}
for role,key in [('BaseColor','Base Color'),('Normal','Normal'),('MetalRough','Roughness')]:
 f=Path(bind[key]).resolve();assert f.is_file();a=task(f,'Textures','T_'+id+'_'+role)[0];assert isinstance(a,unreal.Texture2D)
 a.srgb=role=='BaseColor';a.max_texture_size=2048
 if role=='Normal':a.compression_settings=unreal.TextureCompressionSettings.TC_NORMALMAP;a.set_editor_property('flip_green_channel',True)
 elif role=='MetalRough':a.compression_settings=unreal.TextureCompressionSettings.TC_MASKS
 tex[role]=a;unreal.EditorAssetLibrary.save_loaded_asset(a,False)
shared='/Game/Characters/NPCs/Shared/Materials/M_NPC_MeshyBase_V1';master=unreal.load_asset(shared) if unreal.EditorAssetLibrary.does_asset_exist(shared) else None
if not master:
 master=T.create_asset('M_NPC_MeshyBase_V1','/Game/Characters/NPCs/Shared/Materials',unreal.Material,unreal.MaterialFactoryNew())
if unreal.EditorAssetLibrary.get_metadata_tag(master,'NPCIntegrationComplete')!='1':
 L.delete_all_material_expressions(master);master.set_editor_property('two_sided',True)
 nodes={}
 for j,role in enumerate(['BaseColor','Normal','MetalRough']):
  n=L.create_material_expression(master,unreal.MaterialExpressionTextureSampleParameter2D,-450,j*220);n.set_editor_property('parameter_name',role);n.set_editor_property('texture',tex[role])
  n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL if role=='Normal' else unreal.MaterialSamplerType.SAMPLERTYPE_MASKS if role=='MetalRough' else unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);nodes[role]=n
 L.connect_material_property(nodes['BaseColor'],'RGB',unreal.MaterialProperty.MP_BASE_COLOR);L.connect_material_property(nodes['Normal'],'RGB',unreal.MaterialProperty.MP_NORMAL);L.connect_material_property(nodes['MetalRough'],'G',unreal.MaterialProperty.MP_ROUGHNESS);L.connect_material_property(nodes['MetalRough'],'B',unreal.MaterialProperty.MP_METALLIC);L.recompile_material(master);unreal.EditorAssetLibrary.set_metadata_tag(master,'NPCIntegrationComplete','1');unreal.EditorAssetLibrary.save_loaded_asset(master,False)
mi_path=D+'/Materials/MI_'+id+'_V1';mi=unreal.load_asset(mi_path) if unreal.EditorAssetLibrary.does_asset_exist(mi_path) else T.create_asset('MI_'+id+'_V1',D+'/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
master.set_editor_property('used_with_skeletal_mesh',True);L.recompile_material(master);unreal.EditorAssetLibrary.save_loaded_asset(master,False)
L.set_material_instance_parent(mi,master)
for role,a in tex.items():L.set_material_instance_texture_parameter_value(mi,role,a)
L.update_material_instance(mi);unreal.EditorAssetLibrary.save_loaded_asset(mi,False)
ui=unreal.FbxImportUI()
for k,v in {'import_mesh':True,'import_as_skeletal':kind=='skeletal','import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH if kind=='skeletal' else unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(k,v)
if kind=='skeletal':
 ui.set_editor_property('create_physics_asset',False);data=ui.skeletal_mesh_import_data;name='SK_'+id+'_NPC_V1'
else:
 data=ui.static_mesh_import_data;data.set_editor_property('auto_generate_collision',False);data.set_editor_property('combine_meshes',True);name='SM_'+id+'_Reference_V1'
for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():data.set_editor_property(k,v)
objects=task(C/'Exports'/(name+'.fbx'),'Meshes',name,ui);mesh=next(o for o in objects if isinstance(o,unreal.SkeletalMesh if kind=='skeletal' else unreal.StaticMesh))
clips=[]
if kind=='skeletal':
 slots=list(mesh.materials);assert len(slots)==1;slots[0].material_interface=mi;mesh.materials=slots;skeleton=mesh.skeleton;unreal.EditorAssetLibrary.save_loaded_asset(skeleton,False)
 for n in ['A_'+id+'_Idle_V1','A_'+id+'_Talk_V1']:
  ui=unreal.FbxImportUI()
  for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':skeleton,'override_full_name':True}.items():ui.set_editor_property(k,v)
  for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':30,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
  aa=task(C/'Exports'/(n+'.fbx'),'Animations',n,ui);a=next(o for o in aa if isinstance(o,unreal.AnimSequence));target=D+'/Animations/'+n
  if a.get_path_name().split('.')[0]!=target:assert unreal.EditorAssetLibrary.rename_asset(a.get_path_name().split('.')[0],target)
  a=unreal.load_asset(target);a.set_editor_property('enable_root_motion',False);unreal.EditorAssetLibrary.save_loaded_asset(a,False);clips.append({'path':a.get_path_name(),'seconds':a.get_play_length()})
else:mesh.set_material(0,mi)
unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old_interchange))
(I/(id+'_UnrealImport.json')).write_text(json.dumps({'id':id,'kind':kind,'mesh':mesh.get_path_name(),'material':mi.get_path_name(),'textures':{k:v.get_path_name() for k,v in tex.items()},'clips':clips,'physics':'No gameplay collision/physics asset created','dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()]},indent=2));unreal.log('NPC_IMPORT_DONE '+id)
