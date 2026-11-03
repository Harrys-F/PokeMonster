"""Read-only geometry normal orientation at real surface triangles."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';out={}
for p in ['/Game/Environment/VisualV2WorldOverhaulV3/Meshes/SM_WOV_Ground','/Game/Environment/VisualV2WorldRefinementV4/Meshes/SM_WR4_Ground','/Game/Environment/VisualV2WorldRefinementV4/Meshes/SM_WR4_DistantLand']:
 m=unreal.load_asset(p);dm,_=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(m,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());rows=[]
 for i in [0,1,2,100,500,1000]:
  ps=unreal.GeometryScript_MeshQueries.get_triangle_positions(dm,i);ns=unreal.GeometryScript_MeshQueries.get_triangle_normals(dm,i);rows.append(dict(triangle=i,positions=[v.to_tuple()for v in ps if isinstance(v,unreal.Vector)],normals=[v.to_tuple()for v in ns if isinstance(v,unreal.Vector)]))
 out[p]=rows
(D/'SurfaceNormalsVerified.json').write_text(json.dumps(out,indent=2))
