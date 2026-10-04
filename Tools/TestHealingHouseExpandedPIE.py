"""Foot-only PIE replay of the optional expanded interior.
Start normal PIE in the Healing House map, then execute this file. Movement is
only normalized eight-sector Enhanced Input. No pawn transform or speed setter.
Review checkpoints wait for Saved/HealingExpanded/ContinueReview.txt.
Only deliberate party HP/PP test setup changes gameplay state; the healer itself
performs healing, checkpoint activation and saving through the normal dialogue.
Back up the dev save before this test and restore it afterwards.
"""
import unreal,json,math,time
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();R=ROOT/'Saved/HealingExpanded';R.mkdir(parents=True,exist_ok=True)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_HealingHouseTestMap'
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);mgr=pc.player_camera_manager
sub=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w)
move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
interact=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='InteractAction')
actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor);by={a.get_actor_label():a for a in actors}
cut=by['HouseCutaway'];cm=p.get_component_by_class(unreal.CharacterMovementComponent);sprite=p.get_character_flipbook_component()
gi=unreal.GameplayStatics.get_game_instance(w)
def subsystem(cls):return next(x for x in unreal.ObjectIterator(cls) if x.get_outer()==gi)
enc=subsystem(unreal.PokeMonsterEncounterSubsystem);dialog=subsystem(unreal.PokeMonsterDialogueSubsystem);save=subsystem(unreal.PokeMonsterSaveSubsystem);checkpoint=next(x for x in unreal.ObjectIterator(unreal.GameInstanceSubsystem) if x.get_outer()==gi and x.get_class().get_name()=='PokeMonsterCheckpointSubsystem')
team=list(enc.get_player_party());assert team
# A normal existing demo battle creates genuine HP/PP depletion for the rest test.
if not enc.is_encounter_active():assert enc.start_test_encounter(p,None)
route=[('battleprepare','PrepareDepletedParty',None)]
def walk(label,x,y):route.append(('walk',label,(x,y)))
def inside(label,x,y):walk(label,20000+x,y)
def hold(label,x,y,seconds):route.append(('hold',label,(x,y,seconds)))
def pause(label,seconds=.7):route.append(('pause',label,seconds))
def review(label):route.append(('review',label,None))
review('01_Exterior');walk('WApproach',-510,60);review('02_BeforeEntry');hold('HeldWEntry',0,1,1.05);pause('Entered');review('03_Interior2600')
route += [('camera','Camera2200',2200.),('review','03_Interior2200',None),('camera','Camera2400',2400.),('review','03_Interior2400',None),('camera','CameraChosen2600',2600.)]
inside('FrontAisle',-250,0);inside('HerbTableApproach',-345,270);inside('BedsApproach',-30,260);review('05_BedsAndSeating')
inside('SeatingApproach',390,160);inside('RearFreeAisle',470,80);inside('HealerApproachViaSide',380,120);inside('HealerSide',330,55)
hold('FaceHealer',-1,0,.45);pause('HealerFacing',.25);review('04_Healer')
route += [('interact','HealerInteract',None),('dialog','HealerDialogue',None),('verifyheal','VerifyHealCheckpointSave',None)]
inside('ReturnAisleViaSide',330,150);inside('ReturnAisle',0,170);inside('InsideDoor',-440,0);review('06_ExitView');hold('SExit',0,-1,.85);pause('Exited')
# Nine more round trips, including diagonal W in the exterior's camera basis and
# W+D (world-straight exterior). W+A/W+D diagonals continue inside the room.
for i in range(1,10):
    if i%2:walk('Approach'+str(i),-510,60);hold('WEntry'+str(i),0,1,1.05)
    else:walk('Approach'+str(i),-510,0);hold('WDEntry'+str(i),1,1,.85)
    pause('Entered'+str(i))
    if i in (2,4):
        inside('HeldDiagonalStart'+str(i),-250,0);hold('HeldWA' if i==2 else 'HeldWD',-1 if i==2 else 1,1,.45)
    inside('DoorReturn'+str(i),-440,60 if i%2 else -60)
    hold('DiagonalExit'+str(i),-1 if i%2 else 1,-1,.85);pause('Exited'+str(i))
# Partial reversal before the midpoint, then immediately complete a re-entry.
walk('QuickApproach',-460,0);route.append(('reversein','QuickIn',None));route.append(('reverseout','QuickOut',None));pause('QuickReverseOutside')
walk('LastApproach',-510,60);hold('LastHeldW',0,1,1.05);pause('EnteredLast')
inside('FinalDoor',-440,0);hold('LastSExit',0,-1,.85);pause('ExitedLast');walk('ReturnForecourt',-850,0);pause('FinalOutside')
state={'index':0,'stage_start':unreal.GameplayStatics.get_time_seconds(w),'passed':False,'snapshots':[],'errors':[],'entries':0,'exits':0,'max_speed':0,'reviews':[]}
last=None;frames=(R/'Frames.jsonl').open('w')
if hasattr(unreal,'_healing_route_handle'):unreal.unregister_slate_post_tick_callback(unreal._healing_route_handle)
def vec(v):return [v.x,v.y,v.z]
def inject(x,y,magnitude=1):
 n=max(1,math.hypot(x,y));sub.inject_input_vector_for_action(move,unreal.Vector(x/n*magnitude,y/n*magnitude,0),[],[])
def sample():
 r=mgr.get_camera_rotation();v=p.get_actor_location();velocity=p.get_velocity()
 return {'time':unreal.GameplayStatics.get_time_seconds(w),'stage':route[state['index']][1],'position':vec(v),'velocity':vec(velocity),'basis':p.get_movement_basis_yaw(),'interior_mode':p.is_using_interior_movement_basis(),'relocated':cut.is_viewer_relocated(),'amount':cut.get_cutaway_amount(),'mask':cut.get_relocation_mask(),'camera':{'position':vec(mgr.get_camera_location()),'rotation':[r.pitch,r.yaw,r.roll],'fov':mgr.get_fov_angle()},'input':str(p.get_movement_input()),'facing':str(p.get_facing_direction())}
def finish(error=None):
 if error:state['errors'].append(str(error))
 unreal.unregister_slate_post_tick_callback(unreal._healing_route_handle);del unreal._healing_route_handle;frames.close();inject(0,0)
 (R/'PIERoute.json').write_text(json.dumps(state,indent=2));unreal.log('HH_EXPANDED_FOOT_PASSED' if state['passed'] else 'HH_EXPANDED_FOOT_FAILED '+str(error))
def progress():
 d=sample();label=route[state['index']][1]
 if label.startswith('Entered'):
  assert d['relocated'] and d['amount']==1 and p.is_using_interior_movement_basis(),label
  assert abs(d['basis'])<.02 and abs(d['camera']['rotation'][0]+50)<.02,label
 if label.startswith('Exited') or label in ('QuickReverseOutside','FinalOutside'):
  assert not d['relocated'] and d['amount']==0 and not p.is_using_interior_movement_basis(),label
  assert abs(d['basis']+45)<.02 and abs(d['camera']['rotation'][0]+55)<.02,label
 state['snapshots'].append(d);state['index']+=1;state['stage_start']=unreal.GameplayStatics.get_time_seconds(w);state.pop('review_requested',None)
 if state['index']==len(route):state['passed']=True;finish()
def tick(dt):
 global last
 try:
  kind,label,arg=route[state['index']];d=sample();elapsed=d['time']-state['stage_start'];v=p.get_actor_location()
  assert cm.get_editor_property('max_walk_speed')==210
  assert abs(sprite.get_editor_property('relative_scale3d').z-1.086758)<.00001
  assert v.z>-20,'Fell below floor'
  speed=math.hypot(*d['velocity'][:2]);state['max_speed']=max(state['max_speed'],speed)
  if last and d['relocated']!=last['relocated']:
   if d['relocated']:state['entries']+=1
   else:state['exits']+=1
   # Mapping is absolute; ordinary locomotion between sampled frames is allowed.
   shift=19950 if d['relocated'] else -19950
   distance=math.hypot(d['position'][0]-last['position'][0]-shift,d['position'][1]-last['position'][1])
   assert distance<=210*max(.1,d['time']-last['time'])+2,'Unexpected lateral relocation'
   assert d['mask']>.99 and last['mask']>.99,'Spatial cut was not fully masked'
   assert abs(d['camera']['position'][0]-last['camera']['position'][0])>10000,'Camera must cut rather than fly'
  last=d;frames.write(json.dumps(d)+'\n')
  if kind=='battleprepare':
   inject(0,0)
   if not enc.is_encounter_active():
    state['before_healing']=[{'hp':m.current_hp,'max_hp':m.calculated_stats.max_hp,'pp':[s.current_pp for s in m.get_editor_property('move_slots')]} for m in enc.get_player_party()]
    assert any(m.current_hp<m.calculated_stats.max_hp for m in enc.get_player_party())
    progress()
   else:
    presenter=enc.get_presenter();view=presenter.get_view()
    if not view.busy and not view.finished:
     if view.must_switch:
      target=next(i for i,m in enumerate(view.player_team) if m.can_switch)
      assert presenter.try_select_switch(target)
     else:assert presenter.try_select_move(0)
     assert presenter.resolve_selection()
   if elapsed>120:raise RuntimeError('Preparation battle timeout')
  elif kind=='walk':
   dx=arg[0]-v.x;dy=arg[1]-v.y;distance=math.hypot(dx,dy)
   if distance<10:inject(0,0);progress();return
   if elapsed>25:raise RuntimeError('Blocked '+label+' at '+str(vec(v)))
   yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy
   angle=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;inject(round(math.sin(angle)),round(math.cos(angle)),min(1,distance/220))
  elif kind=='hold':
   if elapsed>=arg[2]:inject(0,0);progress();return
   inject(arg[0],arg[1])
  elif kind=='reversein':
   inject(1,1)
   if d['amount']>0:
    assert not d['relocated'],'Reversal must begin before the spatial cut'
    state['quick_reverse_amount']=d['amount'];inject(-1,-1);progress()
   elif elapsed>3:raise RuntimeError('Quick entry did not cross the threshold')
  elif kind=='reverseout':
   inject(-1,-1)
   if d['amount']==0 and v.x<-470:
    assert not d['relocated'];inject(0,0);progress()
   elif elapsed>4:raise RuntimeError('Quick reversal did not recover exterior')
  elif kind=='pause':
   inject(0,0)
   settled=(not (label.startswith('Entered') or label.startswith('Exited') or label in ('QuickReverseOutside','FinalOutside'))
    or (abs(d['basis']-(0 if label.startswith('Entered') else -45))<.02 and d['amount']==(1 if label.startswith('Entered') else 0)))
   if elapsed>=arg and settled:progress()
   elif elapsed>4:raise RuntimeError('Endpoint did not settle: '+label)
  elif kind=='camera':
   inject(0,0);cut.set_editor_property('interior_camera_distance',arg);progress()
  elif kind=='review':
   inject(0,0)
   (R/'Progress.json').write_text(json.dumps({'label':label,'state':d},indent=2))
   if not state.get('review_requested') and elapsed>.6:
    unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(R/'Review'/label)+'.png"',pc);state['review_requested']=True
   ack=R/'ContinueReview.txt'
   if ack.exists() and ack.read_text().strip()==label:state['reviews'].append(label);progress()
  elif kind=='interact':
   inject(0,0);sub.inject_input_vector_for_action(interact,unreal.Vector(1,0,0),[],[])
   if dialog.is_dialogue_active():progress()
   elif elapsed>3:raise RuntimeError('Healer not reachable/facing incorrect')
  elif kind=='dialog':
   inject(0,0)
   if not dialog.is_dialogue_active():progress()
   elif elapsed>.7:dialog.advance_dialogue()
  elif kind=='verifyheal':
   party=enc.get_player_party();assert len(party)==len(team)
   for member in party:
    assert member.current_hp==member.calculated_stats.max_hp
    for slot in member.get_editor_property('move_slots'):
     if slot.get_editor_property('move'):assert slot.current_pp==slot.max_pp
   assert save.has_save_game()
   # SaveGame internals are deliberately not a writable Python API. Check the
   # serialized checkpoint identity and exact double-precision resting position;
   # C++ save/checkpoint automation separately validates deserialization.
   import struct
   checkpoint_position=p.get_actor_location()
   payload=(ROOT/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()
   assert b'Dev_HealingHouse' in payload and struct.pack('<ddd',*vec(checkpoint_position)) in payload
   state['gameplay']={'healed':True,'pp_full':True,'checkpoint_id':'Dev_HealingHouse','checkpoint_position':vec(checkpoint_position),'saved':True};progress()
 except Exception as error:finish(error)
unreal._healing_route_handle=unreal.register_slate_post_tick_callback(tick)
