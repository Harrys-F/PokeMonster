"""Heat weights on an exact-position welded proxy; original render topology/UV/normals untouched."""
import bpy,bmesh,json
from pathlib import Path
from mathutils.kdtree import KDTree
from mathutils import Matrix
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Zunderlauf';bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Glumanda_Meshy_V1.blend'));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Glumanda_Meshy'];rig=bpy.data.objects['Glumanda_Meshy_Rig'];proxy=body.copy();proxy.data=body.data.copy();bpy.context.collection.objects.link(proxy);proxy.parent=None;proxy.matrix_world=Matrix.Identity(4);proxy.vertex_groups.clear();proxy.modifiers.clear()
bm=bmesh.new();bm.from_mesh(proxy.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bm.to_mesh(proxy.data);bm.free()
rig.data.bones['root'].use_deform=False;rig.data.bones['tail_socket'].use_deform=False
bpy.ops.object.select_all(action='DESELECT');proxy.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.parent_set(type='ARMATURE_AUTO')
assert all(v.groups for v in proxy.data.vertices),'Heat weights incomplete; do not overwrite source'
k=KDTree(len(proxy.data.vertices))
for v in proxy.data.vertices:k.insert(v.co,v.index)
k.balance();body.vertex_groups.clear()
for b in rig.data.bones:body.vertex_groups.new(name=b.name)
for v in body.data.vertices:
 co,i,dist=k.find(v.co);assert dist<1e-5;w={proxy.vertex_groups[g.group].name:g.weight for g in proxy.data.vertices[i].groups if g.weight>1e-5}
 if v.co.z>.39:w={'head':1.}
 def smooth(a,b,x):
  u=max(0.,min(1.,(x-a)/(b-a)));return u*u*(3-2*u)
 foot=max(1-smooth(.025,.055,v.co.z),smooth(.075,.12,-v.co.y)*(1-smooth(.08,.11,v.co.z)))*smooth(.05,.08,abs(v.co.x))
 if foot>0:
  w={k:value*(1-foot) for k,value in w.items()};key='foot_L' if v.co.x>0 else 'foot_R';w[key]=w.get(key,0)+foot
 if v.co.z<.035:w={'tail_01' if v.co.y>.075 else ('foot_L' if v.co.x>0 else 'foot_R') if abs(v.co.x)>.04 else 'pelvis':1.}
 # Original flame/body split is one rigid tail segment across its seam.
 if v.co.x>.13 and v.co.y>.12 and v.co.z>.25:w={'tail_tip':1.}
 total=sum(w.values());assert total>0
 for name,value in w.items():body.vertex_groups[name].add([v.index],value/total,'REPLACE')
bpy.data.objects.remove(proxy,do_unlink=True);bpy.ops.wm.save_as_mainfile(filepath=str(A/'Source/Glumanda_Meshy_V1.blend'));print('REFINED_WEIGHTS_RENDER_MESH_UNCHANGED')
