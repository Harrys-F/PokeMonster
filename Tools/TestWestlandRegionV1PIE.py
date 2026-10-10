"""Actual walking replay, using only ordinary eight-sector Enhanced Input.
No pawn transform, speed, camera or gameplay-state changes. Evidence stays in Saved/.
Run in PIE; choose 'main' or 'loops' in Saved/WestlandRegion/WalkJob.json.
"""
import unreal,json,math,time,sys,statistics
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/WestlandRegion';sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'))
import WestlandRegionLayout as L
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandRegion' in w.get_name()
p=unreal.GameplayStatics.get_player_pawn(w,0);cm=p.get_component_by_class(unreal.CharacterMovementComponent);mgr=unreal.GameplayStatics.get_player_camera_manager(w,0)
sub=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);act=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
mode=json.loads((OUT/'WalkJob.json').read_text())['mode'];route=[]
def path(name,points):
 pts=L.sample(points,spacing=4)
 for e,n in pts:route.append(('walk',name,L.world(e,n)[:2]))
def shot(name):route.append(('shot',name,None))
if mode=='main':
 shot('01_Spielerhof')
 checkpoints=[(0,'Hof'),(5,'Dorf'),(10,'Steinbruecke'),(13,'Wildwiesen'),(17,'Waldruinen'),(20,'Ausgang')]
 for (a,label),(b,nextlabel) in zip(checkpoints,checkpoints[1:]):path(label+'_'+nextlabel,L.MAIN[a:b+1]);shot('%02d_%s'%(b,nextlabel))
else:
 # Start from normal PlayerStart, not from an arbitrary screenshot position.
 path('Hof_Dorf',L.MAIN[:6]);path('Heilhauszugang',L.PATHS[1][1]);shot('21_Heilhausterrasse')
 path('Nordrunde',L.PATHS[2][1][:6]);shot('22_Steinkreis');path('Nordrunde_Rueckweg',L.PATHS[2][1][5:]);path('Bruecke_Wiese',L.MAIN[7:13])
 path('Muehlenrunde',L.PATHS[3][1][:6]);shot('23_Muehle');path('Holzbruecke',L.PATHS[3][1][5:9]);shot('24_Holzbruecke');path('Hof_Rueckkehr',L.PATHS[3][1][8:]);shot('25_Hof_Rueckkehr')
state={'mode':mode,'index':0,'passed':False,'errors':[],'start_wall':time.monotonic(),'start_game':unreal.GameplayStatics.get_time_seconds(w),'foot_m':0,'max_speed_cm_s':0,'screenshots':[],'arrivals':[]};last=p.get_actor_location();last_wall=time.monotonic();frame_ms=[];last_game=state['start_game'];stuck=0;pause=0;busy=False
def inject(x,y):sub.inject_input_vector_for_action(act,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 if error:state['errors'].append(str(error))
 inject(0,0);unreal.unregister_slate_post_tick_callback(unreal._wr_walk);del unreal._wr_walk
 state.update(wall_seconds=time.monotonic()-state['start_wall'],game_seconds=unreal.GameplayStatics.get_time_seconds(w)-state['start_game'])
 if frame_ms:state['frame_ms']={'median':statistics.median(frame_ms),'p95':sorted(frame_ms)[int(len(frame_ms)*.95)],'samples':len(frame_ms),'mean_fps':1000/statistics.mean(frame_ms)}
 (OUT/('Walk_'+mode+'.json')).write_text(json.dumps(state,indent=2));unreal.log('REGION_WALK_DONE '+str(state['passed'])+' '+str(error))
def tick(dt):
 global last,last_wall,last_game,stuck,pause,busy
 if busy:return
 busy=True
 try:
  now=time.monotonic();game=unreal.GameplayStatics.get_time_seconds(w);v=p.get_actor_location();distance=math.hypot(v.x-last.x,v.y-last.y);state['foot_m']+=distance/100;state['max_speed_cm_s']=max(state['max_speed_cm_s'],math.hypot(p.get_velocity().x,p.get_velocity().y));frame_ms.append((now-last_wall)*1000);last_wall=now;last=v
  assert cm.max_walk_speed==210;assert v.z>-1100,'Fell below river/terrain';kind,label,target=route[state['index']]
  if kind=='shot':
   inject(0,0)
   if not pause:
    pause=game+2;filename=OUT/('PIE_'+label+'.png');unreal.AutomationLibrary.take_high_res_screenshot(1280,720,str(filename),delay=.5);state['screenshots'].append(str(filename))
   elif game>=pause:pause=0;state['index']+=1
  else:
   dx=target[0]-v.x;dy=target[1]-v.y;remaining=math.hypot(dx,dy)
   if remaining<90:state['index']+=1;stuck=0
   else:
    yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;t=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;inject(round(math.sin(t))/max(1,math.hypot(round(math.sin(t)),round(math.cos(t)))),round(math.cos(t))/max(1,math.hypot(round(math.sin(t)),round(math.cos(t)))))
    stuck=stuck+max(0,game-last_game) if distance<.2 else 0
    if stuck>4:raise RuntimeError('Blocked '+label+' at '+str(v))
  last_game=game;state['stage']=label;state['position_cm']=[v.x,v.y,v.z];state['game_elapsed']=game-state['start_game'];state['camera']={'pitch':mgr.get_camera_rotation().pitch,'yaw':mgr.get_camera_rotation().yaw,'fov':mgr.get_fov_angle()}
  (OUT/'WalkProgress.json').write_text(json.dumps(state,indent=2))
  if state['index']==len(route):state['passed']=True;finish()
 except Exception as e:finish(e)
 busy=False
assert not hasattr(unreal,'_wr_walk');unreal._wr_walk=unreal.register_slate_post_tick_callback(tick)
