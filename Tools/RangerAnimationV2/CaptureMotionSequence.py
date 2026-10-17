import unreal,json,math,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2';F=O/'Unreal/FinalSequence';F.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if 'NPCMotionV2_PreviewOnly' in [str(t) for t in a.tags]);src=v.source_actor;oldp=p.get_actor_transform();olds=src.get_actor_transform();oldv=v.get_actor_transform();v.set_editor_property('bUseVisual',True);v.refresh_presentation();v.visual.set_forced_lod(0)
p.set_actor_location(unreal.Vector(-760,-1410,50.15),False,True);src.set_actor_location(unreal.Vector(-900,-1590,3),False,True);v.set_actor_rotation(unreal.Rotator(yaw=135),False);unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion2.Viewport 2560 1440')
start=unreal.GameplayStatics.get_time_seconds(w);last=start;elapsed=0.;lastshot=-1.;records=[];origin=src.get_actor_location();back=origin+unreal.Vector(-1,1,0)*150*4.5/math.sqrt(2)
def finish(err=None):
 unreal.unregister_slate_post_tick_callback(unreal._npcmotion2_sequence);del unreal._npcmotion2_sequence;v.set_editor_property('bUseVisual',False);v.refresh_presentation();v.visual.set_forced_lod(0);src.set_actor_transform(olds,False,True);v.set_actor_transform(oldv,False,True);p.set_actor_transform(oldp,False,True)
 (O/'Data/Sequence.json').write_text(json.dumps({'error':err,'frames':records,'source':'Actual embedded PIE screenshots, no camera-parameter changes','capture_rate_target_hz':4,'timing':'Game-time timestamps retained; screenshot stalls excluded from performance measurements'},indent=2))
def tick(dt):
 global elapsed,last,lastshot
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);dt=now-last;last=now;elapsed=now-start
  if elapsed>15:finish();return
  if 2<elapsed<6.5:src.set_actor_location(origin+unreal.Vector(-1,1,0)*150*(elapsed-2)/math.sqrt(2),False,True);stage='WalkTowardCamera'
  elif 8<elapsed<9:v.set_actor_rotation(unreal.Rotator(yaw=135+180*(elapsed-8)),False);stage='Turn180'
  elif 9<elapsed<13.5:src.set_actor_location(back+unreal.Vector(1,-1,0)*150*(elapsed-9)/math.sqrt(2),False,True);stage='WalkAway'
  else:stage='IdleOrStop'
  velocity=unreal.Vector(-1,1,0)*150/math.sqrt(2) if stage=='WalkTowardCamera' else unreal.Vector(1,-1,0)*150/math.sqrt(2) if stage=='WalkAway' else unreal.Vector()
  src.set_preview_motion(src.get_actor_location(),velocity)
  if elapsed-lastshot>.25:
   path=F/('Frame_'+str(len(records)).zfill(3)+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(path)+'"',pc);cam=pc.player_camera_manager;an=v.visual.get_anim_instance()
   records.append({'index':len(records),'time':elapsed,'stage':stage,'path_request':str(path),'position':src.get_actor_location().to_tuple(),'camera':cam.get_camera_location().to_tuple(),'pitch':cam.get_camera_rotation().pitch,'yaw':cam.get_camera_rotation().yaw,'fov':cam.get_fov_angle(),'viewport':list(pc.get_viewport_size()),'walk_alpha':an.walk_alpha,'walk_rate':an.walk_play_rate,'cape_pitch':an.cape_pitch,'bag_swing':an.bag_swing,'lod':v.visual.get_predicted_lod_level()});lastshot=elapsed
 except Exception:finish(traceback.format_exc())
unreal._npcmotion2_sequence=unreal.register_slate_post_tick_callback(tick)
