import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();d=json.loads((O/'FootSessionBefore.json').read_text());after={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in d['profile_before']};assert after==d['profile_scope_before'],(d['profile_scope_before'],after)
for n,v in d['quality_before'].items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
final={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in d['profile_before']};assert final==d['profile_before'],(final,d['profile_before'])
(O/'FootSessionAfter.json').write_text(json.dumps({'profile_restored':after,'original_profile_settings_after_quality_restore':final,'quality_restored':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in d['quality_before']}},indent=2))
