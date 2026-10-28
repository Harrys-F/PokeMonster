"""Map-specific derived basin; original floor, models and authoring files stay intact."""
import bpy,math,json,bmesh
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'Art/World/PokemonAIV3'
assert bpy.app.background and not (D/'SeparatedPond.blend').exists()
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.unit_settings.system='METRIC'
def height(x,y):
 r=math.hypot((x-720)/900,(y+1800)/650)
 t=max(0,min(1,(r-.64)/.39));return -420*(1-t*t*(3-2*t))
def make(name,verts,faces):
 # Match the existing checked FBX pipeline: reflect Y before Unreal conversion.
 me=bpy.data.meshes.new(name);me.from_pydata([(x/100,-y/100,z/100)for x,y,z in verts],[],faces);me.update()
 o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o)
 uv=me.uv_layers.new(name='UVMap')
 for p in me.polygons:
  p.use_smooth=True
  for li in p.loop_indices:
   x,y,z=verts[me.loops[li].vertex_index];uv.data[li].uv=((x-720)/1800+.5,(y+1800)/1300+.5)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 # Grid top winding is explicit in Blender's reflected coordinate basis.
 if name=='SM_AIV3PondWater':
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<0]);bm.to_mesh(me);bm.free()
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(D/'Exports'/(name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False)
 return {'vertices':len(verts),'triangles':sum(len(f)-2 for f in faces)}
verts=[];faces=[];nx=181;ny=131
for j in range(ny):
 for i in range(nx):
  x=-6000+i*50;y=-3250+j*50;verts.append((x,y,height(x,y)))
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;faces.extend([(a,a+nx,a+nx+1),(a,a+nx+1,a+1)])
# Closed deep underside supports collision/distance-field generation, no water-plane fake depth.
edge=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(range((ny-1)*nx+nx-2,(ny-1)*nx-1,-1))+[j*nx for j in range(ny-2,0,-1)]
base=len(verts);verts.extend([(verts[k][0],verts[k][1],-550)for k in edge])
for n,k in enumerate(edge):
 m=(n+1)%len(edge);faces.append((k,edge[m],base+m,base+n))
faces.append(tuple(range(base,base+len(edge))))
summary={'ground':make('SM_AIV3PondGround',verts,faces)}
verts=[(720,-1800,4.2)]+[(720+900*math.cos(i*2*math.pi/128),-1800+650*math.sin(i*2*math.pi/128),4.2)for i in range(128)]
faces=[(0,1+i,1+(i+1)%128)for i in range(128)];summary['water']=make('SM_AIV3PondWater',verts,faces)
bpy.ops.wm.save_as_mainfile(filepath=str(D/'SeparatedPond.blend'));(D/'Geometry.json').write_text(json.dumps(summary,indent=2));print(summary)
