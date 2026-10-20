"""Authored 3D furnishing family. Existing shell, openings, original sources and collision are retained."""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/HealingHouse';dst=A/'Source/HealingHouse_ArtV4.blend';assert not dst.exists();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.unit_settings.system='METRIC';rng=random.Random(420261020);parts=[];assets=[]
mat=bpy.data.materials.new('Painted crafted surface');mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF');v=mat.node_tree.nodes.new('ShaderNodeVertexColor');v.layer_name='Col';mat.node_tree.links.new(v.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.85
wood=(.28,.14,.062);edge=(.40,.24,.105);stone=(.43,.42,.33);sage=(.18,.29,.17);gold=(.62,.46,.19);cream=(.71,.65,.47)
def color(o,c):
 o.data.materials.clear();o.data.materials.append(mat);a=o.data.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
 for x in a.data:x.color=(*c,1)
 parts.append(o);return o
def mesh(n,vs,fs,c):
 m=bpy.data.meshes.new(n);m.from_pydata(vs,[],fs);m.update();o=bpy.data.objects.new(n,m);bpy.context.collection.objects.link(o);return color(o,c)
def box(n,loc,size,c,b=.008):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);color(o,c)
 if b:
  bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('hand softened edges','BEVEL');mod.width=b;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 return o
def tube(n,points,radii,c,sides=9):
 vs=[]
 for i,p in enumerate(points):
  d=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);d.normalize();u=d.cross(Vector((0,0,1)))
  if u.length<.1:u=d.cross(Vector((0,1,0)))
  u.normalize();v=d.cross(u)
  for j in range(sides):vs.append(tuple(Vector(p)+(u*math.cos(j*math.tau/sides)+v*math.sin(j*math.tau/sides))*radii[i]))
 fs=[tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))]
 for i in range(len(points)-1):
  for j in range(sides):fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
 return mesh(n,vs,fs,c)
def lathe(n,loc,profile,c,N=20):
 vs=[(loc[0]+r*math.cos(j*math.tau/N),loc[1]+r*math.sin(j*math.tau/N),loc[2]+z) for r,z in profile for j in range(N)];fs=[]
 for i in range(len(profile)-1):
  for j in range(N):fs.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
 return mesh(n,vs,fs,c)
def leaf(loc,a,L,W,c):
 dr=Vector((math.cos(a),math.sin(a),.6));side=Vector((-math.sin(a),math.cos(a),0));vs=[]
 for i in range(7):
  t=i/6;center=Vector(loc)+dr*L*t+Vector((0,0,.03*math.sin(t*math.pi)))
  for k in [-1,0,1]:vs.append(tuple(center+side*W*math.sin(t*math.pi)*k+Vector((0,0,.009*(1-abs(k))*math.sin(t*math.pi)))))
 return mesh('folded herb leaf',vs,[(i*3+k,(i+1)*3+k,(i+1)*3+k+1,i*3+k+1) for i in range(6) for k in range(2)],c)
def finish(n):
 global parts
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name=n;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=.000001);bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.01);bpy.ops.object.mode_set(mode='OBJECT');o.data.calc_loop_triangles();bad=sum(f.area<1e-12 for f in o.data.polygons)
 # Pointed herb tips are welded above; remove only zero-area tip faces from this new geometry.
 if bad:
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-12],context='FACES');bm.to_mesh(o.data);bm.free()
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False) if hasattr(bpy.ops.mesh,'normals_make_consistent') else None;bpy.ops.object.mode_set(mode='OBJECT');o.data.calc_loop_triangles();assert not any(f.area<1e-12 for f in o.data.polygons)
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_HH4_'+n+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False)
 assets.append({'name':n,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'zero_area_faces':0,'uv':True,'materials':1});parts=[];return o
# Irregular, physically bevelled flagstone apron, less than 2 cm high over the existing collider.
for iy in range(11):
 y=-2.6+iy*.49;x=-2.8+rng.uniform(-.23,.15)
 while x<2.7:
  width=rng.uniform(.34,.67);x2=min(2.8,x+width);c=tuple(k*rng.uniform(.84,1.14) for k in stone);box('worn limestone slab',((x+x2)/2,y,.008),(max(.04,x2-x-.012),.475+rng.uniform(-.008,.008),.016),c,.006);x=x2
finish('FlagstoneApron')
# Real arched firebox with deep backing and masonry voussoirs; not a decorative false doorway.
box('hearth', (0,-.08,.05),(1.92,.85,.10),stone,.02)
for x in [-.73,.73]:
 for z in [.24,.56,.88,1.20]:box('dressed sandstone pier',(x,.10,z),(.43,.58,.30),tuple(k*rng.uniform(.88,1.12) for k in stone),.024)
for i in range(11):
 a=i*math.pi/11;b=(i+.94)*math.pi/11;vs=[]
 for y in [-.20,.39]:
  for rad,t in [(.54,a),(.84,a),(.84,b),(.54,b)]:vs.append((rad*math.cos(t),y,1.13+rad*math.sin(t)))
 mesh('wedge arch stone',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],tuple(k*rng.uniform(.88,1.12) for k in stone))
box('sooted backed firebox',(0,.38,.72),(1.05,.045,1.35),(.055,.048,.034),.01);box('mantel',(0,.07,2.02),(2.02,.72,.14),edge,.025)
for z in [2.18,2.43,2.68]:box('chimney stonework',(0,.25,z),(1.4,.38,.23),stone,.018)
for i in range(4):tube('charred log',[(-.40+i*.08,-.06,.17),(.24+i*.06,.12,.23)],[.065,.055],(.085,.045,.021),12)
finish('Hearth')
# Small opaque flame tongues: emission only, no added lights or shadow casters.
for i in range(7):
 x=rng.uniform(-.30,.30);y=rng.uniform(-.1,.15);h=rng.uniform(.25,.55);vs=[(x-.055,y,.17),(x+.06,y,.17),(x+.035,y,.17+h*.45),(x+.04,y,.17+h),(x-.035,y,.17+h*.55)];mesh('warm flame',vs,[(0,1,2,3,4)],(1,.32,.055))
finish('HearthFlames')
# Joinery cabinet with filled shelves, individual jars, books and tied herbs.
for x in [-.60,.60]:box('carved upright',(x,.10,1.07),(.085,.42,2.14),wood,.015)
box('backboard',(0,.29,1.07),(1.22,.055,2.14),wood)
for z in [.12,.61,1.12,1.65,2.13]:box('shelf',(0,.07,z),(1.38,.52,.065),edge,.015)
for level,z in enumerate([.17,.66,1.17,1.70]):
 for i in range(5):
  x=-.49+i*.235;h=rng.uniform(.19,.32);r=rng.uniform(.065,.09);c=rng.choice([sage,cream,(.27,.35,.31),(.49,.32,.13)])
  lathe('pottery medicine jar',(x,.015,z),[(r*.6,0),(r,.025),(r,h*.7),(r*.45,h*.83),(r*.45,h),(r*.3,h)],c);lathe('cork lid',(x,.015,z+h),[(r*.4,0),(r*.4,.035)],edge,12)
  box('paper label',(x,-r-.001,z+h*.4),(.07,.003,.07),cream,.001)
for x in [-.41,-.14,.15,.42]:
 for i in range(4):leaf((x,.11,2.18),rng.random()*math.tau,.20,.035,sage)
finish('RemedyCabinet')
# Canopy with back curtain only: bed silhouette stays readable from the real camera.
for x in [-.94,.94]:
 for y in [-.56,.56]:lathe('turned bed post',(x,y,0),[(.045,0),(.055,.10),(.033,.23),(.033,1.53),(.055,1.58),(.035,1.72),(.015,1.78)],wood,16)
for y in [-.56,.56]:box('upper rail',(0,y,1.60),(1.96,.06,.08),edge)
for x in [-.94,.94]:box('cross rail',(x,0,1.60),(.06,1.18,.08),edge)
vs=[]
for iz,z in enumerate([.94,1.23,1.53]):
 for ix in range(33):
  x=-.91+ix*1.82/32;vs.append((x,.56+.035*math.sin(ix*math.pi*.5),z-.03*math.cos(ix*.4)))
mesh('pleated linen privacy curtain',vs,[(iz*33+ix,iz*33+ix+1,(iz+1)*33+ix+1,(iz+1)*33+ix) for iz in range(2) for ix in range(32)],(.39,.46,.30))
finish('BedCanopy')
# Folded hanging banner with an original six-leaf herb/seed emblem in relief.
vs=[]
for z in range(13):
 for x in range(9):vs.append(((x/8-.5)*.86,.025*math.sin(x*1.3+z*.28),z/12*1.32))
mesh('woven hanging cloth',vs,[(z*9+x,z*9+x+1,(z+1)*9+x+1,(z+1)*9+x) for z in range(12) for x in range(8)],(.13,.25,.16));tube('hanging rail',[(-.51,.03,1.38),(.51,.03,1.38)],[.025,.025],edge,12)
tube('seed stem',[(0,-.03,.22),(0,-.035,1.10)],[.009,.007],gold,8)
for z in [.42,.64,.86]:
 for sign in [-1,1]:
  pts=[(0,-.04,z),(sign*.17,-.045,z+.09),(sign*.25,-.04,z+.19)];tube('leaf outline',pts,[.008,.014,.003],gold,8)
lathe('seed emblem',(0,-.055,1.05),[(.025,0),(.06,.045),(.01,.10)],gold,16)
finish('HerbalBanner')
# Long windowbox shelf, with a physical bracket and small trailing leaf shapes.
box('wall shelf',(0,.1,.05),(1.25,.30,.10),edge)
for x in [-.49,.49]:tube('shelf bracket',[(x,.23,-.30),(x,-.03,.01)],[.025,.025],wood,8)
for x in [-.41,0,.41]:
 lathe('herb pot',(x,.09,.10),[(.08,0),(.115,.17),(.12,.19),(.095,.20)],(.41,.24,.11))
 for i in range(11):leaf((x,.09,.26),rng.random()*math.tau,rng.uniform(.16,.27),rng.uniform(.018,.04),sage)
finish('HerbalWindowShelf')
# Reusable root / fallen branch, tapered curved topology, keeps paths physically clear.
tube('fallen branch',[(-.70,0,.05),(-.32,.05,.10),(0,0,.15),(.36,-.08,.10),(.73,-.05,.06)],[.04,.065,.07,.045,.013],wood,12)
for sign in [-1,1]:tube('branch fork',[(.15*sign,0,.14),(.29*sign,.28,.11),(.52*sign,.39,.07)],[.045,.028,.008],wood,10)
finish('FallenBranch')
for i,o in enumerate(bpy.context.scene.objects):o.location.x=i*4
bpy.ops.wm.save_as_mainfile(filepath=str(dst));bpy.ops.wm.open_mainfile(filepath=str(dst),load_ui=False);assert len([o for o in bpy.data.objects if o.type=='MESH'])==len(assets)
(A/'ArtV4_Props.json').write_text(json.dumps({'source':str(dst.relative_to(R)),'units':'m','assets':assets,'reopened':True,'new_maps':False,'purpose':'Existing room dressing; shell/openings/colliders are retained; no paid assets'},indent=2));print('ART_V4_PROPS_REOPENED',json.dumps(assets))
