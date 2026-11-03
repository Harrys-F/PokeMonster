import unreal,json,sys,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
(D/'SceneBefore.json').write_text(json.dumps(scene(W),indent=2));rows=[];meshes={}
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 if a.get_editor_property('hidden'):continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh or not c.is_visible()or c.get_editor_property('hidden_in_game'):continue
  m=c.static_mesh;p=m.get_path_name();b=m.get_bounding_box()
  if p not in meshes:meshes[p]=dict(triangles=m.get_num_triangles(0),lods=m.get_num_lods(),size=(b.max-b.min).to_tuple(),materials=[x.material_interface.get_path_name()if x.material_interface else None for x in m.static_materials])
  ts=[c.get_instance_transform(i,True)for i in range(c.get_instance_count())]if isinstance(c,unreal.InstancedStaticMeshComponent)else[c.get_world_transform()]
  rows.append(dict(actor=a.get_name(),label=a.get_actor_label(),mesh=p,materials=[c.get_material(i).get_path_name()if c.get_material(i)else None for i in range(c.get_num_materials())],collision=str(c.get_collision_enabled()),instances=[dict(position=t.translation.to_tuple(),rotation=t.rotation.rotator().to_tuple(),scale=t.scale3d.to_tuple())for t in ts]))
(D/'Inventory.json').write_text(json.dumps(dict(rows=rows,meshes=meshes),indent=2));cuts=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterBuildingCutaway):cuts.append(dict(label=a.get_actor_label(),door=a.door_threshold.get_world_location().to_tuple(),door_rotation=a.door_threshold.get_world_rotation().to_tuple(),relocated=a.relocated_door_threshold.get_world_location().to_tuple(),properties={k:str(a.get_editor_property(k))for k in ['use_relocated_interior','use_interior_camera']}))
(D/'Buildings.json').write_text(json.dumps(cuts,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
