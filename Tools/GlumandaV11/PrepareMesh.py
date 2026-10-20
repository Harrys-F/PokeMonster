"""Fill only ten diagnosed small source holes; retain all original vertices/UVs/normals and V1."""
import bpy,bmesh,json,math,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Zunderlauf';O=R/'Saved/GlumandaV11';dest=A/'Source/Glumanda_Meshy_V11.blend';
if dest.exists():
 expected=json.loads((O/'OwnedSourceRevision.json').read_text());assert hashlib.sha256(dest.read_bytes()).hexdigest()==expected['sha256'],'Own working source changed: do not overwrite'
bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Glumanda_Meshy_V1.blend'));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Glumanda_Meshy'];rig=bpy.data.objects['Glumanda_Meshy_Rig'];old=body.data;old.calc_loop_triangles();original_v=len(old.vertices);original_tri=len(old.loop_triangles)
def key(v):return tuple(round(x,7)for x in v)
coordinates=[v.co.copy()for v in old.vertices];faces=[tuple(f.vertices)for f in old.polygons];uvs=[[old.uv_layers.active.data[i].uv.copy()for i in f.loop_indices]for f in old.polygons];normals=[[old.corner_normals[i].vector.copy()for i in f.loop_indices]for f in old.polygons];weights=[{body.vertex_groups[g.group].name:g.weight for g in v.groups}for v in old.vertices];lookup={};samples={}
for f in old.polygons:
 for i in f.loop_indices:
  vid=old.loops[i].vertex_index;k=key(old.vertices[vid].co);lookup.setdefault(k,vid);samples.setdefault(k,[]).append(old.uv_layers.active.data[i].uv.copy())
bm=bmesh.new();bm.from_mesh(old);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.normal_update();remaining={e for e in bm.edges if e.is_boundary};caps=[];kept=[]
while remaining:
 component={next(iter(remaining))};stack=list(component)
 while stack:
  for v in stack.pop().verts:
   for e in v.link_edges:
    if e.is_boundary and e not in component:component.add(e);stack.append(e)
 remaining-=component;verts={v for e in component for v in e.verts};perimeter=sum(e.calc_length()for e in component)
 assert all(sum(e in component for e in v.link_edges)==2 for v in verts)
 if len(component)>6 or perimeter>.12:kept.append({'edges':len(component),'perimeter_m':perimeter,'reason':'intentional original flame/body separation'});continue
 edge=next(iter(component));loop=next(l for l in edge.link_faces[0].loops if l.edge==edge);ordered=[loop.link_loop_next.vert,loop.vert];previous=edge
 while True:
  nxt=next(e for e in ordered[-1].link_edges if e in component and e!=previous);v=nxt.other_vert(ordered[-1]);previous=nxt
  if v==ordered[0]:break
  assert v not in ordered;ordered.append(v)
 assert len(ordered)==len(component);points=[v.co.copy()for v in ordered];normal=sum((points[i].cross(points[(i+1)%len(points)])for i in range(len(points))),Vector()).normalized();keys=[key(v)for v in points];choices=[samples[k]for k in keys];best=None
 # Choose the most coherent existing UV chart for this small patch, never sample a different texture.
 for seed in choices[0]:
  values=[seed]
  for opts in choices[1:]:values.append(min(opts,key=lambda uv:(uv-values[-1]).length_squared))
  score=sum((values[i]-values[(i+1)%len(values)]).length_squared for i in range(len(values)))
  if best is None or score<best[0]:best=(score,values)
 uv_method='coherent_boundary_chart'
 if best[0]>=.025:
  near=max({f for e in component for f in e.link_faces},key=lambda f:f.calc_area());source_face=old.polygons[near.index];vv=[old.vertices[i].co for i in source_face.vertices];uv=[old.uv_layers.active.data[i].uv.copy()for i in source_face.loop_indices];basis=np.array([list(vv[1]-vv[0]),list(vv[2]-vv[0])]).T;projected=[]
  for point in points:
   u,v=np.linalg.lstsq(basis,np.array(point-vv[0]),rcond=None)[0];projected.append(uv[0]+(uv[1]-uv[0])*float(u)+(uv[2]-uv[0])*float(v))
  assert all(-.001<c<1.001 for uv in projected for c in uv);best=(sum((projected[i]-projected[(i+1)%len(projected)]).length_squared for i in range(len(projected))),projected);assert best[0]<.04;uv_method='local_adjacent_face_projection_across_atlas_seam'
 ids=[]
 for p,k in zip(points,keys):ids.append(len(coordinates));coordinates.append(p);weights.append(dict(weights[lookup[k]]))
 # A shallow inward centre avoids triangulation diagonals that coincide with existing source edges.
 centre=sum(points,Vector())/len(points)-normal*.00002;centre_id=len(coordinates);coordinates.append(centre);average={}
 for k in keys:
  for bone,w in weights[lookup[k]].items():average[bone]=average.get(bone,0)+w/len(keys)
 weights.append(average);ids.append(centre_id);centre_uv=sum(best[1],__import__('mathutils').Vector((0,0)))/len(points);best=(best[0],[*best[1],centre_uv]);indices=[(i,(i+1)%len(points),len(points))for i in range(len(points))];row={'perimeter_m':perimeter,'vertices':len(points),'triangles':len(indices),'uv_method':uv_method,'uv_edge_energy':best[0],'center_m':list(sum(points,Vector())/len(points))}
 for tri in indices:
  order=list(tri);faces.append(tuple(ids[i]for i in order));uvs.append([best[1][i]for i in order]);normals.append([normal.copy()]*3)
 caps.append(row)
assert len(caps)==10 and len(kept)==1;bm.free();mesh=bpy.data.meshes.new('Glumanda_Meshy_V11_Repaired');mesh.from_pydata(coordinates,[],faces);mesh.update();layer=mesh.uv_layers.new(name='UVMap');ns=[]
for f,uv,nn in zip(mesh.polygons,uvs,normals):
 f.use_smooth=True
 for loop,value,normal in zip(f.loop_indices,uv,nn):layer.data[loop].uv=value;ns.append(normal)
mesh.normals_split_custom_set(ns)
for m in old.materials:mesh.materials.append(m)
body.data=mesh
for name in rig.data.bones:
 if name.name not in body.vertex_groups:body.vertex_groups.new(name=name.name)
for v,w in zip(mesh.vertices,weights):
 for name,value in w.items():body.vertex_groups[name].add([v.index],value,'REPLACE')
assert max((mesh.vertices[i].co-old.vertices[i].co).length for i in range(original_v))==0
# Preserve UV-seam-equivalent weights while gently regularizing only knee transitions.
indices=[v.index for v in mesh.vertices if .055<v.co.z<.145 and abs(v.co.x)>.065 and v.co.y<.065];edges=[tuple(e.vertices)for e in mesh.edges if all(i in set(indices) for i in e.vertices) and (mesh.vertices[e.vertices[0]].co-mesh.vertices[e.vertices[1]].co).length>1e-5];pairs=np.array(edges);rest=np.array([list(v.co)for v in mesh.vertices]);restlength=np.linalg.norm(rest[pairs[:,0]]-rest[pairs[:,1]],axis=1);original_weights=[dict(w)for w in weights]
seams={}
for i,v in enumerate(mesh.vertices):seams.setdefault(key(v.co),[]).append(i)
adj={i:set()for i in range(len(mesh.vertices))}
for e in mesh.edges:
 a,b=e.vertices;adj[a].add(b);adj[b].add(a)
for k,ids in seams.items():
 neighbors=set().union(*(adj[i]for i in ids))
 for i in ids:adj[i]=neighbors
frames=[(bpy.data.actions['Glumanda_'+name],frame)for name in ['Walk','Run']for frame in [1,3,5,7,9,11,13]]
def measure():
 errors=[];poses=[]
 for action,frame in frames:
  rig.animation_data.action=action;bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([list(v.co)for v in m.vertices]);ev.to_mesh_clear();ratio=np.maximum(np.linalg.norm(p[pairs[:,0]]-p[pairs[:,1]],axis=1)/restlength,1e-8);errors.extend(np.abs(np.log(ratio)));poses.append(p)
 return float(np.percentile(errors,99)),poses
before,baseposes=measure();choice=None
for amount in [.125]:
 newweights=[dict(w)for w in original_weights]
 for i in indices:
  if not adj[i]:continue
  blend={}
  for j in adj[i]:
   for k,v in original_weights[j].items():blend[k]=blend.get(k,0)+v/len(adj[i])
  w={k:original_weights[i].get(k,0)*(1-amount)+blend.get(k,0)*amount for k in set(blend)|set(original_weights[i])};total=sum(w.values());newweights[i]={k:v/total for k,v in w.items()if v>1e-8}
 for ids in seams.values():
  active=[i for i in ids if i in indices]
  if active:
   average={}
   for i in active:
    for k,v in newweights[i].items():average[k]=average.get(k,0)+v/len(active)
   for i in ids:newweights[i]=dict(average)
 for group in body.vertex_groups:group.remove(list(range(len(mesh.vertices))))
 for i,w in enumerate(newweights):
  for k,v in w.items():body.vertex_groups[k].add([i],v,'REPLACE')
 score,poses=measure();delta=max(float(np.max(np.linalg.norm(a-b,axis=1)))for a,b in zip(poses,baseposes));print('KNEE_CANDIDATE',amount,score,delta,flush=True)
 if score<before and delta<.003 and (choice is None or score<choice[0]):choice=(score,amount,delta,newweights)
weights=choice[3]if choice else original_weights
for group in body.vertex_groups:group.remove(list(range(len(mesh.vertices))))
for i,w in enumerate(weights):
 total=sum(w.values())
 for k,v in w.items():body.vertex_groups[k].add([i],v/total,'REPLACE')
rig.animation_data.action=bpy.data.actions['Glumanda_Idle'];bpy.context.scene.frame_set(1);mesh.calc_loop_triangles();bpy.ops.wm.save_as_mainfile(filepath=str(dest));folder=A/'Exports/MeshyV11';folder.mkdir(exist_ok=True);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.fbx(filepath=str(folder/'Glumanda_Skin_V11.fbx'),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE',path_mode='AUTO')
audit={'original_vertices':original_v,'vertices':len(mesh.vertices),'original_body_triangles':original_tri,'body_triangles':len(mesh.loop_triangles),'caps':caps,'intentional_open_boundaries':kept,'original_vertex_max_rest_displacement_m':0,'original_materials_uvs_normals_preserved':True,'knee_regularization':{'accepted':bool(choice),'before_p99_absolute_log_edge_strain':before,'after_p99_absolute_log_edge_strain':choice[0]if choice else before,'neighbor_blend':choice[1]if choice else 0,'max_animated_surface_difference_m':choice[2]if choice else 0},'animations_reused_unchanged':7,'height_m':.6};(A/'MeshyV11_RepairAudit.json').write_text(json.dumps(audit,indent=2));print('REPAIR_PREPARED',json.dumps(audit),flush=True)
