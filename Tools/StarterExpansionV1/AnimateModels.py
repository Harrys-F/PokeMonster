"""Species-fitted stance IK: short biped steps, four-beat quadruped walk and diagonal run."""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2]
for species in ['Schiggy','Bisasam']:
 A=R/'Art/Characters/Creatures'/species;audit=json.loads((A/'MeshyV1_ModelAudit.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(A/'Source'/(species+'_Meshy_V1.blend')));bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;rig=bpy.data.objects[species+'_Rig'];body=bpy.data.objects[species+'_Body'];rest={p.name:p.bone.matrix_local.copy()for p in rig.pose.bones};heads={p.name:p.bone.head_local.copy()for p in rig.pose.bones};tails={p.name:p.bone.tail_local.copy()for p in rig.pose.bones};chains=audit['leg_chains'];quadruped=species=='Bisasam';result={}
 if bpy.data.actions:
  assert '--revise-generated' in sys.argv,'Explicit revision required for generated working source'
  assert all(a.name in {species+'_'+n for n in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']}for a in bpy.data.actions)
  rig.animation_data_clear()
  for a in list(bpy.data.actions):bpy.data.actions.remove(a)
 # Lock the actual sole vertices, including the inner foot edge, to the fitted foot.
 # Original triangles/UVs/normals are untouched; only this newly generated skin is refined.
 for v in body.data.vertices:
  x,y,z=v.co;side='L'if x>=0 else'R'
  if z>=.080 or abs(x)<.03 or (not quadruped and y>.075):continue
  foot=(('front_'if y<.015 else'hind_')+side+'_foot')if quadruped else'foot_'+side
  t=max(0.,min(1.,(.080-z)/.035));t=t*t*(3-2*t)
  weights={body.vertex_groups[g.group].name:g.weight*(1-t)for g in v.groups};weights[foot]=weights.get(foot,0)+t
  for g in body.vertex_groups:g.remove([v.index])
  total=sum(weights.values())
  for n,value in weights.items():
   if value>1e-7:body.vertex_groups[n].add([v.index],value/total,'REPLACE')
 def orient(n,h,t):
  q=(tails[n]-heads[n]).rotation_difference(t-h);rig.pose.bones[n].matrix=Matrix.Translation(h)@q.to_matrix().to_4x4()@rest[n].to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
 def solve(c,target):
  a,b,f=c['upper'],c['lower'],c['foot'];hip=rig.pose.bones[a].head.copy();L=(tails[a]-heads[a]).length;M=(tails[b]-heads[b]).length;delta=target-hip;dist=delta.length;assert dist<L+M-1e-6,(species,a,dist,L+M);d=delta.normalized();pole=Vector((0,c['pole'],0));pole=(pole-d*pole.dot(d)).normalized();along=(L*L-M*M+dist*dist)/(2*dist);knee=hip+d*along+pole*math.sqrt(max(0.,L*L-along*along));orient(a,hip,knee);orient(b,knee,target);rig.pose.bones[f].matrix=Matrix.Translation(target-heads[f])@rest[f];bpy.context.view_layer.update()
 clips={'Idle':(2.,0),'Walk':(.6,audit['walk_speed_m_s']),'Run':(.4,audit['run_speed_m_s']),'Attack':(.8,0),'Hit':(.4,0),'Faint':(1.2,0),'Happy':(1.,0)}
 for name,(duration,speed)in clips.items():
  n=round(duration*30);duration=n/30;action=bpy.data.actions.new(species+'_'+name);action.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=action;ground=[];positions={c['id']:[]for c in chains};reach=[]
  for frame in range(n+1):
   s.frame_set(frame+1);t=frame/n;wave=math.sin(math.tau*t)
   for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
   root=rig.pose.bones['root'];pelvis=rig.pose.bones['pelvis'];chest=rig.pose.bones['chest'];head=rig.pose.bones['head'];pulse=math.sin(math.pi*t)**2
   if speed:
    pelvis.matrix=Matrix.Translation((0,0,-.010+.0004*(1+math.cos(2*math.tau*t))))@rest['pelvis'];chest.rotation_quaternion=Quaternion((0,0,1),.007*wave);head.rotation_quaternion=Quaternion((0,0,1),-.005*wave)
   elif name=='Idle':chest.scale=(1+.002*wave,1+.002*wave,1+.0015*wave);head.rotation_quaternion=Quaternion((0,0,1),.008*wave)
   elif name=='Attack':root.matrix=Matrix.Translation((0,-.025*pulse,0))@rest['root'];head.rotation_quaternion=Quaternion((1,0,0),.10*pulse)
   elif name=='Hit':root.matrix=Matrix.Translation((0,.015*math.sin(math.pi*t),0))@rest['root'];head.rotation_quaternion=Quaternion((1,0,0),-.08*math.sin(math.pi*t))
   elif name=='Faint':q=t*t*(3-2*t);root.matrix=Matrix.Translation((.025*q,0,.10*q))@Quaternion((0,1,0),math.radians(75)*q).to_matrix().to_4x4()@rest['root']
   elif name=='Happy':head.rotation_quaternion=Quaternion((0,0,1),.055*wave);chest.scale=(1+.007*pulse,1+.004*pulse,1+.005*pulse)
   bpy.context.view_layer.update()
   for c in chains:
    target=heads[c['foot']].copy()
    if speed:
     offset=c['phase']
     if quadruped and name=='Walk':offset={'front_L':0.,'hind_R':.25,'front_R':.5,'hind_L':.75}[c['id']]
     phase=(t+offset)%1.;duty=.60 if name=='Walk'and quadruped else .55 if name=='Walk'else .42;travel=speed*duration*duty;target.y=heads[c['foot']].y
     if phase<duty:target.y+=travel*(phase/duty-.5)
     else:u=(phase-duty)/(1-duty);target.y+=travel*(.5-u);target.z+=(.010 if name=='Walk'else .018)*math.sin(math.pi*u)**1.5
     solve(c,target);positions[c['id']].append({'phase':phase,'stance':phase<duty,'ankle':list(rig.pose.bones[c['foot']].head)})
    elif name!='Faint':target+=root.matrix.translation-rest['root'].translation;solve(c,target)
   if not quadruped:
    chest_delta=rig.pose.bones['chest'].matrix.to_3x3()@rest['chest'].to_3x3().inverted()
    for side,sign,phase_offset in [('L',1,0),('R',-1,.5)]:
     swing=math.sin(math.tau*(t+phase_offset))*(.12 if name=='Walk'else .20 if name=='Run'else .01)
     for prefix in ['upperarm_','forearm_','hand_']:
      bn=prefix+side;direction=(tails[bn]-heads[bn]).normalized()+Vector((0,swing,-.12));h=rig.pose.bones[bn].head.copy();orient(bn,h,h+chest_delta@direction.normalized()*(tails[bn]-heads[bn]).length)
    rig.pose.bones['tail_base'].rotation_quaternion=Quaternion((0,0,1),.025*wave);rig.pose.bones['tail_tip'].rotation_quaternion=Quaternion((0,0,1),.035*math.sin(math.tau*t-.4))
   else:rig.pose.bones['bulb'].rotation_quaternion=Quaternion((0,0,1),(.007 if name=='Idle'else .014)*math.sin(math.tau*t-.5))
   bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();low=min(v.co.z for v in mesh.vertices);ev.to_mesh_clear()
   if name=='Faint'and low<0:matrix=root.matrix.copy();matrix.translation.z-=low;root.matrix=matrix;bpy.context.view_layer.update();low=0.
   ground.append(low)
   for p in rig.pose.bones:
    for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=frame+1,group=p.name)
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for f in bag.fcurves:
      for key in f.keyframe_points:key.interpolation='LINEAR'
  drift=[]
  for rows in positions.values():
   for a,b in zip(rows,rows[1:]):
    if a['stance']and b['stance']and b['phase']>a['phase']:drift.append(abs(b['ankle'][1]-a['ankle'][1]-speed/30))
  result[name]={'frames':n+1,'duration_s':duration,'authored_speed_cm_s':speed*100,'stance_increment_error_m':max(drift,default=0.),'mesh_min_z_m':min(ground),'mesh_max_min_z_m':max(ground),'foot_tracks':positions}
  assert not speed or max(drift)<.00005,result[name]
  assert min(ground)>-.015,(species,name,min(ground))
  s.frame_start=1;s.frame_end=n+1;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(True);bpy.context.view_layer.objects.active=rig
  dest=A/'Exports/MeshyV1'/(species+'_'+name+'.fbx');assert not dest.exists()or '--revise-generated'in sys.argv;bpy.ops.export_scene.fbx(filepath=str(dest),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO')
 rig.animation_data.action=bpy.data.actions[species+'_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(A/'Source'/(species+'_Meshy_V1.blend')));(A/'MeshyV1_AnimationAudit.json').write_text(json.dumps(result,indent=2));print('STARTER_ANIMATED',species,json.dumps({n:{k:v for k,v in d.items()if k!='foot_tracks'}for n,d in result.items()}),flush=True)
