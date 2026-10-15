import bpy,json
from pathlib import Path
p=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
s=bpy.data.scenes['Hobbit_NPC_Base_V1'];bpy.context.window.scene=s
for other in list(bpy.data.scenes):
 if other!=s:
  assert not other.objects, 'Never remove a nonempty existing scene'
  bpy.data.scenes.remove(other)
m=bpy.data.objects['HNB_Body'].data
m.materials.clear();m.materials.append(bpy.data.materials['HNB_Skin'])
for poly in m.polygons:poly.material_index=0
exec(compile((p/'Tools/ProjectFaceDetails.py').read_text(),'ProjectFaceDetails.py','exec'))
bpy.ops.wm.save_as_mainfile(filepath=str(p/'Source/Hobbit_NPC_Base_V1.blend'))
print(json.dumps({'saved_normal_blend':bpy.data.filepath,'active_scene':bpy.context.scene.name}))
