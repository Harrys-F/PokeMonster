"""Reproject map vegetation to actual reshaped terrain, no actor locations or gameplay edits."""
import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert not(D/'Reground.json').exists();assert json.loads((D/'Terrain.json').read_text())['passed'];actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();ignore=[a for a in actors if a.actor_has_tag('BiomePlayerWaterBarrier')];todo=[a for a in actors if a.get_actor_label().startswith(('WVU_','WEP_','WR_Grass','WR_MeadowHerbs'))];rows=[];i=0
# Trees/rocks ignore Visibility; all probes continue to land on the real terrain.
def job():
 for a in todo:
  c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
  if not c or not c.get_instance_count():continue
  b=c.static_mesh.get_bounding_box();maxdelta=0;a.modify()
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,True);p=t.translation;hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(p.x,p.y,p.z+6000),unreal.Vector(p.x,p.y,p.z-12000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE);assert hit,(a.get_actor_label(),i);match=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text());assert match;g=float(match[1]);embed=(b.max.z-b.min.z)*t.scale3d.z*.22 if a.get_actor_label().startswith('WEP_Boulders_')else .8;z=g-b.min.z*t.scale3d.z-embed;maxdelta=max(maxdelta,abs(z-p.z));t.translation=unreal.Vector(p.x,p.y,z);c.update_instance_transform(i,t,True,i==c.get_instance_count()-1,True)
  rows.append(dict(group=a.get_actor_label(),instances=c.get_instance_count(),max_z_adjustment_cm=maxdelta));yield
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'Reground.json').write_text(json.dumps(dict(passed=True,groups=rows),indent=2))
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wep_ground)
 except Exception:
  import traceback
  (D/'RegroundFailure.txt').write_text(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._wep_ground);unreal.log_error(traceback.format_exc())
 busy=False
unreal._wep_ground=unreal.register_slate_post_tick_callback(tick)
