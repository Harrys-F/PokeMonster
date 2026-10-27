import unreal,json
from pathlib import Path
L=unreal.MaterialEditingLibrary;rows=[]
for p in ['/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass','/Game/Environment/VisualV2WorldArtV7/Materials/M_WA7_Ground','/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Ground']:
 m=unreal.load_asset(p);r={'path':p,'shading':str(m.get_editor_property('shading_model')),'statistics':str(L.get_statistics(m)),'nodes':[]}
 for n in L.get_material_expressions(m):
  d={'class':n.get_class().get_name()}
  for k in ['code','texture','parameter_name']:
   try:v=n.get_editor_property(k);d[k]=v.get_path_name()if isinstance(v,unreal.Object)else str(v)
   except Exception:pass
  r['nodes'].append(d)
 rows.append(r)
(Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2StabilityV1/MaterialCandidates.json').write_text(json.dumps(rows,indent=2))
