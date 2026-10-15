import bpy,bmesh,json,math
from pathlib import Path
from collections import Counter
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_V4_HeadSculpt'];bpy.context.window.scene=s;o=next(ob for ob in s.objects if ob.name.startswith('HNV4_Body'));me=o.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()
bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table()
seen=set();parts=[]
for v in bm.verts:
 if v.index in seen:continue
 todo=[v];component=[];seen.add(v.index)
 while todo:
  q=todo.pop();component.append(q.index)
  for e in q.link_edges:
   w=e.other_vert(q)
   if w.index not in seen:seen.add(w.index);todo.append(w)
 parts.append(len(component))
kd=KDTree(len(me.vertices))
for v in me.vertices:kd.insert(v.co,v.index)
kd.balance();duplicates=[];sym=[]
for v in me.vertices:
 sym.append(kd.find(Vector((-v.co.x,v.co.y,v.co.z)))[2])
 for _,j,d in kd.find_range(v.co,1e-7):
  if j>v.index:duplicates.append([v.index,j,float(d)])
me.calc_loop_triangles();tris=[tuple(t.vertices) for t in me.loop_triangles];verts=[v.co.copy() for v in me.vertices]
bvh=BVHTree.FromPolygons(verts,tris,all_triangles=True,epsilon=1e-8)
def seg_tri(p,q,a,b,c):
 d=q-p;e1=b-a;e2=c-a;h=d.cross(e2);det=e1.dot(h)
 if abs(det)<1e-12:return False
 inv=1/det;ss=p-a;u=ss.dot(h)*inv
 if u<1e-7 or u>1-1e-7:return False
 k=ss.cross(e1);v=d.dot(k)*inv
 if v<1e-7 or u+v>1-1e-7:return False
 t=e2.dot(k)*inv;return 1e-6<t<1-1e-6
intersections=[];tested=0
for i,j in bvh.overlap(bvh):
 if i>=j or set(tris[i])&set(tris[j]):continue
 aa=[verts[k] for k in tris[i]];bb=[verts[k] for k in tris[j]];tested+=1
 if any(seg_tri(aa[k],aa[(k+1)%3],*bb) for k in range(3)) or any(seg_tri(bb[k],bb[(k+1)%3],*aa) for k in range(3)):intersections.append([i,j])
def section(axis,pos,filterfun):
 # Trace genuine polygon/plane intersections and count disconnected contours.
 edges=[]
 for p in me.polygons:
  points=[];ids=list(p.vertices)
  for a,b in zip(ids,ids[1:]+ids[:1]):
   pa,pb=verts[a],verts[b];da,db=pa[axis]-pos,pb[axis]-pos
   if da*db<0:
    hit=pa.lerp(pb,da/(da-db))
    if filterfun(hit):points.append(hit)
  if len(points)==2:edges.append(points)
 nodes={};links={}
 for pp in edges:
  keys=[tuple(round(float(x),6) for x in p) for p in pp]
  for key in keys:nodes[key]=1;links.setdefault(key,set())
  links[keys[0]].add(keys[1]);links[keys[1]].add(keys[0])
 seen=set();count=0
 for key in nodes:
  if key in seen:continue
  count+=1;todo=[key];seen.add(key)
  while todo:
   for near in links[todo.pop()]:
    if near not in seen:seen.add(near);todo.append(near)
 return count
sections={'head':section(2,1.240,lambda p:True),'legs':section(2,.456,lambda p:True),'left_arm':section(0,.470,lambda p:True),'right_arm':section(0,-.470,lambda p:True),'four_fingers_left':section(0,.712,lambda p:p.z>.9),'four_fingers_right':section(0,-.712,lambda p:p.z>.9),'thumbs':section(1,-.087,lambda p:abs(p.x)>.61 and p.z>.9),'ten_toes':section(1,-.162,lambda p:p.z<.08)}
face_types=Counter('quads' if len(f.verts)==4 else 'triangles' if len(f.verts)==3 else 'ngons' for f in bm.faces)
models=[]
for col in s.collection.children:
 if not (col.name.startswith('HNV4_BODY') or col.name.startswith('HNV4_EYES')):continue
 for ob in col.objects:
  if ob.type!='MESH':continue
  ob.data.calc_loop_triangles();models.append({'name':ob.name,'vertices':len(ob.data.vertices),'faces':len(ob.data.polygons),'triangles':len(ob.data.loop_triangles),'materials':[m.name for m in ob.data.materials]})
winding_errors=0
for e in bm.edges:
 ll=list(e.link_loops)
 if len(ll)==2 and not (ll[0].vert==ll[1].link_loop_next.vert and ll[0].link_loop_next.vert==ll[1].vert):winding_errors+=1
result={'source':bpy.data.filepath,'blender':bpy.app.version_string,'units':s.unit_settings.system,'unit_scale':s.unit_settings.scale_length,'body_height_m':max(v.co.z for v in me.vertices)-min(v.co.z for v in me.vertices),'sole_z_m':min(v.co.z for v in me.vertices),'future_hair_allowance_m':1.32-max(v.co.z for v in me.vertices),'body_components':parts,'body_vertices':len(me.vertices),'body_faces':len(me.polygons),'body_triangles':len(tris),'body_face_types':dict(face_types),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'boundary_edges':sum(e.is_boundary for e in bm.edges),'loose_vertices':sum(not v.link_faces for v in bm.verts),'degenerate_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'duplicate_vertex_pairs_0_1um':duplicates,'symmetry_max_m':max(sym),'signed_volume_m3':bm.calc_volume(signed=True),'euler_characteristic':len(bm.verts)-len(bm.edges)+len(bm.faces),'shared_edge_winding_errors':winding_errors,'invalid_face_normals':sum(not all(math.isfinite(v) for v in f.normal) or f.normal.length<.99 for f in bm.faces),'cross_sections':sections,'nonadjacent_triangle_pairs_tested':tested,'proper_triangle_intersections':intersections,'intersection_test_limits':'Interior segment/triangle crossings; excludes shared-vertex pairs, coplanar overlaps and tangential contacts. Not a formal exhaustive proof. Eyeball/body seating is intentional and separate.','model_objects':models,'rigs':sum(ob.type=='ARMATURE' for ob in s.objects),'animated_objects':sum(ob.animation_data is not None for ob in s.objects),'deformation_tested':False,'body_modifier_types':[m.type for m in o.modifiers]}
# Compare protected body and eyeballs against the saved, untouched V3 copy.
ref=next(ob for ob in s.objects if ob.name.startswith('REF_V3_HNV3_Body'))
protected=[v.co for v in ref.data.vertices if v.co.z<=1.067 or abs(v.co.x)>=.18]
result['protected_original_vertices']=len(protected)
result['protected_vertex_max_error_m']=max(kd.find(p)[2] for p in protected)
result['eye_checks']=[]
for side in ['L','R']:
 eye=next(ob for ob in s.objects if ob.name.startswith('HNV4_Eyeball_'+side))
 old=next(ob for ob in s.objects if ob.name.startswith('REF_V3_HNV3_Eyeball_'+side))
 result['eye_checks'].append({'side':side,'vertex_count_equal':len(eye.data.vertices)==len(old.data.vertices),'max_vertex_difference_m':max((v.co-w.co).length for v,w in zip(eye.data.vertices,old.data.vertices)),'transform_equal':eye.matrix_world==old.matrix_world})
mask=o.data.attributes['.sculpt_mask'];result['protected_mask_min']=min(mask.data[v.index].value for v in o.data.vertices if v.co.z<=1.067 or abs(v.co.x)>=.18)
result['shape_keys']=[k.name for k in o.data.shape_keys.key_blocks]
result['sculpt_symmetry_x']=s.tool_settings.sculpt.use_symmetry_x
result['native_brush']=s.tool_settings.sculpt.brush.name if s.tool_settings.sculpt.brush else None
bm.free();(BASE/'Review/V4/ReopenAudit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['proper_triangle_intersections','duplicate_vertex_pairs_0_1um','model_objects']},indent=2));print('Intersection pairs',len(intersections))
assert len(parts)==1 and result['nonmanifold_edges']==0 and result['boundary_edges']==0
assert result['protected_vertex_max_error_m']<1e-7
assert result['symmetry_max_m']<1e-6
assert abs(result['body_height_m']-1.282)<1e-6
assert all(e['max_vertex_difference_m']==0 and e['transform_equal'] for e in result['eye_checks'])
