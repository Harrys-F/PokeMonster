import bpy,bmesh,math,json,random
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
scene=bpy.data.scenes['Hobbit_NPC_Base_V2'];bpy.context.window.scene=scene
C={c.name.removeprefix('HNV2_'):c for c in scene.collection.children}
def active(o):
 for q in scene.objects:q.select_set(False)
 o.select_set(True);bpy.context.view_layer.objects.active=o

def apply(o,m):active(o);bpy.ops.object.modifier_apply(modifier=m.name)
def mesh(name,verts,faces,col,materials):
 me=bpy.data.meshes.new('HNV2_'+name+'_Mesh');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('HNV2_'+name,me);C[col].objects.link(o)
 for m in materials:me.materials.append(m)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for p in me.polygons:p.use_smooth=True
 return o

def tube(name,points,radius,col,material,sides=10,flatten=1.):
 vv=[];ff=[];points=[Vector(p) for p in points]
 for i,p in enumerate(points):
  d=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();u=d.cross(Vector((0,0,1)))
  if u.length<.05:u=d.cross(Vector((0,1,0)))
  u.normalize();v=d.cross(u);t=i/max(len(points)-1,1);r=radius(t) if callable(radius) else radius
  for j in range(sides):vv.append(tuple(p+r*(u*math.cos(j*math.tau/sides)+v*math.sin(j*math.tau/sides)*flatten)))
 for i in range(len(points)-1):
  for j in range(sides):ff.append([i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j])
 ff.extend([list(reversed(range(sides))),list(range((len(points)-1)*sides,len(points)*sides))]);return mesh(name,vv,ff,col,[material])

def sphere(name,loc,scale,col,material,segments=24,rings=16):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc);o=bpy.context.object;o.name='HNV2_'+name
 for c in list(o.users_collection):c.objects.unlink(o)
 C[col].objects.link(o);o.scale=scale;active(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o

def material(name,color,rough=.7):
 existing=bpy.data.materials.get('HNV2_'+name)
 if existing:return existing
 m=bpy.data.materials.new('HNV2_'+name);m.use_nodes=True;m.diffuse_color=(*color,1)
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
 return m

def join(objects,name):
 for o in scene.objects:o.select_set(False)
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();o=objects[0];o.name='HNV2_'+name;return o

def archive(objects):
 if 'ARCHIVE_V1' not in C:
  c=bpy.data.collections.new('HNV2_ARCHIVE_V1');scene.collection.children.link(c);C['ARCHIVE_V1']=c;c.hide_render=True;c.hide_viewport=True
 for o in objects:
  for c in list(o.users_collection):c.objects.unlink(o)
  C['ARCHIVE_V1'].objects.link(o);o.name='HNV2_V1Archive_'+o.name.removeprefix('HNV2_')

def body_union(o):
 b=bpy.data.objects['HNV2_Body'];m=b.modifiers.new('LocalAnatomicalUnion','BOOLEAN');m.operation='UNION';m.solver='EXACT';m.object=o;apply(b,m);bpy.data.objects.remove(o,do_unlink=True)

def save_stage(n):
 bpy.context.view_layer.update();p=BASE/'Source/Stages'/('Hobbit_NPC_Base_V2_'+n+'.blend');assert not p.exists();bpy.data.libraries.write(str(p),{scene});print('Saved new stage',p.name)
