"""Existing battle/capture/party/heal/save flows in explicitly isolated PIE RAM preview. No disk save."""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();req=json.loads((R/'Saved/BiomeTestV11/GameplayRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];assert req['label'].isalnum();O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);mode=unreal.GameplayStatics.get_game_mode(w)
def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==gi)
e=sub(unreal.PokeMonsterEncounterSubsystem);inv=sub(unreal.PokeMonsterInventorySubsystem);save=sub(unreal.PokeMonsterSaveSubsystem);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
assert mode.begin_isolated_gameplay_review()and mode.is_isolated_gameplay_review(),'No safe RAM preview: do not run gameplay fixture'
balls=unreal.load_asset('/Game/Data/Items/DA_TestCaptureItem');heal=unreal.load_asset('/Game/Data/Items/DA_TestHealingItem');assert balls and heal
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
cases=[('classic',n,'Zunderlauf')for n in req['species']]+[('classic','Glurak',n)for n in req['species']]+[('world',req['species'][-1],'Zunderlauf')]
s={'i':0,'phase':'begin','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'rows':[],'shots':[]};baseline_party=[]
def cmd(x):unreal.SystemLibrary.execute_console_command(w,x,pc)
def phase(x):s.update(phase=x,time=0.)
def party():
 return [dict(id=c.instance_id.to_string(),species=c.species.get_path_name(),hp=c.current_hp,xp=c.experience,level=c.level,moves=[dict(move=x.get_editor_property('move').get_path_name()if x.get_editor_property('move')else None,pp=x.get_editor_property('current_pp'))for x in c.get_editor_property('move_slots')])for c in e.get_player_party()]
def shot(label):
 path=O/(label+'.png');assert not path.exists();cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['shots'].append(str(path.relative_to(R)));cmd('pm.CreatureReview.CaptureLiveUI BiomeV11_'+req['label']+'_'+label)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_gameplay_v11);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle)
 if not error:
  assert mode.end_isolated_gameplay_review()and not mode.is_isolated_gameplay_review();assert not save.save_current_game()and not save.load_game();assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'fixture':'Explicit native review parties; original authored levels, one-HP capture target, seed 51. RAM-only existing save transport. Not natural wild encounters.','rows':s['rows'],'shots':s['shots'],'save_sha256_before':before,'save_sha256_after':hashlib.sha256(slot.read_bytes()).hexdigest(),'RAM_review_left_active_on_failure':mode.is_isolated_gameplay_review()},indent=2));unreal.log('BIOME_GAMEPLAY_V11_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<900;assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
  if s['i']>=len(cases):finish();return
  presentation,own,target=cases[s['i']];t=s['time']
  if s['phase']=='begin':
   assert not e.is_encounter_active();cmd('pm.StarterReview.Party '+own+' '+target);assert len(e.get_player_party())==2;assert str(e.get_player_party()[0].species.get_internal_id())==own
   s['rows'].append({'presentation':presentation,'own':own,'target':target});cmd('pm.StarterReview.Start '+presentation+' '+own+' '+target);assert e.is_encounter_active();phase('battle')
  elif s['phase']=='battle'and t>3:
   v=e.get_presenter().get_view();assert not v.finished;shot(str(s['i'])+'_'+presentation+'_'+own+'_'+target)
   if presentation=='classic':
    scene=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene)[0];assert scene.player_visual and scene.opponent_visual
    unreal.RenderingLibrary.export_render_target(w,scene.target,str(O),str(s['i'])+'_ClassicStage.png');s['rows'][-1]['framing_distance_cm']=scene.framing_distance
   index=next(i for i,m in enumerate(v.moves)if m.enabled);s['rows'][-1]['selected_move']=str(v.moves[index].name);assert e.get_presenter().try_select_move(index);assert e.get_presenter().resolve_selection();phase('resolve')
  elif s['phase']=='resolve'and t>2:
   if not e.is_encounter_active():phase('after_battle');return
   v=e.get_presenter().get_view()
   if not v.busy and not v.finished:assert e.get_presenter().try_select_flee();assert e.get_presenter().resolve_selection();s['time']=0
  elif s['phase']=='after_battle'and t>1 and not p.is_overworld_input_locked():
   s['rows'][-1]['first_battle_result']=str(e.get_last_result().outcome)
   if target not in req['species']:s['i']+=1;phase('begin');return
   cmd('pm.StarterReview.Party Glurak Machomei '+target);a,reserve,b=e.get_player_party();b.current_hp=1;assert inv.add_item(balls,20);assert inv.add_item(heal,30);s['capture_before']=inv.get_quantity(balls);s['capture_tries']=0;s['captured_id']=b.instance_id.to_string()
   start=unreal.PokeMonsterEncounterStartData(presentation_mode=unreal.PokeMonsterBattlePresentationMode.CLASSIC_BATTLE,encounter_id='ExplicitBiomeCapture_'+target,kind=unreal.PokeMonsterEncounterKind.WILD,source=unreal.PokeMonsterEncounterSource.VISIBLE_CREATURE,player_team=[a,reserve],opponent_team=[b],random_seed=51,allow_flee=True)
   assert e.start_encounter(start,p);phase('switch')
  elif s['phase']=='switch'and t>3:
   v=e.get_presenter().get_view()
   if not v.busy and not v.finished:assert e.get_presenter().try_select_switch(1);assert e.get_presenter().resolve_selection();s['rows'][-1]['team_switch']=True;phase('capture')
  elif s['phase']=='capture':
   if not e.is_encounter_active():phase('caught');return
   v=e.get_presenter().get_view()
   if not v.busy and not v.finished:
    if v.must_switch:assert e.get_presenter().try_select_switch(next(i for i,c in enumerate(v.player_team)if c.can_switch));assert e.get_presenter().resolve_selection();return
    if v.player.current_hp<max(10,v.player.max_hp//3):
     assert e.get_presenter().try_select_healing_item(heal,next(i for i,c in enumerate(v.player_team)if c.active));assert e.get_presenter().resolve_selection();return
    e.get_battle_widget().set_battle_menu(unreal.PokeMonsterBattleMenu.BAG)
    if not s['capture_tries']:shot(target+'_CaptureBag')
    assert e.get_presenter().try_select_capture();assert e.get_presenter().resolve_selection();s['capture_tries']+=1;assert s['capture_tries']<=20
  elif s['phase']=='caught'and t>1 and not p.is_overworld_input_locked():
   assert e.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.CAPTURED;assert e.get_last_result().captured_creature.instance_id.to_string()==s['captured_id'];assert len(e.get_player_party())==3;assert inv.get_quantity(balls)==s['capture_before']-s['capture_tries']
   for i in range(3):
    for _ in range(32):
     c=e.get_player_party()[i]
     if c.current_hp==c.calculated_stats.max_hp:break
     assert e.use_healing_item_on_party_member(heal,i)
   old=party();assert save.save_current_game()and save.load_game();assert party()==old;s['rows'][-1].update(captured=True,capture_attempts=s['capture_tries'],identity_preserved=True,healing_and_RAM_save_reload_equal=True)
   s['i']+=1;phase('begin')
 except Exception:finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100')
unreal._biome_gameplay_v11=unreal.register_slate_post_tick_callback(tick)
