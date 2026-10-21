"""Reopen audit; fit only the two new species' 2D fallback to their smaller capsules."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/StarterExpansionV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not(O/'WildPlacementReopened.json').exists();rows=[];changed=False
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):
 ident=str(a.encounter_id)
 if ident not in ['Dev_Schiggy_Wild_01','Dev_Bisasam_Wild_01']:continue
 body=a.get_component_by_class(unreal.CapsuleComponent);sprite=a.get_component_by_class(unreal.PaperSpriteComponent);target=unreal.Vector(0,0,15-body.get_scaled_capsule_half_height());before=sprite.get_editor_property('relative_location');assert before in [unreal.Vector(0,0,-45),target]
 if before!=target:sprite.set_relative_location(target,False,False);changed=True
 species=a.visual_species;assert species.get_visuals().presentation and not species.get_visuals().presentation.get_validation_errors();assert a.ambient_motion;rows.append({'id':ident,'species':species.get_path_name(),'position':a.get_actor_location().to_tuple(),'fallback_floor_height':body.get_scaled_capsule_half_height()+sprite.get_editor_property('relative_location').z})
assert len(rows)==2
if changed:assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(O/'WildPlacementReopened.json').write_text(json.dumps(rows,indent=2));unreal.log('STARTER_PLACEMENT_REOPENED_PASS')
