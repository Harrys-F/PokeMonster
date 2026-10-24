"""Map-local camera zone and private upper-canopy variants; original tree materials and shadows preserved."""
import unreal,json,sys,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();O=R/'Saved/BiomeTestV11/ForestCameraBuild.json';assert not O.exists()
D='/Game/Environment/BiomeTestV1/DenseForestV11';M=unreal.MaterialEditingLibrary;clones={};sources={};collection=unreal.load_asset('/Game/Environment/DevTestMapVisualV2/Materials/MPC_PlayerSight');assert collection

def node(m,cls):return M.create_material_expression(m,cls)
def link(a,out,b,inp):assert M.connect_material_expressions(a,out,b,inp),(str(a),out,str(b),inp)
def private(m):
 source=m.get_path_name()
 if source in clones:return clones[source]
 dst=D+'/'+m.get_name()+'_Dense';assert not unreal.EditorAssetLibrary.does_asset_exist(dst);n=unreal.EditorAssetLibrary.duplicate_asset(source,dst);assert n;clones[source]=n;sources[dst]=source
 if isinstance(n,unreal.MaterialInstanceConstant):
  M.set_material_instance_parent(n,private(m.get_editor_property('parent')));M.update_material_instance(n)
 else:
  assert isinstance(n,unreal.Material)and n.blend_mode==unreal.BlendMode.BLEND_MASKED
  old=M.get_material_property_input_node(n,unreal.MaterialProperty.MP_OPACITY_MASK);out=M.get_material_property_input_node_output_name(n,unreal.MaterialProperty.MP_OPACITY_MASK);assert old
  P=node(n,unreal.MaterialExpressionWorldPosition);T=node(n,unreal.MaterialExpressionCollectionParameter);T.set_editor_property('collection',collection);T.set_editor_property('parameter_name','PlayerSightTarget')
  C=node(n,unreal.MaterialExpressionCollectionParameter);C.set_editor_property('collection',collection);C.set_editor_property('parameter_name','PlayerSightCamera')
  S=node(n,unreal.MaterialExpressionScalarParameter);S.set_editor_property('parameter_name','DenseCanopyStrength');S.set_editor_property('default_value',0.)
  f=node(n,unreal.MaterialExpressionCustom);f.set_editor_property('desc','Only upper canopy in an explicit local zone. Trunks below target+240cm remain.');f.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT1);inputs=[]
  for name in ['P','T','S','C']:
   i=unreal.CustomInput();i.set_editor_property('input_name',name);inputs.append(i)
  f.set_editor_property('inputs',inputs);f.set_editor_property('code','float3 axis=T-C;float t=dot(P-C,axis)/max(dot(axis,axis),1.);float r=length((P-C)-t*axis);float corridor=(1-smoothstep(220.,380.,r))*smoothstep(.05,.15,t)*(1-smoothstep(.93,1.07,t));return 1-saturate(S)*.98*smoothstep(T.z+240,T.z+480,P.z)*corridor;');link(P,'',f,'P');link(T,'',f,'T');link(S,'',f,'S');link(C,'',f,'C')
  d=node(n,unreal.MaterialExpressionMaterialFunctionCall);assert d.set_material_function(unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA'));link(f,'',d,'Alpha Threshold')
  mask=node(n,unreal.MaterialExpressionMultiply);link(old,out,mask,'A');link(d,'',mask,'B');shadow=node(n,unreal.MaterialExpressionShadowReplace);link(mask,'',shadow,'Default');link(old,out,shadow,'Shadow');assert M.connect_material_property(shadow,'',unreal.MaterialProperty.MP_OPACITY_MASK);M.recompile_material(n)
 assert unreal.EditorAssetLibrary.save_loaded_asset(n,False);return n
rows=[]
for a in ES.get_all_level_actors():
 if not isinstance(a,unreal.StaticMeshActor)or not a.get_actor_label().startswith('Biome_RevealTree_'):continue
 c=a.static_mesh_component;sm=c.static_mesh;assert sm;u,v=L.local(a.get_actor_location().x,a.get_actor_location().y)
 if not(1450<u<4950 and -3300<v<-350):continue
 before=[];after=[]
 for j in range(c.get_num_materials()):
  original=c.get_material(j);source=original
  if sm.get_name()=='SM_WLA_Birch_A':
   suffix=original.get_name().replace('MI_WLA_','');source=unreal.load_asset('/Game/Environment/DevTestMapVisualV2/Materials/MI_V2_'+suffix+'Reveal');assert source
  else:assert sm.get_name()=='SM_WLA_OakAncient_V3'
  variant=private(source);c.set_material(j,variant);before.append(original.get_path_name());after.append(variant.get_path_name())
 rows.append({'actor':a.get_actor_label(),'original':before,'private_variant':after})
assert len(rows)>15
z=ES.spawn_actor_from_class(unreal.PokeMonsterForestCameraZone,unreal.Vector(*L.world(3200,-1700,0)),unreal.Rotator(yaw=45));z.set_actor_label('Biome_DenseForestCamera_V11');z.set_folder_path('BiomeV11/ForestCamera');z.tags=['BiomeTestV1','BiomeV11'];z.bounds.set_box_extent(unreal.Vector(1050,650,600));z.local_arm_length_cm=1700.;z.transition_seconds=.8;z.edge_feather_cm=180.;z.set_editor_property('bEnabled',True)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages());assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1');O.write_text(json.dumps({'zone_uv':[3200,-1700],'half_extents_cm':[1050,650,600],'local_arm_cm':1700,'standard_arm_cm':2850,'transition_s':.8,'edge_feather_cm':180,'trees':rows,'private_material_sources':sources,'ground_shadow_input':'Original opacity mask via ShadowPassSwitch; extra upper-canopy removal only in non-shadow pass','original_reveal_radii_cm':[110,220],'original_materials_edited':False,'original_lights_edited':False,'new_maps':False},indent=2))
