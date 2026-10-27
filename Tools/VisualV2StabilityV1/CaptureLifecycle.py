import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';assert json.loads((D/'CaptureBefore01/Result.json').read_text())['passed'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();PC=unreal.GameplayStatics.get_player_controller(W,0)
unreal.SystemLibrary.execute_console_command(W,'pm.TAAReview.CaptureStart '+str(R/'Saved/VisualV2TAAIntegrationV1/Recordings/StabilityStopBefore01')+' slate 30',PC)
