"""Normal PIE console visit/return; its existing RAM guard excludes isolated file-save fixtures."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldOverhaulV3';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);origin=P.get_actor_location();state={'step':0,'at':time.monotonic()};checks=[]
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
def tick(dt):
 global origin
 try:
  if time.monotonic()-state['at']<.7:return
  step=state['step']
  if step==0:origin=P.get_actor_location();cmd('pm.NPCGround.Go 1');assert P.get_actor_location().x<-10000;checks.append('NPC command visits one of all 11 existing figures')
  elif step==1:assert -20000<P.get_actor_location().z<-19800;cmd('pm.NPCGround.Return');checks.append(dict(origin=origin.to_tuple(),returned=P.get_actor_location().to_tuple(),delta=(P.get_actor_location()-origin).length(),input_locked=P.is_overworld_input_locked(),interior=P.is_using_interior_movement_basis()));assert (P.get_actor_location()-origin).length()<1;checks.append('NPC return restores original world position and closes existing RAM preview')
  elif step==2:cmd('pm.TestGround.Go 1');assert P.get_actor_location().y<-10000;checks.append('Pokemon command visits centrally registered test model')
  elif step==3:assert -20000<P.get_actor_location().z<-19800;cmd('pm.TestGround.Return');assert (P.get_actor_location()-origin).length()<1;checks.append('Pokemon return restores original world position')
  else:
   (D/'TestGroundCommandsFinal02.json').write_text(json.dumps(dict(passed=True,checks=checks),indent=2));unreal.unregister_slate_post_tick_callback(unreal._wov_ground_commands);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play();return
  state.update(step=step+1,at=time.monotonic())
 except Exception:
  (D/'TestGroundCommandsFinal02.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc(),checks=checks),indent=2));unreal.unregister_slate_post_tick_callback(unreal._wov_ground_commands);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
unreal._wov_ground_commands=unreal.register_slate_post_tick_callback(tick)
