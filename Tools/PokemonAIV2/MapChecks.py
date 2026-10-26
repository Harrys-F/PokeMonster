"""Reuse all twelve map checks without saving or mutating any map."""
import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();source=(R/'Tools/GameplayPraxisV1/MapChecks.py').read_text().replace('Saved/ProjectRefinement/GameplayPraxisV1','Saved/ProjectRefinement/PokemonAIV2').replace('PRAXIS_MAPCHECK_','POKEMON_AI_MAPCHECK_')
exec(compile(source,'pokemon_ai_v2_existing_map_checks','exec'),globals())
