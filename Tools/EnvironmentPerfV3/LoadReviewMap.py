
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
target=json.loads((O/'LoadReviewRequest.json').read_text())['map'];assert target in ['/Game/Maps/Dev_TestMap_VisualV2','/Game/Maps/Dev_TestMap_EnvironmentPerfV1','/Game/Maps/Dev_TestMap_EnvironmentPerfV2','/Game/Maps/Dev_TestMap_EnvironmentPerfV3']
assert unreal.EditorLoadingAndSavingUtils.load_map(target)
