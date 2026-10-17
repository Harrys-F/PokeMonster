import unreal,json
from pathlib import Path
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_TreeShadowProxyV1';rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor):
 if not a.get_actor_label().startswith('TSP_'):continue
 c=a.static_mesh_component;c.set_collision_profile_name('NoCollision');c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);c.set_editor_property('generate_overlap_events',False);assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;rows.append({'actor':a.get_actor_label(),'collision_profile':str(c.get_collision_profile_name()),'collision_enabled':str(c.get_collision_enabled())})
assert len(rows)==6;assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level();(Path(unreal.Paths.project_dir())/'Saved/TreeShadowProxyV1/CollisionFix.json').write_text(json.dumps(rows,indent=2))
