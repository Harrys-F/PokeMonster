import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV1';j=json.loads((S/'PerfRequest.json').read_text());w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2';plan=R/'Tools/VisualV2WorldArtQualityV1/Plans'/('VGB1_WorldArt_'+j['phase']+'_PIE.tsv');assert not (R/'Saved/EnvironmentPerfV2'/(plan.stem+'_Done.txt')).exists();unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"')
