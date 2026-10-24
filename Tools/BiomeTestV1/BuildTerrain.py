"""Create only this sandbox's authoring source/FBX; no original asset is edited."""
import bpy,sys,json,math,bmesh
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
D=R/'Art/World/BiomeTestV1';dst=D/'BiomeTest_Terrain_V1.blend';assert bpy.app.background and (not dst.exists() or '--replace-owned-biome-v1' in sys.argv)
(D/'Exports').mkdir(exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
N=209;spacing=50;verts=[];colors=[];faces=[]
for j in range(N):
 v=-L.EXTENT+j*spacing
 for i in range(N):
  u=-L.EXTENT+i*spacing;x,y,z=L.world(u,v,L.height(u,v));verts.append((x/100,-y/100,z/100));colors.append(L.vertex_colour(u,v)) # FBX UE conversion reflects Blender Y; precompensate.
for j in range(N-1):
 for i in range(N-1):
  a=j*N+i;b=a+1;c=a+N;d=c+1;faces.extend([(a,c,d),(a,d,b)])
# World basis reverses orientation: explicit normals are recalculated for an upward surface.
def make(name,vs,fs,cs):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o)
 uv=me.uv_layers.new(name='UVMap');co=me.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
 for p in me.polygons:
  p.use_smooth=True
  for li in p.loop_indices:
   vi=me.loops[li].vertex_index;v=me.vertices[vi].co;uv.data[li].uv=(v.x/2,v.y/2);co.data[li].color=cs[vi]
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 # Clipped water triangles are disconnected; orient EACH face explicitly upward.
 bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<0])
 bm.to_mesh(me);bm.free();me.calc_loop_triangles()
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(D/'Exports'/(name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False)
 return {'vertices':len(me.vertices),'triangles':len(me.loop_triangles),'bounds_m':[(min(v[k]for v in vs),max(v[k]for v in vs))for k in range(3)]}
summary={'terrain':make('SM_BiomeTerrain',verts,faces,colors)}
# Clip each lowered triangle to the exact water elevation, using the same terrain triangulation.
wv=[];wf=[];wc=[]
for f in faces:
 pts=[verts[i]for i in f]
 if min(p[2]for p in pts)>=-.20:continue
 poly=[]
 for a,b in zip(pts,pts[1:]+pts[:1]):
  ai=a[2]<-.2;bi=b[2]<-.2
  if ai:poly.append((a[0],a[1],-.2))
  if ai!=bi:
   t=(-.2-a[2])/(b[2]-a[2]);poly.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]),-.2))
 start=len(wv);wv.extend(poly);wc.extend([(1,1,1,1)]*len(poly))
 for i in range(1,len(poly)-1):wf.append((start,start+i,start+i+1))
summary['water']=make('SM_BiomeWater',wv,wf,wc)
bpy.ops.wm.save_as_mainfile(filepath=str(dst));(D/'Terrain.json').write_text(json.dumps(summary,indent=2));print('BIOME_TERRAIN_SOURCE_CREATED',summary)
