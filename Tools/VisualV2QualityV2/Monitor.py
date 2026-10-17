import unreal,json,csv,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2QualityV2';P=R/'Saved/EnvironmentPerfV1';j=json.loads((O/'Request.json').read_text());label=j['label'];w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=(R/'Tools/VisualV2QualityV2/Plans'/(label+'.tsv')).read_text().splitlines()[1:];last=-1;start=time.monotonic();events=[]
names=['r.VSync','t.MaxFPS','rhi.SyncInterval','r.ScreenPercentage','r.DynamicRes.OperationMode','r.BloomQuality','r.MotionBlurQuality','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Shadow.Virtual.ResolutionLodBiasDirectional','r.Shadow.Virtual.Enable','r.AntiAliasingMethod']
def tick(dt):
 global last
 if (P/(label+'_Done.txt')).exists():
  unreal.unregister_slate_post_tick_callback(unreal._visualenv_monitor);del unreal._visualenv_monitor
  (O/(label+'_RuntimeCvars.json')).write_text(json.dumps(events,indent=2));return
 if time.monotonic()-start<1:return
 f=P/(label+'_Segments.csv');index=len(list(csv.DictReader(f.open()))) if f.exists() else 0
 if index==last or index>=len(rows):return
 last=index;events.append({'index':index,'row':rows[index].split('\t'),'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names}})
 (O/(label+'_RuntimeCvars.json')).write_text(json.dumps(events,indent=2))
unreal._visualenv_monitor=unreal.register_slate_post_tick_callback(tick)
