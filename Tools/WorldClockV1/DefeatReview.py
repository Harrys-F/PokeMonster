"""Existing real WorldBattle + defeat recovery: no time jump or manual-slot rewrite.
Fresh ordinary PIE, isolated storage, existing developer battle fixture only.
"""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WorldClockV1';O=D/'Defeat01';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
Clock=sub(unreal.PokeMonsterWorldClock);Save=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);CP=sub(unreal.PokeMonsterCheckpointSubsystem)
assert Save.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_WorldClockV1Defeat01')
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def absolute():t=Clock.get_time();return(t.day-1)*86400+t.seconds_of_day
P.set_actor_location(unreal.Vector(-200,-100,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
s={'stage':'setup','wall':time.monotonic(),'last':time.monotonic()};result={'checks':[],'isolated_slot':True,'existing_battle_fixture':True,'map_saved':False}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._clock_defeat);result.update(passed=error is None,error=error,final_time=Clock.get_time().export_text());(O/'Result.json').write_text(json.dumps(result,indent=2))
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<90,'Defeat timeout'
  if s['stage']=='setup':
   if time.monotonic()-s['wall']<1:return
   cmd('pm.WorldClock set 6 17 30');cmd('pm.WorldClock reset');assert Save.save_current_game();s['checkpoint']=CP.get_active_checkpoint().export_text();s['file']=R/'Saved/SaveGames/PokeMonster_SaveV2_Test_WorldClockV1Defeat01.sav';s['hash']=hashlib.sha256(s['file'].read_bytes()).hexdigest();cmd('pm.BattleV3.Start world defeat');assert E.is_encounter_active();s['battle_time']=absolute();s['stage']='battle';return
  if E.is_encounter_active():
   assert Clock.is_clock_paused()and absolute()==s['battle_time'],'WorldBattle time progressed'
   v=E.get_presenter().get_view()
   if not v.busy and not v.finished:assert E.get_presenter().try_select_move(0);assert E.get_presenter().resolve_selection()
   return
  if P.is_overworld_input_locked()or CP.is_returning_from_defeat():return
  assert E.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.DEFEAT
  assert CP.was_last_recovery_saved()and Save.has_recovery_game()
  assert hashlib.sha256(s['file'].read_bytes()).hexdigest()==s['hash'],'Manual save changed'
  assert CP.get_active_checkpoint().export_text()==s['checkpoint']
  assert 0<=absolute()-s['battle_time']<30,'Defeat jumped clock'
  assert not Clock.is_clock_paused()
  result['checks']=['Existing WorldBattle pauses clock without battle changes','Actual defeat recovery saves separate isolated recovery slot','No clock jump on defeat','Manual save hash and independent checkpoint unchanged','Clock resumes after recovery'];finish()
 except Exception:finish(traceback.format_exc())
unreal._clock_defeat=unreal.register_slate_post_tick_callback(tick)
