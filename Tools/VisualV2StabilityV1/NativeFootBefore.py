import unreal,json
from pathlib import Path
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);assert not P.is_overworld_input_locked()and not PC.is_menu_open();(Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2StabilityV1/NativeFootBefore.json').write_text(json.dumps({'position':P.get_actor_location().to_tuple(),'world':W.get_name()}))
