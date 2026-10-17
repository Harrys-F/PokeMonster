"""One untimed verified GPU capture, separate from the completed genuine foot route."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_EnvironmentPerfV3';p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);before=p.get_actor_transform()
names=['r.ScreenPercentage','r.Editor.Viewport.OverridePIEScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.ProfileGPU.ShowUI'];saved={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names}
for n,v in zip(names,[100,0,100,0]):unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf3.Viewport 2560 1440');p.set_actor_location(unreal.Vector(-4300,1550,50.15),False,True);start=time.monotonic();sent=False
assert not hasattr(unreal,'_env3_gpu_capture')
def tick(dt):
 global sent
 elapsed=time.monotonic()-start
 if elapsed>10 and not sent:
  cam=pc.player_camera_manager;proof={'map':w.get_path_name(),'viewport':list(pc.get_viewport_size()),'camera':cam.get_camera_location().to_tuple(),'rotation':cam.get_camera_rotation().to_tuple(),'fov':cam.get_fov_angle(),'not_a_foot_test':True,'profile':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.ScreenPercentage','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor']}}
  assert proof['viewport']==[2560,1440];(O/'GPUCaptureProof.json').write_text(json.dumps(proof,indent=2));unreal.log('ENV3_GPU_CAPTURE_BEGIN');unreal.SystemLibrary.execute_console_command(w,'ProfileGPU');sent=True
 if elapsed>18:
  for n,v in saved.items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
  unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf3.Viewport 0 0');p.set_actor_transform(before,False,True);unreal.unregister_slate_post_tick_callback(unreal._env3_gpu_capture);del unreal._env3_gpu_capture;unreal.log('ENV3_GPU_CAPTURE_END');(O/'GPUCaptureDone.txt').write_text('Complete')
unreal._env3_gpu_capture=unreal.register_slate_post_tick_callback(tick)
