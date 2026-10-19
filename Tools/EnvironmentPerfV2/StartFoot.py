
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_EnvironmentPerfV2'
d={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing']};assert list(d.values())==[2.0,2.0,0.0,0.0],d
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440')
assert tuple(unreal.GameplayStatics.get_player_controller(w,0).get_viewport_size())==(2560,1440)
(O/'FootProfileActive.json').write_text(json.dumps(d,indent=2));runpy.run_path(str(R/'Tools/EnvironmentPerfV2/FootTest.py'),run_name='__main__')
