"""Read current editor/PIE encounter configuration without saving a package."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world() or E.get_editor_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):
 m=a.overworld_movement;b=a.get_component_by_class(unreal.CapsuleComponent)
 rows.append({'name':a.get_actor_label(),'id':str(a.encounter_id),'position':a.get_actor_location().to_tuple(),'species':str(a.visual_species),'profile':str(a.profile),'ambient':a.ambient_motion,'group':a.group_size,'radius':m.habitat_radius_override,'extent':m.habitat_half_extent.to_tuple(),'life':str(a.life_state),'body':[b.get_scaled_capsule_radius(),b.get_scaled_capsule_half_height()],'override':m.override_behavior,'behavior':str(m.get_behavior_profile().temperament) if E.get_game_world() else None})
out={'world':w.get_name(),'pie':bool(E.get_game_world()),'wild':rows,'dirty_maps':[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]};(R/'Saved/WildEncountersV2/Inspection.json').write_text(json.dumps(out,indent=2));unreal.log(str(out))
