"""Compose an independent inn proof from untouched kit meshes plus reusable variants.
Background Blender must load WestlandBuildingKit_V1.blend. Never saves that file.
"""
import bpy,bmesh,math,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/Architecture/Westland';OUT=ROOT/'Saved/WestlandInnV1'
SOURCE=ART/'Source/WestlandInn_V1.blend'
assert bpy.app.background and Path(bpy.data.filepath)==ART/'Source/WestlandBuildingKit_V1.blend'
assert not SOURCE.exists() or '--rebuild' in sys.argv
OUT.mkdir(parents=True,exist_ok=True)
kit=json.loads((ART/'WestlandBuildingKit_V1.json').read_text());scene=bpy.context.scene
scene.name='WestlandInn_V1'
oldmodules={m['name']:bpy.data.objects[m['mesh']] for m in kit['modules']}
def digest(o):
 return hashlib.sha256(json.dumps({'vertices':[list(v.co) for v in o.data.vertices],'faces':[list(f.vertices) for f in o.data.polygons],'materials':[m.name for m in o.data.materials]},sort_keys=True).encode()).hexdigest()
oldhashes={n:digest(o) for n,o in oldmodules.items()}
(OUT/'OriginalKitAudit.json').write_text(json.dumps({'source':str(bpy.data.filepath),'module_hashes':oldhashes,'module_count':len(oldmodules)},indent=2)+'\n')
bpy.data.collections['WL_CottageProof'].hide_render=True;bpy.data.collections['WL_CottageProof'].hide_viewport=True
library=bpy.data.collections.new('WL_InnExtensionLibrary');scene.collection.children.link(library)
collision=bpy.data.collections.new('WL_InnExtensionCollision');scene.collection.children.link(collision)
proof=bpy.data.collections.new('WL_InnProof');scene.collection.children.link(proof)
mats={n:bpy.data.materials['WL_'+n] for n in kit['materials']}
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

# Public door is a reusable size variant; exact opening, with three separate bodies.
wall=box((0,1,1.5),(.2,2,3),'Plaster')
cut(wall,box((0,1,1.074),(.6,1.6,2.152),'Plaster'))
finish('WallDoor160x2152m','Walls',[((0,.1,1.5),(.2,.2,3)),((0,1.9,1.5),(.2,.2,3)),((0,1,2.575),(.2,1.6,.85))],'Public clear passage 160x215cm, compatible 2m bay. Separate jamb/lintel collision.')
for y in (-.865,.865):box((-.14,y,1.11),(.16,.13,2.22),'Wood',.008)
box((-.14,0,2.215),(.16,1.86,.13),'Wood',.008)
finish('DoorFrame160x215','Doors',notes='Foot / aperture-center origin; free width 1.60m, height 2.15m.')
for i in range(9):box((0,(i+.5)*1.58/9,1.05),(.055,1.58/9-.012,2.1),'Wood',.007)
for z in (.35,1.76):box((-.04,.79,z),(.035,1.56,.075),'Metal',.004)
box((-.055,1.38,1),(.055,.055,.15),'Metal',.008)
finish('DoorLeaf160x215','Doors',notes='Foot / hinge origin; 158x210cm leaf for public door, opens outwards.')
box((-.15,0,-.035),(.3,1.6,.07),'Stone')
finish('Threshold160cm','Structural',[((-.15,0,-.035),(.3,1.6,.07))])
# Same 2:3 roof pitch; true 8m span variants instead of distorting old roofs.
prism([(0,0),(4,0),(4,8/3)],.2)
finish('GableHalf4m','Walls',notes='One half of an 8m gable, base 4m, rise 8/3m. No global scaling.')
for name,length in [('RoofPanel8mSpan1m',1),('RoofPanel8mSpanEnd30cm',.3)]:
 vs=[(x,y,z) for x in (0,length) for y,z in ((0,0),(4.3,-4.3*2/3),(4.3,-4.3*2/3-.08),(0,-.08))]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mats['Roof']);parts.append(o)
 for row in range(11):
  y=.18+row*.39
  cols=3 if length==1 else 1
  for col in range(cols):
   tile=box(((col+.5)*length/cols,y,-y*2/3+.028),(length/cols-.016,.47,.045),'Roof',.008)
   tile.rotation_euler.x=-math.atan(2/3);bpy.context.view_layer.objects.active=tile;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 finish(name,'Roof',notes='8m roof-span variant, ridge anchor; standard 1m/30cm length, same 2:3 pitch and shingle language.')
beam((0,0,0),(0,4.3,-4.3*2/3),.14)
finish('GableTrimHalf4m','Roof',notes='8m-span half-gable bargeboard, same mounting/pitch contract.')
newdefinition=list(definition);newnames=list(modules)
modules.update(oldmodules)
placements=[]
def place(module,p,yaw=0,fade=False,role='Architecture'):
 p=list(p)
 if module=='CornerPost3m':p[0]+=math.copysign(.06,p[0]);p[1]+=math.copysign(.06,p[1])
 elif module in ('VerticalPost3m','HorizontalBeam2m','DiagonalBrace1m') and role=='Architecture':
  if abs(p[0])==4:p[0]+=math.copysign(.14,p[0])
  elif abs(p[1])==4:p[1]+=math.copysign(.14,p[1])
 label='Inn_'+module+'_'+str(len(placements)).zfill(3)
 o=bpy.data.objects.new(label,modules[module].data);proof.objects.link(o)
 o.location=(p[0],-p[1],p[2]);o.rotation_euler.z=-math.radians(yaw)
 if role=='HearthReserve':
  for slot in o.material_slots:slot.link='OBJECT';slot.material=mats['Stone']
 placements.append({'label':label,'module':module,'position_m':p,'yaw':yaw,'cutaway':fade,'role':role,'existing':module not in newnames})
for x in range(-4,4):
 for y in range(-4,4):place('Floor1m',(x,y,0))
# Eave-facing public front, offset entrance; ridge is perpendicular to cottage ridge.
for front in (True,False):
 x=-4 if front else 4;yaw=0 if front else 180
 for y in (-4,-2,0,2):
  if front:module={-4:'WallWindowArch2m',-2:'WallDoor160x2152m',0:'WallWindowDouble2m',2:'WallWindowDouble2m'}[y]
  else:module='WallWindowDouble2m' if y in (-2,2) else 'WallSolid2m'
  place(module,(x,y if front else -y,0),yaw,front)
  place('HorizontalBeam2m',(x,y if front else -y,3),yaw,front)
  if 'Window' in module:place('WindowArch' if 'Arch' in module else 'WindowDouble',(x,y+1 if front else -y-1,1),yaw,front)
for side in (-1,1):
 y=side*4;yaw=90 if side==-1 else -90
 for x in (-4,-2,0,2):
  module='WallWindowArch2m' if x in (-2,2) else 'WallSolid2m'
  start=-x if side==-1 else x
  place(module,(start,y,0),yaw,side==1)
  place('HorizontalBeam2m',(start,y,3),yaw,side==1)
  if 'Window' in module:place('WindowArch',(-x-1 if side==-1 else x+1,y,1),yaw,side==1)
 # Gables only on side ends, unlike the cottage's front gable.
 for sign in (-1,1):
  place('GableHalf4m',(-4 if sign==-1 else 4,y,3),-90 if sign==-1 else 90,side==1)
  place('GableTrimHalf4m',(0,y+side*.08,3+8/3),90 if sign==-1 else -90,side==1)
for x in (-4,4):
 for y in (-4,4):place('CornerPost3m',(x,y,0),fade=x==-4 or y==4)
for x in (-4,4):
 for y in (-2,0,2):place('VerticalPost3m',(x,y,0),fade=x==-4)
for y in (-4,4):
 for x in (-2,0,2):place('VerticalPost3m',(x,y,0),fade=y==4)
for y in (-4,4):
 for x in (-3,1):place('DiagonalBrace1m',(x,y,1.75),90,fade=y==4)
for side in (-1,1):
 for i in range(-4,4):
  place('StonePlinth1m',(-i if side==-1 else i,side*4,0),90 if side==-1 else -90,side==1)
  if side==1 or i not in (-2,-1):place('StonePlinth1m',(side*4,i if side==-1 else -i,0),0 if side==-1 else 180,side==-1)
# Ridge along +Y, roof descends across X, broad horizontal front silhouette.
for side in (-1,1):
 for y in range(-4,4):
  place('RoofPanel8mSpan1m',(0,y if side==-1 else -y,3+8/3),90 if side==-1 else -90,True)
  place('EaveTrim1m',(side*4.3,y,2.8),90,True)
 for y in (-4.3,4):place('RoofPanel8mSpanEnd30cm',(0,y if side==-1 else -y,3+8/3),90 if side==-1 else -90,True)
for y in range(-4,4):place('RidgeCap1m',(0,y,3+8/3),90,True)
place('DoorFrame160x215',(-4,-1,0),fade=True)
place('DoorLeaf160x215',(-4.22,-1.8,0),90,True)
place('Threshold160cm',(-4,-1,0))
place('Porch160cm',(-4,-1,.30),fade=True)
place('Chimney60cm',(2,2,4.3),fade=True)
# Reserve readable interior zones with a restrained low rail (existing beams),
# and existing stone floor modules as hearth pad; no new furnishing system.
for y in (-1,1):place('HorizontalBeam2m',(2.22,y,.88),0,False,'CounterReserve')
for x in (2,3):
 for y in (-4,-3):place('Floor1m',(x,y,.004),role='HearthReserve')
# Two simple cube proxies mark the counter, not exported bespoke architecture.
proxies=[{'label':'Inn_CounterBase','position_m':[2.55,1,.42],'size_m':[.65,4,.84],'material':'Wood','collision':True},{'label':'Inn_CounterTop','position_m':[2.55,1,.90],'size_m':[.86,4.1,.12],'material':'Wood','collision':True}]
for item in proxies:
 o=box((item['position_m'][0],-item['position_m'][1],item['position_m'][2]),item['size_m'],item['material']);parts=[];o.name=item['label']
 for col in list(o.users_collection):col.objects.unlink(o)
 proof.objects.link(o)
counts={n:sum(p['module']==n for p in placements) for n in modules}
assert all(digest(o)==oldhashes[n] for n,o in oldmodules.items())
for col in (library,collision):col.hide_viewport=True;col.hide_render=True
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
(ART/'WestlandBuildingKit_InnExtensions_V1.json').write_text(json.dumps({'schema':'PokeMonster.WestlandKitExtension.v1','base':'WestlandBuildingKit_V1.json','units':'metres','materials':kit['materials'],'modules':newdefinition,'reason':'Public 160x215 door and 8m roof span cannot be obtained by repeating the existing 130x200 door / 6m span without distortion. All variants remain generic.'},indent=2)+'\n')
layout={'schema':'PokeMonster.WestlandBuilding.v1','building':'WL_Inn_V1','body_m':[8,8,3],'ridge_m':3+8/3,'door_m':[1.6,2.15],'map_origin_cm':[0,-1500,0],'door_center_local_m':[-4,-1,1.075],'placements':placements,'primitive_proxies':proxies,'module_counts':counts,'new_modules':newnames,'unique_building_only_meshes':[],'interior_clear_m':[7.8,7.8],'intentional_asymmetry':['Offset public entrance','Eave-facing front and rotated ridge versus cottage','Rear-right chimney','Back-right counter reserve and back-left hearth reserve'],'interior_zones':{'Entrance':[-4,-1],'MainHall':[-1,0],'CounterReserve':[2.4,2],'FutureSeating':[0,1],'HearthReserve':[3,-3]},'opening_exception':'Public door 1.6m per user brief; .56m capsule leaves .52m each side.'}
(ART/'Buildings/WL_Inn_V1.json').write_text(json.dumps(layout,indent=2)+'\n')
print('WESTLAND_INN_SOURCE_SAVED',SOURCE,'newmodules',len(newdefinition),'placements',len(placements),'existing',sum(p['existing'] for p in placements))
