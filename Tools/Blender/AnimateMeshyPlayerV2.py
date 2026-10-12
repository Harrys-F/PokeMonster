"""Author a speed-matched in-place gait in the preserved V2 working copy, via Blender MCP."""
import bpy, math, json
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster')
assert Path(bpy.data.filepath).name=='Player_Meshy_AnimationQuality_V2.blend'
arm=bpy.data.objects['Player_Meshy_Rig'];obj=bpy.data.objects['Player_Meshy_Body'];scene=bpy.context.scene
arm.animation_data.action=None;arm.data.pose_position='POSE'
arm.hide_set(False);arm.hide_viewport=False;arm.select_set(True);bpy.context.view_layer.objects.active=arm
bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode='EDIT')
for n,x in [('cape_left',.17),('cape_right',-.17)]:
 if n not in arm.data.edit_bones:
  b=arm.data.edit_bones.new(n);b.head=(x,.14,.66);b.tail=(x,.18,.28);b.parent=arm.data.edit_bones['cape_upper']
b=arm.data.edit_bones['bag'];b.head=(.22,-.04,.78);b.tail=(.245,-.04,.59)
bpy.ops.object.mode_set(mode='OBJECT')
groups={g.name:g for g in obj.vertex_groups}
for n in ['cape_left','cape_right']:
 if n not in groups:groups[n]=obj.vertex_groups.new(name=n)
def smooth(a,b,x):
 t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)
def weight(v,w):
 for g in obj.vertex_groups:g.remove([v.index])
 t=sum(w.values())
 for n,q in w.items():
  if q>1e-5:groups[n].add([v.index],q/t,'REPLACE')
bagcount=0;capecount=0
for v in obj.data.vertices:
 x,y,z=v.co
 # Body of the hip satchel only; diagonal strap and upper attachment remain on torso.
 bag=smooth(.182,.213,x)*(1-smooth(.716,.775,z))*smooth(.515,.558,z)*(1-smooth(-.005,.055,y))
 if bag>.001:
  old={obj.vertex_groups[g.group].name:g.weight*(1-bag) for g in v.groups}
  old['bag']=old.get('bag',0)+bag;weight(v,old);bagcount+=1
 elif .21<z<.94 and (y>.077 or (.205<abs(x)<.37 and y>-.052 and z<.85)):
  upper=smooth(.44,.88,z);side=smooth(.045,.21,abs(x))
  w={'cape_upper':upper,'cape_lower':(1-upper)*(1-side),('cape_left' if x>0 else 'cape_right'):(1-upper)*side}
  weight(v,w);capecount+=1
scene.render.fps=60
pb=arm.pose.bones
for p in pb:p.rotation_mode='QUATERNION'
def rot(n,axis,a):
 q=arm.data.bones[n].matrix_local.to_quaternion();pb[n].rotation_quaternion=(q.inverted()@Quaternion(axis,a)@q)@pb[n].rotation_quaternion

def solve(side,ankle,foot_angle):
 s=1 if side=='l' else -1
 bpy.context.view_layer.update();hip=pb['thigh_'+side].head.copy()
 b1=arm.data.bones['thigh_'+side];b2=arm.data.bones['shin_'+side]
 l1=b1.length;l2=b2.length;d=ankle-hip;length=min(d.length,l1+l2-.0005);direction=d.normalized()
 along=(l1*l1-l2*l2+length*length)/(2*length)
 perpendicular=Vector((0,-direction.z,direction.y)).normalized()
 if perpendicular.y>0:perpendicular=-perpendicular
 knee=hip+direction*along+perpendicular*math.sqrt(max(0,l1*l1-along*along))
 tail=Quaternion((1,0,0),foot_angle)@Vector((0,-.16,-.035))
 for n,h,t in [('thigh_'+side,hip,knee),('shin_'+side,knee,ankle),('foot_'+side,ankle,ankle+tail)]:
  b=arm.data.bones[n];q=(b.tail_local-b.head_local).rotation_difference(t-h)
  pb[n].matrix=Matrix.Translation(h)@q.to_matrix().to_4x4()@b.matrix_local.to_3x3().to_4x4();bpy.context.view_layer.update()

def pose(frame,t,walk,duration):
 phase=2*math.pi*t
 for p in pb:p.location=(0,0,0);p.rotation_quaternion=Quaternion()
 if walk:
  # A 0.55 s stride covers 1.155 m at 2.1 m/s. Stance foot travels at exactly -2.1 m/s.
  pb['pelvis'].location=(.008*math.sin(phase),-.092+.006*math.cos(2*phase),0) # pelvis local Y is world Z
  rot('pelvis',(0,0,1),.045*math.sin(phase));rot('spine',(0,0,1),-.035*math.sin(phase))
  rot('chest',(1,0,0),.018+.012*math.sin(2*phase));rot('chest',(0,0,1),-.035*math.sin(phase))
  rot('head',(0,0,1),.02*math.sin(phase))
 else:
  rot('chest',(1,0,0),.006*math.sin(phase));rot('head',(1,0,0),-.003*math.sin(phase))
 # Baked restrained gait flutter; runtime springs add stop/turn response.
 rot('cape_upper',(1,0,0),(-.045-.018*math.sin(2*phase-.5)) if walk else -.012)
 for n,k,offset in [('cape_lower',.045,.9),('cape_left',.06,.6),('cape_right',.06,1.2)]:
  rot(n,(1,0,0),(-.035-k*math.sin(2*phase-offset)) if walk else -.008)
  if walk:rot(n,(0,1,0),.025*math.sin(phase-offset))
 rot('bag',(1,0,0),.075*math.sin(phase-.6) if walk else .003*math.sin(phase))
 for side,s in [('l',1),('r',-1)]:
  a=phase+(0 if s==1 else math.pi)
  q=arm.data.bones['upperarm_'+side].matrix_local.to_quaternion()
  # Opposite arm advances with the opposite leg; forearms remain softly bent.
  pb['upperarm_'+side].rotation_quaternion=q.inverted()@Quaternion((1,0,0),(.22*math.cos(a) if walk else .004*math.sin(a)))@Quaternion((0,1,0),s*math.radians(76))@q
  rot('lowerarm_'+side,(0,1,0),s*math.radians(7))
  if walk:
   u=(t+(0 if s==1 else .5))%1;span=2.1*duration*.5
   if u<.5:forward=span*(.5-2*u);lift=0.;pitch=.025*math.sin(2*math.pi*u)
   else:
    v=(u-.5)*2;forward=-span*.5+span*(v*v*(3-2*v));lift=.066*math.sin(math.pi*v)**2;pitch=-.13*math.sin(math.pi*v)
   ankle=Vector((s*.16,-forward,.085+lift+.002))
   solve(side,ankle,pitch)
 # Enforce foot sole clearance on the actual deformed geometry (not only ankle markers).
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();em=obj.evaluated_get(dg).to_mesh()
 for side in ['l','r']:
  ids=[v.index for v in obj.data.vertices if v.co.z<.085 and ((v.co.x>0)==(side=='l'))]
  low=min(em.vertices[i].co.z for i in ids)
  if low<.0005:
   m=pb['foot_'+side].matrix.copy();m.translation.z+=.0005-low;pb['foot_'+side].matrix=m
 obj.evaluated_get(dg).to_mesh_clear()
 for p in pb:
  p.keyframe_insert(data_path='location',frame=frame,group=p.name);p.keyframe_insert(data_path='rotation_quaternion',frame=frame,group=p.name)
for name,count,walk in [('A_Player_Meshy_Idle_V2',181,False),('A_Player_Meshy_Walk_V2',34,True)]:
 a=bpy.data.actions.get(name) or bpy.data.actions.new(name)
 for layer in list(a.layers):a.layers.remove(layer)
 a.use_fake_user=True;arm.animation_data.action=a
 duration=(count-1)/60
 for f in range(1,count+1):pose(f,(f-1)/(count-1),walk,duration)
 for layer in a.layers:
  for strip in layer.strips:
   for cb in strip.channelbags:
    for curve in cb.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
arm.animation_data.action=bpy.data.actions['A_Player_Meshy_Walk_V2'];scene.frame_start=1;scene.frame_end=34;scene.frame_set(1)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print(json.dumps({'bones':len(arm.data.bones),'bag_weighted_vertices':bagcount,'cape_vertices':capecount,'cycle_seconds':.55,'stance_velocity_m_s':2.1,'stride_m':1.155,'height_m':max(v.co.z for v in obj.data.vertices)-min(v.co.z for v in obj.data.vertices)}))
