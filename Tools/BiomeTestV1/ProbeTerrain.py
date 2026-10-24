"""Read actual Unreal collision elevations, not just authoring height formulas."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world()or E.get_editor_world();rows=[]
for u,v in [(0,0),(-2800,-1800),(-1800,-2800),(-1200,-1800),(-1800,-1200),(3200,2850),(2850,3200),(2050,2700)]:
 x,y,z=L.world(u,v);hit=unreal.SystemLibrary.line_trace_single(w,unreal.Vector(x,y,850),unreal.Vector(x,y,-1200),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,list(unreal.GameplayStatics.get_all_actors_with_tag(w,'BiomePlayerWaterBarrier')),unreal.DrawDebugTrace.NONE,True)
 b=hit.to_tuple()
 rows.append({'uv':[u,v],'expected_z':L.height(u,v),'blocking':b[0],'location':b[4].to_tuple(),'impact':b[5].to_tuple(),'actor':b[9].get_name()if b[9]else None})
(R/'Saved/BiomeTestV1/TerrainProbes.json').write_text(json.dumps(rows,indent=2))
