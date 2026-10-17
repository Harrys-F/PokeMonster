"""Read-only actor/component and complete postprocess-settings signature."""
import unreal

def scene(world):
 def path(o):return o.get_path_name() if o else None
 def trans(t):return [list(t.translation.to_tuple()),[t.rotation.x,t.rotation.y,t.rotation.z,t.rotation.w],list(t.scale3d.to_tuple())]
 def props(o,names):
  d={}
  for n in names:
   try:
    v=o.get_editor_property(n);d[n]=path(v) if isinstance(v,unreal.Object) else str(v)
   except Exception:pass
  return d
 rows={}
 for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor):
  if a.get_class().get_name() in ['WorldSettings','BuoyancyManager','GameplayDebuggerPlayerManager','AbstractNavData']:continue
  row={'class':a.get_class().get_path_name(),'label':a.get_actor_label(),'transform':trans(a.get_actor_transform()),'props':props(a,['hidden','source_actor','idle_animation','walk_animation','conversation_animation','enable_motion_presentation','enable_accessory_motion','authored_walk_speed','dialogue','trainer_profile','encounter_profile','checkpoint_id','use_visual','use_relocated_interior','use_interior_camera','fade_duration']),'components':[]}
  for c in a.get_components_by_class(unreal.SceneComponent):
   cr={'name':c.get_name(),'class':c.get_class().get_path_name(),'transform':trans(c.get_world_transform()),'props':props(c,['cast_shadow','visible','hidden_in_game','static_mesh','skeletal_mesh_asset','sprite','collision_enabled','forced_lod_model','min_lod','instance_start_cull_distance','instance_end_cull_distance','intensity'])}
   if isinstance(c,unreal.PrimitiveComponent):cr['materials']=[path(c.get_material(i)) for i in range(c.get_num_materials())];cr['collision']=str(c.get_collision_enabled())
   if isinstance(c,unreal.InstancedStaticMeshComponent):cr['instances']=[trans(c.get_instance_transform(i,False)) for i in range(c.get_instance_count())]
   row['components'].append(cr)
  if isinstance(a,unreal.PostProcessVolume):
   row['pp']=a.settings.export_text();row['pp_volume']=props(a,['unbound','priority','blend_weight','blend_radius','enabled'])
  rows[a.get_name()]=row
 return {'actors':rows,'world_settings':props(world.get_world_settings(),['default_game_mode','kill_z','global_gravity_z','enable_world_bounds_checks'])}
