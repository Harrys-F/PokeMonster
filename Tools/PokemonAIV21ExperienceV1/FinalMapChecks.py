"""Final checks, preserve the earlier A-stage result file."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve()
s=(R/'Tools/GameplayPraxisV1/MapChecks.py').read_text().replace('Saved/ProjectRefinement/GameplayPraxisV1','Saved/ProjectRefinement/PokemonAIV21ExperienceV1').replace('PRAXIS_MAPCHECK_','AIV21_FINAL_MAPCHECK_').replace('MapChecks.json','FinalMapChecks.json')
exec(compile(s,'aiv21_final_existing_map_checks','exec'),globals())
