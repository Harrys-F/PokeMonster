"""Use existing manual evolution review; seed only an explicitly isolated runtime team if user save has no eligible species."""
import unreal,json
from pathlib import Path
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and hasattr(unreal,'_praxis_guard');P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t)
fixture=False
if not any(str(c.species.get_internal_id())in ['Zunderlauf','Glutexo']for c in E.get_player_party()):
 # End the first preview without writing; prepare the existing explicit party fixture,
 # then re-enter the same RAM transport. No normal save is replaced or restored.
 G=unreal._praxis_guard['ground'];assert G.return_to_world();cmd('pm.EvolutionReview.Party Zunderlauf 15');position=P.get_actor_transform();assert G.visit(0);P.set_actor_transform(position,False,True);assert S.save_current_game();fixture=True
cmd('pm.Evolution.Auto 1');(unreal._praxis_guard['output']/'EvolutionSetup.json').write_text(json.dumps({'user_save_has_no_eligible_fire_species':fixture,'explicit_existing_runtime_party_fixture':fixture,'disk_save_changed':False},indent=2))
