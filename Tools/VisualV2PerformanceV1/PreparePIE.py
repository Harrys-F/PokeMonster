"""Arm one early PIE setup; no scene save, no user slot writes."""
import unreal,time,json,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';started=time.monotonic()
def prepare_inner(dt):
 E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world()
 if not W:
  if time.monotonic()-started>90:unreal.unregister_slate_post_tick_callback(unreal._perf1_prepare)
  return
 P=unreal.GameplayStatics.get_player_pawn(W,0)
 if not P:return
 GI=unreal.GameplayStatics.get_game_instance(W);S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI)
 assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_PerfOptimization01');unreal._perf1_isolated=True
 unreal._perf1_profiles={a.get_name():a.profile.get_path_name()if a.profile else None for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)}
 for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.set_editor_property('profile',None)
 P.set_actor_location(unreal.Vector(-300,2100,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
 E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI)
 (D/'EarlyPIE.json').write_text(json.dumps({'position':P.get_actor_location().to_tuple(),'encounter':E.is_encounter_active(),'isolated':True,'wall':time.time()}))
 unreal.unregister_slate_post_tick_callback(unreal._perf1_prepare)
def prepare(dt):
 try:prepare_inner(dt)
 except Exception:
  import traceback
  unreal.unregister_slate_post_tick_callback(unreal._perf1_prepare)
  (D/'EarlyPIEError.txt').write_text(traceback.format_exc());unreal.log_error(traceback.format_exc())
unreal._perf1_prepare=unreal.register_slate_post_tick_callback(prepare)
