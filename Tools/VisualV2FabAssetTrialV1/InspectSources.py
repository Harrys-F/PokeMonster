import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';out={}
for p in ['/Game/Environment/PokemonAIV3/Materials/M_AIV3RiverConnection','/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_MainPath','/Game/Environment/VisualV2PerformanceV1/Materials/M_PV1_BakedGroundSRGB']:
 m=unreal.load_asset(p);out[p]=dict(blend=str(m.blend_mode),nodes=[])
 for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
  v=dict(type=n.get_class().get_name())
  for k in ['code','parameter_name','texture','r','a','b']:
   try:
    x=n.get_editor_property(k);v[k]=x.get_path_name()if isinstance(x,unreal.Object)else str(x)
   except Exception:pass
  out[p]['nodes'].append(v)
(D/'MaterialSources.json').write_text(json.dumps(out,indent=2))
