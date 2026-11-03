"""Conforming 50-cm inner edge, progressively coarse outer rings: no gap, no second ground layer."""
import unreal,runpy,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Common.py')));grid={(x,y):z for x,y,z in json.loads((D/'GroundHeightGrid.json').read_text())['new']}
def sample(x,y):
 x=min(3000,max(-6000,x));y=min(3250,max(-3250,y));xx=math.floor(x/50)*50;yy=math.floor(y/50)*50;t=(x-xx)/50;u=(y-yy)/50
 def g(a,b):return grid[(min(3000,a),min(3250,b))]
 return (1-u)*((1-t)*g(xx,yy)+t*g(xx+50,yy))+u*((1-t)*g(xx,yy+50)+t*g(xx+50,yy+50))
verts=[];tri=[];distances=[0,50,100,200,400,800,1600,2400,3200,4000]
for side in range(4):
 n=130 if side<2 else 180;base=len(verts)
 for d in distances:
  for i in range(n+1):
   t=i/n
   if side<2:x=(-6000-d if side==0 else 3000+d);y=-3250+t*6500+(2*t-1)*d
   else:x=-6000+t*9000+(2*t-1)*d;y=(-3250-d if side==2 else 3250+d)
   bx=min(3000,max(-6000,x));by=min(3250,max(-3250,y));f=smooth(math.hypot(x-bx,y-by)/1500);ridge=370+140*math.sin(x*.00061+y*.00073)+100*math.sin(x*.0011-y*.00041);z=sample(bx,by)*(1-f)+ridge*f;verts.append(unreal.Vector(x,y,z))
 for row in range(len(distances)-1):
  for i in range(n):
   a=base+row*(n+1)+i;b=a+1;c=a+n+1;e=c+1
   # Unreal static meshes use clockwise front faces; inverse XY cross gives the upward-facing surface.
   for u,v,w in [(a,b,c),(b,e,c)]:
    p,q,r=verts[u],verts[v],verts[w]
    if(q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x)>0:v,w=w,v
    tri.append(unreal.IntVector(u,v,w))
b=unreal.GeometryScriptSimpleMeshBuffers();b.vertices=verts;b.triangles=tri;b.uv0=[unreal.Vector2D(v.x/165,v.y/165)for v in verts];dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,b);m=unreal.load_asset(ROOT+'/Meshes/SM_WR4_DistantLand');opts=unreal.GeometryScriptCopyMeshToAssetOptions();opts.enable_recompute_normals=True;unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,m,opts,unreal.GeometryScriptMeshWriteLOD());assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);save('BackdropStitch.json',dict(vertices=len(verts),triangles=len(tri),inner_edge_spacing_cm=50,progressive_outer_rings_cm=distances,reason='Coarse original background edge exposed a thin join in Westwald view',no_overlapping_playable_ground=True))
