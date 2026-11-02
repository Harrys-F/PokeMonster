"""Genuine calm QHD views from unchanged Third Person. Diagnostic positioning, no save or world edits."""
import unreal,json,time,math,sys,re,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandIntegrationV1';cfg=json.loads((D/'ActiveNative.json').read_text());O=D/cfg['label'];assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(O);sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0));P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};cases=[]
for label in ['WR_NPC_0','WR_NPC_1','WR_NPC_2']:
 a=actors[label];p=a.get_actor_location();ground=p.z-a.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height();cases.append((label,(p.x+400,p.y+250,ground+50.15),math.degrees(math.atan2(-250,-400))+18))
for label in ['WR_Spielerhaus_Cutaway','WR_Gasthaus_Cutaway','HouseCutaway']:
 a=actors[label];b=a.door_threshold;p=b.get_world_location()+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(-700,0,0),b.get_world_rotation().yaw,unreal.Vector(0,0,1));cases.append((label,(p.x,p.y,b.get_world_location().z-b.get_scaled_box_extent().z+50.15),b.get_world_rotation().yaw))
for label,e,n,te,tn in [('Steinkreis',-60,223,-45,235),('Waldruinen',212,190,225,205)]:
 p=L.world(e,n,L.height(e,n));t=L.world(te,tn);cases.append((label,(p[0],p[1],p[2]+50.15),math.degrees(math.atan2(t[1]-p[1],t[0]-p[0]))))
s={'i':0,'phase':0,'at':0};rows=[];start=time.monotonic()
def finish(error=None):
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'views':rows,'seconds':time.monotonic()-start,'diagnostic_positioning_only':True},indent=2));unreal.unregister_slate_post_tick_callback(unreal._westland_views);unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 try:
  assert time.monotonic()-start<100
  if s['i']==len(cases):finish();return
  label,p,yaw=cases[s['i']]
  if s['phase']==0:
   P.set_actor_location(unreal.Vector(*p),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.get_editor_property('ThirdPersonBoom').set_world_rotation(unreal.Rotator(yaw=yaw),False,False);s.update(phase=1,at=time.monotonic())
  elif s['phase']==1:
   if time.monotonic()-s['at']<2.5:return
   assert P.is_third_person_camera()and abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.02;f=O/(label+'.png');unreal.SystemLibrary.execute_console_command(W,'Shot filename="'+str(f)+'" -nosuffix',PC);rows.append({'label':label,'file':str(f),'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'pitch':PC.player_camera_manager.get_camera_rotation().pitch,'yaw':PC.player_camera_manager.get_camera_rotation().yaw});s.update(phase=2,at=time.monotonic())
  elif s['phase']==2 and time.monotonic()-s['at']>.3:
   assert Path(rows[-1]['file']).is_file();s.update(i=s['i']+1,phase=0)
 except Exception:finish(traceback.format_exc())
unreal._westland_views=unreal.register_slate_post_tick_callback(tick)
