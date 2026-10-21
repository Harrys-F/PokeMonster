"""Existing isolated battle/save regression; free wild movement is tested separately."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True)
runpy.run_path(str(R/'Tools/StarterExpansionV1/ReviewModels.py'),run_name='__main__')
