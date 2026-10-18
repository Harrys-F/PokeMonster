import unreal
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world()
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
