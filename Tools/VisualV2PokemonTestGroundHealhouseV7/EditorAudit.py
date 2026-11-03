"""Read-only V7 bounds/material inventory. No assets or maps saved."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
assert not(D/'SceneBefore.json').exists(),'Original before-snapshot must never be overwritten'
(D/'SceneBefore.json').write_text(json.dumps(scene(W),indent=2))
out={'species':[],'imports':[],'textures':[],'room':[]}
for s in unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species():
 p=s.get_visuals().presentation
 def box(m):
  b=m.get_bounds();return dict(origin=b.origin.to_tuple(),extent=b.box_extent.to_tuple())
 out['species'].append(dict(name=str(s.get_display_name()),id=str(s.get_internal_id()),mesh=p.mesh.get_path_name(),bounds=box(p.mesh),swim_bounds=box(p.swim_mesh)if p.swim_mesh else None,presentation=p.export_text()if hasattr(p,'export_text')else str(p),reference=p.reference_size_cm,offset=p.ground_offset_cm,swim_scale=p.swim_bounds_scale,swim_clip=p.swim_clip.get_path_name()if p.swim_clip else None))
ar=unreal.AssetRegistryHelpers.get_asset_registry();ar.scan_paths_synchronous(['/Game/Characters/Creatures/ModelIntakeV6'],False)
for a in ar.get_assets_by_path('/Game/Characters/Creatures/ModelIntakeV6',True):
 if str(a.asset_class_path.asset_name)=='StaticMesh':out['imports'].append(dict(path=str(a.package_name),size=str(a.get_tag_value('ApproxSize'))))
for a in ar.get_all_assets():
 path=str(a.package_name)
 if str(a.asset_class_path.asset_name)=='Texture2D'and ('Pack_Bonus' in path or 'WoodFloor' in path):out['textures'].append(path)
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 if 16000<a.get_actor_location().x<17700:
  out['room'].append(dict(label=a.get_actor_label(),components=[dict(name=c.get_name(),mesh=c.static_mesh.get_path_name()if c.static_mesh else None,materials=[c.get_material(i).get_path_name()if c.get_material(i)else None for i in range(c.get_num_materials())])for c in a.get_components_by_class(unreal.StaticMeshComponent)]))
(D/'EditorAudit.json').write_text(json.dumps(out,indent=2));print('V7 AUDIT',len(out['species']),len(out['imports']),len(out['textures']))
