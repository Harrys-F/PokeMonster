"""Runtime-only isolated representation tests. Never save the map or change lights/PP/camera.
The existing probe owns resolution, quality, fixed camera positions, counters and restoration.
"""
import unreal,json,csv,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';j=json.loads((S/'StudyRequest.json').read_text());label=j['label'];plan=R/'Tools/VisualV2WorldArtQualityV2/Plans'/(label+'.tsv');rows=list(csv.reader(plan.open(),delimiter='\t'))[1:];P=R/'Saved/EnvironmentPerfV2';assert not (P/(label+'_Done.txt')).exists()
w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));groups=[];individual=[];proof=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 if not a.get_actor_label().startswith('WAQ1_'):continue
 c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c and not c.cast_shadow and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
 transforms=[c.get_instance_transform(i,True) for i in range(c.get_instance_count())];groups.append((c,c.is_visible(),c.forced_lod_model,transforms))
unreal.SystemLibrary.execute_console_command(w,'pm.WorldArt2.Prepare')
individual=[(a,a.static_mesh_component) for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if 'WAQ2_TransientIndividual' in [str(t) for t in a.tags]]
assert len(groups)==6 and len(individual)==175
current=-1;last_poll=0.;start=time.monotonic();photo=j.get('photo',False)
def apply(index):
 global current
 factor=rows[index][1];assert factor in ['WAQ2:HISM','WAQ2:Individual','WAQ2:No175','WAQ2:HISM_LOD0','WAQ2:Individual_LOD0']
 unreal.SystemLibrary.execute_console_command(w,'pm.WorldArt2.Mode '+factor.split(':')[1])
 proof.append({'segment':index,'factor':factor,'applied_wall':time.time(),'hism_components_visible':sum(c.is_visible() for c,_,_,_ in groups),'individual_components_visible':sum(c.is_visible() for _,c in individual),'original_instance_count':sum(len(x[3]) for x in groups),'lights_and_pp_changed':False});(S/(label+'_VariantProof.json')).write_text(json.dumps(proof,indent=2));current=index
apply(0);unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"')
def tick(dt):
 global last_poll
 if time.monotonic()-last_poll<.1:return
 last_poll=time.monotonic()
 try:
  if (P/(label+'_Done.txt')).exists():
   for c,visible,lod,_ in groups:c.set_visibility(visible);c.set_forced_lod_model(lod)
   for actor,c in individual:c.set_visibility(False)
   unreal.unregister_slate_post_tick_callback(unreal._waq2_study);return
  f=P/(label+'_Segments.csv');n=len(list(csv.DictReader(f.open()))) if f.exists() else 0
  if n!=current and n<len(rows):apply(n)
 except Exception:
  (S/(label+'_Error.txt')).write_text(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._waq2_study);raise
unreal._waq2_study=unreal.register_slate_post_tick_callback(tick)
