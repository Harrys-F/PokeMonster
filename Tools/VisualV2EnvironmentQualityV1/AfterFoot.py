import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2EnvironmentQualityV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();before=json.loads((O/'FootCvarsBefore.json').read_text())
for n,v in before.items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
after={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in before};assert after==before,(before,after)
(O/'FootCvarsRestored.json').write_text(json.dumps(after,indent=2))
