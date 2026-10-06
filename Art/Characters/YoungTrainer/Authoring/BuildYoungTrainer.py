"""Authored Young Trainer reference model; run phase by phase in Blender.
No existing scene/object is modified. Metres, +Z up, -Y semantic front.
"""
import bpy, math, random, json
from mathutils import Vector
from pathlib import Path
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
REVIEW=ROOT.parents[2]/'Saved/YoungTrainerV1'
REVIEW.mkdir(parents=True,exist_ok=True)
random.seed(71)
PARTS=[]
COLORS={
 'Skin':(.66,.37,.20,1),'SkinWarm':(.55,.23,.13,1),'Hair':(.045,.019,.009,1),'HairLight':(.095,.041,.018,1),
 'Cream':(.64,.53,.36,1),'Red':(.34,.034,.025,1),'RedLight':(.47,.073,.035,1),
 'Blue':(.032,.095,.155,1),'Olive':(.125,.15,.055,1),'OliveLight':(.19,.21,.09,1),
 'Leather':(.16,.066,.027,1),'LeatherLight':(.255,.12,.05,1),'LeatherDark':(.055,.026,.015,1),
 'Brass':(.37,.245,.073,1),'EyeWhite':(.84,.75,.57,1),'Iris':(.24,.09,.017,1),'Pupil':(.012,.005,.003,1),'Highlight':(.95,.89,.73,1),'Canvas':(.29,.27,.14,1),'Leaf':(.12,.19,.025,1)}
MATS={}
for n,color in COLORS.items():
 m=bpy.data.materials.new('YT_'+n);m.diffuse_color=color;m.use_nodes=True
 p=next(x for x in m.node_tree.nodes if x.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=.74 if n!='Brass' else .58;p.inputs['Metallic'].default_value=.25 if n=='Brass' else 0
 MATS[n]=m
original=bpy.context.scene
scene=bpy.data.scenes.new('YoungTrainer_Reference_V1');bpy.context.window.scene=scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
coll=bpy.data.collections.new('YT_Character');scene.collection.children.link(coll)
reviewcoll=bpy.data.collections.new('YT_ReviewOnly');scene.collection.children.link(reviewcoll)
scene['reference']='Reference/Character_Turnaround.png';scene['target_height_m']=1.4
scene['original_scene_preserved']=original.name
scene.world=bpy.data.worlds.new('YT_WarmStudio');scene.world.use_nodes=True
next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND').inputs[0].default_value=(.14,.115,.09,1)
next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND').inputs[1].default_value=.45

def mesh(name,vs,fs,mat,part,bone=None,uv=None):
 data=bpy.data.meshes.new('YT_'+name);data.from_pydata(vs,[],fs);data.update()
 o=bpy.data.objects.new('YT_'+name,data);coll.objects.link(o);o.data.materials.append(MATS[mat])
 o['part']=part;o['rig_mode']=bone or 'torso';o['palette']=mat
 for p in data.polygons:p.use_smooth=True
 if uv:
  layer=data.uv_layers.new(name='UVMap')
  for poly in data.polygons:
   for li in poly.loop_indices:layer.data[li].uv=uv[data.loops[li].vertex_index]
 PARTS.append(o);return o

def loft(name,rings,mat,part,bone=None,segments=24,fold=0,caps=True):
 # Each ring is (x,y,z,rx,ry); repeated cross-sections are deformation loops.
 vs=[];uv=[];fs=[]
 for i,(x,y,z,rx,ry) in enumerate(rings):
  for j in range(segments):
   a=math.tau*j/segments;f=1+fold*math.sin(6*a+i*.7)
   vs.append((x+rx*math.sin(a)*f,y-ry*math.cos(a)*f,z));uv.append((j/segments,i/(len(rings)-1)))
 for i in range(len(rings)-1):
  for j in range(segments):fs.append((i*segments+j,i*segments+(j+1)%segments,(i+1)*segments+(j+1)%segments,(i+1)*segments+j))
 if caps:
  for idx,rev in [(0,True),(len(rings)-1,False)]:
   k=len(vs);x,y,z,_,_=rings[idx];vs.append((x,y,z));uv.append((.5,idx/(len(rings)-1)))
   for j in range(segments):
    a=idx*segments+j;b=idx*segments+(j+1)%segments;fs.append((k,b,a) if rev else (k,a,b))
 return mesh(name,vs,fs,mat,part,bone,uv)

def tube(name,points,radii,mat,part,bone=None,n=16):
 vs=[];uv=[];fs=[]
 for i,p in enumerate(points):
  p=Vector(p);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
  t.normalize();u=t.cross(Vector((0,1,0))).normalized();v=t.cross(u).normalized()
  rx,ry=radii[i] if isinstance(radii[i],tuple) else (radii[i],radii[i])
  for j in range(n):
   a=math.tau*j/n;vs.append(tuple(p+u*(rx*math.cos(a))+v*(ry*math.sin(a))));uv.append((j/n,i/(len(points)-1)))
 for i in range(len(points)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 for idx,rev in [(0,True),(len(points)-1,False)]:
  k=len(vs);vs.append(points[idx]);uv.append((.5,idx/(len(points)-1)))
  for j in range(n):fs.append((k,idx*n+(j+1)%n,idx*n+j) if rev else (k,idx*n+j,idx*n+(j+1)%n))
 return mesh(name,vs,fs,mat,part,bone,uv)

def ellipsoid(name,pos,size,mat,part,bone=None,seg=24,rings=12):
 x,y,z=pos;rx,ry,rz=size
 rr=[(x,y,z-rz+2*rz*i/rings, max(.0004,rx*math.sin(math.pi*i/rings)),max(.0004,ry*math.sin(math.pi*i/rings))) for i in range(rings+1)]
 return loft(name,rr,mat,part,bone,seg)

def box(name,pos,size,mat,part,bone=None,bevel=.008):
 x,y,z=pos;sx,sy,sz=[v/2 for v in size]
 vs=[(x+a*sx,y+b*sy,z+c*sz) for a,b,c in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 fs=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
 o=mesh(name,vs,fs,mat,part,bone)
 if bevel:
  mod=o.modifiers.new('Crafted edges','BEVEL');mod.width=bevel;mod.segments=2
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.modifier_apply(modifier=mod.name);o.select_set(False)
 return o

def curve(name,points,radius,mat,part,bone=None):
 data=bpy.data.curves.new('YT_'+name,'CURVE');data.dimensions='3D';data.resolution_u=8;data.bevel_resolution=1;data.bevel_depth=radius
 sp=data.splines.new('POLY');sp.points.add(len(points)-1)
 for v,p in zip(sp.points,points):v.co=(*p,1)
 o=bpy.data.objects.new('YT_'+name,data);coll.objects.link(o);o.data.materials.append(MATS[mat]);o['part']=part;o['rig_mode']=bone or 'torso';o['palette']=mat;PARTS.append(o);return o

def checkpoint(name):
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Source/Stages'/name),check_existing=False)
 print('SAVED',name,'objects',len(PARTS))

def camera(name,pos,target,ortho=1.7):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);reviewcoll.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=ortho;return o

def area(name,pos,target,power,size,color):
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);reviewcoll.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.energy=power;d.shape='DISK';d.size=size;d.color=color
camera('YT_ReviewFront',(0,-4,.88),(0,0,.70))
camera('YT_ReviewBack',(0,4,.88),(0,0,.70))
camera('YT_ReviewSide',(4,0,.88),(0,0,.70))
camera('YT_ReviewThreeQuarter',(3,-4,1.5),(0,0,.7))
camera('YT_ReviewGame',(3,-3,4.6),(0,0,.7),1.9)
area('YT_Key',(-2,-3,4),(0,0,.8),220,4,(1,.87,.73))
area('YT_Fill',(3,-2,2),(0,0,.8),130,3,(.72,.83,1))
area('YT_Rim',(0,2,3),(0,0,.9),180,3,(1,.76,.52))
scene.camera=bpy.data.objects['YT_ReviewThreeQuarter'];scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=900;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'

# Phase 1-2: measured body and clothing envelope, neutral A-pose.
loft('Head',[(0,.013,1.035,.035,.035),(0,.006,1.055,.080,.068),(0,0,1.095,.121,.104),(0,0,1.135,.147,.127),(0,.008,1.185,.156,.142),(0,.012,1.23,.149,.145),(0,.013,1.275,.131,.133),(0,.016,1.315,.09,.094),(0,.018,1.335,.03,.035)],'Skin','Head','head',40)
loft('Neck',[(0,0,1.0,.054,.052),(0,0,1.03,.052,.05),(0,.006,1.065,.05,.048),(0,.006,1.085,.052,.05)],'Skin','Body','neck')
loft('Shirt',[(0,0,.62,.144,.095),(0,0,.66,.166,.109),(0,0,.74,.163,.11),(0,0,.82,.164,.112),(0,0,.9,.177,.111),(0,0,.96,.19,.105),(0,0,1.006,.164,.086),(0,0,1.035,.055,.05)],'Cream','Shirt',segments=32,fold=.02)
for side in [-1,1]:
 s='L' if side==1 else 'R'
 loft('Pants_'+s,[(side*.108,0,.23,.055,.053),(side*.107,0,.25,.071,.068),(side*.105,0,.28,.09,.082),(side*.104,0,.33,.084,.081),(side*.10,0,.38,.088,.08),(side*.096,0,.44,.101,.095),(side*.094,0,.51,.109,.10),(side*.090,0,.58,.115,.108),(side*.085,0,.64,.115,.112),(side*.083,0,.68,.100,.105)],'Olive','Pants','leg.'+s,24,.035)
 loft('Sock_'+s,[(side*.108,0,.145,.05,.047),(side*.108,0,.17,.052,.049),(side*.108,0,.185,.057,.05),(side*.108,0,.20,.055,.051),(side*.108,0,.225,.058,.052),(side*.108,0,.237,.056,.051)],'Cream','Socks','foot.'+s,20,.026)
 loft('BootSole_'+s,[(side*.108,-.037,0,.071,.112),(side*.108,-.037,.012,.074,.114),(side*.108,-.035,.026,.074,.113)],'LeatherDark','Boots','foot.'+s,28)
 loft('Boot_'+s,[(side*.108,-.035,.025,.072,.11),(side*.108,-.035,.045,.073,.11),(side*.108,-.030,.067,.071,.104),(side*.108,-.023,.092,.066,.088),(side*.108,-.006,.12,.054,.061),(side*.108,0,.15,.056,.057),(side*.108,0,.175,.059,.059)],'Leather','Boots','foot.'+s,28,.018)
 tube('Sleeve_'+s,[(side*.15,0,.98),(side*.19,0,.95),(side*.215,0,.91),(side*.238,0,.868),(side*.255,0,.832)],[(.074,.08),(.073,.074),(.065,.065),(.061,.059),(.062,.056)],'Cream','Shirt','arm.'+s,20)
 tube('Cuff_'+s,[(side*.25,0,.844),(side*.258,0,.825),(side*.263,0,.812)],[(.067,.062),(.072,.063),(.069,.063)],'Cream','Shirt','arm.'+s,20)
 tube('Forearm_'+s,[(side*.258,0,.826),(side*.278,0,.795),(side*.297,0,.756),(side*.315,0,.718),(side*.328,0,.689)],[(.044,.044),(.045,.043),(.037,.038),(.031,.031),(.029,.029)],'Skin','Body','forearm.'+s,20)
 ellipsoid('Palm_'+s,(side*.347,-.004,.652),(.042,.032,.052),'Skin','Hands','hand.'+s,20,10)
 for f in range(4):
  z=.635+(f-1.5)*.014;x=side*(.366+(.003 if f in [1,2] else 0))
  tube('Finger_'+s+str(f),[(x,-.017,z),(x+side*.02,-.025,z-.012),(x+side*.022,-.02,z-.033)],[.011,.011,.008],'Skin','Hands','hand.'+s,10)
 tube('Thumb_'+s,[(side*.325,-.025,.668),(side*.334,-.047,.648),(side*.348,-.047,.64)],[.016,.013,.008],'Skin','Hands','hand.'+s,12)
 for z,rx in [(.235,.062),(.256,.072)]:
  curve('PantsGather_'+s+str(z),[(side*.108+rx*math.sin(a),-.07*math.cos(a),z+.005*math.sin(3*a)) for a in [math.tau*j/40 for j in range(41)]],.003,'OliveLight','Pants','leg.'+s)
checkpoint('01_Blockout.blend')
bpy.app.driver_namespace['YT_ENV']=globals().copy()
print('PHASE_1_2_COMPLETE')
