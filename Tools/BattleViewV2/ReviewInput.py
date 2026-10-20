"""Nintendo-layout logical gamepad events through real Slate routing, not hardware certification."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();request=json.loads((R/'Saved/BattleViewV2/InputRequest.json').read_text())if(R/'Saved/BattleViewV2/InputRequest.json').exists()else{};label=request.get('label','Input02');assert label.isalnum();O=R/'Saved/BattleViewV2'/label;O.mkdir(exist_ok=False)
w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi);assert not enc.is_encounter_active()
steps=[('Focus','COMMANDS'),('A','MOVES'),('B','COMMANDS'),('Down','COMMANDS'),('A','BAG'),('B','COMMANDS'),('Right','COMMANDS'),('A','TEAM'),('B','COMMANDS'),('Down','COMMANDS'),('Right','COMMANDS'),('A','COMMANDS'),('Focus','COMMANDS'),('A','MOVES'),('A','BUSY')]
s={'phase':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'index':0,'events':[],'rounds':0}
def cmd(x):unreal.SystemLibrary.execute_console_command(w,x)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._battle_v2_input);s.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now
  if s['phase']==0:
   cmd('pm.CreatureReview.Start classic meadow');assert enc.is_encounter_active();s.update(phase=1,t=0.)
  elif s['phase']==1 and s['t']>2:
   key,expected=steps[s['index']];cmd('pm.BattleView2.Input '+key);s.update(phase=2,t=0.)
  elif s['phase']==2 and s['t']>.3:
   key,expected=steps[s['index']];widget=enc.get_battle_widget();view=enc.get_presenter().get_view();got='BUSY'if view.busy else str(widget.get_battle_menu()).split('.')[1].split(':')[0];s['events'].append({'key':key,'expected':expected,'actual':got,'round':view.round});assert got==expected,s['events'][-1]
   if s['index']==11:assert view.round==0;cmd('pm.CreatureReview.CaptureLiveUI BattleV2_FleeInformational_'+label)
   s['index']+=1;s.update(phase=3 if s['index']==len(steps)else 1,t=1.7)
  elif s['phase']==3:
   if enc.is_encounter_active():
    pr=enc.get_presenter();view=pr.get_view()
    if not view.busy and not view.finished and s['t']>1:
     assert enc.get_battle_widget().get_battle_menu()==unreal.PokeMonsterBattleMenu.COMMANDS
     assert enc.get_battle_widget().get_command_button(0).has_keyboard_focus(),'Root focus not restored'
     if not s.get('native_second_round'):
      cmd('pm.BattleView2.Input A');cmd('pm.BattleView2.Input Right');cmd('pm.BattleView2.Input A');s['native_second_round']=True
     else:assert pr.try_select_move(0);assert pr.resolve_selection()
     s['rounds']+=1;s['t']=0
   else:finish()
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._battle_v2_input=unreal.register_slate_post_tick_callback(tick)
