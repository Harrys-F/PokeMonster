"""Reuse the verified full input/physics route, changing only the local evidence destination."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve()
s=(R/'Tools/VisualV2EnvironmentV3/Footrun.py').read_text().replace('Saved/ProjectRefinement/EnvironmentV3/FootrunFinal','Saved/ProjectRefinement/LightingV31/Footrun')
exec(compile(s,'existing_VisualV2_input_physics_route','exec'),globals())
