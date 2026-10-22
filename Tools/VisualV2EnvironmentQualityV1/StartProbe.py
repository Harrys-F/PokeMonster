import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2EnvironmentQualityV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_TestMap_VisualV2EnvironmentQualityV1' in w.get_name()
j=json.loads((O/'Request.json').read_text());plan=R/'Tools/VisualV2EnvironmentQualityV1/Plans'/(j['label']+'.tsv');assert plan.exists();assert not (R/'Saved/EnvironmentPerfV1'/(j['label']+'_Done.txt')).exists()
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf.Run "'+str(plan)+'"')

exec((R/'Tools/VisualV2EnvironmentQualityV1/Monitor.py').read_text())
