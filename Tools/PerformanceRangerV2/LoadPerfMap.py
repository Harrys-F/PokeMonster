import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_RangerPerfV2')
