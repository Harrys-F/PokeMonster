"""Guard the existing editor state and temporary CVars; no config or map saves."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()
assert E.get_editor_world().get_name()=='Dev_TestMap_VisualV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
keys=['pm.Evolution.Auto','r.ScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.DynamicRes.OperationMode']
values={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in keys};settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
unreal._praxis_settings={'cvars':values,'throttle':settings.get_editor_property('bThrottleCPUWhenNotForeground')};settings.set_editor_property('bThrottleCPUWhenNotForeground',False);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.Evolution.Auto 0')
