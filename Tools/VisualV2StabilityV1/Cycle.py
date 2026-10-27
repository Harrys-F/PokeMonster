"""One controlled PIE endpoint, with existing gameplay and isolated storage."""
import unreal,json,time,math,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';q=json.loads((D/'CycleRequest.json').read_text());O=D/'Cycles01'/q['label'];O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
C=sub(unreal.PokeMonsterWorldClock);E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);assert unreal._stability_isolated and not E.is_encounter_active()
result={'mode':q['mode'],'checks':[],'trace':[]};route=[];s={'i':0,'start':time.monotonic(),'last':time.monotonic()};memory={}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
def axis(x=0,y=0):
 yaw=math.radians(P.get_movement_basis_yaw());cmd('pm.Input.Axis Gamepad_LeftX '+str(-math.sin(yaw)*x+math.cos(yaw)*y));cmd('pm.Input.Axis Gamepad_LeftY '+str(math.cos(yaw)*x+math.sin(yaw)*y))
def place(x,y):axis();P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def act(n,f,d=.4):route.append((n,f,d,None))
def check(n,p):
 def f():assert p(),n;result['checks'].append(n)
 act(n,f)
def wait(n,p,t=50):route.append((n,lambda:None,t,p))
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right';X='Gamepad_FaceButton_Left'if backend else'Gamepad_FaceButton_Top';mode=q['mode'];cmd('pm.WorldClock reset');cmd('pm.TAAReview.ReadbackSlots 3')
act('Let game settle',lambda:None,1.)
if mode in ['normal','pokemon','phase']:
 if mode=='pokemon':
  for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):
   path=unreal._stability_profiles.get(a.get_name());a.set_editor_property('profile',unreal.load_asset(path)if path else None)
 if mode=='phase':act('Actual phase change',lambda:(cmd('pm.WorldClock set 1 19 59'),cmd('pm.WorldClock speed 60')))
 act('Live autonomous world',lambda:None,3.)
 check('Player remains under normal control',lambda:not E.is_encounter_active()and not P.is_overworld_input_locked())
 if mode=='phase':check('Night phase crossed without changing clock architecture',lambda:C.get_hour()==20)
 check('All configured wild AI retain valid mutual reservations',lambda:all(not a.overworld_movement.social_partner or a.overworld_movement.social_partner.social_partner==a.overworld_movement for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)))
elif mode=='save':
 act('Pause at saved night',lambda:(cmd('pm.WorldClock pause'),cmd('pm.WorldClock set 5 22 0')))
 act('Save isolated slot',lambda:memory.update(saved=S.save_current_game(),position=P.get_actor_location().to_tuple(),clock=C.get_time().export_text(),party=[a.export_text()for a in E.get_player_party()]))
 check('Test save completed',lambda:memory['saved']);act('Change temporary state',lambda:(place(-500,2100),cmd('pm.WorldClock set 8 9 0')))
 act('Load existing isolated slot',lambda:memory.update(loaded=S.load_game()),1.5)
 check('Exact position, clock, team and control restored',lambda:memory['loaded']and P.get_actor_location().to_tuple()==memory['position']and C.get_time().export_text()==memory['clock']and[a.export_text()for a in E.get_player_party()]==memory['party']and not P.is_overworld_input_locked())
elif mode=='interior':
 Cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterBuildingCutaway)if'V2_House'in a.get_actor_label());act('Approach doorway',lambda:place(-3610,500));act('Walk inside',lambda:axis(1,0),.5);act('Stop inside',axis,.85);act('Settle interior',lambda:None,1.5);check('Inside original relocated interior',lambda:Cut.is_viewer_relocated()and P.is_using_interior_movement_basis())
elif mode=='battle':
 act('Battle-safe clearing',lambda:place(-200,-100));act('Existing victory fixture',lambda:cmd('pm.EvolutionReview.Victory current'))
 check('ClassicBattle active and clock paused',lambda:E.is_encounter_active()and C.is_clock_paused());act('Fight',lambda:key('Enter'));act('B selects attack',lambda:key(B))
 def ended():
  if E.is_encounter_active():
   if E.get_presenter().get_view().learning_move:key(A)
   return False
  return not P.is_overworld_input_locked()
 wait('Battle ends with normal control',ended,70);check('Clock resumes after battle',lambda:not C.is_clock_paused())
elif mode=='record':
 capture=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('StabilityStopAfter_'+q['label']);result['capture']=str(capture);act('Start owned recorder',lambda:cmd('pm.TAAReview.CaptureStart '+str(capture)+' slate 30'));act('Three seconds of actual frames before PIE end',lambda:None,3.)
elif mode=='movement':
 act('Open clearing',lambda:place(-200,-100));
 if q.get('recording_name'):
  capture=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/q['recording_name'];result['capture']=str(capture);act('Known real companion in RAM fixture',lambda:cmd('pm.EvolutionReview.Party Zunderlauf 15'));act('Start continuous real gameplay clip',lambda:cmd('pm.TAAReview.CaptureStart '+str(capture)+' slate 30'))
 memory['pose']=P.get_actor_location().to_tuple();directions=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
 for phase in ['Walk','Sprint']:
  if phase=='Sprint':act('L3 toggles sprint on',lambda:key('Gamepad_LeftThumbstick'));check('Sprint latch on',P.is_sprint_mode_enabled)
  for x,y in directions:act(phase+' '+str((x,y)),lambda x=x,y=y:axis(x,y),.35)
  act('Stop '+phase,axis,.35)
 act('L3 toggles sprint off',lambda:key('Gamepad_LeftThumbstick'));check('Sprint latch off',lambda:not P.is_sprint_mode_enabled());act('X opens existing menu',lambda:key(X));check('Quick menu owns focus',PC.is_menu_open);act('Dpad down',lambda:key('Gamepad_DPad_Down'));act('Dpad up',lambda:key('Gamepad_DPad_Up'));act('R category',lambda:key('Gamepad_RightShoulder'));act('L category',lambda:key('Gamepad_LeftShoulder'));act('A closes menu',lambda:key(A));check('Control after menu',lambda:not PC.is_menu_open()and not P.is_overworld_input_locked())
if q.get('recording_name'):
 act('Return to normal controlled gameplay',lambda:None,1.);act('Finish actual continuous recording',lambda:cmd('pm.TAAReview.CaptureStop'))
if mode not in ['normal','pokemon','phase','save','interior','battle','record','movement']:raise AssertionError(mode)
def finish(error=None):
 axis();unreal.unregister_slate_post_tick_callback(unreal._stability_cycle);result.update(passed=error is None,error=error,elapsed=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(result,indent=2));route.clear()
 for n in ['W','GI','P','PC','C','E','S','Cut','a']:globals().pop(n,None)
 gc.collect()
def tick(dt):
 try:
  now=time.monotonic();assert now-s['start']<110;name,f,d,p=route[s['i']]
  if p:
   if not p():assert now-s['last']<d,name;return
  elif now-s['last']<d:return
  result['trace'].append({'step':name,'position':P.get_actor_location().to_tuple(),'game_seconds':unreal.GameplayStatics.get_time_seconds(W),'wall':now-s['start']});f();s.update(i=s['i']+1,last=now);(O/'Progress.json').write_text(json.dumps({'step':s['i'],'last':name}))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._stability_cycle=unreal.register_slate_post_tick_callback(tick)
