"""Explicit WorldBattle exception/lifecycle proof, no map or saved-state mutation."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();request=json.loads((R/'Saved/BattleViewV2/WorldRequest.json').read_text())if(R/'Saved/BattleViewV2/WorldRequest.json').exists()else{};label=request.get('label','WorldProof02');assert label.isalnum();O=R/'Saved/BattleViewV2'/label;O.mkdir(exist_ok=False);w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi);assert not enc.is_encounter_active();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False);s={'phase':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'rounds':0,'position_before':p.get_actor_location().to_tuple(),'camera_before':pc.player_camera_manager.get_camera_location().to_tuple(),'view_target':pc.get_view_target().get_path_name()}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._glumanda_world_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);s.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now
  if s['phase']==0:
   unreal.SystemLibrary.execute_console_command(w,'pm.CreatureReview.Start world',pc);assert enc.is_encounter_active();s.update(phase=1,t=0.)
  elif s['phase']==1 and s['t']>3:
   assert not enc.get_battle_widget().is_classic_presentation();assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene);actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor);s['world_visual_positions']=[v.get_actor_location().to_tuple()for v in actors];assert all(abs(v.get_actor_location().z)<300 for v in actors);assert len(actors)>=3
   unreal.SystemLibrary.execute_console_command(w,'pm.CreatureReview.CaptureLiveUI BattleV2_WorldBattle_'+label,pc);unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(O/'WorldBattle.png')+'"',pc);s.update(phase=2,t=0.)
  elif s['phase']==2:
   if enc.is_encounter_active():
    pr=enc.get_presenter();view=pr.get_view()
    if not view.busy and not view.finished and s['t']>.6:assert pr.try_select_move(0);assert pr.resolve_selection();s['rounds']+=1;s['t']=0
   else:
    s['position_after']=p.get_actor_location().to_tuple();s['camera_after']=pc.player_camera_manager.get_camera_location().to_tuple();assert not p.is_overworld_input_locked();assert math.dist(s['position_before'],s['position_after'])<.01;assert math.dist(s['camera_before'],s['camera_after'])<.01;assert pc.get_view_target().get_path_name()==s['view_target'];s['outcome']=str(enc.get_last_result().outcome);finish()
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._glumanda_world_review=unreal.register_slate_post_tick_callback(tick)
