import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV3';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
names=['sg.'+n+'Quality' for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]
assert not (O/'GPUPrepareBefore.json').exists();(O/'GPUPrepareBefore.json').write_text(json.dumps({n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names},indent=2))
for n in names:unreal.SystemLibrary.execute_console_command(w,n+' 2')
