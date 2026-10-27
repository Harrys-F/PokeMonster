import unreal
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);unreal.SystemLibrary.execute_console_command(E.get_game_world()or E.get_editor_world(),'pm.TAAReview.CaptureStop')
