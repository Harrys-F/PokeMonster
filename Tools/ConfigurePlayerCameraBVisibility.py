"""Adapt only the two existing scoped tree-reveal materials; never saves a map."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CameraB_20261013';D='/Game/Environment/DevTestMapVisualV2/Materials';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();L=unreal.MaterialEditingLibrary
path=D+'/MPC_PlayerSight';mpc=unreal.load_asset(path)
if not mpc:
 mpc=unreal.AssetToolsHelpers.get_asset_tools().create_asset('MPC_PlayerSight',D,unreal.MaterialParameterCollection,unreal.MaterialParameterCollectionFactoryNew());assert mpc
 params=[]
 for name,value in [('PlayerSightTarget',unreal.LinearColor(0,0,0,0)),('PlayerSightShape',unreal.LinearColor(55,110,0,0))]:
  p=unreal.CollectionVectorParameter();p.set_editor_property('parameter_name',name);p.set_editor_property('default_value',value);params.append(p)
 mpc.set_editor_property('vector_parameters',params);assert unreal.EditorAssetLibrary.save_loaded_asset(mpc,False)
params=list(mpc.get_editor_property('vector_parameters'))
if not any(p.get_editor_property('parameter_name')=='PlayerSightCamera' for p in params):
 p=unreal.CollectionVectorParameter();p.set_editor_property('parameter_name','PlayerSightCamera');p.set_editor_property('default_value',unreal.LinearColor(0,0,0,0));params.append(p);mpc.set_editor_property('vector_parameters',params);assert unreal.EditorAssetLibrary.save_loaded_asset(mpc,False)
updated=[]
for name in ['M_V2_CrownReveal','M_V2_BarkRevealBase']:
 m=unreal.load_asset(D+'/'+name);assert m
 f=next(x for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom) if x.get_outer()==m and 'corridor' in x.get_editor_property('code'))
 inputs=[]
 for key in ['P','C','F','Shape','Strength']:
  x=unreal.CustomInput();x.set_editor_property('input_name',key);inputs.append(x)
 f.set_editor_property('inputs',inputs)
 root='*smoothstep(F.z-70,F.z-25,P.z)' if 'Bark' in name else ''
 code='''if(F.w<.5 || Strength<=0)return 1;
float3 Eye=C.xyz; float3 v=F.xyz-Eye; float vv=dot(v,v); if(vv<1)return 1;
float t=dot(P-Eye,v)/vv;
if(t<=.06 || t>=.995)return 1;
float d=length((P-Eye)-t*v);
float inner=Shape.x*t; float outer=max(inner+.01,Shape.y*t);
float corridor=(1-smoothstep(inner,outer,d))*smoothstep(.06,.10,t)*(1-smoothstep(.97,.995,t))ROOT;
return lerp(1,.025,saturate(corridor*Strength));'''.replace('ROOT',root)
 f.set_editor_property('code',code)
 pos=next(x for x in unreal.ObjectIterator(unreal.MaterialExpressionWorldPosition) if x.get_outer()==m);cam=next(x for x in unreal.ObjectIterator(unreal.MaterialExpressionCameraPositionWS) if x.get_outer()==m)
 assert L.connect_material_expressions(pos,'',f,'P')
 for pname,pin in [('PlayerSightTarget','F'),('PlayerSightShape','Shape'),('PlayerSightCamera','C')]:
  n=next((x for x in unreal.ObjectIterator(unreal.MaterialExpressionCollectionParameter) if x.get_outer()==m and x.get_editor_property('parameter_name')==pname),None)
  if not n:n=L.create_material_expression(m,unreal.MaterialExpressionCollectionParameter,-850,1000 if pin=='F' else 1150)
  n.set_editor_property('collection',mpc);n.set_editor_property('parameter_name',pname);assert L.connect_material_expressions(n,'',f,pin)
 strength=next((x for x in unreal.ObjectIterator(unreal.MaterialExpressionScalarParameter) if x.get_outer()==m and x.get_editor_property('parameter_name')=='PlayerRevealStrength'),None)
 if not strength:strength=L.create_material_expression(m,unreal.MaterialExpressionScalarParameter,-850,1300)
 strength.set_editor_property('parameter_name','PlayerRevealStrength');strength.set_editor_property('default_value',0.0);assert L.connect_material_expressions(strength,'',f,'Strength')
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);updated.append(m.get_path_name())
(O/'MaterialConfiguration.json').write_text(json.dumps({'updated_materials':updated,'collection':mpc.get_path_name(),'radii_at_target_cm':[55,110],'finite_cone_t':[.06,.995],'editor_default_strength':0,'maps_saved':False},indent=2))
