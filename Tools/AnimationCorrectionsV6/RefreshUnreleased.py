"""Explicit correction of OWN untracked V6 assets only; never a released-asset reimport tool."""
import unreal,json,ast,subprocess,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();q=json.loads((R/'Saved/AnimationCorrectionsV6/RefreshRequest.json').read_text());name=q['name'];assert name in ['Machomei','Glurak'];P='/Game/Characters/Creatures/'+name+'/AnimationV6';assert not subprocess.check_output(['git','ls-files','--','Content'+P[5:]],cwd=R).strip();A=R/'Art/Characters/Creatures'/name;audit=json.loads((A/'AnimationCorrectionsV6_Audit.json').read_text());assert all(hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']for x in audit['exports']);T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;created=[]
s=(R/'Tools/MotionRefinementV5/ImportCandidates.py').read_text()
for n in ast.parse(s).body:
 if isinstance(n,ast.FunctionDef)and n.name in ['save','create','node','link','prop','custom']:exec(ast.get_source_segment(s,n))
profile=unreal.load_asset(P+'/DA_'+name+'_Presentation_V6');mesh=profile.mesh;sk=mesh.skeleton;assert sk.get_path_name().startswith(P+'/');old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 for x in [dict(next(x for x in audit['exports']if x['role']=='Idle'),mesh_only=True)]+audit['exports']:
  ui=unreal.FbxImportUI();is_mesh=x.get('mesh_only',False)
  for k,v in dict(import_mesh=is_mesh,import_as_skeletal=True,import_animations=not is_mesh,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH if is_mesh else unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True,create_physics_asset=False).items():ui.set_editor_property(k,v)
  data=ui.skeletal_mesh_import_data if is_mesh else ui.anim_sequence_import_data
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True).items():data.set_editor_property(k,v)
  if is_mesh:data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE);data.set_editor_property('normal_import_method',unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)
  else:
   for k,v in dict(use_default_sample_rate=False,custom_sample_rate=x['fps'],animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():data.set_editor_property(k,v)
  t=unreal.AssetImportTask()
  for k,v in dict(filename=str(R/x['path']),destination_path=P,destination_name=('SK_'+name+'_V6'if is_mesh else'A_'+name+'_'+x['role']+'_V6'),automated=True,save=False,replace_existing=True,replace_existing_settings=True,options=ui).items():t.set_editor_property(k,v)
  T.import_asset_tasks([t])
  for obj in t.get_objects():
   if isinstance(obj,(unreal.SkeletalMesh,unreal.AnimSequence)):save(obj,P)
 if name=='Glurak':
  m=create('M_Glurak_CompleteRear_V6',P,unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('two_sided',True);m.set_editor_property('used_with_skeletal_mesh',True);base=node(m,unreal.MaterialExpressionTextureSample,texture=unreal.load_asset('/Game/Characters/Creatures/Glurak/MeshyV1/Textures/T_Glurak_BaseColor'),sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);v=node(m,unreal.MaterialExpressionVertexColor);side=node(m,unreal.MaterialExpressionTwoSidedSign);mask=custom(m,'return saturate(R+G*lerp(1-step(0,S),step(0,S),B));',['R','G','B','S'],unreal.CustomMaterialOutputType.CMOT_FLOAT1)
  for source,out,inp in [(v,'R','R'),(v,'G','G'),(v,'B','B'),(side,'','S')]:link(source,out,mask,inp)
  orange=node(m,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(.52,.145,.024,1));mix=node(m,unreal.MaterialExpressionLinearInterpolate);link(base,'RGB',mix,'A');link(orange,'',mix,'B');link(mask,'',mix,'Alpha');prop(mix,'',unreal.MaterialProperty.MP_BASE_COLOR)
  for typ,sampler,channel,property in [('Normal',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL,'RGB',unreal.MaterialProperty.MP_NORMAL),('MetallicRoughness',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS,'G',unreal.MaterialProperty.MP_ROUGHNESS)]:
   sample=node(m,unreal.MaterialExpressionTextureSample,texture=unreal.load_asset('/Game/Characters/Creatures/Glurak/MeshyV1/Textures/T_Glurak_'+typ),sampler_type=sampler);prop(sample,channel,property)
   if typ=='MetallicRoughness':prop(sample,'B',unreal.MaterialProperty.MP_METALLIC)
  L.recompile_material(m);save(m,P);slots=list(mesh.materials);slots[0].material_interface=m;mesh.set_editor_property('materials',slots);save(mesh,P)
 assert not profile.get_validation_errors();save(profile,P)
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),[x.get_path_name()for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()];(R/'Saved/AnimationCorrectionsV6'/('Refresh'+name+'.json')).write_text(json.dumps(dict(name=name,assets=created,untracked_only=True),indent=2))
