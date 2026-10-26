"""Additional real Unreal sky diagnostic: temporary upward camera, NOT normal gameplay.
No camera asset/map writes; original camera transform/FOV restored immediately afterward.
"""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV1';O=D/'Sky05';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);Camera=P.get_component_by_class(unreal.CameraComponent);Original=Camera.get_relative_transform();Boom=P.get_component_by_class(unreal.SpringArmComponent);OriginalBoom=Boom.get_relative_transform();FOV=Camera.field_of_view;OriginalLock=P.is_overworld_input_locked();P.set_overworld_input_locked(True)
Boom.set_relative_rotation(unreal.Rotator(pitch=-50,yaw=80,roll=0),False,True);Camera.set_relative_rotation(unreal.Rotator(pitch=105,yaw=0,roll=0),False,True);Camera.set_field_of_view(100)
s={'i':0,'stage':'time','last':0};result={'diagnostic_camera_only':True,'camera_temporarily_changed':True,'captures':[]};times=[('Day',12,0),('Dawn',6,0),('Dusk',19,0),('Night',22,0)]
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._daynight_sky);Camera.set_relative_transform(Original,False,True);Camera.set_field_of_view(FOV);Boom.set_relative_transform(OriginalBoom,False,True);P.set_overworld_input_locked(OriginalLock);result.update(passed=error is None,error=error,camera_restored=True);(O/'Result.json').write_text(json.dumps(result,indent=2))
 for n in ['W','PC','P','Camera','Boom']:globals().pop(n,None)
def tick(dt):
 try:
  if s['i']==len(times):finish();return
  n,h,m=times[s['i']]
  if s['stage']=='time':cmd('pm.WorldClock set 1 '+str(h)+' '+str(m));s.update(stage='capture',last=time.monotonic());return
  if time.monotonic()-s['last']<3:return
  cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"');result['captures'].append({'name':n,'camera_rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle()});s.update(i=s['i']+1,stage='time')
 except Exception:finish(traceback.format_exc())
unreal._daynight_sky=unreal.register_slate_post_tick_callback(tick)
