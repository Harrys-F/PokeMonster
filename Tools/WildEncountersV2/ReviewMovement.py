"""Existing movement/sprint acceptance with the explicit three-member habitat enabled."""
import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve()
source=(R/'Tools/OverworldAIV2/ReviewMovement.py').read_text().replace('assert len(wild)==3','assert len(wild)==5')
exec(compile(source,'current_wild_groups_movement_review','exec'),globals())
