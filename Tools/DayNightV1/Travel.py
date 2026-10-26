"""Real OpenLevel round trip: one clock, no lighting controller outside VisualV2."""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/DayNightV1/Travel02';O.mkdir(exist_ok=False);Editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=Editor.get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);Clock=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI)
unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock pause');unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock set 11 22 0');expected=Clock.get_time().export_text();unreal.GameplayStatics.get_player_pawn(W,0).set_overworld_input_locked(True);del W
s={'stage':0,'wall':time.monotonic(),'stable':None};result={'checks':[],'maps':[],'clock':expected}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._daynight_travel);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2))
 for n in ['GI','Clock','Editor']:globals().pop(n,None)
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<150,'Travel timeout';world=Editor.get_game_world()
  if not world:return
  if s['stage']==0:s['stage']=1;unreal.GameplayStatics.open_level(world,'/Game/Maps/Dev_TestMap');return
  target='Dev_TestMap'if s['stage']==1 else'Dev_TestMap_VisualV2'
  if not world.get_name().endswith(target)or not unreal.GameplayStatics.get_player_pawn(world,0):return
  unreal.GameplayStatics.get_player_pawn(world,0).set_overworld_input_locked(True)
  if s['stable']is None:s['stable']=time.monotonic();return
  if time.monotonic()-s['stable']<2:return
  assert unreal.GameplayStatics.get_game_instance(world)==GI and Clock.get_time().export_text()==expected and Clock.is_clock_paused()
  cycle=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if x.get_outer()==world)
  ownsky=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.StaticMeshActor)if a.get_name()=='VisualV2_DayNightSky']
  if s['stage']==1:
   assert not cycle.is_cycle_enabled()and not ownsky;result['checks'].append('Other existing map has neither active cycle nor added sky; exact world clock preserved')
   result['maps'].append(world.get_name());s.update(stage=2,stable=None);unreal.GameplayStatics.open_level(world,'/Game/Maps/Dev_TestMap_VisualV2');return
  assert cycle.is_cycle_enabled()and cycle.is_sky_ready()and len(ownsky)==1 and cycle.get_lighting_sample().stars>.99
  result['maps'].append(world.get_name());result['checks'].append('Return to VisualV2 immediately restores night lighting from unchanged shared clock')
  unreal.SystemLibrary.execute_console_command(world,'pm.WorldClock reset');assert not Clock.is_clock_paused();unreal.GameplayStatics.get_player_pawn(world,0).set_overworld_input_locked(False);result['checks'].append('Clock resumes after loading and normal player control restored');finish()
 except Exception:finish(traceback.format_exc())
unreal._daynight_travel=unreal.register_slate_post_tick_callback(tick)
