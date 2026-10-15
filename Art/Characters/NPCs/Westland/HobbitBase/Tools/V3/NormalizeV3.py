import bpy
from pathlib import Path
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
s=bpy.data.scenes['Hobbit_NPC_Base_V3_Body'];bpy.context.window.scene=s
for q in list(bpy.data.scenes):
 if q!=s:
  assert len(q.objects)==0,'Do not remove a populated scene'
  bpy.data.scenes.remove(q)
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'Source/Hobbit_NPC_Base_V3_Body.blend'))
print('V3 saved as normal standalone Blender file')
