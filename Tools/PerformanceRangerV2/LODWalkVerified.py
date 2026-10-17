"""Targeted LOD-boundary walk. No continuous screenshot capture stalls; capture only switch/waypoint evidence."""
import unreal,json,time,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/V2/LODWalkVerified';O.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));c=v.visual;old=p.get_actor_transform();c.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean'));c.set_anim_instance_class(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterNPCAnimInstance'));c.set_forced_lod(0);p.set_actor_location(unreal.Vector(-835,-1080,50.15),False,True)
s=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction');route=[(-760,-1410),(-1150,-1920),(-1520,-1830),(-1560,-860),(-1580,-100),(-1560,-860),(-1520,-1830),(-1150,-1920),(-760,-1410),(-835,-1080)];i=0;elapsed=0.;stuck=0.;last=p.get_actor_location();lastlod=None;records=[];switches=[];start=time.monotonic()
def input(x,y):s.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 input(0,0);p.set_actor_transform(old,False,True);unreal.unregister_slate_post_tick_callback(unreal._rv2_lodwalk);del unreal._rv2_lodwalk;(O/'LODWalk.json').write_text(json.dumps({'frames':records,'switches':switches,'error':error,'wall_seconds':time.monotonic()-start,'game_seconds':elapsed,'initial_positioning_only':True,'subsequent_movement':'Enhanced Input, no forced LOD, camera unchanged'},indent=2))
def tick(dt):
 global i,elapsed,stuck,last,lastlod
 try:
  elapsed+=dt;q=p.get_actor_location();step=(q-last).length();last=q;cam=pc.player_camera_manager;lod=c.get_predicted_lod_level();r={'t':elapsed,'player':q.to_tuple(),'camera_npc_m':(cam.get_camera_location()-v.get_actor_location()).length()/100,'lod':lod,'recently_rendered':c.was_recently_rendered(.2),'speed_cm_s':p.get_velocity().length()};records.append(r)
  if lastlod is not None and lod!=lastlod:
   f=O/('Switch_'+str(len(switches)).zfill(2)+'_LOD'+str(lod)+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(f)+'"',pc);switches.append({**r,'requested':str(f)})
  lastlod=lod
  if i>=len(route):finish();return
  dx=route[i][0]-q.x;dy=route[i][1]-q.y;distance=math.hypot(dx,dy)
  if distance<18:input(0,0);i+=1;stuck=0;return
  yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;ang=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;mag=min(1,distance/100);input(math.sin(ang)*mag,math.cos(ang)*mag);stuck=stuck+dt if step<.1 else 0;assert stuck<4,('Blocked',i,q);assert elapsed<80;assert p.get_component_by_class(unreal.CharacterMovementComponent).max_walk_speed==210
 except Exception as e:finish(str(e))
unreal._rv2_lodwalk=unreal.register_slate_post_tick_callback(tick)
