"""Read-only runtime progress, usable while an asynchronous review runs."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):
 m=a.overworld_movement;rows.append({'id':str(a.encounter_id),'life':str(a.life_state),'position':a.get_actor_location().to_tuple(),'goal':m.current_goal.to_tuple(),'speed':m.current_speed,'distance':m.distance_travelled,'plans':m.successful_plans,'blocked_steps':m.blocked_steps,'rejected':m.rejected_targets,'escaping':m.escaping_defeat,'escape_blocked':m.escape_blocked,'escape_elapsed':m.escape_elapsed})
(R/'Saved/WildEncountersV2/LiveProgress.json').write_text(json.dumps(rows,indent=2));unreal.log(str(rows))
