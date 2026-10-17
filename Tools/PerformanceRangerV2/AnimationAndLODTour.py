"""Actual Enhanced-Input motion, fixed game camera. Capture a chronological image sequence; no free-camera substitute."""
import unreal,json,time,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/V2/Motion';O.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));c=v.visual;old=(p.get_actor_transform(),c.get_forced_lod());sub=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction');c.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean'));c.set_forced_lod(0);p.set_actor_location(unreal.Vector(-835,-1080,50.15),False,True);start=time.monotonic();nextshot=2.;rows=[];frames=[];lods=[]
def inject(x,y):sub.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 inject(0,0);c.set_forced_lod(old[1]);p.set_actor_transform(old[0],False,True);unreal.unregister_slate_post_tick_callback(unreal._rv2_lodtour);del unreal._rv2_lodtour;(O/'Motion.json').write_text(json.dumps({'frames':frames,'screenshots':rows,'error':error,'note':'Initial deterministic review positioning; subsequent movement exclusively Enhanced Input. No NPC/source actor movement or camera changes.'},indent=2))
def tick(dt):
 global nextshot
 try:
  t=time.monotonic()-start
  if t>24:finish();return
  # Away/toward camera axis on open village path, then diagonal reversal. Keep interaction source untouched.
  if t<2:inject(0,0)
  elif t<7:inject(0,-1)
  elif t<17:inject(0,1)
  elif t<22:inject(0,-1)
  else:inject(0,0)
  pos=p.get_actor_location();cam=pc.player_camera_manager;frames.append({'seconds':t,'player':pos.to_tuple(),'camera_npc_m':(cam.get_camera_location()-v.get_actor_location()).length()/100,'lod':c.get_predicted_lod_level(),'speed_cm_s':p.get_velocity().length(),'rendered':c.was_recently_rendered(.2)})
  if t>=nextshot:
   f=O/('LODWalk_'+str(len(rows)).zfill(2)+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(f)+'"',pc);rows.append({'seconds':t,'requested':str(f),'lod':c.get_predicted_lod_level()});nextshot+=.5
 except Exception as e:finish(str(e))
unreal._rv2_lodtour=unreal.register_slate_post_tick_callback(tick)
