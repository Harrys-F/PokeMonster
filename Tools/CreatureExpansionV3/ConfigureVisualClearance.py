"""Only new expansion species: clearance for original appendages, no new physical colliders."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();specs=json.loads((R/'Tools/CreatureExpansionV3/Species.json').read_text());rows=[]
for name,spec in specs.items():
 species=unreal.load_asset('/Game/Data/Creatures/DA_'+name);settings=species.get_editor_property('overworld');before=settings.body_radius;settings.set_editor_property('body_radius',float(spec['navigation_radius']));species.set_editor_property('overworld',settings);assert unreal.EditorAssetLibrary.save_loaded_asset(species,False);rows.append({'species':name,'before':before,'navigation_clearance_cm':spec['navigation_radius'],'contact_capsule_radius_cm':spec['radius']})
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(R/'Saved/CreatureExpansionV3/VisualClearance.json').write_text(json.dumps(rows,indent=2))
