"""Own short-leg gait: analytic sagittal two-bone IK, in-place clips and measured stance drift."""
import bpy,math,json,bmesh
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Zunderlauf';O=R/'Saved/MeshyGlumandaV1';bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Glumanda_Meshy_V1.blend'));bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;rig=bpy.data.objects['Glumanda_Meshy_Rig'];body=bpy.data.objects['Glumanda_Meshy'];flame=bpy.data.objects['Meshy_TailFlame_Original']
# Rig and original flame already prepared for this source.
boundary={tuple(round(x,6)for x in (flame.matrix_world@v.co))for v in flame.data.vertices}
for v in body.data.vertices:
 if tuple(round(x,6)for x in v.co) in boundary:
  for group in body.vertex_groups:group.remove([v.index])
  body.vertex_groups['tail_tip'].add([v.index],1.,'REPLACE')
rest={p.name:p.bone.matrix_local.copy() for p in rig.pose.bones};heads={p.name:p.bone.head_local.copy()for p in rig.pose.bones};tails={p.name:p.bone.tail_local.copy()for p in rig.pose.bones}
def orient(name,head,tail):
 p=rig.pose.bones[name];q=(tails[name]-heads[name]).rotation_difference(Vector(tail)-Vector(head));p.matrix=Matrix.Translation(head)@q.to_matrix().to_4x4()@rest[name].to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
def ik(side,ankle):
 a='thigh_'+side;b='shin_'+side;f='foot_'+side;hip=rig.pose.bones[a].head.copy();L=(tails[a]-heads[a]).length;M=(tails[b]-heads[b]).length;delta=ankle-hip;distance=delta.length
 assert distance<L+M-.00001,(side,distance,L+M)
 d=delta.normalized();front=Vector((0,-1,0));pole=(front-d*front.dot(d)).normalized();along=(L*L-M*M+distance*distance)/(2*distance);knee=hip+d*along+pole*math.sqrt(max(0,L*L-along*along));orient(a,hip,knee);orient(b,knee,ankle);rig.pose.bones[f].matrix=Matrix.Translation(ankle-heads[f])@rest[f];bpy.context.view_layer.update()
clips={'Idle':(2.,0),'Walk':(.6,.22),'Run':(.4,.36),'Attack':(.8,0),'Hit':(.45,0),'Faint':(1.1,0),'Happy':(1.,0)};audit={};rig.animation_data_clear()
for action in list(bpy.data.actions):
 assert action.name.startswith('Glumanda_'),'Unexpected action in own creature source'
 bpy.data.actions.remove(action)
for name,(duration,speed)in clips.items():
 n=round(duration*30);duration=n/30;action=bpy.data.actions.new('Glumanda_'+name);action.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=action;positions={side:[] for side in ['L','R']};ground=[]
 for frame in range(n+1):
  s.frame_set(frame+1);t=frame/n;wave=math.sin(math.tau*t)
  for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
  root=rig.pose.bones['root'];pelvis=rig.pose.bones['pelvis'];chest=rig.pose.bones['chest'];head=rig.pose.bones['head']
  if name in ['Walk','Run']:
   pelvis.matrix=Matrix.Translation((0,0,.00015*(1+math.cos(2*math.tau*t))))@rest['pelvis']
  elif name=='Idle':chest.scale=(1+.004*wave,1+.006*wave,1+.003*wave);head.rotation_quaternion=Quaternion((0,0,1),math.radians(.7)*wave)
  elif name=='Attack':
   pulse=math.sin(math.pi*t)**2;root.matrix=Matrix.Translation((0,-.035*pulse,0))@rest['root'];chest.rotation_quaternion=Quaternion((1,0,0),math.radians(10)*pulse);head.rotation_quaternion=Quaternion((1,0,0),math.radians(-5)*pulse)
  elif name=='Hit':root.matrix=Matrix.Translation((0,.018*math.sin(math.pi*t),0))@rest['root'];chest.rotation_quaternion=Quaternion((1,0,0),math.radians(-9)*math.sin(math.pi*t))
  elif name=='Faint':
   q=t*t*(3-2*t);root.matrix=Matrix.Translation((.035*q,0,.15*q))@Quaternion((0,1,0),math.radians(82)*q).to_matrix().to_4x4()@rest['root']
  elif name=='Happy':root.matrix=Matrix.Translation((0,0,.045*math.sin(math.pi*t)**2))@rest['root'];head.rotation_quaternion=Quaternion((0,0,1),math.radians(4)*wave)
  bpy.context.view_layer.update()
  for side,offset in [('L',0),('R',.5)]:
   phase=(t+offset)%1
   if name in ['Walk','Run']:
    duty=.5 if name=='Walk'else.42;travel=speed*duration*duty;ankle=heads['foot_'+side].copy();ankle.y=-.025
    if phase<duty:ankle.y+=travel*(phase/duty-.5)
    else:u=(phase-duty)/(1-duty);ankle.y+=travel*(.5-u);ankle.z+=(.012 if name=='Walk' else .018)*math.sin(math.pi*u)**1.5
    ik(side,ankle);positions[side].append({'phase':phase,'ankle':list(rig.pose.bones['foot_'+side].head),'stance':phase<duty})

   elif name in ['Idle','Attack','Hit','Happy']:
    ankle=heads['foot_'+side].copy()+(root.matrix.translation-rest['root'].translation);ik(side,ankle)
  # T-pose input needs a fitted resting arm pose, not V1 local-axis rotations.
  chest_delta=rig.pose.bones['chest'].matrix.to_3x3()@rest['chest'].to_3x3().inverted()
  for side,sign,phase_offset in [('L',1,0),('R',-1,.5)]:
   swing=math.sin(math.tau*(t+phase_offset))*(.18 if name=='Walk' else .28 if name=='Run' else .015)
   for bone_name,direction in [('upperarm_',Vector((sign*.48,-.08+swing,-.874))),('forearm_',Vector((sign*.31,-.15+swing,-.94))),('hand_',Vector((sign*.31,-.22,-.925)))]:
    bn=bone_name+side;h=rig.pose.bones[bn].head.copy();orient(bn,h,h+chest_delta@direction.normalized()*(tails[bn]-heads[bn]).length)
  pelvis_delta=rig.pose.bones['pelvis'].matrix.to_3x3()@rest['pelvis'].to_3x3().inverted()
  for k in range(1,5):
   bn='tail_0'+str(k);h=rig.pose.bones[bn].head.copy();angle=math.radians(2 if name=='Idle' else 4)*math.sin(math.tau*t-k*.42);direction=pelvis_delta@(Quaternion((0,0,1),angle)@(tails[bn]-heads[bn]));orient(bn,h,h+direction)
  bpy.context.view_layer.update()
  dg=bpy.context.evaluated_depsgraph_get();ev=body.evaluated_get(dg);mesh=ev.to_mesh();worst=min(mesh.vertices,key=lambda v:v.co.z);low=worst.co.z
  if low<-.01:
   original=body.data.vertices[worst.index];print('LOW_VERTEX',name,frame,low,list(original.co),[(body.vertex_groups[g.group].name,g.weight) for g in original.groups if g.weight>.001],flush=True)
  ev.to_mesh_clear()
  if name=='Faint' and low<.001:
   matrix=root.matrix.copy();matrix.translation.z+=.001-low;root.matrix=matrix;bpy.context.view_layer.update();low=.001
  ground.append(low)
  for p in rig.pose.bones:
   for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=frame+1,group=p.name)

 # Linear keys keep the explicitly solved stance from overshooting between samples.
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
 drift=[]
 for side,rows in positions.items():
  for i in range(1,len(rows)):
   if rows[i-1]['stance'] and rows[i]['stance'] and rows[i]['phase']>rows[i-1]['phase']:
    dy=rows[i]['ankle'][1]-rows[i-1]['ankle'][1];drift.append(abs(dy-speed/30))
 audit[name]={'frames':n+1,'seconds':duration,'authored_speed_cm_s':speed*100,'stance_increment_error_max_m':max(drift,default=0),'mesh_min_z_m':min(ground),'bones':len(rig.data.bones)}
 assert min(ground)>=-.0005,audit[name]
 if speed:assert max(drift)<.00005,audit[name]
 # FBX export includes only this action and the existing mesh, never the separate flame.
 s.frame_start=1;s.frame_end=n+1;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(True);bpy.context.view_layer.objects.active=rig
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports/MeshyV1'/('Glumanda_'+name+'.fbx')),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO')
rig.animation_data.action=bpy.data.actions['Glumanda_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1)
# Flame source export at local origin. The skeleton socket supplies placement in Unreal.
color=flame.data.color_attributes.get('FlameBend') or flame.data.color_attributes.new(name='FlameBend',type='FLOAT_COLOR',domain='CORNER')
for loop in flame.data.loops:
 mask=max(0.,min(1.,(flame.data.vertices[loop.vertex_index].co.z-.015)/.08));color.data[loop.index].color=(mask,mask,mask,1)
old=flame.matrix_world.copy();oldparent=flame.parent;flame.parent=None;flame.matrix_world=Matrix.Identity(4);bpy.ops.object.select_all(action='DESELECT');flame.select_set(True);bpy.context.view_layer.objects.active=flame
bpy.ops.export_scene.fbx(filepath=str(A/'Exports/MeshyV1/Glumanda_TailFlame.fbx'),use_selection=True,object_types={'MESH'},bake_anim=False,axis_forward='-Y',axis_up='Z',apply_unit_scale=True,mesh_smooth_type='FACE')
flame.parent=oldparent;flame.parent_type='BONE';flame.parent_bone='tail_socket';flame.matrix_world=old
bpy.ops.wm.save_as_mainfile(filepath=str(A/'Source/Glumanda_Meshy_V1.blend'));(A/'MeshyV1_AnimationAudit.json').write_text(json.dumps(audit,indent=2));print('ANIMATION_EXPORT_PASS',json.dumps(audit))
