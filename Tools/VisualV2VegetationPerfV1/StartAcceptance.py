import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2VegetationPerfV1';request=json.loads((S/'AcceptanceRequest.json').read_text());w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1' and unreal.GameplayStatics.get_player_pawn(w,0))
for cmd in [f"pm.EnvPerf2.Viewport {request['width']} {request['height']}",f"r.ScreenPercentage {request['percentage']}",'r.AntiAliasingMethod 2','r.VSync 0','t.MaxFPS 0','r.DynamicRes.OperationMode 0']:unreal.SystemLibrary.execute_console_command(w,cmd)
source=(R/'Tools/VisualV2QualityV2/FootTest.py').read_text().replace('Saved/VisualV2QualityV2','Saved/VisualV2VegetationPerfV1').replace("'Dev_TestMap_VisualV2'","'Dev_TestMap_VisualV2GPUBottleneckV1'")
exec(compile(source,'existing_unchanged_gameplay_route_on_existing_GPU_map','exec'),globals())
