import unreal,json
from pathlib import Path
E=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);rows=[]
for a in E.get_all_level_actors():
 for c in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
  if c.static_mesh and any(v in c.static_mesh.get_name().lower()for v in ['tree','oak','pine','willow','birch']):
   for i in range(c.get_instance_count()):
    t=c.get_instance_transform(i,True)
    if t.translation.x < -4000:rows.append(dict(actor=a.get_actor_label(),mesh=c.static_mesh.get_name(),xyz=t.translation.to_tuple()))
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not isinstance(c,unreal.InstancedStaticMeshComponent) and c.static_mesh and any(v in c.static_mesh.get_name().lower()for v in ['tree','oak','pine','willow','birch']):
   if c.get_world_location().x < -4000:rows.append(dict(actor=a.get_actor_label(),mesh=c.static_mesh.get_name(),xyz=c.get_world_location().to_tuple()))
(Path(unreal.Paths.project_dir())/'Saved/CreaturePolishV4/Sites.json').write_text(json.dumps(rows,indent=2))
