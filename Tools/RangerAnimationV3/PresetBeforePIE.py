import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/RangerAnimationV3';request=json.loads((O/'BenchmarkRequest.json').read_text());e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();q=request['config'][2]
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:unreal.SystemLibrary.execute_console_command(w,'sg.'+n+'Quality '+str(q))
if hasattr(unreal,'AssetCompilingManager'):
 manager=unreal.AssetCompilingManager
 if hasattr(manager,'finish_all_compilation'):manager.finish_all_compilation()
(O/(request['label']+'_Preset.json')).write_text(json.dumps({'quality_set_before_PIE':q,'map':w.get_path_name()},indent=2))
