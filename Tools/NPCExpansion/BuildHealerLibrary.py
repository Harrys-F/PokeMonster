"""Reuse the verified, original-appearance healer; reject the unsafe sleeve locomotion candidate."""
import bpy,json,math,hashlib,numpy as np
from pathlib import Path
from mathutils import Quaternion,Vector
R=Path('/Users/harry/Developer/PokeMonster');C=R/'Art/Characters/NPCs/SilverLady';E=C/'Exports/Library';O=R/'Saved/ProjectRefinement/NPCExpansion/AnimationViews/SilverLady';bpy.ops.wm.open_mainfile(filepath=str(C/'Source/Westland_Healer_ArtV4.blend'),load_ui=False);bpy.context.preferences.filepaths.save_version=0
obj=bpy.data.objects['Westland_Healer'];rig=bpy.data.objects['Westland_Healer_Idle'];rig.animation_data.action=None
for x in list(bpy.data.objects):
 if x not in (obj,rig):bpy.data.objects.remove(x,do_unlink=True)
obj.hide_set(False);obj.hide_render=False;s=bpy.context.scene;s.render.fps=30
mat=bpy.data.materials.new('SilverLady_OriginalAppearance');mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF')
for socket,index in [('Base Color',0),('Roughness',1),('Normal',2)]:
 image=bpy.data.images.load(str(C/'Textures'/('SilverLady_Image_'+str(index)+'.jpg')));image.pack();t=mat.node_tree.nodes.new('ShaderNodeTexImage');t.image=image
 if socket=='Base Color':mat.node_tree.links.new(t.outputs['Color'],p.inputs[socket])
 elif socket=='Normal':
  image.colorspace_settings.name='Non-Color';n=mat.node_tree.nodes.new('ShaderNodeNormalMap');mat.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);mat.node_tree.links.new(n.outputs['Normal'],p.inputs[socket])
 else:
  image.colorspace_settings.name='Non-Color';n=mat.node_tree.nodes.new('ShaderNodeSeparateColor');mat.node_tree.links.new(t.outputs['Color'],n.inputs[0]);mat.node_tree.links.new(n.outputs[1],p.inputs['Roughness']);mat.node_tree.links.new(n.outputs[2],p.inputs['Metallic'])
obj.data.materials.clear();obj.data.materials.append(mat);audit=[]
for kind,seconds in [('Idle',4.),('Talk',3.),('Greet',2.4),('TurnLeft',1.2),('TurnRight',1.2)]:
 count=round(seconds*30)+1;act=bpy.data.actions.new('A_SilverLady_'+kind+'_Library');act.use_fake_user=True
 for frame in range(1,count+1):
  rig.animation_data.action=None;s.frame_set(frame);u=(frame-1)/(count-1)
  for b in rig.pose.bones:b.rotation_mode='QUATERNION';b.rotation_quaternion=Quaternion();b.location=(0,0,0)
  for name,axis,angle in [('chest',(1,0,0),.003*math.sin(2*math.pi*u)),('head',(0,0,1),.024*math.sin(2*math.pi*u) if kind=='Talk' else 0),('head',(1,0,0),.035*math.sin(math.pi*u)**2 if kind=='Greet' else 0)]:
   b=rig.pose.bones[name];q=b.bone.matrix_local.to_quaternion();b.rotation_quaternion=(q.inverted()@Quaternion(axis,angle)@q)@b.rotation_quaternion
  rig.animation_data.action=act
  for b in rig.pose.bones:b.keyframe_insert('location',frame=frame,group=b.name);b.keyframe_insert('rotation_quaternion',frame=frame,group=b.name)
 rig.animation_data.action=None;audit.append({'role':kind,'name':act.name,'frames':count,'duration':seconds})
for x in bpy.data.objects:x.select_set(False)
obj.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;rig.animation_data.action=bpy.data.actions['A_SilverLady_Idle_Library'];s.frame_start=1;s.frame_end=121;s.frame_set(1)
dst=C/'Source/SilverLady_NPCLibrary.blend';assert not dst.exists();bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)
kw=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
rig.data.pose_position='REST';bpy.ops.export_scene.fbx(filepath=str(E/'SK_SilverLady_Library.fbx'),bake_anim=False,**kw);rig.data.pose_position='POSE'
for a in audit:
 rig.animation_data.action=bpy.data.actions[a['name']];s.frame_start=1;s.frame_end=a['frames'];s.frame_set(1);bpy.ops.export_scene.fbx(filepath=str(E/(a['name']+'.fbx')),bake_anim=True,**dict(kw,object_types={'ARMATURE'}))
co=np.empty(len(obj.data.vertices)*3,np.float32);obj.data.vertices.foreach_get('co',co);uv=np.empty(len(obj.data.loops)*2,np.float32);obj.data.uv_layers.active.data.foreach_get('uv',uv)
(O/'Audit.json').write_text(json.dumps({'id':'SilverLady','source':'SilverLady/Source/Westland_Healer_ArtV4.blend','blend':str(dst.relative_to(R)),'bones':3,'vertices':len(obj.data.vertices),'triangles':len(obj.data.polygons),'fingerprints':{'geometry':hashlib.sha256(co.tobytes()).hexdigest(),'uv':hashlib.sha256(uv.tobytes()).hexdigest()},'clips':audit,'limitations':'Existing verified three-bone stationary healer. Greeting is a nod, no hand wave. Walk/run intentionally disabled: failed full sleeve rig is not adopted.'},indent=2))
