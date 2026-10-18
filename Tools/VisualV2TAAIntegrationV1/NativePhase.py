import unreal,time,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();start=time.monotonic()
def tick(dt):
 if time.monotonic()-start<20:return
 if not any(w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0) for w in unreal.ObjectIterator(unreal.World)):return
 unreal.unregister_slate_post_tick_callback(unreal._taa_native);runpy.run_path(str(R/'Tools/VisualV2TAAIntegrationV1/BeginPhase.py'),run_name='__main__')
unreal._taa_native=unreal.register_slate_post_tick_callback(tick)
