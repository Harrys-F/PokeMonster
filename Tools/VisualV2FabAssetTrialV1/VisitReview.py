"""Exercise all six documented PIE visits and the existing RAM-protected return."""
import unreal,runpy,json,time,traceback,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';O=D/'VisitReview';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W;P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);original=P.get_actor_location().to_tuple();party=[x.export_text()for x in E.get_player_party()];sites=['Blumenwiese','Waldrand','Flussufer','Felsgruppe','Kraeutergarten','Lebensraum','Zurueck'];rows=[];s={'i':0,'at':time.monotonic()};start=time.monotonic()
def tick(dt):
 try:
  if time.monotonic()-s['at']<1.5:return
  if s['i']>=len(sites):
   assert math.dist(original,P.get_actor_location().to_tuple())<.1;assert party==[x.export_text()for x in E.get_player_party()];(O/'Result.json').write_text(json.dumps(dict(passed=True,visits=rows,party_and_return_anchor_restored=True),indent=2));unreal.unregister_slate_post_tick_callback(unreal._fat_visits);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play();return
  area=sites[s['i']];runpy.run_path(str(R/'Tools/VisualV2FabAssetTrialV1/Visit.py'),init_globals={'AREA':area});rows.append(dict(area=area,position=P.get_actor_location().to_tuple()));s.update(i=s['i']+1,at=time.monotonic())
 except Exception:
  (O/'Result.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc(),visits=rows),indent=2));unreal.unregister_slate_post_tick_callback(unreal._fat_visits);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
unreal._fat_visits=unreal.register_slate_post_tick_callback(tick)
