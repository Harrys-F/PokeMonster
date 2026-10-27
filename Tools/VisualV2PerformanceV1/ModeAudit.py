import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';L=unreal.MaterialEditingLibrary;rows=[]
for name in ['Ground','MainPath','NorthPath']:
 m=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_'+name);data={'name':name,'scalar_parameters':{},'mode_sources':[]}
 for key in L.get_scalar_parameter_names(m):data['scalar_parameters'][str(key)]=L.get_material_default_scalar_parameter_value(m,key)
 for x in L.get_material_expressions(m):
  if not isinstance(x,unreal.MaterialExpressionCustom)or not any(str(i.get_editor_property('input_name'))=='Mode'for i in x.get_editor_property('inputs')):continue
  data['mode_sources'].append({'node':x.get_name(),'inputs':[str(i.get_editor_property('input_name'))for i in x.get_editor_property('inputs')],'providers':[{'class':p.get_class().get_name(),'name':p.get_name(),'value':str(p.get_editor_property('default_value'))if isinstance(p,unreal.MaterialExpressionScalarParameter)else str(p.get_editor_property('r'))if isinstance(p,unreal.MaterialExpressionConstant)else None}for p in L.get_inputs_for_material_expression(m,x)]})
 rows.append(data)
(D/'ModeAudit.json').write_text(json.dumps(rows,indent=2))
