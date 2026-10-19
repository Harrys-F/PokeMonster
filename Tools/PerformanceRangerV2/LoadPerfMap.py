
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_RangerPerfV2')
