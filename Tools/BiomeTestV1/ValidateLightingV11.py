"""Read-only equality check of copied exterior lights/exposure against untouched VisualV2."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
light_names=['DirectionalLight_Dev','SkyLight_Dev','VS_SoftSkyFill'];props=['intensity','light_color','temperature','use_temperature','indirect_lighting_intensity','cast_shadows','light_source_angle','light_source_soft_angle','shadow_bias','shadow_slope_bias','contact_shadow_length','dynamic_shadow_distance_movable_light','source_type','cubemap','real_time_capture','sky_distance_threshold','lower_hemisphere_is_black','lower_hemisphere_color']
pp_props=['bloom_intensity','auto_exposure_method','auto_exposure_bias','auto_exposure_min_brightness','auto_exposure_max_brightness','white_temp','color_saturation','color_contrast','color_gamma','color_gain','color_offset','dynamic_global_illumination_method','reflection_method','motion_blur_amount']
def value(v):
 if isinstance(v,(float,int,bool,str)):return v
 if hasattr(v,'to_tuple'):return v.to_tuple()
 if isinstance(v,unreal.Object):return v.get_path_name()if v else None
 return str(v)
def snapshot(mapname,prefix,ppname):
 assert unreal.EditorLoadingAndSavingUtils.load_map(mapname);w=E.get_editor_world();actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};out={}
 for label in light_names:
  a=actors[prefix+label];c=a.get_editor_property('light_component');d={'location':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple()}
  for prop in props:
   try:d[prop]=value(c.get_editor_property(prop))
   except Exception:pass
  out[label]=d
 settings=actors[ppname].get_editor_property('settings');out['exterior_postprocess']={}
 for prop in pp_props:
  out['exterior_postprocess'][prop]=value(settings.get_editor_property(prop))
 return out
def equal(a,b):
 if isinstance(a,dict):return a.keys()==b.keys()and all(equal(a[k],b[k])for k in a)
 if isinstance(a,(tuple,list)):return len(a)==len(b)and all(equal(x,y)for x,y in zip(a,b))
 if isinstance(a,(int,float))and isinstance(b,(int,float)):return math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-6)
 return a==b
original=snapshot('/Game/Maps/Dev_TestMap_VisualV2','','V2_OutdoorExposure');biome=snapshot('/Game/Maps/Dev_BiomeTestMap_V1','Biome_','Biome_ApprovedExteriorSettings');assert equal(original,biome),(original,biome);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(R/'Saved/BiomeTestV11/LightingEquality.json').write_text(json.dumps({'passed':True,'source_map':'/Game/Maps/Dev_TestMap_VisualV2','target_map':'/Game/Maps/Dev_BiomeTestMap_V1','exterior_values_equal_with_numeric_tolerance':True,'absolute_numeric_tolerance':1e-6,'source_values':original,'target_values':biome,'excludes':'Explicit local cave channel-1 lights; new geometry naturally casts its own shadows. No GPU benchmark.'},indent=2))
