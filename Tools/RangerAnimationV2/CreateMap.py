
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
target='/Game/Maps/Dev_TestMap_NPCMotionV2';assert not unreal.EditorAssetLibrary.does_asset_exist(target)
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');w=e.get_editor_world();assert w.get_path_name().endswith('Dev_TestMap_VisualV2.Dev_TestMap_VisualV2')
source=next(x for x in a.get_all_level_actors() if x.get_actor_label()=='Slice_Wanderer_Hinweis');v=next(x for x in a.get_all_level_actors() if isinstance(x,unreal.PokeMonsterNPCVisualActor) and x.source_actor==source)
snap={'source':source.get_path_name(),'position':source.get_actor_location().to_tuple(),'rotation':source.get_actor_rotation().to_tuple(),'dialogue':source.dialogue.get_path_name(),'display_name':str(source.display_name),'visual':v.get_path_name(),'visual_location':v.get_actor_location().to_tuple(),'visual_rotation':v.get_actor_rotation().to_tuple(),'visual_mesh':v.visual.get_skeletal_mesh_asset().get_path_name(),'idle':v.idle_animation.get_path_name(),'talk':v.conversation_animation.get_path_name(),'actors':len(a.get_all_level_actors())}
assert unreal.EditorLoadingAndSavingUtils.save_map(w,target);assert unreal.EditorLoadingAndSavingUtils.load_map(target)
(O/'MapBefore.json').write_text(json.dumps(snap,indent=2));unreal.log('NPC_MOTION_MAP_CREATED')
