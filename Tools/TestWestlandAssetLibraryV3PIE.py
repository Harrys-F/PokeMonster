"""Walk the additive forest with real eight-direction Enhanced Input. No teleports.
Camera is never set by the test. Screenshot only after it has settled.
"""
import unreal,json,math,time
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibraryV3';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandAssetLibrary' in w.get_name();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);move=p.get_component_by_class(unreal.CharacterMovementComponent);arm=p.get_component_by_class(unreal.SpringArmComponent);cam=p.get_component_by_class(unreal.CameraComponent);assert move.max_walk_speed==210 and arm.target_arm_length==2500 and cam.field_of_view==35
for cmd in ['t.MaxFPS 0','r.VSync 0','sg.ViewDistanceQuality 1','sg.AntiAliasingQuality 1','sg.ShadowQuality 1','sg.GlobalIlluminationQuality 1','sg.ReflectionQuality 1','sg.PostProcessQuality 1','sg.TextureQuality 1','sg.EffectsQuality 1','sg.FoliageQuality 1','r.ScreenPercentage 75']:unreal.SystemLibrary.execute_console_command(w,cmd)
sub=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);act=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
route=[('walk','V2Approach',(-10,-11)),('walk','V2View',(-4,-17.5)),('shot','V2_Forest',None),('walk','ForestSouth',(3,-19)),('walk','V3View',(10,-19)),('shot','V3_Forest',None),('walk','BushB',(13,-17)),('shot','V3_Bushes',None),('walk','EastPath',(13,-13)),('walk','NorthPath',(10,-8)),('shot','V3_Trunk',None),('walk','RootNorth',(10,-11.2)),('walk','RootWest',(8.4,-11.3)),('walk','RootWestSouth',(8.1,-14)),('walk','RootSouth',(10,-15)),('walk','RootEast',(11.8,-14)),('walk','RootEastNorth',(11.8,-11.5)),('walk','Clear',(13,-10)),('walk','ToReviewLoop',(6,-9)),('walk','Return',(-10,-9)),('walk','Start',(-14,-9)),('menu','OverworldMenu',None)]
if (O/'FootViewJob.json').exists():
 job=json.loads((O/'FootViewJob.json').read_text());route=[('walk',x[0],(x[1],x[2])) for x in job['points']]+[('shot',job['name'],None)];output=job['name']+'FootTest.json'
else:output='FootTest.json'
i=0;pause=None;shot=False;distance=0;last=p.get_actor_location();seconds=0;wall=time.monotonic();stuck=0;directions=set();result={'checks':[],'screenshots':[],'no_test_teleports':True,'camera':[2500,-55,-45,35],'movement_cm_s':210}
def inject(x,y):sub.inject_input_vector_for_action(act,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 inject(0,0);unreal.unregister_slate_post_tick_callback(unreal._wla_v3_walk);del unreal._wla_v3_walk;result.update({'passed':error is None,'error':error,'distance_m':distance/100,'game_seconds':seconds,'wall_seconds':time.monotonic()-wall,'directions_used':sorted(directions)});(O/output).write_text(json.dumps(result,indent=2));unreal.log('WLA_V3_FOOT_DONE '+str(error))
def tick(dt):
 global i,pause,shot,distance,last,seconds,stuck
 try:
  seconds+=dt;q=p.get_actor_location();step=(q-last).length();distance+=step;last=q;assert q.z>40,'Fell below ground';assert move.max_walk_speed==210
  if i>=len(route):finish();return
  kind,label,target=route[i]
  if kind=='walk':
   e=(q.x+q.y)/math.sqrt(2)/100;n=(q.x-q.y)/math.sqrt(2)/100;dx=target[0]-e;dy=target[1]-n
   if math.hypot(dx,dy)<.28:inject(0,0);result['checks'].append({'point':label,'E_N_m':[e,n],'grounded':not move.is_falling()});i+=1;stuck=0;return
   idx=round(math.atan2(dy,dx)/(math.pi/4));a=idx*math.pi/4;inject(math.cos(a),math.sin(a));directions.add(idx%8);stuck=stuck+dt if step<.2 else 0;assert stuck<5,('Movement blocked',label,e,n)
  elif kind=='shot':
   inject(0,0)
   if pause is None:pause=seconds+1.8;shot=False
   elif seconds>=pause and not shot:
    path=O/('PIE_'+label+'.png');unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+str(path)+'"',pc);result['screenshots'].append(str(path));pause=seconds+.8;shot=True
   elif shot and seconds>=pause:i+=1;pause=None
  else:
   inject(0,0);assert pc.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY);assert p.is_overworld_input_locked();assert pc.close_menu();assert not p.is_overworld_input_locked();result['checks'].append({'menu_locks_and_returns_control':True});i+=1
 except Exception as error:finish(str(error))
assert not hasattr(unreal,'_wla_v3_walk');unreal._wla_v3_walk=unreal.register_slate_post_tick_callback(tick)
