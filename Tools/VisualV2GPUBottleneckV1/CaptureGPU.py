"""Extra profile/capture pass only: excluded from all timing comparisons."""
import unreal,time,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2GPUBottleneckV1';P=R/'Saved/EnvironmentPerfV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
label='VGB1_GPUCapture';plan=R/'Tools/VisualV2GPUBottleneckV1/Plans'/(label+'.tsv');assert not plan.exists();plan.write_text(label+'\tPIE\t10\t50\nWald\tControl\t1\t2560\t1440\t2\t100\n')
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"');start=time.monotonic();sent=False
before={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.ProfileGPU.ShowUI','r.ProfileGPU.ShowLeafEvents','r.ProfileGPU.ThresholdPercent']}
def tick(dt):
 global sent
 if (P/(label+'_Done.txt')).exists():
  for n,v in before.items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
  unreal.unregister_slate_post_tick_callback(unreal._vgb_capture);return
 if time.monotonic()-start>12 and not sent:
  pc=unreal.GameplayStatics.get_player_controller(w,0);extent=tuple(pc.get_viewport_size());assert extent==(2560,1440)
  cv={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.ScreenPercentage','r.Lumen.FinalGatherMethod','r.Shadow.Virtual.Enable','r.Nanite']}
  assert cv['r.ScreenPercentage']==100 and cv['r.Lumen.FinalGatherMethod']==1
  (O/'GPUCaptureProof.json').write_text(json.dumps({'viewport':extent,'cvars':cv,'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},indent=2))
  for c in ['r.ProfileGPU.ShowUI 0','r.ProfileGPU.ShowLeafEvents 1','r.ProfileGPU.ThresholdPercent 0.05','ProfileGPU']:unreal.SystemLibrary.execute_console_command(w,c)
  sent=True
unreal._vgb_capture=unreal.register_slate_post_tick_callback(tick)
