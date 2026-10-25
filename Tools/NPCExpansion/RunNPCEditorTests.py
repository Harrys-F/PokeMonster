import unreal
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
unreal.SystemLibrary.execute_console_command(W,'Automation RunTests PokeMonster.NPC')
