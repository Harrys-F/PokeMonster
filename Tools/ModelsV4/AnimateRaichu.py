"""Seven authored in-place roles using the existing visual proxy, with explicit planted-foot IK."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Raichu';bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Raichu_V4.blend'));bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;rig=bpy.data.objects['Raichu_Rig'];body=bpy.data.objects['Raichu'];rest={p.name:p.bone.matrix_local.copy()for p in rig.pose.bones};heads={p.name:p.bone.head_local.copy()for p in rig.pose.bones};tails={p.name:p.bone.tail_local.copy()for p in rig.pose.bones};rig.animation_data_clear()
assert not list(bpy.data.actions),'Do not replace prior hand-authored actions'
def orient(n,h,t):
 p=rig.pose.bones[n];q=(tails[n]-heads[n]).rotation_difference(Vector(t)-Vector(h));p.matrix=Matrix.Translation(h)@q.to_matrix().to_4x4()@rest[n].to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
def ik(side,ankle):
 a='thigh_'+side;b='shin_'+side;f='foot_'+side;hip=rig.pose.bones[a].head.copy();L=(tails[a]-heads[a]).length;M=(tails[b]-heads[b]).length;delta=ankle-hip;distance=delta.length
 assert distance<L+M-.00001,(side,distance,L+M)
 d=delta.normalized();pole=Vector((0,-1,0));pole=(pole-d*pole.dot(d)).normalized();along=(L*L-M*M+distance*distance)/(2*distance);knee=hip+d*along+pole*math.sqrt(max(0,L*L-along*along));orient(a,hip,knee);orient(b,knee,ankle);rig.pose.bones[f].matrix=Matrix.Translation(ankle-heads[f])@rest[f];bpy.context.view_layer.update()
audit={};clips={'Idle':(2.,0),'Walk':(.6,.35),'Run':(.4,.65),'Attack':(.8,0),'Hit':(.5,0),'Faint':(1.2,0),'Happy':(1.2,0)}
for name,(duration,speed)in clips.items():
 n=round(duration*30);duration=n/30;act=bpy.data.actions.new('Raichu_'+name);act.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=act;ground=[];tracks={side:[]for side in ['L','R']}
 for i in range(n+1):
  s.frame_set(i+1);t=i/n;wave=math.sin(math.tau*t)
  for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
  root=rig.pose.bones['root'];pelvis=rig.pose.bones['pelvis'];chest=rig.pose.bones['chest'];head=rig.pose.bones['head'];pulse=math.sin(math.pi*t)**2
  if name in ['Walk','Run']:pelvis.matrix=Matrix.Translation((0,0,-.031+.0015*math.cos(math.tau*2*t)))@rest['pelvis']
  elif name=='Idle':chest.scale=(1+.003*wave,1+.005*wave,1+.003*wave);head.rotation_quaternion=Quaternion((0,0,1),.009*wave)
  elif name=='Attack':root.matrix=Matrix.Translation((0,-.025*pulse,0))@rest['root'];chest.rotation_quaternion=Quaternion((1,0,0),.12*pulse)
  elif name=='Hit':root.matrix=Matrix.Translation((0,.018*pulse,0))@rest['root'];chest.rotation_quaternion=Quaternion((1,0,0),-.13*pulse)
  elif name=='Faint':q=t*t*(3-2*t);root.matrix=Matrix.Translation((0,.05*q,0))@Quaternion((1,0,0),math.radians(82)*q).to_matrix().to_4x4()@rest['root']
  elif name=='Happy':root.matrix=Matrix.Translation((0,0,.025*pulse))@rest['root'];head.rotation_quaternion=Quaternion((0,0,1),.06*wave)
  bpy.context.view_layer.update()
  for side,off in [('L',0),('R',.5)]:
   phase=(t+off)%1;arm=rig.pose.bones['upperarm_'+side]
   if speed:
    duty=.50 if name=='Walk'else .40;travel=speed*duration*duty;ankle=heads['foot_'+side].copy();ankle.y=-.019
    if phase<duty:ankle.y+=travel*(phase/duty-.5)
    else:u=(phase-duty)/(1-duty);ankle.y+=travel*(.5-u);ankle.z+=.023*math.sin(math.pi*u)**1.4
    ik(side,ankle);tracks[side].append({'phase':phase,'stance':phase<duty,'y':rig.pose.bones['foot_'+side].head.y});arm.rotation_quaternion=Quaternion((1,0,0),(.15 if name=='Walk'else .24)*math.sin(math.tau*phase+math.pi))
   elif name in ['Idle','Attack','Hit','Happy']:ik(side,heads['foot_'+side]+root.matrix.translation-rest['root'].translation)
   if name=='Attack':arm.rotation_quaternion=Quaternion((1,0,0),-.65*pulse)
   if name=='Happy':arm.rotation_quaternion=Quaternion((0,1,0),(.20 if side=='L'else-.20)*pulse)
   rig.pose.bones['ear_'+side].rotation_quaternion=Quaternion((0,1,0),.025*math.sin(math.tau*t+off))
  for k in range(1,5):rig.pose.bones['tail_0'+str(k)].rotation_quaternion=Quaternion((0,0,1),(.016 if name=='Idle'else .026)*math.sin(math.tau*t-k*.4))
  bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();low=min(v.co.z for v in m.vertices);ev.to_mesh_clear()
  if name=='Faint':mat=root.matrix.copy();mat.translation.z+=.003-low;root.matrix=mat;bpy.context.view_layer.update();low=.003
  ground.append(low)
  for p in rig.pose.bones:
   for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=i+1,group=p.name)
 for layer in act.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
 drift=[]
 for rows in tracks.values():
  for a,b in zip(rows,rows[1:]):
   if a['stance']and b['stance']and b['phase']>a['phase']:drift.append(abs(b['y']-a['y']-speed/30))
 audit[name]={'duration':duration,'frames':n+1,'speed_cm_s':speed*100,'minimum_surface_z_m':min(ground),'stance_increment_error_m':max(drift,default=0)}
 assert min(ground)>-.012,(name,min(ground))
 if speed:assert max(drift)<.0001,(name,max(drift))
 s.frame_start=1;s.frame_end=n+1;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(True);bpy.context.view_layer.objects.active=rig
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports/V4'/('Raichu_'+name+'.fbx')),use_selection=True,object_types={'ARMATURE','MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO')
rig.animation_data.action=bpy.data.actions['Raichu_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(A/'Source/Raichu_V4.blend'));(A/'AnimationAudit.json').write_text(json.dumps(audit,indent=2));print('RAICHU_CLIPS_EXPORTED',audit)
