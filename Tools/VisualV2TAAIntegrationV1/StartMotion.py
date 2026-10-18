"""Short reproducible real input sequence, actual camera and visible NPC animation.
Only initial positioning is a profiling teleport, never claimed as a gameplay footrun.
"""
import unreal,json,math,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2TAAIntegrationV1';j=json.loads((S/'MotionRequest.json').read_text());D=S/'Motion'/j['label'];D.mkdir(parents=True,exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1'
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport '+str(j['width'])+' '+str(j['height']));unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage '+str(j['percentage']));unreal.SystemLibrary.execute_console_command(w,'r.AntiAliasingMethod '+str(j['aa']));unreal.SystemLibrary.execute_console_command(w,'r.VSync 0');unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS 0');unreal.SystemLibrary.execute_console_command(w,'r.DynamicRes.OperationMode 0')
s=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction');sprint=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='SprintHoldAction')
visual=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));dialog=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem) if x.get_outer()==gi)
# Forest path is traversed with real input. NPC talk is a separate initialized location.
p.set_actor_location(unreal.Vector(-4300,1550,50.15),False,True)
from math import sin,cos,pi
stages=[('Warmup',5,None),('IdleForest',2,(0,0)),('WalkForest',2.6,(1,0)),('StopForest',1,(0,0)),('SprintForest',2.3,(-1,0)),('StopSprint',1,(0,0)),('DiagonalWalk',1.6,(.707,.707)),('DiagonalReturn',1.6,(-.707,-.707)),('TalkSetup',4,None),('NPCIdle',1,(0,0)),('Talk',4,(0,0)),('ReturnIdle',1.5,(0,0))]
index=-1;elapsed=0.;local=0.;last=unreal.GameplayStatics.get_time_seconds(w);records=[];started=False;settalk=False;begun=False;wall=time.monotonic();recording=S/'Recordings'/j['label'];recording.parent.mkdir(exist_ok=True)
def inject(x,y):
 yaw=math.radians(p.get_movement_basis_yaw());s.inject_input_vector_for_action(move,unreal.Vector(-sin(yaw)*x+cos(yaw)*y,cos(yaw)*x+sin(yaw)*y,0),[],[])
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._taa_motion);inject(0,0);s.inject_input_vector_for_action(sprint,unreal.Vector(),[],[])
 if dialog.is_dialogue_active():dialog.close_dialogue()
 unreal.SystemLibrary.execute_console_command(w,'pm.TAAReview.CaptureStop');(D/'Result.json').write_text(json.dumps({'request':j,'error':error,'seconds':elapsed,'wall_seconds':time.monotonic()-wall,'records':records,'recording':str(recording),'initial_profiling_teleports':2},indent=2));unreal.log('VTA1_MOTION_DONE '+str(error))
def tick(dt):
 global index,elapsed,local,last,started,settalk,begun
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-last;last=now;elapsed+=delta;local+=delta
  if index<0 or local>=stages[index][1]:
   index+=1;local=0.
   if index>=len(stages):finish();return
   if index==1:unreal.SystemLibrary.execute_console_command(w,'pm.TAAReview.CaptureStart "'+str(recording)+'"');started=True
   if stages[index][0]=='TalkSetup':inject(0,0);p.set_actor_location(unreal.Vector(-835,-1080,50.15),False,True);settalk=True
  name,seconds,axis=stages[index]
  if name=='TalkSetup':
   if local<.15:inject(-.2,0)
   else:inject(0,0)
  elif axis is not None:inject(*axis)
  if name=='Talk' and local>.3 and not begun:assert p.try_interact() and dialog.is_dialogue_active();begun=True
  if name=='ReturnIdle' and dialog.is_dialogue_active():dialog.close_dialogue()
  s.inject_input_vector_for_action(sprint,unreal.Vector(1 if name=='SprintForest' else 0,0,0),[],[])
  camera=pc.player_camera_manager
  records.append({'t':elapsed,'stage':name,'position':p.get_actor_location().to_tuple(),'velocity':p.get_velocity().to_tuple(),'camera':camera.get_camera_location().to_tuple(),'rotation':camera.get_camera_rotation().to_tuple(),'viewport':list(pc.get_viewport_size()),'aa_cvar':unreal.SystemLibrary.get_console_variable_int_value('r.AntiAliasingMethod'),'sp':unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage'),'sprint':p.is_sprinting(),'npc_conversing':visual.is_conversing()})
 except Exception:finish(traceback.format_exc())
unreal._taa_motion=unreal.register_slate_post_tick_callback(tick)
