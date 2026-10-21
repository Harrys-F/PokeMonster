"""Smooth weights on a virtual position weld; preserve every source point, face and UV corner."""
import numpy as np

def smooth(body,iterations=18):
 m=body.data;count=len(m.vertices);groups=len(body.vertex_groups);co=np.empty(count*3,dtype=np.float32);m.vertices.foreach_get('co',co);co=co.reshape((-1,3));_,inverse=np.unique(np.rint(co/1e-6).astype(np.int64),axis=0,return_inverse=True);n=int(inverse.max())+1
 weights=np.zeros((n,groups),dtype=np.float64);multiplicity=np.bincount(inverse,minlength=n)
 for v in m.vertices:
  for g in v.groups:weights[inverse[v.index],g.group]+=g.weight
 weights/=multiplicity[:,None];ends=np.empty(len(m.edges)*2,dtype=np.int32);m.edges.foreach_get('vertices',ends);ends=inverse[ends.reshape((-1,2))];ends=ends[ends[:,0]!=ends[:,1]];degree=np.bincount(ends.reshape(-1),minlength=n);active=degree>0
 for _ in range(iterations):
  sums=np.zeros_like(weights);np.add.at(sums,ends[:,0],weights[ends[:,1]]);np.add.at(sums,ends[:,1],weights[ends[:,0]]);weights[active]=weights[active]*.55+sums[active]/degree[active,None]*.45
 order=np.argsort(weights,axis=1)[:,-4:];mask=np.zeros_like(weights,dtype=bool);np.put_along_axis(mask,order,True,axis=1);weights*=mask;weights/=weights.sum(axis=1)[:,None]
 for g in body.vertex_groups:g.remove(list(range(count)))
 for v in m.vertices:
  for j in order[inverse[v.index]]:
   value=weights[inverse[v.index],j]
   if value>1e-7:body.vertex_groups[int(j)].add([v.index],float(value),'REPLACE')
 assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in m.vertices)
 return dict(iterations=iterations,virtual_vertices=n,original_vertices=count,maximum_influences=4,no_geometry_or_uv_changes=True)
