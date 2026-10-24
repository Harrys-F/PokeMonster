"""Inspect saved sandbox dependencies, habitat configuration and original camera-material opt-ins."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();assert w.get_name()=='Dev_BiomeTestMap_V1'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
AR=unreal.AssetRegistryHelpers.get_asset_registry();opt=unreal.AssetRegistryDependencyOptions(include_hard_package_references=True,include_soft_package_references=True,include_searchable_names=False,include_hard_management_references=False,include_soft_management_references=False)
seen=set();pending=['/Game/Maps/Dev_BiomeTestMap_V1'];missing=[]
while pending:
 p=pending.pop()
 if p in seen:continue
 seen.add(p)
 for d in AR.get_dependencies(p,opt):
  d=str(d)
  if d.startswith('/Game/'):
   if not unreal.EditorAssetLibrary.does_asset_exist(d):missing.append(d)
   elif d not in seen:pending.append(d)
rows=[];counts={};trees=0;inst=0
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 counts[a.get_class().get_name()]=counts.get(a.get_class().get_name(),0)+1
 for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):inst+=c.get_instance_count()
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if c.static_mesh and c.static_mesh.get_name()in['SM_WLA_OakAncient_V3','SM_WLA_Birch_A']:trees+=1
 if isinstance(a,unreal.PokeMonsterBiomeHabitat):
  rows.append({'name':a.habitat_name,'medium':str(a.medium),'position_world_cm':a.get_actor_location().to_tuple(),'half_extent_cm':a.bounds.get_unscaled_box_extent().to_tuple(),'clearance_radius_cm':a.clearance_radius_cm,'draft_cm':a.water_draft_cm,'ground_flight_enabled':a.get_editor_property('bAllowGroundFlight'),'travel_points':[x.to_tuple()for x in a.travel_points],'specimens':[{'species':s.species.get_path_name(),'diagnostic_only':s.get_editor_property('bWaterDiagnostic'),'size_cm':s.species.get_visuals().presentation.reference_size_cm,'local_position_cm':s.local_position.to_tuple(),'visual_validation':list(s.species.get_visuals().presentation.get_validation_errors())}for s in a.specimens]})
r={'map':w.get_path_name(),'game_mode':w.get_world_settings().default_game_mode.get_path_name(),'actor_classes':counts,'trees':trees,'botanical_instances':inst,'dependencies':sorted(seen),'missing_dependencies':sorted(set(missing)),'habitats':rows,'dirty_maps':[],'dirty_content':[]}
assert not missing and all(not s['visual_validation']for h in rows for s in h['specimens']);(R/'Saved/BiomeTestV1/AssetAudit.json').write_text(json.dumps(r,indent=2))
