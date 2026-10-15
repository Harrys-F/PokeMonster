import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,kdtree
from mathutils.bvhtree import BVHTree
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_Base_V2'];bpy.context.window.scene=s
body=s.objects['HNV2_Body'];bm=bmesh.new();bm.from_mesh(body.data)
seen=set();parts=[]
for v in bm.verts:
 if v in seen:continue
 todo=[v];seen.add(v);n=0
 while todo:
  q=todo.pop();n+=1
  for e in q.link_edges:
   a=e.other_vert(q)
   if a not in seen:seen.add(a);todo.append(a)
 parts.append(n)
kd=kdtree.KDTree(len(bm.verts))
for i,v in enumerate(bm.verts):kd.insert(v.co,i)
kd.balance();sym=max(kd.find(Vector((-v.co.x,v.co.y,v.co.z)))[2] for v in bm.verts)
def contours(axis,position,filterpoint=lambda p:True):
 graph={}
 def key(v):return tuple(round(x,6) for x in v)
 for f in bm.faces:
  points=[]
  for e in f.edges:
   a,b=(v.co for v in e.verts);aa=a[axis]-position;bb=b[axis]-position
   if aa*bb<0:points.append(a.lerp(b,aa/(aa-bb)))
  if len(points)!=2 or not all(filterpoint(p) for p in points):continue
  a,b=(key(p) for p in points);graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
 done=set();n=0
 for p in graph:
  if p in done:continue
  todo=[p];done.add(p);n+=1
  while todo:
   q=todo.pop()
   for a in graph[q]:
    if a not in done:done.add(a);todo.append(a)
 return n
count={'arms_left':contours(0,.4),'arms_right':contours(0,-.4),'legs':contours(2,.2),'head':contours(2,1.18),'four_fingers_left':contours(0,.735),'four_fingers_right':contours(0,-.735),'two_thumbs':contours(1,-.065,lambda p:p.z>.9 and abs(p.x)>.64),'ten_toes':contours(1,-.185,lambda p:p.z<.075)}
dg=bpy.context.evaluated_depsgraph_get();objects=[o for c in s.collection.children if c.name.startswith('HNV2_HOBBIT_') for o in c.objects if o.type=='MESH'];rows=[];z=[];categories={}
for o in objects:
 e=o.evaluated_get(dg);m=e.to_mesh();m.calc_loop_triangles();pos=[e.matrix_world@v.co for v in m.vertices];z.extend(p.z for p in pos);cat='body' if o==body else ('clothing' if any(c.name=='HNV2_HOBBIT_CLOTHING' for c in o.users_collection) else ('hair' if any(c.name=='HNV2_HOBBIT_HAIR' for c in o.users_collection) else 'face_details'))
 categories.setdefault(cat,{'meshes':0,'vertices':0,'triangles':0});categories[cat]['meshes']+=1;categories[cat]['vertices']+=len(m.vertices);categories[cat]['triangles']+=len(m.loop_triangles)
 rows.append({'object':o.name,'category':cat,'source_vertices':len(o.data.vertices),'evaluated_vertices':len(m.vertices),'triangles':len(m.loop_triangles),'materials':[x.name if x else None for x in o.data.materials],'bounds_m':[list(min(p[i] for p in pos) for i in range(3)),list(max(p[i] for p in pos) for i in range(3))]});e.to_mesh_clear()
# Sample actual garment surfaces against skin, excluding trim/nails from body acceptance.
bvh=BVHTree.FromObject(body,dg);clearance=[]
for o in objects:
 if not any(c.name=='HNV2_HOBBIT_CLOTHING' for c in o.users_collection):continue
 penetrating=[];nearest_signed=[]
 for v in o.data.vertices:
  p=o.matrix_world@v.co;hit,n,idx,dist=bvh.find_nearest(p)
  signed=(p-hit).dot(n);nearest_signed.append(signed)
  if signed<-.0006:penetrating.append(v.index)
 clearance.append({'object':o.name,'sampled_vertices':len(o.data.vertices),'negative_signed_samples_over_0_6mm':len(penetrating),'min_signed_distance_m':min(nearest_signed),'vertex_indices':penetrating[:80]})
report={'opened_file':bpy.data.filepath,'blender':bpy.app.version_string,'units':s.unit_settings.system,'unit_scale':s.unit_settings.scale_length,'height_m':max(z)-min(z),'sole_z_m':min(z),'top_z_m':max(z),'body_connected_parts':parts,'body_nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'body_boundary_edges':sum(e.is_boundary for e in bm.edges),'body_degenerate_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'body_symmetry_max_error_m':sym,'body_face_types':{'quads':sum(len(f.verts)==4 for f in bm.faces),'triangles':sum(len(f.verts)==3 for f in bm.faces),'ngons':sum(len(f.verts)>4 for f in bm.faces)},'cross_sections':count,'categories':categories,'objects':rows,'clothing_skin_vertex_distance_samples':clearance,'rigs':sum(o.type=='ARMATURE' for o in s.objects),'animated_objects':sum(bool(o.animation_data and o.animation_data.action) for o in s.objects),'shared_rig_compatibility_tested':False,'full_triangle_intersection_or_deformation_tested':False}
(BASE/'Review/V2/ReopenAudit.json').write_text(json.dumps(report,indent=2));bm.free();print(json.dumps({k:v for k,v in report.items() if k not in ['objects','clothing_skin_vertex_distance_samples']}));print('CLOTHING',json.dumps(clearance))
assert len(parts)==1 and report['body_nonmanifold_edges']==0 and report['body_boundary_edges']==0
assert abs(report['height_m']-1.32)<1e-6 and abs(min(z))<1e-6 and sym<1e-6
assert report['rigs']==0 and report['animated_objects']==0
assert count=={'arms_left':1,'arms_right':1,'legs':2,'head':1,'four_fingers_left':4,'four_fingers_right':4,'two_thumbs':2,'ten_toes':10},count
