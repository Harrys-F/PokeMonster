"""Restore temporary editor review preferences; never writes a game or map."""
import unreal
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()
if hasattr(unreal,'_save_v2_settings'):
 v=unreal._save_v2_settings;settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));settings.set_editor_property('bThrottleCPUWhenNotForeground',v['throttle']);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.Evolution.Auto '+str(v['auto']));del unreal._save_v2_settings
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
