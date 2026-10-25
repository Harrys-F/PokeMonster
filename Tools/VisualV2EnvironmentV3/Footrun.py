"""Actual VisualV2 PIE walking route: physics/input, no in-route test teleports, RAM-only saves."""
import unreal,json,math,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/EnvironmentV3/FootrunFinal';O.mkdir(exist_ok=False);E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world();assert W;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround)if x.get_outer()==W);assert G.visit(0)
Save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);Enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);Dialog=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem)if x.get_outer()==GI);cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterBuildingCutaway)if'V2_House'in a.get_actor_label());cm=P.get_component_by_class(unreal.CharacterMovementComponent)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(slot.read_bytes()).hexdigest();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(v):unreal.SystemLibrary.execute_console_command(W,v,PC)
def axis(x,y):cmd('pm.Input.Axis Gamepad_LeftX '+str(x));cmd('pm.Input.Axis Gamepad_LeftY '+str(y))
def worldinput(dx,dy):
 yaw=math.radians(P.get_movement_basis_yaw());return -math.sin(yaw)*dx+math.cos(yaw)*dy,math.cos(yaw)*dx+math.sin(yaw)*dy
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom'
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
sprint_initial=P.is_sprint_mode_enabled()
if sprint_initial:key('Gamepad_LeftThumbstick')
# Test setup only, before distance/time accounting. No subsequent test teleport.
P.set_actor_location(unreal.Vector(-760,-1410,48.15),False,True);cm.stop_movement_immediately();cmd('pm.EnvPerf2.Viewport 2560 1440')
route=[]
def add(k,n,a=None):route.append((k,n,a))
def walk(n,x,y):add('walk',n,(x,y))
add('pause','InitialSettle',1);add('menu','MenuFocus');walk('Main1',-760,-1160);walk('Main2',-760,-820);walk('Main3',-740,-720);walk('BridgeApproach',-500,-540);walk('BridgeEntry',-350,-490);walk('BridgeMid',-350,-320);add('shot','BachBruecke');walk('BridgeExit',-350,-130);walk('OpenWay',-20,-40);walk('Pass1',220,160);walk('Pass2',410,280);add('shot','Felsen');walk('ArchiveApproach',700,590);walk('Archive',745,680);add('save','RAMSaveLoad');walk('ReturnPass',700,590);walk('ReturnPass2',410,280);walk('ReturnPass1',220,160);walk('ReturnBridge',-350,-130);walk('BridgeSouth',-350,-490);walk('ReturnMain',-740,-720);walk('ReturnStart',-760,-1410);walk('VillageFork',-1150,-1920);walk('VillagePath',-2100,-2060);add('shot','Wiese');walk('VillageSouth',-3350,-1700);walk('VillageWest',-4150,-700);walk('HealerForecourt',-4100,450);add('shot','Heilhaus');walk('HouseDoor',-3610,500);add('hold','Enter',(1,0,.85));add('pause','InteriorReady',1);add('inside','Interior');walk('InteriorAisle',16900,670);walk('HealerSideAisle',17230,650);walk('HealerApproach',17230,555);add('hold','FaceHealer',(0,-1,.12));add('interact','Healer');add('dialog','HealDialogue');add('heal','HPCheck');walk('HealerReturn',17230,650);walk('InteriorFront',16900,670);walk('InsideDoor',16460,500);add('hold','Exit',(-1,0,.85));add('pause','OutsideReady',1);add('outside','Outside');walk('NorthFork',-4100,450);walk('NorthForest',-4300,1550);walk('NorthRidge',-3300,2050);add('shot','Wald');walk('NorthEast',-2150,2000);walk('ForestEast',-1700,1220);walk('ForestMiddle',-1550,650);walk('CrownApproach',-1900,530);add('shot','Kronen');walk('ForestReturn',-1550,650);walk('ForestSouth',-1580,-100);walk('ForestLower',-1560,-860);walk('VillageReturn',-1520,-1830);walk('StartReturnA',-1150,-1920);walk('StartReturn',-760,-1410);add('directions','EightDirections');add('sprint','Sprint');add('menu','FinalMenu');add('save','FinalRAMSaveLoad')
s={'i':0,'elapsed':0.,'lasttime':unreal.GameplayStatics.get_time_seconds(W),'local':{},'distance':0.,'lastpos':P.get_actor_location(),'stuck':0.,'checks':[],'battles':0};start=time.monotonic()
def finish(error=None):
 axis(0,0)
 if Dialog.is_dialogue_active():Dialog.close_dialogue()
 if P.is_sprint_mode_enabled()!=sprint_initial:key('Gamepad_LeftThumbstick')
 restored=G.return_to_world();cmd('pm.EnvPerf2.Viewport 0 0');settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.unregister_slate_post_tick_callback(unreal._env3_foot);(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'checks':s['checks'],'distance_m':s['distance']/100,'battles':s['battles'],'save_unchanged':hashlib.sha256(slot.read_bytes()).hexdigest()==sha,'preview_restored':restored,'no_in_route_test_teleports':True,'setup_position_cm':[-760,-1410,48.15],'input':'existing pm.Input software simulation, no hardware claim'},indent=2));unreal.log('ENV3_FOOT_FINISH '+str(error));unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
def progress(info=None):
 s['checks'].append({'name':route[s['i']][1],'pos':P.get_actor_location().to_tuple(),**(info or{})});s.update(i=s['i']+1,elapsed=0.,local={},stuck=0.);(O/'Progress.json').write_text(json.dumps(s['checks'],indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);delta=now-s['lasttime'];s['lasttime']=now;s['elapsed']+=delta;pos=P.get_actor_location();d=(pos-s['lastpos']).length();s['lastpos']=pos
  if d<1000:s['distance']+=d
  assert time.monotonic()-start<900;assert pos.z>-20 and not cm.is_falling();assert P.get_component_by_class(unreal.CameraComponent).field_of_view==35
  if s['i']==len(route):finish();return
  k,name,arg=route[s['i']];t=s['elapsed'];loc=s['local']
  if Enc.is_encounter_active():
   axis(0,0);pr=Enc.get_presenter();v=pr.get_view()
   if not loc.get('battle'):loc['battle']=True;s['battles']+=1
   if not v.busy and not v.finished:
    if v.must_switch:assert pr.try_select_switch(next(i for i,c in enumerate(v.player_team)if c.can_switch))
    elif v.flee_enabled:assert pr.try_select_flee()
    else:assert pr.try_select_move(0)
    assert pr.resolve_selection()
   s['elapsed']-=delta;return
  if k=='walk':
   dx=arg[0]-pos.x;dy=arg[1]-pos.y;distance=math.hypot(dx,dy)
   if distance<25:axis(0,0);progress();return
   x,y=worldinput(dx,dy);ang=round(math.atan2(x,y)/(math.pi/4))*math.pi/4;mag=max(.38,min(1,distance/90));axis(math.sin(ang)*mag,math.cos(ang)*mag);s['stuck']=s['stuck']+delta if d<.1 else 0;assert s['stuck']<5,('Blocked',name,pos)
  elif k=='hold':
   if t>arg[2]:axis(0,0);progress()
   else:x,y=worldinput(*arg[:2]);axis(x,y)
  elif k=='pause':
   axis(0,0)
   if t>arg:progress()
  elif k=='shot':
   axis(0,0)
   if t>1 and not loc.get('shot'):cmd('HighResShot 2560x1440 filename="'+str(O/(name+'.png'))+'"');loc['shot']=True
   if t>2:progress()
  elif k=='menu':assert PC.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY);assert P.is_overworld_input_locked();assert PC.close_menu();assert not P.is_overworld_input_locked();progress()
  elif k=='save':assert Save.save_current_game() and Save.load_game();assert hashlib.sha256(slot.read_bytes()).hexdigest()==sha;progress({'ram_only':True})
  elif k=='inside':assert cut.is_viewer_relocated() and P.is_using_interior_movement_basis();progress()
  elif k=='outside':assert not cut.is_viewer_relocated() and not P.is_using_interior_movement_basis();progress()
  elif k=='interact':
   axis(0,0)
   if t>.35 and not loc.get('pressed'):key(B);loc['pressed']=True
   if Dialog.is_dialogue_active():progress()
   assert t<3,('B interaction failed',name)
  elif k=='dialog':
   if not Dialog.is_dialogue_active():progress()
   elif t-loc.get('lastpress',0)>.65:key(B);loc['lastpress']=t
  elif k=='heal':assert all(c.current_hp==c.calculated_stats.max_hp for c in Enc.get_player_party());progress()
  elif k in ['directions','sprint']:
   if k=='sprint'and not loc.get('on'):key('Gamepad_LeftThumbstick');loc['on']=True
   if t<4:
    a=min(7,int(t/.5))*math.pi/4;axis(math.sin(a),math.cos(a))
   else:
    axis(0,0)
    if k=='sprint'and P.is_sprint_mode_enabled():key('Gamepad_LeftThumbstick')
    progress()
 except Exception:finish(traceback.format_exc())
unreal._env3_foot=unreal.register_slate_post_tick_callback(tick)
