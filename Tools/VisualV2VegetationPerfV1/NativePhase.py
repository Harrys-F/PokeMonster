import unreal,time,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();start=time.monotonic()
def tick(dt):
 if time.monotonic()-start<20:return
 if not any(w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1' and unreal.GameplayStatics.get_player_pawn(w,0) for w in unreal.ObjectIterator(unreal.World)):return

 for path in ["/Game/Environment/VegetationPerfV1/Materials/M_VVP1_CrownFullyRough","/Game/Environment/VegetationPerfV1/Materials/M_VVP1_FoliageFullyRough"]:assert unreal.load_asset(path)
 if hasattr(unreal,"AssetCompilingManager"):unreal.AssetCompilingManager.finish_all_compilation()
 unreal.unregister_slate_post_tick_callback(unreal._veg_native);runpy.run_path(str(R/'Tools/VisualV2VegetationPerfV1/BeginPhase.py'),run_name='__main__')
unreal._veg_native=unreal.register_slate_post_tick_callback(tick)
