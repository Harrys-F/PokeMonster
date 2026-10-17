"""Matched shadow-only AB/BA/AB pairs using existing native timing probe. No code changes.
The probe's built-in V1 CVars are explicitly overridden to the audited VisualV2
renderer values on EVERY row, identically for original and proxy shadows.
"""
import unreal,json,time,csv,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/TreeShadowProxyV1';N=R/'Saved/EnvironmentPerfV2';request=json.loads((O/'BenchmarkRequest.json').read_text());label=request['label'];assert not (N/(label+'_Done.txt')).exists()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and unreal.GameplayStatics.get_current_level_name(w,True)=='Dev_TestMap_TreeShadowProxyV1'
actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor);trees=[next(a for a in actors if a.get_actor_label()=='V2_ForestOak_'+str(i)).static_mesh_component for i in range(3)];proxies=[a.static_mesh_component for a in actors if a.get_actor_label().startswith('TSP_V2_ForestOak_')];assert len(proxies)==6
snap=[(c,c.cast_shadow) for c in trees+proxies];paused=[(c,c.get_editor_property('pause_anims')) for c in unreal.ObjectIterator(unreal.SkeletalMeshComponent) if c.get_world()==w]
for c,_ in paused:c.set_editor_property('pause_anims',True)
rows=[]
for wi,he,q,sp in [request['config']]:
 for rep,order in [(1,['A','B']),(2,['B','A']),(3,['A','B'])]:
  for state in order:rows.append({'state':state,'repeat':rep,'width':wi,'height':he,'quality':q,'percentage':sp})
condition='CV:r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor=1|r.Shadow.Virtual.SMRT.RayCountDirectional=8|r.Lumen.FinalGatherMethod=1|r.Lumen.HardwareRayTracing=1'
plan=O/(label+'.tsv');assert not plan.exists();plan.write_text(label+'\tPIE\t10\t10\n'+'\n'.join('\t'.join(map(str,['Wald',condition,r['repeat'],r['width'],r['height'],r['quality'],r['percentage']])) for r in rows)+'\n');(O/(label+'_Rows.json')).write_text(json.dumps(rows,indent=2))
current=-1;events=[];started=time.monotonic()
def setstate(state):
 for c in trees:c.set_cast_shadow(state=='A')
 for c in proxies:c.set_cast_shadow(state=='B');assert c.get_editor_property('hidden_in_game') and c.get_editor_property('cast_hidden_shadow') and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
def finish(error=None):
 if error:unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Stop')
 for c,b in snap:c.set_cast_shadow(b)
 for c,b in paused:c.set_editor_property('pause_anims',b)
 unreal.unregister_slate_post_tick_callback(unreal._tree_benchmark);del unreal._tree_benchmark
 (O/(label+'_Control.json')).write_text(json.dumps({'events':events,'error':error,'seconds':time.monotonic()-started,'states_restored':True,'only_visual_shadow_flags_toggled':True},indent=2))
def tick(dt):
 global current
 try:
  if (N/(label+'_Done.txt')).exists():finish();return
  f=N/(label+'_Segments.csv');idx=len(list(csv.DictReader(f.open()))) if f.exists() else 0
  if idx>=len(rows):return
  # Native probe restores its initial component state at each row boundary.
  # Reapply the requested shadow state during warm-up, and verify every frame.
  setstate(rows[idx]['state'])
  if idx!=current:
   current=idx;events.append({'segment':idx,'row':rows[idx],'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'elapsed':time.monotonic()-started,'original_shadow':[bool(c.cast_shadow) for c in trees],'proxy_shadow':[bool(c.cast_shadow) for c in proxies]});(O/'Progress.json').write_text(json.dumps(events,indent=2))
 except Exception:finish(traceback.format_exc())
setstate('A');unreal._tree_benchmark=unreal.register_slate_post_tick_callback(tick)
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"')
