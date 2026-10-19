"""Explicit non-gameplay preview in disposable embedded PIE; actual game camera, no camera overrides."""

# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json,math,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2';D=O/'Data';F=O/'Unreal/FinalMotion';F.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_NPCMotionV2';p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if 'NPCMotionV2_PreviewOnly' in [str(t) for t in a.tags]);src=v.source_actor;oldp=p.get_actor_transform();olds=src.get_actor_transform();oldv=v.get_actor_transform();v.set_editor_property('bUseVisual',True);v.refresh_presentation();c=v.visual;c.set_forced_lod(0)
p.set_actor_location(unreal.Vector(-760,-1410,50.15),False,True);unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion2.Viewport 2560 1440')
stages=[('Idle_Front',2,0,135),('Idle_Side',2,0,45)]
for d in range(8):stages.extend([('Walk_'+str(d),3.6,150,d*45),('Stop_'+str(d),.9,0,d*45)])
stages.extend([('Turn90',2,0,90),('Turn180',2,0,180),('Idle_AfterTurn',2,0,0),('LOD_Away',10,150,-45),('LOD_Back',10,150,135),('ForcedLOD0',1.8,0,135),('ForcedLOD1',1.8,0,135)])
i=-1;t=0.;elapsed=0.;records=[];shots=[];saved=set();lastlod=None;switches=[];origin=unreal.Vector(-900,-1590,3);stagepos=origin;stageyaw=135;created=time.monotonic();last_game_time=unreal.GameplayStatics.get_time_seconds(w)
def finish(error=None):
 v.set_editor_property('bUseVisual',False);v.refresh_presentation();c.set_forced_lod(0);src.set_actor_transform(olds,False,True);v.set_actor_transform(oldv,False,True);p.set_actor_transform(oldp,False,True)
 unreal.unregister_slate_post_tick_callback(unreal._npcmotion2_review);del unreal._npcmotion2_review
 (D/'MotionReview.json').write_text(json.dumps({'error':error,'passed_technical_sequence':error is None,'frames':records,'shots':shots,'automatic_lod_switches':switches,'purpose':'Transform-driven preview only; not AI navigation or a gameplay foot test','camera_unchanged':True,'seconds':elapsed,'wall_seconds':time.monotonic()-created},indent=2))
def shot(name):
 path=F/(name+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(path)+'"',pc);cam=pc.player_camera_manager
 shots.append({'name':name,'path_request':str(path),'viewport':list(pc.get_viewport_size()),'camera':cam.get_camera_location().to_tuple(),'rotation':{'pitch':cam.get_camera_rotation().pitch,'yaw':cam.get_camera_rotation().yaw},'fov':cam.get_fov_angle(),'source_position':src.get_actor_location().to_tuple(),'visual_yaw':v.get_actor_rotation().yaw,'lod':c.get_predicted_lod_level()})
def tick(dt):
 global i,t,elapsed,stagepos,stageyaw,lastlod,last_game_time
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);dt=now-last_game_time;last_game_time=now
  elapsed+=dt;t+=dt
  if i<0 or t>=stages[i][1]:
   i+=1;t=0;saved.clear()
   if i>=len(stages):finish();return
   name,duration,speed,yaw=stages[i]
   if name.startswith('Walk_') or name.startswith('Idle_') and name!='Idle_AfterTurn':src.set_actor_location(origin,False,True);v.set_actor_rotation(unreal.Rotator(yaw=yaw),False)
   if name=='LOD_Away':src.set_actor_location(origin,False,True)
   if name=='ForcedLOD0' or name=='ForcedLOD1':src.set_actor_location(origin,False,True);v.set_actor_rotation(unreal.Rotator(yaw=135),False);c.set_forced_lod(1 if name=='ForcedLOD0' else 2)
   stagepos=src.get_actor_location();stageyaw=v.get_actor_rotation().yaw
  name,duration,speed,yaw=stages[i]
  if speed:
   angle=math.radians(yaw);src.set_actor_location(stagepos+unreal.Vector(math.cos(angle)*speed*t,math.sin(angle)*speed*t,0),False,True)
  elif name.startswith('Turn'):
   v.set_actor_rotation(unreal.Rotator(yaw=stageyaw+yaw*t/duration),False)
  direction=unreal.Vector(math.cos(math.radians(yaw))*speed,math.sin(math.radians(yaw))*speed,0)
  src.set_preview_motion(src.get_actor_location(),direction)
  an=c.get_anim_instance();assert an
  rec={'t':elapsed,'stage':name,'local_t':t,'speed':v.presentation_speed,'walk_alpha':an.walk_alpha,'rate':an.walk_play_rate,'turn_alpha':an.turn_alpha,'cape_pitch':an.cape_pitch,'cape_swing':an.cape_swing,'bag_swing':an.bag_swing,'yaw':v.get_actor_rotation().yaw,'position':src.get_actor_location().to_tuple(),'lod':c.get_predicted_lod_level(),'rendered':c.was_recently_rendered(.2),'feet':{b:c.get_socket_location(b).to_tuple() for b in ['foot_l','foot_r']}}
  assert all(math.isfinite(rec[n]) for n in ['speed','rate','cape_pitch','cape_swing','bag_swing']);records.append(rec)
  if lastlod is not None and rec['lod']!=lastlod and name.startswith('LOD_'):switches.append({'t':elapsed,'stage':name,'lod':rec['lod'],'rendered':rec['rendered'],'camera_distance_m':(pc.player_camera_manager.get_camera_location()-v.get_actor_location()).length()/100});shot('AutoLOD_'+str(len(switches))+'_LOD'+str(rec['lod']))
  lastlod=rec['lod']
  times=[1.2,1.65] if name.startswith('Walk_') else [.7] if name.startswith('Stop_') else [1.3]
  for j,at in enumerate(times):
   if t>at and j not in saved:
    if not name.startswith('LOD_'):shot(name+'_'+str(j))
    saved.add(j)
 except Exception:finish(traceback.format_exc())
assert not hasattr(unreal,'_npcmotion2_review');unreal._npcmotion2_review=unreal.register_slate_post_tick_callback(tick)
