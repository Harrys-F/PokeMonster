"""Ordinary PIE: actual clock, pause, doorway, interior SaveLoad and battle regression.
Only owned isolated disk slot, existing input and existing developer battle fixture.
"""
import unreal,json,time,math,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV1';q=json.loads((D/'ReviewRequest.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
def sub(c,outer=GI):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==outer)
C=sub(unreal.PokeMonsterWorldClock);L=sub(unreal.PokeMonsterDayNightSubsystem,W);S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);CP=sub(unreal.PokeMonsterCheckpointSubsystem)
assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_DayNight'+q['label'])
Cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterBuildingCutaway)if'V2_House'in a.get_actor_label());result={'checks':[],'trace':[],'initial_clock':C.get_time().export_text(),'initial_light':L.get_lighting_sample().export_text(),'isolated_slot':True,'physical_controller_test':False};s={'i':0,'last':time.monotonic(),'start':time.monotonic()};state={};route=[]
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
def axis(x=0,y=0):
 yaw=math.radians(P.get_movement_basis_yaw());cmd('pm.Input.Axis Gamepad_LeftX '+str(-math.sin(yaw)*x+math.cos(yaw)*y));cmd('pm.Input.Axis Gamepad_LeftY '+str(math.cos(yaw)*x+math.sin(yaw)*y))
def place(x,y):axis();P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def act(n,f,d=.5):route.append((n,f,d,None))
def check(n,p):
 def f():assert p(),n;result['checks'].append(n)
 act(n,f)
def wait(n,p,t=50):route.append((n,lambda:None,t,p))
def shot(n):cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"')
def remember(n):state[n]={'clock':C.get_time().export_text(),'sample':L.get_lighting_sample().export_text(),'position':P.get_actor_location().to_tuple(),'party':[c.export_text()for c in E.get_player_party()],'checkpoint':CP.get_active_checkpoint().export_text()}
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right'
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');place(-200,-100)
check('Ordinary new-session clock and lighting are 09:00',lambda:C.get_hour()==9 and L.is_cycle_enabled()and L.is_sky_ready()and L.get_lighting_sample().sun_elevation>0)
act('Pause and exact noon',lambda:(cmd('pm.WorldClock pause'),cmd('pm.WorldClock set 1 12 0')))
act('B75 switch',lambda:cmd('pm.DayNight B'));check('B75 immediate correct lighting',lambda:abs(L.get_lighting_sample().sun_elevation-75)<.001)
act('C85 switch',lambda:cmd('pm.DayNight C'));check('C85 immediate correct lighting',lambda:abs(L.get_lighting_sample().sun_elevation-85)<.001)
act('Return provisional B',lambda:cmd('pm.DayNight B'));act('Remember paused noon light',lambda:remember('paused'));act('Hold paused world clock',lambda:None,1.2);check('Pause freezes actual light sample',lambda:L.get_lighting_sample().export_text()==state['paused']['sample'])
act('Ordinary 1x time resumes',lambda:cmd('pm.WorldClock reset'));act('Wait normal motion',lambda:None,1.4);check('Normal clock resumes actual light movement',lambda:L.get_lighting_sample().export_text()!=state['paused']['sample'])
act('Plus opens actual existing main menu',lambda:key('Gamepad_Special_Right'));check('Actual main menu pauses clock',lambda:PC.is_menu_open()and C.is_clock_paused());act('Remember menu lighting',lambda:remember('menu'));act('Hold actual menu',lambda:None,1.5);check('Menu holds exact world light',lambda:L.get_lighting_sample().export_text()==state['menu']['sample']);act('A closes actual menu',lambda:key(A));check('Closing menu resumes original clock',lambda:not PC.is_menu_open()and not C.is_clock_paused())
act('Ordinary walk through clearing',lambda:axis(1,0),.3);act('Continue normal walk',lambda:None,2.);act('Stop existing movement',axis,.5);act('Gentle direction change',lambda:axis(0,1));act('Continue perpendicular walk',lambda:None,1.5);act('Stop after real foot walk',axis,.5)
act('Accelerated actual dawn start',lambda:(cmd('pm.WorldClock pause'),cmd('pm.WorldClock set 3 4 30'),cmd('pm.WorldClock speed 60'),cmd('pm.WorldClock resume')))
act('Observe real dawn interval',lambda:None,8.);check('Clock-driven dawn crossed phase and sun rose',lambda:C.get_hour()>=6 and L.get_lighting_sample().sun_elevation>0)
act('Pause before interior',lambda:cmd('pm.WorldClock pause'));act('Set normal speed only',lambda:cmd('pm.WorldClock speed 1'))
act('Approach existing doorway',lambda:place(-3610,500),.8);act('Use existing movement through entrance',lambda:axis(1,0),.85);act('Stop inside',axis,1.5);check('Existing relocated interior and camera work',lambda:Cut.is_viewer_relocated()and P.is_using_interior_movement_basis())
act('Day inside',lambda:cmd('pm.WorldClock set 3 12 0'));act('Actual interior day screenshot',lambda:shot('InteriorDay'),3)
act('Night inside',lambda:cmd('pm.WorldClock set 3 22 0'));act('Actual interior night screenshot',lambda:shot('InteriorNight'),3)
act('Save actual night inside',lambda:state.update(saved=S.save_current_game()));check('Existing save accepts interior state',lambda:state['saved']);act('Remember interior snapshot',lambda:remember('inside'))
act('Move outside for load test',lambda:place(-4100,450),1.);act('Change actual clock to day',lambda:cmd('pm.WorldClock set 8 9 0'));act('Existing load',lambda:state.update(loaded=S.load_game()),1.)
check('SaveLoad restores night light, exact clock, room camera, party and independent checkpoint',lambda:state['loaded']and C.get_time().export_text()==state['inside']['clock']and L.get_lighting_sample().export_text()==state['inside']['sample']and Cut.is_viewer_relocated()and P.is_using_interior_movement_basis()and[c.export_text()for c in E.get_player_party()]==state['inside']['party']and CP.get_active_checkpoint().export_text()==state['inside']['checkpoint'])
act('Restored interior screenshot',lambda:shot('InteriorLoaded'),2)
act('Approach existing exit',lambda:place(16460,500),.8);act('Walk back out',lambda:axis(-1,0),.85);act('Stop outdoors',axis,1.5);check('Original exit and outdoor camera work at night',lambda:not Cut.is_viewer_relocated()and not P.is_using_interior_movement_basis())
act('Set before midnight',lambda:cmd('pm.WorldClock set 3 23 59'));act('Accelerate existing clock',lambda:(cmd('pm.WorldClock speed 60'),cmd('pm.WorldClock resume')));wait('Actual midnight rollover',lambda:C.get_day()==4,5)
act('Pause on next day',lambda:cmd('pm.WorldClock pause'),.05);check('Night state survives midnight',lambda:C.get_hour()==0 and L.get_lighting_sample().stars>.99)
act('Normal clock for existing battle fixture',lambda:cmd('pm.WorldClock reset'));act('Battle-safe original location',lambda:place(-200,-100),.8);act('Start existing real ClassicBattle victory fixture',lambda:cmd('pm.EvolutionReview.Victory current'),1.);check('ClassicBattle starts and clock pauses',lambda:E.is_encounter_active()and C.is_clock_paused())
act('Existing Fight selection',lambda:key('Enter'));act('Existing B attack selection',lambda:key(B))
def ended():
 if E.is_encounter_active():
  if E.get_presenter().get_view().learning_move:key(A)
  return False
 return not P.is_overworld_input_locked()
wait('Actual ClassicBattle and existing learning finish',ended,70)
check('Existing battle victory returns control and valid companion state',lambda:not E.is_encounter_active()and not P.is_overworld_input_locked())
act('Restore normal clock control',lambda:cmd('pm.WorldClock reset'))
def finish(error=None):
 axis();unreal.unregister_slate_post_tick_callback(unreal._daynight_gameplay);result.update(passed=error is None,error=error,elapsed=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(result,indent=2));route.clear()
 for n in ['W','GI','P','PC','C','L','S','E','CP','Cut']:globals().pop(n,None)
def tick(dt):
 try:
  now=time.monotonic();assert now-s['start']<300,'Gameplay timeout';n,f,d,p=route[s['i']]
  result['trace'].append({'real':now-s['start'],'clock':C.get_time().export_text(),'light':L.get_lighting_sample().export_text()})
  if p:
   if not p():assert now-s['last']<d,n;return
  elif now-s['last']<d:return
  f();s.update(i=s['i']+1,last=time.monotonic());(O/'Progress.json').write_text(json.dumps({'step':s['i'],'last':n}))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._daynight_gameplay=unreal.register_slate_post_tick_callback(tick)
