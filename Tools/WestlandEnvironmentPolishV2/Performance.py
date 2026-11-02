"""Paired fixed-camera PIE samples at current profile; no graphics-quality overrides."""
import unreal,json,time,math,statistics,traceback,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';label=json.loads((D/'PerformanceRequest.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=False);assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D);sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world();assert W;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);rows=[];samples=[];state={'i':0,'phase':'place','at':time.monotonic()};start=time.monotonic();last=start
sites=[('Dorf',-222,-47,-205,-42),('Wiese',150,13,180,25),('Waldweg',202,120,225,175),('Wald',247,250,265,264),('Fluss',L.river(-145)+10,-145,L.river(-145),-142)];cases=[(r,s)for r in range(3)for s in sites]
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
cvars=['r.GPUCsvStatsEnabled','r.VSync','t.MaxFPS'];before={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in cvars}
for k,v in [('r.GPUCsvStatsEnabled',1),('r.VSync',0),('t.MaxFPS',0)]:cmd(k+' '+str(v))
cmd('pm.WorldClock set 1 12 0');cmd('pm.WorldClock pause')
def finish(error=None):
 cmd('csvprofile stop')
 for k,v in before.items():cmd(k+' '+str(v))
 cmd('pm.WorldClock reset');(O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,rows=rows,seconds=time.monotonic()-start,method='PIE fixed camera, noon paused, no video; three repeats; CSV GPU/thread counters separate'),indent=2));unreal.unregister_slate_post_tick_callback(unreal._wep_perf);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
def tick(dt):
 global samples,last
 try:
  now=time.monotonic();delta=(now-last)*1000;last=now;assert now-start<300
  if state['i']>=len(cases):finish();return
  repeat,(name,e,n,te,tn)=cases[state['i']];elapsed=now-state['at']
  if state['phase']=='place':
   x,y,z=L.world(e,n,L.height(e,n));P.set_actor_location(unreal.Vector(x,y,z+50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();tx,ty,_=L.world(te,tn);P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=math.degrees(math.atan2(ty-y,tx-x))),False,False);state.update(phase='warm',at=now);return
  if state['phase']=='warm'and elapsed>3:
   cmd('csvprofile startfile=WEP_'+label+'_'+str(state['i']));cmd('csvprofile start');samples=[];state.update(phase='sample',at=now);return
  if state['phase']=='sample':
   samples.append(delta)
   if elapsed>6:
    cmd('csvprofile stop');ss=sorted(samples);rows.append(dict(site=name,repeat=repeat+1,frames=len(samples),frame_mean_ms=statistics.mean(samples),fps=1000/statistics.mean(samples),p95_ms=ss[int(len(ss)*.95)],camera=PC.player_camera_manager.get_camera_location().to_tuple(),rotation=PC.player_camera_manager.get_camera_rotation().to_tuple(),viewport=PC.get_viewport_size(),screen_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage'),csv_prefix='WEP_'+label+'_'+str(state['i'])));state.update(phase='place',i=state['i']+1,at=now)
 except Exception:finish(traceback.format_exc())
unreal._wep_perf=unreal.register_slate_post_tick_callback(tick)
