"""Foot-only PIE integration replay for the saved Village Core V1.
Start ordinary PIE in Dev_WestlandVillage, then execute this file in its console.
Only normal eight-sector Enhanced Input is injected. Never move/teleport the pawn,
change speed, spawn, camera or runtime gameplay state. Review stages wait for the
local Saved/WestlandVillage/ContinueReview.txt acknowledgement after a screenshot.
Evidence is written only to ignored Saved/, never committed as an asset/test fixture.
"""
import unreal,json,math,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'Saved/WestlandVillage';R.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/'Art/World/Westland/WestlandVillage_V1.json').read_text())
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandVillage' in w.get_name()
p=unreal.GameplayStatics.get_player_pawn(w,0);mgr=unreal.GameplayStatics.get_player_camera_manager(w,0)
sub=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w)
act=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
cm=p.get_component_by_class(unreal.CharacterMovementComponent);sprite=p.get_character_flipbook_component()
actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor);by={a.get_actor_label():a for a in actors}
cuts={b['id']:by['WV_'+b['id']+'_Cutaway'] for b in data['buildings']};buildings={b['id']:b for b in data['buildings']}

def wp(b,point):
 c,s=math.cos(math.radians(b['yaw'])),math.sin(math.radians(b['yaw']))
 return (b['origin_cm'][0]+point[0]*c-point[1]*s,b['origin_cm'][1]+point[0]*s+point[1]*c)
route=[]
def walk(label,point):route.append(('walk',label,point))
def review(label):route.append(('review',label,None))
def pause(label,seconds=1.1):route.append(('pause',label,seconds))
def enter(b):
 door=b['door_world_cm'];walk(b['id']+'_WApproach',(door[0]-42.43,door[1]+42.43));route.append(('hold',b['id']+'_WEntry',(0,1,1.0)));pause(b['id']+'_Inside');review(b['id']+'_InteriorReview')
def exit(b):
 door=b['door_local_cm'];walk(b['id']+'_InsideDoor',wp(b,(door[0]+55,door[1])));route.append(('hold',b['id']+'_SExit',(0,-1,1.0)));pause(b['id']+'_Outside');walk(b['id']+'_ReturnForecourt',b['forecourt_cm'][:2])
review('01_Dorfeingang')
for i,pt in enumerate([(-1600,120),(-1000,-100),(-650,-250),(-300,-150)]):walk('Main_'+str(i),pt)
review('02_Dorfzentrum')
for i,pt in enumerate([(-1000,-100),(-1120,270),(-930,650),buildings['Birkenhof']['forecourt_cm'][:2]]):walk('HomePath_'+str(i),pt)
review('03_Wohnbereich')
b=buildings['Birkenhof'];enter(b);walk('Birkenhof_RoomCenter',wp(b,(0,0)))
for name,x,y in [('W',0,1),('D',1,0),('S',0,-1),('A',-1,0),('WD',1,1),('WA',-1,1),('SA',-1,-1),('SD',1,-1)]:
 route.extend([('hold','EightWay_'+name,(x,y,.7)),('pause','Idle_'+name,.3)])
exit(b)
# An independent diagonal door pass and diagonal exit in the validated cottage.
door=b['door_world_cm'];walk('Birkenhof_DiagonalApproach',(door[0]-60,door[1]));route.append(('hold','Birkenhof_DiagonalEntry',(1,1,.7)));pause('Birkenhof_DiagonalInside')
d=b['door_local_cm'];walk('Birkenhof_DiagonalExitStart',wp(b,(d[0]+60,d[1]+60)));route.append(('hold','Birkenhof_DiagonalExit',(-1,-1,.9)));pause('Birkenhof_DiagonalOutside');walk('Birkenhof_ForecourtAgain',b['forecourt_cm'][:2])
for i,pt in enumerate([(-650,1780),(-120,2160),(140,2080),buildings['Kraeuterhaus']['forecourt_cm'][:2]]):walk('HerbLane_'+str(i),pt)
review('04_GeschwungenerWeg');b=buildings['Kraeuterhaus'];enter(b);walk('Kraeuterhaus_RoomCenter',wp(b,(0,0)));exit(b)
for i,pt in enumerate([(140,2080),(-120,2160),(-650,1780),buildings['Birkenhof']['forecourt_cm'][:2],(-930,650),(-1120,270),(-1000,-100),(-650,-250),(-200,-150),(0,-60),buildings['Gasthaus']['forecourt_cm'][:2]]):walk('ToInn_'+str(i),pt)
review('05_Gasthausbereich');b=buildings['Gasthaus'];enter(b)
for label,pt in [('RoomCenter',(0,100)),('RearHall',(240,250)),('WingJoin',(400,200)),('RearWing',(430,300))]:walk('Gasthaus_'+label,wp(b,pt))
review('06_GasthausRueckfluegel')
for label,pt in [('WingNotchSide',(420,-100)),('MainHall',(0,100)),('CounterApproach',(60,-130))]:walk('Gasthaus_'+label,wp(b,pt))
exit(b)
for i,pt in enumerate([(0,-60),(190,540),(790,750),buildings['Langhaus']['forecourt_cm'][:2]]):walk('EastLane_'+str(i),pt)
review('07_Langhaus');b=buildings['Langhaus'];enter(b);walk('Langhaus_RoomCenter',wp(b,(0,0)));exit(b)
for i,pt in enumerate([(790,750),(190,540),(0,-60),buildings['Gasthaus']['forecourt_cm'][:2],(-260,-450),(-350,-900),buildings['Wiesenhaus']['forecourt_cm'][:2]]):walk('GardenLane_'+str(i),pt)
review('08_Wiesenhaus');b=buildings['Wiesenhaus'];enter(b);walk('Wiesenhaus_RoomCenter',wp(b,(0,0)));exit(b)
for i,pt in enumerate([(-440,-1870),(-1250,-1880),(-1600,-1200),(-1450,-1410),(-1130,-1350)]):walk('HealingReserve_'+str(i),pt)
review('09_Heilhausplatz')
for i,pt in enumerate([(-1450,-1410),(-1600,-1200),(-1500,-490),(-1000,-100),(-1600,120),data['player_start_cm'][:2]]):walk('ReturnToStart_'+str(i),pt)
pause('Final_Outside');review('10_ReturnedToStart')
state={'index':0,'start_wall':time.monotonic(),'stage_start':unreal.GameplayStatics.get_time_seconds(w),'snapshots':[],'directions':[],'passed':False,'foot_distance_cm':0,'max_speed':0,'movement_game_seconds':0,'reviews':[],'errors':[]}
last_pos=p.get_actor_location();frames=(R/'PIEFrames.jsonl').open('w')
if hasattr(unreal,'_village_route_handle'):unreal.unregister_slate_post_tick_callback(unreal._village_route_handle)

def inject(x,y,magnitude=1):
 n=max(1,math.hypot(x,y));sub.inject_input_vector_for_action(act,unreal.Vector(x/n*magnitude,y/n*magnitude,0),[],[])
def vec(v):return [v.x,v.y,v.z]
def sample():
 r=mgr.get_camera_rotation();fb=sprite.get_flipbook()
 return {'game_time':unreal.GameplayStatics.get_time_seconds(w),'stage':route[state['index']][1],'position':vec(p.get_actor_location()),'velocity':vec(p.get_velocity()),'speed':p.get_velocity().length(),'basis_yaw':p.get_movement_basis_yaw(),'interior_mode':p.is_using_interior_movement_basis(),'cuts':{name:{'active':c.is_cutaway_active(),'amount':c.get_cutaway_amount()} for name,c in cuts.items()},'camera':{'location':vec(mgr.get_camera_location()),'rotation':[r.pitch,r.yaw,r.roll],'fov':mgr.get_fov_angle()},'sprite_scale':vec(sprite.get_editor_property('relative_scale3d')),'flipbook':fb.get_name() if fb else None,'facing':str(p.get_facing_direction()),'state':str(p.get_locomotion_state())}
def check_endpoint(label,d):
 for name,b in buildings.items():
  if label in (name+'_Inside',name+'_DiagonalInside'):
   assert cuts[name].get_cutaway_amount()==1 and p.is_using_interior_movement_basis(),label
   assert abs((d['basis_yaw']-b['yaw']+180)%360-180)<.02,label
   assert abs(d['camera']['rotation'][0]+50)<.02 and abs(d['camera']['fov']-35)<.01,label
   # Exact active room camera uses focus+target and the configured distance.
   focus=b.get('cutaway_focus_local_cm',[0,0,150]);q=wp(b,focus);target=unreal.Vector(q[0],q[1],b['origin_cm'][2]+focus[2]-70)
   assert abs((mgr.get_camera_location()-target).length()-b['camera_distance_cm'])<.1,label
   occl=cuts[name].get_editor_property('occluding_actors');assert all(a.get_editor_property('hidden') for a in occl),label+' hidden'
   retained=[a for a in actors if a.actor_has_tag('WV_Building_'+name) and a.actor_has_tag('WV_Retained')];assert all(not a.get_editor_property('hidden') for a in retained),label+' retained'
  if label in (name+'_Outside',name+'_DiagonalOutside','Final_Outside'):
   assert all(c.get_cutaway_amount()==0 for c in cuts.values()) and not p.is_using_interior_movement_basis(),label
   assert abs(d['basis_yaw']+45)<.02 and abs(d['camera']['rotation'][0]+55)<.02,label
   assert abs(d['camera']['rotation'][1]+45)<.02 and abs(d['camera']['fov']-35)<.01,label

def progress():
 d=sample();check_endpoint(route[state['index']][1],d);state['snapshots'].append(d);state['index']+=1;state['stage_start']=unreal.GameplayStatics.get_time_seconds(w)
 if state['index']==len(route):state['passed']=True;finish()
def finish(error=None):
 if error:state['errors'].append(str(error))
 unreal.unregister_slate_post_tick_callback(unreal._village_route_handle);del unreal._village_route_handle;frames.close()
 try:inject(0,0)
 except Exception:pass
 state['wall_seconds']=time.monotonic()-state['start_wall'];(R/'PIERoute.json').write_text(json.dumps(state,indent=2));unreal.log('WV_FOOT_ROUTE_PASSED' if state['passed'] else 'WV_FOOT_ROUTE_FAILED '+str(error))
def tick(dt):
 global last_pos
 try:
  kind,label,arg=route[state['index']];d=sample();previous_game_time=state.get('last_game_time',d['game_time']);state['last_game_time']=d['game_time'];elapsed=d['game_time']-state['stage_start'];v=p.get_actor_location();state['foot_distance_cm']+=math.hypot(v.x-last_pos.x,v.y-last_pos.y);last_pos=v;state['max_speed']=max(state['max_speed'],math.hypot(d['velocity'][0],d['velocity'][1]))
  assert cm.get_editor_property('max_walk_speed')==210
  assert abs(sprite.get_editor_property('relative_scale3d').z-1.086758)<.00001
  assert v.z>-70,'Player fell below terrain'
  frames.write(json.dumps(d)+'\n')
  if kind=='walk':
   state['movement_game_seconds']+=max(0,d['game_time']-previous_game_time);dx=arg[0]-v.x;dy=arg[1]-v.y
   if math.hypot(dx,dy)<12:inject(0,0);progress();return
   if elapsed>35:raise RuntimeError('Blocked '+label+' at '+str(vec(v)))
   yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;angle=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;inject(round(math.sin(angle)),round(math.cos(angle)),min(1,math.hypot(dx,dy)/220))
  elif kind=='hold':
   state['movement_game_seconds']+=max(0,d['game_time']-previous_game_time)
   if elapsed>=arg[2]:
    if label.startswith('EightWay_'):state['directions'].append(d)
    inject(0,0);progress();return
   inject(arg[0],arg[1])
  elif kind=='pause':
   inject(0,0)
   if elapsed>=arg:progress()
  elif kind=='review':
   inject(0,0)
   (R/'Progress.json').write_text(json.dumps({'label':label,'kind':'review','state':d},indent=2))
   ack=R/'ContinueReview.txt'
   if ack.exists() and ack.read_text().strip()==label:
    state['reviews'].append(d);progress()
 except Exception as e:finish(e)
unreal._village_route_handle=unreal.register_slate_post_tick_callback(tick);unreal.log('WV_FOOT_ROUTE_READY')
