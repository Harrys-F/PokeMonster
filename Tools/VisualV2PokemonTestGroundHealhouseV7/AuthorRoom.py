"""Private V7 PBR graphs and room-only material bindings. No source/geometry/light edits."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';ROOT='/Game/Environment/VisualV2InteriorV7';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();ML=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert all(x.get_path_name().startswith(ROOT+'/')for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages());assert not(D/'Authored.json').exists();assets=[];bindings=[]
def node(m,cls):return ML.create_material_expression(m,cls)
def new(name):
 m=unreal.load_asset(ROOT+'/Materials/M_V7_'+name)or AT.create_asset('M_V7_'+name,ROOT+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 # Delete through a copied list: the UE 5.8 bulk helper mutates its own iterator.
 for expression in list(ML.get_material_expressions(m)):ML.delete_material_expression(m,expression)
 assert not ML.get_material_expressions(m)
 assets.append(m);m.set_editor_property('used_with_instanced_static_meshes',True);return m

def custom(m,code,inputs,typ=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 n=node(m,unreal.MaterialExpressionCustom);n.set_editor_property('code',code);n.set_editor_property('output_type',typ);vs=[]
 for key in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',key);vs.append(i)
 n.set_editor_property('inputs',vs)
 for key,(v,pin)in inputs.items():assert ML.connect_material_expressions(v,pin,n,key)
 return n
def sample(m,path,uv,normal=False):
 n=node(m,unreal.MaterialExpressionTextureSample);n.texture=unreal.load_asset(path);assert n.texture,path
 if normal:n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
 elif n.texture.compression_settings==unreal.TextureCompressionSettings.TC_MASKS:n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
 elif not n.texture.srgb:n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
 assert ML.connect_material_expressions(uv,'',n,'UVs');return n
def scalar(m,v,prop):n=node(m,unreal.MaterialExpressionConstant);n.r=v;ML.connect_material_property(n,'',prop)
def finish(m):
 errors=ML.recompile_material(m);assert not errors,(m.get_name(),errors);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
def projected_uv(m,scale):
 p=node(m,unreal.MaterialExpressionWorldPosition);n=node(m,unreal.MaterialExpressionVertexNormalWS)
 uv=custom(m,'float3 a=abs(N);return (a.z>.55?P.xy:(a.x>a.y?P.yz:P.xz))/'+str(scale)+';',{'P':(p,''),'N':(n,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2);return p,n,uv
# Plaster: existing owned fine micro-normal, restrained irregular lime variation and high roughness.
# The available Fab Wall_1/2/3 are masonry, so they are deliberately not misused as lime plaster.
for name,tint in [('LimePlaster',(.68,.61,.48)),('SageLimewash',(.28,.34,.19))]:
 m=new(name);p,n,uv=projected_uv(m,48);nm=sample(m,'/Game/Environment/VisualV2WorldRefinementV4/Textures/T_WR4_PlasterMicroNormal',uv,True)
 c=custom(m,'float v=.025*sin(P.x*.047+sin(P.z*.037))*cos(P.y*.061+P.z*.023)+.008*sin(P.z*.91+P.x*.31);return float3'+str(tint)+'*(1+v);',{'P':(p,'')});ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);ML.connect_material_property(nm,'RGB',unreal.MaterialProperty.MP_NORMAL);scalar(m,.94,unreal.MaterialProperty.MP_ROUGHNESS);finish(m)
# Real local Fab grain. Floor repeat 2m; long grain joinery uses 1.8m horizontal/0.65m vertical projection.
wood='/Game/Fab/VisualV2RefinementLocal/Textures/T_WR4_Timber_'
for name,scale,tint in [('OakFloor',200,(1.08,.91,.72)),('OakJoinery',180,(.79,.62,.44))]:
 m=new(name);p,n,uv=projected_uv(m,scale);bc=sample(m,wood+'BaseColor',uv);nm=sample(m,wood+'Normal',uv,True)
 c=custom(m,'float3 c=T*float3'+str(tint)+';return lerp(dot(c,float3(.299,.587,.114))*float3(1.08,1,.88),c,.68);',{'T':(bc,'RGB')});ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);nn=custom(m,'return normalize(lerp(float3(0,0,1),N,.5));',{'N':(nm,'RGB')});ML.connect_material_property(nn,'',unreal.MaterialProperty.MP_NORMAL)
 # Existing dedicated roughness. Preserve the source; clamp to matte waxed wood.
 rough=sample(m,wood+'Roughness',uv);rr=custom(m,'return clamp(T.r,.68,.94);',{'T':(rough,'RGB')},unreal.CustomMaterialOutputType.CMOT_FLOAT1);ML.connect_material_property(rr,'',unreal.MaterialProperty.MP_ROUGHNESS);finish(m)
# Review pools only: no dependence on the main pond's position or water system.
m=new('ReviewWater');p=node(m,unreal.MaterialExpressionWorldPosition);t=node(m,unreal.MaterialExpressionTime);c=custom(m,'float v=.5+.5*sin(P.x*.035+T*.55)*sin(P.y*.027-T*.39);return lerp(float3(.025,.105,.095),float3(.065,.19,.16),v*.35);',{'P':(p,''),'T':(t,'')});ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(m,.3,unreal.MaterialProperty.MP_ROUGHNESS);finish(m)
newm={a.get_name().removeprefix('M_V7_'):a for a in assets}
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if not 16000<a.get_actor_location().x<17700:continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  for i in range(c.get_num_materials()):
   old=c.get_material(i);name=old.get_name()if old else '';key=None
   if name=='M_V6_LimePlaster':key='LimePlaster'
   elif name=='M_V6_SageLimewash':key='SageLimewash'
   elif name=='M_V6_OakFloor':key='OakFloor'
   elif name in ['M_V6_OakJoinery','M_WOV_Timber']:key='OakJoinery'
   if key:c.set_material(i,newm[key]);bindings.append(dict(actor=a.get_actor_label(),component=c.get_name(),slot=i,before=old.get_path_name(),after=newm[key].get_path_name()))
assert len(bindings)>80,len(bindings);assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(D/'Authored.json').write_text(json.dumps(dict(materials=[a.get_path_name()for a in assets],bindings=bindings,unchanged='Transforms, geometry, collision, walls, lights, gameplay',sources=[wood+'BaseColor',wood+'Normal',wood+'Roughness','/Game/Environment/VisualV2WorldRefinementV4/Textures/T_WR4_PlasterMicroNormal']),indent=2))
