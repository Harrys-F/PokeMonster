"""Preserved original Nebulak, separated gas surface and one inexpensive 3D envelope mesh."""
import bpy,math,json,hashlib
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Nebulak';P=A/'Source/Nebulak_MotionV5.blend';assert not P.exists();original=A/'Source/Nebulak_PolishV4.blend';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(original);bpy.ops.wm.open_mainfile(filepath=str(original));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Nebulak_Body'];rig=bpy.data.objects['Nebulak_Rig'];oldco=[tuple(v.co)for v in body.data.vertices];olduv=[tuple(v.uv)for v in body.data.uv_layers.active.data];oldweights=[[(g.group,g.weight)for g in v.groups]for v in body.data.vertices]
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def face_clear(p):
 x,y,z=p;return (1-smooth(-.15,-.025,y))*(1-smooth(.16,.34,abs(x)))*smooth(.37,.54,z)*(1-smooth(.93,1.10,z))
attr=body.data.color_attributes.new(name='MotionV5',type='FLOAT_COLOR',domain='CORNER');body.data.color_attributes.active_color=attr;old=body.data.color_attributes['PolishV4'];gasmat=body.data.materials[0].copy();gasmat.name='Nebulak_GasSurface_MotionV5';body.data.materials.append(gasmat);gas_faces=0
for poly in body.data.polygons:
 values=[]
 for i in poly.loop_indices:
  vertex=body.data.vertices[body.data.loops[i].vertex_index];mask=old.data[i].color[0];values.append(mask);attr.data[i].color=(mask,face_clear(vertex.co),.2,1)
 if sum(values)/len(values)>.22:poly.material_index=1;gas_faces+=1
verts=[];faces=[];colors=[];N=18;head=rig.data.bones['head'].matrix_local.inverted();rings=8;segments=12
for i in range(N):
 # Nonuniform Fibonacci distribution around the body, deliberately open in front of the face.
 z=1-2*(i+.5)/N;angle=i*math.pi*(3-math.sqrt(5));r=math.sqrt(max(0,1-z*z));center=Vector((.40*r*math.cos(angle),.23*r*math.sin(angle),.65+.40*z));radius=Vector((.19+.025*math.sin(i*2.1),.14+.015*math.cos(i*1.3),.19+.025*math.sin(i*.7)))
 if face_clear(center)>.7:continue
 raw=[Vector((0,0,1))]
 for ring in range(1,rings):
  theta=math.pi*ring/rings
  for segment in range(segments):
   phi=math.tau*segment/segments;raw.append(Vector((math.sin(theta)*math.cos(phi),math.sin(theta)*math.sin(phi),math.cos(theta))))
 raw.append(Vector((0,0,-1)));base=len(verts)
 for v in raw:
  p=center+Vector((v.x*radius.x,v.y*radius.y,v.z*radius.z));verts.append(head@p);colors.append((1,face_clear(p),(i*.61803398875)%1,1))
 for segment in range(segments):faces.append((base,base+1+segment,base+1+(segment+1)%segments))
 for ring in range(rings-2):
  first=base+1+ring*segments;second=first+segments
  for segment in range(segments):
   a=first+segment;b=first+(segment+1)%segments;c=second+segment;d=second+(segment+1)%segments;faces.extend([(a,c,b),(b,c,d)])
 last=base+1+(rings-2)*segments
 for segment in range(segments):faces.append((base+len(raw)-1,last+(segment+1)%segments,last+segment))
mesh=bpy.data.meshes.new('Nebulak_GasEnvelope_MotionV5');mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new('Nebulak_GasEnvelope_MotionV5',mesh);bpy.context.scene.collection.objects.link(obj);color=mesh.color_attributes.new(name='MotionV5',type='FLOAT_COLOR',domain='CORNER');mesh.color_attributes.active_color=color
for i,loop in enumerate(mesh.loops):color.data[i].color=colors[loop.vertex_index]
for poly in mesh.polygons:poly.use_smooth=True
mesh.uv_layers.new(name='UVMap')
assert oldco==[tuple(v.co)for v in body.data.vertices]and olduv==[tuple(v.uv)for v in body.data.uv_layers.active.data]and oldweights==[[(g.group,g.weight)for g in v.groups]for v in body.data.vertices];assert gas_faces>0
obj.hide_render=True;obj.hide_set(True);rig.animation_data.action=bpy.data.actions['Nebulak_Idle'];bpy.context.scene.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P));assert sha(original)==before
(A/'MotionV5_Audit.json').write_text(json.dumps(dict(source=str(P.relative_to(R)),source_sha256=sha(P),original_sha256=before,original_mesh_geometry_weights_uvs_preserved=True,gas_surface_faces=gas_faces,envelope_triangles=len(faces),envelope_vertices=len(verts),anchor='head',envelope_coordinates='Blender head bone-local coordinates; same FBX axis conversion as body',face_aperture='Fixed front-space mask, original opaque face retained'),indent=2));print('NEBULAK_SOURCE_SAVED',gas_faces,len(faces),flush=True)
