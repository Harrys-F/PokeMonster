"""Manual native keyboard input gate: focus a real battle button, then observe its actual round."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/GlumandaV11/ButtonInput';O.mkdir(exist_ok=False);w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi);assert not enc.is_encounter_active();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False);s={'phase':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'manual_button_passed':False}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._glumanda_button_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);s.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now
  if s['phase']==0 and s['t']>2:
   s['position_before']=p.get_actor_location().to_tuple();unreal.SystemLibrary.execute_console_command(w,'pm.CreatureReview.Start classic',pc);s.update(phase=1,t=0.)
  elif s['phase']==1 and s['t']>3:
   enc.get_battle_widget().get_attack_button(0).set_keyboard_focus();(O/'ReadyForKeyboard.json').write_text(json.dumps({'action':'press Space on foreground Unreal window','round_before':enc.get_presenter().get_view().round}));s.update(phase=2,t=0.)
  elif s['phase']==2:
   view=enc.get_presenter().get_view()
   if view.round>0 and not view.busy:
    assert view.opponent.current_hp<view.opponent.max_hp;s.update(manual_button_passed=True,phase=3,t=0.,round_after_native_button=view.round);unreal.SystemLibrary.execute_console_command(w,'pm.CreatureReview.CaptureLiveUI NativeButtonRound1',pc)
   assert s['t']<100,'No native button input observed'
  elif s['phase']==3:
   if enc.is_encounter_active():
    pr=enc.get_presenter();v=pr.get_view()
    if not v.busy and not v.finished and s['t']>.7:assert pr.try_select_move(0);assert pr.resolve_selection();s['t']=0
   else:assert not p.is_overworld_input_locked();assert math.dist(s['position_before'],p.get_actor_location().to_tuple())<.01;finish()
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._glumanda_button_review=unreal.register_slate_post_tick_callback(tick)
