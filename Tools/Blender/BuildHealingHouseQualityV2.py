"""Versioned quality edits of existing Art V1 forms plus reusable ground props.
Run in background Blender. Existing sources remain untouched; export separately
only after the saved file has been reopened and visually reviewed.
"""
import bpy,bmesh,math,random,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/HealingHouse';OUT=ART/'QualityV2';SOURCE=ART/'Source/HealingHouse_QualityV2.blend';assert bpy.app.background and not SOURCE.exists()
OUT.mkdir(parents=True,exist_ok=True);rng=random.Random(10526)
bpy.ops.wm.open_mainfile(filepath=str(ART/'Source/HealingHouse_ExpandedArt_V1.blend'))
s=bpy.data.scenes['HealingHouse_ExpandedArt_V1'];bpy.context.window.scene=s;s.name='HealingHouse_QualityV2'
keep=['FloorTile2m','CounterStepped','Fireplace','Bench','StoneWainscot2m','Pillow']
lib=bpy.data.collections.new('Quality V2 Export');s.collection.children.link(lib);catalog={}
# Painterly maps are reused by independent Blender and Unreal materials.
texroot=ART/'Textures/QualityV2'
for m in list(bpy.data.materials):
 key=m.name.removeprefix('HH_Art_');name={'Timber':'Wood','Sage':'Cloth','Linen':'Cloth'}.get(key,key)
 if name in ('Wood','Stone','Plaster','Cloth'):
  nodes=m.node_tree.nodes;links=m.node_tree.links;p=next(n for n in nodes if n.type=='BSDF_PRINCIPLED');t=nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(texroot/('T_HH_Painted'+name+'.png')),check_existing=True);links.new(t.outputs['Color'],p.inputs['Base Color'])
  if key=='Timber':
   mul=nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.48,.42,.35,1);links.new(t.outputs['Color'],mul.inputs[1]);links.new(mul.outputs[0],p.inputs['Base Color'])
# Copy only forms whose existing geometry benefits from subtle irregularity.
for name in keep:
 old=bpy.data.objects['HH_Art_'+name];o=old.copy();o.data=old.data.copy();o.name='HH_Q2_'+name;lib.objects.link(o);o.hide_render=False;o.hide_set(False)
 bm=bmesh.new();bm.from_mesh(o.data);remaining=set(bm.verts)
 while remaining:
  seed=remaining.pop();group={seed};stack=[seed]
  while stack:
   v=stack.pop()
   for e in v.link_edges:
    q=e.other_vert(v)
    if q in remaining:remaining.remove(q);group.add(q);stack.append(q)
  center=sum((v.co for v in group),Vector())/len(group)
  fac=rng.uniform(.985,1.018) if name=='StoneWainscot2m' else rng.uniform(.996,1.004)
  for v in group:
   v.co=center+(v.co-center)*fac
   if name in ('StoneWainscot2m','Fireplace'):v.co+=Vector((rng.uniform(-.0015,.0015),rng.uniform(-.0015,.0015),rng.uniform(-.001,.001)))
   elif name not in ('Pillow',):v.co.z+=.0015*math.sin(v.co.x*8+v.co.y*3)
 bm.to_mesh(o.data);bm.free();o.data.update()
 if name=='FloorTile2m':
  for f in o.data.polygons:
   if abs(f.normal.z)>.8:
    for li in f.loop_indices:
     co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.y*1.8,co.x*.65)
 catalog[name]=o
# Soft folded coverlet: one reusable metre-scale mesh, not a new bed system.
def mesh(name,verts,faces,mats,indices=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('HH_Q2_'+name,me);lib.objects.link(o)
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):
  f.use_smooth=name=='Coverlet'
  if indices:f.material_index=indices[i]
 uv=me.uv_layers.new(name='UVMap')
 for f in me.polygons:
  for li in f.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co.x,co.y)
 catalog[name]=o;return o
vs=[];fs=[];nx=20;ny=14
for i in range(nx+1):
 for j in range(ny+1):
  x=-.65+1.3*i/nx;y=-.37+.74*j/ny;edge=max(0,(abs(y)-.28)/.09)
  z=.022+.016*math.sin(x*12+y*7)+.008*math.sin(y*24-x*9)-.09*edge*edge;vs.append((x,y,z))
for i in range(nx):
 for j in range(ny):
  a=i*(ny+1)+j;fs.append((a,a+ny+1,a+ny+2,a+1))
mesh('Coverlet',vs,fs,[bpy.data.materials['HH_Art_Sage']])
# Efficient tapered solid grass blades: no transparent cards / no collision.
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.93;return m
greens=[material('HH_Art_GrassLeaf'+str(i),c) for i,c in enumerate(((.19,.29,.07),(.28,.39,.115),(.39,.44,.13)))];flower=material('HH_Art_FlowerCream',(.74,.60,.33))
for name,count,radius,height in [('GrassSmall',9,.17,.22),('GrassMedium',18,.29,.39),('GrassLarge',28,.40,.55),('MeadowHerbs',12,.23,.31)]:
 vs=[];fs=[];idx=[]
 for b in range(count):
  ang=rng.random()*math.tau;r=radius*math.sqrt(rng.random());base=Vector((r*math.cos(ang),r*math.sin(ang),0));h=height*rng.uniform(.65,1);lean=Vector((math.cos(ang)*h*.35,math.sin(ang)*h*.35,0));side=Vector((-math.sin(ang),math.cos(ang),0))*rng.uniform(.012,.024);n=len(vs)
  for t,w in [(0,1),(.45,.85),(.8,.4),(1,0)]:
   mid=base+Vector((0,0,h*t))+lean*t*t;vs.extend([tuple(mid-side*w),tuple(mid+side*w)])
  for q in range(3):
   a=n+q*2;fs.append((a,a+1,a+3,a+2));idx.append(b%3)
  if name=='MeadowHerbs' and b%3==0:
   tip=base+Vector((0,0,h))+lean
   for petal in range(5):
    a=petal*math.tau/5;u=Vector((math.cos(a)*.045,math.sin(a)*.045,.005));v=Vector((-math.sin(a)*.017,math.cos(a)*.017,0));n=len(vs);vs.extend([tuple(tip),tuple(tip+u+v),tuple(tip+u*1.25),tuple(tip+u-v)]);fs.append((n,n+1,n+2,n+3));idx.append(3)
 mesh(name,vs,fs,greens+[flower],idx)
for name,scale in [('PebbleSmall',(.16,.12,.07)),('PebbleCluster',(.26,.18,.09))]:
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1);o=bpy.context.object;o.name='HH_Q2_'+name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for v in o.data.vertices:
  v.co*=rng.uniform(.91,1.09);v.co.z+=scale[2]*.70
 o.data.materials.append(bpy.data.materials['HH_Art_Stone'])
 for c in list(o.users_collection):c.objects.unlink(o)
 lib.objects.link(o);catalog[name]=o
# Hide original V1 review/library; new preview is linked to export data.
for a in list(s.objects):
 if a.name not in [x.name for x in catalog.values()]:a.hide_render=True;a.hide_set(True)
meta={}
for name,o in catalog.items():
 o.hide_set(False);o.hide_render=False
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-11],context='FACES');bm.to_mesh(o.data);bm.free();o.data.update()
 if not o.data.uv_layers:
  uv=o.data.uv_layers.new(name='UVMap')
  for f in o.data.polygons:
   for li in f.loop_indices:
    c=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(c.x,c.y)
 bpy.context.view_layer.update()
 meta[name]={'object':o.name,'size_cm':[round(v*100,4) for v in o.dimensions],'triangles':sum(len(f.vertices)-2 for f in o.data.polygons),'materials':[m.name for m in o.data.materials],'ground':name.startswith(('Grass','Meadow','Pebble'))}
preview=bpy.data.scenes.new('Quality Review');preview.world=bpy.data.worlds.new('Quality Studio');preview.world.use_nodes=True;bg=preview.world.node_tree.nodes.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.6;wo=preview.world.node_tree.nodes.new('ShaderNodeOutputWorld');preview.world.node_tree.links.new(bg.outputs['Background'],wo.inputs['Surface'])
for i,(name,o) in enumerate(catalog.items()):
 p=o.copy();p.data=o.data;preview.collection.objects.link(p);p.location=((i%4)*3.6,(i//4)*3.3,0);p.hide_set(False);p.hide_render=False
bpy.context.window.scene=preview;bpy.ops.object.light_add(type='AREA',location=(5,-2,14));bpy.context.object.data.energy=2100;bpy.context.object.data.size=10
bpy.ops.object.camera_add(location=(16,-18,21));cam=bpy.context.object;cam.rotation_euler=(Vector((5,4,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=20;preview.camera=cam
preview.render.engine='CYCLES';preview.cycles.samples=12;preview.render.resolution_x=1400;preview.render.resolution_y=1100;preview.render.resolution_percentage=100
for image in bpy.data.images:
 if image.source=='FILE':image.pack()
(OUT/'Props.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE));print('QUALITY_V2_SAVED',len(meta))
