"""Read-only runtime camera and notice-radius diagnosis; only task-owned Saved output."""
import unreal,json
from pathlib import Path
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0)
rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):
 m=a.overworld_movement;b=m.get_behavior_profile();rows.append({'species':str(a.visual_species.get_internal_id()),'position':a.get_actor_location().to_tuple(),'notice':b.notice_radius,'personal':b.personal_space,'disengage':b.disengage_radius,'state':str(m.behavior_state)})
cam=unreal.GameplayStatics.get_player_camera_manager(W,0)
Path(unreal.Paths.project_dir(),'Saved/ProjectRefinement/PokemonAIV21ExperienceV1/Inspect.json').write_text(json.dumps({'player':P.get_actor_location().to_tuple(),'camera':cam.get_camera_location().to_tuple(),'rotation':cam.get_camera_rotation().to_tuple(),'actors':rows},indent=2))
