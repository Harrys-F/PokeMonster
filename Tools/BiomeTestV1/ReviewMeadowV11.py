"""Actual normal PIE footwalk, natural hover lifecycle and bounded flight. Never teleports or writes a save."""
import unreal,json,sys,math,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
req=json.loads((R/'Saved/BiomeTestV11/MeadowReviewRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
hs={h.habitat_name:h for h in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat)};assert len(hs)==15 and sum(len(h.runtime_specimens)for h in hs.values())==16
names={'Raupy':'RaupyWiese','Hornliu':'HornliuWiese','Smettbo':'SmettboFlug','Bibor':'BiborFlug','Habitak':'HabitakFlug'};vs={n:hs[k].runtime_specimens[0]for n,k in names.items()};profiles={n:hs[k].specimens[0].species.get_visuals().presentation for n,k in names.items()};assert all(not x.get_validation_errors()for x in profiles.values())
inp=next(a for a in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if a.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==p and a.get_name()=='MoveAction');sprint=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==p and a.get_name()=='SprintHoldAction')
rock=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor)if a.get_actor_label()=='Biome_HabitakLowRock_V11');rc,re=rock.get_actor_bounds(False);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
route=[('FlightObservation',-1700,1850,120),('MeadowCentre',-2700,2700,22),('HerbsAndCrawlers',-2100,3300,12),('Hub',0,0,0)]
s={'i':0,'phase':'walk','last':unreal.GameplayStatics.get_time_seconds(w),'time':0.,'wall':time.monotonic(),'prev':p.get_actor_location(),'distance':0.,'stuck':0.,'sample':-10.,'rows':[],'shots':[],'states':set(),'departures':[],'overflights':[],'max_hover':0.,'air_distance':0.,'bird_prev':vs['Habitak'].get_actor_location(),'record_requested':False,'record_stopped':False,'record_seen_hover':False,'late_motion':{}};bones={};travel={};record_dir=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('BiomeV11_'+req['label']);assert not record_dir.exists()
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def inject(x,y):inp.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1,0,0),[],[])
def shot(label):
 path=O/(label+'_QHD.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['shots'].append(str(path.relative_to(R)))
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_meadow_v11);inject(0,0);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 if s['record_requested']and not s['record_stopped']and record_dir.exists():cmd('pm.TAAReview.CaptureStop');s['record_stopped']=True
 ranges={n:max(math.dist(v,values[0])for v in values)if values else 0 for n,values in bones.items()}
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'normal_PIE':True,'no_teleports':True,'distance_m':s['distance']/100,'steps':s['i'],'total':len(route),'travel_cm':travel,'late_observation_motion_cm':s['late_motion'],'pose_ranges':ranges,'bird_states':sorted(s['states']),'max_hover_cm':s['max_hover'],'actual_hover_travel_cm':s['air_distance'],'overflights':s['overflights'],'overflight_required_in_this_run':req.get('require_overflight',True),'habitat_departures':s['departures'],'shots':s['shots'],'native_recording_requested':s['record_requested'],'recording_directory':str(record_dir.relative_to(R)),'recording_requires_separate_actual_frame_verification':True,'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest()},indent=2));(O/'Telemetry.json').write_text(json.dumps(s['rows']));unreal.log('BIOME_MEADOW_REVIEW_DONE '+str(error))
def sample(now):
 for n,a in vs.items():
  h=hs[names[n]];q=a.get_actor_location();m=a.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent);travel[n]=m.distance_travelled
  if not h.contains_footprint(q,0):s['departures'].append({'species':n,'position':q.to_tuple()})
  assert a.get_actor_scale3d()==unreal.Vector(1,1,1);bone='segment_3'if n in ['Raupy','Hornliu']else'wing_upper_L'if n in ['Smettbo','Bibor']else'wing_L';t=a.mesh.get_socket_transform(bone,unreal.RelativeTransformSpace.RTS_COMPONENT);values=t.translation.to_tuple()+tuple(getattr(t.rotation,k)for k in ['x','y','z','w']);bones.setdefault(n,[]).append(values)
  s['rows'].append({'time':now,'species':n,'position':q.to_tuple(),'speed':m.current_speed,'travel_cm':m.distance_travelled,'goal':m.current_goal.to_tuple(),'behavior':str(m.behavior_state),'blocked':m.blocked_steps,'rejected':m.rejected_targets,'hover':a.get_ground_hover_state(),'hover_cm':a.get_ground_hover_height()})
  if n in ['Smettbo','Bibor']:assert abs(q.z-h.get_actor_location().z-h.float_clearance_cm)<.05
 a=vs['Habitak'];q=a.get_actor_location();state=a.get_ground_hover_state();s['states'].add(state);height=a.get_ground_hover_height();s['max_hover']=max(s['max_hover'],height)
 if state=='Hover':
  s['air_distance']+=(q-s['bird_prev']).length();s['record_seen_hover']=True
  if abs(q.x-rc.x)<re.x and abs(q.y-rc.y)<re.y:
   assert q.z+height>rc.z+re.z+15;s['overflights'].append({'time':now,'actor':q.to_tuple(),'visual_lift_cm':height,'actual_rock_top_cm':rc.z+re.z})
 s['bird_prev']=q
 if req.get('record',False)and state=='Takeoff'and not s['record_requested']:
  cmd('pm.TAAReview.CaptureStart "'+str(record_dir)+'"');s['record_requested']=True
 if s['record_requested']and s['record_seen_hover']and state=='Grounded'and not s['record_stopped']:
  assert record_dir.exists(),'Existing recorder did not accept our unique recording request';cmd('pm.TAAReview.CaptureStop');s['record_stopped']=True

def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now;s['time']+=delta;assert time.monotonic()-s['wall']<600;q=p.get_actor_location();dist=(q-s['prev']).length();assert dist<500,'Unexpected teleport';s['prev']=q;s['distance']+=dist
  if now-s['sample']>.16:sample(now);s['sample']=now
  if s['i']>=len(route):
   assert not s['departures'];assert all(travel[n]>30 for n in vs);assert {'Grounded','Takeoff','Hover','Landing'}<=s['states'],s['states'];assert s['air_distance']>120;assert s['overflights']or not req.get('require_overflight',True),'No actual obstacle overflight observed';assert 125<s['max_hover']<=140
   for n,v in bones.items():assert max(math.dist(x,v[0])for x in v)>1e-3,('No actual bone animation',n)
   assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;finish();return
  label,u,v,wait=route[s['i']]
  if s['phase']=='walk':
   x,y=L.local(q.x,q.y);du,dv=u-x,v-y;length=math.hypot(du,dv)
   if length>24:
    angle=round(math.atan2(du,dv)/(math.pi/4))*math.pi/4;mag=min(1,length/85);inject(math.sin(angle)*mag,math.cos(angle)*mag);s['stuck']=s['stuck']+delta if dist<.1 else 0;assert s['stuck']<5,('Blocked player route',label,[x,y,q.z]);return
   inject(0,0);s.update(phase='wait',time=0.,stuck=0.)
   if wait:shot(label)
   return
  inject(0,0)
  if s['time']>=wait:
   if label=='FlightObservation':
    for name in vs:
     recent=[x for x in s['rows']if x['species']==name and x['time']>=now-30];assert len(recent)>20;s['late_motion'][name]=recent[-1]['travel_cm']-recent[0]['travel_cm'];assert s['late_motion'][name]>30,('Persistent movement stopped after finite anchors',name,s['late_motion'][name])
    shot('FlightAreaAfterObservation')
   s.update(i=s['i']+1,phase='walk',time=0.)
 except Exception:finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 1280 720');cmd('r.ScreenPercentage 100');cmd('DisableAllScreenMessages 1');unreal._biome_meadow_v11=unreal.register_slate_post_tick_callback(tick)
