import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[];seen=set()
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  mesh=c.static_mesh
  if not mesh or mesh.get_path_name()in seen or not any(n in mesh.get_name()for n in ['Oak','Birch']):continue
  seen.add(mesh.get_path_name());d={'mesh':mesh.get_path_name(),'cpu_access':mesh.get_editor_property('allow_cpu_access')};rows.append(d)
(R/'Saved/OverworldAIV2/TreeCPU.json').write_text(json.dumps(rows,indent=2))
