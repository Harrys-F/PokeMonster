import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/RangerAnimationV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_NPCMotionV2'
old=json.loads((O/'FootSessionBefore.json').read_text())
for n,val in old['quality_before'].items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(val))
a={'world':w.get_path_name(),'dirty_maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.VSync','r.VSyncEditor','t.MaxFPS','rhi.SyncInterval','r.ScreenPercentage','r.Editor.Viewport.OverridePIEScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional']}}
(O/'FinalEditorState.json').write_text(json.dumps(a,indent=2));assert not a['dirty_maps'] and not a['dirty_content'];unreal.log('NPC_MOTION_FINAL_EDITOR_CLEAN')
if hasattr(unreal,'_rangermotion2_queue'):unreal.unregister_slate_post_tick_callback(unreal._rangermotion2_queue);del unreal._rangermotion2_queue
