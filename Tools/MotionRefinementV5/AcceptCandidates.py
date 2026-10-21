"""Explicit reviewed visual-only profile adoption. No map, species identity or save writes."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
initial=json.loads((R/'Saved/MotionRefinementV5/InitialState.json').read_text());receipt=json.loads((R/'Saved/MotionRefinementV5/Import.json').read_text());rows=[]
# Validate the entire two-asset scope before any mutation.
for row in receipt['models']:
 name=row['species'];assert name in ['Glurak','Nebulak'];path='Content/Data/Creatures/DA_'+name+'.uasset';assert hashlib.sha256((R/path).read_bytes()).hexdigest()==initial['originals'][path]
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);old=s.visuals.presentation;new=unreal.load_asset(row['profile']);assert old.get_path_name()==row['previous'];assert not new.get_validation_errors();assert unreal.PokeMonsterCreaturePolishLibrary.have_matching_reference_skeleton(new.mesh,old.mesh)
 assert new.reference_size_cm==old.reference_size_cm and new.walk_speed==old.walk_speed and new.run_speed==old.run_speed and new.ground_offset_cm==old.ground_offset_cm
 rows.append((s,new,str(s.get_internal_id()),old.get_path_name()))
for s,new,identity,previous in rows:
 v=s.visuals;v.set_editor_property('presentation',new);s.set_editor_property('visuals',v);assert str(s.get_internal_id())==identity;assert unreal.EditorAssetLibrary.save_loaded_asset(s,False)
(R/'Saved/MotionRefinementV5/Adoption.json').write_text(json.dumps([dict(species=str(s.get_internal_id()),old=old,new=new.get_path_name(),only_visual_profile_changed=True)for s,new,identity,old in rows],indent=2))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
