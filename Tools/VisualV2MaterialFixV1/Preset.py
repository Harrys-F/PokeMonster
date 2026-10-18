import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2MaterialFixV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
j=json.loads((O/'Request.json').read_text());q=j['config'][2]
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:unreal.SystemLibrary.execute_console_command(w,'sg.'+n+'Quality '+str(q))
unreal.SystemLibrary.execute_console_command(w,'r.Editor.Viewport.OverridePIEScreenPercentage 0');unreal.SystemLibrary.execute_console_command(w,'r.SecondaryScreenPercentage.GameViewport 100')
if hasattr(unreal,'AssetCompilingManager') and hasattr(unreal.AssetCompilingManager,'finish_all_compilation'):unreal.AssetCompilingManager.finish_all_compilation()
(O/(j['label']+'_Preset.json')).write_text(json.dumps({'quality_set_before_PIE':q,'world':w.get_path_name()},indent=2))
