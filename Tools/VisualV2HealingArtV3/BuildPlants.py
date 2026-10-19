"""Independent botanical variants; append and preserve the existing hand-thrown pots.
Run only in background Blender. No existing Blender source is saved.
"""
from pathlib import Path
import bpy,bmesh,math,random,json,sys
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/World/VisualV2HealingArtV3';dst=A/'Source/HealingHouse_PottedPlants_V3.blend'
assert bpy.app.background and (not dst.exists() or '--revise-owned' in sys.argv);bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
mats=[]
for name,col in [('Pot',(.24,.105,.048,1)),('Foliage',(.085,.16,.045,1)),('Soil',(.055,.034,.018,1)),('Blossom',(.68,.54,.22,1))]:
 m=bpy.data.materials.new('HA3_'+name);m.use_nodes=True;bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=col;bs.inputs['Roughness'].default_value=.86
 if name=='Foliage' or name=='Blossom':
  v=m.node_tree.nodes.new('ShaderNodeVertexColor');v.layer_name='Col';m.node_tree.links.new(v.outputs['Color'],bs.inputs['Base Color'])
 if name=='Pot':
  t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'Art/HealingHouse/Textures/QualityV3/T_HH_PaintedTerracotta.png'),check_existing=True)
  mix=m.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.52,.48,.43,1);m.node_tree.links.new(t.outputs['Color'],mix.inputs[1]);m.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
 mats.append(m)
catalog={}
for ix,family in enumerate(['BroadHerb','NarrowHerb','LeafPlant','FlowerPlant','TrailingHerb']):
 rng=random.Random(331+ix);vs=[];fs=[];mi=[];uvs=[];cols=[]
 def vert(p,uv=(0,0),color=(1,1,1,1)):
  vs.append(tuple(p));uvs.append(uv);cols.append(color);return len(vs)-1
 def face(v,mat):fs.append(tuple(v));mi.append(mat)
 # Reuse only the original pottery faces, never the original foliage.
 with bpy.data.libraries.load(str(R/'Art/HealingHouse/Source/HealingHouse_QualityV3.blend'),link=False) as (fr,to):to.objects=['HH_Q3_'+family]
 src=to.objects[0];lookup={}
 for f in src.data.polygons:
  if 'Ceramic' not in src.data.materials[f.material_index].name:continue
  ids=[]
  for vi in f.vertices:
   if vi not in lookup:
    c=src.data.vertices[vi].co;lookup[vi]=vert(c,(math.atan2(c.y,c.x)/math.tau,c.z*2))
   ids.append(lookup[vi])
  face(ids,0)
 bpy.data.objects.remove(src,do_unlink=True)
 def stem(points,r=.003):
  rings=[]
  for i,p in enumerate(points):
   t=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();u=t.cross(Vector((0,1,0))).normalized();v=t.cross(u).normalized();rr=r*(1-.68*i/(len(points)-1));rings.append([vert(p+rr*(u*math.cos(j*math.tau/6)+v*math.sin(j*math.tau/6)),color=(.042,.08,.019,1)) for j in range(6)])
  for a,b in zip(rings,rings[1:]):
   for j in range(6):face((a[j],a[(j+1)%6],b[(j+1)%6],b[j]),1)
  face(tuple(reversed(rings[0])),1);face(rings[-1],1)
 def leaf(a,b,width,col,mat=1,lobes=False):
  d=b-a;side=d.cross(Vector((0,0,1)))
  if side.length<.01:side=Vector((1,0,0))
  side.normalize();n=side.cross(d).normalized();start=vert(a,(.5,0),col);rows=[]
  for i in range(1,8):
   t=i/8;center=a+d*t+n*math.sin(t*math.pi)*.026;span=width*math.sin(math.pi*t)**.82
   if lobes:span*=1+.11*math.sin(t*math.tau*4)
   row=[]
   for j in range(5):
    u=(j-2)/2;p=center+side*(u*span)+n*(.008*(1-u*u)*math.sin(t*math.pi)-.012*u*u*math.sin(t*math.pi));c=tuple(v*(1+.12*math.sin(t*math.pi)-.08*abs(u)) for v in col[:3])+(1,);row.append(vert(p,(j/4,t),c))
   rows.append(row)
  end=vert(b,(.5,1),col)
  for j in range(4):face((start,rows[0][j],rows[0][j+1]),mat)
  for r1,r2 in zip(rows,rows[1:]):
   for j in range(4):face((r1[j],r2[j],r2[j+1],r1[j+1]),mat)
  for j in range(4):face((rows[-1][j],end,rows[-1][j+1]),mat)
 # A visible soil disk, below pot rim, provides a plausible stem attachment.
 center=vert((0,0,.226));ring=[vert((.142*math.cos(i*math.tau/32),.142*math.sin(i*math.tau/32),.226+rng.uniform(-.002,.002))) for i in range(32)]
 for i in range(32):face((center,ring[i],ring[(i+1)%32]),2)
 count={'BroadHerb':15,'NarrowHerb':18,'LeafPlant':14,'FlowerPlant':17,'TrailingHerb':11}[family]
 for k in range(count):
  ang=k*2.399+rng.uniform(-.24,.24);h=rng.uniform(.31,.56);rad=rng.uniform(.10,.24)
  if family=='NarrowHerb':h*=1.10
  trailing=family=='TrailingHerb' or (family=='BroadHerb' and k in [1,7,10])
  base=Vector((.10*math.cos(ang),.10*math.sin(ang),.224));direction=Vector((math.cos(ang),math.sin(ang),0));points=[]
  for j in range(6):
   t=j/5;z=.224+h*(math.sin(t*math.pi*.68) if not trailing else .5*math.sin(t*math.pi)-t*.38);p=base+direction*(rad*t+(.18*t*t if trailing else 0));p.z=z;points.append(p)
  stem(points)
  for j in range(1,5):
   origin=points[j]
   for side in [-1,1]:
    a=ang+side*rng.uniform(.65,1.2);length=rng.uniform(.09,.17)*(1-.055*j);length*=.8 if family=='NarrowHerb' else 1
    tip=origin+Vector((math.cos(a)*length,math.sin(a)*length,rng.uniform(-.03,.055)))
    width=length*({'BroadHerb':.34,'NarrowHerb':.14,'LeafPlant':.40,'FlowerPlant':.25,'TrailingHerb':.29}[family]);light=rng.uniform(.80,1.20);color=tuple(v*light for v in [( .075,.145,.035),(.10,.17,.054),(.10,.16,.078)][k%3])+(1,)
    leaf(origin,tip,width,color,lobes=family=='LeafPlant')
  if family=='FlowerPlant' and k%2==0:
   tip=points[-1]
   for l in range(7):
    a=l*math.tau/7;leaf(tip,tip+Vector((math.cos(a)*.037,math.sin(a)*.037,.012)),.012,(.70,.62,.40,1),3)
   # small warm disk, not a floating sphere
   c=vert(tip+Vector((0,0,.012)),color=(.49,.28,.045,1));rr=[vert(tip+Vector((.012*math.cos(l*math.tau/8),.012*math.sin(l*math.tau/8),.009)),color=(.49,.28,.045,1)) for l in range(8)]
   for l in range(8):face((c,rr[l],rr[(l+1)%8]),3)
 me=bpy.data.meshes.new('HA3_'+family);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('HA3_'+family,me);s.collection.objects.link(o)
 for m in mats:me.materials.append(m)
 uv=me.uv_layers.new(name='UVMap');co=me.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
 for f,mat in zip(me.polygons,mi):
  f.material_index=mat;f.use_smooth=True
  flat_uv=all(uvs[me.loops[li].vertex_index]==(0,0) for li in f.loop_indices)
  axis=max(range(3),key=lambda i:abs(f.normal[i]));ab=[(1,2),(0,2),(0,1)][axis]
  for li in f.loop_indices:
   vi=me.loops[li].vertex_index;p=me.vertices[vi].co;uv.data[li].uv=(p.x*2.6+.5,p.y*2.6+.5) if mat==0 and abs(f.normal.z)>.7 else ((p[ab[0]]*4,p[ab[1]]*4) if flat_uv else uvs[vi]);co.data[li].color=cols[vi]
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.calc_loop_triangles()
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_HA3_'+family+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',add_leaf_bones=False,bake_anim=False,path_mode='COPY',embed_textures=False)
 catalog[family]={'object':o.name,'vertices':len(me.vertices),'triangles':len(me.loop_triangles),'dimensions_m':[max(v.co[i] for v in me.vertices)-min(v.co[i] for v in me.vertices) for i in range(3)],'materials':[m.name for m in me.materials]}
 o.location.x=(ix-2)*1.1;o.hide_render=False;o.hide_set(False)
# A useful source-file inspection layout; export origins above remain at soil level.
world=bpy.data.worlds.new('Neutral inspection world');s.world=world;world.use_nodes=True;next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs[0].default_value=(.11,.13,.15,1)
for name,position,power,size in [('Key',(1,-3,5),600,5),('Fill',(-4,-1,3),330,4),('Rim',(2,3,4),700,3)]:
 light=bpy.data.lights.new(name,'AREA');light.energy=power;light.shape='DISK';light.size=size;o=bpy.data.objects.new(name,light);s.collection.objects.link(o);o.location=position;o.rotation_euler=(Vector((0,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
camera=bpy.data.cameras.new('Botanical overview');o=bpy.data.objects.new('Botanical overview',camera);s.collection.objects.link(o);o.location=(1,-6,4);o.rotation_euler=(Vector((0,0,.35))-o.location).to_track_quat('-Z','Y').to_euler();camera.type='ORTHO';camera.ortho_scale=6.0;s.camera=o
s.render.resolution_x=1800;s.render.resolution_y=800;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.filepath=str(R/'Saved/VisualV2HealingArtV3/BlenderPlants.png')
for image in bpy.data.images:
 if image.source=='FILE':image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(dst));(A/'Plants.json').write_text(json.dumps(catalog,indent=2));bpy.ops.wm.open_mainfile(filepath=str(dst));assert len([o for o in bpy.data.objects if o.type=='MESH'])==5
bpy.ops.render.render(write_still=True)
print('PLANTS_REOPEN_OK',json.dumps(catalog),flush=True)
