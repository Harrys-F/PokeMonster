import bpy,numpy as np,json,time
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_4K_Base_V1'];m=next(o.data for o in s.objects if o.type=='MESH');t=time.time()
v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,3);tri=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',tri);tri=tri.reshape(-1,3)
u,inv=np.unique(v,axis=0,return_inverse=True);inv=inv.astype(np.int32);f=inv[tri];n=len(u)
pairs=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);pairs.sort(axis=1);codes=pairs[:,0].astype(np.int64)*n+pairs[:,1];del pairs
keys,count=np.unique(codes,return_counts=True);del codes
parent=list(range(n));rank=bytearray(n)
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
for code in keys:
 x,y=divmod(int(code),n);x=find(x);y=find(y)
 if x!=y:
  if rank[x]<rank[y]:x,y=y,x
  parent[y]=x
  if rank[x]==rank[y]:rank[x]+=1
roots=np.fromiter((find(i) for i in range(n)),np.int32,count=n);unique,cn=np.unique(roots,return_counts=True)
q={'method':'Read-only array equivalence of EXACT positions only; NO weld/edit applied to Blender geometry. UV/normal seams are not automatically interpreted as holes.','vertices_unique_positions':n,'components_after_virtual_exact_weld':len(unique),'boundary_edges_after_virtual_exact_weld':int(np.count_nonzero(count==1)),'edges_gt2_after_virtual_exact_weld':int(np.count_nonzero(count>2)),'top_components_vertices':sorted(cn.tolist(),reverse=True)[:20],'seconds':time.time()-t}
(B/'Review/4K_Base_V1/VirtualSeamAudit.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2),flush=True)
