"""Real existing-map PIE battle menu/lifecycle exercise. Never saves a map, asset, or game."""
import unreal,json,math,hashlib,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();request=json.loads((R/'Saved/BattleSystemV3/ReviewRequest.json').read_text());label=request['label'];assert label.isalnum();O=R/'Saved/BattleSystemV3'/label;O.mkdir(exist_ok=False)
w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi);inv=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterInventorySubsystem)if s.get_outer()==gi);item=unreal.load_asset('/Game/Data/Items/DA_TestHealingItem');assert not enc.is_encounter_active()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';save_before=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
cases=[('classic','wild'),('world','wild'),('classic','trainer'),('world','story'),('classic','failflee'),('classic','forced'),('world','defeat'),('classic','victory'),('classic','exhausted')]
s={'case':0,'phase':'start','t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'rows':[],'start_wall':time.monotonic()};last_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')
def cmd(text):unreal.SystemLibrary.execute_console_command(w,text,pc)
def shot(name):
 name='BattleV3_'+label+'_'+str(s['case'])+'_'+name;cmd('pm.CreatureReview.CaptureLiveUI '+name);s['rows'][-1].setdefault('screenshots',[]).append(name)
def result_events(pr):return [{'type':str(e.type),'source':str(e.source),'target':str(e.target),'damage':e.damage,'restored_hp':e.restored_hp,'hp_before':e.hp_before,'hp_after':e.hp_after,'xp':e.experience_added,'stage':e.stage_after,'roll':e.flee_roll,'threshold':e.flee_threshold}for e in pr.get_last_result().events]
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._battle_v3_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);cmd('pm.EnvPerf2.Viewport 0 0');cmd('r.ScreenPercentage '+str(last_percentage));save_after=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
 if error is None and save_after!=save_before:error='Developer save changed unexpectedly'
 s.update(passed=error is None,error=error,save_before=save_before,save_after=save_after,mode=request.get('mode','PIE'));(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('BATTLE_V3_REVIEW_DONE '+str(error))
def advance(phase):s.update(phase=phase,t=0.)
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['start_wall']<900,'Review timeout'
  mode,case=cases[s['case']];row=s['rows'][-1]if s['rows']else None
  if s['phase']=='start' and s['t']>1:
   if p.is_overworld_input_locked():return
   row={'mode':mode,'case':case,'position_before':p.get_actor_location().to_tuple(),'camera_before':pc.player_camera_manager.get_camera_location().to_tuple(),'view_target':pc.get_view_target().get_path_name(),'actions':[]};s['rows'].append(row);cmd('pm.BattleV3.Start '+mode+' '+case);assert enc.is_encounter_active();advance('warm')
  elif s['phase']=='warm'and s['t']>3:
   pr=enc.get_presenter();v=pr.get_view();ui=enc.get_battle_widget();assert ui.is_classic_presentation()==(mode=='classic');assert [str(m.name)for m in v.moves[:3]]==(['Verzweifler','Heuler','Glut']if case=='exhausted'else['Kratzer','Heuler','Glut']);assert not v.moves[3].enabled
   assert v.flee_enabled==(case not in['trainer','story']);row['flee_enabled']=v.flee_enabled
   if case in['trainer','story']:assert not pr.try_select_flee()
   visuals=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor);row['tail_flame_components']=sum(1 for a in visuals for c in a.get_components_by_class(unreal.StaticMeshComponent)if str(c.get_attach_socket_name())=='tail_socket'and c.is_visible());row['visual_count']=len(visuals)
   shot('Commands');cmd('pm.BattleView2.Input Focus');cmd('pm.BattleView2.Input Enter');assert ui.get_battle_menu()==unreal.PokeMonsterBattleMenu.MOVES;cmd('pm.BattleView2.Input Escape');assert ui.get_battle_menu()==unreal.PokeMonsterBattleMenu.COMMANDS;cmd('pm.BattleView2.Input A');assert ui.get_battle_menu()==unreal.PokeMonsterBattleMenu.MOVES;cmd('pm.BattleView2.Input B');assert ui.get_battle_menu()==unreal.PokeMonsterBattleMenu.COMMANDS;row['keyboard_and_logical_controller']=True;ui.set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);s['ops']=['bench','active','growl','ember','switch','flee']if case=='wild'else['flee']if case=='failflee'else['move'];s['op']=0;advance('menu')
  elif s['phase']=='menu'and s['t']>.45:
   pr=enc.get_presenter();v=pr.get_view();ui=enc.get_battle_widget();op=s['ops'][s['op']]
   if op in['bench','active']:
    ui.set_battle_menu(unreal.PokeMonsterBattleMenu.BAG);shot('Bag'+str(s['op']));assert ui.get_healing_button(0).get_is_enabled();cmd('pm.BattleV3.Click heal 0');assert ui.get_battle_menu()==unreal.PokeMonsterBattleMenu.TEAM;advance('target')
   else:
    shot('Moves')if s['op']==0 else None
    row['stock_before']=inv.get_quantity(item);row['before_round']=v.round
    if op=='flee':ui.set_battle_menu(unreal.PokeMonsterBattleMenu.COMMANDS);cmd('pm.BattleV3.Click command 3')
    elif op=='switch':ui.set_battle_menu(unreal.PokeMonsterBattleMenu.TEAM);cmd('pm.BattleV3.Click team 1')
    else:ui.set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);cmd('pm.BattleV3.Click move '+str(1 if op=='growl'else 2 if op=='ember'else 0))
    assert pr.get_view().busy;row['pending_op']=op;advance('resolve')
  elif s['phase']=='target'and s['t']>.45:
   op=s['ops'][s['op']];ui=enc.get_battle_widget();shot('HealingTarget'+str(s['op']));assert ui.get_switch_button(0).get_is_enabled();row['stock_before']=inv.get_quantity(item);row['before_round']=enc.get_presenter().get_view().round;cmd('pm.BattleV3.Click team '+('1'if op=='bench'else'0'));assert enc.get_presenter().get_view().busy;row['pending_op']=op;advance('resolve')
  elif s['phase']=='resolve':
   if enc.is_encounter_active():
    pr=enc.get_presenter();v=pr.get_view();ui=enc.get_battle_widget()
    if v.round>row['before_round']and not row.get('recorded'):
     events=result_events(pr);row['actions'].append({'op':row['pending_op'],'round':v.round,'events':events,'stock_before':row['stock_before'],'stock_after':inv.get_quantity(item)});row['recorded']=True
     if any('FLEE_'in e['type']and 'CHOSEN'not in e['type']for e in events):shot('FleeResult')
     if row['pending_op']in['bench','active']:assert inv.get_quantity(item)==row['stock_before']-1
     if row['pending_op']=='growl':assert any('ATTACK_LOWERED'in e['type']for e in events)and not any('DAMAGE'in e['type']and e['source'].endswith('.A')for e in events)
     if case=='failflee'and s['op']==0:assert any('FLEE_FAILED'in e['type']for e in events)
    # Capture actual visible Ember travel; no synthetic test rendering.
    if row['pending_op']=='ember'and not row.get('fire_shot'):
     for image in unreal.ObjectIterator(unreal.Image):
      if image.get_name()=='BattleEffect'and image.get_outer().get_outer()==ui and image.get_visibility()==unreal.SlateVisibility.HIT_TEST_INVISIBLE:shot('EmberTravel');row['fire_shot']=True;break
    if s['t']>.9 and not row.get('action_shot_'+str(s['op'])):shot('Action'+str(s['op']));row['action_shot_'+str(s['op'])]=True
    if not v.busy:
     if v.must_switch:
      row['forced_switch_seen']=True;ui.set_battle_menu(unreal.PokeMonsterBattleMenu.TEAM);shot('ForcedSwitch');idx=next(i for i,m in enumerate(v.player_team)if m.can_switch);cmd('pm.BattleV3.Click team '+str(idx));row['before_round']=v.round;row['pending_op']='forced_switch';row['recorded']=False;advance('resolve');return
     row['recorded']=False;s['op']+=1
     if s['op']<len(s['ops']):advance('menu')
     else:advance('finish_battle')
   elif not p.is_overworld_input_locked():advance('ended')
  elif s['phase']=='finish_battle':
   if not enc.is_encounter_active():advance('ended');return
   pr=enc.get_presenter();v=pr.get_view()
   if v.finished:return
   if not v.busy and s['t']>.6:
    if v.must_switch:assert pr.try_select_switch(next(i for i,m in enumerate(v.player_team)if m.can_switch))
    elif v.flee_enabled and case not in['forced','victory','exhausted']:assert pr.try_select_flee()
    else:assert pr.try_select_move(0)
    assert pr.resolve_selection();row.setdefault('finishing_rounds',[]).append(result_events(pr));s['t']=0
  elif s['phase']=='ended'and s['t']>1:
   if p.is_overworld_input_locked():return
   end=enc.get_last_result();row['outcome']=str(end.outcome);row['position_after']=p.get_actor_location().to_tuple();row['camera_after']=pc.player_camera_manager.get_camera_location().to_tuple();assert pc.get_view_target().get_path_name()==row['view_target'];assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene)
   if case=='wild':assert end.outcome==unreal.PokeMonsterEncounterOutcome.FLED and math.dist(row['position_before'],row['position_after'])<.01
   if case=='victory':assert end.outcome==unreal.PokeMonsterEncounterOutcome.VICTORY
   if case=='defeat':assert end.outcome==unreal.PokeMonsterEncounterOutcome.DEFEAT and all(c.current_hp>0 for c in enc.get_player_party())
   if case=='forced':assert row.get('forced_switch_seen')
   s['case']+=1
   if s['case']==len(cases):finish();return
   advance('start')
 except Exception:
  import traceback
  finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100')
unreal._battle_v3_review=unreal.register_slate_post_tick_callback(tick)
