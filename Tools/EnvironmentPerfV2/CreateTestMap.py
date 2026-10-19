
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
source='/Game/Maps/Dev_TestMap_EnvironmentPerfV1';target='/Game/Maps/Dev_TestMap_EnvironmentPerfV2'
assert not unreal.EditorAssetLibrary.does_asset_exist(target),'Never overwrite an existing test map'
assert unreal.EditorLoadingAndSavingUtils.load_map(source);w=e.get_editor_world();assert w.get_path_name()==source+'.Dev_TestMap_EnvironmentPerfV1'
assert unreal.EditorLoadingAndSavingUtils.save_map(w,target)
assert unreal.EditorLoadingAndSavingUtils.load_map(target);w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV2'
(O/'MapCopy.json').write_text(json.dumps({'source':source,'target':w.get_path_name(),'original_saved':False,'method':'EditorLoadingAndSavingUtils.save_map followed by explicit load_map'},indent=2))
