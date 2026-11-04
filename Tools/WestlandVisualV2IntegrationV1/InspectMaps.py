"""Read-only direct editor comparison; no saves or asset changes."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
result={};mats={};meshes={}
for name in ['Dev_TestMap_VisualV2','Dev_WestlandRegion']:
 assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/'+name);W=E.get_editor_world();assert not(D/(name+'_Before.json')).exists();(D/(name+'_Before.json')).write_text(json.dumps(scene(W),indent=2));rows=[]
 for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   sm=c.static_mesh
   if not sm:continue
   rows.append(dict(name=a.get_name(),label=a.get_actor_label(),component=c.get_name(),mesh=sm.get_path_name(),materials=[c.get_material(i).get_path_name()if c.get_material(i)else None for i in range(c.get_num_materials())],count=c.get_instance_count()if isinstance(c,unreal.InstancedStaticMeshComponent)else 1,location=c.get_world_location().to_tuple(),collision=str(c.get_collision_enabled())))
   if sm.get_path_name()not in meshes:
    box=sm.get_bounding_box();meshes[sm.get_path_name()]=dict(min=box.min.to_tuple(),max=box.max.to_tuple(),triangles=sm.get_num_triangles(0),slots=len(sm.static_materials))
   for i in range(c.get_num_materials()):
    m=c.get_material(i)
    if not m or m.get_path_name()in mats:continue
    entry=dict(type=m.get_class().get_name())
    if isinstance(m,unreal.Material):
     entry['properties']={}
     for k in ['blend_mode','shading_model','two_sided','translucency_lighting_mode','screen_space_reflections','used_with_instanced_static_meshes']:
      try:entry['properties'][k]=str(m.get_editor_property(k))
      except Exception:pass
     entry['nodes']=[]
     for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
      v=dict(type=n.get_class().get_name())
      for k in ['code','parameter_name','default_value','texture','r']:
       try:
        x=n.get_editor_property(k);v[k]=x.get_path_name()if isinstance(x,unreal.Object)else str(x)
       except Exception:pass
      entry['nodes'].append(v)
    elif isinstance(m,unreal.MaterialInstanceConstant):entry.update(parent=m.parent.get_path_name(),scalars=str(m.scalar_parameter_values),vectors=str(m.vector_parameter_values))
    mats[m.get_path_name()]=entry
 functional=[]
 for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
  if not a.get_class().get_path_name().startswith('/Script/PokeMonster.')and a.get_class().get_name()!='PlayerStart':continue
  row=dict(name=a.get_name(),label=a.get_actor_label(),class_name=a.get_class().get_name(),position=a.get_actor_location().to_tuple(),rotation=a.get_actor_rotation().to_tuple(),tags=[str(x)for x in a.tags],properties={},components=[])
  for k in ['display_name','dialogue','source_actor','idle_animation','walk_animation','conversation_animation','checkpoint_id','profile','encounter_id','zone_id','habitat_type','maximum_population','medium','water_surface_z','water_draft_cm','minimum_depth_cm','elliptical_boundary','travel_points','allow_natural_activities','use_relocated_interior','use_interior_camera','use_shadowless_interior_lighting','stable_doorway_transition','constrain_third_person_to_room','doorway_landing_distance','interior_camera_boundary_margin','occluding_actors','distance_based_bush_encounters','habitat_zone_id','seed']:
   try:
    v=a.get_editor_property(k);row['properties'][k]=v.get_path_name()if isinstance(v,unreal.Object)else str(v)
   except Exception:pass
  for c in a.get_components_by_class(unreal.SceneComponent):
   cr=dict(name=c.get_name(),class_name=c.get_class().get_name(),position=c.get_world_location().to_tuple(),rotation=c.get_world_rotation().to_tuple())
   if isinstance(c,unreal.BoxComponent):cr['extent']=c.get_unscaled_box_extent().to_tuple()
   row['components'].append(cr)
  functional.append(row)
 result[name]=rows;result[name+'_functional']=functional
result['materials']=mats;result['meshes']=meshes;(D/'Inventory.json').write_text(json.dumps(result,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();unreal.log('WESTLAND_VISUAL_READONLY_INVENTORY_DONE')
