"""Actual PIE OpenLevel round trip between two existing maps; no map/save writes."""
import unreal,json,time,traceback,gc
from pathlib import Path
# Release completed Python runner cycles before Unreal begins map/GC teardown.
gc.collect()
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WorldClockV1';req=json.loads((D/'Request.json').read_text());O=D/req.get('travel_label','Travel02');O.mkdir(exist_ok=False);Editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=Editor.get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);Clock=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI)
Save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI)
if not req.get('reuse_review_slot',False):assert Save.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_WorldClockV1'+req.get('travel_label','Travel02'))
def cmd(t):unreal.SystemLibrary.execute_console_command(Editor.get_game_world(),t)
cmd('pm.WorldClock set 11 18 30');cmd('pm.WorldClock pause');cmd('pm.WorldClock speed 5');expected=Clock.get_time().export_text();s={'stage':0,'wall':time.monotonic(),'stable':None};result={'checks':[],'same_game_instance':True,'clock':expected,'debug_speed':5,'maps':[]}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._clock_travel);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('WORLD_CLOCK_TRAVEL_DONE '+str(error))
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<120,'Travel timeout';world=Editor.get_game_world()
  if not world:return
  name=world.get_name();pc=unreal.GameplayStatics.get_player_controller(world,0);pawn=unreal.GameplayStatics.get_player_pawn(world,0)
  if s['stage']==0:
   s['stage']=1;unreal.GameplayStatics.open_level(world,'/Game/Maps/Dev_TestMap');return
  target='Dev_TestMap'if s['stage']==1 else'Dev_TestMap_VisualV2'
  if not name.endswith(target)or not pc or not pawn:return
  if s['stable']is None:s['stable']=time.monotonic();return
  if time.monotonic()-s['stable']<1:return
  assert unreal.GameplayStatics.get_game_instance(world)==GI
  assert Clock.get_time().export_text()==expected,(name,Clock.get_time().export_text(),expected)
  assert Clock.get_debug_speed()==5 and Clock.is_clock_paused();result['maps'].append(name)
  result['checks'].append('Same authority, exact time, day and runtime speed after '+name)
  if s['stage']==1:
   s.update(stage=2,stable=None);unreal.GameplayStatics.open_level(world,'/Game/Maps/Dev_TestMap_VisualV2');return
  # Reset is a test control, not a load/reset of the persistent clock.
  cmd('pm.WorldClock reset');assert not Clock.is_clock_paused();result['checks'].append('Clock resumes after both real loading transitions');finish()
 except Exception:finish(traceback.format_exc())
unreal._clock_travel=unreal.register_slate_post_tick_callback(tick)
