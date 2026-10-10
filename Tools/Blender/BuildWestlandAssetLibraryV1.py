"""Authored Westland prop family. Background only; source preservation and review gates.
Metres, Z-up, ground pivots. Curved branches, leaf surfaces, timber joinery, chipped stone.
Existing bench/herb mesh construction reused from Healing House; shared sources never saved.
"""
import bpy,bmesh,math,random,json,sys
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/World/WestlandAssetLibrary';OUT=ROOT/'Saved/WestlandAssetLibrary';rng=random.Random(45117)
assert bpy.app.background
HERO='--heroes' in sys.argv
SOURCE=ART/'Source'/('WestlandAssetLibrary_HeroReview_V1c.blend' if HERO else 'WestlandAssetLibrary_V1.blend')
assert not SOURCE.exists(),'Never overwrite a pre-existing source; create versioned revision'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
mats={};specs={};parts=[];catalog=[];collisions=[]
def material(key,color,tex=None,two=False):
 m=bpy.data.materials.new('WLA_'+key);m.use_nodes=True;m.diffuse_color=(*color,1)
 bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.87
 if tex:
  n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(ROOT/tex),check_existing=True)
  mix=m.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*color,1);m.node_tree.links.new(n.outputs['Color'],mix.inputs[1]);m.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
 mats[key]=m;specs[key]={'color':color,'texture':tex,'two_sided':two};return m
for k,c,t in [('Bark',(.85,.84,.77),'Bark'),('Birch',(.88,.88,.78),'Birch'),('Leaf',(.70,.84,.62),'LeafSummer'),('LeafLight',(.92,.94,.75),'LeafSummer'),('LeafDark',(.46,.66,.40),'LeafSummer'),('Straw',(.9,.85,.65),'Straw')]:material(k,c,'Art/World/WestlandAssetLibrary/Textures/T_WLA_'+t+'.png',k.startswith('Leaf'))
material('Wood',(1,.91,.78),'Art/HealingHouse/Textures/QualityV2/T_HH_PaintedWood.png');material('Timber',(.43,.40,.32),'Art/HealingHouse/Textures/QualityV2/T_HH_PaintedWood.png')
material('Stone',(.91,.96,.90),'Art/HealingHouse/Textures/QualityV2/T_HH_PaintedStone.png');material('Moss',(.54,.72,.39),'Art/World/WestlandAssetLibrary/Textures/T_WLA_Leaf.png')
material('MossStone',(.91,.96,.90),'Art/HealingHouse/Textures/QualityV2/T_HH_PaintedStone.png')
m=mats['MossStone'];bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');mix=next(n for n in m.node_tree.nodes if n.type=='MIX_RGB');attr=m.node_tree.nodes.new('ShaderNodeVertexColor');attr.layer_name='PaintTint';tintnode=m.node_tree.nodes.new('ShaderNodeMixRGB');tintnode.blend_type='MULTIPLY';tintnode.inputs[0].default_value=1;m.node_tree.links.new(mix.outputs[0],tintnode.inputs[1]);m.node_tree.links.new(attr.outputs['Color'],tintnode.inputs[2]);m.node_tree.links.new(tintnode.outputs[0],bs.inputs['Base Color']);specs['MossStone']['vertex_color']=True
for k,c in [('Iron',(.09,.11,.09)),('Apple',(.48,.12,.055)),('FlowerCream',(.82,.74,.53)),('FlowerBlue',(.29,.32,.49)),('Gold',(.53,.32,.10)),('Rune',(.34,.52,.46))]:material(k,c)
def raw(v,f,key,uvs=None,smooth=True):
 me=bpy.data.meshes.new('WLA_surface');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('part',me);s.collection.objects.link(o);o.data.materials.append(mats[key]);parts.append(o)
 uv=me.uv_layers.new(name='UV0')
 for face in me.polygons:
  face.use_smooth=smooth
  for li in face.loop_indices:
   vi=me.loops[li].vertex_index;c=me.vertices[vi].co
   if uvs:uv.data[li].uv=uvs[vi]
   else:
    axis=max(range(3),key=lambda i:abs(face.normal[i]));a,b=((1,2),(0,2),(0,1))[axis];uv.data[li].uv=(c[a],c[b])
 return o
def tube(points,radii,key='Bark',sides=12,twist=.12):
 pts=[Vector(p) for p in points];v=[];uv=[];f=[]
 for j,(p,r) in enumerate(zip(pts,radii)):
  tangent=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized();a=tangent.cross(Vector((0,1,0))).normalized()
  if a.length<.1:a=Vector((1,0,0))
  b=tangent.cross(a).normalized()
  for i in range(sides+1):
   angle=math.tau*i/sides;rr=r*(1+twist*math.sin(i*3.17+j*.56));v.append(p+(a*math.cos(angle)+b*math.sin(angle))*rr);uv.append((i/sides,j/(len(pts)-1)*max(1,(pts[-1]-pts[0]).length/2)))
 for j in range(len(pts)-1):
  for i in range(sides):q=j*(sides+1)+i;f.append((q,q+1,q+sides+2,q+sides+1))
 f.extend([tuple(range(sides-1,-1,-1)),tuple((len(pts)-1)*(sides+1)+i for i in range(sides))]);return raw(v,f,key,uv)
def plank(center,dim,key='Wood',rot=(0,0,0),wear=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=center);o=bpy.context.object;o.scale=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for v in o.data.vertices:v.co+=Vector((rng.uniform(-wear,wear),rng.uniform(-wear,wear),rng.uniform(-wear/2,wear/2)))
 mod=o.modifiers.new('Worn rounded arris','BEVEL');mod.width=min(.022,min(dim)*.13);mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 o.rotation_euler=rot;o.data.materials.append(mats[key]);parts.append(o)
 uv=o.data.uv_layers.active
 for f in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(f.normal[i]));a,b=((1,2),(0,2),(0,1))[axis]
  for li in f.loop_indices:c=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(c[a]*1.2,c[b]*1.2)
 return o
def leaf(base,direction,length,width,key='Leaf',lobed=False):
 base=Vector(base);direction=Vector(direction).normalized();side=direction.cross(Vector((0,0,1))).normalized()
 if side.length<.1:side=Vector((1,0,0))
 up=side.cross(direction).normalized();v=[];uv=[];f=[]
 for j in range(7):
  t=j/6;w=width*math.sin(math.pi*t)**.65*(1+.20*math.sin(j*2.7) if lobed else 1)
  for k in (-1,0,1):v.append(base+direction*length*t+side*w*k+up*(.10*length*math.sin(math.pi*t)-abs(k)*width*.18));uv.append((.12+t*.76,.5+k*.38))
 for j in range(6):
  for k in range(2):q=j*3+k;f.append((q,q+1,q+4,q+3))
 return raw(v,f,key,uv)
def leafcloud(center,size,count):
 c=Vector(center)
 # A sculpted opaque leafy core unifies the canopy; curved peripheral leaves break its contour.
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4,radius=1,location=c);o=bpy.context.object
 for vert in o.data.vertices:
  p=vert.co;rr=1+.11*math.sin(p.x*5+p.y*3)*math.cos(p.z*6)+.07*math.sin(p.y*11+p.x*8);vert.co=Vector((p.x*size[0]*rr*.89,p.y*size[1]*rr*.89,p.z*size[2]*rr*.90))
 for face in o.data.polygons:face.use_smooth=True
 o.data.materials.append(mats['Leaf']);parts.append(o);uv=o.data.uv_layers.new(name='UV0')
 for face in o.data.polygons:
  for li in face.loop_indices:
   p=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(p.x*.42+p.z*.20,p.y*.40+p.z*.22)
 for i in range(count):
  a=rng.uniform(0,math.tau);z=rng.uniform(-.85,1);radius=math.sqrt(max(0,1-z*z))*rng.uniform(.73,1)
  p=c+Vector((math.cos(a)*size[0]*radius,math.sin(a)*size[1]*radius,size[2]*z));ang=a+rng.uniform(-.6,.6)
  leaf(p,(math.cos(ang),math.sin(ang),rng.uniform(-.4,.8)),rng.uniform(.40,.72),rng.uniform(.13,.26),['LeafDark','Leaf','LeafLight'][min(2,max(0,int((z+1)*1.4)))],True)
def sphere(center,size,key,seed=0,segments=24,rings=12):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,radius=1,location=center);o=bpy.context.object;o.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for v in o.data.vertices:
  c=v.co;v.co*=1+.035*math.sin(c.x*7+c.y*4+c.z*9+seed)
 for f in o.data.polygons:f.use_smooth=True
 o.data.materials.append(mats[key]);parts.append(o);return o
def rock(center,size,seed,moss=True):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4,radius=1,location=center);o=bpy.context.object
 for v in o.data.vertices:
  c=v.co;rr=1+.13*math.sin(c.x*4.1+seed)*math.cos(c.y*6+c.z*5)+.055*math.sin(c.z*14+c.x*12);v.co=Vector((c.x*size[0]*rr,c.y*size[1]*rr,c.z*size[2]*rr))
 mod=o.modifiers.new('Weather softened','SMOOTH');mod.factor=.35;mod.iterations=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 o.data.materials.append(mats['MossStone'] if moss else mats['Stone']);parts.append(o)
 if moss:
  col=o.data.color_attributes.new(name='PaintTint',type='FLOAT_COLOR',domain='POINT')
  for v in o.data.vertices:
   p=v.co;w=max(0,min(1,(p.z/size[2]-.05)*.8))*(.5+.5*math.sin(p.x*3+p.y*2+seed))
   col.data[v.index].color=(1-.30*w,1-.10*w,1-.52*w,1)
 uv=o.data.uv_layers.new(name='UV0')
 for f in o.data.polygons:
  f.use_smooth=True;f.material_index=0
  axis=max(range(3),key=lambda i:abs(f.normal[i]));a,b=((1,2),(0,2),(0,1))[axis]
  for li in f.loop_indices:p=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(p[a]*.65,p[b]*.65)
 return o
def end(name,family,collision='none',bodies=None,provenance='new authored form'):
 global parts
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=parts[0];o.name='SM_'+name
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 # Compact material slots without altering geometric form.
 used=sorted(set(f.material_index for f in o.data.polygons));old=list(o.data.materials);indices=[used.index(f.material_index) for f in o.data.polygons];o.data.materials.clear()
 for i in used:o.data.materials.append(old[i])
 for f,i in zip(o.data.polygons,indices):f.material_index=i
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-9],context='FACES');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();o.data.calc_loop_triangles()
 lo=[min(v.co[i] for v in o.data.vertices) for i in range(3)];hi=[max(v.co[i] for v in o.data.vertices) for i in range(3)]
 # Ground-align entire visual mesh; retains authored shape, never scale world/player.
 for v in o.data.vertices:v.co.z-=lo[2]
 height=hi[2]-lo[2];bbox=[hi[i]-lo[i] for i in range(3)];bbox[2]=height
 col=[]
 for j,body in enumerate(bodies or []):
  bpy.ops.mesh.primitive_cube_add(size=1,location=body[0]);c=bpy.context.object;c.name='UCX_'+o.name+'_'+str(j).zfill(2);c.scale=body[1];bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);c.hide_render=True;c.hide_set(True);col.append(c.name)
 catalog.append({'id':name,'object':o.name,'family':family,'dimensions_m':bbox,'triangles':len(o.data.loop_triangles),'materials':[m.name for m in o.data.materials],'collision':collision,'collision_objects':col,'provenance':provenance,'variant':'B' if name.endswith('_B') else 'A','uv':'UV0','origin_m':[0,0,0],'status':'needs_visual_review'})
 coll=bpy.data.collections.new(name);s.collection.children.link(coll)
 for x in [o]+[bpy.data.objects[n] for n in col]:
  for c in list(x.users_collection):c.objects.unlink(x)
  coll.objects.link(x)
 parts=[];return o

def tree(name,height,width,birch=False,fruit=False,ancient=False,variant=0):
 bark='Birch' if birch else 'Bark';trunk=.15 if birch else (.50 if ancient else .25);bend=(-.3 if variant else .25)
 tube([(0,0,0),(.09,-.06,height*.15),(bend,.1,height*.36),(.08,-.05,height*.65)], [trunk*1.6,trunk,trunk*.74,trunk*.28],bark,16)
 for i in range(7 if ancient else 4):
  a=i*2.399+variant*.55;tube([(0,0,.36),(math.cos(a)*trunk,math.sin(a)*trunk,.20),(math.cos(a)*trunk*2,math.sin(a)*trunk*2,.09),(math.cos(a)*trunk*3,math.sin(a)*trunk*3,.025)],[trunk*.45,trunk*.28,trunk*.14,.025],bark,10)
 clusters=[]
 for i in range(9 if ancient else 6):
  a=i*2.399+variant*.44;r=width*(.22 if birch else .29);z=height*(.68+.17*i/(8 if ancient else 5));tip=(math.cos(a)*r,math.sin(a)*r,z)
  tube([(bend,.05,height*.30),(.2*math.cos(a),.2*math.sin(a),height*.43),tip],[trunk*.50,trunk*.30,.035],bark,10)
  sx=width*(.25 if birch else .31);clusters.append((tip,(sx,sx*.88,height*.14)))
 for p,sz in clusters:leafcloud(p,sz,65 if ancient else 55)
 if fruit:
  for j in range(28):
   a=rng.uniform(0,math.tau);r=width*rng.uniform(.15,.40);sphere((r*math.cos(a),r*math.sin(a),height*rng.uniform(.56,.76)),(.07,.07,.075),'Apple',segments=12,rings=6)
 return end(name,'Trees','trunk_only',[((0,0,height*.21),(trunk*1.8,trunk*1.8,height*.42))])

def bush(name,variant=0):
 for j in range(7):
  a=j*2.399;tip=(math.cos(a)*.45,math.sin(a)*.4,.7+rng.random()*.3);tube([(0,0,0),(.1*math.cos(a),.1*math.sin(a),.35),tip],[.035,.02,.005],'Bark',7);leafcloud(tip,(.48,.42,.35),25)
 return end(name,'Vegetation')
def fern(name,variant=0):
 for j in range(9):
  a=j*2.399+variant*.2;d=Vector((math.cos(a),math.sin(a),0));h=rng.uniform(.55,.9)
  pts=[Vector((0,0,.03)),d*.20+Vector((0,0,h*.65)),d*.46+Vector((0,0,h)),d*.63+Vector((0,0,h*.82))];tube(pts,[.012,.009,.005,.001],'LeafDark',5)
  for k in range(1,10):
   t=k/10;p=d*.60*t+Vector((0,0,h*math.sin(t*1.8)));side=Vector((-d.y,d.x,.12));length=.21*math.sin(t*math.pi)**.8
   for sign in (-1,1):leaf(p,side*sign+d*.35,length,.025,'LeafLight' if j%3==0 else 'Leaf')
 return end(name,'Vegetation')
def imported(name,source_name,ground=False):
 with bpy.data.libraries.load(str(ROOT/'Art/HealingHouse/Source/HealingHouse_QualityV3.blend'),link=False) as (a,b):b.objects=[source_name]
 o=b.objects[0];s.collection.objects.link(o);o.location=(0,0,0);o.rotation_euler=(0,0,0);o.scale=(1,1,1)
 if ground:
  remove=[i for i,m in enumerate(o.data.materials) if m and 'Ceramic' in m.name];bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index in remove],context='FACES');bm.to_mesh(o.data);bm.free()
 for i,m in enumerate(o.data.materials):
  key=m.name.split('_')[-1].split('.')[0];o.data.materials[i]=mats.get({'Metal':'Iron','Flower':'FlowerBlue'}.get(key,key),mats['Wood'])
 parts.append(o);return end(name,'Vegetation' if ground else 'Village','none' if ground else 'simple',None if ground else [((0,0,.25),(1.36,.66,.50)),((0,.32,.80),(1.36,.08,.75))],'reuses '+source_name+' from HealingHouse_QualityV3; pot removed' if ground else 'unchanged HH_Q3_Bench construction; painted material family reused')

def stump(name,variant=0):
 tube([(0,0,0),(.02+variant*.08,.01,.35),(-.04+variant*.10,.03,.85)],[.5,.35,.32],'Bark',20)
 for j in range(5):
  a=j*2.4+variant*.4;d=Vector((math.cos(a),math.sin(a),0));tube([(0,0,.22),d*.44+Vector((0,0,.12)),d*.90],[.17,.13,.025],'Bark',8)
 # Exposed cut face, separate timber cap.
 tube([(-.04,.03,.84),(-.04,.03,.865)],[.29,.29],'Wood',24)
 for rr in (.11,.19,.25):
  pts=[(-.04+rr*math.cos(i*math.tau/32),.03+rr*math.sin(i*math.tau/32),.869) for i in range(33)];tube(pts,[.004]*33,'Timber',4)
 return end(name,'Landscape','simple',[((0,0,.4),(.65,.65,.8))])
def root(name,variant=0):
 for i in range(4):
  a=i*.7-.8+variant*.32;tube([(-.7,.08*variant,.1),(-.3,.06,.32+variant*.06),(.4*math.cos(a),.4*math.sin(a),.18),(1.0*math.cos(a),1.0*math.sin(a),.02)],[.10,.16,.08,.015],'Bark',9)
 return end(name,'Landscape')
def fence(name,variant=0):
 for x in (-.9,.9):tube([(x,0,0),(x+.015,0,.6),(x-.015,.02,1.15)],[.085,.075,.06],'Wood',8)
 for z in (.38,.82):plank((0,0,z),(1.95,.10,.13),rot=(0,.015*(-1 if variant else 1),0))
 for x in (-.9,.9):
  for z in (.38,.82):sphere((x,-.066,z),(.018,.009,.018),'Iron',segments=8,rings=4)
 return end(name,'Village','simple',[((0,0,.56),(2,.18,1.12))])
def sign(name,variant=0):
 tube([(0,0,0),(.015,0,1.1),(-.05,.01,2.15)],[.065,.05,.04],'Wood',10)
 for z,sgn in [(1.48+variant*.09,1),(1.88+variant*.13,-1)]:
  outline=[(-.55,-.055,z-.11),(.35,-.055,z-.11),(.53,-.055,z),(.35,-.055,z+.11),(-.55,-.055,z+.11)];outline=[(x*sgn,y,z) for x,y,z in outline];v=outline+[(x,y+.10,z) for x,y,z in outline];f=[tuple(range(4,-1,-1)),tuple(range(5,10))]+[(j,(j+1)%5,(j+1)%5+5,j+5) for j in range(5)];raw(v,f,'Wood',smooth=False)
  for x in (-.2,.12):sphere((x,-.063,z),(.016,.008,.016),'Iron',segments=8,rings=4)
 return end(name,'Village','simple',[((0,0,1.075),(.14,.14,2.15))])
def ring(center,r,t,key='Iron',rot=(0,0,0)):
 bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=6,major_radius=r,minor_radius=t,location=center,rotation=rot);o=bpy.context.object;o.data.materials.append(mats[key]);parts.append(o)
def barrel(name,variant=0):
 N=18
 for i in range(N):
  a=i*math.tau/N;v=[]
  for z,r in [(0,.32),(.12,.36),(.50,.43+variant*.035),(.90,.36),(1,.32)]:
   for side in (-.49,.49):q=a+side*math.tau/N;v.append((math.cos(q)*r,math.sin(q)*r,z))
  raw(v,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(4)],'Wood',[(i/N+k*.02,j*.28) for j in range(5) for k in range(2)])
 for z,r in [(.13,.367),(.33,.41),(.72,.408),(.89,.367)]:ring((0,0,z),r,.018)
 for x in [-.24,-.12,0,.12,.24]:plank((x,0,.975),(.116,2*math.sqrt(max(.01,.32**2-x*x)),.035),wear=.002)
 return end(name,'Village','simple',[((0,0,.50),(.78,.78,1))])
def crate(name,variant=0):
 for z in (.16,.36,.56):
  for y in (-.38,.38):plank((0,y,z),(.85,.065,.185))
  for x in (-.405,.405):plank((x,0,z),(.065,.72,.185))
 for x in (-.37,.37):
  for y in (-.35,.35):plank((x,y,.34),(.075,.075,.67),'Timber')
 for i in range(4):plank((-.30+i*.20,0,.67),(.195,.75,.06))
 for y in (-.42,.42):plank((0,y,.34),(.88,.045,.075),'Timber',rot=(0,-.54,0))
 return end(name,'Village','simple',[((0,0,.35),(.9,.85,.7))])
def cart(name,variant=0):
 for x in (-.62,.62):plank((x,0,.64),(.09,1.95,.13),'Timber')
 for j in range(8):plank((0,-.8+j*.23,.76),(1.22,.215,.065))
 for z in (.91,1.14):
  for x in (-.64,.64):plank((x,0,z),(.065,1.92,.18))
  plank((0,.93,z),(1.32,.065,.18))
 for x in (-.64,.64):
  for y in (-.88,.88):plank((x,y,1),(.09,.09,.54),'Timber')
 tube([(-.83,.15,.48),(.83,.15,.48)],[.07,.07],'Iron',10)
 for x in (-.80,.80):
  ring((x,.15,.48),.43,.055,'Timber',rot=(0,math.pi/2,0));ring((x,.15,.48),.435,.015,'Iron',rot=(0,math.pi/2,0))
  for j in range(10):
   a=j*math.tau/10;tube([(x,.15,.48),(x,.15+math.cos(a)*.40,.48+math.sin(a)*.40)],[.025,.02],'Wood',6)
  tube([(x-.08,.15,.48),(x+.08,.15,.48)],[.09,.09],'Wood',12)
 for x in (-.55,.55):plank((x,-1.5,.65),(.09,1.50,.08),'Wood',rot=(.06,0,0))
 return end(name,'Village','simple',[((0,0,1),(1.4,1.9,.65)),((-.8,.15,.46),(.13,.90,.90)),((.8,.15,.46),(.13,.90,.90))])
def hay(name,variant=0):
 # Deformed bale with layered straw texture and tied ropes, no loose transparent overdraw.
 o=plank((0,0,.46),(1.20,.78,.86),'Straw',wear=.065)
 for x in (-.37,.37):
  pts=[(x,-.43,.12),(x,-.44,.85),(x,-.30,.93),(x,.35,.93),(x,.43,.84),(x,.43,.12),(x,.3,.04),(x,-.35,.04),(x,-.43,.12)];tube(pts,[.018]*len(pts),'Timber',6)
 return end(name,'Farm','simple',[((0,0,.46),(1.25,.82,.90))])
def woodpile(name,variant=0):
 for row in range(3-variant):
  for j in range(5+variant-row):
   x=(j-(4+variant-row)/2)*.27;z=.14+row*.23;tube([(x,-.65,z),(x+.012,0,z),(x,.65,z)],[.13,.12,.125],'Bark',12);tube([(x,-.657,z),(x,-.666,z)],[.113,.113],'Wood',12)
 return end(name,'Farm','simple',[((0,0,.4),(1.5,1.3,.8))])
def ruin(name,kind,variant=0):
 if kind=='column':
  plank((0,0,.10),(.88,.88,.20),'Stone',wear=.045);tube([(0,0,.20),(.015,-.02,.7),(-.03,.02,1.40),(.04,.0,1.8)],[.29,.27,.25,.22],'Stone',16,.15)
  for j in range(8):
   a=j*math.tau/8;tube([(.27*math.cos(a),.27*math.sin(a),.30),(.25*math.cos(a),.25*math.sin(a),1.35)],[.012,.012],'Stone',5)
  for i in range(14):leaf((rng.uniform(-.3,.3),rng.uniform(-.3,.3),rng.uniform(.15,.8)),(1,.4,.4),.15,.05,'LeafDark')
  bodies=[((0,0,.90),(.66,.66,1.8))]
 elif kind=='rune':
  o=rock((0,0,.9),(.56,.32,1.10),4+variant)
  # Raised inset rune ribbons; decorative, not a gameplay actor.
  for pts in [[(-.16,-.315,.5),(-.16,-.34,1.45),(.12,-.33,1.25),(-.16,-.34,1.07)],[(.02,-.34,.62),(.19,-.34,.83),(.02,-.34,1.04)]]:tube(pts,[.012]*len(pts),'Rune',5)
  bodies=[((0,0,1),(.82,.5,2))]
 else:
  for row in range(4):
   count=5 if row<2 else 4-row//3
   for j in range(count):
    x=(j-2)*.5+(row%2)*.20;z=.20+row*.37;plank((x,0,z),(.49,.52,.36),'Stone',wear=.055)
  for j in range(28):
   a=rng.uniform(0,math.tau);leaf((rng.uniform(-1,1),-.28,rng.uniform(.1,1.2)),(math.cos(a),.15,math.sin(a)),.18,.065,'Leaf')
  bodies=[((0,0,.75),(2.4,.58,1.5))]
 return end(name,'Ruins','simple',bodies)
def grass(name,variant=0):
 for j in range(24):
  a=j*2.399;h=rng.uniform(.15,.40);leaf((rng.uniform(-.18,.18),rng.uniform(-.18,.18),0),(math.cos(a)*.30,math.sin(a)*.30,1),h,.012,'LeafLight' if j%4==0 else 'Leaf')
 return end(name,'Vegetation')

# Six representative meshes reviewed before family expansion.
tree('WLA_OakAncient_A',12,7,ancient=True);tree('WLA_OakYoung_A',5,2.8)
fern('WLA_Fern_A');rock((0,0,1),(1.4,1.0,1.10),2);end('WLA_Boulder_A','Landscape','simple',[((0,0,1),(2.3,1.7,2))])
imported('WLA_Bench_A','HH_Q3_Bench');ruin('WLA_Runestone_A','rune')
if not HERO:
 assert (OUT/'HeroReviewAccepted.json').exists(),'Local visual review required before expanding'
 for suffix,v in [('_A',0),('_B',1)]:
  if v:tree('WLA_OakAncient'+suffix,11.6,7.1,ancient=True,variant=v);tree('WLA_OakYoung'+suffix,5.1,2.7,variant=v);fern('WLA_Fern'+suffix,v);rock((0,0,1.05),(1.35,1.10,1.1),7);end('WLA_Boulder'+suffix,'Landscape','simple',[((0,0,1),(2.3,1.8,2))]);ruin('WLA_Runestone'+suffix,'rune',v)
  tree('WLA_Birch'+suffix,9,3.4,birch=True,variant=v);tree('WLA_FruitTree'+suffix,5,4,fruit=True,variant=v);bush('WLA_Bush'+suffix,v);grass('WLA_Grass'+suffix,v)
  if v==0:imported('WLA_Herb_A','HH_Q3_BroadHerb',True);imported('WLA_Wildflowers_A','HH_Q3_FlowerPlant',True)
  else:imported('WLA_Herb_B','HH_Q3_NarrowHerb',True)
  for j in range(5):rock((rng.uniform(-.45,.45),rng.uniform(-.4,.4),.1),(.12+rng.random()*.15,.12+rng.random()*.13,.10+rng.random()*.10),j+v,False)
  end('WLA_SmallStones'+suffix,'Landscape');stump('WLA_Stump'+suffix,v);root('WLA_Root'+suffix,v);fence('WLA_Fence'+suffix,v);sign('WLA_Signpost'+suffix,v);cart('WLA_Cart'+suffix,v);barrel('WLA_Barrel'+suffix,v);crate('WLA_Crate'+suffix,v);hay('WLA_Haybale'+suffix,v);woodpile('WLA_Woodpile'+suffix,v);ruin('WLA_Column'+suffix,'column',v);ruin('WLA_WallRemnant'+suffix,'wall',v)
 # Bench B is deliberately reuse, not a needless duplicate mesh. Color variation handled as instance.

(ART/('Heroes.json' if HERO else 'Assets.json')).write_text(json.dumps({'units':'metres','materials':specs,'assets':catalog},indent=2)+'\n')
# Review gallery uses collection instances, source meshes remain grounded at origin.
for c in s.collection.children:
 if c.name.startswith('WLA_'):c.hide_render=True;c.hide_viewport=True
for i,item in enumerate(catalog):
 col=bpy.data.collections[item['id']];ob=bpy.data.objects.new('Review_'+item['id'],None);ob.instance_type='COLLECTION';ob.instance_collection=col;s.collection.objects.link(ob);ob.location=((i%6)*8,(i//6)*8,0)
s.world=bpy.data.worlds.new('WestlandReviewWorld');s.world.color=(.25,.25,.25)
bpy.ops.object.camera_add(location=(20,-24,24));cam=bpy.context.object;cam.name='ReviewCamera';target=Vector((16,8,1));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=50;s.camera=cam
bpy.ops.object.light_add(type='AREA',location=(10,-10,22));bpy.context.object.data.energy=2800;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=18
s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=1600;s.render.resolution_y=1000;s.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE));print('WLA_SOURCE_SAVED',SOURCE,len(catalog))
