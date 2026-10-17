"""Scoped map-component factors for explicit probe plans. No assets or editor-world objects changed."""
import unreal,json,csv,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV1';req=json.loads((O/'Request.json').read_text());label=req['plan'];plan=(R/'Tools/EnvironmentPerfV1/Plans'/(label+'.tsv')).read_text().splitlines();rows=[r.split('\t') for r in plan[1:] if r];w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
trees=[];small=[];volumes=[]
for c in unreal.ObjectIterator(unreal.StaticMeshComponent):
 if c.get_world()!=w or not c.static_mesh:continue
 n=c.static_mesh.get_name()
 if n.startswith('SM_WLA_') and any(k in n for k in ['Oak','Birch']):trees.append((c,c.get_editor_property('bOverrideMinLOD'),c.get_editor_property('min_lod')))
 if isinstance(c,unreal.InstancedStaticMeshComponent) and n.startswith('SM_WLA_') and any(k in n for k in ['Grass','Fern','Wildflowers','Herb']):small.append((c,c.get_editor_property('instance_start_cull_distance'),c.get_editor_property('instance_end_cull_distance')))
for v in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume):
 if v.get_editor_property('unbound'):
  s=v.get_editor_property('settings');names=['override_motion_blur_amount','motion_blur_amount','override_lumen_final_gather_quality','lumen_final_gather_quality','override_bloom_intensity','bloom_intensity'];volumes.append((v,{n:s.get_editor_property(n) for n in names}))
current=-1;created=time.monotonic();events=[]
def restore():
 for c,override,lod in trees:c.set_editor_property('bOverrideMinLOD',override);c.set_editor_property('min_lod',lod)
 for c,a,b in small:c.set_cull_distances(a,b)
 for v,values in volumes:
  s=v.get_editor_property('settings')
  for n,val in values.items():s.set_editor_property(n,val)
  v.set_editor_property('settings',s)
def finish(error=None):
 restore();unreal.unregister_slate_post_tick_callback(unreal._envperf_factors);del unreal._envperf_factors
 (O/(label+'_SceneFactors.json')).write_text(json.dumps({'events':events,'error':error,'tree_components':len(trees),'small_foliage_groups':len(small)},indent=2))
def tick(dt):
 global current
 try:
  if (O/(label+'_Done.txt')).exists():finish();return
  if time.monotonic()-created<.6:return
  f=O/(label+'_Segments.csv');i=len(list(csv.DictReader(f.open()))) if f.exists() else 0
  if i>=len(rows) or i==current:return
  current=i;restore();condition=rows[i][1];factors=req.get('candidate',[]) if condition=='Candidate' else [condition]
  if 'TreeMinLOD1' in factors:
   for c,_,_ in trees:c.set_editor_property('bOverrideMinLOD',True);c.set_editor_property('min_lod',1)
  if 'SmallFoliageCull' in factors:
   for c,_,_ in small:c.set_cull_distances(3200,4300)
  for v,_ in volumes:
   s=v.get_editor_property('settings')
   for factor,override,key,value in [('MotionBlurOff','override_motion_blur_amount','motion_blur_amount',0.0),('GIFinalGatherHalf','override_lumen_final_gather_quality','lumen_final_gather_quality',.5),('BloomOff','override_bloom_intensity','bloom_intensity',0.0)]:
    if factor in factors:s.set_editor_property(override,True);s.set_editor_property(key,value)
   v.set_editor_property('settings',s)
  events.append({'segment':i,'site':rows[i][0],'condition':condition,'applied':factors,'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
 except Exception:
  unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf.Stop');finish(traceback.format_exc())
unreal._envperf_factors=unreal.register_slate_post_tick_callback(tick)
