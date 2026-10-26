"""Normal-speed real presented frames, solely to review shadow-update stability."""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV11AI22';O=D/'ShadowMotionA02';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
C=sub(unreal.PokeMonsterWorldClock);E=sub(unreal.PokeMonsterEncounterSubsystem);assert sub(unreal.PokeMonsterSaveSubsystem).use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_ShadowMotionA02')
Config=unreal.get_default_object(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterDayNightSettings'));old=Config.get_editor_property('RotationThresholdDegrees');profiles=[(a,a.get_editor_property('profile'))for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)]
for a,p in profiles:a.set_editor_property('profile',None)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('sg.ShadowQuality 2');cmd('r.ScreenPercentage 100');P.set_actor_location(unreal.Vector(-1353.161706774002,-775.1272881918381,50.22354983301621),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
Capture=R/'Saved/VisualV2TAAIntegrationV1/Recordings/DayNightV11Shadow02'
route=[];s={'i':0,'last':time.monotonic()};r={'recordings':[]}
def act(n,f,d=.5):route.append((n,f,d))
for name,threshold in [('Raw',0),('Cached',.025)]:
 act('Set '+name,lambda t=threshold:(Config.set_editor_property('RotationThresholdDegrees',t),cmd('pm.WorldClock pause'),cmd('pm.WorldClock set 1 12 0'),cmd('pm.WorldClock speed 1')))
 act('Start '+name,lambda n=name:(cmd('pm.WorldClock resume'),cmd('pm.TAAReview.CaptureStart '+str(Capture/n)+' slate 30')),2)
 act('Stop '+name,lambda n=name:(cmd('pm.TAAReview.CaptureStop'),r['recordings'].append({'name':n,'clock':C.get_time().export_text()})),8)
 act('Drain readbacks',lambda n=name:check_capture(n),3)
def check_capture(name):
 assert(Capture/name/'Complete.txt').exists()and(Capture/name/'Frames.csv').exists(),'No native recording'
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._shadow_motion);cmd('pm.TAAReview.CaptureStop');Config.set_editor_property('RotationThresholdDegrees',old)
 for a,p in profiles:a.set_editor_property('profile',p)
 r.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(r,indent=2));route.clear()
 for n in ['W','GI','PC','P','C','E','profiles','a','p']:globals().pop(n,None)
def tick(dt):
 try:
  assert not E.is_encounter_active();n,f,d=route[s['i']]
  if time.monotonic()-s['last']<d:return
  f();s.update(i=s['i']+1,last=time.monotonic())
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._shadow_motion=unreal.register_slate_post_tick_callback(tick)
