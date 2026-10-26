"""Read-only twelve-map check via the existing tool, separate evidence for phase B."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve()
s=(R/'Tools/GameplayPraxisV1/MapChecks.py').read_text().replace('Saved/ProjectRefinement/GameplayPraxisV1','Saved/ProjectRefinement/LearnMovesV1').replace('PRAXIS_MAPCHECK_','LEARNV1_MAPCHECK_').replace('MapChecks.json','MapChecks_B.json');exec(compile(s,'existing_map_checks_phase_b','exec'),globals())
