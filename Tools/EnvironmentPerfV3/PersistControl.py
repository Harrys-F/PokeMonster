
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV3'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterEnvironmentRenderProfileV3)
# Preserve the measured V2 renderer state on the new exact-name-guarded world.
# No LOD candidate is adopted: worst-case QHD did not show a reliable gain.
p=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_class(unreal.PokeMonsterEnvironmentRenderProfileV3,unreal.Vector(0,0,-10000));p.set_actor_label('EnvironmentPerfV3_RevalidatedV2Profile')
values={'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':'2','r.Shadow.Virtual.SMRT.RayCountDirectional':'2','r.Lumen.FinalGatherMethod':'0','r.Lumen.HardwareRayTracing':'0'};p.set_editor_property('renderer_overrides',values)
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_EnvironmentPerfV3')
(O/'PersistedState.json').write_text(json.dumps({'map':w.get_path_name(),'renderer_overrides':values,'new_vegetation_settings_adopted':False,'minimum_lod_test_rejected':True,'reason':'No consistent gain, including native QHD High 100; preserve geometry quality','actor':p.get_actor_label()},indent=2))
