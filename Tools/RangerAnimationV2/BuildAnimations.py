"""Independent Ranger work copy. No edits to V1/player or live Blender scene."""
import bpy,math,json,numpy as np,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');C=R/'Art/Characters/NPCs/Ranger';O=C/'Review/AnimationV2';E=C/'Exports/AnimationV2';s=bpy.context.scene
assert bpy.app.background and Path(bpy.data.filepath).name=='Ranger_NPC_V2_Protected.blend'
out=C/'Source/Ranger_NPC_AnimationQuality_V2.blend';assert not out.exists()
rig=s.objects['Ranger_Pilot_Rig'];models=[s.objects[n] for n in ['Ranger_Runtime_Pilot','Ranger_V2_LOD0','Ranger_V2_LOD1']];run=models[1];rig.animation_data.action=None;rig.data.pose_position='REST'
# All changes occur in a new .blend. Retain source geometry, UVs and materials, no simplification.
geom={o.name:hashlib.sha256(np.array([v.co[:] for v in o.data.vertices],np.float32).tobytes()).hexdigest() for o in models}
for o in s.objects:o.select_set(False)
rig.hide_set(False);rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
for side,sg in [('l',1),('r',-1)]:
 for n,h,t in [('thigh',(sg*.13,-.035,.91),(sg*.195,-.045,.48)),('shin',(sg*.195,-.045,.48),(sg*.235,-.035,.115)),('foot',(sg*.235,-.035,.115),(sg*.235,-.19,.055))]:
  b=rig.data.edit_bones[n+'_'+side];b.head=h;b.tail=t
 b=rig.data.edit_bones.new('cape_'+side);b.head=(sg*.20,.13,.98);b.tail=(sg*.30,.19,.25);b.parent=rig.data.edit_bones['cape_upper']
b=rig.data.edit_bones['bag'];b.head=(.26,-.19,.93);b.tail=(.27,-.20,.76)
bpy.ops.object.mode_set(mode='OBJECT')
def smooth(a,b,x):
 t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)
counts={}
for obj in models:
 groups={g.name:g for g in obj.vertex_groups}
 for n in ['cape_l','cape_r']:
  if n not in groups:groups[n]=obj.vertex_groups.new(name=n)
 changed=0;cape=0;bags=0
 for v in obj.data.vertices:
  x,y,z=v.co;ax=abs(x);side='l' if x>0 else 'r'
  old={obj.vertex_groups[g.group].name:g.weight for g in v.groups}
  if old.get('back_sword',0)>.5:continue
  # Preserve previously repaired sleeve/hand weights; soften shoulder attachment only.
  if ax>.18 and z>1.18 and (y<.035 or ax>.48):
   w=old
  elif z>1.48:w=old
  else:
   if z>.97:
    t=smooth(1.04,1.34,z);w={'spine':1-t,'chest':t}
   elif z>.80:
    t=smooth(.86,1.01,z);w={'pelvis':1-t,'spine':t}
   else:
    hip=smooth(.73,.88,z);k=smooth(.39,.56,z);ank=smooth(.11,.22,z)
    w={'pelvis':hip,'thigh_'+side:(1-hip)*k,'shin_'+side:(1-hip)*(1-k)*ank,'foot_'+side:(1-hip)*(1-k)*(1-ank)}
   # Spatial cape envelope excludes boots and the anterior leg cross-section.
   cf=smooth(.045,.095,y)*(1-smooth(1.32,1.47,z))*smooth(.145,.21,z)
   cf=max(cf,smooth(.275,.34,ax)*smooth(-.09,.03,y)*(1-smooth(1.18,1.32,z))*smooth(.16,.23,z))
   if cf>.001:
    upper=smooth(.68,1.32,z);lateral=smooth(.06,.25,ax)
    cw={'cape_upper':upper,'cape_lower':(1-upper)*(1-lateral),'cape_'+side:(1-upper)*lateral}
    w={n:q*(1-cf) for n,q in w.items()}
    for n,q in cw.items():w[n]=w.get(n,0)+q*cf
    cape+=1
   # Hip pouch only; belt/strap attachment above .94m stays with pelvis.
   bf=smooth(.205,.255,x)*(1-smooth(.915,.965,z))*smooth(.735,.78,z)*(1-smooth(-.145,-.09,y))
   if bf>.001:
    w={n:q*(1-bf) for n,q in w.items()};w['bag']=w.get('bag',0)+bf;bags+=1
  w={n:q for n,q in w.items() if q>1e-5};total=sum(w.values());assert total>0
  for g in groups.values():g.remove([v.index])
  for n,q in w.items():groups[n].add([v.index],q/total,'REPLACE')
  changed+=1
 counts[obj.name]={'reweighted_vertices':changed,'cape_region':cape,'bag_region':bags,'triangles':len(obj.data.polygons),'vertices':len(obj.data.vertices)}
 # FBX/Unreal linear skinning is the reference, not Blender-only dual quaternion.
 for m in obj.modifiers:
  if m.type=='ARMATURE':m.use_deform_preserve_volume=False
pb=rig.pose.bones
for p in pb:p.rotation_mode='QUATERNION'
rig.data.pose_position='POSE';s.render.fps=60

def rot(n,axis,a):
 q=rig.data.bones[n].matrix_local.to_quaternion();pb[n].rotation_quaternion=(q.inverted()@Quaternion(axis,a)@q)@pb[n].rotation_quaternion

def solve(side,ankle,angle):
 bpy.context.view_layer.update();hip=pb['thigh_'+side].head.copy();a=rig.data.bones['thigh_'+side];b=rig.data.bones['shin_'+side];l1=a.length;l2=b.length;d=ankle-hip;length=min(d.length,l1+l2-.0004);dr=d.normalized();along=(l1*l1-l2*l2+length*length)/(2*length)
 perp=Vector((0,-dr.z,dr.y)).normalized();knee=hip+dr*along+perp*math.sqrt(max(0,l1*l1-along*along))
 tail=Quaternion((1,0,0),angle)@Vector((0,-.155,-.060))
 for n,h,t in [('thigh_'+side,hip,knee),('shin_'+side,knee,ankle),('foot_'+side,ankle,ankle+tail)]:
  b=rig.data.bones[n];q=(b.tail_local-b.head_local).rotation_difference(t-h);pb[n].matrix=Matrix.Translation(h)@q.to_matrix().to_4x4()@b.matrix_local.to_3x3().to_4x4();bpy.context.view_layer.update()
footids={side:[v.index for v in run.data.vertices if v.co.z<.145 and (v.co.x>0)==(side=='l')] for side in ['l','r']}
clips=[('Idle',181,3.),('Walk',55,.9),('Talk',181,3.),('TurnLeft',49,.8),('TurnRight',49,.8)]
checks=[]
for kind,count,duration in clips:
 act=bpy.data.actions.new('A_Ranger_'+kind+'_AQV2');act.use_fake_user=True;rig.animation_data.action=act;floor=100.;contact=[]
 for f in range(1,count+1):
  t=(f-1)/(count-1);ph=t*2*math.pi;walk=kind=='Walk';turn=kind.startswith('Turn');sg=1 if kind=='TurnLeft' else -1
  for p in pb:p.location=(0,0,0);p.rotation_quaternion=Quaternion()
  if walk or turn:
   # Pelvis local Y is world Z. Keep short, low-amplitude motion and alternating contacts.
   pb['pelvis'].location=(.009*math.sin(ph),-.061+.004*math.cos(2*ph),0)
   rot('pelvis',(0,0,1),.035*math.sin(ph));rot('spine',(0,0,1),-.026*math.sin(ph));rot('chest',(0,0,1),-.025*math.sin(ph));rot('chest',(1,0,0),.018)
  else:rot('chest',(1,0,0),.004*math.sin(ph));rot('head',(1,0,0),-.003*math.sin(ph))
  rot('cape_upper',(1,0,0),-.015-(.025+.012*math.sin(2*ph-.6) if walk else 0))
  for n,off in [('cape_lower',.8),('cape_l',.5),('cape_r',1.1)]:
   rot(n,(1,0,0),-.012-(.018+.018*math.sin(2*ph-off) if walk else 0));rot(n,(0,1,0),.014*math.sin(ph-off) if walk else 0)
  rot('bag',(1,0,0),.022*math.sin(ph-.5) if walk else .002*math.sin(ph))
  for side,sign in [('l',1),('r',-1)]:
   a=ph+(0 if sign==1 else math.pi);q=rig.data.bones['upperarm_'+side].matrix_local.to_quaternion()
   pb['upperarm_'+side].rotation_quaternion=q.inverted()@Quaternion((1,0,0),.16*math.cos(a) if walk else .003*math.sin(a))@Quaternion((0,1,0),sign*math.radians(74))@q
   rot('lowerarm_'+side,(0,1,0),sign*math.radians(9))
   if walk or turn:
    u=(t+(0 if sign==1 else .5))%1
    if u<.5:forward=.675*(.5-2*u);lift=0;angle=.055*(1-4*u)
    else:
     v=(u-.5)*2;forward=-.3375+.675*(v*v*(3-2*v));lift=.067*math.sin(math.pi*v)**2;angle=-.18*math.sin(math.pi*v)
    if turn:forward*=.18;lift*=.7
    ankle=Vector((sign*.225,-.035-forward,.115+lift));solve(side,ankle,angle)
   if kind=='Talk':
    gesture=math.sin(math.pi*t)**2;rot('lowerarm_l',(1,0,0),-.28*gesture);rot('upperarm_l',(1,0,0),.06*gesture);rot('head',(0,0,1),.035*math.sin(ph));rot('head',(1,0,0),.012*math.sin(2*ph))
  # Enforce the real sole, evaluated with linear skinning, at each exported sample.
  bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=run.evaluated_get(dg);me=ev.to_mesh();lows={side:min(me.vertices[i].co.z for i in ids) for side,ids in footids.items()};ev.to_mesh_clear()
  for side,low in lows.items():
   if low<.0005:
    m=pb['foot_'+side].matrix.copy();m.translation.z+=.0005-low;pb['foot_'+side].matrix=m
  bpy.context.view_layer.update();ev=run.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();lo=min(v.co.z for v in me.vertices);floor=min(floor,lo);ev.to_mesh_clear()
  contact.append({'frame':f,'ankles':[pb['foot_'+side].head[:] for side in ['l','r']]})
  for p in pb:p.keyframe_insert(data_path='location',frame=f,group=p.name);p.keyframe_insert(data_path='rotation_quaternion',frame=f,group=p.name)
 for layer in act.layers:
  for strip in layer.strips:
   for cb in strip.channelbags:
    for curve in cb.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
 checks.append({'clip':kind,'frames':count,'duration':duration,'surface_min_z_m':floor,'contacts':contact});print('CLIP_DONE',kind,floor,flush=True)
# Save reference and working source, original actions remain available in this independent file.
for o in s.objects:
 if o.type=='MESH':o.hide_render=o!=run;o.hide_set(o!=run)
for im in bpy.data.images:
 if im.source=='FILE' and im.users and not im.packed_file:im.pack()
rig.animation_data.action=bpy.data.actions['A_Ranger_Idle_AQV2'];s.frame_start=1;s.frame_end=181;s.frame_set(1);s['authored_walk_speed_cm_s']=150.;s['status']='Independent animation quality candidate; not gameplay approved';s['source_file']='Ranger_NPC_V2_Protected.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
# Exports use exactly the same hierarchy/settings for each LOD and animation.
kw=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
for idx,obj in enumerate(models[1:]):
 for o in s.objects:o.select_set(False)
 rig.select_set(True);obj.hide_set(False);obj.select_set(True);bpy.context.view_layer.objects.active=rig;rig.data.pose_position='REST';bpy.ops.export_scene.fbx(filepath=str(E/('SK_Ranger_AQV2_LOD'+str(idx)+'.fbx')),bake_anim=False,**kw)
rig.data.pose_position='POSE'
for o in s.objects:o.select_set(False)
rig.select_set(True);run.select_set(True);bpy.context.view_layer.objects.active=rig
for kind,count,duration in clips:
 rig.animation_data.action=bpy.data.actions['A_Ranger_'+kind+'_AQV2'];s.frame_start=1;s.frame_end=count;s.frame_set(1);bpy.ops.export_scene.fbx(filepath=str(E/('A_Ranger_'+kind+'_AQV2.fbx')),bake_anim=True,**kw)
a={'source':s['source_file'],'work_file':str(out),'rig_bones':len(rig.data.bones),'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'head':b.head_local[:],'tail':b.tail_local[:]} for b in rig.data.bones],'geometry_unchanged':all(geom[o.name]==hashlib.sha256(np.array([v.co[:] for v in o.data.vertices],np.float32).tobytes()).hexdigest() for o in models),'meshes':counts,'clips':checks,'textures':[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file)} for im in bpy.data.images if im.users and im.source=='FILE'],'limitations':['Single fused source mesh: spatial cape/pouch weights require visual and deformation review.','No finger bones.','No runtime ground IK or terrain adaptation.','Turns use a restrained step cycle; actor yaw remains the movement system responsibility.']}
(O/'Data/BlenderAnimationAudit.json').write_text(json.dumps(a,indent=2))
# Actual pose sheets, no synthetic image generation.
s.render.engine='CYCLES';s.cycles.samples=6;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=720;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.camera.data.type='ORTHO';s.camera.data.ortho_scale=2.1
for o in s.objects:
 if o.type=='MESH':o.hide_render=o!=run
for label,kind,fr,loc in [('Idle_Front','Idle',1,(0,-5,.9)),('Walk_Contact','Walk',1,(3,-5,1.9)),('Walk_Passing','Walk',14,(3,-5,1.9)),('Walk_Opposite','Walk',28,(3,-5,1.9)),('Walk_Side','Walk',8,(5,0,.9)),('Talk','Talk',91,(3,-5,1.9)),('Cape_Back','Walk',14,(3,5,1.9))]:
 rig.animation_data.action=bpy.data.actions['A_Ranger_'+kind+'_AQV2'];s.frame_set(fr);s.camera.location=loc;s.camera.rotation_euler=(Vector((0,0,.9))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/'Blender'/(label+'.png'));bpy.ops.render.render(write_still=True);print('RENDER_DONE',label,flush=True)
print('ANIMATION_SOURCE_COMPLETE',flush=True)
