"""Read the existing normal save after a fresh ordinary PIE start; no save writes."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/GlutexoEvolutionV2'/json.loads((R/'Saved/GlutexoEvolutionV2/ManualReviewRequest.json').read_text())['label']
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gi=unreal.GameplayStatics.get_game_instance(w)
s=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==gi);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi)
assert s.load_game()
team=[dict(id=c.instance_id.to_string(),species=c.species.get_path_name(),level=c.level,xp=c.experience)for c in e.get_player_party()]
unreal.SystemLibrary.execute_console_command(w,'pm.Evolution.Auto 1')
(D/'Restart.json').write_text(json.dumps(team,indent=2))
