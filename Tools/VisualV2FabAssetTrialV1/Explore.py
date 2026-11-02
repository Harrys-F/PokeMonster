import unreal,json,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();out={'actors':[],'paths':{}}
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 if a.get_actor_label().startswith(('V2_Path','V2_Fence','Refined','EQ3_')) or isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterRestPoint,unreal.PokeMonsterBuildingCutaway)):
  row=dict(label=a.get_actor_label(),position=a.get_actor_location().to_tuple(),type=a.get_class().get_name(),components=[])
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   row['components'].append(dict(mesh=c.static_mesh.get_path_name()if c.static_mesh else None,position=c.get_world_location().to_tuple(),count=c.get_instance_count()if isinstance(c,unreal.InstancedStaticMeshComponent)else 1,bounds=str(c.get_local_bounds()),materials=[c.get_material(i).get_path_name()if c.get_material(i)else None for i in range(c.get_num_materials())]))
  out['actors'].append(row)
for name in ['new_window_width','new_window_height','last_executed_play_mode_type','play_net_mode','play_number_of_clients']:
 try:out['paths'][name]=str(unreal.get_default_object(unreal.LevelEditorPlaySettings).get_editor_property(name))
 except Exception:pass
(D/'Explore.json').write_text(json.dumps(out,indent=2))
