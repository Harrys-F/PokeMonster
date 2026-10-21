"""Final wing skin isolation by actual surface connectivity, preserving nearby arms.
Restore original weights in the owned candidate, then apply a continuous membrane-distance field.
"""
import bpy,json,hashlib,numpy as np,heapq,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Glurak';p=A/'Source/Glurak_PolishV4.blend';audit=json.loads((A/'PolishV4_Audit.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not __import__('subprocess').check_output(['git','ls-files','--',str(p.relative_to(R))],cwd=R).strip(),'Candidate is versioned: do not overwrite a released source';assert digest(p)==audit['source_sha256'];original=A/'Source/Glurak_Meshy_V1.blend';orig_sha=digest(original);bpy.ops.wm.open_mainfile(filepath=str(original));ob=bpy.data.objects['Glurak_Body'];group_names=[g.name for g in ob.vertex_groups];original_weights=np.zeros((len(ob.data.vertices),len(group_names)))
for v in ob.data.vertices:
 for g in v.groups:original_weights[v.index,g.group]=g.weight
bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Glurak_Body'];rig=bpy.data.objects['Glurak_Rig'];s=bpy.context.scene;assert group_names==[g.name for g in body.vertex_groups];co=np.array([tuple(v.co)for v in body.data.vertices]);edges=np.array([e.vertices[:]for e in body.data.edges]);lengths=np.linalg.norm(co[edges[:,0]]-co[edges[:,1]],axis=1);region=(np.abs(co[:,0])>.25)&(co[:,2]>.55)&(co[:,1]<.7);selected=region[edges[:,0]]|region[edges[:,1]]
def stretch():
 rig.animation_data.action=bpy.data.actions['Glurak_Attack'];rows=[]
 for f in [7,13,19]:
  s.frame_set(f);o=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=o.to_mesh();pts=np.array([tuple(v.co)for v in m.vertices]);g=np.linalg.norm(pts[edges[:,0]]-pts[edges[:,1]],axis=1)-lengths;worst=np.flatnonzero(selected)[np.argmax(g[selected])];rows.append(dict(frame=f,max_edge_growth_cm=float(g[selected].max()*100),edges_over_3cm=int(sum(g[selected]>.03)),max_edge_vertices=co[edges[worst]].tolist()));o.to_mesh_clear()
 return rows
before=stretch();mat=body.data.materials[0];image=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].links[0].from_node.image;width,height=image.size;px=np.array(image.pixels[:]).reshape(height,width,4);uv=np.array([tuple(v.uv)for v in body.data.uv_layers.active.data]);vi=np.array([v.vertex_index for v in body.data.loops]);c=px[(uv[:,1]%1*(height-1)).astype(int),(uv[:,0]%1*(width-1)).astype(int),:3];valid=(c[:,1:].max(1)/(c[:,0]+.002)>1.55)&(c.max(1)<.50)&((c.max(1)-c.min(1))/(c.max(1)+.002)>.25)&region[vi];seeds=np.unique(vi[valid]);assert len(seeds)>5000
_,inverse=np.unique(np.rint(co/1e-6).astype(np.int64),axis=0,return_inverse=True);n=int(inverse.max())+1;ends=inverse[edges];ends=ends[ends[:,0]!=ends[:,1]];adj=[[]for _ in range(n)];positions=np.zeros((n,3));multiplicity=np.bincount(inverse,minlength=n);np.add.at(positions,inverse,co);positions/=multiplicity[:,None]
for a,b in ends:
 d=float(np.linalg.norm(positions[a]-positions[b]));adj[a].append((int(b),d));adj[b].append((int(a),d))
dist=np.full(n,np.inf);heap=[]
for v in np.unique(inverse[seeds]):dist[v]=0;heap.append((0.,int(v)))
heapq.heapify(heap)
while heap:
 d,i=heapq.heappop(heap)
 if d!=dist[i]or d>.30:continue
 for j,l in adj[i]:
  nd=d+l
  if nd<dist[j]and nd<.30:dist[j]=nd;heapq.heappush(heap,(nd,j))
def bone_distance(v,name):
 b=rig.data.bones[name];a=b.head_local;delta=b.tail_local-a;t=max(0,min(1,(v-a).dot(delta)/delta.length_squared));return(v-a-t*delta).length
weights=original_weights.copy();wing_indices=[i for i,name in enumerate(group_names)if name.startswith('wing_')];changed=0
for v in body.data.vertices:
 d=dist[inverse[v.index]];oldwing=original_weights[v.index,wing_indices].sum()
 if d>.25 and oldwing<1e-6:continue
 base=original_weights[v.index].copy();base[wing_indices]=0
 if base.sum()<1e-7:
  side='L'if v.co.x>0 else'R';names=['chest','head','upperarm_'+side,'forearm_'+side,'hand_'+side]
  for name in names:base[group_names.index(name)]=1/max(.015,bone_distance(v.co,name))**4
 base/=base.sum();t=max(0,min(1,(.16-d)/.10));t=t*t*(3-2*t);side='L'if v.co.x>0 else'R';wing=np.zeros(len(group_names))
 for name in ['wing_base_'+side,'wing_tip_'+side]:wing[group_names.index(name)]=1/max(.015,bone_distance(v.co,name))**4
 wing/=wing.sum();weights[v.index]=base*(1-t)+wing*t;changed+=1
# Smooth across actual welded surface neighbors, never across nearby but separate arms.
w=np.zeros((n,len(group_names)));np.add.at(w,inverse,weights);w/=multiplicity[:,None];degree=np.bincount(ends.reshape(-1),minlength=n);active=(degree>0)&(dist<.24)&(dist>.015)
for iteration in range(24):
 sums=np.zeros_like(w);np.add.at(sums,ends[:,0],w[ends[:,1]]);np.add.at(sums,ends[:,1],w[ends[:,0]]);w[active]=w[active]*.55+sums[active]/degree[active,None]*.45
order=np.argsort(w,axis=1)[:,-4:];mask=np.zeros_like(w,dtype=bool);np.put_along_axis(mask,order,True,axis=1);w*=mask;w/=w.sum(1)[:,None]
for group in body.vertex_groups:group.remove(list(range(len(body.data.vertices))))
for v in body.data.vertices:
 for index in order[inverse[v.index]]:
  value=w[inverse[v.index],index]
  if value>1e-8:body.vertex_groups[int(index)].add([v.index],float(value),'REPLACE')
after=stretch();result=dict(before=before,after=after,affected_vertices=changed,membrane_seeds=len(seeds),virtual_vertices=n,method='Original weights + membrane geodesic field, 24 iterations only in transition, max four influences; no proximity jump from wing to arm');(R/'Saved/CreaturePolishV4/WingGeodesic.json').write_text(json.dumps(result,indent=2));print('WING_GEODESIC',json.dumps(result),flush=True);assert max(v['max_edge_growth_cm']for v in after)<5,'Reject before saving: deformation still too large';assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in body.data.vertices)
rig.animation_data.action=bpy.data.actions['Glurak_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;f=A/'Exports/PolishV4/Glurak_Idle.fbx';bpy.ops.export_scene.fbx(filepath=str(f),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO',colors_type='LINEAR');bpy.ops.wm.save_as_mainfile(filepath=str(p));assert digest(original)==orig_sha;audit['source_sha256']=digest(p);audit['exports'][0]['sha256']=digest(f);audit['changes']['final_wing_skin']=result;(A/'PolishV4_Audit.json').write_text(json.dumps(audit,indent=2))
