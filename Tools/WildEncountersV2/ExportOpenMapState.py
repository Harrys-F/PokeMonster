"""Export the currently open map to ignored diagnostic text. Never loads or saves any map."""
import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2';target=R/'Saved/WildEncountersV2/OpenBefore.t3d';assert not target.exists()
t=unreal.AssetExportTask();t.object=w;t.filename=str(target);t.exporter=unreal.LevelExporterT3D();t.automated=True;t.selected=False;t.prompt=False;t.replace_identical=False;assert unreal.Exporter.run_asset_export_task(t),t.errors;assert target.exists();unreal.log('OPEN_MAP_READ_ONLY_EXPORT '+str(target))
