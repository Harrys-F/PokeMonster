"""V4 reusable botanical accents and irregular shallow entrance stones; background only."""
from pathlib import Path
import bpy,bmesh,math,random,json
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/World/VisualV2HealingArtV4';assert bpy.app.background;dst=A/'Source/HealingHouse_GardenDetails_V4.blend';assert not dst.exists()
bpy.ops.wm.open_mainfile(filepath=str(A/'Source/HealingHouse_PottedPlants_V4.blend'));s=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0
for o in list(bpy.data.objects):
 if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
fol=bpy.data.materials['HA4_Foliage'];flower=bpy.data.materials['HA4_Blossom'];stone=bpy.data.materials.new('HA4_Stone');stone.diffuse_color=(.27,.24,.19,1);stone.use_nodes=True;stone.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.27,.24,.19,1);stone.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.91
out={}
def finish(o,name):
 o.name='HA4_'+name;o.location=(0,0,0);o.data.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles()
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_HA4_'+name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False,path_mode='COPY',embed_textures=False)
 out[name]={'object':o.name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'materials':[m.name for m in o.data.materials],'dimensions_m':[max(v.co[i] for v in o.data.vertices)-min(v.co[i] for v in o.data.vertices) for i in range(3)]};return o
# Vegetation derived from the new authored botanical geometry, no pots buried underground.
for src,name in [('BroadHerb','GardenHerb'),('FlowerPlant','GardenFlowers')]:
 o=bpy.data.objects['HA4_'+src].copy();o.data=o.data.copy();s.collection.objects.link(o);bm=bmesh.new();bm.from_mesh(o.data);drop=[f for f in bm.faces if f.material_index in [0,2]];bmesh.ops.delete(bm,geom=drop,context='FACES');bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(o.data);bm.free()
 for v in o.data.vertices:v.co=(v.co-Vector((0,0,.224)))*.62
 finish(o,name)
# Detailed curved grass blades, softer/slender silhouette than the old straight cards.
rng=random.Random(42019)
def mesh_obj(name,vs,fs,uvs,colors,materials):
 m=bpy.data.meshes.new(name);m.from_pydata(vs,[],fs);m.update();o=bpy.data.objects.new(name,m);s.collection.objects.link(o)
 for mat in materials:m.materials.append(mat)
 uv=m.uv_layers.new(name='UVMap');col=m.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
 for f in m.polygons:
  f.use_smooth=True
  for li in f.loop_indices:vi=m.loops[li].vertex_index;uv.data[li].uv=uvs[vi];col.data[li].color=colors[vi]
 return o
vs=[];fs=[];uv=[];cs=[]
for i in range(48):
 a=rng.random()*math.tau;r=rng.random()**.5*.17;base=Vector((math.cos(a)*r,math.sin(a)*r,0));h=rng.uniform(.12,.34);dr=Vector((math.cos(a),math.sin(a),0));side=Vector((-math.sin(a),math.cos(a),0));width=rng.uniform(.007,.015);rows=[];color=tuple(v*rng.uniform(.8,1.1) for v in (.062,.125,.025))+(1,)
 for j in range(6):
  t=j/6;center=base+dr*h*.64*t*t+Vector((0,0,h*(t-.22*t*t)));span=width*(1-t)**.7;row=[]
  for k in [-1,0,1]:row.append(len(vs));vs.append(tuple(center+side*span*k+Vector((0,0,.003*(1-abs(k))))));uv.append(((k+1)/2,t));cs.append(color)
  rows.append(row)
 for r1,r2 in zip(rows,rows[1:]):
  for k in range(2):fs.append((r1[k],r2[k],r2[k+1],r1[k+1]))
 tip=len(vs);vs.append(tuple(base+dr*h*.64+Vector((0,0,h*.78))));uv.append((.5,1));cs.append(color)
 for k in range(2):fs.append((rows[-1][k],tip,rows[-1][k+1]))
finish(mesh_obj('GrassTuft',vs,fs,uv,cs,[fol]),'GrassTuft')
# Compact ivy sprays in the facade Y/Z plane. Old actor transforms remain untouched.
for variant in ['A','B']:
 rng=random.Random(427 if variant=='A' else 198);vs=[];fs=[];uv=[];cs=[]
 for l in range(9):
  cy=rng.uniform(-.43,.43);cz=rng.uniform(-.43,.43);ang=rng.uniform(-.7,.7);length=rng.uniform(.23,.36);wid=length*.58;start=len(vs);shade=rng.uniform(.75,1.15);color=(.035*shade,.10*shade,.018*shade,1)
  # Five-lobed radial contour with a shallow raised centre; no alpha cards.
  vs.append((-.04,cy,cz));uv.append((.5,.5));cs.append(color)
  for j in range(20):
   a=j*math.tau/20;rr=1+.23*math.cos(a*5);y=math.cos(a)*wid*rr;z=math.sin(a)*length*rr;y,z=y*math.cos(ang)-z*math.sin(ang),y*math.sin(ang)+z*math.cos(ang);vs.append((-.01-.035*math.sin(a)**2,cy+y,cz+z));uv.append((.5+.45*math.cos(a),.5+.45*math.sin(a)));cs.append(color)
  for j in range(20):fs.append((start,start+1+j,start+1+(j+1)%20))
 finish(mesh_obj('IvySprig'+variant,vs,fs,uv,cs,[fol]),'IvySprig'+variant)
# Unequal shaped worn stone, 30cm across, bevels and planar UVs, no collision.
rng=random.Random(618);N=9;vs=[];fs=[]
outline=[(math.cos(i*math.tau/N)*rng.uniform(.13,.17),math.sin(i*math.tau/N)*rng.uniform(.11,.15)) for i in range(N)]
for z,scale in [(0,.9),(.014,1),(.035,.91)]:
 for x,y in outline:vs.append((x*scale,y*scale,z+rng.uniform(-.001,.001)))
for r in range(2):
 for j in range(N):fs.append((r*N+j,r*N+(j+1)%N,(r+1)*N+(j+1)%N,(r+1)*N+j))
fs.append(tuple(range(N-1,-1,-1)));fs.append(tuple(range(2*N,3*N)))
o=mesh_obj('Flagstone',vs,fs,[(x*3,y*3) for x,y,z in vs],[(1,1,1,1)]*len(vs),[stone])
# For every bevel side choose its best planar projection to avoid zero-area UVs.
for f in o.data.polygons:
 axis=max(range(3),key=lambda i:abs(f.normal[i]));ab=[(1,2),(0,2),(0,1)][axis]
 for li in f.loop_indices:v=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(v[ab[0]]*3,v[ab[1]]*3)
finish(o,'Flagstone')
for o in list(bpy.data.objects):
 if o.name not in [v['object'] for v in out.values()]:bpy.data.objects.remove(o,do_unlink=True)
for i,o in enumerate(bpy.data.objects):o.location.x=i*.9
for im in bpy.data.images:
 if im.source=='FILE':im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(dst));(A/'Details.json').write_text(json.dumps(out,indent=2));bpy.ops.wm.open_mainfile(filepath=str(dst));assert len([o for o in bpy.data.objects if o.type=='MESH'])==6
print('DETAILS_REOPEN_OK',json.dumps(out))
