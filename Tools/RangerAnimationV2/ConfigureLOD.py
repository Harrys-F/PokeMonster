import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion2.AuditLODs .22');m=unreal.load_asset('/Game/Characters/NPCs/RangerMotionV2/Meshes/SK_Ranger_AQV2');unreal.EditorAssetLibrary.save_loaded_asset(m,False)
