"""Final read-only checks after PIE; all twelve existing maps, no package saves."""
import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve()
source=(R/'Tools/GameplayPraxisV1/MapChecks.py').read_text().replace('Saved/ProjectRefinement/GameplayPraxisV1','Saved/ProjectRefinement/WorldClockV1').replace('PRAXIS_MAPCHECK_','WORLD_CLOCK_FINAL_MAPCHECK_').replace('MapChecks.json','FinalMapChecks.json')
exec(compile(source,'world_clock_final_map_checks','exec'),globals())
