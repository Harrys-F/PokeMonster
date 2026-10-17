import unreal,json
from pathlib import Path
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world()
d={'maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'content':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
Path(unreal.Paths.project_dir(),'Saved/RangerAnimationV2/EditorBeforeBuild.json').write_text(json.dumps(d,indent=2));assert not d['maps'] and not d['content'],'Protect unsaved editor changes'
unreal.SystemLibrary.quit_editor()
