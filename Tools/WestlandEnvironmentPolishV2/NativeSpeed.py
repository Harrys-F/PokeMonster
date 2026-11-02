"""Actual swept movement measurements and trunk/camera collision in an isolated native game."""
import unreal,json,time,math,statistics,sys,traceback,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';cfg=json.loads((D/'ActiveNative.json').read_text());O=D/cfg['label'];assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(O);sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0));P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);M=P.get_component_by_class(unreal.CharacterMovementComponent);sub=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if s.get_world()==W);move=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==P and a.get_name()=='GamepadMoveAction');clock=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==unreal.GameplayStatics.get_game_instance(W));assert P.get_test_speed_factor()==1
cases=[(source,factor,sprint)for source in ['WASD_software','Stick_action']for factor in [1,2,3]for sprint in [False,True]];state={'i':0,'phase':'place','at':time.monotonic()};rows=[];checks=[];start=time.monotonic();now0=unreal.GameplayStatics.get_time_seconds(W);clock0=clock.get_time().export_text();samples=[];root=None
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};points=[]
for label,a in actors.items():
 if not label.startswith(('WVU_Trees_','WEP_Canopy_','WEP_Sapling_')):continue
 c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
 for i in range(c.get_instance_count()):points.append(c.get_instance_transform(i,True).translation+unreal.Vector(0,0,100))
for q in points:
 e,n=L.en(q.x,q.y)
 if not(180<e<260 and 75<n<175):continue
 clear=True
 for other in points:
  if other==q:continue
  nearx=max(q.x+250,min(q.x+700,other.x))
  if math.hypot(other.x-nearx,other.y-q.y)<300:clear=False;break
 if clear:root=q;break

assert root

def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
def inject(v):sub.inject_input_vector_for_action(move,unreal.Vector(0,v,0),[],[])
def release():
 cmd('pm.Input.Key W up');cmd('pm.Input.Key LeftShift up');inject(0)
 if P.is_sprint_mode_enabled():cmd('pm.Input.Key Gamepad_LeftThumbstick down');cmd('pm.Input.Key Gamepad_LeftThumbstick up')
def setphase(n):state.update(phase=n,at=time.monotonic());(O/'Progress.json').write_text(json.dumps(dict(phase=n,index=state['i'],seconds=time.monotonic()-start)))
def position(e,n,yaw):
 x,y,z=L.world(e,n,L.height(e,n));P.set_actor_location(unreal.Vector(x,y,z+50.15),False,True);M.stop_movement_immediately();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=yaw),False,False)
def finish(error=None):
 release();cmd('pm.Speed 1');cmd('pm.Speed Status');assert P.get_test_speed_factor()==1
 if error is None:
  for probe in json.loads((D/'TerrainPhysicsProbes.json').read_text()):
   x,y,_=L.world(probe['e'],probe['n']);z=probe['expected_z_cm'];hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,z+4000),unreal.Vector(x,y,z-4000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[P]+[a for a in actors.values()if a.actor_has_tag('BiomePlayerWaterBarrier')],unreal.DrawDebugTrace.NONE);assert hit,probe
   match=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text());assert match;actual=float(match[1]);assert abs(actual-z)<1,('Cooked terrain mismatch',probe,actual);checks.append(dict(test='Actual cooked reshaped terrain collision',east_m=probe['e'],north_m=probe['n'],expected_z_cm=z,actual_z_cm=actual))
  graphics={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in ['r.ScreenPercentage','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.TemporalAA.Upsampling','r.Shadow.Virtual.Enable','r.Shadow.Virtual.SMRT.RayCountDirectional','sg.ViewDistanceQuality','sg.ShadowQuality','sg.GlobalIlluminationQuality','sg.TextureQuality','sg.FoliageQuality']};(O/'Graphics.json').write_text(json.dumps(graphics,indent=2))
 (O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,movement=rows,checks=checks,seconds=time.monotonic()-start,physical_gamepad=False,original_user_saves_used=False,world_game_seconds=unreal.GameplayStatics.get_time_seconds(W)-now0,clock_before=clock0,clock_after=clock.get_time().export_text()),indent=2));unreal.unregister_slate_post_tick_callback(unreal._wvu_speed);unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global samples
 try:
  assert time.monotonic()-start<180
  elapsed=time.monotonic()-state['at']
  if state['phase']=='place':
   release();position(-110,-185,math.degrees(math.atan2(40,70)));samples=[];setphase('settle')
  elif state['phase']=='settle'and elapsed>.5:
   source,factor,sprint=cases[state['i']];cmd('pm.Speed '+str(factor));assert P.get_test_speed_factor()==factor
   if source=='WASD_software':cmd('pm.Input.Key W down')
   else:inject(1)
   if sprint:
    if source=='WASD_software':cmd('pm.Input.Key LeftShift down')
    else:cmd('pm.Input.Key Gamepad_LeftThumbstick down');cmd('pm.Input.Key Gamepad_LeftThumbstick up')
   setphase('measure')
  elif state['phase']=='measure':
   source,factor,sprint=cases[state['i']]
   if source=='Stick_action':inject(1)
   if elapsed>.9:
    velocity=P.get_velocity();samples.append(math.hypot(velocity.x,velocity.y))
   if elapsed>2.7:
    expected=210*factor*(1.5 if sprint else 1);assert samples;vmax=max(samples);assert abs(M.max_walk_speed-expected)<.01;assert .94*expected<=vmax<=1.01*expected,(cases[state['i']],vmax,expected)
    rows.append(dict(source=source,factor=factor,sprint=sprint,expected_cm_s=expected,max_cm_s=vmax,mean_steady_cm_s=statistics.mean(samples),samples=len(samples)));release();state['i']+=1
    if state['i']<len(cases):setphase('place')
    else:
     cmd('pm.Speed 3');P.set_actor_location(unreal.Vector(root.x-250,root.y,root.z-100+50.15),False,True);M.stop_movement_immediately();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=0),False,False);state['min_distance']=999;setphase('trunk_settle')
  elif state['phase']=='trunk_settle'and elapsed>.7:
   cmd('pm.Input.Key W up');cmd('pm.Input.Key LeftShift down');setphase('trunk')
  elif state['phase']=='trunk':
   q=P.get_actor_location();dx=root.x-q.x;dy=root.y-q.y;yaw=math.radians(P.get_movement_basis_yaw());vx=-math.sin(yaw)*dx+math.cos(yaw)*dy;vy=math.cos(yaw)*dx+math.sin(yaw)*dy;norm=max(1,math.hypot(vx,vy));sub.inject_input_vector_for_action(move,unreal.Vector(vx/norm,vy/norm,0),[],[]);d=math.hypot(dx,dy);state['min_distance']=min(state['min_distance'],d);assert not(q.x>root.x and abs(q.y-root.y)<45),'Passed through physical trunk'
   if elapsed>2:
    release();capsule=P.get_component_by_class(unreal.CapsuleComponent);overlap=unreal.SystemLibrary.capsule_overlap_components(W,P.get_actor_location(),capsule.get_scaled_capsule_radius()-.5,capsule.get_scaled_capsule_half_height()-.5,[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],unreal.StaticMeshComponent,[P]);assert not overlap,('Actual capsule penetrates geometry',overlap);velocity=P.get_velocity();assert math.hypot(velocity.x,velocity.y)<5,'Not stopped at trunk';checks.append(dict(test='Factor3 swept authored trunk collision',minimum_center_distance_cm=state['min_distance'],capsule_overlap_components=0,position=P.get_actor_location().to_tuple()));P.set_actor_location(unreal.Vector(root.x+300,root.y,root.z-100+50.15),False,True);M.stop_movement_immediately();setphase('camera_near')
  elif state['phase']=='camera_near'and elapsed>1.2:
   distance=(PC.player_camera_manager.get_camera_location()-P.third_person_boom.get_world_location()).length();assert 0<distance<330,('Camera did not shorten',distance);assert abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.02;checks.append(dict(test='Existing spring-arm trunk collision',distance_cm=distance));P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=180),False,False);setphase('camera_clear')
  elif state['phase']=='camera_clear'and elapsed>1.2:
   distance=(PC.player_camera_manager.get_camera_location()-P.third_person_boom.get_world_location()).length();assert 340<distance<360;checks.append(dict(test='Camera clears and returns to existing 350cm',distance_cm=distance));cmd('pm.Speed 1');assert M.max_walk_speed==210;finish()
 except Exception:finish(traceback.format_exc())
unreal._wvu_speed=unreal.register_slate_post_tick_callback(tick)
