"""Genuine editor region overview, separate from unchanged Third Person test views."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';label=json.loads((D/'PhotoRequest.json').read_text())['label'];O=D/label;E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();old=E.get_level_viewport_camera_info();start=time.monotonic();s={'shot':False};f=O/'Gesamtansicht.png'
E.set_level_viewport_camera_info(unreal.Vector(-30405,30405,50000),unreal.Rotator(pitch=-45,yaw=-45))
def tick(dt):
 try:
  if time.monotonic()-start>4 and not s['shot']:
   unreal.SystemLibrary.execute_console_command(W,'HighResShot 2560x1440 filename="'+str(f)+'"');s['shot']=True
  if s['shot']and time.monotonic()-start>6:
   assert f.is_file();E.set_level_viewport_camera_info(*old);(O/'Overview.json').write_text(json.dumps(dict(passed=True,file=str(f),editor_overview=True)));unreal.unregister_slate_post_tick_callback(unreal._wvuoverview)
 except Exception:
  E.set_level_viewport_camera_info(*old);(O/'Overview.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc())));unreal.unregister_slate_post_tick_callback(unreal._wvuoverview)
unreal._wvuoverview=unreal.register_slate_post_tick_callback(tick)
