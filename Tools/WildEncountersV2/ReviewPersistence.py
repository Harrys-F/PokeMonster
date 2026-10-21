"""Actual victory/escape -> post-KO save/load -> explicit pre-KO snapshot load.
Only the guarded development save slot is exercised; no packages or original assets are written.
"""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/WildEncountersV2/PersistenceRequest.json').read_text())['label'];O=R/'Saved/WildEncountersV2'/label;assert O.exists()and not(O/'Result.json').exists();slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==gi);wild=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor);a=next(x for x in wild if 'Zunderlauf'in str(x.visual_species));origin=unreal.Vector(*next(x['position']for x in json.loads((R/'Saved/WildEncountersV2/Inspection.json').read_text())['wild']if x['id']==str(a.encounter_id)));m=a.overworld_movement
for x in wild:x.overworld_movement.set_movement_paused(True)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def party():return [(x.instance_id.to_string(),x.current_hp,x.experience)for x in e.get_player_party()]
cmd('pm.StarterReview.Party Schiggy Bisasam Zunderlauf');cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');p.set_actor_location(origin+unreal.Vector(140,0,-9.85),False,True)
assert save.save_current_game();before_bytes=slot.read_bytes();before_party=party();assert not e.is_encounter_completed(a.encounter_id)
s={'phase':'start','seconds':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'original_spawn':origin.to_tuple(),'pre_ko_party':before_party,'pre_ko_snapshot_sha256':hashlib.sha256(before_bytes).hexdigest(),'fixture':'Explicit 1-HP visible-source battle; actual escape and both save/load directions'}
def phase(x):s.update(phase=x,seconds=0.)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._wild_persistence_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',old);s.update(passed=error is None,error=error,save_after_sha256=hashlib.sha256(slot.read_bytes()).hexdigest());(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('WILD_PERSISTENCE_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['seconds']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<180
  if s['phase']=='start'and s['seconds']>1:
   cmd('Shot filename="'+str(O/'BeforeKO.png')+'"');own,reserve,opponent=e.get_player_party();opponent.current_hp=1;s['xp_before']=own.experience
   d=unreal.PokeMonsterEncounterStartData(presentation_mode=unreal.PokeMonsterBattlePresentationMode.CLASSIC_BATTLE,encounter_id=a.encounter_id,kind=unreal.PokeMonsterEncounterKind.WILD,source=unreal.PokeMonsterEncounterSource.VISIBLE_CREATURE,player_team=[own,reserve],opponent_team=[opponent],random_seed=51,allow_flee=True,source_actor=a);assert e.start_encounter(d,p);phase('fight')
  elif s['phase']=='fight':
   if e.is_encounter_active():
    pr=e.get_presenter();v=pr.get_view()
    if not v.busy and not v.finished:i=next(i for i,x in enumerate(v.moves)if str(x.name)=='Aquaknarre');assert pr.try_select_move(i);assert pr.resolve_selection()
   else:
    assert e.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.VICTORY;assert e.get_player_party()[0].experience>s['xp_before'];s['xp_after']=e.get_player_party()[0].experience;phase('escape')
  elif s['phase']=='escape':
   assert not e.is_encounter_active();assert e.is_encounter_completed(a.encounter_id)
   if a.life_state==unreal.PokeMonsterWildLifeState.REMOVED:
    assert a.is_outside_player_view();s['escaped_distance']=m.distance_travelled;assert save.save_current_game();after_hash=hashlib.sha256(slot.read_bytes()).hexdigest();assert save.load_game();assert a.life_state==unreal.PokeMonsterWildLifeState.REMOVED and a.get_editor_property('hidden');assert e.is_encounter_completed(a.encounter_id);s['post_ko_load_no_respawn']=True
    # Rewind only this test's known snapshot. The outer runner preserves the user's original slot.
    assert hashlib.sha256(slot.read_bytes()).hexdigest()==after_hash,'Concurrent save write';slot.write_bytes(before_bytes);assert save.load_game();assert not e.is_encounter_completed(a.encounter_id);assert a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and not a.get_editor_property('hidden');assert a.get_actor_location().distance(origin)<.1;assert party()==before_party;s['pre_ko_load_restored_spawn_and_party']=True;phase('reactivated')
   assert s['seconds']<90,'Escape did not finish'
  elif s['phase']=='reactivated':
   assert not e.is_encounter_active();assert m.is_inside_habitat(a.get_actor_location()-unreal.Vector(0,0,60));assert len(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor))==5
   if s['seconds']>3 and not s.get('shot'):cmd('Shot filename="'+str(O/'PreKOLoadRestored.png')+'"');s['shot']=True
   if s['seconds']>5:
    assert m.distance_travelled>5,'Restored wild did not resume movement';s['restored_movement_distance']=m.distance_travelled;finish()
 except Exception:finish(traceback.format_exc())
unreal._wild_persistence_review=unreal.register_slate_post_tick_callback(tick)
