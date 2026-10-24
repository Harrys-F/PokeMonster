"""New swim source from accepted surface-repaired Schiggy; original mesh/rig/actions remain intact."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Matrix,Quaternion
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Schiggy';source=A/'Source/Schiggy_Surface_V2.blend';dest=A/'Source/Schiggy_Swim_V11.blend';assert not dest.exists();before=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0
rig=bpy.data.objects['Schiggy_Rig'];body=bpy.data.objects['Schiggy_Body'];s=bpy.context.scene;s.render.fps=30
original_actions=[a.name for a in bpy.data.actions];a=bpy.data.actions.new('Schiggy_Swim');a.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=a
for frame in range(37):
 s.frame_set(frame+1);t=frame/36;wave=math.sin(math.tau*t)
 for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
 # Gentle forward lean and alternating arm sweeps/leg paddles. Head/face and shell remain rigid.
 rig.pose.bones['root'].rotation_quaternion=Quaternion((1,0,0),math.radians(16));rig.pose.bones['root'].location.z=.045
 for side,sg in [('L',1),('R',-1)]:
  w=math.sin(math.tau*t+(0 if sg>0 else math.pi));rig.pose.bones['upperarm_'+side].rotation_quaternion=Quaternion((0,1,0),sg*(.12+.30*w))@Quaternion((1,0,0),.24*w)
  rig.pose.bones['forearm_'+side].rotation_quaternion=Quaternion((0,0,1),sg*.10*(1-w))
  rig.pose.bones['thigh_'+side].rotation_quaternion=Quaternion((1,0,0),.18*w);rig.pose.bones['shin_'+side].rotation_quaternion=Quaternion((1,0,0),-.10*(1-w))
 rig.pose.bones['tail_base'].rotation_quaternion=Quaternion((0,0,1),.09*wave)
 for p in rig.pose.bones:
  for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=frame+1,group=p.name)
for layer in a.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for curve in bag.fcurves:
    for k in curve.keyframe_points:k.interpolation='LINEAR'
for i in bpy.data.images:
 if i.type=='IMAGE':i.pack()
s.frame_start=1;s.frame_end=37;s.frame_set(1);out=A/'Exports/BiomeV11';out.mkdir(exist_ok=False);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.fbx(filepath=str(out/'Schiggy_Swim.fbx'),use_selection=True,object_types={'ARMATURE','MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE')
bpy.ops.wm.save_as_mainfile(filepath=str(dest));assert hashlib.sha256(source.read_bytes()).hexdigest()==before
(A/'SwimV11_Audit.json').write_text(json.dumps({'original':str(source.relative_to(R)),'original_sha256':before,'source':str(dest.relative_to(R)),'original_actions_retained':original_actions,'mesh_uv_weights_rest_rig_unchanged':True,'new_clip':'Schiggy_Swim','frames':37,'duration_s':1.2},indent=2));print('SCHIGGY_SWIM_READY')
