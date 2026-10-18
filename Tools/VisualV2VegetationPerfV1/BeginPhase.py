"""Paired native map AA and temporarily bypassed blendable; no lighting changes."""
import unreal,json,time,csv,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2VegetationPerfV1';P=R/'Saved/EnvironmentPerfV2';j=json.loads((S/'Request.json').read_text());label=j['label'];plan=R/'Tools/VisualV2VegetationPerfV1/Plans'/(label+'.tsv');w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1' and unreal.GameplayStatics.get_player_pawn(w,0));pc=unreal.GameplayStatics.get_player_controller(w,0);D=S/'Screenshots'/label;D.mkdir(parents=True,exist_ok=False);rows=list(csv.reader(plan.open(),delimiter='\t'))[1:];current=-1;stage=time.monotonic();sent=False;proof=[];paused={}
assert not (P/(label+'_Done.txt')).exists();unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"');(S/(label+'_Review.json')).write_text(json.dumps({'captures':[],'error':None}))
def tick(dt):
 global current,stage,sent
 try:
  if (P/(label+'_Done.txt')).exists():
   for c,v in paused.items():c.set_editor_property('pause_anims',v)
   unreal.unregister_slate_post_tick_callback(unreal._veg_phase);(S/(label+'_Review.json')).write_text(json.dumps({'captures':proof,'error':None},indent=2));return
  f=P/(label+'_Segments.csv');i=len(list(csv.DictReader(f.open()))) if f.exists() else 0
  if i!=current:current=i;stage=time.monotonic();sent=False
  if i>=len(rows) or rows[i][2]!='90' or sent or time.monotonic()-stage<2.7:return
  if not paused:
   for c in unreal.ObjectIterator(unreal.SkeletalMeshComponent):
    if c.get_world()==w:paused[c]=c.pause_anims;c.set_editor_property('pause_anims',True)
  r=rows[i];cam=pc.player_camera_manager;file=D/(r[0]+'_'+r[1].replace(':','_')+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(file)+'"',pc);sent=True
  lights=[];shadows=[]
  for cls in [unreal.LightComponent,unreal.SkyLightComponent]:
   for c in unreal.ObjectIterator(cls):
    if c.get_world()!=w:continue
    props={}
    for n in ['intensity','light_color','indirect_lighting_intensity','cast_shadows','source_angle','temperature','use_temperature','real_time_capture','cubemap','volumetric_scattering_intensity']:
     try:
      v=c.get_editor_property(n);props[n]=v.export_text() if hasattr(v,'export_text') else v.get_path_name() if isinstance(v,unreal.Object) else str(v)
     except Exception:pass
    lights.append({'path':c.get_path_name(),'transform':c.get_world_transform().export_text(),'props':props})
  for c in unreal.ObjectIterator(unreal.PrimitiveComponent):
   if c.get_world()==w:shadows.append([c.get_path_name(),c.cast_shadow])
  pp=[]
  for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume):
   s=unreal.PostProcessSettings();s.import_text(a.settings.export_text());weighted=s.weighted_blendables;snap=[{'object':x.object.get_class().get_name() if x.object else None,'weight':x.weight} for x in weighted.array];weighted.array=[];s.weighted_blendables=weighted;pp.append({'name':a.get_name(),'without_blendables':s.export_text(),'blendables':snap})
  proof.append({'file_request':str(file),'site':r[0],'factor':r[1],'config':j['config'],'viewport':list(pc.get_viewport_size()),'camera':cam.get_camera_location().to_tuple(),'rotation':cam.get_camera_rotation().to_tuple(),'fov':cam.get_fov_angle(),'lights':lights,'shadows':shadows,'pp':pp});(S/(label+'_Review.json')).write_text(json.dumps({'captures':proof,'error':None},indent=2))
 except Exception:
  (S/(label+'_PhotoError.txt')).write_text(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._veg_phase)
unreal._veg_phase=unreal.register_slate_post_tick_callback(tick)
