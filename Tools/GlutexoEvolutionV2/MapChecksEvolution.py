"""Read-only checks of every existing map. Never creates or saves a map."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();rows=[]
for p in sorted((R/'Content/Maps').glob('*.umap')):
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
 name='/Game/Maps/'+p.stem;assert unreal.EditorLoadingAndSavingUtils.load_map(name)
 unreal.log('EVOLUTION_V2_MAPCHECK_BEGIN '+name);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'MAP CHECK');unreal.log('EVOLUTION_V2_MAPCHECK_END '+name);rows.append(name)
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(R/'Saved/GlutexoEvolutionV2/MapChecksB.json').write_text(json.dumps(rows,indent=2))
