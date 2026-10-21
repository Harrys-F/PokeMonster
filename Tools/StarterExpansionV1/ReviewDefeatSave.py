"""Actual PIE defeat -> return -> autosave -> reload. Runner preserves the developer slot."""
import unreal,json,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/StarterExpansionV1/DefeatSaveRequest.json').read_text())['label'];assert label.isalnum();O=R/'Saved/StarterExpansionV1'/label;assert O.exists()and not(O/'Result.json').exists()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==gi)
e=sub(unreal.PokeMonsterEncounterSubsystem);c=sub(unreal.PokeMonsterCheckpointSubsystem);save=sub(unreal.PokeMonsterSaveSubsystem);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
# This is a valid current-world return point, not an asset or permanent checkpoint edit.
start=p.get_actor_location();site=unreal.PokeMonsterCheckpointData(checkpoint_id='ExplicitStarterSaveReturn',map_package='/Game/Maps/Dev_TestMap_VisualV2',location=start,rotation=p.get_actor_rotation());assert c.restore_checkpoint(site)
s={'phase':'start','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'position_before':start.to_tuple()}
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._starter_defeat);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);s.update(passed=error is None,error=error,save_after_sha256=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('STARTER_DEFEAT_DONE '+str(error))
def phase(v):s.update(phase=v,time=0.)
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<180
  if s['phase']=='start'and s['time']>1:
   cmd('pm.BattleV3.Start classic defeat');assert e.is_encounter_active();assert not save.save_current_game();s['battle_save_blocked']=True;phase('fight')
  elif s['phase']=='fight':
   if e.is_encounter_active():
    pr=e.get_presenter();v=pr.get_view()
    if not v.busy and not v.finished:assert pr.try_select_move(0);assert pr.resolve_selection()
   else:phase('return')
  elif s['phase']=='return'and not p.is_overworld_input_locked()and s['time']>1:
   assert e.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.DEFEAT;assert c.was_last_recovery_saved();team=e.get_player_party();assert all(x.current_hp==x.calculated_stats.max_hp for x in team);s['position_returned']=p.get_actor_location().to_tuple();assert p.get_actor_location().distance(start)<5;s['saved']=True;s['team_before_reload']=[{'id':x.instance_id.to_string(),'hp':x.current_hp,'xp':x.experience}for x in team];assert save.load_game();after=e.get_player_party();assert s['team_before_reload']==[{'id':x.instance_id.to_string(),'hp':x.current_hp,'xp':x.experience}for x in after];assert str(c.get_active_checkpoint().checkpoint_id)=='ExplicitStarterSaveReturn';s['reload_equal']=True;cmd('pm.CreatureReview.CaptureLiveUI StarterDefeatSave_Returned');finish()
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._starter_defeat=unreal.register_slate_post_tick_callback(tick)
