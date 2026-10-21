"""Read-only saved actor configuration plus native transient ground/route queries."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):
 if 'CreatureExpansionV3'not in [str(t)for t in a.tags]:continue
 c=a.get_component_by_class(unreal.CapsuleComponent);hh=c.get_scaled_capsule_half_height();m=a.overworld_movement;m.configure(a.visual_species,hh,c.get_scaled_capsule_radius(),hh,None,a.seed);g=a.get_actor_location()-unreal.Vector(0,0,hh);directions=[]
 for i in range(8):
  goal=m.project_walkable(g+unreal.Vector(math.cos(i*math.tau/8)*200,math.sin(i*math.tau/8)*200,0));ok=goal is not None and m.can_traverse(g,goal);directions.append(dict(direction=i,valid=bool(ok),goal=goal.to_tuple()if goal else None))
 rows.append(dict(species=str(a.visual_species.get_internal_id()),ground=g.to_tuple(),routes=directions,reachable=sum(x['valid']for x in directions)))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(R/'Saved/CreatureExpansionV3/HabitatConnections.json').write_text(json.dumps(rows,indent=2))
