import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/RangerAnimationV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
a={'world':e.get_editor_world().get_path_name(),'pie':bool(e.get_game_world()),'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
(O/'EditorBefore.json').write_text(json.dumps(a,indent=2));assert not a['pie'] and not a['dirty_maps'] and not a['dirty_content'],a
exec((R/'Tools/RangerAnimationV3/Queue.py').read_text())
