"""Interleaved V1/Merged/V2 at identical probe poses. No saved actor/asset changes."""
import unreal,json,csv,time,traceback,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';sys.path.insert(0,str(R/'Tools/VisualV2WorldArtQualityV2'));from RuntimeVariants import Variants
j=json.loads((S/'StudyRequest.json').read_text());label=j['label'];plan=R/'Tools/VisualV2WorldArtQualityV2/Plans'/(label+'.tsv');rows=list(csv.reader(plan.open(),delimiter='\t'))[1:];P=R/'Saved/EnvironmentPerfV2';assert not (P/(label+'_Done.txt')).exists();w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));v=Variants(w);proof=[];current=-1;last=0.
def apply(index):
 global current
 mode=rows[index][1].split(':')[1];v.apply(mode);current=index;proof.append({'segment':index,'mode':mode,'site':rows[index][0],'applied_wall':time.time(),'six_groups':len(v.groups),'instances':sum(c.get_instance_count() for _,c in v.groups),'slots':sum(c.get_num_materials() for _,c in v.groups),'pp_and_light_settings_unchanged':True});(S/(label+'_VariantProof.json')).write_text(json.dumps(proof,indent=2))
apply(0);unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"')
def tick(dt):
 global last
 if time.monotonic()-last<.1:return
 last=time.monotonic()
 try:
  if (P/(label+'_Done.txt')).exists():v.apply('V1');unreal.unregister_slate_post_tick_callback(unreal._waq2_matrix);return
  f=P/(label+'_Segments.csv');index=len(list(csv.DictReader(f.open()))) if f.exists() else 0
  if index!=current and index<len(rows):apply(index)
 except Exception:
  (S/(label+'_Error.txt')).write_text(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._waq2_matrix);raise
unreal._waq2_matrix=unreal.register_slate_post_tick_callback(tick)
