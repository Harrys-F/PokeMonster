"""Read-only provenance, bounds and ground contact diagnostic for the questioned crate."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV2'
a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.get_actor_label()=='V2_House_HH_V3_SupplyCrate');c=a.static_mesh_component;origin,extent=a.get_actor_bounds(False)
d={'actor':a.get_actor_label(),'mesh':c.static_mesh.get_path_name(),'position_cm':a.get_actor_location().to_tuple(),'extent_cm':extent.to_tuple(),'bottom_z_cm':origin.z-extent.z,'collision':str(c.get_collision_enabled()),'source':'Tools/DressHealingHouseV3.py:175 decorative SupplyCrate','line_trace_api':unreal.SystemLibrary.line_trace_single.__doc__}
h=unreal.SystemLibrary.line_trace_single(w,unreal.Vector(origin.x,origin.y,100),unreal.Vector(origin.x,origin.y,-200),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[a],unreal.DrawDebugTrace.NONE,True)
d['trace_result']=str(h)
if h:
 d['hit_api']=[n for n in dir(h) if not n.startswith('_')]
 if hasattr(h,'to_tuple'):
  t=h.to_tuple();d['ground_hit']={'blocking':t[0],'impact_cm':t[5].to_tuple(),'actor':t[9].get_actor_label() if t[9] else None,'gap_cm':d['bottom_z_cm']-t[5].z}
(O/'CubeGroundAudit.json').write_text(json.dumps(d,indent=2))
