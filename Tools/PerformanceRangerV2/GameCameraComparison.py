"""Disposable PIE review. Camera settings unchanged. Teleport positioning only for matched review shots, never claimed as a foot test."""
import unreal,json,time,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/V2/UnrealAccepted';O.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));c=v.visual;old=(p.get_actor_transform(),v.get_actor_transform(),c.get_skeletal_mesh_asset(),c.get_animation_mode(),c.get_anim_instance().get_class(),c.get_forced_lod(),c.get_editor_property('pause_anims'));records=[];rows=[]
for site,pos in [('Dialog',(-835,-1080,50.15)),('Typical',(-760,-1410,50.15)),('Forest',(-746.5,-718,50.15))]:
 for view,yaw in [('Front',135),('Side',45),('ThreeQuarter',90),('Back',315)]:
  for variant,lod in [('V1',0),('V2',1),('V2LOD1',2)]:rows.append((site,pos,view,yaw,variant,lod))
i=0;start=0;active=False;shot_sent=False
before={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.VSync','t.MaxFPS','r.ScreenPercentage']}
for n,val in [('r.VSync',0),('t.MaxFPS',0),('r.ScreenPercentage',75)]:unreal.SystemLibrary.execute_console_command(w,n+' '+str(val))
def finish(error=None):
 c.set_skeletal_mesh_asset(old[2]);c.set_animation_mode(old[3]);c.set_anim_instance_class(old[4]);c.set_forced_lod(old[5]);c.set_editor_property('pause_anims',old[6]);v.set_actor_transform(old[1],False,True);p.set_actor_transform(old[0],False,True)
 for n,x in before.items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(x))
 unreal.unregister_slate_post_tick_callback(unreal._rv2_review);del unreal._rv2_review;(O/'Comparison.json').write_text(json.dumps({'records':records,'error':error,'camera_unchanged':True,'pose':'Idle single-node, 0.25 seconds, playback stopped; same phase for each pair'},indent=2))
def tick(dt):
 global i,start,active,shot_sent
 try:
  if i>=len(rows):finish();return
  site,pos,view,yaw,variant,lod=rows[i]
  if not active:
   p.set_actor_location(unreal.Vector(*pos),False,True);v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=yaw,roll=0),True);c.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1' if variant=='V1' else '/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean'));c.set_forced_lod(lod);c.set_editor_property('pause_anims',False);c.play_animation(v.idle_animation,False);c.set_position(.25,False);c.set_play_rate(0);start=time.monotonic();active=True;shot_sent=False;return
  warm=4. if i%12==0 else 1.5
  if time.monotonic()-start<warm:return
  if shot_sent:
   if time.monotonic()-start>=warm+.6:i+=1;active=False
   return
  path=O/(site+'_'+view+'_'+variant+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(path)+'"',pc);cam=pc.player_camera_manager;records.append({'requested':str(path),'site':site,'view':view,'variant':variant,'forced_lod':lod,'predicted_lod':c.get_predicted_lod_level(),'camera_cm':cam.get_camera_location().to_tuple(),'camera_rotation':cam.get_camera_rotation().to_tuple(),'fov':cam.get_fov_angle(),'camera_npc_distance_m':(cam.get_camera_location()-v.get_actor_location()).length()/100,'player_npc_distance_m':(p.get_actor_location()-v.get_actor_location()).length()/100,'viewport':list(pc.get_viewport_size())});shot_sent=True
 except Exception as e:finish(str(e))
unreal._rv2_review=unreal.register_slate_post_tick_callback(tick)
