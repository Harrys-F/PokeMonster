
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/TreeShadowProxyV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_TreeShadowProxyV1'
actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor);trees=[next(a for a in actors if a.get_actor_label()=='V2_ForestOak_'+str(i)).static_mesh_component for i in range(3)];helpers=[a.static_mesh_component for a in actors if a.get_actor_label().startswith('TSP_')];assert len(helpers)==6 and all(not c.cast_shadow for c in trees);assert all(c.cast_shadow and c.get_editor_property('cast_hidden_shadow') and c.get_editor_property('hidden_in_game') and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION for c in helpers)
d={'map':w.get_path_name(),'game_world':False,'proxies':len(helpers),'trees':len(trees),'no_temporary_receiver':not any(a.get_actor_label()=='TSP_TestOnly_SlopeReceiver8deg' for a in actors),'dirty_maps':[str(x) for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[str(x) for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.Shadow.Virtual.Enable','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Editor.Viewport.OverridePIEScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.ScreenPercentage','r.VSync','t.MaxFPS']}}
assert not d['dirty_maps'] and not d['dirty_content'] and d['no_temporary_receiver'];(O/'FinalEditorState.json').write_text(json.dumps(d,indent=2));unreal.log('TREE_SHADOW_FINAL_REOPEN_PASS')
