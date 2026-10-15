import bpy,json,math,numpy as np,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/Retopo_V2';s=bpy.data.scenes['Hobbit_NPC_Retopo_V2'];bpy.context.window.scene=s
assert len(bpy.data.scenes)==1
hp=s.objects['RTV2_HP_REFERENCE_UNMODIFIED'];target=s.objects['RTV2_Head_MANUAL_RETOPO_REQUIRED'];assert len(target.data.vertices)==0
# Blender 5.2 uses per-element Face Project, mutually exclusive with base Face snapping.
t=s.tool_settings;t.snap_elements={'FACE_PROJECT'};t.use_snap=True;t.use_snap_nonedit=True;t.use_snap_selectable=False;t.use_snap_self=False;t.use_snap_edit=False;t.use_snap_align_rotation=False
imgs=bpy.data.collections.new('REVIEW_REF_IMAGES');next(c for c in s.collection.children if c.name=='REVIEW').children.link(imgs)
for name,filename in [('Front','01_Reference_Front.png'),('Right','02_Reference_Right.png'),('Left','03_Reference_Left.png')]:
 cam=s.objects['RTV2_Camera_'+name];im=bpy.data.images.load(str(P/'Previews'/filename),check_existing=False);im.name='RTV2_PACKED_REFERENCE_'+name;im.pack()
 o=bpy.data.objects.new('RTV2_IMAGE_REFERENCE_'+name,None);imgs.objects.link(o);o.empty_display_type=next(i.identifier for i in bpy.types.Object.bl_rna.properties['empty_display_type'].enum_items if i.identifier=='IMAGE');o.data=im;o.empty_display_size=.43;o.color=(1,1,1,.35)
 o.rotation_euler=cam.rotation_euler;o.location=Vector((0,0,1.205))+(Vector((0,0,1.205))-cam.location).normalized()*.4;o.empty_image_depth=next(i.identifier for i in bpy.types.Object.bl_rna.properties['empty_image_depth'].enum_items if i.identifier=='BACK');o.hide_select=True;o.hide_set(True)
 o['subject']='Highpoly reference rendering, not retopo outcome';o['ortho_scale_m']=.43;o['head_center_z_m']=1.205
 # Packed image reference path remains valid if blend moves within Source directory.
 im.filepath=bpy.path.relpath(str(P/'Previews'/filename));
 for pf in im.packed_files:pf.filepath=im.filepath
# Review overrides are stored as helpers; original material graph remains unmodified.
clay=bpy.data.materials.new('RTV2_REVIEW_ONLY_Clay');clay.use_nodes=True;clay.use_fake_user=True;bs=next(n for n in clay.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.42,.39,.35,1);bs.inputs['Roughness'].default_value=.78
wire=clay.copy();wire.name='RTV2_REVIEW_ONLY_Wire';wire.use_fake_user=True;bs=next(n for n in wire.node_tree.nodes if n.type=='BSDF_PRINCIPLED');n=wire.node_tree.nodes.new('ShaderNodeWireframe');n.use_pixel_size=True;n.inputs['Size'].default_value=.5;mix=wire.node_tree.nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.55,.5,.44,1);mix.inputs[2].default_value=(.008,.012,.016,1);wire.node_tree.links.new(n.outputs[0],mix.inputs[0]);wire.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
manual=bpy.data.texts.new('RTV2_MANUELLE_RETOPO_ANLEITUNG.md');manual.write((P/'MANUELLE_RETOPO_ANLEITUNG.md').read_text())
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   space=area.spaces.active;space.region_3d.view_rotation=Quaternion((1,0,0),math.pi/2);space.region_3d.view_perspective='ORTHO';space.region_3d.view_location=(0,0,1.205);space.region_3d.view_distance=.7
   space.clip_start=.001;space.clip_end=100;space.shading.type=next(i.identifier for i in bpy.types.View3DShading.bl_rna.properties['type'].enum_items if i.identifier=='SOLID');space.shading.color_type='MATERIAL';space.overlay.show_floor=False;space.overlay.show_axis_x=False;space.overlay.show_axis_y=False
s.camera=s.objects['RTV2_Camera_Front'];s.view_layers[0].material_override=None
s.view_layers[0].objects.active=target
for o in s.objects:
 if o.select_get():o.select_set(False)
target.select_set(True)
s.render.filepath=str(P/'Previews/ManualWorkspace_Render.png')
a=json.loads((P/'WorkspaceAudit.json').read_text());a['snap']={'enabled':t.use_snap,'elements':list(t.snap_elements),'nonedit_targets':t.use_snap_nonedit,'selectable_targets_only':t.use_snap_selectable,'self':t.use_snap_self,'explanation':'FACE_PROJECT is Blender 5.2 individual Face projection; excludes self/edit geometry, permits locked highpoly target'};a['image_reference_planes']=[o.name for o in imgs.objects];a['studio_override_helpers']=[clay.name,wire.name];a['saved_workspace']=bpy.context.workspace.name
(P/'WorkspaceAudit.json').write_text(json.dumps(a,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('FINAL_WORKSPACE_SAVED',flush=True)
