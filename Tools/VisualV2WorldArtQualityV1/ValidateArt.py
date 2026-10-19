"""Read-only saved-scene and new-decoration validation; no art quality claim from geometry counts."""
import unreal,json,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2';sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
actual=scene(w);expected=json.loads((S/'AfterScene.json').read_text());assert actual==expected,'Unexpected editor/actor changes';out=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 if not a.get_actor_label().startswith('WAQ1_'):continue
 c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.cast_shadow;mesh=c.get_editor_property('static_mesh');mats=[]
 for i in range(c.get_num_materials()):
  mat=c.get_material(i);parent=mat
  while isinstance(parent,unreal.MaterialInstance):parent=parent.parent
  assert parent.used_with_instanced_static_meshes;mats.append(mat.get_path_name())
 out.append({'label':a.get_actor_label(),'instances':c.get_instance_count(),'mesh':mesh.get_path_name(),'lod_triangles':[mesh.get_num_triangles(i) for i in range(mesh.get_num_lods())],'material_slots':c.get_num_materials(),'materials':mats,'collision':str(c.get_collision_enabled()),'shadow':c.cast_shadow,'culling_cm':[c.instance_start_cull_distance,c.instance_end_cull_distance]})
assert len(out)==6 and sum(x['instances'] for x in out)==175
state={'world':w.get_path_name(),'actor_count':len(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)),'new_groups':out,'scene_matches_saved_design':True,'new_meshes':0,'new_textures':0,'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_assets':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]};assert not state['dirty_maps'] and not state['dirty_assets'];(S/'Validation.json').write_text(json.dumps(state,indent=2));unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
