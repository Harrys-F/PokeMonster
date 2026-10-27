"""Read-only checks of every existing map; no new worlds saved."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();original=E.get_editor_world().get_path_name().split('.')[0];rows=[]
for p in sorted((R/'Content/Maps').glob('*.umap')):
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
 name='/Game/Maps/'+p.stem;assert unreal.EditorLoadingAndSavingUtils.load_map(name);unreal.log('GRAPHICS_C_MAPCHECK_BEGIN '+name);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'MAP CHECK');unreal.log('GRAPHICS_C_MAPCHECK_END '+name);rows.append(name)
assert unreal.EditorLoadingAndSavingUtils.load_map(original)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(R/'Saved/ProjectRefinement/GraphicsVariantC/MapChecksFinal.json').write_text(json.dumps(rows,indent=2))
