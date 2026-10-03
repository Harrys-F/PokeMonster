"""Create a standalone Westland kit. Read V3 as reference, never save V3.
Run in background Blender with HealingHouse_V3.blend loaded. Refuses overwrite.
"""
import bpy, bmesh, math, json, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'Art/Architecture/Westland'; REVIEW=ROOT/'Saved/WestlandKitV1'
SOURCE=ART/'Source/WestlandBuildingKit_V1.blend'
assert bpy.app.background and Path(bpy.data.filepath)==ROOT/'Art/HealingHouse/Source/HealingHouse_V3.blend'
assert not SOURCE.exists() or '--rebuild' in sys.argv, 'Preserve existing kit source; explicit --rebuild is required for this task-owned output.'
reference={'file':str(bpy.data.filepath),'objects':len(bpy.context.scene.objects),'materials':{},'independent_reconstruction':True}
for m in bpy.data.materials:
 if m.name.startswith('HH_V2_'):
  reference['materials'][m.name]={'color':list(m.diffuse_color),'nodes':len(m.node_tree.nodes) if m.node_tree else 0}
REVIEW.mkdir(parents=True,exist_ok=True)
(REVIEW/'HealingHouseReference.json').write_text(json.dumps(reference,indent=2)+'\n')
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.name='WestlandBuildingKit_V1'
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
library=bpy.data.collections.new('WL_ModuleLibrary');scene.collection.children.link(library)
proof=bpy.data.collections.new('WL_CottageProof');scene.collection.children.link(proof)
collision=bpy.data.collections.new('WL_CollisionSources');scene.collection.children.link(collision)
colors={'Plaster':(.73,.61,.43),'Wood':(.31,.17,.075),'Timber':(.13,.075,.035),'Stone':(.39,.40,.35),'Roof':(.48,.13,.065),'Metal':(.15,.16,.14),'Glass':(.95,.60,.19)}
mats={}
for n,c in colors.items():
 m=bpy.data.materials.new('WL_'+n);m.diffuse_color=(*c,1);m.use_nodes=True
 node=m.node_tree.nodes.get('Principled BSDF');node.inputs['Base Color'].default_value=(*c,1);node.inputs['Roughness'].default_value=.85
 mats[n]=m
parts=[];definition=[];modules={};colliders={}
def box(p,s,mat='Timber',bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.dimensions=s
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mats[mat])
 if bevel:
  mod=o.modifiers.new('Soft handworked edge','BEVEL');mod.width=bevel;mod.segments=1
  bpy.ops.object.modifier_apply(modifier=mod.name)
 parts.append(o);return o
def prism(points,depth,mat='Plaster'):
 # profile points are (Y,Z); X is the wall normal.
 n=len(points);vs=[(x,y,z) for x in (-depth/2,depth/2) for y,z in points]
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new('Profile');me.from_pydata(vs,[],fs);me.update()
 o=bpy.data.objects.new('Profile',me);scene.collection.objects.link(o);o.data.materials.append(mats[mat]);parts.append(o);return o
def beam(a,b,width=.12,mat='Timber'):
 a,b=Vector(a),Vector(b);o=box((a+b)/2,(width,width,(b-a).length),mat,.007)
 o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();bpy.context.view_layer.objects.active=o
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return o
def arch(w,sill,spring):
 return [(-w/2,sill),(w/2,sill)]+[(math.cos(i*math.pi/16)*w/2,spring+math.sin(i*math.pi/16)*w/2) for i in range(17)]
def cut(wall,cutter):
 mod=wall.modifiers.new('Real opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.context.view_layer.objects.active=wall;bpy.ops.object.modifier_apply(modifier=mod.name)
 parts.remove(cutter);bpy.data.objects.remove(cutter,do_unlink=True)
def finish(name,category,boxes=(),notes=''):
 global parts
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0]
 if len(parts)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='SM_WL_'+name
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 # Authoring -Y is Unreal +Y. Explicit handedness conversion preserves pivots.
 for v in o.data.vertices:v.co.y*=-1
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.normal_update();bm.to_mesh(o.data);bm.free();o.data.update()
 for c in list(o.users_collection):c.objects.unlink(o)
 library.objects.link(o)
 o['module_category']=category;o['axis_contract']='Blender +X inward, -Y along bay, +Z up; Unreal +X/+Y/+Z'
 modules[name]=o;parts=[];colliders[name]=[]
 for i,(p,s) in enumerate(boxes):
  co=box((p[0],-p[1],p[2]),s,'Stone');parts=[]
  co.name='UCX_'+o.name+'_'+str(i).zfill(2)
  for c in list(co.users_collection):c.objects.unlink(co)
  collision.objects.link(co);colliders[name].append(co)
 o.data.calc_loop_triangles();vs=[(v.co.x,-v.co.y,v.co.z) for v in o.data.vertices]
 definition.append({'name':name,'mesh':o.name,'category':category,'min_m':[min(v[i] for v in vs) for i in range(3)],'max_m':[max(v[i] for v in vs) for i in range(3)],'triangles':len(o.data.loop_triangles),'materials':[m.name for m in o.data.materials],'collision_boxes':[{'center_m':p,'size_m':s} for p,s in boxes],'notes':notes})
 return o
for width in (1,2):
 box((0,width/2,1.5),(.2,width,3),'Plaster')
 finish('WallSolid'+str(width)+'m','Walls',[((0,width/2,1.5),(.2,width,3))],'Origin at lower bay start, width along +Y in Unreal.')
for kind in ('Arch','Double'):
 wall=box((0,1,1.5),(.2,2,3),'Plaster')
 if kind=='Arch':
  cutter=prism([(y+1,z) for y,z in arch(1,1,1.6)],.6);cut(wall,cutter)
 else:cut(wall,box((0,1,1.55),(.6,1.1,1.1),'Plaster'))
 # Bottom sill wall prevents the player stepping into window openings.
 boxes=[((0,1,.5),(.2,2,1)),((0,1,2.6),(.2,2,.8)),((0,.2,1.55),(.2,.4,1.1)),((0,1.8,1.55),(.2,.4,1.1))]
 finish('WallWindow'+kind+'2m','Walls',boxes,'Applied Exact Boolean, sill 1m; compatible window module centered Y=1m.')
wall=box((0,1,1.5),(.2,2,3),'Plaster');cut(wall,box((0,1,.999),(.6,1.3,2.002),'Plaster'))
finish('WallDoor2m','Walls',[((0,.175,1.5),(.2,.35,3)),((0,1.825,1.5),(.2,.35,3)),((0,1,2.5),(.2,1.3,1))],'Clear opening Y=.35..1.65, Z=0..2m; separate side/lintel collision.')
prism([(0,0),(3,0),(3,2)],.2);finish('GableHalf3m','Walls',notes='One half of a 6m gable; repeat mirrored by 180-degree yaw, no scaling.')
for n,size in [('CornerPost3m',(.18,.18,3)),('VerticalPost3m',(.12,.12,3))]:
 box((0,0,1.5),size,'Timber',.01);finish(n,'Timber')
box((0,1,0),(.16,2,.16),'Timber',.01);finish('HorizontalBeam2m','Timber')
beam((0,0,0),(0,1,1));finish('DiagonalBrace1m','Timber')
box((0,.5,.18),(.25,1,.36),'Stone',.012);finish('StonePlinth1m','Structural')
# Repeated roof strips: a 2:3 pitch. Ridge origin makes eaves/trim independent.
for name,length in [('RoofPanel1m',1),('RoofPanelEnd30cm',.3)]:
 vs=[(x,y,z) for x in (0,length) for y,z in ((0,0),(3.3,-2.2),(3.3,-2.28),(0,-.08))]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mats['Roof']);parts.append(o)
 # Restrained staggered shingle rhythm; regular geometry meets exactly at seams.
 for row in range(8):
  y=.18+row*.41
  cols=3 if length==1 else 1
  for col in range(cols):
   x=(col+.5)*length/cols
   tile=box((x,y,-y*2/3+.028),(length/cols-.016,.49,.045),'Roof',.008)
   tile.rotation_euler.x=-math.atan(2/3);bpy.context.view_layer.objects.active=tile;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 finish(name,'Roof',notes='Ridge origin; local +Y descends 2:3, strip length along +X. Opposite slope uses yaw 180.')
box((.5,0,0),(1,.14,.16),'Timber',.009);finish('EaveTrim1m','Roof')
beam((0,0,0),(0,3.3,-2.2),.14);finish('GableTrimHalf3m','Roof')
box((.5,0,.02),(1,.24,.13),'Timber',.018);finish('RidgeCap1m','Roof')
for y in (-.715,.715):box((-.14,y,1.035),(.16,.13,2.07),'Wood',.008)
box((-.14,0,2.065),(.16,1.56,.13),'Wood',.008);finish('DoorFrame130x200','Doors',notes='Origin at opening center / floor. Free opening 130x200cm.')
for i in range(7):box((0,(i+.5)*1.28/7,.975),(.055,1.28/7-.012,1.95),'Wood',.007)
for z in (.32,1.62):box((-.04,.64,z),(.035,1.26,.075),'Metal',.004)
box((-.055,1.10,.95),(.055,.055,.15),'Metal',.008);finish('DoorLeaf130x200','Doors',notes='Floor / hinge pivot, width along +Y; test placement opens outwards 90 degrees.')
for kind in ('Arch','Double','Round'):
 if kind=='Arch':
  profile=arch(1,0,.6);glass=prism(profile,.04,'Glass')
  for a,b in zip(profile[2:],profile[3:]):beam((-.14,*a),(-.14,*b),.085,'Wood')
  for y in (-.54,.54):box((-.14,y,.32),(.12,.085,.64),'Wood',.006)
  box((-.14,0,0),(.18,1.14,.085),'Wood',.006)
  box((-.16,0,.35),(.10,.065,.7),'Wood',.005)
 elif kind=='Double':
  box((0,0,.55),(.04,1.1,1.1),'Glass')
  for y in (-.6,0,.6):box((-.14,y,.55),(.14,.07,1.25),'Wood',.006)
  for z in (0,1.1):box((-.14,0,z),(.18,1.27,.08),'Wood',.006)
  box((-.14,0,.55),(.14,1.2,.06),'Wood',.005)
 else:
  points=[(.35*math.cos(i*2*math.pi/24),.35+.35*math.sin(i*2*math.pi/24)) for i in range(24)]
  prism(points,.04,'Glass')
  for i,a in enumerate(points):
   b=points[(i+1)%len(points)];beam((-.14,*a),(-.14,*b),.075,'Wood')
  box((-.14,0,.35),(.09,.065,.7),'Wood',.005);box((-.14,0,.35),(.09,.7,.065),'Wood',.005)
 finish('Window'+kind,'Windows',notes='Floor-relative origin at lower sill / horizontal opening center; decorative module is NoCollision.')
box((0,0,.83),(.6,.6,1.66),'Stone',.015)
for z in (.28,.62,.96,1.3):box((0,0,z),(.63,.63,.065),'Stone',.008)
box((0,0,1.72),(.76,.76,.12),'Stone',.015);finish('Chimney60cm','Structural')
# Small private rain hood, with no sign and no public veranda.
for y in (-.85,.85):beam((-.03,y,1.7),(-.8,y,2.15),.085)
box((-.48,0,2.2),(1.10,1.85,.10),'Roof',.015)
box((-.98,0,2.14),(.12,1.95,.14),'Timber',.01);finish('Porch160cm','Structural')
box((.5,.5,-.08),(1,1,.16),'Wood');finish('Floor1m','Structural',[((.5,.5,-.08),(1,1,.16))],'Origin at top corner; 1m XY tile, top exactly Z=0.')
box((-.15,0,-.035),(.3,1.3,.07),'Stone');finish('Threshold130cm','Structural',[((-.15,0,-.035),(.3,1.3,.07))])
placements=[]
def place(module,p,yaw=0,fade=False):
 p=list(p)
 if module=='CornerPost3m':
  p[0]+=math.copysign(.06,p[0]);p[1]+=math.copysign(.06,p[1])
 elif module in ('VerticalPost3m','HorizontalBeam2m','DiagonalBrace1m'):
  if abs(p[0])==3:p[0]+=math.copysign(.14,p[0])
  elif abs(p[1])==3:p[1]+=math.copysign(.14,p[1])
 o=bpy.data.objects.new('Cottage_'+module+'_'+str(len(placements)).zfill(3),modules[module].data);proof.objects.link(o)
 o.location=(p[0],-p[1],p[2]);o.rotation_euler.z=-math.radians(yaw)
 placements.append({'label':o.name,'module':module,'position_m':p,'yaw':yaw,'cutaway':fade})
for x in range(-3,3):
 for y in range(-3,3):place('Floor1m',(x,y,0))
for front in (True,False):
 x=-3 if front else 3;yaw=0 if front else 180
 for y in (-3,-1,1):
  module=('WallDoor2m' if y==-1 else 'WallWindowArch2m') if front else 'WallSolid2m'
  place(module,(x,y if front else -y,0),yaw,front)
  place('HorizontalBeam2m',(x,y if front else -y,3),yaw,front)
 for sign in (-1,1):
  place('GableHalf3m',(x,sign*3,3),0 if sign==-1 else 180,front)
  place('GableTrimHalf3m',(x-.08 if front else x+.08,0,5),0 if sign==1 else 180,front)
for side in (-1,1):
 y=side*3;yaw=-90 if side==1 else 90
 for x in (-3,-1,1):
  module='WallWindowDouble2m' if side==-1 and x==-1 else 'WallSolid2m'
  start=-x if side==-1 else x
  place(module,(start,y,0),yaw,side==-1)
  place('HorizontalBeam2m',(start,y,3),yaw,side==-1)
 for x in range(-3,3):
  place('StonePlinth1m',(-x if side==-1 else x,y,0),yaw,side==-1)
for x in (-3,3):
 for y in (-3,3):place('CornerPost3m',(x,y,0),fade=x==-3 or y==-3)
for x in (-3,3):
 for y in (-1,1):place('VerticalPost3m',(x,y,0),fade=x==-3)
for y in (-3,3):
 for x in (-1,1):place('VerticalPost3m',(x,y,0),fade=y==-3)
for y in (-3,3):
 for x in (-2,1):place('DiagonalBrace1m',(x,y,1.75),90,fade=y==-3)
for y in (-3,-2,1,2):place('StonePlinth1m',(-3,y,0),fade=True)
for y in range(-3,3):place('StonePlinth1m',(3,-y,0),180)
for side in (-1,1):
 for x in range(-3,3):
  place('RoofPanel1m',(x if side==1 else -x,0,5),0 if side==1 else 180,True)
  place('EaveTrim1m',(x,side*3.3,2.8),fade=True)
 for x in (-3.3,3):place('RoofPanelEnd30cm',(x if side==1 else -x,0,5),0 if side==1 else 180,True)
for x in range(-3,3):place('RidgeCap1m',(x,0,5),fade=True)
place('DoorFrame130x200',(-3,0,0),fade=True)
place('DoorLeaf130x200',(-3.22,-.65,0),90,True)
for y in (-2,2):place('WindowArch',(-3,y,1),fade=True)
place('WindowDouble',(0,-3,1),90,True)
place('Porch160cm',(-3,0,0),fade=True)
place('Threshold130cm',(-3,0,0))
place('Chimney60cm',(1.7,1.65,3.9),fade=True)
counts={n:sum(p['module']==n for p in placements) for n in modules}
for col in (library,collision):col.hide_viewport=True;col.hide_render=True
scene.world=bpy.data.worlds.new('WestlandWorld');scene.world.color=(.35,.4,.45)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
metadata={'schema':'PokeMonster.WestlandKit.v1','units':'metres','blender_axis':'X inward, -Y bay direction, Z up','unreal_axis':'X inward, Y bay direction, Z up','grid_m':1,'wall_bay_m':2,'wall_height_m':3,'wall_thickness_m':.2,'roof_pitch':'2:3','modules':definition,'materials':list(colors),'no_external_links':True}
(ART/'WestlandBuildingKit_V1.json').write_text(json.dumps(metadata,indent=2)+'\n')
(ART/'Buildings/WL_Cottage_V1.json').write_text(json.dumps({'schema':'PokeMonster.WestlandBuilding.v1','building':'WL_Cottage_V1','body_m':[6,6,3],'ridge_m':5,'door_m':[1.3,2],'placements':placements,'module_counts':counts,'unique_building_only_meshes':[],'interior_clear_m':[5.8,5.8],'intentional_asymmetry':['One side window','Small chimney offset to the rear'],'opening_exception':'Private home door 1.3m is deliberately smaller than public V3 door 1.5m; capsule width .56m.'},indent=2)+'\n')
print('WESTLAND_SOURCE_SAVED',SOURCE,'modules',len(modules),'placements',len(placements))
