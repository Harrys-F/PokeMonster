"""Ordinary Enhanced Input walk through the enriched ruin, no teleports or saves."""
import unreal,json,sys,time,math,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
req=json.loads((R/'Saved/BiomeTestV11/RuinReviewRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);h=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat)if x.habitat_name=='Ruine');a=h.runtime_specimens[0]
inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w);move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='MoveAction');sprint=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='SprintHoldAction')
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
route=[('ForestApproach',1500,-1500,0),('RuinApproach',2800,-2800,0),('Portal',3000,-2800,3),('RuinCentre',3000,-3400,4),('WestAisle',2700,-3420,0),('RearWest',2700,-3700,0),('Runestone',3000,-3700,3),('RearEast',3300,-3700,0),('EastAisle',3300,-3400,0),('RuinCentreReturn',3000,-3400,12),('PortalReturn',3000,-2800,0),('RuinApproachReturn',2800,-2800,0),('ForestReturn',1500,-1500,0),('Hub',0,0,0)]
s={'i':0,'stage':'walk','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'prev':p.get_actor_location(),'distance':0.,'stuck':0.,'rows':[],'shots':[],'departures':[],'sample':-1.,'recording':False};rec=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('BiomeV11_'+req['label']);assert not rec.exists()
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def inject(x,y):inp.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1,0,0),[],[])
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_ruin_v11);inject(0,0);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 if s['recording']:cmd('pm.TAAReview.CaptureStop')
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'normal_PIE':True,'no_teleports':True,'steps':s['i'],'total':len(route),'distance_m':s['distance']/100,'gengar_travel_cm':a.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent).distance_travelled,'departures':s['departures'],'rows':s['rows'],'shots':s['shots'],'recording':str(rec.relative_to(R)),'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest()},indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now;s['time']+=delta;assert time.monotonic()-s['wall']<360;q=p.get_actor_location();dist=(q-s['prev']).length();assert dist<500;s['prev']=q;s['distance']+=dist;assert q.z>-30
  if now-s['sample']>.3:
   if not h.contains_footprint(a.get_actor_location(),0):s['departures'].append(a.get_actor_location().to_tuple())
   s['sample']=now
  if s['i']>=len(route):
   assert not s['departures'];assert a.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent).distance_travelled>30;assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;finish();return
  name,u,v,wait=route[s['i']]
  if s['stage']=='walk':
   x,y=L.local(q.x,q.y);du,dv=u-x,v-y;length=math.hypot(du,dv)
   if length>24:
    angle=round(math.atan2(du,dv)/(math.pi/4))*math.pi/4;mag=min(1,length/85);inject(math.sin(angle)*mag,math.cos(angle)*mag);s['stuck']=s['stuck']+delta if dist<.1 else 0;assert s['stuck']<5,('Blocked ruin route',name,[x,y,q.z]);return
   inject(0,0);s.update(stage='wait',time=0.,stuck=0.);s['rows'].append({'name':name,'position':q.to_tuple()})
   if name=='Portal'and req.get('record',False):cmd('pm.TAAReview.CaptureStart "'+str(rec)+'"');s['recording']=True
   if wait:
    path=O/(name+'_QHD.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['shots'].append(str(path.relative_to(R)))
   return
  inject(0,0)
  if s['time']>=wait:
   if name=='Runestone'and s['recording']:cmd('pm.TAAReview.CaptureStop');s['recording']=False
   s.update(i=s['i']+1,stage='walk',time=0.)
 except Exception:finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 1280 720');cmd('r.ScreenPercentage 100');cmd('DisableAllScreenMessages 1');unreal._biome_ruin_v11=unreal.register_slate_post_tick_callback(tick)
