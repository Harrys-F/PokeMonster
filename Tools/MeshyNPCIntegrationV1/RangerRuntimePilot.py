import bpy,bmesh,numpy as np,math,json,sys
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');C=R/'Art/Characters/NPCs/Ranger';I=R/'Art/Characters/NPCs/IntegrationV1';s=bpy.context.scene;assert bpy.app.background and Path(bpy.data.filepath).name=='Ranger_NPC_Source_V1.blend'
hp=next(o for o in s.objects if o.type=='MESH');run=hp.copy();run.data=hp.data.copy();run.name='Ranger_Runtime_Pilot';c=bpy.data.collections.new('RUNTIME_PILOT');s.collection.children.link(c);c.objects.link(run)
run.data.transform(run.matrix_world);run.matrix_world.identity();hp.hide_render=True;hp.hide_set(True)
bpy.context.view_layer.objects.active=run;run.select_set(True);hp.select_set(False)
# Local runtime copy only: weld exact-position import seam splits, keeping loop UVs.
bm=bmesh.new();bm.from_mesh(run.data);before=len(bm.verts);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.to_mesh(run.data);bm.free();print('WELD_DONE',before,len(run.data.vertices),flush=True)
source_tri=len(run.data.polygons);mod=run.modifiers.new('Controlled_runtime_reduction_NOT_retopology','DECIMATE');mod.decimate_type='COLLAPSE';mod.ratio=90000/source_tri;mod.use_collapse_triangulate=True
bpy.ops.object.modifier_apply(modifier=mod.name);run.data.update();print('REDUCTION_DONE',len(run.data.polygons),flush=True)
# This is a reduction trial, not proof of animation-ready quad topology.
rigdata=bpy.data.armatures.new('Ranger_Pilot_Skeleton');rig=bpy.data.objects.new('Ranger_Pilot_Rig',rigdata);c.objects.link(rig);run.select_set(False);rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT');bones={}
def bone(n,h,t,parent=None):
 b=rigdata.edit_bones.new(n);b.head=h;b.tail=t
 if parent:b.parent=bones[parent]
 bones[n]=b
bone('root',(0,0,0),(0,0,.12));bone('pelvis',(0,0,.91),(0,0,1.05),'root');bone('spine',(0,0,1.05),(0,0,1.26),'pelvis');bone('chest',(0,0,1.26),(0,0,1.48),'spine');bone('neck',(0,0,1.48),(0,0,1.57),'chest');bone('head',(0,0,1.57),(0,0,1.79),'neck')
bone('cape_upper',(0,.11,1.43),(0,.16,.95),'chest');bone('cape_lower',(0,.16,.95),(0,.17,.28),'cape_upper');bone('bag',(.19,-.11,.91),(.23,-.11,.69),'pelvis');bone('back_sword',(-.16,.15,1.39),(-.18,.15,1.73),'chest')
for side,sign in [('l',1),('r',-1)]:
 bone('clavicle_'+side,(sign*.035,0,1.43),(sign*.24,0,1.43),'chest');bone('upperarm_'+side,(sign*.24,0,1.43),(sign*.54,0,1.43),'clavicle_'+side);bone('lowerarm_'+side,(sign*.54,0,1.43),(sign*.79,-.005,1.43),'upperarm_'+side);bone('hand_'+side,(sign*.79,-.005,1.43),(sign*.91,-.02,1.425),'lowerarm_'+side)
 bone('thigh_'+side,(sign*.115,0,.91),(sign*.12,-.01,.48),'pelvis');bone('shin_'+side,(sign*.12,-.01,.48),(sign*.12,0,.105),'thigh_'+side);bone('foot_'+side,(sign*.12,0,.105),(sign*.12,-.16,.055),'shin_'+side)
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True;groups={n:run.vertex_groups.new(name=n) for n in bones}
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def assign(v,w):
 w={n:q for n,q in w.items() if q>1e-5};total=sum(w.values())
 for n,q in w.items():groups[n].add([v.index],q/total,'REPLACE')
for v in run.data.vertices:
 x,y,z=v.co;ax=abs(x);side='l' if x>0 else 'r'
 # Explicit adapted arm region overrides cloak only at shoulder-height sleeves.
 arm_mix=smooth(.18,.32,ax)*smooth(1.29,1.40,z)
 if z>1.54 and ax<.24:w={'head':1}
 elif arm_mix>.001:
  t=smooth(.48,.60,ax);a={'upperarm_'+side:1-t,'lowerarm_'+side:t} if ax<.70 else {'lowerarm_'+side:1-smooth(.74,.81,ax),'hand_'+side:smooth(.74,.81,ax)};w={'chest':1-arm_mix};w.update({n:q*arm_mix for n,q in a.items()})
 elif y>.055 and .25<z<1.40:
  t=smooth(.58,1.25,z);w={'cape_upper':t,'cape_lower':1-t}
 elif z>1.48:w={'neck':1-smooth(1.50,1.58,z),'head':smooth(1.50,1.58,z)}
 elif z>.87:
  t=smooth(1.04,1.34,z);w={'spine':1-t,'chest':t}
 elif z>.32:
  t=smooth(.41,.56,z);w={'shin_'+side:1-t,'thigh_'+side:t}
 else:
  t=smooth(.10,.20,z);w={'foot_'+side:1-t,'shin_'+side:t}
 assign(v,w)
run.parent=rig;mod=run.modifiers.new('Pilot deformation','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
pb=rig.pose.bones
for p in pb:p.rotation_mode='QUATERNION'
def rot(n,axis,a):
 q=rig.data.bones[n].matrix_local.to_quaternion();pb[n].rotation_quaternion=(q.inverted()@Quaternion(axis,a)@q)@pb[n].rotation_quaternion
s.render.fps=30;rig.animation_data_create()
for name,count in [('A_Ranger_Idle_Pilot',91),('A_Ranger_Gesture_Pilot',61)]:
 act=bpy.data.actions.new(name);act.use_fake_user=True;rig.animation_data.action=act
 for f in range(1,count+1):
  phase=2*math.pi*(f-1)/(count-1)
  for p in pb:p.location=(0,0,0);p.rotation_quaternion=Quaternion()
  rot('chest',(1,0,0),.004*math.sin(phase));rot('head',(0,0,1),.005*math.sin(phase));rot('cape_upper',(1,0,0),-.012+.004*math.sin(phase-.5));rot('cape_lower',(1,0,0),-.012+.007*math.sin(phase-.7))
  for side,sign in [('l',1),('r',-1)]:rot('upperarm_'+side,(0,1,0),sign*math.radians(74));rot('lowerarm_'+side,(0,1,0),sign*math.radians(6))
  if 'Gesture' in name:rot('lowerarm_l',(1,0,0),-.18*math.sin(math.pi*(f-1)/(count-1))**2)
  for p in pb:p.keyframe_insert(data_path='location',frame=f,group=p.name);p.keyframe_insert(data_path='rotation_quaternion',frame=f,group=p.name)
 for layer in act.layers:
  for strip in layer.strips:
   for cb in strip.channelbags:
    for curve in cb.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
rig.animation_data.action=bpy.data.actions['A_Ranger_Idle_Pilot'];s.frame_start=1;s.frame_end=91;s.frame_set(1);s['status']='Unapproved Ranger rig/reduction pilot; requires visual deformation check'
f=C/'Source/Ranger_NPC_RigPilot_V1.blend';assert not f.exists();bpy.ops.wm.save_as_mainfile(filepath=str(f))
frames=[]
for action,frame,label in [('A_Ranger_Idle_Pilot',1,'04_Idle_Pilot'),('A_Ranger_Gesture_Pilot',31,'05_Gesture_Pilot')]:
 rig.animation_data.action=bpy.data.actions[action];s.frame_set(frame);bpy.context.view_layer.update();s.camera.location=(3,-5,2.1);s.camera.rotation_euler=(Vector((0,0,.9))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=2.1;s.render.filepath=str(C/'Previews'/(label+'.png'));bpy.ops.render.render(write_still=True);frames.append(s.render.filepath)
report={'source_triangles':source_tri,'runtime_vertices':len(run.data.vertices),'runtime_triangles':len(run.data.polygons),'rig_bones':len(rigdata.bones),'rig_landmarks':'Human-specific manually chosen from Ranger front/profile render; NOT Hobbit 140cm proportions','frames':frames,'status':'pilot_requires_visual_approval','notes':['No guaranteed finger articulation','Cloak and sword regional weights require close-up inspection','No Walk authored until idle and arm deformation pass','Not animation-ready solely because it has weights']};(I/'Ranger_PilotAudit.json').write_text(json.dumps(report,indent=2));print('PILOT_DONE',flush=True)
