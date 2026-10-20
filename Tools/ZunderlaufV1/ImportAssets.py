"""Explicit imports of this creature only; no original asset, player or map is reimported."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();A=R/'Art/Characters/Creatures/Zunderlauf';O=R/'Saved/ZunderlaufV1';P='/Game/Characters/Creatures/Zunderlauf';T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world()
# A failed first import may resume only its own, path-checked assets.
assert (O/'ImportStarted.json').exists() or not unreal.EditorAssetLibrary.does_asset_exist(P+'/Meshes/SK_Zunderlauf')
(O/'ImportStarted.json').write_text(json.dumps({'source':str(A),'namespace':P}))
assert not (O/'Import.json').exists(),'Completed first import: use the explicit own mesh refresh, not another import'
created=[]
def save(o):assert unreal.EditorAssetLibrary.save_loaded_asset(o,False);created.append(o.get_path_name());return o
def task(path,folder,name,options=None):
 existing=unreal.load_asset(P+'/'+folder+'/'+name) if unreal.EditorAssetLibrary.does_asset_exist(P+'/'+folder+'/'+name) else None
 if existing:
  imports=existing.get_editor_property('asset_import_data').extract_filenames();assert str(path) in imports,(existing.get_path_name(),imports);return [existing]
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(path),'destination_path':P+'/'+folder,'destination_name':name,'automated':True,'save':False,'replace_existing':False}.items():t.set_editor_property(k,v)
 if options:t.options=options
 T.import_asset_tasks([t]);return list(t.get_objects())
def node(m,cls,**props):
 n=L.create_material_expression(m,cls)
 for k,v in props.items():n.set_editor_property(k,v)
 return n
def link(a,b,socket,out=''):assert L.connect_material_expressions(a,out,b,socket)
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0')
try:
 tex={}
 for typ in ['DIFFUSE','NORMAL','ROUGHNESS']:
  texture=next(x for x in task(A/'Textures'/('Zunderlauf_'+typ+'.png'),'Textures','T_Zunderlauf_'+typ)if isinstance(x,unreal.Texture2D))
  if typ!='DIFFUSE':texture.set_editor_property('srgb',False)
  if typ=='NORMAL':texture.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);texture.set_editor_property('flip_green_channel',True)
  if typ=='ROUGHNESS':texture.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
  tex[typ]=save(texture)
 mat=unreal.load_asset(P+'/Materials/M_Zunderlauf') or T.create_asset('M_Zunderlauf',P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());L.delete_all_material_expressions(mat);mat.set_editor_property('used_with_skeletal_mesh',True)
 for typ,prop,sampler in [('DIFFUSE',unreal.MaterialProperty.MP_BASE_COLOR,unreal.MaterialSamplerType.SAMPLERTYPE_COLOR),('NORMAL',unreal.MaterialProperty.MP_NORMAL,unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL),('ROUGHNESS',unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)]:
  n=node(mat,unreal.MaterialExpressionTextureSample,texture=tex[typ],sampler_type=sampler);assert L.connect_material_property(n,'R'if typ=='ROUGHNESS'else'RGB',prop)
 spec=node(mat,unreal.MaterialExpressionConstant,r=.32);L.connect_material_property(spec,'',unreal.MaterialProperty.MP_SPECULAR);L.recompile_material(mat);save(mat)
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH,'create_physics_asset':False}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 mesh=next(x for x in task(A/'Exports/Zunderlauf_Idle.fbx','Meshes','SK_Zunderlauf',ui)if isinstance(x,unreal.SkeletalMesh));sk=mesh.skeleton
 slots=list(mesh.materials)
 for slot in slots:slot.material_interface=mat
 mesh.materials=slots;save(sk);save(mesh)
 clips={};clipaudit=[]
 for name in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
  ui=unreal.FbxImportUI()
  for k,v in {'import_mesh':False,'import_as_skeletal':True,'import_animations':True,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_ANIMATION,'skeleton':sk,'override_full_name':True}.items():ui.set_editor_property(k,v)
  for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'use_default_sample_rate':False,'custom_sample_rate':30,'animation_length':unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME}.items():ui.anim_sequence_import_data.set_editor_property(k,v)
  clip=next(x for x in task(A/'Exports'/('Zunderlauf_'+name+'.fbx'),'Animations','A_Zunderlauf_'+name,ui)if isinstance(x,unreal.AnimSequence));target=P+'/Animations/A_Zunderlauf_'+name
  if clip.get_path_name().split('.')[0]!=target:assert unreal.EditorAssetLibrary.rename_asset(clip.get_path_name().split('.')[0],target);clip=unreal.load_asset(target)
  clip.set_editor_property('enable_root_motion',False);clips[getattr(unreal.PokeMonsterCreatureClip,name.upper())]=save(clip);clipaudit.append({'name':name,'path':clip.get_path_name(),'seconds':clip.get_play_length()})
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_as_skeletal':False,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(k,v)
 ui.static_mesh_import_data.set_editor_property('convert_scene_unit',True);ui.static_mesh_import_data.set_editor_property('auto_generate_collision',False)
 fire=next(x for x in task(A/'Exports/Zunderlauf_TailFlame.fbx','Meshes','SM_TailFlame',ui)if isinstance(x,unreal.StaticMesh));save(fire)
 fm=unreal.load_asset(P+'/Materials/M_TailFlame') or T.create_asset('M_TailFlame',P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());L.delete_all_material_expressions(fm);fm.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT)
 fres=node(fm,unreal.MaterialExpressionFresnel);core=node(fm,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(4.5,2.5,.20,1));edge=node(fm,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(2.5,.21,.018,1));lerp=node(fm,unreal.MaterialExpressionLinearInterpolate);link(core,lerp,'A');link(edge,lerp,'B');link(fres,lerp,'Alpha');L.connect_material_property(lerp,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
 # A few millimetres of vertex movement, opaque 3D silhouette, no particle system or translucent overdraw.
 time=node(fm,unreal.MaterialExpressionTime);sin=node(fm,unreal.MaterialExpressionSine,period=1.8);link(time,sin,'');axis=node(fm,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(.38,.22,0,1));mul=node(fm,unreal.MaterialExpressionMultiply);link(axis,mul,'A');link(sin,mul,'B');L.connect_material_property(mul,'',unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET);L.recompile_material(fm);save(fm)
 factory=unreal.DataAssetFactory();factory.set_editor_property('data_asset_class',unreal.PokeMonsterCreaturePresentationData)
 data=T.create_asset('DA_Zunderlauf_Presentation',P,unreal.PokeMonsterCreaturePresentationData,factory)
 for k,v in {'mesh':mesh,'clips':clips,'walk_speed':35.,'run_speed':60.,'ground_offset_cm':.71433,'tail_flame':fire,'flame_material':fm,'flame_bone':'tail_socket'}.items():data.set_editor_property(k,v)
 save(data)
 assert not unreal.EditorAssetLibrary.does_asset_exist('/Game/Data/Creatures/DA_Zunderlauf')
 species=unreal.EditorAssetLibrary.duplicate_asset('/Game/Data/Creatures/DA_TestFire','/Game/Data/Creatures/DA_Zunderlauf');species.set_editor_property('internal_id','Zunderlauf');species.set_editor_property('display_name','Zunderlauf');vis=species.get_editor_property('visuals');vis.set_editor_property('presentation',data);species.set_editor_property('visuals',vis);save(species)
 factory=unreal.DataAssetFactory();factory.set_editor_property('data_asset_class',unreal.PokeMonsterEncounterProfile)
 profile=T.create_asset('DA_Zunderlauf_Wild','/Game/Data/Encounters',unreal.PokeMonsterEncounterProfile,factory)
 oldprofile=unreal.load_asset('/Game/Data/Encounters/DA_DevWild');entries=list(oldprofile.get_editor_property('entries'));entry=next(e for e in entries if 'TestFire' in str(e.get_editor_property('species')));entry.set_editor_property('species',species);entry.set_editor_property('weight',1);profile.set_editor_property('entries',[entry]);save(profile)
 (O/'Import.json').write_text(json.dumps({'assets':created,'clips':clipaudit,'material_slots':len(slots),'source':str(A),'balance':'DA_TestFire copied unchanged except identity and optional visuals','no_physics_asset':mesh.get_editor_property('physics_asset') is None,'map_changed':False},indent=2));unreal.log('ZUNDERLAUF_IMPORT_PASS')
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(old))
