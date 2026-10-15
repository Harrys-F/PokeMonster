import bpy,numpy as np,json,hashlib
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1';s=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'];assert bpy.context.scene==s
assert s.render.filepath.startswith(str(P));assert not s['GameReady_approved'];hp=s.objects['GRT_HighPoly_Reference'];m=hp.data
v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);nm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',nm);a=json.loads((P/'RegionAnalysis.json').read_text())['complete_source']
assert hashlib.sha256(v.tobytes()+f.tobytes()).hexdigest()==a['geometry_hash'];assert hashlib.sha256(uv.tobytes()).hexdigest()==a['uv_hash'];assert hashlib.sha256(nm.tobytes()).hexdigest()==a['normal_hash'];assert not any(o.type=='ARMATURE' for o in s.objects)
images=[im for im in bpy.data.images if im.name.startswith('GRT_')];assert len(images)==10 and all(im.packed_file and Path(bpy.path.abspath(im.filepath)).exists() for im in images)
# Compare original reference material graph by node types, sockets and packed image contents.
def graph(mat):
 def key(n):return (n.type,hashlib.sha256(bytes(n.image.packed_file.data)).hexdigest() if n.type=='TEX_IMAGE' and n.image else '')
 return {'nodes':sorted(key(n) for n in mat.node_tree.nodes),'links':sorted((key(l.from_node),l.from_socket.identifier,key(l.to_node),l.to_socket.identifier) for l in mat.node_tree.links),'principled_inputs':[(i.identifier,tuple(i.default_value) if hasattr(i.default_value,'__len__') and not isinstance(i.default_value,str) else i.default_value) for i in next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs]}
copygraph=graph(hp.data.materials[0])
with bpy.data.libraries.load(str(B/'Source/Hobbit_NPC_4K_Base_V1.blend'),link=False) as (src,dst):dst.materials=list(src.materials)
assert copygraph==graph(dst.materials[0]);q={'reopened':bpy.data.filepath,'active_scene_correct':True,'source_geometry_uv_normals_unchanged':True,'source_material_graph_and_defaults_unchanged':True,'all_10_new_textures_packed_and_external_available':True,'approved_game_ready':False,'no_rig':True,'safe_new_render_path':s.render.filepath,'source_height_m':float(v.reshape(-1,3)[:,2].max()-v.reshape(-1,3)[:,2].min())};(P/'ReopenFinal.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
# Read-only verification; appended reference material not saved into test file.
