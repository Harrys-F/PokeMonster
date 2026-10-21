"""Read-only movement/obstacle inventory of the existing VisualV2 editor world."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2';rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 n=a.get_actor_label();cl=a.get_class().get_name()
 if not(any(t in n.lower()for t in ['water','river','fluss','bridge','wild','zunder','playerstart'])or 'WildCreature'in cl):continue
 center,extent=a.get_actor_bounds(False);rows.append({'name':n,'class':cl,'location':a.get_actor_location().to_tuple(),'center':center.to_tuple(),'extent':extent.to_tuple(),'tags':[str(t)for t in a.tags],'components':[{'class':c.get_class().get_name(),'mesh':c.static_mesh.get_path_name()if isinstance(c,unreal.StaticMeshComponent)and c.static_mesh else None,'collision':str(c.get_collision_enabled())}for c in a.get_components_by_class(unreal.PrimitiveComponent)]})
p=R/'Saved/StarterExpansionV1/WorldInventory.json';assert not p.exists();p.write_text(json.dumps(rows,indent=2));unreal.log('STARTER_WORLD_INVENTORY '+str(len(rows)))
