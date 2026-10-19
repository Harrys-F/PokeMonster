import bpy,json
from pathlib import Path
I=Path('/Users/harry/Developer/PokeMonster/Art/Characters/NPCs/IntegrationV1');p=Path(bpy.data.filepath);id=p.parent.parent.name
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];rigs=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'];ims=[i for i in bpy.data.images if i.source=='FILE' and i.users];actions=[a.name for a in bpy.data.actions]
assert len(rigs)==1 and len(meshes)==2 and len(ims)==3 and all(i.packed_file for i in ims)
assert any('Idle' in a for a in actions) and any(('Talk' in a or 'Gesture' in a) for a in actions)
out={'file':str(p),'meshes':len(meshes),'rigs':len(rigs),'bones':len(rigs[0].data.bones),'actions':actions,'packed_images':[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file)} for i in ims],'ok':True}
(I/(id+'_RuntimeReopen.json')).write_text(json.dumps(out,indent=2));print('RUNTIME_REOPEN_OK',id)
