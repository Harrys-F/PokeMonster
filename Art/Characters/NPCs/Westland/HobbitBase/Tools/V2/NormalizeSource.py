import bpy
from pathlib import Path
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_Base_V2'];bpy.context.window.scene=s
for other in list(bpy.data.scenes):
 if other!=s:
  assert not other.objects,'Never remove a populated scene'
  bpy.data.scenes.remove(other)
s.unit_settings.system='METRIC';s.unit_settings.scale_length=1.;s.unit_settings.length_unit='METERS'
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'Source/Hobbit_NPC_Base_V2.blend'))
print('Normal Blender V2 file saved; V1 untouched')
