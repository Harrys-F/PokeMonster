import unreal
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_game_world();assert w
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Stop')
