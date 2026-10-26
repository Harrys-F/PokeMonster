"""Read collision settings of existing obstacles; never creates or edits a world object."""
import unreal,json
from pathlib import Path
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.PrimitiveComponent):
  if c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION:continue
  label=a.get_actor_label();name=c.get_name()
  if any(x in(label+' '+name).lower()for x in ['house','heal','stone','boulder','rock','tree','fence']):
   bounds=a.get_actor_bounds(True,False);rows.append({'actor':label,'component':name,'enabled':str(c.get_collision_enabled()),'pawn':str(c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)),'center':bounds[0].to_tuple(),'extent':bounds[1].to_tuple(),'class':c.get_class().get_name()})
R=Path(unreal.Paths.project_dir()).resolve();(R/'Saved/ProjectRefinement/GameplayPraxisV1/CollisionInventory.json').write_text(json.dumps(rows,indent=2))
