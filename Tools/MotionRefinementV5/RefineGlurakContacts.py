"""Verified own candidate only: lift low belly 1.3 cm while IK retains both original foot transforms."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Glurak';p=A/'Source/Glurak_MotionV5.blend';audit=json.loads((A/'MotionV5_Audit.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not __import__('subprocess').check_output(['git','ls-files','--',str(p.relative_to(R))],cwd=R).strip(),'Candidate is versioned: do not overwrite a released source';assert digest(p)==audit['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;rig=bpy.data.objects['Glurak_Rig'];body=bpy.data.objects['Glurak_Body'];s=bpy.context.scene;action=bpy.data.actions['Glurak_Run_MotionV5'];rig.animation_data.action=action;start,end=map(int,action.frame_range);cache={};offset=Vector((0,0,.013))
for f in range(start,end+1):
 s.frame_set(f);cache[f]={b.name:b.matrix.copy()for b in rig.pose.bones}
def orient(n,a,b):
 bone=rig.data.bones[n];q=(bone.tail_local-bone.head_local).rotation_difference(b-a);rig.pose.bones[n].matrix=Matrix.Translation(a)@q.to_matrix().to_4x4()@bone.matrix_local.to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
foot_errors=[];zs=[]
for f in range(start,end+1):
 s.frame_set(f)
 for b in rig.pose.bones:
  m=cache[f][b.name].copy()
  if b.name!='root':m.translation+=offset
  b.matrix=m;bpy.context.view_layer.update()
 for side in ['L','R']:
  thigh='thigh_'+side;shin='shin_'+side;foot='foot_'+side;hip=cache[f][thigh].translation+offset;ankle=cache[f][foot].translation;v=ankle-hip;distance=v.length;a=rig.data.bones[thigh].length;b=rig.data.bones[shin].length;assert abs(a-b)<distance<(a+b)*.999
  direction=v.normalized();pole=Vector((0,-1,0));pole=(pole-direction*pole.dot(direction)).normalized();x=(a*a-b*b+distance*distance)/(2*distance);knee=hip+direction*x+pole*math.sqrt(max(0,a*a-x*x));orient(thigh,hip,knee);orient(shin,knee,ankle);rig.pose.bones[foot].matrix=cache[f][foot]
 bpy.context.view_layer.update()
 foot_errors.append(max((rig.pose.bones['foot_'+side].matrix.translation-cache[f]['foot_'+side].translation).length for side in ['L','R']))
 for bone in rig.pose.bones:
  for prop in ['location','rotation_quaternion','scale']:bone.keyframe_insert(data_path=prop,frame=f)
 ob=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh();zs.append(min(v.co.z for v in m.vertices));ob.to_mesh_clear()
assert min(zs)>-.0001,(min(zs),max(foot_errors));assert max(foot_errors)<1e-5
rig.animation_data.action=bpy.data.actions['Glurak_Idle_MotionV5'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p));audit['source_sha256']=digest(p);audit['metrics']['Run']['minimum_z_cm']=min(zs)*100;audit['run_contact_repair']=dict(hip_lift_cm=1.3,maximum_original_foot_transform_error_m=max(foot_errors));(A/'MotionV5_Audit.json').write_text(json.dumps(audit,indent=2));print('GLURAK_CONTACTS_PASS',min(zs)*100,max(foot_errors),flush=True)
