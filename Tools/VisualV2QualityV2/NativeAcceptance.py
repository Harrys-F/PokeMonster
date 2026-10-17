"""Opt-in native Development acceptance. Starts after the real game player exists."""
import unreal,json,time,runpy,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2QualityV2';j=json.loads((O/'AcceptanceRequest.json').read_text());dest=O/'Acceptance'/j['label'];started=False;completed=None;begin=time.monotonic()
def tick(dt):
 global started,completed
 try:
  if not started:
   worlds=[w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:
    assert time.monotonic()-begin<120,'Player initialization timeout';return
   if time.monotonic()-begin<10:return
   started=True;runpy.run_path(str(R/'Tools/VisualV2QualityV2/StartAcceptance.py'),run_name='__main__')
  if (dest/'FootTest.json').exists():
   if completed is None:completed=time.monotonic()
   if time.monotonic()-completed>5:
    unreal.unregister_slate_post_tick_callback(unreal._veq2_native);del unreal._veq2_native
    w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));unreal.SystemLibrary.execute_console_command(w,'quit')
 except Exception:
  (dest/'NativeFailure.txt').write_text(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._veq2_native);del unreal._veq2_native
unreal._veq2_native=unreal.register_slate_post_tick_callback(tick)
