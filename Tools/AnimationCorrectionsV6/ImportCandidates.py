"""New V6 namespaces only. No map/species/default-player adoption."""
import unreal,json,ast,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/AnimationCorrectionsV6';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;created=[];rows=[]
s=(R/'Tools/MotionRefinementV5/ImportCandidates.py').read_text()
for n in ast.parse(s).body:
 if isinstance(n,ast.FunctionDef)and n.name in ['save','create','node','link','prop','custom','task','anim','gas_material']:
  code=ast.get_source_segment(s,n)
  if n.name=='gas_material':code=code.replace("'.17'if surface else'.20'","'.23'if surface else'.27'").replace('(.095,.012,.19,1)','(.12,.018,.24,1)').replace('(.28,.055,.46,1)','(.34,.072,.55,1)')
  exec(code)
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 for name in ['Player','Glurak','Nebulak','Machomei','Myrapla']:
  P=('/Game/Characters/YoungTrainer'if name=='Player'else'/Game/Characters/Creatures/'+name)+'/AnimationV6';assert not unreal.EditorAssetLibrary.does_directory_exist(P);A=R/('Art/Characters/YoungTrainer'if name=='Player'else'Art/Characters/Creatures/'+name);audit=json.loads((A/'AnimationCorrectionsV6_Audit.json').read_text());assert all(hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']for x in audit['exports']);before=None;mesh=None
  if name=='Player':sk=unreal.load_asset('/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2').skeleton
  else:
   before=unreal.load_asset('/Game/Data/Creatures/DA_'+name).get_visuals().presentation;ui=unreal.FbxImportUI()
   for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False).items():ui.set_editor_property(k,v)
   for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
   mesh=next(x for x in task(A/'Exports/AnimationV6'/(name+'_Idle.fbx'),P,'SK_'+name+'_V6',ui)if isinstance(x,unreal.SkeletalMesh));sk=mesh.skeleton;assert unreal.PokeMonsterCreaturePolishLibrary.have_matching_reference_skeleton(mesh,before.mesh);slots=list(mesh.materials)
   for i,slot in enumerate(slots):
    if name=='Nebulak'and i==1:slot.material_interface=gas_material(P,'M_Nebulak_GasSurface_V6',True)
    elif name=='Nebulak'and i==2:
     m=create('M_Nebulak_ClosedCore_V6',P,unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('used_with_skeletal_mesh',True);c=node(m,unreal.MaterialExpressionConstant3Vector,constant=unreal.LinearColor(.004,.003,.009,1));prop(c,'',unreal.MaterialProperty.MP_BASE_COLOR);r=node(m,unreal.MaterialExpressionConstant,r=.82);prop(r,'',unreal.MaterialProperty.MP_ROUGHNESS);v=node(m,unreal.MaterialExpressionConstant,r=.12);prop(v,'',unreal.MaterialProperty.MP_SPECULAR);L.recompile_material(m);slot.material_interface=save(m,P)
    else:slot.material_interface=before.mesh.materials[i].material_interface
   mesh.set_editor_property('materials',slots);save(sk,P);save(mesh,P)
  clips={};hover={};player=[]
  for x in audit['exports']:
   a=anim(R/x['path'],P,'A_'+name+'_'+x['role']+'_V6',sk,x['fps'])
   if name=='Player':player.append(dict(role=x['role'],asset=a.get_path_name()));continue
   if x['role']in ['Takeoff','Hover','Land']:hover[x['role']]=a
   else:clips[getattr(unreal.PokeMonsterCreatureClip,x['role'].upper())]=a
  if name=='Player':rows.append(dict(name=name,clips=player));continue
  profile=unreal.EditorAssetLibrary.duplicate_asset(before.get_path_name(),P+'/DA_'+name+'_Presentation_V6');profile.set_editor_property('mesh',mesh);profile.set_editor_property('clips',clips)
  if name=='Glurak':
   for k,role in [('takeoff_clip','Takeoff'),('hover_clip','Hover'),('land_clip','Land')]:profile.set_editor_property(k,hover[role])
  if name=='Nebulak':
   profile.set_editor_property('overworld_float_amplitude_cm',6.);effects=list(profile.effect_anchors)
   for effect in effects:
    if str(effect.id)=='GasEnvelope':effect.set_editor_property('material',gas_material(P,'M_Nebulak_Envelope_V6',False))
   profile.set_editor_property('effect_anchors',effects)
  assert not profile.get_validation_errors(),profile.get_validation_errors();save(profile,P);rows.append(dict(name=name,previous=before.get_path_name(),profile=profile.get_path_name(),mesh=mesh.get_path_name(),height=mesh.get_bounds().box_extent.z*2))
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),[x.get_path_name()for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()];(O/'Import.json').write_text(json.dumps(dict(models=rows,assets=created),indent=2));unreal.log('V6_CANDIDATES_IMPORTED')
