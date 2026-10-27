"""Separate GPU-tree sample, explicitly excluded from regular timings."""
import unreal,time,json,runpy,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:cmd('sg.'+n+'Quality 2')
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('r.DynamicRes.OperationMode 0');cmd('pm.WorldClock set 1 12 0');P.set_actor_location(unreal.Vector(-4300,1550,50.15),False,True)
runpy.run_path(str(R/'Tools/VisualV2PerformanceV1/Inventory.py'),run_name='__main__')
state={'start':time.monotonic(),'sent':False};old={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.ProfileGPU.ShowUI','r.ProfileGPU.ShowLeafEvents','r.ProfileGPU.ThresholdPercent']}
def tick(dt):
 elapsed=time.monotonic()-state['start']
 if elapsed>6 and not state['sent']:
  assert tuple(PC.get_viewport_size())==(2560,1440)
  unreal.log('PERFOPT_GPU_BASELINE_BEGIN')
  for x in ['r.ProfileGPU.ShowUI 0','r.ProfileGPU.ShowLeafEvents 1','r.ProfileGPU.ThresholdPercent 0.1','ProfileGPU']:cmd(x)
  state['sent']=True
 if elapsed>12:
  for n,v in old.items():cmd(n+' '+str(v))
  unreal.unregister_slate_post_tick_callback(unreal._perf1_profile);(D/'GPUProfileBaseline.json').write_text(json.dumps({'requested':state['sent'],'viewport':list(PC.get_viewport_size()),'excluded_from_benchmark':True}));unreal.log('PERFOPT_GPU_BASELINE_END')
unreal._perf1_profile=unreal.register_slate_post_tick_callback(tick)
