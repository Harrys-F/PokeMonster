import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/RangerAnimationV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_NPCMotionV3'
old=json.loads((S/'FootSessionBefore.json').read_text())
for n,v in old['quality_before'].items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
a={'world':w.get_path_name(),'pie':False,'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.VSync','r.VSyncEditor','t.MaxFPS','rhi.SyncInterval','r.ScreenPercentage','r.Editor.Viewport.OverridePIEScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional']}}
assert not a['dirty_maps'] and not a['dirty_content'],a
(S/'FinalEditorState.json').write_text(json.dumps(a,indent=2))
if hasattr(unreal,'_rangermotion3_queue'):unreal.unregister_slate_post_tick_callback(unreal._rangermotion3_queue);del unreal._rangermotion3_queue
