import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));out={'throttle':s.get_editor_property('bThrottleCPUWhenNotForeground'),'cvars':{}}
for n,v in [('r.Editor.Viewport.OverridePIEScreenPercentage',0),('r.SecondaryScreenPercentage.GameViewport',100)]:
 out['cvars'][n]=unreal.SystemLibrary.get_console_variable_float_value(n);unreal.SystemLibrary.execute_console_command(e.get_editor_world(),n+' '+str(v))
if not (O/'EditorSettingsBefore.json').exists():(O/'EditorSettingsBefore.json').write_text(json.dumps(out,indent=2))
s.set_editor_property('bThrottleCPUWhenNotForeground',False)
exec((R/'Tools/EnvironmentPerfV1/Queue.py').read_text())
