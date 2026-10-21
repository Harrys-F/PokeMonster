"""Actual existing ClassicBattle presentation with runtime-only seeded starter fixtures."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/StarterPolishV2/EffectsPIE';O.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);s={'case':0,'phase':'start','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'rows':[],'wall':time.monotonic(),'fixture':'runtime QA only, existing ClassicBattle; no assets/save mutation'};cases=[('Schiggy','Bisasam',[2,0,1]),('Bisasam','Schiggy',[2,2])]
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def phase(v):s.update(phase=v,time=0.)
def finish(err=None):
 unreal.unregister_slate_post_tick_callback(unreal._polish_effects);s.update(passed=err is None,error=err);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<240
  own,other,slots=cases[s['case']]
  if s['phase']=='start'and s['time']>1:
   assert not e.is_encounter_active();cmd('pm.StarterReview.Party '+own+' '+other+' Zunderlauf');a,b,_=e.get_player_party();a.current_hp=max(1,a.current_hp-8);data=unreal.PokeMonsterEncounterStartData(presentation_mode=unreal.PokeMonsterBattlePresentationMode.CLASSIC_BATTLE,encounter_id='PolishEffects_'+own,kind=unreal.PokeMonsterEncounterKind.WILD,source=unreal.PokeMonsterEncounterSource.VISIBLE_CREATURE,player_team=[a],opponent_team=[b],random_seed=31,allow_flee=True);assert e.start_encounter(data,p);s['slot']=0;phase('choose')
  elif s['phase']=='choose'and s['time']>2:
   assert e.is_encounter_active();pr=e.get_presenter();view=pr.get_view()
   if view.busy:return
   assert not view.finished
   if s['slot']>=len(slots):phase('flee');return
   slot=slots[s['slot']];e.get_battle_widget().set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);cmd('Shot filename='+str(O/(own+'_MoveMenu_'+str(slot)+'.png')));assert pr.try_select_move(slot);assert pr.resolve_selection();s['rows'].append({'species':own,'slot':slot,'name':str(view.moves[slot].name),'events':[str(x.type)for x in pr.get_last_result().events]});phase('anim')
  elif s['phase']=='anim':
   if s['time']>.9 and not s.get('shot'):cmd('Shot filename='+str(O/(own+'_Effect_'+str(s['slot'])+'.png')));s['shot']=True
   if not e.get_presenter().get_view().busy and s['time']>2:s['slot']+=1;s['shot']=False;phase('choose')
  elif s['phase']=='flee':
   if not e.is_encounter_active():phase('returned');return
   pr=e.get_presenter();view=pr.get_view()
   if not view.busy and not view.finished:assert pr.try_select_flee();assert pr.resolve_selection()
  elif s['phase']=='returned'and s['time']>2 and not p.is_overworld_input_locked():
   s['case']+=1
   if s['case']==len(cases):
    assert any('SEED_DAMAGE'in x for row in s['rows']for x in row['events']),s['rows'];finish();return
   phase('start')
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._polish_effects=unreal.register_slate_post_tick_callback(tick)
