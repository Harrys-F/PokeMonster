"""Minimal staged cleanup probe; separates ordinary menu use from QHD capture."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WorldClockV1';q=json.loads((D/'Request.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False);Ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=Ed.get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);Save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);assert Save.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_WorldClockV1'+q['label']);P.set_actor_location(unreal.Vector(-200,-100,50.15),False,True)
s={'stage':0,'last':time.monotonic()};r={'mode':q.get('probe','capture'),'checks':[]}
def tick(dt):
 try:
  if time.monotonic()-s['last']<1:return
  stage=s['stage'];(O/'Progress.json').write_text(json.dumps({'stage':stage,'mode':r['mode']}))
  if stage==0:PC.toggle_main_menu()
  elif stage==1:
   if r['mode']=='capture':unreal.SystemLibrary.execute_console_command(W,'pm.CreatureReview.CaptureLiveUI WorldClock'+q['label']+' qhd',PC)
   PC.close_menu()
  elif stage==2:unreal.SystemLibrary.collect_garbage()
  elif stage==3:r['checks'].append('First cleanup after ordinary menu/capture survived')
  elif stage==4:unreal.unregister_slate_post_tick_callback(unreal._clock_cleanup);r['passed']=True;(O/'Result.json').write_text(json.dumps(r,indent=2))
  s['stage']+=1;s['last']=time.monotonic()
 except Exception:
  unreal.unregister_slate_post_tick_callback(unreal._clock_cleanup);r.update(passed=False,error=traceback.format_exc());(O/'Result.json').write_text(json.dumps(r,indent=2))
unreal._clock_cleanup=unreal.register_slate_post_tick_callback(tick)
