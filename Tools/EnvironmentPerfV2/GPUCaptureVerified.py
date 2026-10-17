"""Capture GPU during an asserted QHD scope; no model/tool scheduling delay."""
import unreal,time,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
profiles=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterEnvironmentRenderProfileV2)
for a in profiles:a.set_rendering_overrides_enabled(False)
plan=R/'Tools/EnvironmentPerfV2/Plans/GPUCaptureVerified.tsv';assert not plan.exists();plan.write_text('GPUCaptureVerified\tPIE\t10\t20\nWald\tControl\t1\t2560\t1440\t2\t100\n')
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"');start=time.monotonic();sent=False
before={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.ProfileGPU.ShowUI','r.ProfileGPU.ShowLeafEvents','r.ProfileGPU.ThresholdPercent']}
def tick(dt):
 global sent
 if (O/'GPUCaptureVerified_Done.txt').exists():
  for a in profiles:a.set_rendering_overrides_enabled(True)
  for n,v in before.items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
  unreal.unregister_slate_post_tick_callback(unreal._envperf_gpu_capture);del unreal._envperf_gpu_capture;return
 if time.monotonic()-start>8 and not sent:
  pc=unreal.GameplayStatics.get_player_controller(w,0);extent=tuple(pc.get_viewport_size());assert extent==(2560,1440),extent
  names=['r.ScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing']
  vals={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names};assert list(vals.values())==[100.,100.,1.,1.],vals
  (O/'GPUCaptureVerified_Proof.json').write_text(json.dumps({'viewport':extent,'cvars':vals,'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},indent=2))
  for c in ['r.ProfileGPU.ShowUI 0','r.ProfileGPU.ShowLeafEvents 1','r.ProfileGPU.ThresholdPercent 0.1','ProfileGPU']:unreal.SystemLibrary.execute_console_command(w,c)
  sent=True
unreal._envperf_gpu_capture=unreal.register_slate_post_tick_callback(tick)
