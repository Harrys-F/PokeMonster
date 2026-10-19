"""Actual standalone screenshots, outside all timing windows; no synthetic scene captures."""
import unreal,time,runpy,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';sys.path.insert(0,str(R/'Tools/VisualV2WorldArtQualityV2'));from RuntimeVariants import Variants
j=json.loads((S/'NativeReviewRequest.json').read_text());start=time.monotonic();stage=0;pending=None;variants=None;configs=[('V1',1280,720),('V2',1280,720),('V1',2560,1440),('V2',2560,1440)];proof=[]
def tick(dt):
 global stage,pending,variants
 if time.monotonic()-start<20:return
 w=next((w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0)),None)
 if not w:return
 if variants is None:variants=Variants(w)
 if stage>=len(configs):
  variants.apply('V1');(S/('NativeReview_Q'+str(j['quality'])+'_Done.json')).write_text(json.dumps(proof,indent=2));unreal.unregister_slate_post_tick_callback(unreal._waq2_native_photo);unreal.SystemLibrary.execute_console_command(w,'quit');return
 mode,width,height=configs[stage];label=f"Standalone_Q{j['quality']}_{mode}_{width}_{height}"
 if pending is None:
  variants.apply(mode);(S/'PhotoRequest.json').write_text(json.dumps({'label':label,'width':width,'height':height,'percentage':100,'quality':j['quality'],'mode':'Standalone'}));runpy.run_path(str(R/'Tools/VisualV2WorldArtQualityV2/Photos.py'),run_name='__main__');pending=label
 if (S/'Photos'/label/'Result.json').exists():proof.append({'label':label,'images':str(S/'Photos'/label),'quality':j['quality'],'mode':mode,'width':width,'height':height});stage+=1;pending=None
unreal._waq2_native_photo=unreal.register_slate_post_tick_callback(tick)
