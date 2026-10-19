
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
j=json.loads((O/'Request.json').read_text());plan=R/'Tools/EnvironmentPerfV3/Plans'/(j['plan']+'.tsv');assert plan.exists();assert not (O/(j['plan']+'_Done.txt')).exists()
assert 'Dev_TestMap_EnvironmentPerfV3' in w.get_name()
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterEnvironmentRenderProfileV3):a.set_rendering_overrides_enabled(False)
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf3.Run "'+str(plan)+'"')
