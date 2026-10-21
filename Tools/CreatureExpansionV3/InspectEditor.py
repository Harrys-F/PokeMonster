"""Read-only active editor state; never load a map or save/discard a package."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);s={'time':time.time(),'world':E.get_editor_world().get_path_name(),'pie':bool(E.get_game_world()),'dirty_maps':[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]};(R/'Saved/CreatureExpansionV3/EditorState.json').write_text(json.dumps(s,indent=2));unreal.log('EXPANSION_EDITOR_STATE '+json.dumps(s))
