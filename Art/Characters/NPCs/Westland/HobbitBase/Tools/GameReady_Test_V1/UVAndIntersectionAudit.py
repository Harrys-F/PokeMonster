import bpy,numpy as np,json,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_ray_tri
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1';s=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'];bpy.context.window.scene=s;result={}
for name in ['HeadHair','Torso']:
 o=s.objects['GRT_'+name];m=o.data;nv=len(m.vertices);v=np.empty(nv*3,np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,3);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);f=f.reshape(-1,3);uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2)
 # Pixel-center raster: coverage is an independent test of the UV domain, not alpha on blank atlas.
 res=2048;coverage=np.zeros((res,res),np.uint16)
 for t in uv:
  lo=np.maximum(0,np.floor(t.min(0)*res-.5).astype(int));hi=np.minimum(res-1,np.ceil(t.max(0)*res-.5).astype(int))
  if np.any(hi<lo):continue
  xx=(np.arange(lo[0],hi[0]+1)+.5)/res;yy=(np.arange(lo[1],hi[1]+1)+.5)/res;X,Y=np.meshgrid(xx,yy);a,b,c=t;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-14:continue
  aa=((b[1]-c[1])*(X-c[0])+(c[0]-b[0])*(Y-c[1]))/den;bb=((c[1]-a[1])*(X-c[0])+(a[0]-c[0])*(Y-c[1]))/den;inside=(aa>1e-7)&(bb>1e-7)&((aa+bb)<1-1e-7);coverage[lo[1]:hi[1]+1,lo[0]:hi[0]+1]+=inside.astype(np.uint16)
 im=next(im for im in bpy.data.images if im.name=='GRT_'+name+'_BaseColor');pixels=np.empty(res*res*4,np.float32);im.pixels.foreach_get(pixels);pixels=pixels.reshape(res,res,4);mask=coverage>0
 r={'uv_occupied_texels':int(np.count_nonzero(mask)),'uv_coverage_fraction':float(np.mean(mask)),'uv_interior_overlapping_texels':int(np.count_nonzero(coverage>1)),'base_color_empty_alpha_inside_uv':int(np.count_nonzero((pixels[:,:,3]<.5)&mask)),'base_color_black_inside_uv':int(np.count_nonzero((pixels[:,:,:3].max(2)<1/255)&mask)),'height_bounds_m':[float(v[:,2].min()),float(v[:,2].max())]}
 tree=BVHTree.FromObject(o,bpy.context.evaluated_depsgraph_get(),deform=False,cage=False,epsilon=0);pairs=tree.overlap(tree);confirmed=0;candidate=0;coplanar=0
 for i,j in pairs:
  if i>=j or np.any(f[i][:,None]==f[j][None,:]):continue
  a=[Vector(p) for p in v[f[i]]];b=[Vector(p) for p in v[f[j]]];n=(a[1]-a[0]).cross(a[2]-a[0]);dist=[abs(n.dot(p-a[0]))/max(n.length,1e-20) for p in b]
  if max(dist)<1e-7:coplanar+=1;continue
  candidate+=1;hit=False
  for poly,target in [(a,b),(b,a)]:
   for k in range(3):
    orig=poly[k];dr=poly[(k+1)%3]-orig;q=intersect_ray_tri(*target,dr,orig,True)
    if q is not None and dr.length_squared>1e-16:
     t=(q-orig).dot(dr)/dr.length_squared
     if 1e-6<t<1-1e-6:hit=True;break
   if hit:break
  confirmed+=hit
 r['self_intersections']={'bvh_pairs':len(pairs),'nonadjacent_noncoplanar_pairs_tested':candidate,'confirmed_triangle_pair_crossings':confirmed,'unresolved_coplanar_pairs':coplanar,'limits':'Rest pose, zero expansion; endpoint and adjacent triangle contacts excluded. Triangle pairs, not distinct visible defects.'};result[name]=r;print('UV_INTERSECTION',name,r,flush=True)
(P/'UVAndIntersectionAudit.json').write_text(json.dumps(result,indent=2))
