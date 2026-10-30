"""Observe original natural water AI and render configuration in an isolated native save directory."""
import unreal,json,time,traceback,shutil
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosWaterV2';q=json.loads((D/'Active.json').read_text());O=D/q['label'];s={'start':time.monotonic(),'phase':'init','at':0,'sample':0};r={'checks':[],'samples':[],'assets':{},'purpose':'Baseline observation; completed diagnosis is not a passed movement acceptance test'};W=PC=P=H=C=E=S=None
assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(O/'UserData')
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def encode(x):
 if isinstance(x,unreal.Object):return x.get_path_name()
 if hasattr(x,'to_tuple'):return x.to_tuple()
 if hasattr(x,'export_text'):return str(x.export_text())
 return str(x)
def props(x,names):
 d={}
 for n in names:
  try:d[n]=encode(x.get_editor_property(n))
  except Exception:pass
 return d
def inventory():
 a=unreal.load_asset('/Game/Data/Creatures/DA_Garados');d=a.get_visuals().presentation;m=d.mesh;r['assets']={'species':a.get_path_name(),'overworld':a.overworld.export_text(),'presentation':d.get_path_name(),'mesh':m.get_path_name(),'skeleton':m.skeleton.get_path_name(),'clips':{str(k):v.get_path_name()for k,v in d.clips.items()},'swimming':props(d,['swim_idle_clip','swim_clip','swim_reference_speed','rig_family','reference_size_cm','ground_offset_cm']),'materials':[str(x.material_interface.get_path_name())for x in m.materials],'bounds':m.get_bounds().export_text(),'bone_names':[]}
 for c in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterCreatureVisualActor):
  if c.mesh.get_skeletal_mesh_asset()==m:r['assets']['bone_names']=[str(n)for n in c.mesh.get_all_socket_names()];break
 r['rendering']={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.ScreenPercentage','r.TemporalAA.Upsampling','r.Shadow.Virtual.SMRT.RayCountDirectional']}
def sample():
 rows=[]
 for a in H.population:
  if str(a.visual_species.get_internal_id())not in ['Garados','Karpador']:continue
  m=a.overworld_movement;v=next((x for x in a.get_attached_actors()if isinstance(x,unreal.PokeMonsterCreatureVisualActor)),None);cap=a.get_component_by_class(unreal.CapsuleComponent);foot=a.get_actor_location()-unreal.Vector(0,0,cap.get_scaled_capsule_half_height());row={'species':str(a.visual_species.get_internal_id()),'actor':a.get_path_name(),'seed':a.seed,'position':a.get_actor_location().to_tuple(),'foot':foot.to_tuple(),'hidden':a.get_editor_property('hidden'),'movement_tick':m.is_component_tick_enabled(),'clock_paused':C.is_clock_paused(),'water_draft':m.water_draft_override_cm,'inside':m.is_inside_habitat(foot),**props(m,['current_speed','distance_travelled','successful_plans','blocked_steps','rejected_targets','behavior_state','b_activity_running','activity_remaining','activity_decisions','b_activity_distant','b_activities_enabled','settings'])}
  if v:row.update(mesh=v.mesh.get_skeletal_mesh_asset().get_path_name(),aquatic=v.aquatic_pose_alpha,visual_motion=v.motion_speed,head=v.mesh.get_socket_location('head').to_tuple())
  if str(a.visual_species.get_internal_id())=='Garados':
   z=m.biome_habitat;row['habitat']=z.get_actor_location().to_tuple();row['travel_points']=[]
   for p in z.travel_points:
    target=z.get_actor_transform().transform_location(p);g=m.project_walkable(target);row['travel_points'].append({'target':target.to_tuple(),'projection':encode(g),'traverse':m.can_traverse(foot,unreal.Vector(target.x,target.y,foot.z))})
  rows.append(row)
 r['samples'].append({'seconds':time.monotonic()-s['at'],'player':P.get_actor_location().to_tuple(),'water':rows})
def finish(error=None):
 try:
  cmd('csvprofile stop');src=Path(unreal.Paths.project_saved_dir())/'Profiling/CSV/GaradosWaterV2_Baseline.csv'
  if src.exists():shutil.copyfile(src,O/'Performance.csv')
 except Exception:r['csv_note']=traceback.format_exc()
 distances={n:max([float(x['distance_travelled'])for row in r['samples']for x in row['water']if x['species']==n]+[0])for n in ['Garados','Karpador']}
 if q.get('require_movement')and error is None:
  final={x['species']:x for x in r['samples'][-1]['water']}
  if set(final)!=set(['Garados','Karpador'])or any(float(x['distance_travelled'])<=20 for x in final.values()):error='Original water_check criterion failed: both current swimmers must travel more than 20 cm'
  for row in r['samples']:
   for x in row['water']:
    if not x['inside']or abs(x['foot'][2]-(4.2-x['water_draft']))>.1 or x.get('aquatic')!=1:error='Original water_sample boundary/immersion criterion failed'
  if error is None:r['checks'].append('Original water_check and water_sample criteria retained: both current fish >20 cm; every foot inside at correct draft with aquatic pose')
 r.update(passed=error is None,error=error,observed_distance_cm=distances,natural_garados_movement_observed=distances['Garados']>20,seconds=time.monotonic()-s['start']);unreal.unregister_slate_post_tick_callback(unreal._garados_baseline);(O/'Result.json').write_text(json.dumps(r,indent=2,default=str))
 if W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,PC,P,H,C,E,S
 try:
  now=time.monotonic();assert now-s['start']<160
  if s['phase']=='init':
   if now-s['start']<12:return
   ws=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not ws:return
   W=ws[0];PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W);H=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterHabitatSubsystem)if x.get_outer()==W);C=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI);S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);assert S.load_game();cmd('pm.EnvPerf2.Viewport 2560 1440');s.update(phase='loaded',at=now);return
  if s['phase']=='loaded':
   if now-s['at']<3 or S.is_load_in_progress():return
   P.set_actor_location(unreal.Vector(1800,-600,50.15),False,True);inventory();cmd('csvprofile startfile=GaradosWaterV2_Baseline');cmd('csvprofile start');s.update(phase='observe',at=now);return
  if now-s['sample']>=1:sample();s['sample']=now;(O/'Progress.json').write_text(json.dumps({'seconds':now-s['at'],'samples':len(r['samples'])}))
  if now-s['at']>=95:finish()
 except Exception:finish(traceback.format_exc())
unreal._garados_baseline=unreal.register_slate_post_tick_callback(tick)
