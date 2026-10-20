"""Four actual PIE environment/menu/animation/lifecycle reviews; no asset or save writes."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();request=json.loads((R/'Saved/BattleViewV2/ReviewRequest.json').read_text())if(R/'Saved/BattleViewV2/ReviewRequest.json').exists()else{};label=request.get('label','Review03');assert label.isalnum();O=R/'Saved/BattleViewV2'/label;O.mkdir(exist_ok=False);w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi);assert not enc.is_encounter_active();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
screen_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage');themes=['meadow','forest','cave','ruins'];s={'theme':0,'phase':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'rows':[]};unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport '+str(request.get('width',2560))+' '+str(request.get('height',1440)));unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 100')
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def shot(name):
 name='BattleV2_'+themes[s['theme']]+'_'+name+'_'+label;cmd('pm.CreatureReview.CaptureLiveUI '+name);s['rows'][-1].setdefault('screenshots',[]).append(name)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._battle_v2_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);cmd('pm.EnvPerf2.Viewport 0 0');cmd('r.ScreenPercentage '+str(screen_percentage));s.update(passed=error is None,error=error,mode=request.get('mode','PIE'),requested_viewport=[request.get('width',2560),request.get('height',1440)]);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('BATTLE_V2_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now
  if s['phase']==0 and s['t']>2:
   s['rows'].append({'theme':themes[s['theme']],'position_before':p.get_actor_location().to_tuple(),'camera_before':pc.player_camera_manager.get_camera_location().to_tuple(),'reactions':[],'rounds':0});cmd('pm.CreatureReview.Start classic '+themes[s['theme']]);assert enc.is_encounter_active();s.update(phase=1,t=0.)
  elif s['phase']==1 and s['t']>5:
   a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene));entry=s['rows'][-1];entry['environment']=str(a.environment);entry['framing_distance']=a.framing_distance;entry['dressing_instances']=sum(c.get_instance_count()for c in a.get_components_by_class(unreal.InstancedStaticMeshComponent));assert entry['dressing_instances']>=25;entry['capture_location']=a.capture.get_world_location().to_tuple();assert enc.get_battle_widget().get_battle_menu()==unreal.PokeMonsterBattleMenu.COMMANDS;shot('Commands');s.update(phase=2,t=0.)
  elif s['phase']in [2,3,4]and s['t']>1:
   page=[unreal.PokeMonsterBattleMenu.MOVES,unreal.PokeMonsterBattleMenu.TEAM,unreal.PokeMonsterBattleMenu.BAG][s['phase']-2];enc.get_battle_widget().set_battle_menu(page);s.update(phase=s['phase']+10,t=0.)
  elif s['phase']in [12,13,14]and s['t']>.6:
   shot(['Moves','Team','Bag'][s['phase']-12]);s.update(phase=s['phase']-9,t=0.)
  elif s['phase']==5:
   enc.get_battle_widget().set_battle_menu(unreal.PokeMonsterBattleMenu.COMMANDS);s.update(phase=6,t=0.)
  elif s['phase']==6:
   entry=s['rows'][-1]
   if enc.is_encounter_active():
    pr=enc.get_presenter();v=pr.get_view()
    for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor):
     if str(a.reaction)not in entry['reactions']:entry['reactions'].append(str(a.reaction))
    if not v.busy and not v.finished and s['t']>.7:assert pr.try_select_move(0);assert pr.resolve_selection();entry['rounds']+=1;s['t']=0
    if v.busy and 'action_shot'not in entry and s['t']>.4:shot('Attack');entry['action_shot']=True
   else:
    entry['position_after']=p.get_actor_location().to_tuple();entry['camera_after']=pc.player_camera_manager.get_camera_location().to_tuple();assert math.dist(entry['position_before'],entry['position_after'])<.01;assert math.dist(entry['camera_before'],entry['camera_after'])<.01;assert not p.is_overworld_input_locked();assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene);s['theme']+=1
    if s['theme']==len(themes):finish();return
    s.update(phase=0,t=0.)
 except Exception:
  import traceback
  finish(traceback.format_exc());unreal.log_error(traceback.format_exc())
unreal._battle_v2_review=unreal.register_slate_post_tick_callback(tick)
