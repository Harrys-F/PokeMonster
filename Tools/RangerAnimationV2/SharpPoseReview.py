"""Paused animation samples in actual game camera; no graphics-quality modification."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2';F=O/'Unreal/SharpPoses';F.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if a.source_actor.get_class().get_name()=='PokeMonsterNPC');c=v.visual;p.set_actor_location(unreal.Vector(-835,-1080,50.15),False,True);unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion2.Viewport 2560 1440')
rows=[(view,yaw,phase,lod) for view,yaw in [('FrontQuarter',90),('BackQuarter',270)] for phase in [0.,.225,.45,.675] for lod in [1,2]];i=-1;started=0.;sent=False;records=[]
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._npcmotion2_sharp);del unreal._npcmotion2_sharp;(O/'Data/SharpPoses.json').write_text(json.dumps({'error':error,'records':records,'purpose':'Actual UE single-node Walk samples, paused after 2s settling. Not movement footage. No motion-blur or camera settings changed.'},indent=2))
def tick(dt):
 global i,started,sent
 try:
  if i<0 or sent and time.monotonic()-started>2.5:
   i+=1
   if i>=len(rows):finish();return
   view,yaw,phase,lod=rows[i];v.set_actor_rotation(unreal.Rotator(yaw=yaw),False);c.set_forced_lod(lod);c.set_editor_property('pause_anims',False);c.play_animation(v.walk_animation,False);c.set_position(phase,False);c.set_play_rate(0);started=time.monotonic();sent=False;return
  if time.monotonic()-started>2 and not sent:
   view,yaw,phase,lod=rows[i];path=F/(view+'_'+str(phase).replace('.','p')+'_LOD'+str(lod-1)+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(path)+'"',pc);cam=pc.player_camera_manager;records.append({'requested':str(path),'view':view,'phase_seconds':phase,'lod':c.get_predicted_lod_level(),'source_position':v.get_actor_location().to_tuple(),'camera':cam.get_camera_location().to_tuple(),'pitch':cam.get_camera_rotation().pitch,'yaw':cam.get_camera_rotation().yaw,'fov':cam.get_fov_angle()});sent=True
 except Exception:finish(traceback.format_exc())
unreal._npcmotion2_sharp=unreal.register_slate_post_tick_callback(tick)
