import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
j=json.loads((O/'Request.json').read_text());plan=R/'Tools/EnvironmentPerfV2/Plans'/(j['plan']+'.tsv');assert plan.exists();assert not (O/(j['plan']+'_Done.txt')).exists()
profiles=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterEnvironmentRenderProfileV2)
if j['plan'].startswith('Repair'):
 for a in profiles:a.set_rendering_overrides_enabled(False)
else:assert not profiles,'Run paired probe before persisting V2 profile; standalone uses preserved V1 world'
assert w.get_name() in ['Dev_TestMap_VisualV2','Dev_TestMap_EnvironmentPerfV2']
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"')
