"""Rig and in-place clips for the separately saved Meshy player. Run via Blender MCP."""
import bpy, math, json
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion
R=Path('/Users/harry/Developer/PokeMonster')
S=R/'Art/Characters/YoungTrainer/Source/Player_Meshy_GameReady_V1.blend'
E=R/'Art/Characters/YoungTrainer/Exports/MeshyV1'; E.mkdir(parents=True,exist_ok=True)
T=R/'Art/Characters/YoungTrainer/Textures/MeshyV1'; T.mkdir(parents=True,exist_ok=True)
assert bpy.data.filepath==str(S), 'Never modify original source'
obj=bpy.data.objects['Player_Meshy_Body']
assert not any(o.type=='ARMATURE' for o in bpy.data.objects), 'Run on prepared copy only'
# Preserve original proportions; normalize reduced mesh to exactly 1.40 m, soles at zero.
zmin=min(v.co.z for v in obj.data.vertices); zmax=max(v.co.z for v in obj.data.vertices)
scale=1.4/(zmax-zmin)
for v in obj.data.vertices:
 v.co=Vector((v.co.x*scale,v.co.y*scale,(v.co.z-zmin)*scale))
for p in obj.data.polygons:p.use_smooth=True
mat=obj.active_material; mat.name='M_Player_Meshy'
images={}
for name,label in [('Image_0','T_Player_Meshy_BaseColor'),('Image_1','T_Player_Meshy_ORM'),('Image_2','T_Player_Meshy_Normal')]:
 i=bpy.data.images[name]; i.name=label; i.filepath_raw=str(T/(label+'.png'));i.file_format='PNG';i.save();i.pack();images[label]=str(T/(label+'.png'))
armdata=bpy.data.armatures.new('Player_Meshy_Skeleton'); arm=bpy.data.objects.new('Player_Meshy_Rig',armdata);bpy.context.collection.objects.link(arm)
bpy.context.view_layer.objects.active=arm;arm.select_set(True);obj.select_set(False);bpy.ops.object.mode_set(mode='EDIT')
bones={}
def bone(n,h,t,parent=None):
 b=armdata.edit_bones.new(n);b.head=h;b.tail=t
 if parent:b.parent=bones[parent]
 bones[n]=b
bone('root',(0,0,0),(0,0,.12))
bone('pelvis',(0,0,.61),(0,0,.74),'root')
bone('spine',(0,0,.74),(0,0,.91),'pelvis')
bone('chest',(0,0,.91),(0,0,1.055),'spine')
bone('neck',(0,0,1.055),(0,0,1.13),'chest')
bone('head',(0,0,1.13),(0,0,1.37),'neck')
bone('cape_upper',(0,.105,1.015),(0,.145,.66),'chest')
bone('cape_lower',(0,.145,.66),(0,.18,.275),'cape_upper')
bone('bag',(.195,-.095,.80),(.195,-.095,.64),'spine')
for side,s in [('l',1),('r',-1)]:
 bone('clavicle_'+side,(s*.035,0,1.035),(s*.215,0,1.04),'chest')
 bone('upperarm_'+side,(s*.215,0,1.04),(s*.425,-.005,1.043),'clavicle_'+side)
 bone('lowerarm_'+side,(s*.425,-.005,1.043),(s*.585,-.024,1.025),'upperarm_'+side)
 bone('hand_'+side,(s*.585,-.024,1.025),(s*.697,-.038,1.005),'lowerarm_'+side)
 bone('thigh_'+side,(s*.105,0,.61),(s*.133,-.009,.32),'pelvis')
 bone('shin_'+side,(s*.133,-.009,.32),(s*.16,0,.085),'thigh_'+side)
 bone('foot_'+side,(s*.16,0,.085),(s*.16,-.16,.05),'shin_'+side)
bpy.ops.object.mode_set(mode='OBJECT');arm.show_in_front=True
# Regional weights keep the cape independent of the legs and the bag rigid.
groups={n:obj.vertex_groups.new(name=n) for n in bones}
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def assign(i,w):
 w={n:v for n,v in w.items() if v>.0001};total=sum(w.values())
 for n,v in w.items():groups[n].add([i],v/total,'REPLACE')
for v in obj.data.vertices:
 x,y,z=v.co;ax=abs(x);side='l' if x>=0 else 'r'
 if z>1.09 and ax<.245:
  t=smooth(1.085,1.145,z);w={'neck':1-t,'head':t}
 elif ax>.225 and z>.91:
  if ax<.43:
   t=smooth(.365,.465,ax);w={'upperarm_'+side:1-t,'lowerarm_'+side:t}
  else:
   t=smooth(.545,.605,ax);w={'lowerarm_'+side:1-t,'hand_'+side:t}
 elif y>.092 and z<.94:
  t=smooth(.40,.83,z);w={'cape_lower':1-t,'cape_upper':t}
 elif x>.155 and y<-.075 and .63<z<.82:
  w={'bag':1}
 elif z>.56:
  if z<.76:
   t=smooth(.66,.79,z);w={'pelvis':1-t,'spine':t}
  elif z<.965:
   t=smooth(.84,.97,z);w={'spine':1-t,'chest':t}
  else:
   t=smooth(1.025,1.10,z);w={'chest':1-t,'neck':t}
 else:
  if z<.16:
   t=smooth(.075,.19,z);w={'foot_'+side:1-t,'shin_'+side:t}
  else:
   t=smooth(.26,.40,z);w={'shin_'+side:1-t,'thigh_'+side:t}
 assign(v.index,w)
# Blend the sleeve/shoulder boundary continuously; avoid stretched T-pose spikes.
for v in obj.data.vertices:
 x,y,z=v.co;ax=abs(x);side='l' if x>=0 else 'r'
 if ax<.175 or z<.78:continue
 strength=smooth(.175,.305,ax)*smooth(.80,.96,z)
 if strength<.001:continue
 if ax<.43:
  t=smooth(.365,.465,ax);a={'upperarm_'+side:1-t,'lowerarm_'+side:t}
 else:
  t=smooth(.545,.605,ax);a={'lowerarm_'+side:1-t,'hand_'+side:t}
 w={'chest' if z>.86 else 'spine':1-strength};w.update({n:q*strength for n,q in a.items()})
 for g in obj.vertex_groups:g.remove([v.index])
 assign(v.index,w)
# The wrapped cape sides need their own bones even in front of the rear plane.
for v in obj.data.vertices:
 x,y,z=v.co
 if .21<z<.89 and (y>.075 or (abs(x)>.195 and y>-.06)):
  t=smooth(.4,.83,z)
  for grp in obj.vertex_groups:grp.remove([v.index])
  assign(v.index,{'cape_upper':t,'cape_lower':1-t})
obj.parent=arm;mod=obj.modifiers.new('Humanoid deformation','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True
scene=bpy.context.scene;scene.render.fps=30
pb=arm.pose.bones
for p in pb:p.rotation_mode='QUATERNION'
def global_rotation(name,axis,angle):
 b=armdata.bones[name].matrix_local.to_quaternion();pb[name].rotation_quaternion=b.inverted()@Quaternion(axis,angle)@b

def pose(frame,phase,walk):
 for p in pb:p.location=(0,0,0);p.rotation_quaternion=Quaternion()
 breath=.012*math.sin(phase) if not walk else .01*math.sin(2*phase)
 global_rotation('chest',(1,0,0),breath)
 global_rotation('head',(0,0,1),.014*math.sin(phase))
 global_rotation('cape_upper',(1,0,0),.018*math.sin(phase))
 global_rotation('cape_lower',(1,0,0),.025*math.sin(phase-.4))
 for side,s in [('l',1),('r',-1)]:
  # Relaxed arms; opposing swing, not a permanent T-pose.
  global_rotation('upperarm_'+side,(0,1,0),s*math.radians(73))
  swing=(.17*math.cos(phase+(0 if s==1 else math.pi))) if walk else .006*math.sin(phase)
  q=pb['upperarm_'+side].rotation_quaternion.copy()
  b=armdata.bones['upperarm_'+side].matrix_local.to_quaternion()
  pb['upperarm_'+side].rotation_quaternion=(b.inverted()@Quaternion((1,0,0),swing)@b)@q
  global_rotation('lowerarm_'+side,(0,1,0),s*math.radians(7))
  if walk:
   a=phase+(0 if s==1 else math.pi)
   # Alternating stance and raised recovery foot, solved as a two-link chain.
   hip=Vector((s*.105,0,.61));ankle=Vector((s*.16,-.115*math.cos(a),.085+.072*max(0,math.sin(a))**2))
   l1=(armdata.bones['thigh_'+side].tail_local-armdata.bones['thigh_'+side].head_local).length
   l2=(armdata.bones['shin_'+side].tail_local-armdata.bones['shin_'+side].head_local).length
   d=ankle-hip;length=min(d.length,l1+l2-.001);direction=d.normalized()
   along=(l1*l1-l2*l2+length*length)/(2*length)
   perpendicular=Vector((0,-direction.z,direction.y)).normalized()
   if perpendicular.y>0:perpendicular=-perpendicular
   knee=hip+direction*along+perpendicular*math.sqrt(max(0,l1*l1-along*along))
   for n,h,t in [('thigh_'+side,hip,knee),('shin_'+side,knee,ankle),('foot_'+side,ankle,ankle+Vector((0,-.16,-.035)))]:
    b=armdata.bones[n];q=(b.tail_local-b.head_local).rotation_difference(t-h)
    pb[n].matrix=Matrix.Translation(h)@(q.to_matrix().to_4x4()@b.matrix_local.to_3x3().to_4x4())
    bpy.context.view_layer.update()
 for p in pb:
  p.keyframe_insert(data_path='location',frame=frame,group=p.name)
  p.keyframe_insert(data_path='rotation_quaternion',frame=frame,group=p.name)

arm.animation_data_create()
for name,count,iswalk in [('A_Player_Meshy_Idle',61,False),('A_Player_Meshy_Walk',31,True)]:
 action=bpy.data.actions.new(name);arm.animation_data.action=action
 for frame in range(1,count+1):pose(frame,2*math.pi*(frame-1)/(count-1),iswalk)
 action.use_fake_user=True
 # Linear keys at 30 Hz avoid quaternion overshoot between baked contact poses.
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
arm.animation_data.action=bpy.data.actions['A_Player_Meshy_Idle'];scene.frame_start=1;scene.frame_end=61;scene.frame_set(1)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(S))
print(json.dumps({'file':str(S),'height':max(v.co.z for v in obj.data.vertices)-min(v.co.z for v in obj.data.vertices),'faces':len(obj.data.polygons),'vertices':len(obj.data.vertices),'bones':len(armdata.bones),'actions':[a.name for a in bpy.data.actions],'textures':images},indent=2))
