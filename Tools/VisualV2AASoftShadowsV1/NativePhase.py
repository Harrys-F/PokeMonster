import unreal,json,time,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2AASoftShadowsV1';started=False;begin=time.monotonic()
def tick(dt):
 global started
 if started or time.monotonic()-begin<20:return
 worlds=[w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1' and unreal.GameplayStatics.get_player_pawn(w,0)]
 if not worlds:return
 started=True;unreal.unregister_slate_post_tick_callback(unreal._vmf_native);j=json.loads((O/'Request.json').read_text());runpy.run_path(str(R/('Tools/VisualV2AASoftShadowsV1/BeginCost.py' if j.get('cost') else 'Tools/VisualV2AASoftShadowsV1/BeginPhase.py')),run_name='__main__')
unreal._vmf_native=unreal.register_slate_post_tick_callback(tick)
