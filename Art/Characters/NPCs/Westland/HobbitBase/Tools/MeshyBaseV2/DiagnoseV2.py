import bpy,bmesh,json,math,struct,hashlib
from pathlib import Path
from collections import Counter
from mathutils import Vector
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V2_Cleanup'];bpy.context.window.scene=s;o=s.objects['HNM2_Body'];rig=s.objects['HNM2_Rig'];me=o.data
bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table();bm.edges.ensure_lookup_table()
parts=[];seen=set()
for v in bm.verts:
 if v.index in seen:continue
 q=[v];seen.add(v.index);part=[]
 while q:
  a=q.pop();part.append(a.index)
  for e in a.link_edges:
   t=e.other_vert(a)
   if t.index not in seen:seen.add(t.index);q.append(t)
 parts.append(part)
kd=KDTree(len(me.vertices))
for v in me.vertices:kd.insert(v.co,v.index)
kd.balance();dups=[];nearest=[];compatible=[]
def weights(v):return tuple((g.group,round(g.weight,8)) for g in v.groups)
for v in bm.verts:
 if not v.link_faces:continue
 for co,j,d in kd.find_range(v.co,1e-6):
  if j>v.index and bm.verts[j].link_faces:
   pair={'a':v.index,'b':j,'distance_m':d,'weights_exact_equal':weights(me.vertices[v.index])==weights(me.vertices[j])};dups.append(pair)
   if pair['weights_exact_equal']:compatible.append(pair)
 if any(e.is_boundary for e in v.link_edges):
  ds=[d for _,j,d in kd.find_n(v.co,14) if j!=v.index and j not in {w.index for e in v.link_edges for w in e.verts} and bm.verts[j].link_faces]
  if ds:nearest.append(min(ds))
# Diagnostic only: tolerance sweep on disposable BMeshes, never save or accept automatically.
sweep=[]
for tol in []:
 bb=bmesh.new();bb.from_mesh(me);bmesh.ops.remove_doubles(bb,verts=list(bb.verts),dist=tol)
 sweep.append({'tolerance_m':tol,'vertices':len(bb.verts),'boundary_edges':sum(e.is_boundary for e in bb.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bb.edges)});bb.free()
me.calc_loop_triangles();verts=[v.co.copy() for v in me.vertices];tris=[tuple(t.vertices) for t in me.loop_triangles];bvh=BVHTree.FromPolygons(verts,tris,all_triangles=True,epsilon=1e-8)
def crossing(p,q,a,b,c):
 d=q-p;e1=b-a;e2=c-a;h=d.cross(e2);det=e1.dot(h)
 if abs(det)<1e-12:return False
 inv=1/det;v=p-a;u=v.dot(h)*inv
 if not 1e-7<u<1-1e-7:return False
 k=v.cross(e1);w=d.dot(k)*inv
 if w<1e-7 or u+w>1-1e-7:return False
 t=e2.dot(k)*inv;return 1e-6<t<1-1e-6
hits=[];candidate_count=0
for i,j in bvh.overlap(bvh):
 if i>=j or set(tris[i])&set(tris[j]):continue
 aa=[verts[k] for k in tris[i]];bb=[verts[k] for k in tris[j]];candidate_count+=1
 if any(crossing(aa[k],aa[(k+1)%3],*bb) for k in range(3)) or any(crossing(bb[k],bb[(k+1)%3],*aa) for k in range(3)):hits.append([i,j])
# Normal orientation compared with each actual geometric face normal.
dots=[]
for p in me.polygons:
 for l in p.loop_indices:dots.append(me.corner_normals[l].vector.dot(p.normal))
near=sorted(nearest);mat=me.materials[0];pr=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');uv=me.uv_layers.active
result={'mesh_objects':1,'vertices':len(me.vertices),'triangles':len(tris),'faces':len(me.polygons),'components':len(parts),'components_with_faces':sum(any(bm.verts[i].link_faces for i in p) for p in parts),'loose_vertices':[v.index for v in bm.verts if not v.link_faces],'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'nonmanifold_junction_edges':sum(len(e.link_faces)>2 for e in bm.edges),'degenerate_faces':[f.index for f in bm.faces if f.calc_area()<1e-12],'duplicate_active_vertex_pairs_1um':dups,'compatible_duplicate_pairs_1um':compatible,'tolerance_sweep_not_applied':sweep,'nearest_boundary_nonedge_vertex_quantiles_m':{str(q):near[min(len(near)-1,int(q*(len(near)-1)))] for q in [0,.1,.25,.5,.75,.9,1]},'proper_triangle_crossings':hits,'bvh_candidates_tested':candidate_count,'intersection_limits':'Shared vertices, coplanar and tangential contacts excluded; no formal proof. Clothing layers can overlap intentionally.','custom_normals':me.has_custom_normals,'normal_dot_negative_count':sum(d<0 for d in dots),'normal_dot_below_0_2_count':sum(d<.2 for d in dots),'normal_dot_min':min(dots),'normal_finite':all(math.isfinite(d) for d in dots),'inconsistent_manifold_edge_winding':sum(e.is_manifold and not e.is_contiguous for e in bm.edges),'uv_finite':all(math.isfinite(x) for u in uv.data for x in u.uv),'uv_min':[min(u.uv[i] for u in uv.data) for i in range(2)],'uv_max':[max(u.uv[i] for u in uv.data) for i in range(2)],'uv_degenerate_triangles':sum(abs((uv.data[p.loop_indices[1]].uv-uv.data[p.loop_indices[0]].uv).cross(uv.data[p.loop_indices[2]].uv-uv.data[p.loop_indices[0]].uv))<1e-12 for p in me.polygons),'alpha':pr.inputs['Alpha'].default_value,'alpha_linked':pr.inputs['Alpha'].is_linked,'transmission':pr.inputs['Transmission Weight'].default_value,'backface_culling':mat.use_backface_culling,'surface_render_method':mat.surface_render_method,'displacement_connected':any(n.type=='OUTPUT_MATERIAL' and n.inputs['Displacement'].is_linked for n in mat.node_tree.nodes),'textures':[{'name':n.image.name,'packed':bool(n.image.packed_file),'size':list(n.image.size),'colorspace':n.image.colorspace_settings.name,'alpha_mode':n.image.alpha_mode} for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image],'rest_pose':rig.data.pose_position,'rig_matrix':list(map(list,rig.matrix_world)),'mesh_matrix':list(map(list,o.matrix_world)),'bone_hierarchy':[{'name':b.name,'parent':b.parent.name if b.parent else None,'head':list(b.head_local),'tail':list(b.tail_local),'deform':b.use_deform} for b in rig.data.bones],'pose_constraints':[(p.name,c.type) for p in rig.pose.bones for c in p.constraints]}
bm.free();(B/'Review/MeshyBaseV2/Diagnosis_V2.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k not in ['bone_hierarchy','loose_vertices','proper_triangle_crossings','duplicate_active_vertex_pairs_1um','compatible_duplicate_pairs_1um']});print('Crossings',len(hits),'duplicate pairs',len(dups),'compatible',len(compatible))
