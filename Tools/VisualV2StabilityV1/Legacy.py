import unreal,json
from pathlib import Path
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.PrimitiveComponent):
  m=c.static_mesh if isinstance(c,unreal.StaticMeshComponent)else None
  if ('Tree'in a.get_actor_label()and'V2_Tree'not in a.get_actor_label())or(m and '/Engine/BasicShapes/'in m.get_path_name()and c.is_visible()):rows.append({'actor':a.get_actor_label(),'mesh':m.get_path_name()if m else None,'hidden':a.get_editor_property('bHidden'),'visible':c.is_visible(),'hidden_in_game':c.get_editor_property('hidden_in_game'),'pos':c.get_world_location().to_tuple(),'materials':[x.get_path_name()if x else None for x in c.get_materials()]})
(Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2StabilityV1/Legacy.json').write_text(json.dumps(rows,indent=2))
