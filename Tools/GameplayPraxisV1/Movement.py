"""Existing native recorder: player walk/sprint/stop in eight directions, fixed normal camera."""
import unreal,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0)
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True);a.set_actor_enable_collision(False)
original_mode=P.is_sprint_mode_enabled()
def l3():
 for state in ['down','up']:unreal.SystemLibrary.execute_console_command(W,'pm.Input.Key Gamepad_LeftThumbstick '+state)
if original_mode:l3()
source=(R/'Tools/VisualV2EnvironmentV3/Motion.py').read_text().replace('Saved/ProjectRefinement/EnvironmentV3/MotionFinal','Saved/ProjectRefinement/GameplayPraxisV1/Movement01/Motion').replace("clips=[('Grass',-2100,-1760),('Water',-350,-130)]","clips=[('PlayerMovement',-2100,-1760)]").replace('EnvironmentV3_Final_','GameplayPraxisV1_')
source=source.replace("cmd('pm.EnvPerf2.Viewport 2560 1440')", "cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100')")
old="""   if t<1.4:axis(.7,0)
   elif t<2.8:axis(-.7,0)
   elif t<4.0:axis(0,.7)
   elif t<5.:axis(0,-.7)
   else:"""
new="""   if t<8:
    if t>=4 and not P.is_sprint_mode_enabled():l3()
    a=int((t%4)/.5)*math.pi/4;axis(math.sin(a),math.cos(a))
   elif t<9:
    axis(0,0)
    if P.is_sprint_mode_enabled():l3()
   else:"""
assert old in source;source=source.replace(old,new).replace(" axis(0,0);cmd('pm.TAAReview.CaptureStop')", " axis(0,0)\n if P.is_sprint_mode_enabled()!=original_mode:l3()\n cmd('pm.TAAReview.CaptureStop')")
exec(compile(source,'existing_native_player_motion_evidence','exec'),globals())
