import unreal,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_EnvironmentPerfV1'
d={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional']};assert all(v==2 for v in d.values()),d
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf.Viewport 2560 1440')
assert tuple(unreal.GameplayStatics.get_player_controller(w,0).get_viewport_size())==(2560,1440)
(O/'FootProfileActive.json').write_text(json.dumps(d,indent=2));runpy.run_path(str(R/'Tools/EnvironmentPerfV1/FootTest.py'),run_name='__main__')
