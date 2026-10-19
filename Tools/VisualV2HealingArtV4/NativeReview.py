"""True native game camera photos; no benchmarking, no runtime art switches."""
import unreal,time,runpy,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV4';j=json.loads((S/'NativeReviewRequest.json').read_text());start=time.monotonic();stage=0;pending=None;proof=[]
def tick(dt):
 global stage,pending
 if time.monotonic()-start<20:return
 w=next((w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0)),None)
 if not w:return
 if stage>=2:
  (S/(f"NativeReview_Q{j['quality']}_{j['phase']}_Done.json")).write_text(json.dumps(proof,indent=2));unreal.unregister_slate_post_tick_callback(unreal._ha4_native_photo);unreal.SystemLibrary.execute_console_command(w,'quit');return
 width,height=[(1280,720),(2560,1440)][stage];label=f"Standalone_Q{j['quality']}_{j['phase']}_{width}_{height}"
 if pending is None:
  (S/'PhotoRequest.json').write_text(json.dumps({'label':label,'width':width,'height':height,'percentage':100,'quality':j['quality'],'mode':'Standalone','force_secondary_100':j.get('full100',False)}));runpy.run_path(str(R/'Tools/VisualV2HealingArtV4/Photos.py'),run_name='__main__');pending=label
 if (S/'Photos'/label/'Result.json').exists():proof.append({'label':label});stage+=1;pending=None
unreal._ha4_native_photo=unreal.register_slate_post_tick_callback(tick)
