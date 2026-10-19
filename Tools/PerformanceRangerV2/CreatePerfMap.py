
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/V2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();assert W.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();target='/Game/Maps/Dev_TestMap_RangerPerfV2';assert not unreal.EditorAssetLibrary.does_asset_exist(target);assert unreal.EditorLoadingAndSavingUtils.save_map(W,target);W=E.get_editor_world();v=next(a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if isinstance(a,unreal.PokeMonsterNPCVisualActor));assert v.source_actor.get_actor_label()=='Slice_Wanderer_Hinweis';m=unreal.load_asset('/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2');assert m and m.skeleton==v.visual.get_skeletal_mesh_asset().skeleton;v.visual.set_skeletal_mesh_asset(m);v.refresh_presentation();assert unreal.EditorLoadingAndSavingUtils.save_map(W,target);(O/'PerformanceMap.json').write_text(json.dumps({'map':target,'source_actor':v.source_actor.get_actor_label(),'source_position':v.source_actor.get_actor_location().to_tuple(),'visual_position':v.get_actor_location().to_tuple(),'rotation':str(v.get_actor_rotation()),'new_mesh':m.get_path_name(),'original_map':'Not saved/overwritten'},indent=2))
