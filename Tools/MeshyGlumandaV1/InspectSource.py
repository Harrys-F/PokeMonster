"""Inspect/render only the identified input. No original geometry or material changes saved."""
import bpy,math,json,bmesh
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];O=R/'Saved/MeshyGlumandaV1';source=R/'Art/Characters/Creatures/Incoming/Glumanda.glb'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete();bpy.ops.import_scene.gltf(filepath=str(source));body=next(o for o in bpy.context.scene.objects if o.type=='MESH');bpy.context.view_layer.update();coords=[body.matrix_world@v.co for v in body.data.vertices];mn=Vector(tuple(min(v[i]for v in coords)for i in range(3)));mx=Vector(tuple(max(v[i]for v in coords)for i in range(3)));center=(mn+mx)/2;scale=.6/(mx.z-mn.z)
body.matrix_world.translation-=Vector((center.x,center.y,mn.z));body.scale*=scale;body.location*=scale;bpy.context.view_layer.update()
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=800;s.render.resolution_y=900;s.render.resolution_percentage=100;s.world.color=(.2,.2,.2)
for loc,power,size in [((1,-2,3),180,3),((-2,-1,2),100,2),((1,2,2),200,2)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,.3))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.05
for name,loc in [('Front',(0,-2,.7)),('Back',(0,2,.7)),('Side',(2,0,.7)),('Quarter',(1,-2,1))]:
 cam.location=loc;cam.rotation_euler=(Vector((0,0,.30))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/('Input_'+name+'.png'));bpy.ops.render.render(write_still=True)
bm=bmesh.new();bm.from_mesh(body.data);seen=set();islands=[]
for v in bm.verts:
 if v in seen:continue
 todo=[v];seen.add(v);rows=[]
 while todo:
  u=todo.pop();rows.append(u)
  for e in u.link_edges:
   q=e.other_vert(u)
   if q not in seen:seen.add(q);todo.append(q)
 islands.append({'vertices':len(rows),'center':list(sum((body.matrix_world@u.co for u in rows),Vector())/len(rows))})
result={'original_min':list(mn),'original_max':list(mx),'scale_to_60cm':scale,'islands':sorted(islands,key=lambda a:-a['vertices']),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_nonboundary_edges':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'textures':[{'name':im.name,'size':list(im.size),'colorspace':im.colorspace_settings.name} for im in bpy.data.images]};bm.free();(O/'GeometryInspection.json').write_text(json.dumps(result,indent=2));print('SOURCE_INSPECTED')
