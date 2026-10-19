import unreal,json,time,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2ShadowQualityV8';config=json.loads((R/'Art/World/VisualV2ShadowQualityV8/Variants.json').read_text());start=time.monotonic();state={'i':0,'pending':False,'rows':[]}
def tick(dt):
 if time.monotonic()-start<20:return
 w=next((x for x in unreal.ObjectIterator(unreal.World) if x.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(x,0)),None)
 if not w:return
 i=state['i']
 if i==3:
  unreal.unregister_slate_post_tick_callback(unreal._sv8_native);(S/'NativeABC_Done.json').write_text(json.dumps(state['rows'],indent=2));unreal.SystemLibrary.execute_console_command(w,'quit');return
 variant=['A','B','C'][i];label='Standalone_'+variant
 if not state['pending']:
  (S/'VariantRequest.json').write_text(json.dumps(config[variant]));runpy.run_path(str(R/'Tools/VisualV2ShadowQualityV8/RuntimeVariant.py'),run_name='__main__');(S/'PhotoRequest.json').write_text(json.dumps({'label':label,'width':2560,'height':1440,'percentage':100,'quality':1,'variant':config[variant]}));runpy.run_path(str(R/'Tools/VisualV2ShadowQualityV8/Photos.py'),run_name='__main__');state['pending']=True
 if (S/'Photos'/label/'Result.json').exists():state['rows'].append({'label':label});state['i']+=1;state['pending']=False
unreal._sv8_native=unreal.register_slate_post_tick_callback(tick)
