import unreal,json
from pathlib import Path
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor):
 if not a.get_actor_label().startswith('TSP_'):continue
 c=a.static_mesh_component;rows.append({'actor':a.get_actor_label(),'hidden':c.get_editor_property('hidden_in_game'),'actor_hidden':a.get_editor_property('hidden'),'cast_hidden_shadow':c.get_editor_property('cast_hidden_shadow'),'collision':str(c.get_collision_enabled()),'cast_shadow':c.cast_shadow,'mesh':c.static_mesh.get_path_name()})
(Path(unreal.Paths.project_dir())/'Saved/TreeShadowProxyV1/RuntimeAudit.json').write_text(json.dumps(rows,indent=2))
