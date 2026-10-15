import bpy,json,hashlib,shutil
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_4K_Base_V1'];bpy.context.window.scene=s
for q in list(bpy.data.scenes):
 if q!=s and not q.objects:bpy.data.scenes.remove(q)
meta=json.loads((B/'Review/4K_Base_V1/InputGLB.json').read_text());lookup={x['sha256']:x['path'] for x in meta['extracted_images']}
for im in bpy.data.images:
 if im.packed_file:
  digest=hashlib.sha256(bytes(im.packed_file.data)).hexdigest();assert digest in lookup
  im.filepath=bpy.path.relpath(lookup[digest])
  for pf in im.packed_files:pf.filepath=im.filepath
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Source/Hobbit_NPC_4K_Base_V1.blend'))
p=B/'Source/Hobbit_NPC_4K_Base_V1_ImportReference.blend';assert not p.exists();shutil.copy2(bpy.data.filepath,p)
print('MASTER_NORMALIZED_AND_REFERENCE_COPIED',flush=True)
