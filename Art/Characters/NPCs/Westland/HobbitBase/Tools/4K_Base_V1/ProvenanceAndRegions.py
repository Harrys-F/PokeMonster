import bpy,numpy as np,json,hashlib,struct,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_ray_tri
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_4K_Base_V1'];m=next(o.data for o in s.objects if o.type=='MESH');t0=time.time()
v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,3);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);f=f.reshape(-1,3)
b=(B/'Incoming/4K_Base_V1/Meshy_Hobbit.glb').read_bytes();l=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+l]);offset=20+l+8

def accessor(i):
 a=d['accessors'][i];vw=d['bufferViews'][a['bufferView']];dt={5126:np.float32,5125:np.uint32,5123:np.uint16}[a['componentType']];nc={'SCALAR':1,'VEC3':3,'VEC2':2}[a['type']];return np.frombuffer(b,dtype=dt,count=a['count']*nc,offset=offset+vw.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,nc)
source=accessor(0);converted=source[:,[0,2,1]].copy();converted[:,1]*=-1
uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);suv=accessor(2).copy();suv[:,1]=1-suv[:,1]
proof={'positions_equal_glTF_Yup_to_Blender_Zup':bool(np.array_equal(v,converted)),'position_max_abs_error_m':float(np.abs(v-converted).max()),'triangle_indices_equal':bool(np.array_equal(f.ravel(),accessor(3).ravel())),'uv_corner_max_abs_error':float(np.abs(uv-suv[f.ravel()]).max()),'original_sha256':hashlib.sha256(b).hexdigest()}
del b,source,converted,uv,suv
# Limited high-value regions: excludes adjacent/shared/coincident vertex contacts.
regions=[('Nose_Mouth',[-.08,-.25,1.07],[.08,-.025,1.25]),('Hand_L',[.55,-.2,.94],[.75,.10,1.10]),('Hand_R',[-.75,-.2,.94],[-.55,.10,1.10]),('Foot_L',[.07,-.22,0],[.27,.15,.16]),('Foot_R',[-.27,-.22,0],[-.07,.15,.16]),('Cape_Hem',[-.34,-.06,.24],[.34,.25,.35])]
cent=(v[f[:,0]]+v[f[:,1]]+v[f[:,2]])/3;out=[]
def crosses(a,b):
 for poly,target in [(a,b),(b,a)]:
  for i in range(3):
   orig=poly[i];dr=poly[(i+1)%3]-orig
   hit=intersect_ray_tri(target[0],target[1],target[2],dr,orig,True)
   if hit is not None and dr.length_squared>1e-16:
    q=(hit-orig).dot(dr)/dr.length_squared
    if 1e-6<q<1-1e-6:return True
 return False
for name,lo,hi in regions:
 mask=np.all((cent>=lo)&(cent<=hi),axis=1);idx=np.where(mask)[0];ff=f[idx];u,inv=np.unique(ff,return_inverse=True);verts=v[u];faces=inv.reshape(-1,3);tree=BVHTree.FromPolygons(verts.tolist(),faces.tolist(),all_triangles=True,epsilon=0.0);pairs=tree.overlap(tree);count=0;examples=[];checked=0;shared=0;coplanar=0
 for i,j in pairs:
  if i>=j:continue
  aa=faces[i];bb=faces[j]
  if np.any(aa[:,None]==bb[None,:]) or np.any(np.all(verts[aa][:,None,:]==verts[bb][None,:,:],axis=2)):shared+=1;continue
  a=[Vector(q) for q in verts[aa]];b=[Vector(q) for q in verts[bb]];n=(a[1]-a[0]).cross(a[2]-a[0]);dist=[abs(n.dot(p-a[0]))/max(n.length,1e-20) for p in b]
  if max(dist)<1e-7:coplanar+=1;continue
  checked+=1
  if crosses(a,b):
   count+=1
   if len(examples)<12:examples.append({'faces':[int(idx[i]),int(idx[j])],'center_m':cent[idx[i]].tolist()})
 out.append({'region':name,'centroid_bounds_m':[lo,hi],'faces':len(idx),'bvh_pair_entries':len(pairs),'shared_or_coincident_contacts_excluded':shared,'coplanar_candidates_not_resolved':coplanar,'noncoplanar_pairs_tested':checked,'confirmed_noncoplanar_crossings':count,'examples':examples})
 print('REGION_DONE',name,count,flush=True);del tree,pairs
proof['regional_intersection_audit']=out;proof['self_intersection_coverage']='Centroid-selected regions only, no full-model exhaustive test; coplanar candidates excluded and remain unresolved. Adjacent/coincident contacts excluded. Counts are triangle pairs, not independent visual defects.';proof['seconds']=time.time()-t0
(B/'Review/4K_Base_V1/ProvenanceAndRegions.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof,indent=2),flush=True)
