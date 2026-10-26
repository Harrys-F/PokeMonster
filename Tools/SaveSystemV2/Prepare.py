"""Read-only scene baseline; temporary review settings only, no project/config writes."""
from pathlib import Path
import unreal,json,sys
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/SaveSystemV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world() and E.get_editor_world().get_name()=='Dev_TestMap_VisualV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
p=D/'OriginalScene.json'
if not p.exists():p.write_text(json.dumps(scene(E.get_editor_world()),indent=2))
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
if not hasattr(unreal,'_save_v2_settings'):unreal._save_v2_settings={'throttle':settings.get_editor_property('bThrottleCPUWhenNotForeground'),'auto':unreal.SystemLibrary.get_console_variable_int_value('pm.Evolution.Auto')}
settings.set_editor_property('bThrottleCPUWhenNotForeground',False);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.Evolution.Auto 0')
