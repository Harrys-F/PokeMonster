"""Explicit UNSAVED three-starter party fixture, independent of ordinary-PIE availability proof.
Run only in a fresh PIE. Stop PIE afterwards; never writes a save or asset.
"""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/TestGroundV1';out=O/'CompanionProbe.json';assert not out.exists()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi)
g=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==w)
c=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w)
assert not e.is_encounter_active()and not p.is_overworld_input_locked()and len(g.specimens)==10
f=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(f.read_bytes()).hexdigest();origin=p.get_actor_location();result={'explicit_unsaved_party_fixture':True,'checks':[]};started=time.monotonic();phase=0;deadline=0
unreal.SystemLibrary.execute_console_command(w,'pm.StarterReview.Party Zunderlauf Schiggy Bisasam')
ids=[x.instance_id.to_string()for x in e.get_player_party()];assert len(ids)==3;assert g.visit(3)
def verify():
 visuals=[x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor)if x.actor_has_tag('CreaturePartyCompanion')]
 assert len(g.specimens)==10 and len(visuals)==1 and c.get_visual()==visuals[0]
 assert [x.instance_id.to_string()for x in e.get_player_party()]==ids
 assert not e.is_encounter_active();return(visuals[0].get_actor_location()-p.get_actor_location()).length()
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._testground_companion_probe);delattr(unreal,'_testground_companion_probe')
 result.update(passed=error is None,error=error,save_unchanged=hashlib.sha256(f.read_bytes()).hexdigest()==sha);out.write_text(json.dumps(result,indent=2))
def tick(dt):
 global phase,deadline
 try:
  t=unreal.GameplayStatics.get_time_seconds(w)
  if time.monotonic()-started>90:raise TimeoutError()
  if t<deadline:return
  if phase==0:
   if not c.get_visual():return
   distance=verify();assert distance<600;result['checks'].append('One existing 3D companion alongside ten independent specimens');result['companion_distance_cm']=distance
   assert g.react('faint');phase=1;deadline=t+3
  elif phase==1:
   verify();result['checks'].append('Test faint reaction changes no party member and triggers no battle');assert g.return_to_world();phase=2;deadline=t+2
  else:
   verify();assert(p.get_actor_location()-origin).length()<3;result['checks'].append('Companion resumes near original return location; same three party IDs');finish()
 except Exception:finish(traceback.format_exc())
unreal._testground_companion_probe=unreal.register_slate_post_tick_callback(tick)
