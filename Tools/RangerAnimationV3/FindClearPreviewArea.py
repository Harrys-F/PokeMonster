import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh:continue
  n=c.static_mesh.get_name();kind='tree' if any(x in n for x in ['Oak','Birch','FruitTree','Tree_']) else 'rock' if 'Rock' in n else 'building' if any(x in n for x in ['Roof','Wall','Foundation']) else None
  if not kind:continue
  ts=[c.get_instance_transform(i,True) for i in range(c.get_instance_count())] if isinstance(c,unreal.InstancedStaticMeshComponent) else [c.get_world_transform()]
  for t in ts:rows.append({'mesh':n,'kind':kind,'p':t.translation.to_tuple()})
(R/'Saved/RangerAnimationV3/Obstacles.json').write_text(json.dumps(rows,indent=2))
