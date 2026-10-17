import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/RangerAnimationV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
j=json.loads((O/'Request.json').read_text());plan=R/'Tools/RangerAnimationV2/Plans'/(j['plan']+'.tsv');assert plan.exists();assert not (O/(j['plan']+'_Done.txt')).exists()
assert 'Dev_TestMap_NPCMotionV2' in w.get_name()
unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion2.Run '+str(plan))
