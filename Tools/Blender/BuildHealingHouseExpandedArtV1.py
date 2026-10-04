"""Author reusable, metre-scale interior props in a NEW Blender source.
Existing V3 sources are opened read-only in a separate audit, never overwritten.
Run background Blender. Export is deliberately a separate, post-review step.
"""
import bpy, bmesh, math, json, random, sys
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; ART=ROOT/'Art/HealingHouse'
SOURCE=ART/'Source/HealingHouse_ExpandedArt_V1.blend'
assert bpy.app.background and (not SOURCE.exists() or '--revise-owned-source' in sys.argv), 'Do not overwrite an existing source'
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.name='HealingHouse_ExpandedArt_V1';s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
random.seed(7319)
colors={'Wood':(.29,.145,.058),'Timber':(.095,.044,.018),'Plaster':(.66,.52,.34),'Stone':(.29,.265,.22),'Mortar':(.12,.10,.075),'Sage':(.15,.245,.105),'Linen':(.58,.49,.31),'Gold':(.54,.34,.10),'Metal':(.045,.052,.032),'Leaf':(.105,.22,.075),'LeafLight':(.23,.34,.105),'Flower':(.49,.235,.22),'Ceramic':(.39,.215,.11),'Glass':(.11,.26,.20),'Book':(.16,.20,.26),'Paper':(.63,.55,.35),'Fire':(1,.235,.018),'Window':(.40,.50,.34)}
mats={}
for name,color in colors.items():
 m=bpy.data.materials.new('HH_Art_'+name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=next(n for n in m.node_tree.nodes if n.bl_idname=='ShaderNodeBsdfPrincipled');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.85
 # Gentle small-scale tonal variation, never giant grain. Portable UE equivalents
 # use the same palette plus a shared authored texture.
 if name in ('Wood','Timber','Stone','Plaster','Sage','Linen'):
  nodes=m.node_tree.nodes;links=m.node_tree.links;noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=18 if name in ('Sage','Linen') else 5
  ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=tuple(c*.82 for c in color)+(1,);ramp.color_ramp.elements[1].color=tuple(min(1,c*1.13) for c in color)+(1,)
  links.new(noise.outputs['Fac'],ramp.inputs['Fac']);links.new(ramp.outputs['Color'],p.inputs['Base Color'])
 if name in ('Fire','Window'):
  p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=2 if name=='Fire' else .35
 mats[name]=m
parts=[];catalog={}
def finish(o,mat,bevel=0):
 o.data.materials.append(mats[mat]);parts.append(o)
 if bevel:
  b=o.modifiers.new('Crafted rounded edges','BEVEL');b.width=bevel;b.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
 return o
def box(loc,size,mat='Wood',bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,mat,bevel)
def cyl(loc,radius,height,mat='Wood',rotation=(0,0,0),vertices=16):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=height,location=loc,rotation=rotation);return finish(bpy.context.object,mat,.004)
def ellipsoid(loc,size,mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,location=loc);o=bpy.context.object;o.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for f in o.data.polygons:f.use_smooth=True
 return finish(o,mat)
def beam(a,b,width,mat='Timber'):
 delta=Vector(b)-Vector(a);o=box((Vector(a)+Vector(b))/2,(width,width,delta.length),mat,.008);o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return o
def end(name):
 global parts
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=parts[0];o.name='HH_Art_'+name
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-10],context='FACES');bm.to_mesh(o.data);bm.free();o.data.update()
 # Metre UVs derived from local faces, unaffected by actor/room scaling.
 uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap')
 for f in o.data.polygons:
  axes=([1,2] if abs(f.normal.x)>.8 else [0,2] if abs(f.normal.y)>.8 else [0,1])
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 # Independent FBX models have exactly one local-origin mesh; source preview
 # composition uses linked copies in another collection, never baked room coords.
 o['ReusableProp']=True
 catalog[name]={'object':o.name,'size_cm':[round(v*100,3) for v in o.dimensions],'triangles':sum(len(f.vertices)-2 for f in o.data.polygons),'materials':[m.name for m in o.data.materials]};parts=[];return o
# One 2m parquet/dielen tile: ten narrow planks, staggered ends.
for i in range(10):
 y=-.9+i*.2
 for j in range(2):box((-.5+j,y,-.017),( .995,.195,.034),'Wood',.004)
end('FloorTile2m')
# Window bay centered on origin, complete actual aperture, wall depth 20cm.
# 120x120cm opening at sill100, top220, room wall300.
box((0,-.8,1.5),(.2,.4,3),'Plaster');box((0,.8,1.5),(.2,.4,3),'Plaster')
box((0,0,.5),(.2,1.2,1),'Plaster');box((0,0,2.6),(.2,1.2,.8),'Plaster')
for y in (-.65,.65):box((-.05,y,1.6),(.27,.10,1.30),'Wood')
for z in (.95,2.25):box((-.06,0,z),(.29,1.4,.1),'Wood')
box((-.11,0,1.60),(.065,.045,1.25),'Timber');box((-.11,0,1.60),(.065,1.25,.045),'Timber')
box((.095,0,1.60),(.025,1.19,1.19),'Window',.002);box((-.16,0,.94),(.42,1.5,.09),'Stone')
end('WindowWall2m')
# Thin stone footing panel, adds joints and irregular tone at room edge only.
box((0,0,.28),(.12,2,.56),'Mortar')
for row in range(3):
 for i in range(5):
  box((-.035,-.8+i*.4+( .08 if row%2 else 0),.095+row*.18),(.16,.38,.16),'Stone',.022)
end('StoneWainscot2m')
# Dressed reception: exact retained blocking footprint .8x3.4; split tops80/105.
for y in (-1.275,-.425,.425,1.275):
 height=.8 if y> .84 else 1.05
 box((0,y,height/2),(.78,.82,height-.07),'Wood',.018)
 box((0,y,height-.035),(.92,.87,.07),'Wood',.012)
 for dy in (-.34,.34):box((-.405,y+dy,height/2),(.08,.065,height-.09),'Timber')
 for z in (.10,height-.12):box((-.415,y,z),(.07,.78,.065),'Timber')
 for v in range(4):box((-.43,y-.25+v*.17,height*.47),(.016,.012,height*.57),'Gold',.003)
# central sage panel with leaf insignia, not final franchise insignia
box((-.447,-.42,.51),(.016,.64,.55),'Sage',.006)
beam((-.466,-.42,.30),(-.466,-.42,.71),.025,'Gold')
for v in range(3):
 for sign in (-1,1):beam((-.468,-.42,.35+v*.09),(-.468,-.42+sign*.16,.45+v*.09),.018,'Gold')
end('CounterStepped')
# Proper masonry fireplace: open firebox, soot back, recessed stone arch/jambs.
box((0,0,.045),(1.1,1.9,.09),'Stone',.028)
box((.37,0,1.2),(.18,1.48,2.30),'Stone',.035)
box((-.05,0,.21),(.80,1.2,.32),'Mortar',.022)
for side in (-1,1):
 for row in range(7):box((-.08,side*.66,.21+row*.20),(.69,.29,.18),'Stone',.035)
for i in range(7):box((-.10,-.66+i*.22,1.58),(.74,.205,.20),'Stone',.026)
box((.13,0,1.97),(.57,1.55,.62),'Stone',.035)
box((-.12,0,1.71),(.96,1.78,.12),'Wood',.014)
for i in range(3):
 cyl((-.17,-.33+i*.31,.30),.10,.63,'Timber',rotation=(math.pi/2,0,0))
 ellipsoid((-.14,-.30+i*.3,.46),(.13,.12,.24 if i!=1 else .34),'Fire')
for y in (-.50,0,.50):cyl((-.50,y,.30),.025,.43,'Metal')
end('Fireplace')
# Seating: real slatted bench + cushions;45cmseat.
for x in (-.48,.48):
 for y in (-.31,.31):box((x,y,.205),(.10,.10,.41),'Timber')
for i in range(4):box((0,-.27+i*.18,.42),(1.3,.17,.06),'Wood')
for x in (-.56,.56):box((x,.34,.72),(.085,.085,.92),'Timber')
for z in (.70,.89):box((0,.35,z),(1.3,.065,.17),'Wood')
for x in (-.32,.32):ellipsoid((x,0,.475),(.29,.29,.07),'Sage')
end('Bench')
#75cm tabletop,turnedleg proportions.
box((0,0,.715),(1.15,.70,.07),'Wood',.027)
for x in (-.43,.43):
 for y in (-.22,.22):
  cyl((x,y,.355),.065,.70,'Timber');ellipsoid((x,y,.34),(.085,.085,.11),'Wood')
beam((-.43,0,.19),(.43,0,.19),.06,'Wood');end('Table')
# hand-thrown ceramic, smooth lathe profiles, bottle and basket.
def lathe(profile,mat):
 verts=[];faces=[];N=20
 for z,r in profile:
  for i in range(N):verts.append((r*math.cos(i*2*math.pi/N),r*math.sin(i*2*math.pi/N),z))
 for j in range(len(profile)-1):
  for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
 mesh=bpy.data.meshes.new('ThrownProfile');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('ThrownProfile',mesh);s.collection.objects.link(o)
 for f in mesh.polygons:f.use_smooth=True
 return finish(o,mat)
lathe([(0,.001),(.01,.09),(.08,.15),(.22,.14),(.28,.08),(.32,.085),(.33,.071),(.29,.067),(.22,.11),(.04,.11),(.03,.001)],'Ceramic');end('CeramicJar')
lathe([(0,.001),(.01,.06),(.04,.08),(.19,.08),(.23,.035),(.29,.03),(.30,.04)],'Glass');cyl((0,0,.305),.035,.04,'Wood');end('Vial')
lathe([(0,.001),(.015,.14),(.04,.18),(.18,.23),(.20,.225)],'Wood')
for i in range(10):
 a=i*2*math.pi/10;beam((.145*math.cos(a),.145*math.sin(a),.015),(.23*math.cos(a),.23*math.sin(a),.20),.018,'Gold')
for z in (.05,.11,.18):
 bpy.ops.mesh.primitive_torus_add(major_radius=.15+z*.4,minor_radius=.008,major_segments=24,minor_segments=6,location=(0,0,z));finish(bpy.context.object,'Gold')
end('Basket')
# Plant is leafy geometry, with clear stems and flower cluster; not spheres.
lathe([(0,.001),(.01,.13),(.23,.19),(.26,.20),(.28,.20),(.28,.17),(.24,.16)],'Ceramic')
for i in range(7):
 a=i*2.4;rad=.15+.05*(i%2);tip=(rad*math.cos(a),rad*math.sin(a),.58+.08*(i%3))
 beam((0,0,.24),tip,.013,'Leaf')
 for t in (.45,.72):
  mid=Vector((0,0,.24)).lerp(Vector(tip),t)
  for sign in (-1,1):
   o=ellipsoid(mid+Vector((sign*.055,sign*.04,.025)),(.09,.028,.019),'LeafLight' if i%2 else 'Leaf');o.rotation_euler.z=a
 if i in (1,4,6):
  for j in range(5):ellipsoid(Vector(tip)+Vector((.036*math.cos(j*1.256),.036*math.sin(j*1.256),0)),(.028,.018,.014),'Flower')
end('HerbPot')
for i in range(11):
 a=i*2.4;tip=(.15*math.cos(a),.14*math.sin(a),.12+(i%3)*.08)
 beam((0,0,.65),tip,.012,'Leaf')
 for j in range(3):ellipsoid(Vector(tip)+Vector((j*.018,0,j*.07)),(.075,.022,.018),'LeafLight' if i%3==0 else 'Leaf')
cyl((0,0,.56),.03,.05,'Gold');end('DriedHerbs')
# cloth wall banner with scalloped bottom, stitched edges, organic leaf motif.
box((0,0,.60),(.026,1.05,1.20),'Sage',.009)
for y in (-.48,.48):box((-.018,y,.62),(.012,.018,1.10),'Gold',.002)
beam((-.025,0,.18),(-.025,0,.94),.022,'Gold')
for i in range(5):
 for sign in (-1,1):beam((-.027,0,.25+i*.12),(-.027,sign*(.15+(i%2)*.08),.36+i*.12),.028,'Gold')
cyl((0,0,1.26),.027,1.22,'Wood',(math.pi/2,0,0));end('Banner')
# woven rug with muted stitched rim and botanical geometry, floor contact.
box((0,0,.008),(2.25,1.6,.016),'Sage',.018)
for x in (-1.05,1.05):box((x,0,.019),(.025,1.48,.006),'Gold',.002)
for y in (-.73,.73):box((0,y,.019),(2.12,.025,.006),'Gold',.002)
for i in range(-4,5):
 beam((i*.19,-.58,.023),(i*.19+.12,-.47,.023),.017,'Linen');beam((i*.19,.58,.023),(i*.19+.12,.47,.023),.017,'Linen')
beam((-.55,0,.024),(.55,0,.024),.018,'Gold')
for i in range(5):
 for sign in (-1,1):beam((-.45+i*.21,0,.026),(-.35+i*.21,sign*.18,.026),.025,'Gold')
end('Rug')
# reusable carved post and brace unit.
box((0,0,1.5),(.17,.17,3),'Timber');box((0,0,.13),(.24,.24,.26),'Stone')
beam((0,0,2.1),(0,.58,2.69),.10);end('WallPost')
# Apothecary shelf accessory: organized labelled books/bottles, attach atop
# existing V3 shelf board. Furniture itself continues to use the V3 mesh.
for i in range(5):
 box((-.32+i*.14,0,.15),(.11,.18,.30+(.04 if i%2 else 0)),'Book' if i%2 else 'Ceramic',.008)
 box((-.32+i*.14,-.096,.18),(.075,.007,.065),'Paper',.002)
end('ShelfStock')
# Reusable small pillow for V3 bed material/softness dressing.
ellipsoid((0,0,.07),(.24,.32,.07),'Linen');end('Pillow')
# Store catalog and unpositioned assets in their own library collection.
lib=bpy.data.collections.new('Reusable Library');s.collection.children.link(lib)
for o in list(s.objects):
 if o.type=='MESH':
  for c in list(o.users_collection):c.objects.unlink(o)
  lib.objects.link(o);o.hide_render=True;o.hide_set(True)
(ART/'ExpandedArtV1/Props.json').write_text(json.dumps(catalog,indent=2))
# A separate illustrative staging scene, not export geometry.
preview=bpy.data.scenes.new('Prop Review');preview.unit_settings.system='METRIC';preview.unit_settings.scale_length=1
for i,(name,entry) in enumerate(catalog.items()):
 original=bpy.data.objects[entry['object']];o=original.copy();o.data=original.data;preview.collection.objects.link(o);o.hide_render=False;o.hide_set(False);o.location=((i%5)*4,(i//5)*4,0);o.name='Review_'+name
bpy.context.window.scene=preview
bpy.ops.object.light_add(type='AREA',location=(7,5,15));lamp=bpy.context.object;lamp.data.energy=2200;lamp.data.shape='DISK';lamp.data.size=12
bpy.ops.object.camera_add(location=(18,-19,25));camera=bpy.context.object;camera.rotation_euler=(Vector((8,6,0))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=25;preview.camera=camera
preview.world=bpy.data.worlds.new('Soft studio');preview.world.use_nodes=True;preview.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.20,.16,.11,1);preview.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.7
preview.render.engine='CYCLES';preview.cycles.samples=12;preview.render.resolution_x=1600;preview.render.resolution_y=1100;preview.render.resolution_percentage=100
preview.view_settings.view_transform='AgX'
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE));print('SOURCE_SAVED',SOURCE,'PROP_TRIANGLES',sum(v['triangles'] for v in catalog.values()))
