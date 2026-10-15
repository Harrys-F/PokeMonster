import bpy,numpy as np,json
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');m=next(o.data for o in bpy.data.scenes['Hobbit_NPC_4K_Base_V1'].objects if o.type=='MESH')
v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,3);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);f=f.reshape(-1,3)
u,inv=np.unique(v,axis=0,return_inverse=True);n=len(u);f=inv[f].astype(np.int32);pairs=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);pairs.sort(axis=1);keys,count=np.unique(pairs[:,0].astype(np.int64)*n+pairs[:,1],return_counts=True);del pairs
q={}
for name,mask in [('boundary',count==1),('greater_than_two_faces',count>2)]:
 codes=keys[mask];a=codes//n;b=codes%n;edges=np.stack([u[a],u[b]],axis=1);q[name]={'count':len(codes),'length_min_m':float(np.linalg.norm(u[a]-u[b],axis=1).min()),'length_max_m':float(np.linalg.norm(u[a]-u[b],axis=1).max()),'edges_m':edges.tolist()}
f.sort(axis=1);uf,ct=np.unique(f,axis=0,return_counts=True);q['duplicate_triangles_virtual_positions']=int(np.sum(ct-1));q['method']='Exact-position equivalence; read-only. No vertices joined in source.'
(B/'Review/4K_Base_V1/ResidualEdges.json').write_text(json.dumps(q,indent=2));print({k:v if not isinstance(v,dict) else {a:b for a,b in v.items() if a!='edges_m'} for k,v in q.items()},flush=True)
