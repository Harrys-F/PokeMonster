"""All fifteen actual new moves, unchanged ClassicBattle and five WorldBattle paths. Technical runtime stats."""
from pathlib import Path
import unreal,json,time,traceback
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/LearnMovesV1';q=json.loads((D/'Request.json').read_text());O=D/q['label'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_'+q['label'])
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True);a.set_actor_enable_collision(False)
plan=json.loads((R/'Tools/LearnMovesV1/Plan.json').read_text());cases=[];seen=set()
for row in plan['rows']:
 species=next(x['species']for x in plan['bindings']if x['id']==row['id']);cases.append(dict(id=row['id'],species=species,mode='classic'))
for c in list(cases):
 if c['species']not in seen:cases.append(dict(c,mode='world'));seen.add(c['species'])
assert len(cases)==20
s={'case':0,'phase':'start','t':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'wall':time.monotonic()};result={'cases':[],'technical_fixture':True,'physical_controller_test':False};live={}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def phase(p):s.update(phase=p,t=0.)
def shot(n):cmd('pm.CreatureReview.CaptureLiveUI LearnProduction'+q['label']+str(s['case'])+n)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._learn_production);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
def choose():
 pr=live['pr'];assert pr.try_select_move(0);assert pr.resolve_selection()
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<800;c=cases[s['case']]
  if s['phase']=='start'and s['t']>.5:
   assert not E.is_encounter_active()and not P.is_overworld_input_locked();cmd('pm.CrystalMoves.Start '+c['mode']+' '+c['id']+' '+c['species']+' 71');assert E.is_encounter_active();live['pr']=E.get_presenter();result['cases'].append(dict(c,rounds=[],position=P.get_actor_location().to_tuple()));phase('ready')
  elif s['phase']=='ready'and s['t']>1:
   assert E.get_battle_widget().is_classic_presentation()==(c['mode']=='classic');v=live['pr'].get_view();assert not v.busy;result['cases'][-1]['pp_before']=v.moves[0].current_pp;shot('Before');choose();phase('attack')
  elif s['phase']=='attack':
   pr=live['pr'];v=pr.get_view();row=result['cases'][-1];r=pr.get_last_result()
   if v.round>len(row['rounds'])and r.succeeded:
    events=[dict(type=str(e.type),source=str(e.source),move=str(e.move_id),damage=e.damage,pp_before=e.pp_before,pp_after=e.pp_after,text=str(e.information))for e in r.events];row['rounds'].append(dict(round=v.round,events=events))
    if len(row['rounds'])==1:
     assert any('MOVE_EXECUTED'in e['type']and c['id']in e['move']and '.A:'in e['source']for e in events),(c,events);assert v.moves[0].current_pp==row['pp_before']-1;shot('After')
   if not E.is_encounter_active():phase('ended')
   elif not v.busy and not v.finished:phase('flee')
  elif s['phase']=='flee'and s['t']>.5:
   pr=live['pr']
   if not E.is_encounter_active():phase('ended');return
   if pr.try_select_flee():assert pr.resolve_selection();phase('escape')
   else:assert len(result['cases'][-1]['rounds'])<5;choose();phase('attack')
  elif s['phase']=='escape':
   if not E.is_encounter_active():phase('ended')
   elif not live['pr'].get_view().busy and not live['pr'].get_view().finished:phase('flee')
  elif s['phase']=='ended'and not P.is_overworld_input_locked()and s['t']>.3:
   assert not unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterClassicBattleScene);assert P.get_actor_location().distance(unreal.Vector(*result['cases'][-1]['position']))<.5;result['cases'][-1]['returned']=True;s['case']+=1;(O/'Progress.json').write_text(json.dumps(dict(completed=s['case'],total=len(cases))))
   if s['case']==len(cases):finish();return
   phase('start')
 except Exception:finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');unreal._learn_production=unreal.register_slate_post_tick_callback(tick)
