"""Normal PIE, existing Enhanced Input and collision; no teleports, disk saves or battle fixtures."""
import unreal,json,sys,time,math,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
request=json.loads((R/'Saved/BiomeTestV11/WaterReviewRequest.json').read_text());label=request['label'];clip=request.get('motion_sequence',False);O=R/'Saved/BiomeTestV11'/label;O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);save=next(a for a in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if a.get_outer()==gi)
inp=next(a for a in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if a.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==p and a.get_name()=='MoveAction');sprint=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==p and a.get_name()=='SprintHoldAction')
habitats={a.habitat_name:a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat)};assert len(habitats)==10;assert sum(len(h.runtime_specimens)for h in habitats.values())==11
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();assert not save.save_current_game()and not save.load_game()and not save.delete_dev_save()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
route=[('WaterApproach',1600,1600,0),('JettyApproach',1900,2800,0),('JettyObservation',2500,2800,40),('JettyReturn',1750,2800,0),('WestBank',1750,2800,15),('NorthBank',1900,3650,0),('BridgeWest',2850,4100,0),('BridgeEast',3910,4100,0),('EastBank',4420,3000,25),('BridgeReturnEast',3910,4100,0),('BridgeReturnWest',2850,4100,0),('NorthReturn',1750,3650,0),('WestReturn',1750,2800,0),('JunctionReturn',1600,1600,0),('Hub',0,0,0)]
if clip:route=[(n,u,v,min(wait,6))for n,u,v,wait in route]
s={'i':0,'time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'previous':p.get_actor_location(),'distance':0.,'stuck':0.,'sample':-1.,'frame':-10.,'stage':'walk','rows':[],'shots':[],'frames':[]};bones={};first={};travel={};media={};departures=[]
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def inject(x,y):inp.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1,0,0),[],[])
cmd('r.ScreenPercentage 100');cmd('DisableAllScreenMessages 1')
def sample(now):
 for key,bone in [('Karpador','tail_tip'),('Garados','body_5'),('SchiggyUfer','hand_L')]:
  h=habitats[key];assert len(h.runtime_specimens)==1;v=h.runtime_specimens[0];q=v.get_actor_location();m=v.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent);profile=h.specimens[0].presentation_override or h.specimens[0].species.get_visuals().presentation;assert not profile.get_validation_errors();assert profile.mesh==v.mesh.get_skeletal_mesh_asset();assert not v.effect_components
  if not h.contains_footprint(q,0):departures.append((key,q.to_tuple()))
  if v.aquatic_pose_alpha>.8:
   b=v.mesh.get_socket_transform(bone,unreal.RelativeTransformSpace.RTS_COMPONENT).translation.to_tuple();bones.setdefault(key,[]).append(b)
  media.setdefault(key,set()).add('water'if v.aquatic_pose_alpha>.8 else'land');travel[key]=m.distance_travelled
  s['rows'].append({'t':now,'name':key,'position':q.to_tuple(),'speed':v.motion_speed,'aquatic':v.aquatic_pose_alpha,'travel_cm':m.distance_travelled,'blocked':m.blocked_steps,'rejected':m.rejected_targets,'goal':m.current_goal.to_tuple(),'state':str(m.behavior_state)})
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_water_v11);inp.inject_input_vector_for_action(move,unreal.Vector(),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(),[],[]);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 ranges={k:max(math.dist(a,b)for a in vs for b in [vs[0]])if vs else 0 for k,vs in bones.items()}
 result={'passed':error is None,'error':error,'normal_PIE':True,'no_teleports':True,'distance_m':s['distance']/100,'steps':s['i'],'total':len(route),'bone_motion_ranges_cm':ranges,'travel_cm':travel,'media':{k:sorted(v)for k,v in media.items()},'habitat_departures':departures,'shots':s['shots'],'frames':s['frames'],'original_save_sha256':before,'after_save_sha256':hashlib.sha256(slot.read_bytes()).hexdigest()};(O/'Result.json').write_text(json.dumps(result,indent=2));(O/'Telemetry.json').write_text(json.dumps(s['rows']));unreal.log('BIOME_WATER_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now;s['time']+=delta;assert time.monotonic()-s['wall']<420
  q=p.get_actor_location();dist=(q-s['previous']).length();s['previous']=q;s['distance']+=dist;assert q.z>-100,'Player fell into deep water'
  if now-s['sample']>.3:sample(now);s['sample']=now
  if s['i']>=len(route):
   assert not departures and all(travel.get(k,0)>30 for k in ['Karpador','Garados','SchiggyUfer'])
   for k in ['Karpador','Garados','SchiggyUfer']:
    assert len(bones.get(k,[]))>4 and max(math.dist(v,bones[k][0])for v in bones[k])>.3,('No actual swim-bone animation',k)
   assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;finish();return
  name,u,v,wait=route[s['i']]
  if s['stage']=='walk':
   x,y=L.local(q.x,q.y);du,dv=u-x,v-y;length=math.hypot(du,dv)
   if length>24:
    angle=round(math.atan2(du,dv)/(math.pi/4))*math.pi/4;mag=min(1,length/85);inject(math.sin(angle)*mag,math.cos(angle)*mag);s['stuck']=s['stuck']+delta if dist<.1 else 0;assert s['stuck']<5,('Blocked walk',name,[x,y,q.z]);return
   inject(0,0);s.update(stage='wait',time=0,stuck=0)
   if wait:
    path=O/(name+'_QHD.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['shots'].append(str(path.relative_to(R)))
   return
  inject(0,0)
  if wait and now-s['frame']>(.14 if clip else 1.2):
   D=O/'Frames';D.mkdir(exist_ok=True);path=D/(str(len(s['frames'])).zfill(4)+'.png');cmd('HighResShot 1280x720 filename="'+str(path)+'"');s['frames'].append({'path':str(path.relative_to(R)),'game_time':now});s['frame']=now
  if s['time']>=wait:s.update(i=s['i']+1,stage='walk',time=0)
 except Exception:finish(traceback.format_exc())
unreal._biome_water_v11=unreal.register_slate_post_tick_callback(tick)
