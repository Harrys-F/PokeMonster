"""Independent, bounded static healer-pose study from the existing FBX; not an animation-ready rig."""
import bpy,math,json,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];C=R/'Art/Characters/NPCs/SilverLady';S=R/'Saved/ArtPassV3';dst=C/'Source/SilverLady_HealerPose.blend';assert not dst.exists();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;bpy.ops.import_scene.fbx(filepath=str(C/'Exports/SM_SilverLady_Reference_V1.fbx'));o=next(o for o in bpy.context.scene.objects if o.type=='MESH');bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
# FBX carries historical absolute paths. Resolve only this independent import's existing images.
for image in bpy.data.images:
 if image.source=='FILE' and image.users:
  path=C/'Textures'/Path(image.filepath).name
  assert path.is_file(),path
  image.filepath=str(path);image.reload();image.pack()
ref=o.copy();ref.data=o.data.copy();bpy.context.scene.collection.objects.link(ref);ref.name='SilverLady_REFERENCE_UNCHANGED';ref.hide_render=True;ref.hide_set(True);o.name='SilverLady_HealerPose';s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
# Rebuild only the independent study material from the existing texture bindings.
mat=bpy.data.materials.new('SilverLady_ExistingPaintedMaterial');mat.use_nodes=True;nodes=mat.node_tree.nodes;p=nodes.get('Principled BSDF')
for role,file in [('Base Color','0'),('Roughness','1'),('Normal','2')]:
 im=bpy.data.images.load(str(C/'Textures'/('SilverLady_Image_'+file+'.jpg')));im.pack();t=nodes.new('ShaderNodeTexImage');t.image=im
 if role=='Base Color':mat.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color'])
 elif role=='Normal':im.colorspace_settings.name='Non-Color';n=nodes.new('ShaderNodeNormalMap');mat.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);mat.node_tree.links.new(n.outputs['Normal'],p.inputs['Normal'])
 else:
  im.colorspace_settings.name='Non-Color';sep=nodes.new('ShaderNodeSeparateColor');mat.node_tree.links.new(t.outputs['Color'],sep.inputs[0]);mat.node_tree.links.new(sep.outputs[1],p.inputs['Roughness']);mat.node_tree.links.new(sep.outputs[2],p.inputs['Metallic'])
o.data.materials.clear();o.data.materials.append(mat)
arm=bpy.data.armatures.new('SilverLady_PoseStudy');rig=bpy.data.objects.new('SilverLady_PoseStudy',arm);s.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;o.select_set(False);rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT');root=arm.edit_bones.new('body');root.head=(0,0,.85);root.tail=(0,0,1.15)
for side,sign in [('l',1),('r',-1)]:
 b=arm.edit_bones.new('upper_'+side);b.head=(sign*.235,0,1.505);b.tail=(sign*.525,0,1.495);b.parent=root
 f=arm.edit_bones.new('fore_'+side);f.head=b.tail;f.tail=(sign*.79,0,1.48);f.parent=b
 for key,x,parent in [('sleeveupper',.41,b),('sleevefore',.68,f)]:
  c=arm.edit_bones.new(key+'_'+side);c.head=(sign*x,0,1.40);c.tail=(sign*x,0,.90);c.parent=parent;c.use_inherit_rotation=False
bpy.ops.object.mode_set(mode='OBJECT');groups={b.name:o.vertex_groups.new(name=b.name) for b in arm.bones}
def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
for v in o.data.vertices:
 x,y,z=v.co;xx=abs(x);side='l' if x>0 else 'r';outer=smooth(.20,.30,xx)*(1-smooth(1.58,1.65,z));armweight=outer*smooth(1.30,1.46,z);cloth=outer*(1-smooth(1.25,1.43,z))*smooth(.36,.55,z);blend=smooth(.47,.60,xx);weights={'body':max(0,1-armweight-cloth),'upper_'+side:armweight*(1-blend),'fore_'+side:armweight*blend,'sleeveupper_'+side:cloth*(1-blend),'sleevefore_'+side:cloth*blend};total=sum(weights.values())
 for k,w in weights.items():
  if w>1e-6:groups[k].add([v.index],w/total,'REPLACE')
mod=o.modifiers.new('Bounded arm and gravity sleeve pose','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
# Bone-local Y follows each arm. World Y lowers the arms, world Z brings the hands forward.
from mathutils import Matrix
for side,sign in [('l',1),('r',-1)]:
 for key,down,front in [('upper',29,18),('fore',8,20)]:
  pbone=rig.pose.bones[key+'_'+side];rest=pbone.bone.matrix_local.to_3x3();world=Matrix.Rotation(math.radians(sign*down),3,'Y')@Matrix.Rotation(math.radians(-sign*front),3,'Z');pbone.rotation_mode='QUATERNION';pbone.rotation_quaternion=(rest.inverted()@world@rest).to_quaternion()
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dg);em=e.to_mesh();coords=np.array([v.co[:] for v in em.vertices]);audit={'vertices':len(em.vertices),'triangles':sum(len(f.vertices)-2 for f in em.polygons),'min_z':float(coords[:,2].min()),'max_z':float(coords[:,2].max()),'width':float(np.ptp(coords[:,0])),'finite':bool(np.isfinite(coords).all()),'rig_purpose':'Static arm/sleeve pose study, not validated animation rig','original_fbx_unchanged':True};e.to_mesh_clear();assert audit['finite'] and audit['min_z']>-.05,audit
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.export_scene.fbx(filepath=str(C/'Exports/SM_SilverLady_HealerPose.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim=False)
s.world=bpy.data.worlds.new('StudyWorld');s.world.color=(.15,.15,.15)
for loc,power in [((-3,-4,4),500),((3,2,3),350)]:
 d=bpy.data.lights.new('Review','AREA');d.energy=power;d.shape='DISK';d.size=3;a=bpy.data.objects.new('Review',d);s.collection.objects.link(a);a.location=loc;a.rotation_euler=(Vector((0,0,.95))-a.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('Review');cam=bpy.data.objects.new('Review',d);s.collection.objects.link(cam);s.camera=cam;d.type='ORTHO';d.ortho_scale=2.2;cam.location=(2.2,-4,1.7);cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=True;s.render.resolution_x=650;s.render.resolution_y=800;s.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=str(dst));bpy.ops.wm.open_mainfile(filepath=str(dst));assert bpy.data.objects.get('SilverLady_REFERENCE_UNCHANGED') and bpy.data.objects.get('SilverLady_PoseStudy');s=bpy.context.scene;s.render.filepath=str(S/'SilverLadyPoseStudy.png');bpy.ops.render.render(write_still=True);(C/'HealerPose.json').write_text(json.dumps(audit,indent=2));print('POSE_STUDY_REOPENED',json.dumps(audit))
