"""Real game-camera captures in disposable PIE. Controlled positioning is NOT a foot test.
Run only between benchmarks. Screenshot stalls occur inside an 8s warm-up, not reported as performance data.
"""
import unreal,json,time,csv,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2GPUBottleneckV1';P=R/'Saved/EnvironmentPerfV2';request=json.loads((O/'ReviewRequest.json').read_text());label=request['label'];folder=O/'Screenshots'/label;folder.mkdir(parents=True,exist_ok=False)
w=next(w for w in unreal.ObjectIterator(unreal.World) if 'Dev_TestMap_VisualV2GPUBottleneckV1' in w.get_name() and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);original=p.get_actor_transform()
rows=request['rows'];plan=R/'Tools/VisualV2GPUBottleneckV1/Plans'/(label+'.tsv');assert not plan.exists();plan.write_text('\t'.join(map(str,[label,request.get('mode','PIE'),8,1]))+'\n'+'\n'.join('\t'.join(map(str,[r['site'],r['condition'],1,2560,1440,request.get('quality',2),request.get('percentage',100)])) for r in rows)+'\n')
paused=[(c,c.get_editor_property('pause_anims')) for c in unreal.ObjectIterator(unreal.SkeletalMeshComponent) if c.get_world()==w]
for c,_ in paused:c.set_editor_property('pause_anims',True)
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"');current=-1;stage=time.monotonic();created=stage;sent=False;records=[]
def finish(error=None):
 if error:unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Stop')
 for c,state in paused:c.set_editor_property('pause_anims',state)
 p.set_actor_transform(original,False,True);unreal.unregister_slate_post_tick_callback(unreal._vgb1_review);del unreal._vgb1_review
 (folder/'Review.json').write_text(json.dumps({'rows':records,'error':error,'synthetic_images':False,'purpose':'Matched actual-game-camera review, not foot locomotion','quality':request.get('quality',2),'percentage':request.get('percentage',100)},indent=2))
def tick(dt):
 global current,stage,sent
 try:
  if current<0 and time.monotonic()-created<.6:return
  if (P/(label+'_Done.txt')).exists():finish();return
  f=P/(label+'_Segments.csv');index=0
  if f.exists():
   completed=list(csv.DictReader(f.open()));index=len(completed)
  if index>=len(rows):return
  if index!=current:
   current=index;stage=time.monotonic();sent=False;p.set_actor_location(unreal.Vector(*rows[current]['position']),False,True)
  if time.monotonic()-stage<5 or sent:return
  r=rows[current];path=folder/(str(current).zfill(2)+'_'+r['site']+'_'+r.get('tag',r['condition'].replace(':','_').replace('=','_'))+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(path)+'"',pc);cam=pc.player_camera_manager
  records.append({'request':str(path),'site':r['site'],'condition':r['condition'],'position':p.get_actor_location().to_tuple(),'camera_cm':cam.get_camera_location().to_tuple(),'camera_rotation':cam.get_camera_rotation().to_tuple(),'fov':cam.get_fov_angle(),'viewport':list(pc.get_viewport_size()),'map':w.get_path_name()});sent=True
 except Exception:finish(traceback.format_exc())
unreal._vgb1_review=unreal.register_slate_post_tick_callback(tick)
