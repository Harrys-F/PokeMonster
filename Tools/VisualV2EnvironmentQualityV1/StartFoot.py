import unreal,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2EnvironmentQualityV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2EnvironmentQualityV1'
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf.Viewport 2560 1440')
# Combined runtime regression only; not a performance comparison or saved map preset.
names={'r.ScreenPercentage':75,'r.MotionBlurQuality':0,'r.BloomQuality':0,'r.Shadow.Virtual.SMRT.RayCountDirectional':2,'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':2}
before={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names};(O/'FootCvarsBefore.json').write_text(json.dumps(before,indent=2))
for n,v in names.items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
player=unreal.GameplayStatics.get_player_pawn(w,0);arm=player.get_component_by_class(unreal.SpringArmComponent);camera=player.get_component_by_class(unreal.CameraComponent);capsule=player.get_component_by_class(unreal.CapsuleComponent)
assert arm.target_arm_length==2850 and camera.field_of_view==35
(O/'FootGraphics.json').write_text(json.dumps({'camera_distance_cm':arm.target_arm_length,'fov':camera.field_of_view,'capsule_radius_cm':capsule.get_unscaled_capsule_radius(),'capsule_half_height_cm':capsule.get_unscaled_capsule_half_height(),'viewport':list(unreal.GameplayStatics.get_player_controller(w,0).get_viewport_size()),'values':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names}},indent=2))
runpy.run_path(str(R/'Tools/VisualV2EnvironmentQualityV1/FootTest.py'),run_name='__main__')
