import unreal,json,time
from pathlib import Path
D=Path(unreal.Paths.project_dir()).resolve()/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==W);assert G.visit_target('Modell:Aquana');start=time.monotonic()
def tick(dt):
 if time.monotonic()-start<1:return
 unreal.unregister_slate_post_tick_callback(unreal._v6_modelprobe);rows=[]
 for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.StaticMeshActor):
  c=a.static_mesh_component
  if c.static_mesh and 'ModelIntakeV6'in c.static_mesh.get_path_name():rows.append(dict(path=a.get_path_name(),bounds=str(a.get_actor_bounds(False)),location=a.get_actor_location().to_tuple(),collision=str(c.get_collision_enabled()),expected=str(unreal.CollisionEnabled.NO_COLLISION),mesh=c.static_mesh.get_path_name()))
 (D/'ModelProbe.json').write_text(json.dumps(rows,indent=2));unreal.SystemLibrary.execute_console_command(W,'Shot filename="'+str(D/'ModelProbe.png')+'" -nosuffix');G.return_to_world()
unreal._v6_modelprobe=unreal.register_slate_post_tick_callback(tick)
