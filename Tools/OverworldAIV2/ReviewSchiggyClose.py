"""Native existing ClassicBattle detail camera, identical pose, no camera/scale changes."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/OverworldAIV2/SchiggyClose';O.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);old=unreal.load_asset('/Game/Characters/Creatures/Schiggy/MeshyV1/DA_Schiggy_Presentation');new=unreal.load_asset('/Game/Characters/Creatures/Schiggy/SurfaceV2/DA_Schiggy_Presentation');s={'phase':'begin','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'i':0,'posed':False,'shot':False,'rows':[]}
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._ai_schiggy_close);s.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<90
  if s['phase']=='begin':cmd('pm.StarterReview.Start classic Bisasam Schiggy');assert e.is_encounter_active();s.update(phase='photos',time=0.);return
  if s['phase']=='photos':
   scene=next(iter(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene)));v=scene.opponent_visual;label,profile=[('Before',old),('After',new)][s['i']]
   if not s['posed']:
    assert v.set_presentation(profile);v.mesh.set_editor_property('pause_anims',False);v.mesh.play_animation(profile.clips[unreal.PokeMonsterCreatureClip.IDLE],True);v.mesh.set_play_rate(0);v.mesh.set_position(.22,False);s['posed']=True
   if s['time']>4 and not s['shot']:
    cmd('pm.CreatureReview.CaptureLiveUI AIV2_Schiggy_'+label);unreal.RenderingLibrary.export_render_target(w,scene.target,str(O),label);s['rows'].append({'label':label,'profile':profile.get_path_name(),'location':v.get_actor_location().to_tuple(),'scale':v.get_actor_scale3d().to_tuple(),'native_render_target':[scene.target.size_x,scene.target.size_y],'pose_seconds':.22});s['shot']=True
   if s['time']>6:
    if s['i']==0:s.update(i=1,time=0.,posed=False,shot=False)
    else:v.set_presentation(new);s.update(phase='flee',time=0.)
  elif s['phase']=='flee':
   if not e.is_encounter_active():assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene);finish();return
   view=e.get_presenter().get_view()
   if not view.busy and not view.finished:assert e.get_presenter().try_select_flee();assert e.get_presenter().resolve_selection()
 except Exception as ex:finish(str(ex));raise
unreal._ai_schiggy_close=unreal.register_slate_post_tick_callback(tick)
