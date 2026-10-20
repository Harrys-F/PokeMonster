"""Only the existing species' Presentation reference changes. All other values are compared."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/MeshyGlumandaV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
review=json.loads((O/'RuntimeReviewCandidateFinal/Result.json').read_text());assert review['passed'] and review['native_run_max_blend']>.95
s=unreal.load_asset('/Game/Data/Creatures/DA_Zunderlauf');d=unreal.load_asset('/Game/Characters/Creatures/Zunderlauf/MeshyV1/DA_Glumanda_Presentation');assert not d.get_validation_errors()
v=s.get_editor_property('visuals');old=v.get_editor_property('presentation');assert old.get_path_name()=='/Game/Characters/Creatures/Zunderlauf/DA_Zunderlauf_Presentation.DA_Zunderlauf_Presentation'
def state():
 return {k:str(s.get_editor_property(k)) for k in ['internal_id','display_name','pokedex_number','base_capture_rate','primary_type','secondary_type','base_stats','gender','starting_level','growth_rate','evolutions']}|{'other_visuals':{k:str(v.get_editor_property(k)) for k in ['front_flipbook','back_flipbook','overworld_flipbook'] if hasattr(v,k)}}
before=state();v.set_editor_property('presentation',d);s.set_editor_property('visuals',v);assert state()==before;assert str(s.get_internal_id())=='Zunderlauf';assert unreal.EditorAssetLibrary.save_loaded_asset(s,False)
(O/'Binding.json').write_text(json.dumps({'species':s.get_path_name(),'old_presentation':old.get_path_name(),'new_presentation':d.get_path_name(),'unchanged_species_values':before,'map_saved':False,'one_visual_reference_changed':True},indent=2));unreal.log('MESHY_GLUMANDA_SPECIES_VISUAL_ONLY_BOUND')
