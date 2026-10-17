import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
j=json.loads((O/'Request.json').read_text());plan=R/'Tools/EnvironmentPerfV1/Plans'/(j['plan']+'.tsv');assert plan.exists();assert not (O/(j['plan']+'_Done.txt')).exists()
assert w.get_name() in ['Dev_TestMap_VisualV2','Dev_TestMap_EnvironmentPerfV1']
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf.Run "'+str(plan)+'"')
