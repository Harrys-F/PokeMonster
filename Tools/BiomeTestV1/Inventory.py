"""Read-only source-scene and reusable asset inventory. No existing asset/map saves."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 if isinstance(a,(unreal.DirectionalLight,unreal.SkyLight,unreal.PostProcessVolume,unreal.SkyAtmosphere,unreal.ExponentialHeightFog)):
  d={'label':a.get_actor_label(),'class':a.get_class().get_path_name(),'location':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple()}
  for p in ['light_component','component','settings','unbound','blend_radius','priority']:
   try:
    v=a.get_editor_property(p)
    if isinstance(v,unreal.Object):
     d[p]={}
     for k in ['intensity','light_color','temperature','use_temperature','source_angle','indirect_lighting_intensity','cast_shadows','mobility','volumetric_scattering_intensity','real_time_capture','lower_hemisphere_is_black','sky_distance_threshold','fog_density','fog_height_falloff']:
      try:d[p][k]=str(v.get_editor_property(k))
      except Exception:pass
    else:d[p]=str(v)
   except Exception:pass
  rows.append(d)
assets={}
for p in unreal.EditorAssetLibrary.list_assets('/Game/Environment',recursive=True,include_folder=False):
 if any(t in p for t in ['OakAncient_V3','SM_WLA_Birch_A.','SM_WLA_Boulder_A.','SM_WLA_Boulder_B.','WR_WoodBridge.','WR_StoneBridge.','M_OrganicWater.','T_HA4','T_WA5_Forest','T_WA5_WetBank','M_WAQ2_PlantVertexColour.']):
  a=unreal.load_asset(p);d={'class':a.get_class().get_name()}
  if isinstance(a,unreal.StaticMesh):d.update(bounds=[x.to_tuple()for x in [a.get_bounding_box().min,a.get_bounding_box().max]],materials=[s.material_interface.get_path_name()if s.material_interface else None for s in a.static_materials])
  if isinstance(a,unreal.Material):d['custom']=[n.get_editor_property('code')for n in unreal.MaterialEditingLibrary.get_material_expressions(a)if isinstance(n,unreal.MaterialExpressionCustom)]
  assets[p]=d
pokemon={}
for name in ['Bisasam','Pikachu','Glurak','Schiggy','Enton','Machomei','Glutexo','Nebulak','Gengar']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);p=s.get_visuals().presentation
 pokemon[name]={'size_cm':p.reference_size_cm,'ground_offset':p.ground_offset_cm,'walk':p.walk_speed,'run':p.run_speed,'bounds':[p.mesh.get_bounds().origin.to_tuple(),p.mesh.get_bounds().box_extent.to_tuple()],'hover':p.get_editor_property('bAllowGroundHover'),'float':p.overworld_float_amplitude_cm,'validation':list(p.get_validation_errors())}
(R/'Saved/BiomeTestV1/Inventory.json').write_text(json.dumps({'lights':rows,'assets':assets,'pokemon':pokemon},indent=2))
