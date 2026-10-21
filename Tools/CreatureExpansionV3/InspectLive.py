"""Read-only native overworld/battle observer; no state mutation."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):
 if 'CreatureExpansionV3'not in [str(t)for t in a.tags]:continue
 m=a.overworld_movement;rows.append(dict(species=str(a.visual_species.get_internal_id()),position=a.get_actor_location().to_tuple(),life=str(a.life_state),distance=m.distance_travelled,speed=m.current_speed,plans=m.successful_plans,blocked=m.blocked_steps))
(R/'Saved/CreatureExpansionV3/LiveState.json').write_text(json.dumps(dict(time=time.time(),battle=e.is_encounter_active(),rows=rows),indent=2))
