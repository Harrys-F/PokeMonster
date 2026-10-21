import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
for cmd in ['pm.EnvPerf2.Viewport 2560 1440','r.ScreenPercentage 100']:unreal.SystemLibrary.execute_console_command(w,cmd)
