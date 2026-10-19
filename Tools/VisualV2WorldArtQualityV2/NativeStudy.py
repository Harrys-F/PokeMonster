import unreal,time,runpy,json,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();started=time.monotonic()
def tick(dt):
 if time.monotonic()-started<20:return
 if not any(w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0) for w in unreal.ObjectIterator(unreal.World)):return
 unreal.unregister_slate_post_tick_callback(unreal._waq2_native);request=json.loads((R/'Saved/VisualV2WorldArtQualityV2/StudyRequest.json').read_text())
 try:
  name='RuntimeMatrix.py' if request.get('kind')=='matrix' else 'RuntimeStudy.py';runpy.run_path(str(R/'Tools/VisualV2WorldArtQualityV2'/name),run_name='__main__')
 except Exception:
  (R/'Saved/VisualV2WorldArtQualityV2'/(request['label']+'_Error.txt')).write_text(traceback.format_exc());unreal.log_error(traceback.format_exc())
  w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));unreal.SystemLibrary.execute_console_command(w,'quit')
unreal._waq2_native=unreal.register_slate_post_tick_callback(tick)
