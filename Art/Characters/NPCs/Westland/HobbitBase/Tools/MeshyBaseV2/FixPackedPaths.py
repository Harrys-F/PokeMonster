import bpy,json,hashlib
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V2_Cleanup'];bpy.context.window.scene=s;rows=[]
for n in s.objects['HNM2_Body'].data.materials[0].node_tree.nodes:
 if n.type!='TEX_IMAGE' or not n.image:continue
 im=n.image;before=hashlib.sha256(im.packed_file.data).hexdigest();paths=[p.filepath for p in im.packed_files]
 for packed in im.packed_files:packed.filepath=im.filepath
 assert before==hashlib.sha256(im.packed_file.data).hexdigest()
 rows.append({'image':im.name,'old_packed_paths':paths,'new_packed_paths':[p.filepath for p in im.packed_files],'texture_bytes_unchanged':True})
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
suffix='Checkpoint' if 'StagesMeshyBaseV2' in bpy.data.filepath else 'Master'
(B/'Review/MeshyBaseV2'/('PackedPathRepair_'+suffix+'.json')).write_text(json.dumps(rows,indent=2));print(rows)
