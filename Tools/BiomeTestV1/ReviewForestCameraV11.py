"""Ordinary PIE footwalk through local forest camera, entrance/exit, ruin and hub. No teleports or disk saves."""
import unreal,json,sys,time,math,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
req=json.loads((R/'Saved/BiomeTestV11/ForestReviewRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);arm=p.get_component_by_class(unreal.SpringArmComponent);cam=p.get_component_by_class(unreal.CameraComponent);vis=p.get_component_by_class(unreal.PokeMonsterCameraVisibilityComponent);z=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterForestCameraZone)[0];assert z.get_editor_property('bEnabled')
inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w);move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='MoveAction');sprint=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='SprintHoldAction')
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
route=[('OriginalForestClearing',1500,-1500,2),('ForestApproach',2000,-1500,0),('CanopyEntry',2300,-1500,2),('DensePathWest',2400,-1800,0),('UnderCanopy',3200,-1800,5),('DensePathEast',3600,-2000,2),('UnderCanopyReturn',3200,-1800,0),('DensePathWestReturn',2400,-1800,0),('ForestExit',1900,-1500,3),('ClearingBeforeRuin',1500,-1500,0),('RuinApproach',2800,-2800,0),('RuinPortal',3000,-2800,0),('RuinCentre',3000,-3400,3),('RuinExit',3000,-2800,0),('RuinApproachReturn',2800,-2800,0),('ForestClearingReturn',1500,-1500,0),('Hub',0,0,3)]
s={'i':0,'stage':'walk','last':unreal.GameplayStatics.get_time_seconds(w),'time':0.,'wall':time.monotonic(),'prev':p.get_actor_location(),'distance':0.,'stuck':0.,'best_length':1e9,'no_progress':0.,'rows':[],'shots':[],'sample':-1.,'original':arm.target_arm_length,'intermediate_frames':0,'faded_max':0,'recording':False,'arm_previous':arm.target_arm_length,'max_step_cm':0.};rec=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('BiomeV11_'+req['label']);assert not rec.exists()
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def inject(x,y):inp.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1,0,0),[],[])
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_forest_review);inject(0,0);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 if s['recording']:cmd('pm.TAAReview.CaptureStop')
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'normal_PIE':True,'no_teleports':True,'distance_m':s['distance']/100,'steps':s['i'],'total':len(route),'intermediate_transition_frames':s['intermediate_frames'],'maximum_faded_tree_count':s['faded_max'],'max_observed_arm_step_cm':s['max_step_cm'],'rows':s['rows'],'shots':s['shots'],'recording':str(rec.relative_to(R)),'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest()},indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now;s['time']+=delta;assert time.monotonic()-s['wall']<400;q=p.get_actor_location();dist=(q-s['prev']).length();assert dist<500;s['prev']=q;s['distance']+=dist
  assert 1699.99<=arm.target_arm_length<=2850.01;assert cam.field_of_view==35 and vis.reveal_radius_scale==2.;rot=arm.get_editor_property('relative_rotation');assert abs(rot.pitch+50)<.01 and abs(rot.yaw+45)<.01
  step=abs(arm.target_arm_length-s['arm_previous']);s['max_step_cm']=max(s['max_step_cm'],step);assert step<=2200*max(delta,.001)+2.,('Abrupt camera step',step,delta);s['arm_previous']=arm.target_arm_length
  if .01<z.current_amount<.99:s['intermediate_frames']+=1
  s['faded_max']=max(s['faded_max'],vis.get_dense_canopy_faded_tree_count())
  if s['i']>=len(route):
   assert s['intermediate_frames']>10 and s['faded_max']>0;assert arm.target_arm_length==2850 and vis.dense_canopy_amount==0 and vis.get_dense_canopy_faded_tree_count()==0;assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;finish();return
  name,u,v,wait=route[s['i']]
  if s['stage']=='walk':
   x,y=L.local(q.x,q.y);du,dv=u-x,v-y;length=math.hypot(du,dv)
   if length>24:
    if length<s['best_length']-5:s['best_length']=length;s['no_progress']=0.
    else:s['no_progress']+=delta
    assert s['no_progress']<8,('No progress along forest review route',name,[x,y,q.z])
    angle=round(math.atan2(du,dv)/(math.pi/4))*math.pi/4;mag=min(1,length/85);inject(math.sin(angle)*mag,math.cos(angle)*mag);s['stuck']=s['stuck']+delta if dist<.1 else 0;assert s['stuck']<5,('Blocked forest route',name,[x,y,q.z]);return
   inject(0,0);s.update(stage='wait',time=0.,stuck=0.)
   if name=='ForestApproach'and req.get('record',False):cmd('pm.TAAReview.CaptureStart "'+str(rec)+'"');s['recording']=True
   return
  inject(0,0)
  if s['time']>=wait:
   if name in ['OriginalForestClearing','ForestExit','RuinCentre','Hub']:assert arm.target_arm_length==2850 and vis.dense_canopy_amount==0
   if name in ['UnderCanopy','DensePathEast']:assert arm.target_arm_length==1700 and vis.get_dense_canopy_faded_tree_count()>0
   if wait:
    path=O/(name+'_QHD.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['shots'].append(str(path.relative_to(R)))
   s['rows'].append({'name':name,'position':q.to_tuple(),'arm_cm':arm.target_arm_length,'dense_amount':vis.dense_canopy_amount,'faded_trees':vis.get_dense_canopy_faded_tree_count()})
   if name=='ForestExit'and s['recording']:cmd('pm.TAAReview.CaptureStop');s['recording']=False
   s.update(i=s['i']+1,stage='walk',time=0.,best_length=1e9,no_progress=0.);(O/'Progress.json').write_text(json.dumps({'completed':s['i'],'total':len(route),'last':name,'distance_m':s['distance']/100}))
 except Exception:finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 1280 720');cmd('r.ScreenPercentage 100');cmd('DisableAllScreenMessages 1');unreal._biome_forest_review=unreal.register_slate_post_tick_callback(tick)
