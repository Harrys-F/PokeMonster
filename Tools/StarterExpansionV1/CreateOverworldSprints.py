"""Separate companion-only sprint clips; never save over existing models or battle animations."""
import bpy,math,json,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2]
for species,model,rig_name,body_name,speed,duty,crouch,center_y in [('Zunderlauf','Glumanda_Meshy_V11.blend','Glumanda_Meshy_Rig','Glumanda_Meshy',1.8,.16,0.,.012),('Schiggy','Schiggy_Meshy_V1.blend','Schiggy_Rig','Schiggy_Body',1.6,.13,0.,-.030),('Bisasam','Bisasam_Meshy_V1.blend','Bisasam_Rig','Bisasam_Body',1.8,.20,.030,None)]:
 A=R/'Art/Characters/Creatures'/species;source=A/'Source'/model;before=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0;rig=bpy.data.objects[rig_name];body=bpy.data.objects[body_name];s=bpy.context.scene;s.render.fps=60;rest={p.name:p.bone.matrix_local.copy()for p in rig.pose.bones};heads={p.name:p.bone.head_local.copy()for p in rig.pose.bones};tails={p.name:p.bone.tail_local.copy()for p in rig.pose.bones}
 chains=json.loads((A/'MeshyV1_ModelAudit.json').read_text())['leg_chains']if species!='Zunderlauf'else[dict(id=side,upper='thigh_'+side,lower='shin_'+side,foot='foot_'+side,pole=-1,phase=phase)for side,phase in [('L',0),('R',.5)]]
 export=A/'Exports/OverworldV1'/(species+'_Sprint.fbx');library=A/'Source'/(species+'_OverworldSprint_V1.blend');assert(not export.exists()and not library.exists())or '--revise-generated'in sys.argv;export.parent.mkdir(parents=True,exist_ok=True);old_run=bpy.data.actions[('Glumanda'if species=='Zunderlauf'else species)+'_Run'];action=bpy.data.actions.new(species+'_OverworldSprint');action.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=action;tracks={c['id']:[]for c in chains};ground=[]
 def orient(n,h,t):q=(tails[n]-heads[n]).rotation_difference(t-h);rig.pose.bones[n].matrix=Matrix.Translation(h)@q.to_matrix().to_4x4()@rest[n].to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
 for frame in range(31):
  t=frame/30;old_frame=old_run.frame_range[0]+t*(old_run.frame_range[1]-old_run.frame_range[0]);rig.animation_data.action=old_run;s.frame_set(int(old_frame),subframe=old_frame-int(old_frame));bpy.context.view_layer.update();secondary={p.name:p.matrix_basis.copy()for p in rig.pose.bones if p.name.startswith('tail_')or p.name=='bulb'};rig.animation_data.action=action;s.frame_set(frame+1);wave=math.sin(math.tau*t)
  for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
  half=t%.5;flight=math.sin(math.pi*(half-duty)/(.5-duty))if half>duty else 0.;root=rig.pose.bones['root'];root.matrix=Matrix.Translation((0,0,.030*flight))@rest['root'];bpy.context.view_layer.update();rig.pose.bones['pelvis'].location.y=0;rig.pose.bones['pelvis'].matrix=Matrix.Translation((0,0,-crouch))@rig.pose.bones['pelvis'].matrix;bpy.context.view_layer.update()
  rig.pose.bones['chest'].rotation_quaternion=Quaternion((0,0,1),.012*wave);rig.pose.bones['head'].rotation_quaternion=Quaternion((0,0,1),-.010*wave);bpy.context.view_layer.update()
  for c in chains:
   phase=(t+c['phase'])%1;foot=c['foot'];ankle=heads[foot].copy();ankle.y=center_y if center_y is not None else ankle.y;travel=speed*.5*duty
   if phase<duty:ankle.y+=travel*(phase/duty-.5)
   else:u=(phase-duty)/(1-duty);ankle.y+=travel*(.5-u);ankle.z+=.060*math.sin(math.pi*u)**1.3
   a,b=c['upper'],c['lower'];hip=rig.pose.bones[a].head.copy();L=(tails[a]-heads[a]).length;M=(tails[b]-heads[b]).length;delta=ankle-hip;dist=delta.length;assert abs(L-M)+1e-5<dist<L+M-1e-5,(species,a,frame,dist,L+M);d=delta.normalized();pole=Vector((0,c['pole'],0));pole=(pole-d*pole.dot(d)).normalized();along=(L*L-M*M+dist*dist)/(2*dist);knee=hip+d*along+pole*math.sqrt(max(0,L*L-along*along));orient(a,hip,knee);orient(b,knee,ankle);rig.pose.bones[foot].matrix=Matrix.Translation(ankle-heads[foot])@rest[foot];bpy.context.view_layer.update();tracks[c['id']].append({'phase':phase,'stance':phase<duty,'ankle':list(rig.pose.bones[foot].head)})
  if species!='Bisasam':
   chest_delta=rig.pose.bones['chest'].matrix.to_3x3()@rest['chest'].to_3x3().inverted()
   for side,sign,offset in [('L',1,0),('R',-1,.5)]:
    swing=.16*math.sin(math.tau*(t+offset))
    for prefix in ['upperarm_','forearm_','hand_']:
     n=prefix+side;direction=Vector((sign*.48,-.08+swing,-.874))if species=='Zunderlauf'else(tails[n]-heads[n]).normalized()+Vector((0,swing,-.12));h=rig.pose.bones[n].head.copy();orient(n,h,h+chest_delta@direction.normalized()*(tails[n]-heads[n]).length)
  for n,matrix in secondary.items():rig.pose.bones[n].matrix_basis=matrix
  bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();ground.append(min(v.co.z for v in m.vertices));ev.to_mesh_clear()
  for p in rig.pose.bones:
   for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=frame+1,group=p.name)
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for f in bag.fcurves:
     for key in f.keyframe_points:key.interpolation='LINEAR'
 errors=[]
 for rows in tracks.values():
  for a,b in zip(rows,rows[1:]):
   if a['stance']and b['stance']and b['phase']>a['phase']:errors.append(abs(b['ankle'][1]-a['ankle'][1]-speed/60))
 assert max(errors)<.00005;assert min(ground)>-.012,(species,min(ground));s.frame_start=1;s.frame_end=31;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
 bpy.ops.export_scene.fbx(filepath=str(export),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO')
 # Save a small, genuinely editable rig/action scene. No duplicate model or packed images.
 for obj in list(bpy.data.objects):
  if obj!=rig:bpy.data.objects.remove(obj,do_unlink=True)
 for other in list(bpy.data.actions):
  if other!=action:bpy.data.actions.remove(other)
 for material in list(bpy.data.materials):bpy.data.materials.remove(material)
 for image in list(bpy.data.images):bpy.data.images.remove(image)
 for mesh in list(bpy.data.meshes):bpy.data.meshes.remove(mesh)
 s.name=species+'_SprintSource';s['ReferenceModel']=str(source.relative_to(R));s['Purpose']='Companion-only rig/action; append the unchanged reference model for skin review';s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
 bpy.ops.wm.save_as_mainfile(filepath=str(library))
 result={'species':species,'reference_source':str(source.relative_to(R)),'reference_source_sha256':before,'rig_action_source':str(library.relative_to(R)),'fbx':str(export.relative_to(R)),'duration':.5,'fps':60,'reference_speed_cm_s':speed*100,'stance_fraction':duty,'stance_increment_error_max_m':max(errors),'mesh_min_z_m':min(ground),'foot_tracks':tracks,'battle_animations_unchanged':True};(A/'OverworldSprint_AnimationAudit.json').write_text(json.dumps(result,indent=2));assert hashlib.sha256(source.read_bytes()).hexdigest()==before;print('OVERWORLD_SPRINT_EXPORTED',species,min(ground),max(errors),flush=True)
