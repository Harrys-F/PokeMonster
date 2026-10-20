"""Camera-matched screenshot diagnostic only; runtime positions restored, no map writes."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/GlumandaV11/SightAccepted';O.mkdir(exist_ok=False);w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);v=p.get_component_by_class(unreal.PokeMonsterCameraVisibilityComponent);mpc=unreal.load_asset('/Game/Environment/DevTestMapVisualV2/Materials/MPC_PlayerSight');old=p.get_actor_location();rot=p.get_actor_rotation();scale=v.reveal_radius_scale;settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
p.set_actor_location(unreal.Vector(-1910,530,old.z),False,True);v.reveal_radius_scale=1.;unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 100');s={'phase':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'rows':[]}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._glumanda_sight_review);v.reveal_radius_scale=scale;p.set_actor_location(old,False,True);p.set_actor_rotation(rot,True);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);s.update(passed=error is None,error=error,diagnostic_teleport_not_footrun=True);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now
  if s['phase']<2 and s['t']>4:
   name='A_Original'if s['phase']==0 else'B_DoubleDiameter';r=unreal.MaterialLibrary.get_vector_parameter_value(w,mpc,'PlayerSightShape');assert list(pc.get_viewport_size())==[2560,1440];assert abs(r.r-(55 if s['phase']==0 else 110))<.01;assert abs(r.g-(110 if s['phase']==0 else 220))<.01
   unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(O/(name+'.png'))+'"',pc);s['rows'].append({'name':name,'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'rotation':pc.player_camera_manager.get_camera_rotation().to_tuple(),'radius_cm':[r.r,r.g],'viewport':list(pc.get_viewport_size())});s['phase']+=1;s['t']=0
  elif s['phase']==1 and s['t']>.5:v.reveal_radius_scale=2.
  elif s['phase']==2 and s['t']>.5:
   assert math.dist(s['rows'][0]['camera'],s['rows'][1]['camera'])<.001;finish()
 except Exception as e:finish(str(e));unreal.log_error(str(e))
unreal._glumanda_sight_review=unreal.register_slate_post_tick_callback(tick)
