"""Local walking test through the actual Enhanced Input movement action; no teleports."""
import unreal,math,time,json,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/TreeShadowProxyV1';D=R/'Art/World/TreeShadowProxyV1/Review';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);cm=p.get_component_by_class(unreal.CharacterMovementComponent);cam=p.get_component_by_class(unreal.CameraComponent);arm=p.get_component_by_class(unreal.SpringArmComponent)
s=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
for c in unreal.ObjectIterator(unreal.SkeletalMeshComponent):
 if c.get_world()==w:c.set_editor_property('pause_anims',False)
route=[(-4300,1550),(-4500,1850),(-4100,2000),(-3650,2120),(-3270,2000),(-2890,2050),(-2300,2000),(-2150,1750),(-2300,2100),(-3300,2050),(-4100,1800),(-4300,1550)]
startpos=p.get_actor_location();near=(startpos-unreal.Vector(*route[0],startpos.z)).length()<50
if not near:
 assert (startpos-unreal.Vector(-760,-1410,startpos.z)).length()<160,('Unexpected saved start; do not teleport',startpos)
 route=[(startpos.x,startpos.y),(-1150,-1920),(-2100,-2060),(-3350,-1700),(-4150,-700),(-4100,450)]+route
i=1;distance=0;last=p.get_actor_location();started=time.monotonic();stage=started;stuck=0;records=[];frames=[];lastshot=0
def inject(x,y):s.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 inject(0,0);unreal.unregister_slate_post_tick_callback(unreal._tree_walk);del unreal._tree_walk
 (D/'WalkTest.json').write_text(json.dumps({'passed':error is None,'error':error,'no_test_teleports':True,'distance_m':distance/100,'steps':records,'frames':frames,'seconds':time.monotonic()-started},indent=2))
def tick(dt):
 global i,distance,last,stage,stuck,lastshot
 try:
  q=p.get_actor_location();step=(q-last).length();assert step<100,'Unexpected relocation';distance+=step;last=q
  assert cm.max_walk_speed==210 and cam.field_of_view==35 and arm.target_arm_length==2850
  assert not cm.is_falling() and q.z>-20
  proxies=[a.static_mesh_component for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.get_actor_label().startswith('TSP_')]
  assert len(proxies)==6 and all(c.get_editor_property('hidden_in_game') and c.cast_shadow and c.get_editor_property('cast_hidden_shadow') and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION for c in proxies)
  if i>=len(route):finish();return
  dx=route[i][0]-q.x;dy=route[i][1]-q.y;dist=math.hypot(dx,dy)
  if dist<22:
   inject(0,0);records.append({'waypoint':i,'position':q.to_tuple(),'seconds':time.monotonic()-started});i+=1;stage=time.monotonic();stuck=0;return
  yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;ang=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;inject(math.sin(ang)*min(1,dist/90),math.cos(ang)*min(1,dist/90));stuck=stuck+dt if step<.1 else 0;assert stuck<4,('Blocked',i,q)
  frames.append({'time':time.monotonic()-started,'position':q.to_tuple(),'velocity':p.get_velocity().to_tuple()})
  if time.monotonic()-lastshot>2:
   lastshot=time.monotonic();unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(O/('Walk_'+str(len(frames)).zfill(5)+'.png'))+'"',pc)
 except Exception:finish(traceback.format_exc())
unreal._tree_walk=unreal.register_slate_post_tick_callback(tick)
