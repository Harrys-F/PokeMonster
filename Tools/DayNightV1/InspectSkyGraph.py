"""Read-only inspection of the reused Engine sky material graph and defaults."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();M=unreal.load_asset('/Engine/EngineSky/M_Sky_Panning_Clouds2');L=unreal.MaterialEditingLibrary;result={'scalar':{},'vector':{},'nodes':[]}
for kind in ['scalar','vector']:
 for name in getattr(L,'get_'+kind+'_parameter_names')(M):result[kind][str(name)]=str(getattr(L,'get_material_default_'+kind+'_parameter_value')(M,name))
for n in L.get_material_expressions(M):
 r={'name':n.get_name(),'class':n.get_class().get_name(),'inputs':[x.get_name()if x else None for x in L.get_inputs_for_material_expression(M,n)],'input_names':[str(x)for x in L.get_material_expression_input_names(n)]}
 for p in ['parameter_name','default_value','constant','r','g','b','a','const_a','const_b','texture','desc']:
  try:r[p]=str(n.get_editor_property(p))
  except Exception:pass
 result['nodes'].append(r)
result['emissive']=L.get_material_property_input_node(M,unreal.MaterialProperty.MP_EMISSIVE_COLOR).get_name();(R/'Saved/ProjectRefinement/DayNightV1/SkyGraph.json').write_text(json.dumps(result,indent=2))
