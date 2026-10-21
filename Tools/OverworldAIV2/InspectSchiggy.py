"""Read-only seam-aware topology diagnosis; temporary welded copy is never saved."""
import bpy,bmesh,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];O=R/('Saved/OverworldAIV2/SchiggyLinearFinal'if '--linear-final'in sys.argv else'Saved/OverworldAIV2/SchiggyLocalFinal'if '--local-final'in sys.argv else'Saved/OverworldAIV2/SchiggyCaps'if '--caps'in sys.argv else'Saved/OverworldAIV2/SchiggyFinal'if '--final'in sys.argv else'Saved/OverworldAIV2/SchiggyRepaired'if '--repaired'in sys.argv else'Saved/OverworldAIV2/SchiggyDiagnosis');O.mkdir(exist_ok=False);source=R/('Art/Characters/Creatures/Schiggy/Source/Schiggy_Surface_V2.blend'if '--repaired'in sys.argv or '--final'in sys.argv or '--caps'in sys.argv or '--local-final'in sys.argv or '--linear-final'in sys.argv else'Art/Characters/Creatures/Schiggy/Source/Schiggy_Meshy_V1.blend');digest=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));body=bpy.data.objects['Schiggy_Body'];rig=bpy.data.objects['Schiggy_Rig'];rig.animation_data.action=bpy.data.actions['Schiggy_Idle'];bpy.context.scene.frame_set(1);bm=bmesh.new();bm.from_mesh(body.data);original={'vertices':len(bm.verts),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces)};bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bm.normal_update();bound={e for e in bm.edges if e.is_boundary};loops=[]
while bound:
 first=bound.pop();todo=[first];edges=[];seen=set()
 while todo:
  e=todo.pop()
  if e in seen:continue
  seen.add(e);edges.append(e)
  for v in e.verts:
   for n in v.link_edges:
    if n in bound:bound.remove(n);todo.append(n)
 vs={v for e in edges for v in e.verts};pts=[v.co for v in vs];loops.append({'edges':len(edges),'center':list(sum(pts,Vector())/len(pts)),'min':[min(p[i]for p in pts)for i in range(3)],'max':[max(p[i]for p in pts)for i in range(3)],'points':[list(p)for p in pts]})
r={'source_sha256':digest,'original':original,'welded_vertices':len(bm.verts),'welded_nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'welded_zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'holes':sorted(loops,key=lambda x:-x['edges'])};bm.free();(O/'Topology.json').write_text(json.dumps(r,indent=2));s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.render.resolution_x=s.render.resolution_y=1000;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('DiagnosisWorld');s.world.color=(.20,.20,.20)
for loc,power in [((1,-2,2),160),((-2,-1,1),120)]:
 bpy.ops.object.light_add(type='AREA',location=loc);a=bpy.context.object;a.data.energy=power;a.data.size=2;a.rotation_euler=(Vector((0,-.1,.32))-a.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(.17,-1.4,.43));cam=bpy.context.object;cam.rotation_euler=(Vector((0,-.12,.355))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.34;s.camera=cam
for label in ['Original','WithoutNormal','Clay']:
 if label=='WithoutNormal':
  for mat in body.data.materials:
   if mat.use_nodes:
    for n in mat.node_tree.nodes:
     if n.type=='BSDF_PRINCIPLED':
      for link in list(n.inputs['Normal'].links):mat.node_tree.links.remove(link)
 if label=='Clay':
  clay=bpy.data.materials.new('DiagnosticClay');clay.diffuse_color=(.38,.38,.38,1);body.data.materials.clear();body.data.materials.append(clay)
 s.render.filepath=str(O/(label+'.png'));bpy.ops.render.render(write_still=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==digest;print('SCHIGGY_DIAGNOSIS',original,'welded_holes',len(loops),'maximum',max([len(x['points'])for x in loops],default=0),flush=True)
