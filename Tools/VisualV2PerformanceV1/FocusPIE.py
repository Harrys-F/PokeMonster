import unreal
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world();assert W and unreal._perf1_isolated
PC=unreal.GameplayStatics.get_player_controller(W,0);assert not PC.is_menu_open()
unreal.WidgetLibrary.set_focus_to_game_viewport()
