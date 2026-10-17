import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV1';last=0
if hasattr(unreal,'_envperf_monitor'):unreal.unregister_slate_post_tick_callback(unreal._envperf_monitor)
names=['sg.ViewDistanceQuality','sg.AntiAliasingQuality','sg.ShadowQuality','sg.GlobalIlluminationQuality','sg.ReflectionQuality','sg.PostProcessQuality','sg.TextureQuality','sg.EffectsQuality','sg.FoliageQuality','sg.ShadingQuality','r.VSync','t.MaxFPS','r.DynamicRes.OperationMode','r.ScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.Editor.Viewport.OverridePIEScreenPercentage','r.Shadow.Virtual.Enable','r.ShadowQuality','r.Shadow.MaxResolution','r.Shadow.DistanceScale','r.Shadow.Virtual.ResolutionLodBiasDirectional','r.Shadow.Virtual.SMRT.RayCountDirectional','r.AmbientOcclusionLevels','r.BloomQuality','r.DepthOfFieldQuality','r.MotionBlurQuality','r.AntiAliasingMethod','r.TSR.History.ScreenPercentage','r.TSR.History.UpdateQuality','r.Lumen.DiffuseIndirect.Allow','r.Lumen.Reflections.Allow','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Lumen.FinalGatherMethod','r.SSR.Quality']
def monitor(dt):
 global last
 now=time.monotonic()
 if now-last<2:return
 last=now;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
 if not w:return
 d={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'map':w.get_path_name(),'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names}}
 with (O/'RuntimeSettings.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
unreal._envperf_monitor=unreal.register_slate_post_tick_callback(monitor)
