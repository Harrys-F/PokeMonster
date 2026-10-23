"""Actual production moves in existing-map PIE/UMG, with explicitly controlled runtime combatants.
Screens are real viewport captures. No map/assets/save writes; no physical controller claim.
"""
import unreal,json,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/MoveEffectsV4/ProductionReviewRequest.json').read_text())['label'];assert label.isalnum();O=R/'Saved/MoveEffectsV4'/label;O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_TestMap_VisualV2'in w.get_name();pc=unreal.GameplayStatics.get_player_controller(w,0);p=unreal.GameplayStatics.get_player_pawn(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi)
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):a.destroy_actor()
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterWildEncounterZone):a.set_actor_enable_collision(False)
plan=json.loads((R/'Tools/MoveEffectsV4/ProductionReviewPlan.json').read_text())['cases'];cases=[dict(c,mode='classic')for c in plan];seen=set()
for c in plan:
 if c['species']not in seen:cases.append(dict(c,mode='world'));seen.add(c['species'])
assert len(cases)==59 and len(seen)==10
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False);percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')
s={'case':0,'phase':'start','t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'rows':[],'shots':[],'technical_fixture':True,'actual_production_assets':True,'physical_controller_test':False}
def cmd(x):unreal.SystemLibrary.execute_console_command(w,x,pc)
def phase(x):s.update(phase=x,t=0.)
def shot(x):
 name='Crystal'+label+str(s['case'])+x;cmd('pm.CreatureReview.CaptureLiveUI '+name);s['shots'].append(str(R/'Saved/GlumandaV11/LiveUI'/name/'ActualSlateViewport.png'))
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._crystal_production_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);cmd('pm.EnvPerf2.Viewport 0 0');cmd('r.ScreenPercentage '+str(percentage));after=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
 if after!=before:error=(error or '')+' Developer save changed'
 s.update(passed=error is None,error=error,save_before=before,save_after=after);(O/'Result.json').write_text(json.dumps(s,ensure_ascii=False,indent=2));unreal.log('CRYSTAL_PRODUCTION_REVIEW_DONE '+str(error))
def choose():
 ui=enc.get_battle_widget();ui.set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);cmd('pm.Input.Key Gamepad_FaceButton_Right tap')
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<1600,'Review timed out';c=cases[s['case']]
  if s['phase']=='start'and s['t']>.5:
   assert not enc.is_encounter_active();s['rows'].append(dict(c,position_before=p.get_actor_location().to_tuple(),rounds=[]));cmd('pm.CrystalMoves.Start '+c['mode']+' '+c['id']+' '+c['species']+' 71');assert enc.is_encounter_active();phase('ready')
  elif s['phase']=='ready'and s['t']>1.5:
   assert pc.get_viewport_size()==(2560,1440);v=enc.get_presenter().get_view();assert not v.busy;assert enc.get_battle_widget().is_classic_presentation()==(c['mode']=='classic');s['rows'][-1]['pp_before']=v.moves[0].current_pp;shot('Before');choose();phase('attack')
  elif s['phase']=='attack':
   assert enc.is_encounter_active();pr=enc.get_presenter();v=pr.get_view();row=s['rows'][-1]
   if v.round>len(row['rounds'])and not v.busy:
    result=pr.get_last_result();assert result.succeeded
    events=[dict(type=str(e.type),source=str(e.source),target=str(e.target),move=str(e.move_id),damage=e.damage,hp_before=e.hp_before,hp_after=e.hp_after,pp_before=e.pp_before,pp_after=e.pp_after,text=str(e.information))for e in result.events]
    assert any('MOVE_EXECUTED'in e['type']and 'PokeMonsterBattleSide.A'in e['source']and c['id']in e['move']for e in events),(c,events)
    row['rounds'].append(dict(round=v.round,events=events));row['pp_after']=v.moves[0].current_pp
    if len(row['rounds'])==1:assert row['pp_after']==row['pp_before']-1;shot('After')
    phase('flee')
  elif s['phase']=='flee'and s['t']>.5:
   pr=enc.get_presenter()
   if pr.try_select_flee():assert pr.resolve_selection();s['rows'][-1]['flee_attempts']=s['rows'][-1].get('flee_attempts',0)+1;phase('ended')
   else:
    assert len(s['rows'][-1]['rounds'])<5,'Unexpected persistent action lock';choose();phase('attack')
  elif s['phase']=='ended'and enc.is_encounter_active():
   pr=enc.get_presenter();v=pr.get_view()
   if not v.busy and not v.finished and s['t']>.5:
    events=pr.get_last_result().events
    assert any('FLEE_FAILED'in str(e.type)for e in events),'Unexpected encounter still active'
    assert s['rows'][-1].get('flee_attempts',0)<10,'Escape attempt guard'
    s['rows'][-1].setdefault('failed_escape_events',[]).extend([dict(threshold=e.flee_threshold,roll=e.flee_roll)for e in events if 'FLEE_FAILED'in str(e.type)])
    phase('flee')
  elif s['phase']=='ended'and not enc.is_encounter_active()and not p.is_overworld_input_locked():
   row=s['rows'][-1];assert p.get_actor_location().distance(unreal.Vector(*row['position_before']))<.1;assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene);row['returned']=True;s['case']+=1
   (O/'Progress.json').write_text(json.dumps(dict(completed=s['case'],total=len(cases))))
   if s['case']==len(cases):finish();return
   phase('start')
 except Exception:
  import traceback
  finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');unreal._crystal_production_review=unreal.register_slate_post_tick_callback(tick)
