import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();pc=unreal.GameplayStatics.get_player_controller(w,0)
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
cmd('pm.StarterReview.Party Schiggy Bisasam Zunderlauf');cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100')
s={'time':time.monotonic()}
def tick(dt):
 if time.monotonic()-s['time']<5:return
 unreal.unregister_slate_post_tick_callback(unreal._polish_qhd);(R/'Saved/StarterPolishV2/QHDViewport.json').write_text(json.dumps({'viewport':pc.get_viewport_size(),'screen_percentage':unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage'),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'rotation':str(pc.player_camera_manager.get_camera_rotation()),'fov':pc.player_camera_manager.get_fov_angle()},indent=2));cmd('Shot filename='+str(R/'Saved/StarterPolishV2/QHDCheck.png'));cmd('pm.TAAReview.CaptureStart '+str(R/'Saved/VisualV2TAAIntegrationV1/Recordings/StarterPolishQHD01'))
unreal._polish_qhd=unreal.register_slate_post_tick_callback(tick)
