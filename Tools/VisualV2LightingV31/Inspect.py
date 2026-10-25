"""Read-only map-specific lighting, exposure, AO and renderer audit."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/LightingV31';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
assert not(D/'BeforeScene.json').exists();(D/'BeforeScene.json').write_text(json.dumps(scene(W),indent=2));out={'lights':[],'postprocess':[],'renderer':{}}
props=['intensity','light_color','use_temperature','temperature','light_source_angle','shadow_amount','cast_shadows','cast_static_shadows','cast_dynamic_shadows','indirect_lighting_intensity','volumetric_scattering_intensity','affects_world','mobility','lighting_channels','source_type','cubemap','real_time_capture','lower_hemisphere_is_black','lower_hemisphere_color','occlusion_max_distance','occlusion_contrast','occlusion_exponent','min_occlusion','occlusion_tint','transmission','samples_per_pixel']
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.LightComponentBase):
  row={'actor':a.get_name(),'label':a.get_actor_label(),'class':c.get_class().get_name(),'transform':str(a.get_actor_transform()),'props':{}}
  for p in props:
   try:
    v=c.get_editor_property(p);row['props'][p]=v.get_path_name()if isinstance(v,unreal.Object)else v.export_text()if hasattr(v,'export_text')else str(v)
   except Exception:pass
  out['lights'].append(row)
 if isinstance(a,unreal.PostProcessVolume):
  row={'actor':a.get_name(),'label':a.get_actor_label(),'unbound':a.get_editor_property('unbound'),'settings':{}}
  for p in ['auto_exposure_method','auto_exposure_min_brightness','auto_exposure_max_brightness','auto_exposure_bias','auto_exposure_apply_physical_camera_exposure','ambient_occlusion_intensity','ambient_occlusion_radius','ambient_occlusion_power','ambient_occlusion_static_fraction','ambient_occlusion_quality','dynamic_global_illumination_method','lumen_scene_lighting_quality','lumen_final_gather_quality','indirect_lighting_intensity','color_gamma','color_gain','film_slope','film_toe','film_shoulder']:
   try:row['settings'][p]=str(a.settings.get_editor_property(p))
   except Exception:pass
  out['postprocess'].append(row)
for v in ['r.SkyLightingQuality','r.Lumen.DiffuseIndirect.Allow','r.Lumen.ScreenProbeGather.IrradianceFieldGather','r.Shadow.Virtual.Enable','r.AmbientOcclusionLevels','r.DistanceFieldAO','r.EyeAdaptationQuality','r.DefaultFeature.AutoExposure','r.TonemapperGamma','r.SSR.Quality','sg.GlobalIlluminationQuality','sg.ShadowQuality']:
 out['renderer'][v]=unreal.SystemLibrary.get_console_variable_float_value(v)
(D/'Inspection.json').write_text(json.dumps(out,indent=2));unreal.log('LIGHT_V31_INSPECTED')
