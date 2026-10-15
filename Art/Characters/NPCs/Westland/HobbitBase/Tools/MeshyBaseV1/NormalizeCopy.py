import bpy
from mathutils import Vector
s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V1'];bpy.context.window.scene=s
for other in list(bpy.data.scenes):
 if other!=s and not other.objects:bpy.data.scenes.remove(other)
rig=s.objects['HNM1_Rig'];mesh=s.objects['HNM1_Body'];rig.hide_set(False);mesh.hide_set(False)
for ob in s.objects:ob.select_set(False)
rig.select_set(True);bpy.context.view_layer.objects.active=rig
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  sp=area.spaces.active;sp.region_3d.view_location=(0,0,.70);sp.region_3d.view_distance=2.8;sp.region_3d.view_rotation=Vector((0,1,0)).to_track_quat('-Z','Y');sp.region_3d.view_perspective=next(i.identifier for i in bpy.types.RegionView3D.bl_rna.properties['view_perspective'].enum_items if i.identifier=='ORTHO');sp.overlay.show_extras=False
  sp.shading.type=next(i.identifier for i in bpy.types.View3DShading.bl_rna.properties['type'].enum_items if i.identifier=='MATERIAL')
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('Saved regular standalone NPC file',bpy.data.filepath)
