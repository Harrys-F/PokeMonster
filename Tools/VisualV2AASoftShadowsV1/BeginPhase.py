"""Start the unchanged scoped probe; images only in excluded photo segments."""
import unreal,json,time,csv,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2AASoftShadowsV1';P=R/'Saved/EnvironmentPerfV2';j=json.loads((O/'Request.json').read_text());label=j['label'];plan=R/'Tools/VisualV2AASoftShadowsV1/Plans'/(label+'.tsv');w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1' and unreal.GameplayStatics.get_player_pawn(w,0));pc=unreal.GameplayStatics.get_player_controller(w,0)
assert not (P/(label+'_Done.txt')).exists();dest=O/'Screenshots'/label;dest.mkdir(parents=True,exist_ok=False);rows=list(csv.reader(plan.open(),delimiter='\t'))[1:];current=-1;stage=time.monotonic();sent=False;proof=[]
(O/(label+'_Review.json')).write_text(json.dumps({'captures':[],'error':None,'initial_manifest':True},indent=2))
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"');photo_paused={}
def tick(dt):
 global current,stage,sent
 try:
  if (P/(label+'_Done.txt')).exists():
   for c,v in photo_paused.items():c.set_editor_property('pause_anims',v)
   unreal.unregister_slate_post_tick_callback(unreal._vmf_phase);(O/(label+'_Review.json')).write_text(json.dumps({'captures':proof,'error':None},indent=2));return
  f=P/(label+'_Segments.csv');index=len(list(csv.DictReader(f.open()))) if f.exists() else 0
  if index!=current:current=index;stage=time.monotonic();sent=False
  if current>=len(rows) or rows[current][2]!='90':return
  if not photo_paused:
   for c in unreal.ObjectIterator(unreal.SkeletalMeshComponent):
    if c.get_world()==w:photo_paused[c]=c.get_editor_property('pause_anims');c.set_editor_property('pause_anims',True)
  if sent or time.monotonic()-stage<3:return
  r=rows[current];cam=pc.player_camera_manager;assert list(pc.get_viewport_size())==list(map(int,r[3:5]))
  filename=dest/(r[0]+'_'+r[1].replace(':','_')+'_'+'_'.join(r[3:7])+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(filename)+'"',pc);sent=True
  bushes=[]
  for c in unreal.ObjectIterator(unreal.HierarchicalInstancedStaticMeshComponent):
   if c.get_world()==w and c.static_mesh and 'WildBush' in c.static_mesh.get_name():bushes.append({'component':c.get_path_name(),'instances':c.get_instance_count(),'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())]})
  proof.append({'requested_file':str(filename),'config':list(map(int,r[3:7])),'viewport':list(pc.get_viewport_size()),'camera':cam.get_camera_location().to_tuple(),'rotation':cam.get_camera_rotation().to_tuple(),'fov':cam.get_fov_angle(),'bushes':bushes,'photo_outside_timing_rows':True,'variant':r[1],'site':r[0],'aa':unreal.SystemLibrary.get_console_variable_int_value('r.AntiAliasingMethod'),'decals':[{'location':c.get_world_location().to_tuple(),'visible':c.is_visible(),'size':c.decal_size.to_tuple()} for c in unreal.ObjectIterator(unreal.DecalComponent) if c.get_world()==w and c.get_decal_material()], 'lights':[{'path':c.get_path_name(),'position':c.get_world_location().to_tuple(),'rotation':c.get_world_rotation().to_tuple(),'intensity':c.intensity,'color':str(c.light_color),'cast_shadows':c.cast_shadows,'indirect_intensity':c.indirect_lighting_intensity} for c in unreal.ObjectIterator(unreal.LightComponent) if c.get_world()==w], 'pp':[{'name':a.get_name(),'settings':a.settings.export_text()} for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume)]});(O/(label+'_Review.json')).write_text(json.dumps({'captures':proof,'error':None},indent=2))
 except Exception:
  (O/(label+'_PhotoError.txt')).write_text(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._vmf_phase)
unreal._vmf_phase=unreal.register_slate_post_tick_callback(tick)
