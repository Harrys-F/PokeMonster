import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world()
d={'world':w.get_path_name(),'game_world':str(e.get_game_world()),'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'actors':[]}
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 row={'label':a.get_actor_label(),'class':a.get_class().get_path_name(),'transform':str(a.get_actor_transform()),'components':[]}
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  row['components'].append({'name':c.get_name(),'mesh':c.static_mesh.get_path_name() if c.static_mesh else None,'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())],'transform':str(c.get_world_transform()),'shadow':c.cast_shadow,'instances':c.get_instance_count() if isinstance(c,unreal.InstancedStaticMeshComponent) else None})
 d['actors'].append(row)
(O/'InitialEditor.json').write_text(json.dumps(d,indent=2));unreal.log('ENV3_INITIAL_AUDIT '+json.dumps({k:v for k,v in d.items() if k!='actors'}))
