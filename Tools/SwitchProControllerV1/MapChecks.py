"""Read-only Map Checks for every existing map; never creates or saves a map."""
import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();rows=[]
for p in sorted((r/'Content/Maps').glob('*.umap')):
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
 name='/Game/Maps/'+p.stem;assert unreal.EditorLoadingAndSavingUtils.load_map(name)
 unreal.log('SWITCH_PRO_MAPCHECK_BEGIN '+name);unreal.SystemLibrary.execute_console_command(e.get_editor_world(),'MAP CHECK');unreal.log('SWITCH_PRO_MAPCHECK_END '+name);rows.append(name)
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(r/'Saved/ProjectRefinement/SwitchProMapChecksRequested.json').write_text(json.dumps(rows,indent=2))
