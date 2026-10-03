"""Recompose the existing Inn source from its unchanged 33-module library.
Run background Blender with WestlandInn_V1.blend; saves only that owned source/layout.
No new meshes, materials or FBX exports. Original bootstrap builder remains historical.
"""
import bpy,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/Architecture/Westland';OUT=ROOT/'Saved/WestlandInnCamera';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ART/'Source/WestlandInn_V1.blend'
assert bpy.app.background and Path(bpy.data.filepath)==SOURCE
kit=json.loads((ART/'WestlandBuildingKit_V1.json').read_text());ext=json.loads((ART/'WestlandBuildingKit_InnExtensions_V1.json').read_text());definitions=kit['modules']+ext['modules']
modules={m['name']:bpy.data.objects[m['mesh']] for m in definitions}
def digest(o):return hashlib.sha256(json.dumps({'vertices':[list(v.co) for v in o.data.vertices],'faces':[list(f.vertices) for f in o.data.polygons],'materials':[m.name for m in o.data.materials]},sort_keys=True).encode()).hexdigest()
before={n:digest(o) for n,o in modules.items()}
proof=bpy.data.collections['WL_InnProof']
for o in list(proof.objects):bpy.data.objects.remove(o,do_unlink=True)
placements=[]
def place(module,p,yaw=0,fade=False,role='Architecture'):
 label='Inn_'+module+'_'+str(len(placements)).zfill(3)
 o=bpy.data.objects.new(label,modules[module].data);proof.objects.link(o);o.location=(p[0],-p[1],p[2]);o.rotation_euler.z=-math.radians(yaw)
 if role=='HearthReserve':
  for slot in o.material_slots:slot.link='OBJECT';slot.material=bpy.data.materials['WL_Stone']
 placements.append({'label':label,'module':module,'position_m':list(p),'yaw':yaw,'cutaway':fade,'role':role,'existing':True})
# 48 m2 hall and 12 m2 lower rear wing. No floor in the exterior L-notch.
for x in range(-3,3):
 for y in range(-4,4):place('Floor1m',(x,y,0),role='MainHallFloor')
for x in range(3,5):
 for y in range(-2,4):place('Floor1m',(x,y,0),role='WingFloor')
def wall(p,yaw,module,fade=False,role='Wall'):
 x,y=p;a=math.radians(yaw);nx=-math.cos(a);ny=-math.sin(a)
 place(module,(x,y,0),yaw,fade,role)
 place('HorizontalBeam2m',(x+nx*.14,y+ny*.14,3),yaw,fade,'FacadeTimber')
 place('VerticalPost3m',(x+nx*.14,y+ny*.14,0),yaw,fade,'FacadeTimber')
 if 'Window' in module:
  place('WindowArch' if 'Arch' in module else 'WindowDouble',(x-math.sin(a),y+math.cos(a),1),yaw,fade,'Window')
 # Plinth excludes the genuine doorway aperture.
 if 'Door' not in module:
  for t in (0,1):place('StonePlinth1m',(x-math.sin(a)*t,y+math.cos(a)*t,0),yaw,fade,'Plinth')
 elif 'Door' in module:
  # Only the upper lintel; no timber or plinth across the passage.
  pass
# +Y spans along each local wall module; normal points inward.
for y,m in [(-4,'WallWindowArch2m'),(-2,'WallDoor160x2152m'),(0,'WallWindowDouble2m'),(2,'WallWindowDouble2m')]:wall((-3,y),0,m,True,'FrontWall')
wall((3,-2),180,'WallWindowArch2m',False,'MainRearWall')
for y,m in [(-2,'WallWindowDouble2m'),(0,'WallSolid2m'),(2,'WallWindowArch2m')]:wall((5,y+2),180,m,False,'WingRearWall')
for x,m in [(-3,'WallSolid2m'),(-1,'WallWindowArch2m'),(1,'WallSolid2m')]:wall((x+2,-4),90,m,False,'LeftWall')
for x,m in [(-3,'WallWindowDouble2m'),(-1,'WallSolid2m'),(1,'WallWindowArch2m'),(3,'WallSolid2m')]:wall((x,4),-90,m,False,'RightWall')
wall((5,-2),90,'WallWindowArch2m',False,'WingNotchWall')
for x,y in [(-3,-4),(-3,4),(5,4),(5,-2),(3,-2),(3,-4)]:place('CornerPost3m',(x,y,0),fade=x==-3,role='Corner')
for x,y,yaw in [(-2,4,-90),(0,-4,90),(4,-2,90)]:place('DiagonalBrace1m',(x,y,1.75),yaw,role='FacadeTimber')
# Main ridge along +X, plus parallel offset/lower 6m wing ridge.
for end in (-3,3):
 for sign in (-1,1):
  place('GableHalf4m',(end,sign*4,3),0 if sign==-1 else 180,True,'FrontGable' if end==-3 else 'JunctionUpperGable')
  place('GableTrimHalf4m',(end+(-.08 if end==-3 else .08),0,3+8/3),0 if sign==1 else 180,True,'RoofTrim')
for sign in (-1,1):
 place('GableHalf3m',(5,1+sign*3,3),0 if sign==-1 else 180,False,'WingRearGable')
 place('GableTrimHalf3m',(5.08,1,5),0 if sign==1 else 180,True,'RoofTrim')
for side in (-1,1):
 yaw=0 if side==1 else 180
 for x in range(-3,3):
  place('RoofPanel8mSpan1m',(x if side==1 else x+1,0,3+8/3),yaw,True,'MainRoof')
  place('EaveTrim1m',(x,side*4.3,2.8),0,True,'RoofTrim')
 for x in (-3.3,3):
  if not (side==1 and x==3):place('RoofPanel8mSpanEnd30cm',(x if side==1 else x+.3,0,3+8/3),yaw,True,'MainRoof')
 # Wing strips begin at the junction; no coplanar end caps underneath the main roof.
 for x in (3,4):place('RoofPanel1m',(x if side==1 else x+1,1,5),yaw,True,'WingRoof')
 place('RoofPanelEnd30cm',(5 if side==1 else 5.3,1,5),yaw,True,'WingRoof')
 for x in (3,4):place('EaveTrim1m',(x,1+side*3.3,2.8),0,True,'RoofTrim')
for x in range(-3,3):place('RidgeCap1m',(x,0,3+8/3),0,True,'MainRoof')
for x in (3,4):place('RidgeCap1m',(x,1,5),0,True,'WingRoof')
place('DoorFrame160x215',(-3,-1,0),fade=True,role='Entrance')
place('DoorLeaf160x215',(-3.22,-1.8,0),90,True,'Entrance')
place('Threshold160cm',(-3,-1,0),role='Entrance')
place('Porch160cm',(-3,-1,.30),fade=True,role='Entrance')
place('Chimney60cm',(4,1.4,4.3),fade=True,role='Chimney')
for y in (1,2):place('Floor1m',(4,y,.004),role='HearthReserve')
proxies=[{'label':'Inn_CounterBase','position_m':[1.4,-2.3,.42],'size_m':[.65,2.6,.84],'material':'Wood','collision':True},{'label':'Inn_CounterTop','position_m':[1.4,-2.3,.90],'size_m':[.86,2.7,.12],'material':'Wood','collision':True}]
for item in proxies:
 bpy.ops.mesh.primitive_cube_add(size=1,location=(item['position_m'][0],-item['position_m'][1],item['position_m'][2]));o=bpy.context.object;o.name=item['label'];o.dimensions=item['size_m'];bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(bpy.data.materials['WL_Wood'])
 for c in list(o.users_collection):c.objects.unlink(o)
 proof.objects.link(o)
assert all(digest(o)==before[n] for n,o in modules.items())
counts={n:sum(p['module']==n for p in placements) for n in modules}
layout={'schema':'PokeMonster.WestlandBuilding.v1','building':'WL_Inn_V1','body_m':[8,8,3],'main_hall_m':[6,8,3],'rear_wing_m':[2,6,3],'ridge_m':3+8/3,'wing_ridge_m':5,'door_m':[1.6,2.15],'map_origin_cm':[0,-1500,0],'door_center_local_m':[-3,-1,1.075],'placements':placements,'primitive_proxies':proxies,'module_counts':counts,'new_modules':[],'unique_building_only_meshes':[],'interior_clear_m':[5.8,7.8],'interior_camera':{'distance_cm':2200,'pitch':-50,'yaw_offset':0,'focus_local_m':[1,0,.8]},'interior_regions_cm':[{'center':[-100,0,0],'extent':[310,410,200]},{'center':[300,100,0],'extent':[110,310,200]}],'intentional_asymmetry':['Rectangular hall plus offset lower rear wing','Offset public entrance','Parallel roofs of 8m and 6m span','Rear-wing chimney'],'interior_zones':{'Entrance':[-3,-1],'MainHall':[0,0],'CounterReserve':[1.4,-2.3],'FutureSeating':[0,1.5],'HearthReserve':[4,2],'RearWing':[4,0]},'opening_exception':'Public 1.60 x 2.15 m per user brief; 56cm capsule leaves 52cm clearance per side.'}
layout['future_sign_reserve']={'center_local_m':[-3.22,-1,2.60],'size_m':[1.0,.10,.45],'note':'Free lintel area above the public entrance; no sign/decor added.'}
(ART/'Buildings/WL_Inn_V1.json').write_text(json.dumps(layout,indent=2)+'\n')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
(OUT/'SourceRecomposition.json').write_text(json.dumps({'modules_unchanged':before,'placements':len(placements),'reused':len(placements),'new_modules':0,'source':str(SOURCE)},indent=2)+'\n')
print('INN_RECOMPOSED',len(placements),'100% existing modules')
