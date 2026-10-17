"""Actual embedded-PIE framebuffer recording and timestamped animation telemetry.
Explicit preview source is not a gameplay NPC or navigation test.
"""
import unreal,json,math,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3';F=O/'Unreal/Recording'
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_NPCMotionV3'
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor)
main=next(x for x in actors if x.source_actor.get_class().get_name()=='PokeMonsterNPC')
v=next(x for x in actors if 'NPCMotionV3_PreviewOnly' in [str(t) for t in x.tags]);src=v.source_actor
p.set_actor_location(unreal.Vector(-835,-1080,50.15),False,True)
main.visual.set_visibility(False);v.set_editor_property('bUseVisual',True);v.refresh_presentation();src.set_preview_motion(unreal.Vector(-940,-1390,3),unreal.Vector());v.set_actor_rotation(unreal.Rotator(yaw=135),False)
unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion3.Viewport 1280 740')
gi=unreal.GameplayStatics.get_game_instance(w);dialog=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem) if x.get_outer()==gi)
stages=[('Warmup',3,0,135),('Idle_10s',10,0,135)]
for i,yaw in enumerate([0,90,180,270,0,180]):stages.append(('NormalWalk_'+str(i),2.5,150,yaw))
for d in [0,4,1,5,2,6,3,7]:stages.extend([('Direction_'+str(d*45),2.,150,d*45),('AbruptStop_'+str(d*45),.65,0,d*45)])
stages.extend([('Turn90',3,0,90),('Turn180',3,0,180),('IdleAfterTurn',2,0,0),('Talk',8,0,0),('ReturnIdle',3,0,0)])
i=-1;local_t=0.;elapsed=0.;last=unreal.GameplayStatics.get_time_seconds(w);records=[];stagepos=src.get_actor_location();stageyaw=135;started=False;talk_started=False;wall=time.monotonic();stages_done=[]
def finish(error=None):
 unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion3.CaptureStop')
 unreal.unregister_slate_post_tick_callback(unreal._r3_record);del unreal._r3_record
 if dialog.is_dialogue_active():dialog.close_dialogue()
 (O/'Data/RecordedMotion.json').write_text(json.dumps({'error':error,'frames':records,'stages':stages_done,'game_seconds':elapsed,'wall_seconds':time.monotonic()-wall,'source':'Real Unreal viewport framebuffer via native ReadPixels and asynchronous PNG writing, target <=20Hz. Not synthetic or Blender renders. Capture overhead is excluded from performance benchmarks.','preview_is_not_gameplay_navigation':True,'macOS_screen_capture_permission':False},indent=2))
def tick(dt):
 global i,local_t,elapsed,last,stagepos,stageyaw,started,talk_started
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-last;last=now;local_t+=delta;elapsed+=delta
  if i<0 or local_t>=stages[i][1]:
   if i>=0:stages_done.append({'name':stages[i][0],'actual_seconds':local_t,'end_t':elapsed})
   i+=1;local_t=0.
   if i>=len(stages):finish();return
   stagepos=src.get_actor_location();stageyaw=v.get_actor_rotation().yaw
   if i==1:
    unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion3.CaptureStart "'+str(F)+'"');started=True
  name,duration,speed,yaw=stages[i]
  velocity=unreal.Vector(math.cos(math.radians(yaw))*speed,math.sin(math.radians(yaw))*speed,0)
  src.set_preview_motion(stagepos+velocity*local_t,velocity)
  if name.startswith('Turn'):v.set_actor_rotation(unreal.Rotator(yaw=stageyaw+yaw*local_t/duration),False)
  if name=='Talk':
   v.set_editor_property('bUseVisual',False);v.refresh_presentation();main.visual.set_visibility(True)
   if local_t>1 and not talk_started:assert p.try_interact() and dialog.is_dialogue_active();talk_started=True
  if name=='ReturnIdle' and dialog.is_dialogue_active():dialog.advance_dialogue()
  an=(main if name in ['Talk','ReturnIdle'] else v).visual.get_anim_instance()
  cm=pc.player_camera_manager
  records.append({'t':elapsed,'local_t':local_t,'stage':name,'speed':v.presentation_speed,'walk_alpha':an.walk_alpha,'rate':an.walk_play_rate,'turn_alpha':an.turn_alpha,'conversation_alpha':an.conversation_alpha,'plant_correction_cm':an.plant_correction_cm,'cape_pitch':an.cape_pitch,'bag_swing':an.bag_swing,'position':src.get_actor_location().to_tuple(),'yaw':v.get_actor_rotation().yaw,'camera':cm.get_camera_location().to_tuple(),'pitch':cm.get_camera_rotation().pitch,'camera_yaw':cm.get_camera_rotation().yaw,'fov':cm.get_fov_angle(),'feet':{b:v.visual.get_socket_location(b).to_tuple() for b in ['foot_l','foot_r']},'viewport':pc.get_viewport_size()})
 except Exception:finish(traceback.format_exc())
assert not hasattr(unreal,'_r3_record');unreal._r3_record=unreal.register_slate_post_tick_callback(tick)
