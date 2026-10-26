"""Ordinary editor PIE; real existing menus/dialogue/battles/doorway, isolated native saves.
Diagnostic start positions and existing party/battle fixtures are explicitly recorded.
No map writes, AI changes, model edits, lighting changes or user save writes.
"""
import unreal,json,time,math,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WorldClockV1';req=json.loads((D/'Request.json').read_text());O=D/req['label'];O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
GI=unreal.GameplayStatics.get_game_instance(W);P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
Clock=sub(unreal.PokeMonsterWorldClock);S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);Dialog=sub(unreal.PokeMonsterDialogueSubsystem);Checkpoint=sub(unreal.PokeMonsterCheckpointSubsystem)
Cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterBuildingCutaway)if'V2_House'in a.get_actor_label())
assert S.use_isolated_pie_test_slot(req['slot'])
user=R/'Saved/SaveGames/PokeMonster_Dev.sav';user_hash=hashlib.sha256(user.read_bytes()).hexdigest();slot=R/'Saved/SaveGames'/(req['slot']+'.sav')
result={'ordinary_pie':True,'diagnostic_positions':True,'existing_party_and_battle_fixtures':True,'physical_controller_test':False,'slot':req['slot'],'checks':[],'steps':[],'captures':[],'events':[]};route=[];state={};s={'index':0,'due':time.monotonic(),'start':time.monotonic()}
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right';X='Gamepad_FaceButton_Left'if backend else'Gamepad_FaceButton_Top'
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
def axis(x=0,y=0):
 yaw=math.radians(P.get_movement_basis_yaw());cmd('pm.Input.Axis Gamepad_LeftX '+str(-math.sin(yaw)*x+math.cos(yaw)*y));cmd('pm.Input.Axis Gamepad_LeftY '+str(math.cos(yaw)*x+math.sin(yaw)*y))
def place(x,y):axis();P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def stamp():
 t=Clock.get_time();return {'day':t.day,'second':t.seconds_of_day,'phase':str(Clock.get_phase()),'paused':Clock.is_clock_paused(),'speed':Clock.get_debug_speed(),'label':str(Clock.get_time_label())}
def absolute():t=Clock.get_time();return(t.day-1)*86400+t.seconds_of_day
def snap():return[c.export_text()for c in E.get_player_party()]
# Keep no Python event adapters alive across world cleanup. The first native-event
# observation is preserved in PIE01; repeat runs inspect automatic transitions.
def capture(n):
 name='WorldClock'+req['label']+n;cmd('pm.CreatureReview.CaptureLiveUI '+name+' qhd');result['captures'].append({'name':n,'directory':str(R/'Saved/GlumandaV11/LiveUI'/name),'method':'actual Slate and separately identified live QHD PIE/UMG render'})
def act(n,fn,delay=.5):route.append((n,fn,delay,None))
def check(n,p):
 def f():assert p(),(n,stamp());result['checks'].append(n)
 act(n,f)
def wait(n,p,timeout=80):route.append((n,lambda:None,timeout,p))
def remember(n):state[n]={'absolute':absolute(),'clock':stamp(),'party':snap(),'position':P.get_actor_location().to_tuple(),'checkpoint':Checkpoint.get_active_checkpoint().export_text()}
def frozen(n):return absolute()==state[n]['absolute']
def load_saved():assert S.load_game(),S.get_last_storage_message()
def save_now():assert S.save_current_game(),S.get_last_storage_message()
def open_main():key('Gamepad_Special_Right')
def menu_save():
 act('Plus opens existing main menu',open_main)
 for _ in range(2):act('Existing Dpad selects Save',lambda:key('Gamepad_DPad_Down'))
 act('B requests Save',lambda:key(B));act('B confirms existing Save',lambda:key(B))
def close():
 if PC.is_menu_open():key(A)
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');place(-200,-100)
if req.get('mode')=='restart':
 act('Fresh process default runtime speed',lambda:result.update(initial=stamp()))
 check('Fresh GameInstance uses 1x without debug pause',lambda:Clock.get_debug_speed()==1 and not Clock.is_clock_paused())
 act('Stop ordinary time for exact load inspection',lambda:cmd('pm.WorldClock pause'))
 act('Existing isolated on-disk slot loads',load_saved,1.)
 check('Saved day and fractional time restored after editor restart',lambda:stamp()['day']==7 and abs(stamp()['second']-86340)<.001)
 act('Open menu after restarted load',open_main);act('Capture restored world time',lambda:capture('RestartLoaded'))
else:
 assert not slot.exists()
 act('Existing nontrivial party fixture',lambda:cmd('pm.EvolutionReview.Party Zunderlauf 15'))
 act('Pause developer clock safely',lambda:cmd('pm.WorldClock pause'))
 act('Set exact new-game time for screenshot',lambda:cmd('pm.WorldClock set 1 9 0'))
 act('Plus opens existing main menu',open_main);check('Existing main-menu time label',lambda:str(PC.get_overworld_widget().get_view().world_time_label)=='Tag 1 – 09:00 Uhr')
 act('Capture Day1 09:00',lambda:capture('Start0900'));act('Remember overlapping menu/debug pause',lambda:remember('menu'))
 act('Wait during open menu',lambda:None,1.2);check('Menu/debug overlap freezes time',lambda:frozen('menu'))
 act('Resume debug while menu still open',lambda:cmd('pm.WorldClock resume'));act('Wait remaining menu reason',lambda:None,1.2);check('Debug resume cannot release menu pause',lambda:frozen('menu'))
 act('A closes menu',close);check('Menu close resumes clock',lambda:not Clock.is_clock_paused())
 act('Begin ordinary real-time measurement',lambda:state.update(measure=absolute(),wall=time.monotonic()))
 act('Five real seconds of ordinary exploration',lambda:None,5.)
 def measure():
  real=time.monotonic()-state['wall'];game=absolute()-state['measure'];result['real_time_conversion']={'real_seconds':real,'game_seconds':game,'rate':game/real};assert abs(game/real-12)<.8,result['real_time_conversion']
 act('Verify 12x rate and absence of doubled ticks',measure)
 act('Walk with existing input',lambda:axis(1,0),.4);act('Stop after normal walk',axis,.8)
 act('X opens team submenu',lambda:key(X));act('Remember submenu time',lambda:remember('submenu'));act('L/R changes category',lambda:key('Gamepad_RightShoulder'));act('Hold submenu',lambda:None,1.);check('Submenu and category navigation freeze time',lambda:frozen('submenu'))
 act('Add explicit Unreal pause',lambda:unreal.GameplayStatics.set_game_paused(W,True));act('Close submenu while explicitly paused',close);act('Wait explicit pause',lambda:None,1.);check('Closing menu preserves explicit pause',lambda:frozen('submenu'))
 act('Release explicit Unreal pause',lambda:unreal.GameplayStatics.set_game_paused(W,False));check('No stale pause after explicit resume',lambda:not Clock.is_clock_paused())
 act('Diagnostic approach to existing Wanderer',lambda:place(-825,-1080),.8);act('Face Wanderer',lambda:axis(-1,0),.12);act('Stop at Wanderer',axis,.3);act('B uses original interaction',lambda:key(B));check('Actual existing dialogue active',Dialog.is_dialogue_active);act('Remember dialogue time',lambda:remember('dialogue'));act('Hold dialogue',lambda:None,1.);check('Dialogue freezes time',lambda:frozen('dialogue'))
 act('Close existing dialogue',PC.close_dialogue);check('Dialogue close releases its reason',lambda:not Clock.is_clock_paused())
 act('Diagnostic approach to actual healing-house doorway',lambda:place(-3610,500),.8);act('Walk through original entrance',lambda:axis(1,0),.85);act('Stop inside',axis,1.5);check('Actual interior entered',lambda:Cut.is_viewer_relocated()and P.is_using_interior_movement_basis())
 act('Pause for exact interior SaveLoad',lambda:cmd('pm.WorldClock pause'));act('Set later day time',lambda:cmd('pm.WorldClock set 3 16 42'));menu_save();act('Remember saved interior',lambda:remember('interior'));act('Interior time screenshot',lambda:capture('Later1642'));act('Close menu',close)
 act('Move outside diagnostically',lambda:place(-4100,450),1.);act('Change only runtime clock',lambda:cmd('pm.WorldClock set 9 1 2'));act('Load existing interior slot',load_saved,1.);check('Interior and exact saved time restored',lambda:Cut.is_viewer_relocated()and P.is_using_interior_movement_basis()and frozen('interior')and snap()==state['interior']['party']);act('Open loaded menu',open_main);act('Capture interior restored time',lambda:capture('InteriorLoaded'));act('Close menu',close)
 act('Approach existing room exit',lambda:place(16460,500),.8);act('Walk out',lambda:axis(-1,0),.85);act('Stop outside',axis,1.5);check('Exit preserves same central clock',lambda:not Cut.is_viewer_relocated()and frozen('interior'))
 act('Set just before dawn',lambda:cmd('pm.WorldClock set 4 4 59'));act('Set 60x debug speed',lambda:cmd('pm.WorldClock speed 60'));act('Resume toward phase boundary',lambda:cmd('pm.WorldClock resume'))
 wait('Actual automatic dawn boundary',lambda:Clock.get_phase()==unreal.PokeMonsterDayPhase.DAWN,8)
 act('Pause after boundary',lambda:cmd('pm.WorldClock pause'),.05);act('Open phase menu',open_main);act('Capture dawn boundary',lambda:capture('DawnBoundary'));act('Close menu',close)
 act('Set just before midnight',lambda:cmd('pm.WorldClock set 4 23 59'));act('Use 10x',lambda:cmd('pm.WorldClock speed 10'));act('Resume toward midnight',lambda:cmd('pm.WorldClock resume'))
 wait('Actual automatic day rollover',lambda:Clock.get_day()==5,8)
 act('Pause after midnight',lambda:cmd('pm.WorldClock pause'),.05);act('Open day menu',open_main);act('Capture actual day rollover',lambda:capture('DayRollover'));act('Close menu',close)
 act('Reset speed and debug hold',lambda:cmd('pm.WorldClock reset'));check('Reset is 1x and normal time',lambda:Clock.get_debug_speed()==1 and not Clock.is_clock_paused())
 act('Return to battle-safe clearing',lambda:place(-200,-100),1.);act('Existing actual victory fixture',lambda:cmd('pm.EvolutionReview.Victory current'),1.);check('ClassicBattle pauses clock',lambda:E.is_encounter_active()and Clock.is_clock_paused());act('Remember active battle time',lambda:remember('battle'));act('Hold battle command selection',lambda:None,1.);check('Command selection keeps exact time',lambda:frozen('battle'));act('Open Fight with keyboard',lambda:key('Enter'));act('Select existing attack with B',lambda:key(B))
 def battle_done():
  if E.is_encounter_active():
   if E.get_presenter().get_view().learning_move:key(A)
   assert frozen('battle'),'Time advanced in ClassicBattle';return False
  return not P.is_overworld_input_locked()
 wait('Real battle and learning presentation finish',battle_done,60);check('After combat clock resumes without stale reason',lambda:not Clock.is_clock_paused())
 act('Pause final night save',lambda:cmd('pm.WorldClock pause'));act('Set final night save near midnight',lambda:cmd('pm.WorldClock set 7 23 59'));act('Existing manual disk save',save_now);act('Remember night save',lambda:remember('night'));act('Advance debug date deliberately',lambda:cmd('pm.WorldClock set 12 12 12'));act('Load night save',load_saved,1.);check('Night day phase team and position restored',lambda:frozen('night')and snap()==state['night']['party']and math.dist(P.get_actor_location().to_tuple(),state['night']['position'])<.3);act('Open final restored menu',open_main);act('Capture restored night',lambda:capture('NightLoaded'));act('Close menu',close)
 check('Automatic phase and day transitions observed',lambda:any(x['day']==5 for x in result['steps'])and any('DAWN' in x['phase'] for x in result['steps']))
 result['restart_slot']=req['slot']

def finish(error=None):
 axis();unreal.GameplayStatics.set_game_paused(W,False);unreal.unregister_slate_post_tick_callback(unreal._worldclock_review)
 result.update(passed=error is None,error=error,final=stamp(),original_save_unchanged=hashlib.sha256(user.read_bytes()).hexdigest()==user_hash,elapsed_real_seconds=time.monotonic()-s['start']);assert result['original_save_unchanged'];(O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('WORLD_CLOCK_REVIEW_DONE '+str(error))
 # This completed run must not retain old world/actor wrappers in a lambda cycle.
 route.clear()
 for name in ['W','GI','P','PC','Clock','S','E','Dialog','Checkpoint','Cut']:globals().pop(name,None)
def tick(dt):
 try:
  now=time.monotonic();assert now-s['start']<420,'Review timeout';n,fn,delay,pred=route[s['index']]
  if pred:
   if not pred():assert now-s['due']<delay,n;return
  elif now-s['due']<delay:return
  fn();result['steps'].append({'name':n,**stamp()});s['index']+=1;s['due']=time.monotonic();(O/'Progress.json').write_text(json.dumps({'step':s['index'],'last':n,'clock':stamp()},indent=2))
  if s['index']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._worldclock_review=unreal.register_slate_post_tick_callback(tick)
