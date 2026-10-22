import unreal,json,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2EnvironmentQualityV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world()
source='/Game/Maps/Dev_TestMap_VisualV2';target='/Game/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1';records={};world_configs={}
def path(o):return o.get_path_name() if o else None
def trans(t):return [list(t.translation.to_tuple()),[t.rotation.x,t.rotation.y,t.rotation.z,t.rotation.w],list(t.scale3d.to_tuple())]
def props(o,names):
 d={}
 for n in names:
  try:
   v=o.get_editor_property(n);d[n]=path(v) if isinstance(v,unreal.Object) else str(v)
  except:pass
 return d
for name in [source,target]:
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.load_map(name);w=e.get_editor_world();rows={};world_configs[name]=props(w.get_world_settings(),['default_game_mode','kill_z','global_gravity_z','enable_world_bounds_checks'])
 for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
  if a.get_class().get_name() in ['WorldSettings','BuoyancyManager','GameplayDebuggerPlayerManager','AbstractNavData']:continue
  row={'class':a.get_class().get_path_name(),'label':a.get_actor_label(),'transform':trans(a.get_actor_transform()),'props':props(a,['hidden','source_actor','idle_animation','walk_animation','conversation_animation','enable_motion_presentation','enable_accessory_motion','authored_walk_speed','dialogue','trainer_profile','encounter_profile','checkpoint_id','use_visual','use_relocated_interior','use_interior_camera','fade_duration']),'components':[]}
  for c in a.get_components_by_class(unreal.SceneComponent):
   cr={'name':c.get_name(),'class':c.get_class().get_path_name(),'transform':trans(c.get_world_transform()),'props':props(c,['cast_shadow','visible','hidden_in_game','static_mesh','skeletal_mesh_asset','sprite','collision_enabled','forced_lod_model','min_lod','instance_start_cull_distance','instance_end_cull_distance','intensity'])}
   if isinstance(c,unreal.PrimitiveComponent):cr['materials']=[path(c.get_material(i)) for i in range(c.get_num_materials())];cr['collision']=str(c.get_collision_enabled())
   if isinstance(c,unreal.SkeletalMeshComponent):cr['skeletal_mesh_asset']=path(c.get_skeletal_mesh_asset())
   if isinstance(c,unreal.InstancedStaticMeshComponent):cr['instances']=[trans(c.get_instance_transform(i,False)) for i in range(c.get_instance_count())]
   row['components'].append(cr)
  if isinstance(a,unreal.PostProcessVolume):row['pp']=props(a.get_editor_property('settings'),['override_bloom_intensity','bloom_intensity','override_motion_blur_amount','motion_blur_amount','override_auto_exposure_bias','auto_exposure_bias'])
  rows[a.get_name()]=row
 text=json.dumps(rows,sort_keys=True).replace(name+'.'+name.rsplit('/',1)[-1],'MAP_SELF').replace(name,'MAP_SELF');records[name]=json.loads(text)
 unreal.log('VEQ1_MAPCHECK_BEGIN '+name);unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');unreal.log('VEQ1_MAPCHECK_END '+name)
(O/'MapCopySignatures.json').write_text(json.dumps(records,indent=2))
assert world_configs[source]==world_configs[target],world_configs
A=records[source];B=records[target];diff={'missing':sorted(set(A)-set(B)),'extra':sorted(set(B)-set(A)),'changed':[n for n in A.keys()&B.keys() if A[n]!=B[n]]};assert not any(diff.values()),diff
out={'source':source,'target':target,'actors_compared':len(A),'differences':diff,'world_settings':world_configs,'original_saved':False,'dirty_maps':[path(x) for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[path(x) for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]};(O/'MapCopyAudit.json').write_text(json.dumps(out,indent=2));unreal.log('VEQ1_MAP_COPY_IDENTICAL '+str(len(A)))
