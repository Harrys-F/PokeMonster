"""Short native presented-frame motion evidence, existing capture pipeline; not a benchmark."""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EnvironmentV3/MotionFinal';D.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround)if x.get_outer()==W);assert G.visit(0);settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False);dilation=unreal.GameplayStatics.get_global_time_dilation(W);unreal.GameplayStatics.set_global_time_dilation(W,.20)
clips=[('Grass',-2100,-1760),('Water',-350,-130)];s={'i':0,'phase':'place','since':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'rows':[]};start=time.monotonic()
def cmd(v):unreal.SystemLibrary.execute_console_command(W,v,PC)
def axis(x,y):cmd('pm.Input.Axis Gamepad_LeftX '+str(x));cmd('pm.Input.Axis Gamepad_LeftY '+str(y))
cmd('pm.EnvPerf2.Viewport 2560 1440')
def step(p):s['phase']=p;s['since']=0.
def finish(error=None):
 axis(0,0);cmd('pm.TAAReview.CaptureStop');unreal.GameplayStatics.set_global_time_dilation(W,dilation);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);cmd('pm.EnvPerf2.Viewport 0 0');restored=G.return_to_world();unreal.unregister_slate_post_tick_callback(unreal._env3_motion);(D/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'rows':s['rows'],'restored':restored,'method':'native Slate presented frames, world time dilation .20; encode original game timestamps, no interpolation, not realtime FPS'},indent=2));unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['since']+=now-s['last'];s['last']=now;assert time.monotonic()-start<140
  name,x,y=clips[s['i']];t=s['since']
  if s['phase']=='place':P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();step('settle')
  elif s['phase']=='settle'and t>1:
   source=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('EnvironmentV3_Final_'+name);assert not source.exists();s['source']=str(source);cmd('pm.TAAReview.CaptureStart "'+str(source)+'" slate 60');step('record')
  elif s['phase']=='record':
   if t<1.4:axis(.7,0)
   elif t<2.8:axis(-.7,0)
   elif t<4.0:axis(0,.7)
   elif t<5.:axis(0,-.7)
   else:axis(0,0);cmd('pm.TAAReview.CaptureStop');s['rows'].append({'name':name,'source':s['source'],'game_duration':t});step('drain')
  elif s['phase']=='drain'and t>.5:
   s['i']+=1
   if s['i']==len(clips):finish();return
   step('place')
 except Exception:finish(traceback.format_exc())
unreal._env3_motion=unreal.register_slate_post_tick_callback(tick)
