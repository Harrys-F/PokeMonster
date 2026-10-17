import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV3'
for n,v in json.loads((O/'GPUPrepareBefore.json').read_text()).items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
saved=json.loads((O/'EditorSettingsBefore.json').read_text())
for n,v in saved['cvars'].items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));s.set_editor_property('bThrottleCPUWhenNotForeground',saved['throttle'])
d={'map':w.get_path_name(),'game_world':None,'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.Editor.Viewport.OverridePIEScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.ScreenPercentage','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional','r.ProfileGPU.ShowUI']},'throttle_restored':s.get_editor_property('bThrottleCPUWhenNotForeground'),'save_sha256':hashlib.sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest()}
assert not d['dirty_maps'] and not d['dirty_content'];assert d['save_sha256']==(O/'DevSaveInitialSHA256.txt').read_text();(O/'FinalEditorState.json').write_text(json.dumps(d,indent=2));unreal.log('ENVIRONMENT_PERF_V3_FINAL_EDITOR_CLEAN')
