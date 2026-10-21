"""Import only separate MotionV5 candidates; no species/map/player-default switch."""
import unreal,json,hashlib,subprocess
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/MotionRefinementV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;created=[];rows=[];U='/Game/Characters/YoungTrainer/MotionV3'
def save(a,P):
 assert a.get_path_name().startswith(P+'/');assert unreal.EditorAssetLibrary.save_loaded_asset(a,False);created.append(a.get_path_name());return a
def create(n,P,cls,factory):
 assert not unreal.EditorAssetLibrary.does_asset_exist(P+'/'+n);a=T.create_asset(n,P,cls,factory);assert a;return a
def node(m,cls,**props):
 a=L.create_material_expression(m,cls)
 for k,v in props.items():a.set_editor_property(k,v)
 return a
def link(a,out,b,inp):assert L.connect_material_expressions(a,out,b,inp)
def prop(a,out,p):assert L.connect_material_property(a,out,p)
def custom(m,code,inputs,typ):
 a=node(m,unreal.MaterialExpressionCustom,code=code,output_type=typ);args=[]
 for n in inputs:
  v=unreal.CustomInput();v.set_editor_property('input_name',n);args.append(v)
 a.set_editor_property('inputs',args);return a
def task(source,P,n,ui):
 assert not unreal.EditorAssetLibrary.does_asset_exist(P+'/'+n)
 t=unreal.AssetImportTask()
 for k,v in dict(filename=str(source),destination_path=P,destination_name=n,automated=True,save=False,replace_existing=False,options=ui).items():t.set_editor_property(k,v)
 T.import_asset_tasks([t]);return list(t.get_objects())
def gas_material(P,n,surface):
 m=create(n,P,unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT);m.set_editor_property('two_sided',True);m.set_editor_property('used_with_skeletal_mesh',True);m.set_editor_property('translucency_lighting_mode',unreal.TranslucencyLightingMode.TLM_SURFACE)
 V=node(m,unreal.MaterialExpressionVertexColor);time=node(m,unreal.MaterialExpressionTime);pos=node(m,unreal.MaterialExpressionWorldPosition);normal=node(m,unreal.MaterialExpressionPixelNormalWS);cam=node(m,unreal.MaterialExpressionCameraVectorWS)
 flow=custom(m,'float3 q=P*.039; float a=sin(q.x+T*.63+S*6.28)+.5*cos(q.z*.83-T*.41);float b=sin(q.y*.91-T*.37+S*4)+.45*cos(q.x*.71+T*.19);float c=sin(q.z*.77+T*.29+S*5.2)+.4*cos(q.y*.67-T*.53);return float3(a,b,c)*'+('3.5'if surface else'5.5')+'*M*(1-F);',['P','T','S','M','F'],unreal.CustomMaterialOutputType.CMOT_FLOAT3)
 for a,out,inp in [(pos,'','P'),(time,'','T'),(V,'B','S'),(V,'R','M'),(V,'G','F')]:link(a,out,flow,inp)
 prop(flow,'',unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
 density=custom(m,'float3 q=P*.052;float n=.5+.22*sin(q.x*1.31+T*.27+sin(q.y*.83-T*.17))+.18*sin(q.z*.91-T*.43+cos(q.x*.71+T*.23))+.10*cos(q.y*1.23+q.z*.67+T*.13+S*6.28);return saturate((n-.20)*1.3);',['P','T','S'],unreal.CustomMaterialOutputType.CMOT_FLOAT1)
 for a,out,inp in [(pos,'','P'),(time,'','T'),(V,'B','S')]:link(a,out,density,inp)
 alpha=custom(m,'return D*'+('.17'if surface else'.20')+'*pow(saturate(abs(dot(normalize(N),normalize(C)))),1.45)*(1-saturate(F*1.12));',['D','N','C','F'],unreal.CustomMaterialOutputType.CMOT_FLOAT1)
 for a,out,inp in [(density,'','D'),(normal,'','N'),(cam,'','C'),(V,'G','F')]:link(a,out,alpha,inp)
 prop(alpha,'',unreal.MaterialProperty.MP_OPACITY)
 low=node(m,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(.095,.012,.19,1));high=node(m,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(.28,.055,.46,1));mix=node(m,unreal.MaterialExpressionLinearInterpolate);link(low,'',mix,'A');link(high,'',mix,'B');link(density,'',mix,'Alpha');prop(mix,'',unreal.MaterialProperty.MP_BASE_COLOR);glow=node(m,unreal.MaterialExpressionMultiply,const_b=.09);link(mix,'',glow,'A');prop(glow,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR);rough=node(m,unreal.MaterialExpressionConstant,r=.95);prop(rough,'',unreal.MaterialProperty.MP_ROUGHNESS);spec=node(m,unreal.MaterialExpressionConstant,r=.08);prop(spec,'',unreal.MaterialProperty.MP_SPECULAR);L.recompile_material(m);return save(m,P)
def anim(file,P,name,sk,fps):
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
 for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=fps,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
 a=next(x for x in task(file,P,name,ui)if isinstance(x,unreal.AnimSequence));a.set_editor_property('enable_root_motion',False);return save(a,P)
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 for name in ['Glurak','Nebulak']:
  P='/Game/Characters/Creatures/'+name+'/MotionV5';assert not unreal.EditorAssetLibrary.does_directory_exist(P);A=R/'Art/Characters/Creatures'/name;audit=json.loads((A/'MotionV5_Audit.json').read_text());assert all(hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']for x in audit['exports']);before=unreal.load_asset('/Game/Data/Creatures/DA_'+name).visuals.presentation;ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False).items():ui.set_editor_property(k,v)
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
  mesh=next(x for x in task(A/'Exports/MotionV5'/(name+'_Idle.fbx'),P,'SK_'+name+'_MotionV5',ui)if isinstance(x,unreal.SkeletalMesh));sk=mesh.skeleton;assert unreal.PokeMonsterCreaturePolishLibrary.have_matching_reference_skeleton(mesh,before.mesh);slots=list(mesh.materials);assert len(slots)==2
  if name=='Glurak':
   for i,slot in enumerate(slots):slot.material_interface=before.mesh.materials[i].material_interface
  else:
   slots[0].material_interface=unreal.load_asset('/Game/Characters/Creatures/Nebulak/MeshyV1/Materials/M_Nebulak');slots[1].material_interface=gas_material(P,'M_Nebulak_GasSurface',True)
  mesh.set_editor_property('materials',slots);save(sk,P);save(mesh,P);clips={};hover={}
  for x in audit['exports']:
   if x['role']=='GasEnvelope':continue
   a=anim(R/x['path'],P,'A_'+name+'_'+x['role'],sk,30)
   if x['role']in ['Takeoff','Hover','Land']:hover[x['role']]=a
   else:clips[getattr(unreal.PokeMonsterCreatureClip,x['role'].upper())]=a
  profile=unreal.EditorAssetLibrary.duplicate_asset(before.get_path_name(),P+'/DA_'+name+'_Presentation');profile.set_editor_property('mesh',mesh);profile.set_editor_property('clips',clips)
  if name=='Glurak':profile.set_editor_property('allow_ground_hover',True);profile.set_editor_property('takeoff_clip',hover['Takeoff']);profile.set_editor_property('hover_clip',hover['Hover']);profile.set_editor_property('land_clip',hover['Land']);profile.set_editor_property('hover_height_cm',90.)
  else:
   ui=unreal.FbxImportUI()
   for k,v in dict(import_mesh=True,import_as_skeletal=False,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():ui.set_editor_property(k,v)
   for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,combine_meshes=True,auto_generate_collision=False,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():ui.static_mesh_import_data.set_editor_property(k,v)
   gas=next(x for x in task(A/'Exports/MotionV5/Nebulak_GasEnvelope.fbx',P,'SM_Nebulak_GasEnvelope',ui)if isinstance(x,unreal.StaticMesh));material=gas_material(P,'M_Nebulak_GasEnvelope',False);gas.set_material(0,material);save(gas,P);effect=unreal.PokeMonsterCreatureEffectAnchor();effect.set_editor_property('id','GasEnvelope');effect.set_editor_property('socket','head');effect.set_editor_property('offset',unreal.PokeMonsterCreaturePolishLibrary.get_reference_bone_transform(mesh,'head').inverse());effect.set_editor_property('mesh',gas);effect.set_editor_property('material',material);profile.set_editor_property('effect_anchors',list(profile.effect_anchors)+[effect])
  assert not profile.get_validation_errors(),profile.get_validation_errors();save(profile,P);rows.append(dict(species=name,profile=profile.get_path_name(),previous=before.get_path_name(),mesh=mesh.get_path_name(),clips=len(clips),hover_clips=len(hover)))
 # Player animation import targets the unchanged original skeleton; never save that skeleton.
 P=U;assert not unreal.EditorAssetLibrary.does_directory_exist(P);mesh=unreal.load_asset('/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2');sk=mesh.skeleton;A=R/'Art/Characters/YoungTrainer';audit=json.loads((A/'MotionQualityV3_Audit.json').read_text());player=[]
 for x in audit['exports']:
  assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'];a=anim(R/x['path'],P,'A_Player_'+x['role']+'_V3',sk,60);player.append(dict(role=x['role'],path=a.get_path_name(),seconds=a.get_play_length()))
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()];assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(O/'Import.json').write_text(json.dumps(dict(models=rows,player=player,assets=created,original_skeleton_not_saved=True),indent=2));unreal.log('MOTION_V5_IMPORT_COMPLETE')
