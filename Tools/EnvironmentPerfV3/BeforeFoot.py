
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV3'
names=['sg.ViewDistanceQuality','sg.AntiAliasingQuality','sg.ShadowQuality','sg.GlobalIlluminationQuality','sg.ReflectionQuality','sg.PostProcessQuality','sg.TextureQuality','sg.EffectsQuality','sg.FoliageQuality','sg.ShadingQuality','r.ScreenPercentage','r.VSync','t.MaxFPS']
profile=['r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing']
d={'quality_before':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names},'profile_before':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in profile}}
assert not (O/'FootSessionBefore.json').exists();(O/'FootSessionBefore.json').write_text(json.dumps(d,indent=2))
for n in names:unreal.SystemLibrary.execute_console_command(w,n+' '+str(2 if n.startswith('sg.') else 75 if n=='r.ScreenPercentage' else 0))
d['profile_scope_before']={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in profile};(O/'FootSessionBefore.json').write_text(json.dumps(d,indent=2))
