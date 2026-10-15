import bpy,numpy as np,json,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_ray_tri
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_4K_Base_V1'];bpy.context.window.scene=s;o=next(o for o in s.objects if o.type=='MESH');m=o.data;t=time.time()
v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,3);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);f=f.reshape(-1,3)
print('BUILD_FULL_BVH',flush=True);tree=BVHTree.FromObject(o,bpy.context.evaluated_depsgraph_get(),deform=False,cage=False,epsilon=0.0);pairs=tree.overlap(tree);print('FULL_BVH_PAIRS',len(pairs),flush=True)
count=0;coplanar=0;shared=0;tested=0;examples=[]
def crossing(a,b):
 for poly,target in [(a,b),(b,a)]:
  for k in range(3):
   orig=poly[k];dr=poly[(k+1)%3]-orig;hit=intersect_ray_tri(target[0],target[1],target[2],dr,orig,True)
   if hit is not None and dr.length_squared>1e-16:
    tt=(hit-orig).dot(dr)/dr.length_squared
    if 1e-6<tt<1-1e-6:return True
 return False
for i,j in pairs:
 if i>=j:continue
 aa=f[i];bb=f[j]
 if np.any(aa[:,None]==bb[None,:]) or np.any(np.all(v[aa][:,None,:]==v[bb][None,:,:],axis=2)):shared+=1;continue
 a=[Vector(q) for q in v[aa]];b=[Vector(q) for q in v[bb]];n=(a[1]-a[0]).cross(a[2]-a[0]);dist=[abs(n.dot(p-a[0]))/max(n.length,1e-20) for p in b]
 if max(dist)<1e-7:coplanar+=1;continue
 tested+=1
 if crossing(a,b):
  count+=1
  if len(examples)<500:examples.append({'faces':[i,j],'center_m':((v[aa[0]]+v[aa[1]]+v[aa[2]])/3).tolist()})
normal=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',normal);normal=normal.reshape(-1,3);cross=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]);cross/=np.maximum(np.linalg.norm(cross,axis=1)[:,None],1e-20);dots=np.einsum('ij,ikj->ik',cross,normal.reshape(-1,3,3));q={'all_faces_bvh':len(f),'pair_entries':len(pairs),'shared_or_exact_coincident_vertex_pairs_excluded':shared,'coplanar_candidates_unresolved':coplanar,'noncoplanar_pairs_tested':tested,'confirmed_noncoplanar_crossings':count,'examples':examples,'triangles_with_any_opposed_corner':int(np.count_nonzero(np.any(dots<0,axis=1))),'corner_normals_opposed_to_face_dot_lt0':int(np.count_nonzero(dots<0)),'corner_normals_min_dot':float(dots.min()),'seconds':time.time()-t,'limits':'Whole-model BVH with zero expansion; segment-triangle checks excluding endpoint-only contacts, shared or exactly coincident vertex contacts and coplanar cases. Not a proof against every floating-point, near-contact, shared-vertex or coplanar defect. Rest pose only; no animation deformation test.'}
(B/'Review/4K_Base_V1/FullIntersectionAudit.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2),flush=True)
