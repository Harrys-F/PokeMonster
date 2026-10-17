import bpy,json
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');C=Path(bpy.data.filepath).parent.parent;id=C.name
name='A_'+id+'_Talk_V1'
if name not in bpy.data.actions:
 with bpy.data.libraries.load(str(R/'Art/Characters/NPCs/Ranger/Source/Ranger_NPC_V1.blend'),link=False) as (src,d):d.actions=['A_Ranger_Gesture_Pilot']
 d.actions[0].name=name
for a in bpy.data.actions:
 if a.name.startswith('A_'+id+'_'):a.use_fake_user=True
assert name in bpy.data.actions
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('ACTION_PERSISTENCE_REPAIRED',id)
