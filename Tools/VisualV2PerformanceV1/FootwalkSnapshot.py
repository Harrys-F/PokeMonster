import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';q=json.loads((D/'FootwalkRequest.json').read_text());W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and unreal._perf1_isolated;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
if q.get('setup'):
 P.set_actor_location(unreal.Vector(-200,-100,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock set 1 9 0',PC)
p=D/'ManualFootwalk.json';a=json.loads(p.read_text())if p.exists()else[];a.append({'label':q['label'],'utc_epoch':time.time(),'position':P.get_actor_location().to_tuple(),'velocity':P.get_velocity().to_tuple(),'sprint':P.is_sprint_mode_enabled(),'input_locked':P.is_overworld_input_locked(),'camera':PC.player_camera_manager.get_camera_location().to_tuple()});p.write_text(json.dumps(a,indent=2))
