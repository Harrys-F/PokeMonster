import unreal,json,csv,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2GPUBottleneckV1';P=R/'Saved/EnvironmentPerfV2';j=json.loads((O/'Request.json').read_text());label=j['label'];w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=(R/'Tools/VisualV2GPUBottleneckV1/Plans'/(label+'.tsv')).read_text().splitlines()[1:];last=-1;start=time.monotonic();events=[]
names=['r.Lumen.DiffuseIndirect.Allow','r.Lumen.Reflections.Allow','r.Lumen.HardwareRayTracing','r.Nanite','r.Nanite.ProjectEnabled','r.Shadow.Virtual.Cache','r.VSync','t.MaxFPS','rhi.SyncInterval','r.ScreenPercentage','r.DynamicRes.OperationMode','r.BloomQuality','r.MotionBlurQuality','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Shadow.Virtual.ResolutionLodBiasDirectional','r.Shadow.Virtual.Enable','r.AntiAliasingMethod']
def signature():
 result=[]
 for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   sm=c.static_mesh
   if not sm or not sm.get_name().startswith('SM_WLA_') or not any(n in sm.get_name() for n in ['Oak','Birch','Bush','Grass','Fern','Flower','Herb']):continue
   result.append({'actor':a.get_name(),'component':c.get_name(),'visible':c.is_visible(),'shadow':c.cast_shadow,'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())]})
 return result
def tick(dt):
 global last
 if (P/(label+'_Done.txt')).exists():
  unreal.unregister_slate_post_tick_callback(unreal._visualenv_monitor);del unreal._visualenv_monitor
  (O/(label+'_Restored.json')).write_text(json.dumps({'signature':signature(),'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names}},indent=2));(O/(label+'_RuntimeCvars.json')).write_text(json.dumps(events,indent=2));return
 if time.monotonic()-start<1:return
 f=P/(label+'_Segments.csv');index=len(list(csv.DictReader(f.open()))) if f.exists() else 0
 if index==last or index>=len(rows):return
 row=rows[index].split('\t')
 if row[1]=='Control':
  expected={'r.AntiAliasingMethod':4,'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':1,'r.Shadow.Virtual.SMRT.RayCountDirectional':4 if int(row[5])==1 else 8,'r.Lumen.FinalGatherMethod':0 if int(row[5])==1 else 1}
  actual={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in expected}
  assert actual==expected,('Invalid stock baseline',actual,expected)
 last=index;events.append({'index':index,'row':rows[index].split('\t'),'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'signature':signature(),'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names}})
 (O/(label+'_RuntimeCvars.json')).write_text(json.dumps(events,indent=2))
unreal._visualenv_monitor=unreal.register_slate_post_tick_callback(tick)
