"""Separate unattended commandlet only: export saved map to ignored diagnostic text."""
import unreal
from pathlib import Path
assert '-run=pythonscript'in unreal.SystemLibrary.get_command_line().lower()
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
R=Path(unreal.Paths.project_dir()).resolve();assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');w=E.get_editor_world();target=R/'Saved/WildEncountersV2/DiskBefore.t3d';assert not target.exists();t=unreal.AssetExportTask();t.object=w;t.filename=str(target);t.exporter=unreal.LevelExporterT3D();t.automated=True;t.selected=False;t.prompt=False;t.replace_identical=False;assert unreal.Exporter.run_asset_export_task(t),t.errors;assert target.exists();unreal.log('DISK_MAP_READ_ONLY_EXPORT '+str(target))
