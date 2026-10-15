import bpy,json,numpy as np,hashlib
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_4K_Base_V1'];assert bpy.context.scene==s;o=next(o for o in s.objects if o.type=='MESH');m=o.data
v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);norm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',norm)
a=json.loads((B/'Review/4K_Base_V1/TechnicalAudit.json').read_text());assert hashlib.sha256(v.tobytes()+f.tobytes()).hexdigest()==a['geometry_hash'];assert hashlib.sha256(uv.tobytes()).hexdigest()==a['uv_hash'];assert hashlib.sha256(norm.tobytes()).hexdigest()==a['normal_hash']
proof=json.loads((B/'Review/4K_Base_V1/InputGLB.json').read_text());expected={i['sha256'] for i in proof['extracted_images']};imgs=[]
for im in bpy.data.images:
 if im.packed_file:
  digest=hashlib.sha256(bytes(im.packed_file.data)).hexdigest();assert digest in expected;assert Path(bpy.path.abspath(im.filepath)).exists();imgs.append({'image':im.name,'packed_sha256':digest,'external_exists':True})
assert len(imgs)==3;assert not any(o.type=='ARMATURE' for o in s.objects)
assert list(o.scale)==[1.,1.,1.];assert not o.modifiers and not o.vertex_groups
ref=B/'Source/Hobbit_NPC_4K_Base_V1_ImportReference.blend';master=B/'Source/Hobbit_NPC_4K_Base_V1.blend';assert hashlib.sha256(master.read_bytes()).hexdigest()==hashlib.sha256(ref.read_bytes()).hexdigest()
q={'reopened_file':bpy.data.filepath,'active_scene_correct':True,'mesh_objects':1,'armatures':0,'actions':len(bpy.data.actions),'unchanged_geometry_uv_normals':True,'textures_packed_byte_exact':imgs,'external_textures_resolved':True,'master_reference_byte_identical':True,'scale':[1,1,1],'height_m':float(v.reshape(-1,3)[:,2].max()-v.reshape(-1,3)[:,2].min()),'minimum_z_m':float(v.reshape(-1,3)[:,2].min())};(B/'Review/4K_Base_V1/ReopenFinal.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2),flush=True)
