
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();assert w.get_path_name()=='/Game/Maps/Dev_TestMap_NPCMotionV2.Dev_TestMap_NPCMotionV2';a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);v=next(x for x in a.get_all_level_actors() if isinstance(x,unreal.PokeMonsterNPCVisualActor) and x.source_actor);src=v.source_actor
before=json.loads((O/'MapBefore.json').read_text());assert src.get_actor_location().to_tuple()==tuple(before['position']);assert src.dialogue.get_path_name()==before['dialogue'];assert str(src.display_name)==before['display_name']
v.visual.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/RangerMotionV2/Meshes/SK_Ranger_AQV2'))
for prop,clip in [('idle_animation','Idle'),('walk_animation','Walk'),('conversation_animation','Talk'),('turn_left_animation','TurnLeft'),('turn_right_animation','TurnRight')]:v.set_editor_property(prop,unreal.load_asset('/Game/Characters/NPCs/RangerMotionV2/Animations/A_Ranger_'+clip+'_AQV2'))
v.set_editor_property('bEnableMotionPresentation',True);v.set_editor_property('bEnableAccessoryMotion',True);v.set_editor_property('authored_walk_speed',150.);v.set_actor_label('NPCVisual_Wanderer_AnimationQuality_V2');v.refresh_presentation()
unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_NPCMotionV2')
(O/'MapConfigured.json').write_text(json.dumps({'map':w.get_path_name(),'source_position':src.get_actor_location().to_tuple(),'source_dialogue':src.dialogue.get_path_name(),'source_name':str(src.display_name),'source_identity_retained':True,'visual':v.get_path_name(),'mesh':v.visual.get_skeletal_mesh_asset().get_path_name(),'authored_walk_speed':v.authored_walk_speed,'original_wanderer_patrol':'None; source gameplay unchanged','preview_driver':'Spawned only by explicit runtime test; no permanent NPC or route'},indent=2))
