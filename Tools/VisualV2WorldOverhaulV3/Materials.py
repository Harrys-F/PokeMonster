"""Own map-local graphs and variants, no imported/shared asset saves."""
import runpy
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Common.py')));AT=unreal.AssetToolsHelpers.get_asset_tools();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/Materials/M_WOV_Ground'),'Own materials already created; do not rerun'
def new(name):return AT.create_asset(name,ROOT+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
def node(m,cls):return ML.create_material_expression(m,cls)
def custom(m,code,inputs,typ=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 n=node(m,unreal.MaterialExpressionCustom);n.set_editor_property('code',code);n.set_editor_property('output_type',typ);ls=[]
 for key in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',key);ls.append(i)
 n.set_editor_property('inputs',ls)
 for key,(src,pin)in inputs.items():assert ML.connect_material_expressions(src,pin,n,key)
 return n
def finish(m):m.set_editor_property('used_with_instanced_static_meshes',True);ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
def scalar(m,v,prop):n=node(m,unreal.MaterialExpressionConstant);n.r=v;assert ML.connect_material_property(n,'',prop)
def surface(name,color,texture=None,scale=150,rough=.82):
 m=new(name);P=node(m,unreal.MaterialExpressionWorldPosition);N=node(m,unreal.MaterialExpressionVertexNormalWS);uv=custom(m,'float3 a=abs(N);return (a.z>.6?P.xy:(a.x>a.y?P.yz:P.xz))/'+str(float(scale))+';',{'P':(P,''),'N':(N,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2)
 if texture:
  t=node(m,unreal.MaterialExpressionTextureSample);t.texture=unreal.load_asset(texture);assert t.texture;ML.connect_material_expressions(uv,'',t,'UVs');c=custom(m,'float g=dot(T,float3(.299,.587,.114));return lerp(T,g.xxx,.50)*float3('+','.join(str(x)for x in color)+');',{'T':(t,'RGB')})
 else:c=custom(m,'float grain=.95+.05*sin(P.z*.08+sin(P.x*.017));return float3('+','.join(str(x)for x in color)+')*grain;',{'P':(P,'')})

 if texture:
  np=texture.replace('_basecolor','_normal');nt=node(m,unreal.MaterialExpressionTextureSample);nt.texture=unreal.load_asset(np);assert nt.texture;nt.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL);ML.connect_material_expressions(uv,'',nt,'UVs');nn=custom(m,'return normalize(lerp(float3(0,0,1),N,.30));',{'N':(nt,'RGB')});ML.connect_material_property(nn,'',unreal.MaterialProperty.MP_NORMAL)
 ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(m,rough,unreal.MaterialProperty.MP_ROUGHNESS);finish(m);return m
surface('M_WOV_Timber',(.72,.53,.32),'/Game/Pack_Bonus/Textures/Wooden_Floor_2/T_Pack_Bonus_Wooden_Floor_2_basecolor',120)
surface('M_WOV_Stone',(.80,.75,.63),'/Game/Pack_Bonus/Textures/Stone_1/T_Pack_Bonus_Stone_1_basecolor',160)
surface('M_WOV_Plaster',(.64,.54,.37),None)
m=new('M_WOV_Cobbles');P=node(m,unreal.MaterialExpressionWorldPosition);c=custom(m,'float2 q=P.xy/38; q.x+=fmod(floor(q.y),2)*.5;float2 f=frac(q);float e=smoothstep(.02,.12,min(min(f.x,1-f.x),min(f.y,1-f.y)));float v=frac(sin(dot(floor(q),float2(12.9898,78.233)))*43758.5453);return lerp(float3(.10,.085,.065),float3(.34,.30,.23)*(.82+v*.36),e);',{'P':(P,'')});ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(m,.88,unreal.MaterialProperty.MP_ROUGHNESS);finish(m)
m=new('M_WOV_Roof');P=node(m,unreal.MaterialExpressionWorldPosition);c=custom(m,'float2 q=P.xy/float2(25,18);q.x+=fmod(floor(q.y),2)*.5;float2 f=frac(q);float edge=smoothstep(.01,.07,min(f.x,1-f.x))*smoothstep(.01,.10,f.y);float v=frac(sin(dot(floor(q),float2(9.7,71.3)))*4312.5);return lerp(float3(.055,.025,.018),float3(.23,.085,.038)*(.8+.5*v),edge);',{'P':(P,'')});ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(m,.76,unreal.MaterialProperty.MP_ROUGHNESS);finish(m)
# Six existing wildflower variants are duplicated, never alter Westland assets.
for name in ['Cream','Yellow','Blue','Violet','Red','Pink']:
 m=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/WestlandEnvironmentPolishV2/Materials/MI_WEP_Blossom_'+name,ROOT+'/Materials/MI_WOV_Flower_'+name);assert m;assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
# Global ground proportions replace the prior six-area colour islands.
m=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/VisualV2EnvironmentPolishV2/Materials/M_EP2_Ground',ROOT+'/Materials/M_WOV_Ground');assert m
for n in ML.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom)and'float meadow='in n.get_editor_property('code'):
  n.set_editor_property('code',"float2 p=P.xy;float forest=max(saturate(1-dot((p-float2(-4900,1700))/float2(1200,1250),(p-float2(-4900,1700))/float2(1200,1250))),saturate(1-dot((p-float2(1500,1400))/float2(1100,1350),(p-float2(1500,1400))/float2(1100,1350))));forest=max(forest,saturate(1-dot((p-float2(-2700,2300))/float2(1300,650),(p-float2(-2700,2300))/float2(1300,650))));float variation=.90+.07*sin(p.x*.002+sin(p.y*.003))+.03*sin(p.y*.011);float3 c=G*float3(.82,1.0,.70)*variation;c=lerp(c,F*1.14,forest*.84);float stream=min(length(p-float2(clamp(p.x,-910,1100),-320)),length(p-float2(720,clamp(p.y,-680,-320))));float pond=abs(length((p-float2(720,-1800))/float2(900,650))-1);float bank=max(1-smoothstep(40,175,stream),1-smoothstep(.02,.13,pond));float g=dot(R,float3(.299,.587,.114));c=lerp(c,g*float3(.78,.70,.51),bank*.84);float hill=saturate(1-length((p-float2(-720,960))/float2(520,430)));c=lerp(c,R*.85,hill*.48);return c;")
 if isinstance(n,unreal.MaterialExpressionCustom)and'float3 dirt='in n.get_editor_property('code'):
  n.set_editor_property('code','float g=dot(T,float3(.299,.587,.114));float3 dirt=lerp(T*float3(.92,.73,.51),g*float3(1.02,.80,.57),.85);return lerp(C,dirt*.90,M);')
finish(m)
# Retain water footprint; flowing highlights are purely visual and map-local.
for name,src in [('Stream','/Game/Environment/VisualV2FabAssetTrialV1/Materials/M_FAT_Stream'),('Pond','/Game/Environment/PokemonAIV3/Materials/M_AIV3PondWater')]:
 m=unreal.EditorAssetLibrary.duplicate_asset(src,ROOT+'/Materials/M_WOV_'+name);assert m
 P=node(m,unreal.MaterialExpressionWorldPosition);t=node(m,unreal.MaterialExpressionTime);n=custom(m,'float a=sin((P.x-T*18)*.055+sin(P.y*.028));float b=cos(P.y*.064+T*.7+sin(P.x*.017));return normalize(float3(a*.085,b*.065,1));',{'P':(P,''),'T':(t,'')});ML.connect_material_property(n,'',unreal.MaterialProperty.MP_NORMAL);scalar(m,.19 if name=='Stream'else .25,unreal.MaterialProperty.MP_ROUGHNESS);finish(m)
(D/'Materials.json').write_text(json.dumps(dict(own_graphs=['Timber','Stone','Plaster','Cobbles','Roof','Ground','Stream','Pond'],flower_variants=6,shared_materials_modified=False),indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
