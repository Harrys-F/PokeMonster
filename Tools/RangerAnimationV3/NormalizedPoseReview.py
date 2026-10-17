import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3';F=O/'Unreal/NormalizedPose';F.mkdir(exist_ok=True)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_NPCMotionV3'
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if a.source_actor.get_class().get_name()=='PokeMonsterNPC')
p.set_actor_location(unreal.Vector(-835,-1080,50.15),False,True);unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion3.Viewport 2560 1440')
v.set_actor_rotation(unreal.Rotator(yaw=90),False);c=v.visual;c.set_forced_lod(1);c.play_animation(v.walk_animation,False);c.set_position(.2,False);c.set_play_rate(0)
start=time.monotonic();sent=False
def tick(dt):
 global sent
 if not sent and time.monotonic()-start>2:
  path=F/'FrontQuarter_QuarterCycle.png';unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(path)+'"',pc);cam=pc.player_camera_manager
  (O/'Data/NormalizedPose.json').write_text(json.dumps({'requested':str(path),'phase_seconds':.2,'normalized_phase':.25,'v2_matching_seconds':.225,'source_position':v.get_actor_location().to_tuple(),'camera':cam.get_camera_location().to_tuple(),'pitch':cam.get_camera_rotation().pitch,'yaw':cam.get_camera_rotation().yaw,'fov':cam.get_fov_angle(),'lod':c.get_predicted_lod_level(),'actor_yaw':v.get_actor_rotation().yaw},indent=2));sent=True
 if sent and time.monotonic()-start>4:
  unreal.unregister_slate_post_tick_callback(unreal._r3_normalized);del unreal._r3_normalized
unreal._r3_normalized=unreal.register_slate_post_tick_callback(tick)
