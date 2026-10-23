"""Observe real existing full route; no gameplay decisions and no asset/save mutations."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/GlumandaV11/Acceptance'/json.loads((R/'Saved/GlumandaV11/AcceptanceRequest.json').read_text())['label'];w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));pc=unreal.GameplayStatics.get_player_controller(w,0);p=unreal.GameplayStatics.get_player_pawn(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi);s={'encounters':[],'in_battle':False,'reactions':set(),'party_name_after_load':False,'last_round':-1};settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=json.loads((O/'EditorSettingsBefore.json').read_text())['throttle']
def tick(dt):
 try:
  active=enc.is_encounter_active()
  if active and not s['in_battle']:
   assert enc.get_battle_widget().is_classic_presentation();s['encounters'].append({'start_player':p.get_actor_location().to_tuple(),'view_target':pc.get_view_target().get_path_name(),'classic':True,'shots':0,'rounds':[]});s['last_round']=-1
  if active:
   entry=s['encounters'][-1]
   observed=p.get_actor_location().to_tuple();delta=math.dist(entry['start_player'],observed)
   entry['max_player_delta_cm']=max(entry.get('max_player_delta_cm',0.),delta)
   if delta>=.01:entry['movement_failure']={'observed':observed,'delta_cm':delta,'velocity':p.get_velocity().to_tuple(),'locked':p.is_overworld_input_locked(),'round':enc.get_presenter().get_view().round}
   assert delta<.01,entry.get('movement_failure')
   assert entry['view_target']==pc.get_view_target().get_path_name()
   scene=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene));assert scene.target
   for v in [scene.player_visual,scene.opponent_visual]:
    if v:s['reactions'].add(str(v.reaction));assert v.mesh.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
   view=enc.get_presenter().get_view()
   if view.round!=s['last_round']:
    entry['rounds'].append({'round':view.round,'own_name':str(view.player.name),'opponent_name':str(view.opponent.name),'player_3d':bool(scene.player_visual),'enemy_3d':bool(scene.opponent_visual)});s['last_round']=view.round
    if entry['shots']<3:
     name='Route'+str(len(s['encounters']))+'Round'+str(view.round);unreal.SystemLibrary.execute_console_command(w,'pm.CreatureReview.CaptureLiveUI '+name);entry['shots']+=1
  elif s['in_battle']:
   entry=s['encounters'][-1];assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene);assert not p.is_overworld_input_locked();assert math.dist(entry['start_player'],p.get_actor_location().to_tuple())<.01;entry['end_player']=p.get_actor_location().to_tuple();entry['result']=str(enc.get_last_result().outcome)
  s['in_battle']=active
  if (O/'FootProgress.json').exists() and any(x['name']=='SaveLoad'for x in json.loads((O/'FootProgress.json').read_text())):
   assert str(unreal.load_asset('/Game/Data/Creatures/DA_Zunderlauf').get_display_name())=='Glumanda';s['party_name_after_load']=True
  if (O/'FootTest.json').exists():
   unreal.unregister_slate_post_tick_callback(unreal._glumanda_gameplay_observer);s['reactions']=sorted(s['reactions']);s['passed']=True;(O/'CreatureGameplay.json').write_text(json.dumps(s,indent=2));settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle)
 except Exception:
  import traceback
  unreal.unregister_slate_post_tick_callback(unreal._glumanda_gameplay_observer);s['reactions']=sorted(s['reactions']);s.update(passed=False,error=traceback.format_exc());settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);(O/'CreatureGameplay.json').write_text(json.dumps(s,indent=2));raise
unreal._glumanda_gameplay_observer=unreal.register_slate_post_tick_callback(tick)
