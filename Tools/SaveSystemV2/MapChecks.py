"""Reuse the existing read-only twelve-map check, with isolated evidence paths."""
import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve()
source=(R/'Tools/GameplayPraxisV1/MapChecks.py').read_text().replace('Saved/ProjectRefinement/GameplayPraxisV1','Saved/ProjectRefinement/SaveSystemV2').replace('PRAXIS_MAPCHECK_','SAVEV2A_MAPCHECK_').replace('MapChecks.json','MapChecks_A.json')
exec(compile(source,'existing_readonly_map_checks_save_v2','exec'),globals())
