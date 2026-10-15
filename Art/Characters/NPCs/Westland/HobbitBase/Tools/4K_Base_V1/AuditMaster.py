import bpy,numpy as np,json,hashlib,time
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_4K_Base_V1'];bpy.context.window.scene=s
o=next(o for o in s.objects if o.type=='MESH');m=o.data;t0=time.time()
def arr(seq,field,n,dtype=np.float32):
 a=np.empty(n,dtype=dtype);seq.foreach_get(field,a);return a
v=arr(m.vertices,'co',len(m.vertices)*3).reshape(-1,3);e=arr(m.edges,'vertices',len(m.edges)*2,np.int32).reshape(-1,2);tri=arr(m.loops,'vertex_index',len(m.loops),np.int32).reshape(-1,3);ei=arr(m.loops,'edge_index',len(m.loops),np.int32)
usage=np.bincount(ei,minlength=len(e));unique,dupc=np.unique(v,axis=0,return_counts=True)
print('ARRAY_AUDIT_READY',flush=True)
a=v[tri[:,1]]-v[tri[:,0]];b=v[tri[:,2]]-v[tri[:,0]];cross=np.cross(a,b);area=np.linalg.norm(cross,axis=1)*.5;del a,b,cross,unique
start=tri.ravel();end=np.roll(tri,-1,axis=1).ravel();ori=np.where(start<end,1,-1);sums=np.bincount(ei,weights=ori,minlength=len(e));del start,end,ori,ei
parent=list(range(len(v)));rank=bytearray(len(v))
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
for x,y in e:
 x=find(int(x));y=find(int(y))
 if x!=y:
  if rank[x]<rank[y]:x,y=y,x
  parent[y]=x
  if rank[x]==rank[y]:rank[x]+=1
labels=np.fromiter((find(i) for i in range(len(v))),dtype=np.int32,count=len(v));ids,counts=np.unique(labels,return_counts=True);fid,fcounts=np.unique(labels[tri[:,0]],return_counts=True);face_lookup=dict(zip(fid.tolist(),fcounts.tolist()))
components=sorted([{'root':int(i),'vertices':int(n),'faces':face_lookup.get(int(i),0)} for i,n in zip(ids,counts)],key=lambda q:q['faces'],reverse=True)
print('COMPONENTS_READY',len(components),flush=True)
uv=arr(m.uv_layers.active.data,'uv',len(m.loops)*2).reshape(-1,2);norm=arr(m.corner_normals,'vector',len(m.loops)*3).reshape(-1,3);ln=np.linalg.norm(norm,axis=1)
materials=[]
for mat in m.materials:
 pr=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');materials.append({'name':mat.name,'slots':1,'backface_culling':mat.use_backface_culling,'surface_render_method':mat.surface_render_method,'alpha':pr.inputs['Alpha'].default_value,'alpha_linked':pr.inputs['Alpha'].is_linked,'nodes':[{'name':n.name,'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None} for n in mat.node_tree.nodes]})
images=[{'name':im.name,'resolution':list(im.size),'colorspace':im.colorspace_settings.name,'packed':bool(im.packed_file),'filepath':im.filepath,'packed_sha256':hashlib.sha256(bytes(im.packed_file.data)).hexdigest()} for im in bpy.data.images if im.packed_file]
pts=[o.matrix_world@Vector(p) for p in o.bound_box];low=[min(p[i] for p in pts) for i in range(3)];high=[max(p[i] for p in pts) for i in range(3)];height=high[2]-low[2]
report={'reopen':True,'scene':s.name,'vertices':len(v),'edges':len(e),'polygons':len(m.polygons),'triangles':len(tri),'mesh_objects':1,'armatures':sum(ob.type=='ARMATURE' for ob in s.objects),'actions':[a.name for a in bpy.data.actions],'component_count':len(components),'components_top20':components[:20],'components_with_faces':sum(c['faces']>0 for c in components),'isolated_vertices':sum(c['vertices'] for c in components if c['faces']==0),'boundary_edges':int(np.count_nonzero(usage==1)),'edges_more_than_2_faces':int(np.count_nonzero(usage>2)),'loose_edges':int(np.count_nonzero(usage==0)),'nonmanifold_including_boundary':int(np.count_nonzero(usage!=2)),'inconsistent_winding_manifold_edges':int(np.count_nonzero((usage==2)&(np.abs(sums)>0))),'duplicate_vertices_exact_redundant':int(np.sum(dupc-1)),'duplicate_position_groups':int(np.count_nonzero(dupc>1)),'degenerate_exact_zero_area':int(np.count_nonzero(area==0)),'near_degenerate_area_lt_1e_12_m2':int(np.count_nonzero(area<1e-12)),'area_min':float(area.min()),'nonfinite_positions':int(np.count_nonzero(~np.isfinite(v))),'nonfinite_uv':int(np.count_nonzero(~np.isfinite(uv))),'uv_min':uv.min(0).tolist(),'uv_max':uv.max(0).tolist(),'has_custom_normals':m.has_custom_normals,'nonfinite_corner_normals':int(np.count_nonzero(~np.isfinite(norm))),'zero_corner_normals':int(np.count_nonzero(ln<1e-7)),'corner_normal_lengths':[float(ln.min()),float(ln.max())],'materials':materials,'images':images,'world_min_m':low,'world_max_m':high,'height_m':height,'size_variant_uniform_factors':{str(h):h/height for h in [1.20,1.32,1.45]},'geometry_hash':hashlib.sha256(v.tobytes()+tri.tobytes()).hexdigest(),'uv_hash':hashlib.sha256(uv.tobytes()).hexdigest(),'normal_hash':hashlib.sha256(norm.tobytes()).hexdigest(),'seconds':time.time()-t0,'self_intersections':'Pending regional BVH examination; full exhaustive intersection test not yet performed.'}
(B/'Review/4K_Base_V1/TechnicalAudit.json').write_text(json.dumps(report,indent=2));(B/'Review/4K_Base_V1/Components.json').write_text(json.dumps(components,indent=2));print(json.dumps({k:q for k,q in report.items() if k not in ['materials','images','components_top20']},indent=2),flush=True)
# Only armature and actions loaded from old file; old body never loaded or used.
with bpy.data.libraries.load(str(B/'Source/Hobbit_NPC_MeshyBase_V2_Cleanup.blend'),link=False) as (src,dst):
 dst.armatures=list(src.armatures);dst.actions=list(src.actions)
rig={'source':'Source/Hobbit_NPC_MeshyBase_V2_Cleanup.blend','armatures':[{'name':a.name,'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'head':list(b.head_local),'tail':list(b.tail_local),'deform':b.use_deform} for b in a.bones]} for a in dst.armatures],'actions':[{'name':a.name,'range':list(a.frame_range)} for a in dst.actions]}
(B/'Review/4K_Base_V1/RigReference.json').write_text(json.dumps(rig,indent=2));print('RIG_READ_ONLY_REFERENCE_READY',flush=True)
