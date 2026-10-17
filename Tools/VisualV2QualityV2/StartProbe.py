import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2QualityV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_TestMap_VisualV2' in w.get_name()
j=json.loads((O/'Request.json').read_text());plan=R/'Tools/VisualV2QualityV2/Plans'/(j['label']+'.tsv');assert plan.exists();assert not (R/'Saved/EnvironmentPerfV1'/(j['label']+'_Done.txt')).exists()
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf.Run "'+str(plan)+'"')

exec((R/'Tools/VisualV2QualityV2/Monitor.py').read_text())
