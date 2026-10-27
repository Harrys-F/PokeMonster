import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GraphicsVariantC';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
v=unreal._perf1_preferences;s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));s.set_editor_property('bThrottleCPUWhenNotForeground',v['throttle']);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.Evolution.Auto '+str(v['auto']));unreal.log('PERF1_CLEAN_CLOSE_READY')
