"""Animate the existing Water V3 rig only. No topology, rest pose, skin, material or original source edits."""
import bpy,math,json,hashlib,sys
import numpy as np
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Garados';D=R/'Saved/ProjectRefinement/GaradosWaterV4';src=A/'Source/Garados_Water_V3.blend';out=A/'Source/Garados_Water_V4.blend';export=A/'Exports/WaterV4';assert not out.exists()or '--revise-own-v4'in sys.argv
source_hash=hashlib.sha256(src.read_bytes()).hexdigest();assert hashlib.sha256((R/'Art/Characters/Creatures/Incoming/Garados.glb').read_bytes()).hexdigest()=='ce0661729d56dfa628a3232f4296bd5ae3bd51a914f417e8e82426e33133f5b9'
bpy.ops.wm.open_mainfile(filepath=str(src));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Garados_Water_Body'];rig=bpy.data.objects['Garados_Water_Rig'];scene=bpy.context.scene
# A full fingerprint proves that only animation data is changed in this working source.
def fingerprint():
 h=hashlib.sha256();h.update(str([(v.index,tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in body.data.vertices]).encode());h.update(str([tuple(p.vertices)for p in body.data.polygons]).encode())
 for uv in body.data.uv_layers:h.update(str([tuple(v.uv)for v in uv.data]).encode())
 h.update(str([(b.name,list(b.head_local),list(b.tail_local),str(b.matrix_local),b.parent.name if b.parent else None)for b in rig.data.bones]).encode());h.update(str([m.name for m in body.data.materials]).encode());return h.hexdigest()
geometry=fingerprint();names=['spine_'+str(i).zfill(2)for i in range(20)];lengths=[rig.data.bones[n].length for n in names];rest={b.name:b.matrix_local.copy()for b in rig.data.bones};head_origin=rig.data.bones['head'].head_local.copy();scene.render.fps=60;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;export.mkdir(parents=True,exist_ok=True)
def setbone(name,origin,direction,bank=0):
 old=rig.data.bones[name].tail_local-rig.data.bones[name].head_local;flat=Quaternion((1,0,0),math.atan2(direction.z,direction.y)-math.atan2(old.z,old.y));yaw=math.atan2(-direction.x,direction.y)if name!='head'else math.atan2(direction.x,-direction.y);rotation=Quaternion(direction.normalized(),bank)@Quaternion((0,0,1),yaw)@flat;m=rotation.to_matrix().to_4x4()@rest[name];m.translation=origin;rig.pose.bones[name].matrix=m;bpy.context.view_layer.update()
def pose(phase,strength,observe,turn):
 for b in rig.pose.bones:b.matrix_basis=Matrix.Identity(4)
 pitches=[math.radians(-75)*max(0.,1-i/14)**1.10*observe for i in range(20)];rise=-sum(L*math.sin(p)for L,p in zip(lengths,pitches));pos=head_origin+Vector((.020*strength*math.sin(phase+.25),0,rise));head=Vector((.020*strength*math.sin(phase+.25)+.035*observe*math.sin(phase),-1,.16*observe));setbone('head',pos,head,math.radians(-turn))
 for i,(name,L)in enumerate(zip(names,lengths)):
  t=i/19;envelope=.060+.720*(t*t*(3-2*t));wave=strength*envelope*math.sin(phase-t*math.tau*1.15);pitch=pitches[i];direction=Vector((math.sin(wave)*math.cos(pitch),math.cos(wave)*math.cos(pitch),math.sin(pitch)));bank=math.radians(-4*turn)*math.sin(math.pi*t);setbone(name,pos,direction,bank);pos+=direction*L
roles={'SwimSlow':(.70,0,0),'SwimNormal':(1.,0,0),'SwimFast':(1.18,0,0),'SwimTurnLeft':(1.,0,1),'SwimTurnRight':(1.,0,-1),'SwimObserve':(.04,1,0)};audit={};bounds=[];seconds=2.8;frames=168
for role,(strength,observe,turn)in roles.items():
 name='Garados_'+role+'_V4';previous=bpy.data.actions.get(name)
 if previous:bpy.data.actions.remove(previous)
 action=bpy.data.actions.new(name);action.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=action;first=None;last=None;head_z=[];tail_z=[];tail_x=[];middle_x=[]
 for f in range(frames+1):
  scene.frame_set(f+1);pose(math.tau*f/frames,strength,observe,turn);head_z.append(rig.pose.bones['head'].head.z);tail_z.append(rig.pose.bones['spine_19'].tail.z);tail_x.append(rig.pose.bones['spine_19'].tail.x);middle_x.append(rig.pose.bones['spine_10'].head.x)
  for b in rig.pose.bones:
   b.rotation_mode='QUATERNION'
   for prop in ['location','rotation_quaternion','scale']:b.keyframe_insert(data_path=prop,frame=f+1,group=b.name)
  ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();coords=np.empty(len(mesh.vertices)*3,dtype=np.float64);mesh.vertices.foreach_get('co',coords);coords=coords.reshape(-1,3);bounds.append({'clip':role,'frame':f,'min':coords.min(0).tolist(),'max':coords.max(0).tolist(),'radius_cm':float(np.linalg.norm(coords[:,:2],axis=1).max()*100)})
  if f==0:first=coords.copy()
  if f==frames:last=coords.copy()
  ev.to_mesh_clear()
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
 seam=float(np.linalg.norm(last-first,axis=1).max());assert seam<1e-5,(role,seam)
 scene.frame_start=1;scene.frame_end=frames+1;scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig
 bpy.ops.export_scene.fbx(filepath=str(export/(name+'.fbx')),use_selection=True,object_types={'ARMATURE'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0)
 audit[role]={'seconds':seconds,'sample_rate':60,'frames':frames+1,'strength':strength,'observe':observe,'turn_bank':turn,'loop_seam_max_m':seam,'head_z_m':[min(head_z),max(head_z)],'tail_z_m':[min(tail_z),max(tail_z)],'tail_side_peak_to_peak_cm':(max(tail_x)-min(tail_x))*100,'mid_side_peak_to_peak_cm':(max(middle_x)-min(middle_x))*100};print('WATER_V4_CLIP',role,flush=True)
assert fingerprint()==geometry,'Geometry/rest/skin changed';assert hashlib.sha256(src.read_bytes()).hexdigest()==source_hash
rig.animation_data.action=bpy.data.actions['Garados_SwimNormal_V4'];scene.frame_start=1;scene.frame_end=169;scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out));summary={'source':str(src.relative_to(R)),'source_sha256':source_hash,'mesh_rest_skin_uv_material_fingerprint':geometry,'geometry_rest_skin_unchanged':True,'land_and_battle_animations_unchanged':True,'animation_only_fbx':True,'clips':audit,'authored_max_radius_cm':max(x['radius_cm']for x in bounds),'bounds_m':{'min':np.array([x['min']for x in bounds]).min(0).tolist(),'max':np.array([x['max']for x in bounds]).max(0).tolist()}};(A/'WaterV4_Audit.json').write_text(json.dumps(summary,indent=2));(D/'AuthoredBounds.json').write_text(json.dumps(bounds));print('WATER_V4_SOURCE',json.dumps(summary),flush=True)
