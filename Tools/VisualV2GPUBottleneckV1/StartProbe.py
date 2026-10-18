import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2GPUBottleneckV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_TestMap_VisualV2GPUBottleneckV1' in w.get_name()
j=json.loads((O/'Request.json').read_text());plan=R/'Tools/VisualV2GPUBottleneckV1/Plans'/(j['label']+'.tsv');assert plan.exists();assert not (R/'Saved/EnvironmentPerfV2'/(j['label']+'_Done.txt')).exists()
if j['label']=='VGB1_Final_PIE_FactorsAA':
 import runpy
 runpy.run_path(str(R/'Tools/VisualV2GPUBottleneckV1/PhotoThenProbe.py'),run_name='__main__')
else:
 unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"')
 exec((R/'Tools/VisualV2GPUBottleneckV1/Monitor.py').read_text())
