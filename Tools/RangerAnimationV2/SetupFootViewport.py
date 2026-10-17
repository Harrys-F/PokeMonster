import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/RangerAnimationV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_NPCMotionV2'
p=unreal.GameplayStatics.get_player_pawn(w,0);arm=p.get_component_by_class(unreal.SpringArmComponent);camera=p.get_component_by_class(unreal.CameraComponent)
assert arm.target_arm_length==2850 and camera.field_of_view==35
unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion2.Viewport 2560 1440')
(O/'FootProfileActive.json').write_text(json.dumps({'map':w.get_path_name(),'distance':arm.target_arm_length,'fov':camera.field_of_view,'renderer_values':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing']}},indent=2))
