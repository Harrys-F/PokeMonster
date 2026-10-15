import bpy
from pathlib import Path
s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V2_Cleanup'];bpy.context.window.scene=s
for other in list(bpy.data.scenes):
 if other!=s and not other.objects:bpy.data.scenes.remove(other)
for n in s.objects['HNM2_Body'].data.materials[0].node_tree.nodes:
 if n.type=='TEX_IMAGE' and n.image:
  kind=next(k for k in ['BaseColor','ORM','Normal'] if k in n.image.name);n.image.filepath='//../../Textures/MeshyBaseV2/T_Hobbit_MeshyBase_V2_'+kind+'.png';n.image.pack();print(n.image.name,n.image.filepath,'packed',bool(n.image.packed_file))
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);print('Own before-cleanup checkpoint opens in its model scene; packed textures retained.')
