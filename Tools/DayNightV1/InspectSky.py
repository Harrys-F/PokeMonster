"""Read Engine sky assets only; no spawn or material edit in baseline world."""
import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir());m=unreal.load_asset('/Engine/EngineSky/M_Sky_Panning_Clouds2');mesh=unreal.load_asset('/Engine/EngineSky/SM_SkySphere');o={'material':m.get_path_name()if m else None,'mesh':mesh.get_path_name()if mesh else None}
if m:
 for kind in ['scalar','vector','texture']:
  fn=getattr(unreal.MaterialEditingLibrary,'get_'+kind+'_parameter_names');o[kind]=[str(n)for n in fn(m)]
(r/'Saved/ProjectRefinement/DayNightV1/SkyAssets.json').write_text(json.dumps(o,indent=2))
