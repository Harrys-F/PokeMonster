"""Apply only visually reviewed map-local postprocess overrides; never save the baseline."""

# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV1';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();changes=[]
for v in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume):
 s=v.get_editor_property('settings');unbound=v.get_editor_property('unbound');before={k:s.get_editor_property(k) for k in ['override_bloom_intensity','bloom_intensity','override_motion_blur_amount','motion_blur_amount']}
 s.set_editor_property('override_bloom_intensity',True);s.set_editor_property('override_motion_blur_amount',True)
 if unbound:s.set_editor_property('bloom_intensity',0.0);s.set_editor_property('motion_blur_amount',0.0)
 v.set_editor_property('settings',s);changes.append({'actor':v.get_actor_label(),'unbound':unbound,'before':before,'after':{k:s.get_editor_property(k) for k in before}})
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterEnvironmentRenderProfile)
profile=actors.spawn_actor_from_class(unreal.PokeMonsterEnvironmentRenderProfile,unreal.Vector(0,0,0));assert profile
profile.set_actor_label('EnvironmentPerfV1_RenderOnly');profile.set_editor_property('bEnableHalfResolutionLumenIntegration',True);profile.set_editor_property('bEnableTwoRayDirectionalShadows',True)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(O/'PersistedCandidate.json').write_text(json.dumps({'map':w.get_path_name(),'changes':changes,'persistent_global_render_settings_changed':False,'runtime_scoped_cvars':{'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':2,'r.Shadow.Virtual.SMRT.RayCountDirectional':2},'profile_actor':profile.get_path_name(),'geometry_materials_vegetation_camera_changed':False},indent=2))
