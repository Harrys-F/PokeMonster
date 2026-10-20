"""Explicit same-world classic presentation/lifecycle review. Never saves an asset or developer slot."""
import unreal,json,math,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/GlumandaV11/ClassicProofFinal';O.mkdir(exist_ok=False)
w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi);assert not enc.is_encounter_active()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 100')
s={'started_game_seconds':unreal.GameplayStatics.get_time_seconds(w),'phase':0,'elapsed':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'shots':0,'start_position':p.get_actor_location().to_tuple(),'view_target':pc.get_view_target().get_path_name(),'camera_before':None,'rounds':0,'reactions':set()}
def command(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._glumanda_classic_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);s['passed']=error is None;s['error']=error;s['reactions']=sorted(s['reactions']);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('GLUMANDA_CLASSIC_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['elapsed']+=now-s['last'];s['last']=now
  assert list(pc.get_viewport_size())==[2560,1440]
  if s['phase']==0 and s['elapsed']>2:
   s['start_position']=p.get_actor_location().to_tuple();s['camera_before']=pc.player_camera_manager.get_camera_location().to_tuple();s['rotation_before']=pc.player_camera_manager.get_camera_rotation().to_tuple();command('pm.CreatureReview.Start classic');assert enc.is_encounter_active();s.update(phase=1,elapsed=0.)
  elif s['phase']==1 and s['elapsed']>5:
   assert enc.get_battle_widget().is_classic_presentation();scene=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene));assert scene.player_visual and scene.opponent_visual
   for v in [scene.player_visual,scene.opponent_visual]:assert v.mesh.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
   s['stage']={'position':scene.get_actor_location().to_tuple(),'capture':scene.capture.get_world_location().to_tuple(),'own':scene.player_visual.get_actor_location().to_tuple(),'enemy':scene.opponent_visual.get_actor_location().to_tuple(),'own_rotation':scene.player_visual.get_actor_rotation().to_tuple(),'enemy_rotation':scene.opponent_visual.get_actor_rotation().to_tuple()}
   command('pm.CreatureReview.CaptureLiveUI ClassicIdleFinal');command('Shot filename="'+str(O/'ActualWorldFramebuffer.png')+'"');s.update(phase=2,elapsed=0.)
  elif s['phase']==2:
   pr=enc.get_presenter()
   if enc.is_encounter_active():
    for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor):s['reactions'].add(str(a.reaction))
    if s['elapsed']>.7 and not pr.get_view().busy and not pr.get_view().finished:assert pr.try_select_move(0);assert pr.resolve_selection();s['rounds']+=1;s['elapsed']=0
    if pr.get_view().busy and s['shots']<4 and s['elapsed']>.35:command('pm.CreatureReview.CaptureLiveUI ClassicActionFinal'+str(s['shots']));s['shots']+=1
   else:
    s['position_after']=p.get_actor_location().to_tuple();s['camera_after']=pc.player_camera_manager.get_camera_location().to_tuple();assert not p.is_overworld_input_locked();assert pc.get_view_target().get_path_name()==s['view_target'];assert math.dist(p.get_actor_location().to_tuple(),s['start_position'])<.01;assert math.dist(pc.player_camera_manager.get_camera_location().to_tuple(),s['camera_before'])<.01;assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene);s['camera_after']=pc.player_camera_manager.get_camera_location().to_tuple();s['position_after']=p.get_actor_location().to_tuple();s['outcome']=str(enc.get_last_result().outcome);finish()
  if now-s.get('started_game_seconds',now)>120:raise RuntimeError('Review timeout')
 except Exception as e:
  import traceback
  finish(traceback.format_exc());unreal.log_error(str(e))
unreal._glumanda_classic_review=unreal.register_slate_post_tick_callback(tick)
