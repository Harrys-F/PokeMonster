import bpy,numpy as np,json,time
from pathlib import Path
p=Path(bpy.data.filepath);id=p.parent.parent.name;I=p.parents[3]/'IntegrationV1';I=Path('/Users/harry/Developer/PokeMonster/Art/Characters/NPCs/IntegrationV1');out=[]
for o in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 m=o.data;n=len(m.vertices);co=np.empty(n*3,np.float32);m.vertices.foreach_get('co',co);co=co.reshape(-1,3);edges=np.empty(len(m.edges)*2,np.int32);m.edges.foreach_get('vertices',edges);edges=edges.reshape(-1,2)
 def components(edges,n):
  parent=np.arange(n,dtype=np.int32);sizes=np.ones(n,dtype=np.int32)
  def find(x):
   while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
   return x
  for aa,bb in edges:
   a=find(aa);b=find(bb)
   if a==b:continue
   if sizes[a]<sizes[b]:a,b=b,a
   parent[b]=a;sizes[a]+=sizes[b]
  return int(np.count_nonzero(parent==np.arange(n))),sorted([int(x) for x in sizes[parent==np.arange(n)]],reverse=True)[:12]
 raw,largest=components(edges,n);unique,inverse=np.unique(co,axis=0,return_inverse=True);weld,weldlargest=components(inverse[edges],len(unique))
 m.calc_loop_triangles();tri=np.empty(len(m.loop_triangles)*3,np.int32);m.loop_triangles.foreach_get('loops',tri);tri=tri.reshape(-1,3);uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2)[tri];a=uv[:,1]-uv[:,0];b=uv[:,2]-uv[:,0];det=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])
 out.append({'object':o.name,'raw_index_connected_components':raw,'largest_raw_component_vertex_counts':largest,'exact_position_duplicate_vertices':n-len(unique),'components_after_analysis_only_exact_position_weld':weld,'largest_welded_components':weldlargest,'uv_triangles_area_below_1e_12':int(np.count_nonzero(det<2e-12)),'note':'Read-only connectivity; UV/normal split duplicates are not automatically defects. Components do not establish semantic rider/clothing independence. Full self-intersection test not performed.'})
(I/(id+'_Connectivity.json')).write_text(json.dumps(out,indent=2));print('CONNECTIVITY_DONE',id)
