import unreal
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_EnvironmentPerfV1')
