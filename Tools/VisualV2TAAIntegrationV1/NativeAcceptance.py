import unreal,time,runpy,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2TAAIntegrationV1';begin=time.monotonic();started=False
request=json.loads((S/'AcceptanceRequest.json').read_text());done=S/'Acceptance'/request['label']/'FootTest.json'
def tick(dt):
 global started
 if not started and time.monotonic()-begin>20 and any(w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0) for w in unreal.ObjectIterator(unreal.World)):
  started=True;runpy.run_path(str(R/'Tools/VisualV2TAAIntegrationV1/StartAcceptance.py'),run_name='__main__')
 if done.exists():
  unreal.unregister_slate_post_tick_callback(unreal._taa_native_acceptance)
  w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));unreal.SystemLibrary.execute_console_command(w,'quit')
unreal._taa_native_acceptance=unreal.register_slate_post_tick_callback(tick)
