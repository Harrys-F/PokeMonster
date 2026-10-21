import unreal,json
from pathlib import Path
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();r=dict(pie=bool(w))
if w:
 p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);d=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem)if x.get_outer()==gi);r.update(player=p.get_actor_location().to_tuple(),locked=p.is_overworld_input_locked(),menu=pc.is_menu_open(),encounter=e.is_encounter_active(),last_outcome=str(e.get_last_result().outcome))
(Path(unreal.Paths.project_dir())/'Saved/CreaturePolishV4/RuntimeState.json').write_text(json.dumps(r,indent=2))
