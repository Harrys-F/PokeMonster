"""Read-only target-map geometry and decoration audit."""
import unreal,json,sys,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
s=scene(W);(D/'SceneBefore.json').write_text(json.dumps(s,indent=2));out={'paths':[],'sprites':[],'flat_meshes':[],'landscapes':[],'reference_counts':{}}
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 if 'Landscape'in a.get_class().get_name():out['landscapes'].append(a.get_path_name())
 if isinstance(a,unreal.PaperSpriteActor):
  c=a.render_component;out['sprites'].append(dict(name=a.get_name(),label=a.get_actor_label(),visible=c.is_visible(),hidden_actor=a.get_editor_property('hidden'),hidden_component=c.get_editor_property('hidden_in_game'),collision=str(c.get_collision_enabled()),sprite=c.get_editor_property('source_sprite').get_path_name()if c.get_editor_property('source_sprite')else None,position=a.get_actor_location().to_tuple(),tags=[str(x)for x in a.tags]))
 if a.get_actor_label().startswith('V2_Path_'):
  c=a.static_mesh_component;dm,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(c.static_mesh,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());_,vs,_=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);ps=unreal.GeometryScript_List.convert_vector_list_to_array(vs);out['paths'].append(dict(name=a.get_name(),label=a.get_actor_label(),vertices=len(ps),bounds=str(c.get_local_bounds()),world_offset=a.get_actor_location().to_tuple(),collision=str(c.get_collision_enabled()),materials=[c.get_material(i).get_path_name()for i in range(c.get_num_materials())],mesh=c.static_mesh.get_path_name(),min_z=min(p.z for p in ps),max_z=max(p.z for p in ps)))
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh or not c.is_visible()or c.get_editor_property('hidden_in_game')or a.get_editor_property('hidden'):continue
  b=c.static_mesh.get_bounding_box();dims=(b.max-b.min).to_tuple()
  if min(dims)<1:out['flat_meshes'].append(dict(actor=a.get_actor_label(),mesh=c.static_mesh.get_path_name(),dimensions=dims))
(D/'GeometryAudit.json').write_text(json.dumps(out,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()

task=unreal.AssetExportTask();task.object=W;task.filename=str(D/'MapBefore.t3d');task.automated=True;task.prompt=False;task.replace_identical=True;task.exporter=unreal.LevelExporterT3D();assert unreal.Exporter.run_asset_export_task(task)
