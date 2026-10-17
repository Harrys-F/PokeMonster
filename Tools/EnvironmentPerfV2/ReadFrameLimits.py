import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
for c in ['getall Engine bSmoothFrameRate','getall Engine bUseFixedFrameRate','getall Engine FixedFrameRate','getall Engine SmoothedFrameRateRange']:unreal.SystemLibrary.execute_console_command(w,c)
