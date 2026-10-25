"""Visually verified corrections: linear grass colours, genuinely lit water, stone/bridge detail."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();A=R/'Art/World/VisualV2EnvironmentV3';D=R/'Saved/ProjectRefinement/EnvironmentV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world();L=unreal.MaterialEditingLibrary;ROOT='/Game/Environment/VisualV2EnvironmentV3';scope=json.loads((A/'Scope.json').read_text());assert not (D/'Polished.json').exists()
def custom(m,code,inputs):
 n=L.create_material_expression(m,unreal.MaterialExpressionCustom);arr=[]
 for k in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',k);arr.append(i)
 n.set_editor_property('inputs',arr);n.set_editor_property('code',code);n.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
 for k,(x,out)in inputs.items():assert L.connect_material_expressions(x,out,n,k)
 return n
def constant(m,v,prop):
 n=L.create_material_expression(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',v);L.connect_material_property(n,'',prop)
def finish(m):
 if isinstance(m,unreal.Material):m.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(m)
 assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
def clone(src,name):
 path=ROOT+'/Materials/'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(path);m=unreal.EditorAssetLibrary.duplicate_asset(src,path);assert m;scope['assets'].append(path);return m
def bind(c,i,m):
 scope['bindings'].append({'actor':c.get_owner().get_name(),'component':c.get_name(),'slot':i,'before':c.get_material(i).get_path_name(),'after':m.get_path_name()});c.set_material(i,m)
m=unreal.load_asset(ROOT+'/Materials/M_EQ3_Grass')
for n in L.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom):
  s=n.get_editor_property('code')
  if 'return C.rgb*lerp'in s:n.set_editor_property('code',s.replace('return C.rgb*lerp','float3 eqLinear=lerp(C.rgb/12.92,pow(max((C.rgb+.055)/1.055,0),2.4),step(.04045,C.rgb));return eqLinear*lerp'))
finish(m)
# Previous unlit shader ignored its normal and roughness. Route its real colour into a lit surface.
m=unreal.load_asset(ROOT+'/Materials/M_EQ3_Stream');color=L.get_material_property_input_node(m,unreal.MaterialProperty.MP_EMISSIVE_COLOR);assert color;m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_DEFAULT_LIT);m.set_editor_property('translucency_lighting_mode',unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING);L.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR);constant(m,0,unreal.MaterialProperty.MP_EMISSIVE_COLOR);finish(m)
# Reuse the painted stone texture and original per-instance parameters.
base=clone('/Game/Environment/WestlandAssetLibrary/Materials/M_WLA_Painted','M_EQ3_MossRockBase');color=L.get_material_property_input_node(base,unreal.MaterialProperty.MP_BASE_COLOR);p=L.create_material_expression(base,unreal.MaterialExpressionWorldPosition);nrm=L.create_material_expression(base,unreal.MaterialExpressionVertexNormalWS)
n=custom(base,'float broad=.5+.27*sin(P.x*.012+sin(P.z*.021))+.22*cos(P.y*.017-P.z*.009);float fissure=pow(saturate(sin(P.x*.045+sin(P.z*.037)*1.4+P.y*.021)),18);float moss=saturate(N.z)*smoothstep(.35,.82,broad)*.47;float3 stone=C.rgb*(.91+.18*broad)*(1-.13*fissure);return lerp(stone,stone*float3(.62,.85,.44),moss);',{'C':(color,''),'P':(p,''),'N':(nrm,'')});L.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR)
n=custom(base,'return normalize(float3(.10*cos(P.x*.12+P.z*.08),.08*sin(P.y*.14+P.z*.11),1));',{'P':(p,'')});L.connect_material_property(n,'',unreal.MaterialProperty.MP_NORMAL);finish(base)
rock={}
for src,name in [('/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_MossStone','MI_EQ3_MossStone'),('/Game/Environment/VisualV2WorldArtV5/Materials/MI_WLA_MossStone_Instanced','MI_EQ3_MossStoneInstanced')]:
 mi=clone(src,name);L.set_material_instance_parent(mi,base);finish(mi);rock[src]=mi
# Original bridge geometry/collision, weathered matte oak rather than saturated orange.
m=clone('/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Wood','M_EQ3_BridgeOak');color=L.get_material_property_input_node(m,unreal.MaterialProperty.MP_BASE_COLOR);p=L.create_material_expression(m,unreal.MaterialExpressionWorldPosition)
n=custom(m,'float2 q=P.xy;float grain=sin(q.y*.29+sin(q.x*.018)*1.6);float wear=.5+.25*sin(q.x*.021+sin(q.y*.012))+.25*cos(q.y*.033);float grey=dot(C.rgb,float3(.299,.587,.114));return lerp(C.rgb,grey*float3(.93,.90,.80),.32)*float3(.83,.88,.84)*(.91+.15*wear+.04*grain);',{'C':(color,''),'P':(p,'')});L.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR);constant(m,.9,unreal.MaterialProperty.MP_ROUGHNESS);finish(m)
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  for i in range(c.get_num_materials()):
   old=c.get_material(i)
   if not old:continue
   path=old.get_path_name().split('.')[0]
   if path in rock and c.static_mesh and any(x in c.static_mesh.get_name()for x in ['Boulder','Rock','Pebble','MossStone']):bind(c,i,rock[path])
   elif a.get_actor_label().startswith('VS_Bridge') and path=='/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Wood':bind(c,i,m)
scope['assets']=sorted(set(scope['assets']));(A/'Scope.json').write_text(json.dumps(scope,indent=2));(D/'Polished.json').write_text(json.dumps({'linear_colour_corrected':True,'water_lighting':'DefaultLit SurfacePerPixel, no scene capture, no refraction','stone_and_bridge_bindings':len(scope['bindings'])},indent=2));assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
