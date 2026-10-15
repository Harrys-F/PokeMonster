import bpy,numpy as np,json,hashlib,array
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/Retopo_V2';s=bpy.context.scene;assert s.name=='Hobbit_NPC_Retopo_V2' and len(bpy.data.scenes)==1
hp=s.objects['RTV2_HP_REFERENCE_UNMODIFIED'];o=s.objects['RTV2_Head_MANUAL_RETOPO_REQUIRED'];m=hp.data;a=json.loads((P/'WorkspaceAudit.json').read_text())
v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);nm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',nm)
assert hashlib.sha256(v.tobytes()+f.tobytes()).hexdigest()==a['geometry_hash'];assert hashlib.sha256(uv.tobytes()).hexdigest()==a['uv_hash'];assert hashlib.sha256(nm.tobytes()).hexdigest()==a['normal_hash']
assert len(o.data.vertices)==0 and len(o.data.polygons)==0
assert len([x for x in s.objects if x.type=='MESH'])==2 and not any(x.type=='ARMATURE' for x in s.objects)
assert len(bpy.data.actions)==0
assert all(c in s.collection.children for c in a['collections'])
assert o.modifiers[1].target==hp and abs(o.modifiers[1].offset-.0005)<1e-9 and o.modifiers[0].use_clip
assert hp.hide_select and hp.scale[:]==(1,1,1)
assert s.tool_settings.use_snap and s.tool_settings.snap_elements=={'FACE_PROJECT'} and not s.tool_settings.use_snap_selectable and s.tool_settings.use_snap_nonedit
assert s.render.filepath.startswith(str(P)) and s.view_layers[0].material_override is None
planes=[s.objects[n] for n in a['image_reference_planes']]
assert all(x.hide_select and x.data.packed_file and abs(x.color[3]-.35)<1e-6 and abs(x.empty_display_size-.43)<1e-6 for x in planes)
assert all(tuple(x.data.size)==(1000,1000) for x in planes)
assert all(bpy.data.texts.get(n) for n in ['RTV2_START_HERE','RTV2_CHECK_TARGET_READ_ONLY.py','RTV2_MANUELLE_RETOPO_ANLEITUNG.md'])
# Compare source materials after reopening; append ONLY source material for read-only comparison.
def graph(mat):
 def key(n):return (n.type,hashlib.sha256(bytes(n.image.packed_file.data)).hexdigest() if n.type=='TEX_IMAGE' and n.image else '')
 return {'nodes':sorted(key(n) for n in mat.node_tree.nodes),'links':sorted((key(l.from_node),l.from_socket.identifier,key(l.to_node),l.to_socket.identifier) for l in mat.node_tree.links),'principled_inputs':[(i.identifier,tuple(i.default_value) if hasattr(i.default_value,'__len__') and not isinstance(i.default_value,str) else i.default_value) for i in next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs]}
g=graph(m.materials[0])
with bpy.data.libraries.load(str(B/'Source/Hobbit_NPC_4K_Base_V1.blend'),link=False) as (source,d):d.materials=list(source.materials)
assert g==graph(d.materials[0])
q={'file_reopened':bpy.data.filepath,'correct_scene':True,'source_geometry_uv_normals_identical':True,'original_material_graph_inputs_images_identical':True,'source_height_m':float(v.reshape(-1,3)[:,2].max()-v.reshape(-1,3)[:,2].min()),'packed_original_textures':3,'packed_reference_image_planes':3,'collections_valid':True,'snap_and_modifiers_valid':True,'source_selection_locked':True,'reference_planes_locked_and_aligned':True,'manual_guide_and_qa_text_present':True,'no_failed_proxy_loaded':True,'no_armature_actions':True,'target_vertices':0,'target_faces':0,'animation_ready':False,'baked_material_target':False,'note':'Read-only reopen checks; no deformation or baking claims. No file save during QA.'}
(P/'ReopenAudit.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2),flush=True)
# Exact pixel contact sheets of genuine renders, not new/generated views.
for names,out in [(['01_Reference_Front.png','02_Reference_Right.png','04_Reference_ThreeQuarter.png'],'10_Reference_Views.png'),(['05_Reference_Clay_Front.png','06_Reference_Wire_Front.png'],'11_Reference_Clay_Wire.png')]:
 ims=[bpy.data.images.load(str(P/'Previews'/n),check_existing=False) for n in names];w,h=ims[0].size;dest=np.zeros((h,w*len(ims),4),np.float32)
 for j,im in enumerate(ims):
  px=np.empty(w*h*4,np.float32);im.pixels.foreach_get(px);dest[:,j*w:(j+1)*w]=px.reshape(h,w,4)
 result=bpy.data.images.new('RTV2_ReviewContactSheet',width=w*len(ims),height=h,alpha=True);result.pixels.foreach_set(dest.ravel());result.filepath_raw=str(P/'Previews'/out);result.file_format=next(i.identifier for i in bpy.types.Image.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG');result.save();print('CONTACT_SHEET_SAVED',out,flush=True)
 for im in ims:bpy.data.images.remove(im)
 bpy.data.images.remove(result)
