import unreal,json
from pathlib import Path
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world()
d={'maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]};assert not any(d.values()),d
Path(unreal.Paths.project_dir(),'Saved/VisualV2WorldArtQualityV1/BeforeClose.json').write_text(json.dumps(d,indent=2));unreal.SystemLibrary.quit_editor()
