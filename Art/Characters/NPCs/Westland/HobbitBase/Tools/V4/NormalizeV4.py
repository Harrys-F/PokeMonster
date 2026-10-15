import bpy
from pathlib import Path
s=bpy.data.scenes['Hobbit_NPC_V4_HeadSculpt'];bpy.context.window.scene=s
for other in list(bpy.data.scenes):
 if other!=s and not other.objects:bpy.data.scenes.remove(other)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('Reopened and normalized V4 only',bpy.data.filepath)
