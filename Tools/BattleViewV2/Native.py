"""Standalone development-game startup. No editor/package/save mutations."""
import unreal,time,runpy,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();request=json.loads((R/'Saved/BattleViewV2/ReviewRequest.json').read_text());begin=time.monotonic();started=False;result=R/'Saved/BattleViewV2'/request['label']/'Result.json'
def tick(dt):
 global started
 if not started and time.monotonic()-begin>20 and any(w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)for w in unreal.ObjectIterator(unreal.World)):
  started=True;runpy.run_path(str(R/'Tools/BattleViewV2/Review.py'),run_name='__main__')
 if result.exists():
  unreal.unregister_slate_post_tick_callback(unreal._battle_v2_native);w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));unreal.SystemLibrary.execute_console_command(w,'quit')
unreal._battle_v2_native=unreal.register_slate_post_tick_callback(tick)
