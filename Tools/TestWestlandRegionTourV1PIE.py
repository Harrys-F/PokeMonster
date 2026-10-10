"""Real PIE regional tour. Ordinary Enhanced Input walking and existing UI commands.
No test teleport, speed override, camera override, battle-rule or party-state mutation.
Existing building relocation remains part of gameplay. Evidence is saved under Saved/.
"""
import unreal,json,math,time,sys,statistics
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/WestlandRegion';sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'));import WestlandRegionLayout as L;import importlib;importlib.reload(L)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandRegion' in w.get_name()
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);cm=p.get_component_by_class(unreal.CharacterMovementComponent);mgr=unreal.GameplayStatics.get_player_camera_manager(w,0)
sub=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);act=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
gi=unreal.GameplayStatics.get_game_instance(w);enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem) if x.get_outer()==gi);dlg=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem) if x.get_outer()==gi)
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};cut=actors['HouseCutaway'];mode=json.loads((OUT/'TourJob.json').read_text())['mode'];route=[]
def path(name,points):
 for e,n in L.sample(points,spacing=4):route.append(('walk',name,L.world(e,n)[:2]))
def straight(name,points):
 for a,b in zip(points,points[1:]):
  steps=max(1,math.ceil(math.dist(a,b)/3))
  for j in range(steps+1):route.append(('walk',name,L.world(*(a[k]+(b[k]-a[k])*j/steps for k in (0,1)))[:2]))
def close(name,q):route.append(('close',name,[q.x,q.y]))
def shot(name):route.append(('shot',name,None))
def action(kind,label,target=None):route.append((kind,label,target))
def door(c,offset,rel=False):
 t=c.get_editor_property('relocated_door_threshold' if rel else 'door_threshold');q=t.get_world_location();r=t.get_world_rotation();return q+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(offset,0,0),r.yaw,unreal.Vector(0,0,1))
if mode=='west':
 path('Farm_forecourt',[(-300,-220),(-300,-228),(-312,-228),(-312,-225)]);shot('31_Hof_Haus');path('Farm_NPC',[(-312,-225),(-303,-223),(-299,-217.1)]);close('Wanderer_approach',unreal.Vector(*L.world(-299,-217.1)));action('interact','Wanderer','WR_NPC_0');action('dialogue','Wanderer_pages');action('menu','Team_inventory_menu')
 path('Hof_Dorf',[(-299,-217.1)]+L.MAIN[:6]);shot('32_Dorfplatz')
 c=actors['WR_Gasthaus_Cutaway'];q=door(c,-300);en=L.en(q.x,q.y);path('Inn_front',[(-220,-35),(-215,-48),en]);shot('33_Gasthaus');path('Inn_return',[en,(-215,-48),(-220,-35)])
 path('Healing_access',L.PATHS[1][1]);q=door(cut,-300);path('Healing_front',[(-310,190),L.en(q.x,q.y)]);shot('34_Heilhaus_Aussen');close('Healing_door_front',door(cut,-90));action('enter','Healing_threshold');shot('35_Heilhaus_Innen')
 center=cut.get_editor_property('relocated_interior_area').get_world_location();close('Interior_center',center);healer=actors['HouseHealer'];q=healer.get_actor_location()+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(-195,0,0),-45,unreal.Vector(0,0,1));close('Healer_approach',q);action('interact','Heilerin','HouseHealer');action('dialogue','Heilung_save_confirmation');action('healed','HP_PP_full');shot('36_Heilerin')
 close('Interior_return_center',center);close('Interior_door',door(cut,90,True));action('exit','Healing_exit');shot('37_Healing_exit');close('Exterior_clear_door',door(cut,-220));path('Healing_to_north',[L.en(door(cut,-220).x,door(cut,-220).y),(-310,190)])
 path('Nordrunde',L.PATHS[2][1][:4]);shot('38_Aussicht');path('Circle',L.PATHS[2][1][3:6]);shot('39_Steinkreis');path('North_return',L.PATHS[2][1][5:]);path('Stone_bridge',L.MAIN[7:13]);shot('40_Steinbruecke_Rueckblick');path('Wild_approach',[(125,10),(148,8),(154,9)]);close('Wild_close',unreal.Vector(*L.world(154,9)));shot('41_Wildkreatur');action('interact','Wild_meadow','WR_Wild_0');action('battle','Wild_battle');action('menu','Menu_after_battle');shot('42_Nach_Wildkampf')
elif mode=='review':
 # Normal foot circuit after the south replay. All landmark screenshots use the player camera.
 shot('60_Wildwiesen');path('Meadow_bank',[(154,9),(148,8),(125,10),L.PATHS[5][1][0]]);path('Bank_to_mill',L.PATHS[5][1]);path('Mill_side',[(145,-210),(153,-220),(153,-239)]);straight('Mill_front',[(153,-239),(153,-237),(145,-237)]);shot('69_Muehle')
 r=L.river(-235);straight('Mill_to_bridge',[(145,-237),(153,-237),(153,-235),(r+12,-235),(r+8,-235),(r-8,-235),(r-12,-235)]);shot('70_Holzbruecke');path('Mill_to_farm',[(r-12,-235),(-35,-245),(-125,-255),(-225,-245),(-300,-220)]);path('Farm_front',[(-300,-220),(-300,-228),(-312,-228),(-312,-225)]);shot('68_Spielerhof')
 path('Farm_village',[(-312,-225),(-300,-228),(-300,-220)]+L.MAIN[:6]);shot('63_Dorfplatz');c=actors['WR_Gasthaus_Cutaway'];q=door(c,-450);en=L.en(q.x,q.y);path('Inn_front',[(-220,-35),(-215,-48),en]);shot('64_Gasthaus');path('Inn_return',[en,(-215,-48),(-220,-35)])
 path('Healing_access',L.PATHS[1][1]);q=door(cut,-450);path('Healing_front',[(-310,190),L.en(q.x,q.y)]);shot('65_Heilhaus');close('Healing_door_front',door(cut,-90));action('enter','Healing_threshold');shot('66_Heilhaus_Innen')
 center=cut.get_editor_property('relocated_interior_area').get_world_location();close('Interior_center',center);close('Interior_door',door(cut,90,True));action('exit','Healing_exit');close('Exterior_clear_door',door(cut,-220));path('Healing_to_north',[L.en(door(cut,-220).x,door(cut,-220).y),(-310,190)]);path('Nordrunde',L.PATHS[2][1][:6]);shot('67_Steinkreis');path('North_return',L.PATHS[2][1][5:]);path('Bridge_meadows',L.MAIN[7:14]);shot('71_Steinbruecke');path('Forest_route',L.MAIN[13:18]);shot('61_Waldruinen');path('Exit',L.MAIN[17:]);shot('62_Regionsausgang')
elif mode=='south':
 r=L.river(-235);west=(r-12,-235);east=(r+12,-235)
 path('Farm_mill_return',[(-300,-220),(-225,-245),(-125,-255),(-35,-245),west]);shot('50_Holzbruecke_Westufer')
 path('Wood_bridge_east',[west,(r-8,-235),(r+8,-235),east]);path('Mill_front',[east,(153,-235),(153,-240),(153,-220),(145,-210)]);shot('51_Muehle_Fassade')
 path('Wood_bridge_back',[(145,-210),(153,-220),(153,-240),(153,-235),east,(r+8,-235),(r-8,-235),west]);shot('52_Holzbruecke_Querung')
 path('Wood_bridge_again',[west,(r-8,-235),(r+8,-235),east,(153,-235),(153,-240),(153,-220),(145,-210)]);path('River_bank_return',list(reversed(L.PATHS[5][1])));shot('53_Uferweg');path('Wild_meadow_return',[L.PATHS[5][1][0],(125,10),(154,9)]);shot('54_Wildwiesen_Final')

else:
 # Starts at the end of the west tour in the same running PIE session.
 path('Meadow_rejoin',[(154,9),(148,8),(125,10)]);path('Forest_route',L.MAIN[12:18]);shot('43_Waldruinen');path('Exit',L.MAIN[17:]);shot('44_Regionsausgang');path('Exit_return',list(reversed(L.MAIN[17:])))
 path('Forest_loop',L.PATHS[4][1][:3]);shot('45_Verborgene_Lichtung');path('Forest_loop_return',L.PATHS[4][1][2:]);path('Meadows_return',list(reversed(L.MAIN[11:14])));path('River_hidden',L.PATHS[5][1][:3]);shot('46_Uferfund');path('River_to_mill',L.PATHS[5][1][2:]);path('Mill',L.PATHS[3][1][4:6]);shot('47_Muehle');path('Wood_bridge',L.PATHS[3][1][5:9]);shot('48_Holzbruecke');path('Farm_return',L.PATHS[3][1][8:]);shot('49_Hof_Rueckkehr')
state={'mode':mode,'index':0,'passed':False,'errors':[],'start_wall':time.monotonic(),'start_game':unreal.GameplayStatics.get_time_seconds(w),'foot_m':0,'max_speed_cm_s':0,'screenshots':[],'checks':[],'runtime_relocations':[]};resume=OUT/'TourResume.json'
if resume.exists():
 r=json.loads(resume.read_text());assert r['mode']==mode;state['index']=r['index'];state['resume_evidence']=r['previous']
last=p.get_actor_location();last_wall=time.monotonic();frame_ms=[];last_game=state['start_game'];stuck=0;pause=0;busy=False;phase=0;deadline=0

def inject(x,y):sub.inject_input_vector_for_action(act,unreal.Vector(x,y,0),[],[])
def steer(q):
 dx=q[0]-p.get_actor_location().x;dy=q[1]-p.get_actor_location().y;yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;t=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;a=round(math.sin(t));b=round(math.cos(t));d=max(1,math.hypot(a,b));inject(a/d,b/d)
def done():
 global phase,deadline,stuck,pause
 inject(0,0);state['index']+=1;phase=0;deadline=0;stuck=0;pause=0

def finish(error=None):
 if error:state['errors'].append(str(error))
 inject(0,0);unreal.unregister_slate_post_tick_callback(unreal._wr_tour);del unreal._wr_tour
 state.update(wall_seconds=time.monotonic()-state['start_wall'],game_seconds=unreal.GameplayStatics.get_time_seconds(w)-state['start_game'])
 if frame_ms:state['frame_ms']={'median':statistics.median(frame_ms),'p95':sorted(frame_ms)[int(len(frame_ms)*.95)],'samples':len(frame_ms),'mean_fps':1000/statistics.mean(frame_ms)}
 (OUT/('Tour_'+mode+'.json')).write_text(json.dumps(state,indent=2));unreal.log('REGION_TOUR_DONE '+mode+' '+str(state['passed'])+' '+str(error))

def tick(dt):
 global last,last_wall,last_game,stuck,pause,busy,phase,deadline
 if busy:return
 busy=True
 try:
  now=time.monotonic();game=unreal.GameplayStatics.get_time_seconds(w);v=p.get_actor_location();distance=math.hypot(v.x-last.x,v.y-last.y)
  if distance>2000:state['runtime_relocations'].append({'from':[last.x,last.y,last.z],'to':[v.x,v.y,v.z],'inside':cut.is_viewer_relocated()});assert cut.get_editor_property('use_relocated_interior')
  else:state['foot_m']+=distance/100
  state['max_speed_cm_s']=max(state['max_speed_cm_s'],math.hypot(p.get_velocity().x,p.get_velocity().y));frame_ms.append((now-last_wall)*1000);last_wall=now;last=v;assert cm.max_walk_speed==210;assert v.z>-1100,'Fell below terrain';kind,label,target=route[state['index']]
  if kind in ['walk','close']:
   remaining=math.hypot(target[0]-v.x,target[1]-v.y)
   if remaining<(90 if kind=='walk' else 28):done()
   else:
    steer(target);stuck=stuck+max(0,game-last_game) if distance<.2 else 0
    if stuck>4:raise RuntimeError('Blocked '+label+' at '+str(v))
  elif kind=='shot':
   inject(0,0)
   if not pause:pause=game+2;filename=OUT/('PIE_'+label+'.png');unreal.AutomationLibrary.take_high_res_screenshot(1280,720,str(filename),delay=.5);state['screenshots'].append(str(filename))
   elif game>=pause:done()
  elif kind in ['enter','exit']:
   entering=kind=='enter'
   if cut.is_viewer_relocated()==entering:
    state['checks'].append({'check':label,'relocated':entering,'cutaway':cut.get_cutaway_amount()});done()
   else:
    if not deadline:deadline=game+8
    assert game<deadline,'Door transition timeout';q=door(cut,130 if entering else -130,not entering);steer([q.x,q.y])
  elif kind=='interact':
   t=actors[target]
   if phase==0:
    q=t.get_actor_location();steer([q.x,q.y]);deadline=game+.10;phase=1
   elif game>=deadline:
    inject(0,0);found=p.find_interactable_in_range();assert found==t,'Interaction target unavailable: '+str(found);assert p.try_interact(),'Interaction refused';state['checks'].append({'check':label,'interactable':target});done()
  elif kind=='dialogue':
   inject(0,0);assert not pc.is_menu_open()
   if phase==0:assert dlg.is_dialogue_active(),'No dialogue';assert p.is_overworld_input_locked(),'Dialogue failed to lock';state['checks'].append({'check':label,'pages':dlg.get_page_count(),'input_locked':True});phase=1;deadline=game+1
   elif game>=deadline:
    if dlg.is_dialogue_active():pc.advance_dialogue();deadline=game+1
    else:assert not p.is_overworld_input_locked(),'Dialogue failed to unlock';done()
  elif kind=='menu':
   inject(0,0);assert not enc.is_encounter_active();assert pc.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY);assert p.is_overworld_input_locked();assert pc.close_menu();assert not p.is_overworld_input_locked();state['checks'].append({'check':label,'menu_locked_and_unlocked':True});done()
  elif kind=='healed':
   team=enc.get_player_party();assert team
   for c in team:
    assert c.current_hp==c.calculated_stats.max_hp
    for slot in c.move_slots:assert slot.current_pp==slot.max_pp
   assert (ROOT/'Saved/SaveGames/PokeMonster_Dev.sav').exists();state['checks'].append({'check':label,'team_count':len(team),'save_exists':True});done()
  elif kind=='battle':
   inject(0,0)
   if phase==0:assert enc.is_encounter_active(),'No wild encounter';assert p.is_overworld_input_locked();assert not pc.open_menu();phase=1;deadline=game+180;state['checks'].append({'check':label,'menu_blocked_during_battle':True})
   elif not enc.is_encounter_active():
    result=enc.get_last_result();state['checks'].append({'check':label,'result':str(result.outcome),'rounds':result.rounds,'kind':str(result.kind)});assert not p.is_overworld_input_locked();done()
   else:
    assert game<deadline,'Battle timeout';presenter=enc.get_presenter();view=presenter.get_view()
    if not view.busy and not view.presentation_pending and not view.finished:
     widget=enc.get_battle_widget()
     if view.must_switch:
      i=next(i for i,t in enumerate(view.player_team) if t.can_switch);widget.call_method('Team'+str(i))
     else:
      i=next(i for i,m in enumerate(view.moves) if m.enabled);widget.call_method('Move'+str(i))
  last_game=game;state['stage']=label;state['position_cm']=[v.x,v.y,v.z];state['game_elapsed']=game-state['start_game'];state['camera']={'pitch':mgr.get_camera_rotation().pitch,'yaw':mgr.get_camera_rotation().yaw,'fov':mgr.get_fov_angle()}
  if state['index']==len(route):state['passed']=True;finish()
  else:(OUT/'TourProgress.json').write_text(json.dumps(state,indent=2))
 except Exception as e:finish(e)
 busy=False
assert not hasattr(unreal,'_wr_tour');unreal._wr_tour=unreal.register_slate_post_tick_callback(tick)
