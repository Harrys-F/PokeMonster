"""Read-only editor/PIE inventory. Never saves maps, sources or a game."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/PokemonAIV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world()or E.get_editor_world()
rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):
 m=a.overworld_movement
 rows.append({'label':a.get_actor_label(),'id':str(a.encounter_id),'species':str(a.visual_species.get_internal_id())if a.visual_species else None,'position':a.get_actor_location().to_tuple(),'ambient':a.get_editor_property('ambient_motion'),'activities':m.activities.export_text(),'enabled':m.activities_enabled,'behavior':m.get_behavior_profile().export_text(),'radius':m.habitat_radius_override,'tick':m.is_component_tick_enabled()})
(O/('PIEInventory.json'if E.get_game_world()else'EditorInventory.json')).write_text(json.dumps(rows,indent=2));unreal.log('POKEMON_AI_INVENTORY '+str(len(rows)))
