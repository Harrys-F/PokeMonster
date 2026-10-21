"""Read-only Meshy inspection. Views and measurements stay in ignored Saved/."""
import bpy,bmesh,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];label=sys.argv[sys.argv.index('--')+1]if '--'in sys.argv else'Inspection';assert label.isalnum();O=R/'Saved/StarterExpansionV1'/label;O.mkdir(parents=True,exist_ok=False)
for name,file,height in [('Schiggy','Shiggy.glb',.5),('Bisasam','Bisasam.glb',.7)]:
 bpy.ops.wm.read_factory_settings(use_empty=True);source=R/'Art/Characters/Creatures/Incoming'/file;digest=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.import_scene.gltf(filepath=str(source));objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(objects)==1;body=objects[0];m=body.data;m.calc_loop_triangles();points=[body.matrix_world@v.co for v in m.vertices];mn=Vector(tuple(min(p[i]for p in points)for i in range(3)));mx=Vector(tuple(max(p[i]for p in points)for i in range(3)));center=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z));scale=height/(mx.z-mn.z);body.location-=center;body.scale*=scale;body.location*=scale;bpy.context.view_layer.update()
 bm=bmesh.new();bm.from_mesh(m);seen=set();islands=[]
 for v in bm.verts:
  if v in seen:continue
  seen.add(v);todo=[v];verts=[]
  while todo:
   u=todo.pop();verts.append(u)
   for e in u.link_edges:
    q=e.other_vert(u)
    if q not in seen:seen.add(q);todo.append(q)
  pts=[(body.matrix_world@u.co) for u in verts];islands.append({'vertices':len(verts),'min':[min(p[i]for p in pts)for i in range(3)],'max':[max(p[i]for p in pts)for i in range(3)]})
 result={'file':str(source.relative_to(R)),'sha256':digest,'meshes':len(objects),'vertices':len(m.vertices),'polygons':len(m.polygons),'triangles':len(m.loop_triangles),'source_bounds':[list(mn),list(mx)],'scale':scale,'height_m':height,'normalized_bounds':[[min((p-center)[i]*scale for p in points)for i in range(3)],[max((p-center)[i]*scale for p in points)for i in range(3)]],'materials':len(m.materials),'uv_layers':[u.name for u in m.uv_layers],'armatures':[o.name for o in bpy.context.scene.objects if o.type=='ARMATURE'],'actions':len(bpy.data.actions),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'islands':sorted(islands,key=lambda x:-x['vertices']),'images':[{'name':i.name,'size':list(i.size)}for i in bpy.data.images]};bm.free();(O/(name+'.json')).write_text(json.dumps(result,indent=2))
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.render.resolution_x=900;s.render.resolution_y=900;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('InspectionWorld');s.world.color=(.18,.18,.18)
 for loc,power,size in [((1,-2,3),220,3),((-2,-1,2),140,2),((1,2,2),220,2)]:
  bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,height/2))-l.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=height*1.7
 for view,loc in [('Front',(0,-2,height*.65)),('Side',(2,0,height*.65)),('Back',(0,2,height*.65)),('Quarter',(1,-2,height*1.2))]:
  cam.location=loc;cam.rotation_euler=(Vector((0,0,height/2))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(name+'_'+view+'.png'));bpy.ops.render.render(write_still=True)
 assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
 print('MODEL_INSPECTED',name,json.dumps({k:result[k]for k in ['vertices','triangles','source_bounds','normalized_bounds','boundary_edges','zero_area_faces']}),flush=True)
