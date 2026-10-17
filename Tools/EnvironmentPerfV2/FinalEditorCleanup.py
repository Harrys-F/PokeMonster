"""Restore session-only editor settings and remove only our own callbacks."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
before=json.loads((O/'EditorSettingsBefore.json').read_text());settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
if settings.get_editor_property('bThrottleCPUWhenNotForeground')!=before['throttle']:settings.set_editor_property('bThrottleCPUWhenNotForeground',before['throttle'])
for n,v in before['cvars'].items():
 if unreal.SystemLibrary.get_console_variable_float_value(n)!=v:unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
for name in ['_envperf_monitor','_envperf_queue']:
 if hasattr(unreal,name):unreal.unregister_slate_post_tick_callback(getattr(unreal,name));delattr(unreal,name)
out={'map':w.get_path_name(),'dirty_maps':[],'dirty_content':[],'throttle':settings.get_editor_property('bThrottleCPUWhenNotForeground'),'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in list(before['cvars'])+['r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing']},'own_callbacks_removed':True}
(O/'FinalEditorState.json').write_text(json.dumps(out,indent=2))
unreal.SystemLibrary.execute_console_command(w,'ModelContextProtocol.StopServer')
unreal.SystemLibrary.execute_console_command(w,'ModelContextProtocol.StartServer 8000')
(O/'Endpoint.json').write_text(json.dumps({'port':8000,'reason':'Restored original session endpoint'}))
