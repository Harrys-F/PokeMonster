"""Reuse all twelve map checks without saving or mutating any map."""
import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();source=(R/'Tools/GameplayPraxisV1/MapChecks.py').read_text().replace('Saved/ProjectRefinement/GameplayPraxisV1','Saved/ProjectRefinement/WorldClockV1').replace('PRAXIS_MAPCHECK_','WORLD_CLOCK_MAPCHECK_')
exec(compile(source,'world_clock_existing_map_checks','exec'),globals())
