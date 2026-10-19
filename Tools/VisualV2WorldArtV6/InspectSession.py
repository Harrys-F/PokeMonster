import unreal,json
from pathlib import Path
D='/Game/Environment/VisualV2WorldArtV6';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
r={'assets':list(unreal.EditorAssetLibrary.list_assets(D,True,False)),'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'game':bool(E.get_game_world())};Path(unreal.Paths.project_dir(),'Saved/VisualV2WorldArtV6/Inspection.json').write_text(json.dumps(r,indent=2))
