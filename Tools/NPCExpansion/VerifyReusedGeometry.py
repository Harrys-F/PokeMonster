"""Read-only equality of the reused original working meshes and the animation authoring meshes."""
import bpy,json,hashlib,struct,numpy as np
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');rows=[]
def snapshot(obj,rig):
 h=hashlib.sha256();co=np.empty(len(obj.data.vertices)*3,np.float32);obj.data.vertices.foreach_get('co',co);h.update(co.tobytes())
 for p in obj.data.polygons:h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
 uv=hashlib.sha256()
 for layer in obj.data.uv_layers:
  for d in layer.data:uv.update(struct.pack('<2f',*d.uv))
 weights=hashlib.sha256()
 for v in obj.data.vertices:
  for name,w in sorted((obj.vertex_groups[g.group].name,g.weight) for g in v.groups):weights.update((name+':').encode());weights.update(struct.pack('<f',w))
 bones={b.name:{'matrix':[list(r)for r in b.matrix_local],'parent':b.parent.name if b.parent else None}for b in rig.data.bones}
 return {'geometry':h.hexdigest(),'uv':uv.hexdigest(),'weights':weights.hexdigest(),'rest_bones':bones,'object_matrix':[list(r)for r in obj.matrix_world]}
for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
 if not a.get('reuse_mesh'):continue
 C=R/'Art/Characters/NPCs'/a['id'];old=R/'Art/Characters/NPCs'/a['existing'];original_sha=hashlib.sha256(old.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False);before=snapshot(bpy.data.objects[a['mesh']],bpy.data.objects[a['rig']]);bpy.ops.wm.open_mainfile(filepath=str(C/'Source'/(a['id']+'_NPCLibrary.blend')),load_ui=False);after=snapshot(next(o for o in bpy.data.objects if o.type=='MESH'),next(o for o in bpy.data.objects if o.type=='ARMATURE'));assert before==after,a['id'];assert hashlib.sha256(old.read_bytes()).hexdigest()==original_sha;rows.append({'id':a['id'],'identical_geometry_uv_skin_weights_rest_skeleton_and_transform':True,'original_source_sha256':original_sha})
(R/'Saved/ProjectRefinement/NPCExpansion/ReusedGeometryVerification.json').write_text(json.dumps(rows,indent=2));print('REUSED_GEOMETRY_IDENTICAL',len(rows),flush=True)
