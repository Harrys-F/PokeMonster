import bpy,json,hashlib
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');I=R/'Art/Characters/NPCs/IntegrationV1';C=Path(bpy.data.filepath).parent.parent;id=C.name
s=bpy.context.scene;mesh=[o for o in s.objects if o.type=='MESH'];ims=[im for im in bpy.data.images if im.source=='FILE' and im.users];x={'id':id,'reopened':bpy.data.filepath,'scene':s.name,'meshes':len(mesh),'vertices':sum(len(o.data.vertices) for o in mesh),'packed_images':[{'name':im.name,'packed':bool(im.packed_file),'pixels':list(im.size),'external_exists':Path(bpy.path.abspath(im.filepath)).exists(),'sha256':hashlib.sha256(bytes(im.packed_file.data)).hexdigest() if im.packed_file else None} for im in ims],'world_height_m':max((o.matrix_world@v).z for o in mesh for v in [__import__('mathutils').Vector(c) for c in o.bound_box])-min((o.matrix_world@__import__('mathutils').Vector(c)).z for o in mesh for c in o.bound_box)}
assert len(mesh)==1 and len(ims)==3 and all(im.packed_file for im in ims)
(I/(id+'_Reopen.json')).write_text(json.dumps(x,indent=2));print('REOPEN_OK',id)
