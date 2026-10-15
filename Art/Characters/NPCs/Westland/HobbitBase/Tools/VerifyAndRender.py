"""Read-only reopen audit and native Blender previews, scoped to HobbitBase."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,kdtree
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
s=bpy.data.scenes['Hobbit_NPC_Base_V1'];bpy.context.window.scene=s
body=bpy.data.objects['HNB_Body'];bm=bmesh.new();bm.from_mesh(body.data);seen=set();groups=[]
for v in bm.verts:
 if v in seen:continue
 todo=[v];seen.add(v);count=0
 while todo:
  q=todo.pop();count+=1
  for e in q.link_edges:
   a=e.other_vert(q)
   if a not in seen:seen.add(a);todo.append(a)
 groups.append(count)
nonmanifold=sum(not e.is_manifold for e in bm.edges);boundaries=sum(e.is_boundary for e in bm.edges)
kd=kdtree.KDTree(len(bm.verts))
for i,v in enumerate(bm.verts):kd.insert(v.co,i)
kd.balance();sym=max(kd.find(Vector((-v.co.x,v.co.y,v.co.z)))[2] for v in bm.verts)
# Count closed intersection contours without modifying the saved mesh.
def slice_loops(axis,position,filterpoint=lambda p:True):
 segments=[]
 for f in bm.faces:
  points=[]
  for e in f.edges:
   a,b=(q.co for q in e.verts);aa=a[axis]-position;bb=b[axis]-position
   if aa*bb<0:
    p=a.lerp(b,aa/(aa-bb));points.append(p)
  if len(points)==2 and all(filterpoint(p) for p in points):segments.append(points)
 graph={}
 def key(p):return tuple(round(x,6) for x in p)
 for a,b in segments:
  ka,kb=key(a),key(b);graph.setdefault(ka,set()).add(kb);graph.setdefault(kb,set()).add(ka)
 visited=set();n=0
 for a in graph:
  if a in visited:continue
  n+=1;stack=[a];visited.add(a)
  while stack:
   q=stack.pop()
   for nxt in graph[q]:
    if nxt not in visited:visited.add(nxt);stack.append(nxt)
 return n
legs=slice_loops(2,.22);arm_l=slice_loops(0,.4);arm_r=slice_loops(0,-.4);head=slice_loops(2,1.18);toes=slice_loops(1,-.19,lambda p:p.z<.10)
model=[o for c in s.collection.children if c.name in ['HOBBIT_BODY','HOBBIT_CLOTHING','HOBBIT_FACE','HOBBIT_HAIR'] for o in c.objects];dg=bpy.context.evaluated_depsgraph_get();positions=[];tris=0;verts=0;rows=[]
for o in model:
 e=o.evaluated_get(dg);m=e.to_mesh();m.calc_loop_triangles();pp=[e.matrix_world@v.co for v in m.vertices];positions.extend(pp);tris+=len(m.loop_triangles);verts+=len(m.vertices);rows.append({'name':o.name,'verts':len(m.vertices),'triangles':len(m.loop_triangles),'materials':[m.name if m else None for m in o.data.materials]});e.to_mesh_clear()
lo=min(p.z for p in positions);hi=max(p.z for p in positions);report={'file_opened':bpy.data.filepath,'blender_version':bpy.app.version_string,'units':s.unit_settings.system,'unit_scale':s.unit_settings.scale_length,'height_m':hi-lo,'sole_z_m':lo,'top_z_m':hi,'body_components':groups,'nonmanifold_edges':nonmanifold,'boundary_edges':boundaries,'symmetry_max_error_m':sym,'cross_section_counts':{'left_arm':arm_l,'right_arm':arm_r,'legs':legs,'heads':head,'toe_contours':toes},'armatures':sum(o.type=='ARMATURE' for o in s.objects),'actions':sum(bool(o.animation_data and o.animation_data.action) for o in s.objects),'evaluated_model_vertices':verts,'evaluated_model_triangles':tris,'objects':rows,'saved_file_modified':False}
(BASE/'Review/ReopenAudit.json').write_text(json.dumps(report,indent=2))
assert len(groups)==1 and nonmanifold==0 and boundaries==0
assert abs((hi-lo)-1.32)<1e-6 and abs(lo)<1e-6 and sym<1e-6
assert (arm_l,arm_r,legs,head,toes)==(1,1,2,1,10),report['cross_section_counts']
(BASE/'Review/ReopenAudit.json').write_text(json.dumps(report,indent=2));bm.free()
# Preview cameras are temporary changes in this read-only Blender process; never save.
cam=s.camera;target=Vector((0,0,.66));s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.render.resolution_x=1100;s.render.resolution_y=1100;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
views=[('Front',(0,-4,.66),'ORTHO',1.85),('Back',(0,4,.66),'ORTHO',1.85),('Side_Right',(4,0,.66),'ORTHO',1.65),('Side_Left',(-4,0,.66),'ORTHO',1.65),('ThreeQuarter',(2.5,-3.5,1.7),'ORTHO',1.8),('Camera_25D_Detail',(3,-3,5.71),'PERSP',None),('Camera_25D_2850cm',(12.953,-12.953,22.492),'PERSP',None)]
paths=[]
for name,loc,kind,size in views:
 cam.location=loc;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=kind
 if size:cam.data.ortho_scale=size
 else:cam.data.lens=36/(2*math.tan(math.radians(35)/2));cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
 if name=='Camera_25D_2850cm':s.render.resolution_x=1600;s.render.resolution_y=900
 else:s.render.resolution_x=1100;s.render.resolution_y=1100
 s.render.filepath=str(BASE/'Previews'/('Hobbit_'+name+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath)
report['previews']=paths;report['render_complete']=True;(BASE/'Review/ReopenAudit.json').write_text(json.dumps(report,indent=2));print(json.dumps({'audit_passed':True,'height_m':hi-lo,'body_components':len(groups),'toe_contours':toes,'previews':paths}))
