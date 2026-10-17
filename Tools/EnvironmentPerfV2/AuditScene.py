import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV2';rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh:continue
  pos=a.get_actor_location()
  if c.static_mesh.get_name()=='Cube' and -5400<pos.x<-2500 and -1000<pos.y<1700:
   rows.append({'actor':a.get_actor_label(),'path':a.get_path_name(),'position':pos.to_tuple(),'scale':a.get_actor_scale3d().to_tuple(),'bounds':str(c.get_local_bounds()),'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())],'collision':str(c.get_collision_enabled())})
(O/'CubeCandidates.json').write_text(json.dumps(rows,indent=2))
