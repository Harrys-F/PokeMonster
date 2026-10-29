"""Animate one fitted species. World-space two-bone IK avoids local-axis gait errors."""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent));from Anatomy import SPECS
name=sys.argv[sys.argv.index('--')+1];spec=SPECS[name];A=R/'Art/Characters/Creatures'/name;audit=json.loads((A/'MeshyV1_ModelAudit.json').read_text());source=A/'Source'/(name+'_Meshy_V1.blend');bpy.ops.wm.open_mainfile(filepath=str(source));assert not bpy.data.actions;rig=bpy.data.objects[name+'_Rig'];body=bpy.data.objects[name+'_Body'];scene=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0;h=spec['height'];rest={p.name:p.bone.matrix_local.copy()for p in rig.pose.bones};heads={p.name:p.bone.head_local.copy()for p in rig.pose.bones};tails={p.name:p.bone.tail_local.copy()for p in rig.pose.bones};chains=audit['leg_chains'];records={}
def orient(n,head,tail):
 q=(tails[n]-heads[n]).rotation_difference(tail-head);rig.pose.bones[n].matrix=Matrix.Translation(head)@q.to_matrix().to_4x4()@rest[n].to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
def solve(c,target):
 a,b,f=c['upper'],c['lower'],c['foot'];hip=rig.pose.bones[a].head.copy();L=(tails[a]-heads[a]).length;M=(tails[b]-heads[b]).length;delta=target-hip;dist=delta.length;reach_error=max(0.,dist-L-M+1e-6);assert reach_error<h*.002,(name,a,reach_error);dist=min(dist,L+M-1e-6);d=delta.normalized();pole=Vector((0,c['pole'],0));pole=(pole-d*pole.dot(d)).normalized();along=(L*L-M*M+dist*dist)/(2*dist);knee=hip+d*along+pole*math.sqrt(max(0.,L*L-along*along));orient(a,hip,knee);orient(b,knee,hip+d*dist);rig.pose.bones[f].matrix=Matrix.Translation(target-heads[f])@rest[f];bpy.context.view_layer.update();return reach_error
clips={'Idle':(2.,0),'Walk':(.64,spec['walk']),'Run':(.4,spec['run']),'Attack':(.8,0),'Hit':(.4,0),'Faint':(1.2,0),'Happy':(1.,0)}
for role,(duration,speed)in clips.items():
 frames=round(duration*30);duration=frames/30;action=bpy.data.actions.new(name+'_'+role);action.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=action;tracks={c['id']:[]for c in chains};ground=[];maxreach=0.
 for frame in range(frames+1):
  scene.frame_set(frame+1);t=frame/frames;wave=math.sin(math.tau*t);pulse=math.sin(math.pi*t)**2
  for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
  root=rig.pose.bones['root'];pelvis=rig.pose.bones['pelvis'];chest=rig.pose.bones['chest'];head=rig.pose.bones['head']
  if spec['family']=='Floating':
   pelvis.matrix=Matrix.Translation((0,0,h*(.018*wave if role in ['Idle','Walk','Run','Happy']else 0)))@rest['pelvis'];chest.rotation_quaternion=Quaternion((0,0,1),.025*wave)
  elif speed:pelvis.matrix=Matrix.Translation((0,0,-spec.get('run_pelvis_drop_m'if role=='Run'else'walk_pelvis_drop_m',h*(.035 if role=='Run'else .025))+h*.0015*(1+math.cos(2*math.tau*t))))@rest['pelvis'];chest.rotation_quaternion=Quaternion((0,0,1),.012*wave)
  else:chest.scale=(1+.002*wave,1+.002*wave,1+.0015*wave)
  if role=='Idle':head.rotation_quaternion=Quaternion((0,0,1),.008*wave)
  elif role=='Attack':root.matrix=Matrix.Translation((0,-h*.055*pulse,0))@rest['root'];head.rotation_quaternion=Quaternion((1,0,0),.08*pulse)
  elif role=='Hit':root.matrix=Matrix.Translation((0,h*.03*math.sin(math.pi*t),0))@rest['root'];head.rotation_quaternion=Quaternion((1,0,0),-.06*math.sin(math.pi*t))
  elif role=='Faint':
   q=t*t*(3-2*t)
   if spec.get('faint_ground_lock',False):root.matrix=Matrix.Translation((0,h*.05*q,0))@Quaternion((1,0,0),math.radians(82)*q).to_matrix().to_4x4()@rest['root']
   else:root.matrix=Matrix.Translation((h*.04*q,0,h*.20*q))@Quaternion((0,1,0),math.radians(72)*q).to_matrix().to_4x4()@rest['root']
  elif role=='Happy':head.rotation_quaternion=Quaternion((0,0,1),.045*wave)
  bpy.context.view_layer.update()
  for c in chains:
   target=heads[c['foot']].copy()
   if speed:
    phase=(t+c['phase'])%1;duty=.57 if role=='Walk'else .44;travel=speed*duration*duty
    if phase<duty:target.y+=travel*(phase/duty-.5)
    else:u=(phase-duty)/(1-duty);target.y+=travel*(.5-u);target.z+=h*(.018 if role=='Walk'else .035)*math.sin(math.pi*u)**1.5
    maxreach=max(maxreach,solve(c,target));tracks[c['id']].append(dict(phase=phase,stance=phase<duty,ankle=list(rig.pose.bones[c['foot']].head)))
   elif role!='Faint':target+=root.matrix.translation-rest['root'].translation;maxreach=max(maxreach,solve(c,target))
  if 'upperarm_L'in rig.pose.bones:
   for side,sign,offset in [('L',1,0),('R',-1,.5)]:
    for prefix in ['','lower_']if name=='Machomei'else['']:
     arm=prefix+'upperarm_'+side;chest_delta=rig.pose.bones['chest'].matrix.to_3x3()@rest['chest'].to_3x3().inverted();lower=spec.get('arm_lower_radians',.35 if name in ['Pikachu','Enton','Glurak']else .06)
     swing=(.18 if role=='Walk'else .26 if role=='Run'else .015)*math.sin(math.tau*(t+offset)+(math.pi if prefix else 0));q=Quaternion((1,0,0),swing)@Quaternion((0,1,0),sign*lower)
     if role=='Attack':q=Quaternion((0,0,1),sign*-.24*pulse)@q
     direction=chest_delta@(q@(tails[arm]-heads[arm]));start=rig.pose.bones[arm].head.copy();orient(arm,start,start+direction)
  for n in rig.pose.bones.keys():
   p=rig.pose.bones[n]
   if n.startswith('tail_'):p.rotation_quaternion=Quaternion((0,0,1),spec.get('tail_sway_radians',.025)*math.sin(math.tau*t-.4*list(rig.pose.bones.keys()).index(n)))
   elif n.startswith('flame_'):p.rotation_quaternion=Quaternion((1,0,0),.025*math.sin(2*math.tau*t))
   elif n.startswith('ear_'):p.rotation_quaternion=Quaternion((1,0,0),.015*wave)
   elif n.startswith('leaf_'):p.rotation_quaternion=Quaternion((1,0,0),.018*math.sin(math.tau*t+.7*list(rig.pose.bones.keys()).index(n)))
   elif n.startswith('gas_'):p.rotation_quaternion=Quaternion((0,0,1),.025*math.sin(math.tau*t+int(n[-1])*.7))
   elif n.startswith('wing_'):p.rotation_quaternion=Quaternion((0,1,0),.012*wave*(1 if n.endswith('L')else-1))
  bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();low=min(v.co.z for v in mesh.vertices);ev.to_mesh_clear()
  if role=='Faint'and (low<0 or spec.get('faint_ground_lock',False)):m=root.matrix.copy();m.translation.z-=low;root.matrix=m;bpy.context.view_layer.update();low=0.
  ground.append(low)
  for p in rig.pose.bones:
   for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=frame+1,group=p.name)
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
 drift=[]
 for rows in tracks.values():
  for a,b in zip(rows,rows[1:]):
   if a['stance']and b['stance']and b['phase']>a['phase']:drift.append(abs(b['ankle'][1]-a['ankle'][1]-speed/30))
 assert max(drift,default=0)<.00005;assert min(ground)>-h*.04,(name,role,min(ground))
 records[role]=dict(frames=frames+1,duration_s=duration,speed_cm_s=speed*100,foot_stance_increment_error_m=max(drift,default=0),max_unreachable_m=maxreach,min_z_m=min(ground),max_min_z_m=max(ground),foot_tracks=tracks)
 scene.frame_start=1;scene.frame_end=frames+1;scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(True);bpy.context.view_layer.objects.active=rig;dest=A/'Exports/MeshyV1'/(name+'_'+role+'.fbx');assert not dest.exists()or '--revise-generated'in sys.argv;bpy.ops.export_scene.fbx(filepath=str(dest),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO');print('CLIP_EXPORTED',name,role,flush=True)
rig.animation_data.action=bpy.data.actions[name+'_Idle'];scene.frame_start=1;scene.frame_end=61;scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(source));(A/'MeshyV1_AnimationAudit.json').write_text(json.dumps(records,indent=2));print('ANIMATED',name,flush=True)
