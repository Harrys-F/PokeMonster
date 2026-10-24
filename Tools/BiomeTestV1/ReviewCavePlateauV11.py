"""Normal PIE with existing Enhanced Input; only the building's authored masked relocation may teleport."""
import unreal,json,sys,math,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
req=json.loads((R/'Saved/BiomeTestV11/CaveReviewRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);cap=p.get_component_by_class(unreal.CapsuleComponent);cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBuildingCutaway)if a.get_actor_label()=='Biome_CaveInterior_V11');h=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat)if a.habitat_name=='Hoehle');assert len(h.runtime_specimens)==1
inp=next(a for a in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if a.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==p and a.get_name()=='MoveAction');sprint=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==p and a.get_name()=='SprintHoldAction')
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def room(x,y):return(25000+L.C*(x+y),L.C*(-x+y))
route=[]
def walk(name,xy,wait=0):route.append(('walk',name,xy,wait))
for i,(u,v,z)in enumerate(L.PLATEAU_APPROACH):walk('Ascent_'+str(i),L.world(u,v)[:2],5 if i==len(L.PLATEAU_APPROACH)-1 else 0)
for i,(u,v,z)in enumerate(reversed(L.PLATEAU_APPROACH[:-1])):walk('Descent_'+str(i),L.world(u,v)[:2])
for i,uv in enumerate(L.CAVE_ROUTE[:-1]):walk('CaveApproach_'+str(i),L.world(*uv)[:2],4 if i==len(L.CAVE_ROUTE)-2 else 0)
route.append(('enter','CaveEntry',None,2))
for name,xy in [('CaveCentre',room(0,0)),('CaveLeft',room(0,-400)),('CaveRear',room(550,100)),('CaveRight',room(100,400)),('CaveReturn',room(-790,0))]:walk(name,xy,5 if name=='CaveCentre'else 0)
route.append(('exit','CaveExit',None,2))
for i,uv in enumerate(reversed(L.CAVE_ROUTE[:-1])):walk('CaveReturn_'+str(i),L.world(*uv)[:2])
walk('Hub',(0,0))
s={'i':0,'stage':'walk','last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'time':0.,'stuck':0.,'prev':p.get_actor_location(),'distance':0.,'peak_foot_cm':0.,'relocations':[],'was_inside':cut.is_viewer_relocated(),'mask':0.,'rows':[],'shots':[],'frames':[],'frame_time':-10.,'cave_travel':0.}
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def inject(x,y,fast=True):inp.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1 if fast else 0,0,0),[],[])
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_cave_v11);inject(0,0);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'distance_m':s['distance']/100,'steps':s['i'],'total':len(route),'peak_player_foot_cm':s['peak_foot_cm'],'only_authored_masked_relocations':s['relocations'],'cave_creature_travel_cm':s['cave_travel'],'shots':s['shots'],'frames':s['frames'],'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest()},indent=2));(O/'Telemetry.json').write_text(json.dumps(s['rows']));unreal.log('BIOME_CAVE_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now;s['time']+=delta;assert time.monotonic()-s['wall']<600
  q=p.get_actor_location();dist=(q-s['prev']).length();s['prev']=q;inside=cut.is_viewer_relocated();mask=cut.get_relocation_mask()
  if dist>1000:
   assert inside!=s['was_inside']and max(mask,s['mask'])>.9,('Unexpected teleport',dist,inside,mask,s['mask']);s['relocations'].append({'entered':inside,'mask':mask,'previous_mask':s['mask'],'distance_cm':dist})
  else:s['distance']+=dist
  s['was_inside']=inside;s['mask']=mask;s['peak_foot_cm']=max(s['peak_foot_cm'],q.z-cap.get_scaled_capsule_half_height());assert q.z>-50,'Player fell below walkable floor'
  if inside:
   assert cut.is_viewer_in_relocated_room(q);a=h.runtime_specimens[0];assert cut.is_viewer_in_relocated_room(a.get_actor_location());m=a.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent);s['cave_travel']=max(s['cave_travel'],m.distance_travelled)
  if s['i']>=len(route):
   assert 1490<s['peak_foot_cm']<1520;assert len(s['relocations'])==2 and s['relocations'][0]['entered']and not s['relocations'][1]['entered'];assert s['cave_travel']>30;assert not inside and cut.get_cutaway_amount()<.01;assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;finish();return
  kind,name,target,wait=route[s['i']]
  if s['stage']=='walk':
   reached=False
   if kind in ['enter','exit']:
    reached=inside==(kind=='enter')and(cut.get_cutaway_amount()>.99 if kind=='enter'else cut.get_cutaway_amount()<.01)
    if not reached:inject(0,.65 if kind=='enter'else-.65,False)
   else:
    dx,dy=target[0]-q.x,target[1]-q.y;du,dv=L.local(dx,dy);length=math.hypot(du,dv);reached=length<24
    if not reached:
     angle=round(math.atan2(du,dv)/(math.pi/4))*math.pi/4;mag=min(1,length/85);inject(math.sin(angle)*mag,math.cos(angle)*mag)
   if not reached:
    s['stuck']=s['stuck']+delta if dist<.1 else 0;assert s['stuck']<5,('Blocked',name,L.local(q.x,q.y),q.z);return
   inject(0,0);s.update(stage='wait',time=0.,stuck=0.);s['rows'].append({'point':name,'position':q.to_tuple(),'inside':inside,'cutaway':cut.get_cutaway_amount(),'camera':pc.player_camera_manager.get_camera_location().to_tuple()})
   if wait:
    path=O/(name+'_QHD.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['shots'].append(str(path.relative_to(R)))
   return
  inject(0,0)
  if wait and now-s['frame_time']>.16:
   d=O/'Frames';d.mkdir(exist_ok=True);path=d/(str(len(s['frames'])).zfill(4)+'.png');cmd('HighResShot 1280x720 filename="'+str(path)+'"');s['frames'].append({'path':str(path.relative_to(R)),'game_time':now,'kind':name});s['frame_time']=now
  if s['time']>=wait:s.update(i=s['i']+1,stage='walk',time=0.)
 except Exception:finish(traceback.format_exc())
cmd('DisableAllScreenMessages 1');cmd('r.ScreenPercentage 100');unreal._biome_cave_v11=unreal.register_slate_post_tick_callback(tick)
