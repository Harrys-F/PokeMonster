"""Standalone using one own PIE-produced fixture in an isolated built-in UserDir."""
import unreal,json,time,runpy,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';q=json.loads((D/'NativeRequest.json').read_text());DATA=Path(unreal.Paths.project_saved_dir()).resolve();assert DATA.is_relative_to(D/q['label']/'UserData');start=time.monotonic();state={'loaded':False}
def tick(dt):
 worlds=[]
 try:
  if time.monotonic()-start<12:return
  worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)]
  if not worlds:return
  W=worlds[0];GI=unreal.GameplayStatics.get_game_instance(W);S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);C=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI);assert not E.is_encounter_active()
  for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.set_editor_property('profile',None)
  if not state['loaded']:assert S.load_game();state['loaded']=True;return
  if S.is_load_in_progress():return
  assert C.get_hour()==12 and C.get_real_minutes_per_day()==120
  unreal._perf1_isolated=True;unreal.unregister_slate_post_tick_callback(unreal._perf1_native_start);(D/'Request.json').write_text(json.dumps(q));runpy.run_path(str(R/'Tools/VisualV2PerformanceV1/Benchmark.py'),run_name='__main__')
 except Exception:
  unreal.unregister_slate_post_tick_callback(unreal._perf1_native_start);O=D/q['label'];O.mkdir(exist_ok=True);(O/'StartupError.txt').write_text(traceback.format_exc());unreal.log_error(traceback.format_exc());unreal.SystemLibrary.quit_game(worlds[0]if worlds else None,None,unreal.QuitPreference.QUIT,False)
unreal._perf1_native_start=unreal.register_slate_post_tick_callback(tick)
