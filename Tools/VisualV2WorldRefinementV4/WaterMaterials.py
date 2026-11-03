"""Two single existing water surfaces with own low-amplitude flow and depth coefficients."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/MaterialHelpers.py')));assert not(D/'WaterMaterials.json').exists()
def vector(m,v):n=node(m,unreal.MaterialExpressionConstant3Vector);n.set_editor_property('constant',unreal.LinearColor(*v,1));return n
for name in ['Stream','Pond']:
 m=new(name);m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_SINGLE_LAYER_WATER);m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);P=node(m,unreal.MaterialExpressionWorldPosition);T=node(m,unreal.MaterialExpressionTime)
 if name=='Pond':code='float2 q=(P.xy-float2(720,-1800))/float2(900,650);float a=atan2(q.y,q.x);float r=.969+.016*sin(3*a+.6)+.011*sin(7*a-1.2);return 1-smoothstep(-4,1,(length(q)-r)*650);'
 else:code='float2 q=P.xy;float y=-320+5*sin(q.x*.008);float width=64+6*sin(q.x*.005+1);float river=length(q-float2(clamp(q.x,-910,1100),y))-width;float branch=length(q-float2(720,clamp(q.y,-680,-320)))-60;return 1-smoothstep(-3,3,min(river,branch));'
 mask=custom(m,code,{'P':(P,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT1);ML.connect_material_property(mask,'',unreal.MaterialProperty.MP_OPACITY_MASK);c=custom(m,'float a=sin((P.x-T*18)*.10+sin(P.y*.15));float speck=pow(saturate(a),12)*pow(saturate(sin(P.y*.11+P.x*.025)),4);return float3(.012,.030,.027)+speck*.008;',{'P':(P,''),'T':(T,'')});ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);nm=custom(m,'float a=(P.x-T*18)*.10+sin(P.y*.073);float b=P.y*.12+P.x*.03+T*.29;return normalize(float3(.018*sin(a)+.009*cos(b),.025*cos(a*.7)+.012*sin(b),1));',{'P':(P,''),'T':(T,'')});ML.connect_material_property(nm,'',unreal.MaterialProperty.MP_NORMAL);scalar(m,.22 if name=='Pond'else .19,unreal.MaterialProperty.MP_ROUGHNESS);scalar(m,.21,unreal.MaterialProperty.MP_OPACITY);scalar(m,.5,unreal.MaterialProperty.MP_SPECULAR);sl=node(m,unreal.MaterialExpressionSingleLayerWaterMaterialOutput)
 for pin,v in [('ScatteringCoefficients',(.0005,.0011,.0008)),('AbsorptionCoefficients',(.0032,.0018,.0014)),('ColorScaleBehindWater',(.97,1.,.97))]:assert ML.connect_material_expressions(vector(m,v),'',sl,pin)
 n=node(m,unreal.MaterialExpressionConstant);n.r=.18;ML.connect_material_expressions(n,'',sl,'PhaseG');finish(m)
 label='P2D_OrganicWater'if name=='Stream'else'P2D_Surface_Pond_Water';a=actors[label];a.modify();a.static_mesh_component.set_material(0,m)
save('WaterMaterials.json',dict(surfaces=2,pond_core_unchanged=True,flow_cm_per_second=18,no_extra_lights_or_water_surface=True))
