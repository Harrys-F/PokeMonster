import bpy,json,hashlib
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');out={}
for i in [0,1]:
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(R/('Art/Characters/NPCs/Ranger/Exports/V2_Protected/SK_Ranger_NPC_V2_LOD'+str(i)+'.fbx')));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');m=next(o for o in bpy.data.objects if o.type=='MESH');out[str(i)]={'rig':rig.name,'matrix':str(rig.matrix_world),'mesh_matrix':str(m.matrix_world),'bones':[(b.name,b.parent.name if b.parent else None,[list(x) for x in b.matrix_local]) for b in rig.data.bones],'vertex_groups':[g.name for g in m.vertex_groups],'armature_modifiers':[(x.name,x.object.name if x.object else None) for x in m.modifiers if x.type=='ARMATURE']}
(R/'Art/Characters/NPCs/Ranger/Review/V2/FBXRigs.json').write_text(json.dumps(out,indent=2))
