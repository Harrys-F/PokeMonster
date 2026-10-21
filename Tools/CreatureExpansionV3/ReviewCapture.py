"""Real existing capture/team/heal/save flows for seven new species; controlled runtime fixture only."""
import unreal,json,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/CreatureExpansionV3/CaptureReviewRequest.json').read_text())['label'];O=R/'Saved/CreatureExpansionV3'/label;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==gi)
e=sub(unreal.PokeMonsterEncounterSubsystem);inv=sub(unreal.PokeMonsterInventorySubsystem);save=sub(unreal.PokeMonsterSaveSubsystem);balls=unreal.load_asset('/Game/Data/Items/DA_TestCaptureItem');heal=unreal.load_asset('/Game/Data/Items/DA_TestHealingItem');assert balls and heal
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False);s={'case':0,'phase':'start','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'rows':[]};cases=[('Glurak',n)for n in ['Pikachu','Myrapla','Enton','Machomei','Nebulak','Gengar','Glurak']]
sources={str(actor.visual_species.get_internal_id()):actor for actor in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor) if actor.visual_species and '_Group_' not in str(actor.encounter_id)}
for actor in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):actor.overworld_movement.set_movement_paused(True);actor.set_editor_property('profile',None)
for zone in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterWildEncounterZone):zone.set_actor_enable_collision(False)
s['fixture']='Explicit canonical level-100 player/reserve via existing progression, one-HP opponent and seed 51; capture/switch/healing/save QA, not balancing or natural wild encounter.'
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def phase(v):s.update(phase=v,time=0.)
def shot(n):cmd('pm.CreatureReview.CaptureLiveUI Starter_'+label+'_'+str(s['case'])+'_'+n)
def party():return [{'id':x.instance_id.to_string(),'species':str(x.species),'hp':x.current_hp,'xp':x.experience}for x in e.get_player_party()]
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._starter_capture);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';s.update(passed=error is None,error=error,save_after_sha256=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('STARTER_CAPTURE_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<900
  own,target=cases[s['case']]
  if s['phase']=='start'and s['time']>1:
   assert not e.is_encounter_active();cmd('pm.StarterReview.Party '+own+' Machomei '+target);a,reserve,b=e.get_player_party();ra,a=unreal.PokeMonsterCreatureProgression.add_experience(a,2000000);rr,reserve=unreal.PokeMonsterCreatureProgression.add_experience(reserve,2000000);assert a.level==reserve.level==100;a.current_hp=a.calculated_stats.max_hp;reserve.current_hp=reserve.calculated_stats.max_hp;b.current_hp=1;data=unreal.PokeMonsterEncounterStartData(presentation_mode=unreal.PokeMonsterBattlePresentationMode.CLASSIC_BATTLE,encounter_id=sources[target].encounter_id,kind=unreal.PokeMonsterEncounterKind.WILD,source=unreal.PokeMonsterEncounterSource.VISIBLE_CREATURE,player_team=[a,reserve],opponent_team=[b],random_seed=51,allow_flee=True,source_actor=sources[target]);assert inv.add_item(balls,20);assert inv.add_item(heal,50);s['rows'].append({'target':target,'opponent_hp_fixture':1,'opponent_id':b.instance_id.to_string(),'balls_before':inv.get_quantity(balls),'attempts':0});assert e.start_encounter(data,p);phase('switch')
  elif s['phase']=='switch'and s['time']>3:
   pr=e.get_presenter();v=pr.get_view()
   if not v.busy and not v.finished:assert v.player_team[1].can_switch;assert pr.try_select_switch(1);assert pr.resolve_selection();s['rows'][-1]['switch_selected']=True;phase('capture')
  elif s['phase']=='capture':
   if not e.is_encounter_active():phase('result');return
   pr=e.get_presenter();v=pr.get_view()
   if not v.busy and not v.finished:
    if v.must_switch:
     assert pr.try_select_switch(next(i for i,c in enumerate(v.player_team)if c.can_switch));assert pr.resolve_selection();return
    if v.player.current_hp<10 and v.player.max_hp-v.player.current_hp>=20:
     index=next(i for i,c in enumerate(v.player_team)if c.active);assert pr.try_select_healing_item(heal,index);assert pr.resolve_selection();s['rows'][-1]['battle_heals']=s['rows'][-1].get('battle_heals',0)+1;return
    e.get_battle_widget().set_battle_menu(unreal.PokeMonsterBattleMenu.BAG);shot('CaptureMenu');assert v.capture_enabled;assert pr.try_select_capture();assert pr.resolve_selection();s['rows'][-1]['attempts']+=1;assert s['rows'][-1]['attempts']<=20
  elif s['phase']=='result'and s['time']>2 and not p.is_overworld_input_locked():
   r=e.get_last_result();assert r.outcome==unreal.PokeMonsterEncounterOutcome.CAPTURED;assert sources[target].life_state==unreal.PokeMonsterWildLifeState.REMOVED and sources[target].get_editor_property('hidden');assert not sources[target].overworld_movement.escaping_defeat;s['rows'][-1]['source_removed_without_escape']=True;assert r.captured_creature.instance_id.to_string()==s['rows'][-1]['opponent_id'];assert len(e.get_player_party())==3;assert inv.get_quantity(balls)==s['rows'][-1]['balls_before']-s['rows'][-1]['attempts'];s['rows'][-1]['capture_transfer']=str(r.capture_transfer)
   for i in range(3):
    for n in range(32):
     c=e.get_player_party()[i]
     if c.current_hp==c.calculated_stats.max_hp:break
     assert e.use_healing_item_on_party_member(heal,i)
    assert e.get_player_party()[i].current_hp==e.get_player_party()[i].calculated_stats.max_hp
   before=party();assert save.save_current_game();assert save.load_game();assert party()==before;assert sources[target].life_state==unreal.PokeMonsterWildLifeState.REMOVED and sources[target].get_editor_property('hidden');s['rows'][-1]['source_still_removed_after_reload']=True;s['rows'][-1].update(healed=True,save_reload_equal=True,party=before);shot('CaughtHealed');s['case']+=1
   if s['case']==len(cases):finish();return
   phase('start')
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._starter_capture=unreal.register_slate_post_tick_callback(tick)
