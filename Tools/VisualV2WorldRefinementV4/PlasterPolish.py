"""Remove the visibly repeated old plaster source pattern; edit only own V4 graph."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/MaterialHelpers.py')))
m=new('Plaster');P=node(m,unreal.MaterialExpressionWorldPosition);N=node(m,unreal.MaterialExpressionVertexNormalWS)
uv=custom(m,'float3 a=abs(N);return (a.z>.55?P.xy:(a.x>a.y?P.yz:P.xz))/85;',{'P':(P,''),'N':(N,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2)
n=sample(m,ROOT+'/Textures/T_WR4_PlasterMicroNormal',uv,True)
c=custom(m,'float v=.011*sin(P.x*.037+sin(P.z*.023))+.007*sin(P.y*.081+P.z*.064);return float3(.70,.642,.526)+v;',{'P':(P,'')});ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);ML.connect_material_property(n,'RGB',unreal.MaterialProperty.MP_NORMAL);scalar(m,.94,unreal.MaterialProperty.MP_ROUGHNESS);finish(m);save('PlasterPolish.json',dict(rejected='Regular chevron pattern in inherited painted-plaster base colour',replacement='Own low-contrast warm lime plaster and fine micro-normal'))
