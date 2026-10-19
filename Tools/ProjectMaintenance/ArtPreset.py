import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();w=E.get_editor_world()
for name in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:unreal.SystemLibrary.execute_console_command(w,'sg.'+name+'Quality 2')
unreal.SystemLibrary.execute_console_command(w,'r.Editor.Viewport.OverridePIEScreenPercentage 0');unreal.SystemLibrary.execute_console_command(w,'r.SecondaryScreenPercentage.GameViewport 100')
if hasattr(unreal,'AssetCompilingManager'):unreal.AssetCompilingManager.finish_all_compilation()
