"""Validate saved PP settings, then exercise unchanged real movement and gameplay."""
import unreal,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2MaterialFixV1';j=json.loads((O/'AcceptanceRequest.json').read_text());dest=O/'Acceptance'/j['label'];w=next(x for x in unreal.ObjectIterator(unreal.World) if x.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(x,0))
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf.Viewport '+str(j['width'])+' '+str(j['height']));unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage '+str(j['percentage']))
p=unreal.GameplayStatics.get_player_pawn(w,0);c=p.get_component_by_class(unreal.CameraComponent);a=p.get_component_by_class(unreal.SpringArmComponent)
assert a.target_arm_length==2850 and c.field_of_view==35
volumes={v.get_actor_label():v for v in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume)};outside=volumes['V2_OutdoorExposure'];inside=volumes['V2_House_HH_Art_InteriorLighting'];assert outside.settings.override_motion_blur_amount and outside.settings.motion_blur_amount==0;assert inside.settings.override_motion_blur_amount and inside.settings.motion_blur_amount==.5;assert inside.priority>outside.priority
names=['r.MotionBlurQuality','r.BloomQuality','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Lumen.FinalGatherMethod','r.Shadow.Virtual.SMRT.RayCountDirectional','r.DefaultFeature.MotionBlur'];values={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in names};assert values['r.MotionBlurQuality']>0 and values['r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor']==1;assert values['r.Shadow.Virtual.SMRT.RayCountDirectional']==(4 if j['quality']==1 else 8)
(dest/'Graphics.json').write_text(json.dumps({'request':j,'viewport':list(unreal.GameplayStatics.get_player_controller(w,0).get_viewport_size()),'camera_distance_cm':a.target_arm_length,'camera_fov':c.field_of_view,'camera_postprocess_motion_override':c.post_process_settings.override_motion_blur_amount,'cvars':values,'outdoor_motion_amount':outside.settings.motion_blur_amount,'indoor_motion_amount':inside.settings.motion_blur_amount},indent=2));exec(compile((R/'Tools/VisualV2QualityV2/FootTest.py').read_text().replace('Saved/VisualV2QualityV2','Saved/VisualV2MaterialFixV1'),'tracked_FootTest_adapter','exec'),globals())
# Additional read-only sky inventory; not a rendering change.
skies=[]
for c in unreal.ObjectIterator(unreal.SkyLightComponent):
 if c.get_world()!=w:continue
 row={'component':c.get_path_name(),'properties':{}}
 for n in ['mobility','intensity','real_time_capture','source_type','cubemap_resolution','cast_shadows']:
  try:row['properties'][n]=str(c.get_editor_property(n))
  except Exception:pass
 skies.append(row)
(dest/'SkyLight.json').write_text(json.dumps(skies,indent=2))
