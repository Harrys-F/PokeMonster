"""New namespaces only; never reimport original assets or change species automatically."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();assert not __import__('subprocess').check_output(['git','ls-files','--',*[f'Content/Characters/Creatures/{n}/PolishV4' for n in ['Enton','Nebulak','Glurak']]],cwd=R).strip(),'Historical one-time importer must not overwrite released V4 packages';O=R/'Saved/CreaturePolishV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert all('/PolishV4/' in p.get_path_name() and any('/'+n+'/' in p.get_path_name() for n in ['Enton','Nebulak','Glurak']) for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages());w=E.get_editor_world();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;inventory=json.loads((O/'Inventory.json').read_text());rows=[];created=[]
def save(a,P):
 assert a.get_path_name().startswith(P+'/');assert unreal.EditorAssetLibrary.save_loaded_asset(a,False);created.append(a.get_path_name());return a
def node(m,c,**props):
 n=L.create_material_expression(m,c)
 for k,v in props.items():n.set_editor_property(k,v)
 return n
def link(a,out,b,inp):assert L.connect_material_expressions(a,out,b,inp)
def prop(a,out,p):assert L.connect_material_property(a,out,p)
def custom(m,code,inputs,output):
 n=node(m,unreal.MaterialExpressionCustom,code=code,output_type=output);args=[]
 for k in inputs:
  v=unreal.CustomInput();v.set_editor_property('input_name',k);args.append(v)
 n.set_editor_property('inputs',args);return n
def task(file,P,name,ui):
 if unreal.EditorAssetLibrary.does_asset_exist(P+'/'+name):
  a=unreal.load_asset(P+'/'+name);assert str(file) in a.get_editor_property('asset_import_data').extract_filenames();return [a]
 t=unreal.AssetImportTask()
 for k,v in dict(filename=str(file),destination_path=P,destination_name=name,automated=True,save=False,replace_existing=False,options=ui).items():t.set_editor_property(k,v)
 T.import_asset_tasks([t]);return list(t.get_objects())
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0')
try:
 for name in ['Enton','Nebulak','Glurak']:
  P='/Game/Characters/Creatures/'+name+'/PolishV4';assert not any(k.startswith('Content/Characters/Creatures/'+name+'/PolishV4/') for k in json.loads((O/'InitialState.json').read_text())['original_files']);A=R/'Art/Characters/Creatures'/name;before=unreal.load_asset(inventory['profiles'][name]['profile']);audit=json.loads((A/'PolishV4_Audit.json').read_text());source=A/'Exports/PolishV4'/(name+'_Idle.fbx');assert hashlib.sha256(source.read_bytes()).hexdigest()==audit['exports'][0]['sha256']
  if unreal.EditorAssetLibrary.does_asset_exist(P+'/DA_'+name+'_Presentation'):
   profile=unreal.load_asset(P+'/DA_'+name+'_Presentation');assert not profile.get_validation_errors();rows.append(dict(species=name,profile=profile.get_path_name(),original_profile=before.get_path_name(),skeleton=profile.mesh.skeleton.get_path_name(),minimum_cm=audit['minima']));created.extend(unreal.EditorAssetLibrary.list_assets(P,True,False));continue
  ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False).items():ui.set_editor_property(k,v)
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
  mesh=next(a for a in task(source,P,'SK_'+name+'_PolishV4',ui)if isinstance(a,unreal.SkeletalMesh));sk=mesh.skeleton;slots=list(mesh.materials)
  material=before.mesh.materials[0].material_interface
  if name!='Enton':
   material=unreal.load_asset(P+'/M_'+name+'_PolishV4') if unreal.EditorAssetLibrary.does_asset_exist(P+'/M_'+name+'_PolishV4') else T.create_asset('M_'+name+'_PolishV4',P,unreal.Material,unreal.MaterialFactoryNew());L.delete_all_material_expressions(material);material.set_editor_property('two_sided',True);material.set_editor_property('used_with_skeletal_mesh',True);V=node(material,unreal.MaterialExpressionVertexColor);time=node(material,unreal.MaterialExpressionTime);base=node(material,unreal.MaterialExpressionTextureSample,texture=unreal.load_asset('/Game/Characters/Creatures/'+name+'/MeshyV1/Textures/T_'+name+'_BaseColor'),sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
   for typ,sampler,channel,property in [('Normal',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL,'RGB',unreal.MaterialProperty.MP_NORMAL),('MetallicRoughness',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS,'G',unreal.MaterialProperty.MP_ROUGHNESS)]:
    sample=node(material,unreal.MaterialExpressionTextureSample,texture=unreal.load_asset('/Game/Characters/Creatures/'+name+'/MeshyV1/Textures/T_'+name+'_'+typ),sampler_type=sampler);prop(sample,channel,property)
    if typ=='MetallicRoughness':prop(sample,'B',unreal.MaterialProperty.MP_METALLIC)
   if name=='Glurak':
    orange=node(material,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(.52,.145,.024,1));mix=node(material,unreal.MaterialExpressionLinearInterpolate);link(base,'RGB',mix,'A');link(orange,'',mix,'B');link(V,'R',mix,'Alpha');prop(mix,'',unreal.MaterialProperty.MP_BASE_COLOR)
   else:
    material.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);material.set_editor_property('opacity_mask_clip_value',.333)
    pos=node(material,unreal.MaterialExpressionWorldPosition);flow=custom(material,'return M*float3(sin(P.x*.052+T*.55)+.5*sin(P.z*.083-T*.31),sin(P.y*.061-T*.43)+.4*cos(P.x*.071+T*.27),.6*sin(P.z*.059+T*.37)+.35*cos(P.y*.068-T*.29))*1.1;', ['P','T','M'],unreal.CustomMaterialOutputType.CMOT_FLOAT3);link(pos,'',flow,'P');link(time,'',flow,'T');link(V,'R',flow,'M');prop(flow,'',unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
    variation=custom(material,'return C*(1+M*.045*sin(T*.71+P.x*.035+P.z*.047));',['C','M','T','P'],unreal.CustomMaterialOutputType.CMOT_FLOAT3);link(base,'RGB',variation,'C');link(V,'R',variation,'M');link(time,'',variation,'T');link(pos,'',variation,'P');prop(variation,'',unreal.MaterialProperty.MP_BASE_COLOR)
    normal=node(material,unreal.MaterialExpressionPixelNormalWS);camera=node(material,unreal.MaterialExpressionCameraVectorWS);edge=custom(material,'return 1-M*.65*pow(1-abs(dot(normalize(N),normalize(C))),2);',['M','N','C'],unreal.CustomMaterialOutputType.CMOT_FLOAT1);link(V,'R',edge,'M');link(normal,'',edge,'N');link(camera,'',edge,'C');d=node(material,unreal.MaterialExpressionMaterialFunctionCall);d.set_material_function(unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA'));link(edge,'',d,'Alpha Threshold');prop(d,'',unreal.MaterialProperty.MP_OPACITY_MASK)
   L.recompile_material(material);save(material,P)
  for i,slot in enumerate(slots):slot.material_interface=material if i==0 else before.mesh.materials[i].material_interface
  mesh.materials=slots;save(sk,P);save(mesh,P);clips={}
  for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
   file=A/'Exports'/('MeshyV1'if name=='Enton'else'PolishV4')/(name+'_'+role+'.fbx');ui=unreal.FbxImportUI()
   for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
   for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
   clip=next(a for a in task(file,P,'A_'+name+'_'+role,ui)if isinstance(a,unreal.AnimSequence));clip.set_editor_property('enable_root_motion',False);clips[getattr(unreal.PokeMonsterCreatureClip,role.upper())]=save(clip,P)
  profile=unreal.EditorAssetLibrary.duplicate_asset(before.get_path_name(),P+'/DA_'+name+'_Presentation');profile.set_editor_property('mesh',mesh);profile.set_editor_property('clips',clips);assert not profile.get_validation_errors(),profile.get_validation_errors();save(profile,P);rows.append(dict(species=name,profile=profile.get_path_name(),original_profile=before.get_path_name(),skeleton=sk.get_path_name(),minimum_cm=audit['minima']))
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(old))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(O/'ImportedCandidates.json').write_text(json.dumps(dict(models=rows,assets=created),indent=2));unreal.log('POLISH_CANDIDATES_IMPORTED')
