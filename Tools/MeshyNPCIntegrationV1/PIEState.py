import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir()).resolve()/'Art/Characters/NPCs/IntegrationV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0) if w else None;pc=unreal.GameplayStatics.get_player_controller(w,0) if w else None
(P/'PIEState.json').write_text(json.dumps({'pie':bool(w),'map':w.get_path_name() if w else None,'viewport':list(pc.get_viewport_size()) if pc else None,'position':p.get_actor_location().to_tuple() if p else None},indent=2))
