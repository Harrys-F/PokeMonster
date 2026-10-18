import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
if w:unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Stop')
