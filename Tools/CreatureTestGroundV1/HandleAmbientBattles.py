"""Regression-driver helper only: flee real extra wild battles late in the legacy forest walk.
No encounter creation, forced finish, path/actor teleport, party fixture or asset changes.
Must be attached after starting the existing full route; never needed for normal PIE.
"""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/GlumandaV11/Acceptance'/json.loads((R/'Saved/GlumandaV11/AcceptanceRequest.json').read_text())['label']
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gi=unreal.GameplayStatics.get_game_instance(w);enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi)
result={'test_driver_only':True,'uses_existing_legal_flee':True,'extra_battles':[]};was_active=False;entered=0.;attempts=0
assert not hasattr(unreal,'_ground_ambient_battles')
def tick(dt):
 global was_active,entered,attempts
 try:
  if(O/'FootTest.json').exists():
   unreal.unregister_slate_post_tick_callback(unreal._ground_ambient_battles);delattr(unreal,'_ground_ambient_battles');(O/'AmbientBattles.json').write_text(json.dumps(result,indent=2));return
  path=O/'FootProgress.json'
  if not path.exists():return
  steps=json.loads(path.read_text())
  if not any(x['name']=='NorthEast'for x in steps):return
  active=enc.is_encounter_active()
  if not active:
   if was_active:result['extra_battles'][-1]['result']=str(enc.get_last_result().outcome);(O/'AmbientBattles.json').write_text(json.dumps(result,indent=2))
   was_active=False;return
  pr=enc.get_presenter();v=pr.get_view()
  if not was_active:
   was_active=True;entered=time.monotonic();attempts=0
   result['extra_battles'].append({'opponent':str(v.opponent.name),'position':unreal.GameplayStatics.get_player_pawn(w,0).get_actor_location().to_tuple(),'classic':enc.get_battle_widget().is_classic_presentation(),'menu_flee_enabled':v.flee_enabled})
  assert time.monotonic()-entered<30,'Extra wild battle did not finish'
  if v.finished:return
  if v.busy:
   if v.presentation_pending:pr.finish_presentation()
   return
  assert v.flee_enabled,'Never bypass trainer/story flee restrictions';assert attempts<3
  assert pr.try_select_flee();assert pr.resolve_selection();attempts+=1;pr.finish_presentation()
 except Exception:
  unreal.unregister_slate_post_tick_callback(unreal._ground_ambient_battles);delattr(unreal,'_ground_ambient_battles');result['error']=traceback.format_exc();(O/'AmbientBattles.json').write_text(json.dumps(result,indent=2));unreal.log_error(result['error'])
unreal._ground_ambient_battles=unreal.register_slate_post_tick_callback(tick)
