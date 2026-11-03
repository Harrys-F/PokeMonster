"""Real target-map QHD photos and three CSV samples/site; no persistent runtime changes."""
import unreal,json,time,math,statistics,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldOverhaulV3';label=json.loads((D/'Request.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=True);assert not(O/'Result.json').exists();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D)
editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=editor.get_game_world()if editor else None;pie=W is not None
if not W:W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0))
assert W and 'Dev_TestMap_VisualV2'in W.get_name();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);sites=json.loads((R/'Tools/VisualV2WorldOverhaulV3/Sites.json').read_text());cases=[(0,s)for s in json.loads((R/'Tools/VisualV2WorldOverhaulV3/AtlasSites.json').read_text())];rows=[];samples=[];state={'i':0,'phase':'place','at':time.monotonic(),'busy':False};start=last=time.monotonic()
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
cv=['r.GPUCsvStatsEnabled','r.VSync','t.MaxFPS'];old={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in cv}
for k,v in [('r.GPUCsvStatsEnabled',1),('r.VSync',0),('t.MaxFPS',0)]:cmd(k+' '+str(v))
runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Metadata.py'),run_name='__main__');cmd('pm.EnvPerf2.Viewport 2560 1440')
GI=unreal.GameplayStatics.get_game_instance(W);Clock=next(c for c in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if c.get_outer()==GI);Light=next(c for c in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if c.get_outer()==W);original_time=Clock.get_time()
if pie:cmd('pm.WorldClock set 1 12 0');cmd('pm.WorldClock pause')
else:
 Save=next(c for c in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if c.get_outer()==GI);runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/ClockFixture.py'))['set_hour'](W,PC,Save,12)

def finish(error=None):
 cmd('csvprofile stop')
 for k,v in old.items():cmd(k+' '+str(v))
 cmd('pm.WorldClock reset')if pie else PC.close_menu();cmd('pm.EnvPerf2.Viewport 0 0');(O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,rows=rows,seconds=time.monotonic()-start,pie=pie,method='Three 6s CSV samples after 4s settling/site. Separate photos after samples; no video during measurement.'),indent=2));unreal.unregister_slate_post_tick_callback(unreal._fab_capture);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()if pie else unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global samples,last
 if state['busy']:return
 state['busy']=True
 try:

  if not pie:
   if Save.is_load_in_progress():return
   assert Clock.get_hour()==12 and Clock.is_clock_paused()
   assert abs(Light.get_lighting_sample().sun_elevation-75)<.03
  now=time.monotonic();delta=(now-last)*1000;last=now;assert now-start<450
  if state['i']>=len(cases):finish();return
  rep,(name,x,y,yaw)=cases[state['i']];elapsed=now-state['at']
  if state['phase']=='place':
   P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=yaw),False,False);state.update(phase='warm',at=now);return
  if state['phase']=='warm'and elapsed>3:
   cmd('csvprofile startfile=FAB_'+label+'_'+str(state['i']));cmd('csvprofile start');samples=[];state.update(phase='sample',at=now);return
  if state['phase']=='sample':
   samples.append(delta)
   if elapsed>.2:
    cmd('csvprofile stop');ss=sorted(samples);h=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterHabitatSubsystem)if x.get_outer()==W);rows.append(dict(site=name,repeat=rep+1,frames=len(samples),fps=1000/statistics.mean(samples),frame_mean_ms=statistics.mean(samples),p95_ms=ss[int(len(ss)*.95)],player=P.get_actor_location().to_tuple(),camera=PC.player_camera_manager.get_camera_location().to_tuple(),rotation=PC.player_camera_manager.get_camera_rotation().to_tuple(),viewport=PC.get_viewport_size(),screen_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage'),active_population=len(h.population),clock=Clock.get_time().export_text(),sun_elevation=Light.get_lighting_sample().sun_elevation,csv_prefix='FAB_'+label+'_'+str(state['i'])))
    assert PC.get_viewport_size()==(2560,1440),PC.get_viewport_size();assert abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.03
    if rep==0:cmd('Shot filename="'+str(O/(name+'.png'))+'" -nosuffix')
    state.update(phase='after',at=now);return
  if state['phase']=='after'and elapsed>1:state.update(phase='place',i=state['i']+1,at=now)
 except Exception:finish(traceback.format_exc())
 finally:state['busy']=False
unreal._fab_capture=unreal.register_slate_post_tick_callback(tick)
