"""Map Check all already-existing maps without modifying or saving a package."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/StarterExpansionV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
def clean():return not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not E.get_game_world() and clean();rows=[]
for p in sorted((R/'Content/Maps').glob('*.umap')):
 path='/Game/Maps/'+p.stem;assert unreal.EditorLoadingAndSavingUtils.load_map(path)
 unreal.log('STARTER_EXPANSION_FINAL_MAPCHECK_BEGIN '+path)
 unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'MAP CHECK')
 unreal.log('STARTER_EXPANSION_FINAL_MAPCHECK_END '+path);assert clean();rows.append({'map':path})
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2') and clean()
(O/'MapChecksRequested.json').write_text(json.dumps(rows,indent=2));unreal.log('STARTER_EXPANSION_FINAL_MAPCHECKS_REQUESTED')
