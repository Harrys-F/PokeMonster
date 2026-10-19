
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P=R/'Art/Characters/NPCs/Ranger/Review/V2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert 'Dev_TestMap_RangerPerfV2.' in w.get_path_name();a=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor);baseline=unreal.load_asset('/Game/Maps/Dev_TestMap_VisualV2');b=unreal.GameplayStatics.get_all_actors_of_class(baseline,unreal.Actor)
def snap(actors):
 return {x.get_actor_label():{'class':x.get_class().get_path_name(),'position':x.get_actor_location().to_tuple(),'rotation':x.get_actor_rotation().to_tuple(),'scale':x.get_actor_scale3d().to_tuple()} for x in actors if x.get_actor_label() not in ['WorldSettings']}
sa=snap(a);sb=snap(b);diff={k:[sb.get(k),sa.get(k)] for k in set(sa)|set(sb) if sa.get(k)!=sb.get(k)};v=next(x for x in a if isinstance(x,unreal.PokeMonsterNPCVisualActor));out={'map':w.get_path_name(),'actor_count':len(a),'baseline_actor_count':len(b),'actor_transform_differences':diff,'visual_mesh':v.visual.get_skeletal_mesh_asset().get_path_name(),'visual_collision':str(v.visual.get_collision_enabled()),'skeleton':v.visual.get_skeletal_mesh_asset().skeleton.get_path_name(),'idle':v.idle_animation.get_path_name(),'talk':v.conversation_animation.get_path_name(),'source_actor':v.source_actor.get_actor_label(),'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]};(P/'FinalMapAudit.json').write_text(json.dumps(out,indent=2));unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');unreal.SystemLibrary.execute_console_command(w,'pm.Perf.AuditLODs')
