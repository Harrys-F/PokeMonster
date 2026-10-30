"""Three short native CSV windows: normal active world, no recording or terrain-probe loop."""
import unreal,json,time,traceback,shutil
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosWaterV2';q=json.loads((D/'Active.json').read_text());O=D/q['label'];s={'start':time.monotonic(),'phase':'init','at':0,'i':1,'done':False};r={'checks':[],'windows':[]};W=PC=P=S=C=H=None
assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(O/'UserData')
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def finish(error=None):
 if s['done']:return
 s['done']=True;unreal.unregister_slate_post_tick_callback(unreal._garados_perf)
 try:cmd('csvprofile stop')
 except Exception:pass
 r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2,default=str));unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,PC,P,S,C,H
 try:
  now=time.monotonic();assert now-s['start']<180
  if s['phase']=='init':
   if now-s['start']<12:return
   ws=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not ws:return
   W=ws[0];PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(t,o=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==o)
   S=sub(unreal.PokeMonsterSaveSubsystem);C=sub(unreal.PokeMonsterWorldClock);H=sub(unreal.PokeMonsterHabitatSubsystem,W);assert S.load_game();cmd('pm.EnvPerf2.Viewport 2560 1440');s.update(phase='load',at=now);return
  if s['phase']=='load':
   if now-s['at']<4 or S.is_load_in_progress():return
   P.set_actor_location(unreal.Vector(1800,-600,50.15),False,True);s.update(phase='populate',at=now);return
  if s['phase']=='populate':
   found=[a for a in H.population if str(a.visual_species.get_internal_id())=='Garados']
   if not found:
    assert now-s['at']<45,'No natural Garados admitted before the water performance check';return
   r['natural_garados']=found[0].get_path_name();P.set_actor_location(unreal.Vector(1300,-1200,50.15),False,True);s.update(phase='warm',at=now);return
  if s['phase']=='warm':
   if now-s['at']<20:return
   r['rendering']={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.ScreenPercentage','r.TemporalAA.Upsampling','r.Shadow.Virtual.Enable','r.Shadow.Virtual.SMRT.RayCountDirectional','r.VSync','t.MaxFPS']};assert list(r['rendering'].values())[:6]==[0.,0.,75.,1.,1.,4.];r['viewport']=unreal.WidgetLayoutLibrary.get_viewport_size(W).to_tuple();r['high']={n:unreal.SystemLibrary.get_console_variable_int_value('sg.'+n+'Quality')for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']};assert all(v==2 for v in r['high'].values());r['day_length']=C.get_real_minutes_per_day();
   for a in H.population:
    if str(a.visual_species.get_internal_id())=='Garados':a.overworld_movement.measure_activity_cost=True
   r['garados_start_cm']={a.get_path_name():a.overworld_movement.distance_travelled for a in H.population if str(a.visual_species.get_internal_id())=='Garados'};r['clock_running']=not C.is_clock_paused();r['position']=P.get_actor_location().to_tuple();r['camera']=PC.player_camera_manager.get_camera_location().to_tuple();r['camera_rotation']=PC.player_camera_manager.get_camera_rotation().to_tuple();s['phase']='begin'
  if s['phase']=='begin':
   assert not C.is_clock_paused();name='GaradosWaterV2_Perf'+str(s['i']);cmd('csvprofile startfile='+name);cmd('csvprofile start');s.update(phase='measure',at=now,name=name);r['windows'].append({'name':name,'hour':C.get_hour(),'active_pokemon':len(H.population),'garados':sum(str(a.visual_species.get_internal_id())=='Garados'for a in H.population)});return
  if s['phase']=='measure'and now-s['at']>=15:cmd('csvprofile stop');s.update(phase='drain',at=now);return
  if s['phase']=='drain':
   src=Path(unreal.Paths.project_saved_dir())/'Profiling/CSV'/(s['name']+'.csv')
   if now-s['at']<3 or not src.exists():return
   shutil.copyfile(src,O/(s['name']+'.csv'));s['i']+=1
   if s['i']>3:
    assert any(str(a.visual_species.get_internal_id())=='Garados'for a in H.population),'Measured water specimen disappeared';r['garados_cpu']=[{'additional_distance_cm':a.overworld_movement.distance_travelled-r['garados_start_cm'].get(a.get_path_name(),0),'measured_ticks':a.overworld_movement.measured_ticks,'tick_work_us':a.overworld_movement.tick_work_microseconds,'planning_work_us':a.overworld_movement.planning_work_microseconds,'measured_plans':a.overworld_movement.measured_plans}for a in H.population if str(a.visual_species.get_internal_id())=='Garados'];r['checks'].append('Three unrecorded native windows, live Pokemon/clock, production C/IFG/TAAU75/VSM4 High');finish();return
   s['phase']='begin'
 except Exception:finish(traceback.format_exc())
unreal._garados_perf=unreal.register_slate_post_tick_callback(tick)
