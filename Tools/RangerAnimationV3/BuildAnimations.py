"""V3: anatomical knee pole and sagittal, close-set foot trajectories.
No original mesh, UV, source, material, V2 rig or animation is overwritten.
"""
import bpy,math,json,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
R=Path('/Users/harry/Developer/PokeMonster')
C=R/'Art/Characters/NPCs/Ranger';O=C/'Review/AnimationV3';E=C/'Exports/AnimationV3'
s=bpy.context.scene;r=s.objects['Ranger_Pilot_Rig'];pb=r.pose.bones
out=C/'Source/Ranger_NPC_AnimationQuality_V3.blend'
assert bpy.app.background and Path(bpy.data.filepath).name=='Ranger_NPC_AnimationQuality_V2.blend'
assert not out.exists()
models=[s.objects[n] for n in ['Ranger_Runtime_Pilot','Ranger_V2_LOD0','Ranger_V2_LOD1']]
run=models[1]
original={o.name:hashlib.sha256(np.array([v.co[:] for v in o.data.vertices],np.float32).tobytes()).hexdigest() for o in models}
for p in pb:p.rotation_mode='QUATERNION'
r.animation_data.action=None;r.data.pose_position='POSE';s.render.fps=60
for o in models:
 for m in o.modifiers:
  if m.type=='ARMATURE':m.use_deform_preserve_volume=False
def rot(n,axis,a):
 q=r.data.bones[n].matrix_local.to_quaternion()
 pb[n].rotation_quaternion=(q.inverted()@Quaternion(axis,a)@q)@pb[n].rotation_quaternion
def solve(side,ankle,pitch):
 bpy.context.view_layer.update()
 hip=pb['thigh_'+side].head.copy();a=r.data.bones['thigh_'+side];b=r.data.bones['shin_'+side]
 l1,l2=a.length,b.length;delta=ankle-hip;length=delta.length
 assert length<l1+l2,('Unreachable ankle',side,length,l1+l2)
 dr=delta/length;along=(l1*l1-l2*l2+length*length)/(2*length)
 # Character forward is -Y in Blender. Project the anatomical knee pole onto
 # the plane normal to hip-ankle; V2 used the opposite (rearward) pole.
 pole=Vector((0,-1,0));perp=(pole-dr*pole.dot(dr)).normalized()
 knee=hip+dr*along+perp*math.sqrt(max(0,l1*l1-along*along))
 tail=Quaternion((1,0,0),pitch)@Vector((0,-.155,-.060))
 for n,h,t in [('thigh_'+side,hip,knee),('shin_'+side,knee,ankle),('foot_'+side,ankle,ankle+tail)]:
  rest=r.data.bones[n];delta=(rest.tail_local-rest.head_local).rotation_difference(t-h)
  pb[n].matrix=Matrix.Translation(h)@delta.to_matrix().to_4x4()@rest.matrix_local.to_3x3().to_4x4()
  bpy.context.view_layer.update()
 return hip,knee
def smooth(t):return t*t*t*(10+t*(-15+6*t))
footids={side:[v.index for v in run.data.vertices if v.co.z<.145 and (v.co.x>0)==(side=='l')] for side in ['l','r']}
clips=[('Idle',181,3.),('Walk',49,.8),('Talk',181,3.),('TurnLeft',61,1.),('TurnRight',61,1.)]
checks=[]
for kind,count,duration in clips:
 act=bpy.data.actions.new('A_Ranger_'+kind+'_AQV3');act.use_fake_user=True
 # Leave the action detached while authoring each frame, preventing dependency
 # updates from re-evaluating the existing animation over newly assigned poses.
 r.animation_data.action=None
 contacts=[];floor=100.
 for f in range(1,count+1):
  s.frame_set(f);t=(f-1)/(count-1);ph=2*math.pi*t;walk=kind=='Walk';turn=kind.startswith('Turn')
  for p in pb:p.location=(0,0,0);p.rotation_quaternion=Quaternion();p.scale=(1,1,1)
  # Small lateral transfer, a lowered relaxed pelvis, no exaggerated bounce.
  pb['pelvis'].location=(.008*math.sin(ph) if walk else 0.,-.078+(.003*math.cos(2*ph) if walk else 0.),0.)
  rot('pelvis',(0,0,1),.025*math.sin(ph) if walk else 0.)
  rot('chest',(0,0,1),-.040*math.sin(ph) if walk else 0.)
  rot('chest',(1,0,0),.012+(.003*math.sin(ph) if not walk else 0.))
  rot('head',(1,0,0),-.006+.002*math.sin(ph))
  for side,sign in [('l',1),('r',-1)]:
   a=ph+(0 if sign==1 else math.pi);q=r.data.bones['upperarm_'+side].matrix_local.to_quaternion()
   # Opposite arm to the advancing leg, restrained elbow flexion.
   swing=.12*math.cos(a) if walk else .002*math.sin(a)
   pb['upperarm_'+side].rotation_quaternion=q.inverted()@Quaternion((1,0,0),swing)@Quaternion((0,1,0),sign*math.radians(73))@q
   rot('lowerarm_'+side,(0,1,0),sign*math.radians(10))
   if kind=='Talk':
    g=math.sin(math.pi*t)**2;rot('lowerarm_l',(1,0,0),-.22*g);rot('upperarm_l',(1,0,0),.045*g)
   u=(t+(0 if sign==1 else .5))%1.;stance=u<.5
   forward=0.;lift=0.;pitch=0.
   if walk:
    if stance:forward=.30-1.20*u
    else:
     v=(u-.5)*2;forward=-.30-.60*v+1.20*smooth(v)
     lift=.055*math.sin(math.pi*v)**2;pitch=-.12*math.sin(math.pi*v)
   elif turn:
    # Alternating short lifts; separate mirrored step arcs for each direction.
    v=(u-.5)*2 if not stance else 0.
    lift=.024*math.sin(math.pi*v)**2 if not stance else 0.
    direction=1 if kind=='TurnLeft' else -1
    forward=direction*sign*.025*math.sin(ph)
   ankle=Vector((sign*.145,-.035-forward,.115+lift))
   hip,knee=solve(side,ankle,pitch)
   # Move the entire solved chain for sole clearance, rather than translating
   # the foot alone away from the shin as V2's post-pass did.
   ev=run.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
   low=min(me.vertices[i].co.z for i in footids[side]);ev.to_mesh_clear()
   if low<.0005:ankle.z+=.0005-low;hip,knee=solve(side,ankle,pitch)
   contacts.append({'frame':f,'side':side,'stance':stance if walk else not turn,'ankle':list(ankle),'hip':list(hip),'knee':list(knee),'pole_forward':knee.y-(hip.y+ankle.y)*.5})
  if kind=='Talk':rot('head',(0,0,1),.024*math.sin(ph))
  # Keep V2 secondary mechanism, with smaller baked amplitudes. Weight changes
  # are deferred until the corrected legs have passed the first visual review.
  rot('cape_upper',(1,0,0),-.020-(.012*math.sin(2*ph-.6) if walk else 0))
  for n,off in [('cape_lower',.8),('cape_l',.5),('cape_r',1.1)]:
   rot(n,(1,0,0),-.010-(.014*math.sin(2*ph-off) if walk else 0))
  rot('bag',(1,0,0),.010*math.sin(ph-.5) if walk else .001*math.sin(ph))
  bpy.context.view_layer.update();ev=run.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();floor=min(floor,min(v.co.z for v in me.vertices));ev.to_mesh_clear()
  # Temporarily attach only for key insertion; detach before next dependency update.
  r.animation_data.action=act
  for p in pb:
   p.keyframe_insert(data_path='location',frame=f,group=p.name)
   p.keyframe_insert(data_path='rotation_quaternion',frame=f,group=p.name)
  r.animation_data.action=None
 for layer in act.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
 checks.append({'clip':kind,'frames':count,'duration':duration,'minimum_z_m':floor,'contacts':contacts})
 print('CLIP_DONE',kind,floor,flush=True)
for o in s.objects:
 if o.type=='MESH':o.hide_render=o!=run;o.hide_set(o!=run)
for im in bpy.data.images:
 if im.source=='FILE' and im.users and not im.packed_file:im.pack()
r.animation_data.action=bpy.data.actions['A_Ranger_Idle_AQV3'];s.frame_start=1;s.frame_end=181;s.frame_set(1)
s['source_file']='Ranger_NPC_AnimationQuality_V2.blend';s['authored_walk_speed_cm_s']=150.;s['status']='V3 anatomical correction candidate; not approved'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
kw=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
for idx,obj in enumerate(models[1:]):
 for o in s.objects:o.select_set(False)
 r.select_set(True);obj.hide_set(False);obj.select_set(True);bpy.context.view_layer.objects.active=r;r.data.pose_position='REST'
 bpy.ops.export_scene.fbx(filepath=str(E/('SK_Ranger_AQV3_LOD'+str(idx)+'.fbx')),bake_anim=False,**kw)
r.data.pose_position='POSE'
for o in s.objects:o.select_set(False)
r.select_set(True);run.select_set(True);bpy.context.view_layer.objects.active=r
for kind,count,duration in clips:
 r.animation_data.action=bpy.data.actions['A_Ranger_'+kind+'_AQV3'];s.frame_start=1;s.frame_end=count;s.frame_set(1)
 bpy.ops.export_scene.fbx(filepath=str(E/('A_Ranger_'+kind+'_AQV3.fbx')),bake_anim=True,**kw)
audit={'source':s['source_file'],'file':str(out),'bones':len(r.data.bones),'geometry_unchanged':all(original[o.name]==hashlib.sha256(np.array([v.co[:] for v in o.data.vertices],np.float32).tobytes()).hexdigest() for o in models),'weights_unchanged':True,'clips':checks,'walk_speed_cm_s':150,'cycle_seconds':.8,'stride_pair_m':1.2,'foot_track_width_m':.29,'knee_pole_blender':[0,-1,0]}
(O/'Data/BlenderAnimationAudit.json').write_text(json.dumps(audit,indent=2))
s.render.engine='CYCLES';s.cycles.samples=8;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=720;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.camera.data.type='ORTHO';s.camera.data.ortho_scale=2.1
for o in s.objects:
 if o.type=='MESH':o.hide_render=o!=run
for label,kind,fr,loc in [('Idle_Front','Idle',1,(0,-5,.9)),('Walk_Contact','Walk',1,(3,-5,1.9)),('Walk_0225','Walk',14.5,(3,-5,1.9)),('Walk_Side','Walk',14.5,(5,0,.9)),('Walk_Opposite','Walk',25,(3,-5,1.9)),('Cape_Back','Walk',14.5,(3,5,1.9))]:
 r.animation_data.action=bpy.data.actions['A_Ranger_'+kind+'_AQV3'];s.frame_set(int(fr),subframe=fr-int(fr));s.camera.location=loc;s.camera.rotation_euler=(Vector((0,0,.9))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/'Blender'/(label+'.png'));bpy.ops.render.render(write_still=True)
print('V3_SOURCE_COMPLETE',flush=True)
