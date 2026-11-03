"""Read-only actual terrain collision, authored grid, original paths and functional anchors."""
import unreal,json,runpy,math,re,statistics
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world();design=runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Design.py'));data=json.loads((D/'GroundHeightGrid.json').read_text());old={(x,y):z for x,y,z in data['old']};new={(x,y):z for x,y,z in data['new']};actors=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor);ground=next(a for a in actors if a.get_actor_label()=='V2_Ground');ignore=[a for a in actors if a!=ground];roads=[abs(z-old[(x,y)])for(x,y),z in new.items()if design['pd'](x,y)<150];assert max(roads)<.01
rays=[]
for x,y in [(-5400,1950),(-5000,-2550),(-2200,2450),(1950,1750),(2250,-800),(2300,-2700),(-900,1100),(-350,-550),(-3100,500),(-2750,-1000),(700,-1800),(700,-1200),(1300,-1800)]:
 hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,1000),unreal.Vector(x,y,-1000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,True,ignore,unreal.DrawDebugTrace.NONE);assert hit,(x,y);m=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text());assert m,(x,y,hit.export_text());z=float(m[1]);assert abs(z-new[(x,y)])<.1,(x,y,z,new[(x,y)]);rays.append(dict(x=x,y=y,collision_z=z))
slopes=[]
for(x,y),z in new.items():
 if design['pondr'](x,y)<1.15:continue
 for dx,dy in [(50,0),(0,50)]:
  if(x+dx,y+dy)in new:slopes.append(math.degrees(math.atan(abs(z-new[(x+dx,y+dy)])/50)))
assert max(slopes)<45,max(slopes)
a=next(a for a in actors if a.get_actor_label()=='WR4_DistantLand');assert a.static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
out=dict(grid_vertices=len(new),route_grid_samples=len(roads),max_route_height_change_cm=max(roads),terrain_max_axis_slope_degrees=max(slopes),terrain_p95_axis_slope_degrees=sorted(slopes)[int(len(slopes)*.95)],terrain_collision_rays=rays,pond_core_collision_cm=next(r['collision_z']for r in rays if r['x']==700 and r['y']==-1800),visual_backdrop_only=True,navigation_note='Existing wild movement uses habitat floor projection and collision sweeps, not a new NavMesh architecture. Runtime population/traversal is separately tested.')
(D/'GeometryAudit.json').write_text(json.dumps(out,indent=2));print(out)
