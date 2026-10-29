"""Read-only Meshy intake. No mesh is authored and no original file is saved."""
import bpy,bmesh,json,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/RaichuMeshyCorrection';source=R/'Art/Characters/Creatures/Incoming/Raichu.glb';sha=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source));objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in objects for v in o.data.vertices];mn=Vector([min(p[i]for p in points)for i in range(3)]);mx=Vector([max(p[i]for p in points)for i in range(3)]);origin=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z));scale=.8/(mx.z-mn.z);rows=[]
for o in objects:
 m=o.data;m.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(m);rows.append({'name':o.name,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'uv_layers':len(m.uv_layers),'materials':len(m.materials),'boundary_edges':sum(e.is_boundary for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces)});bm.free();newpoints=[(o.matrix_world@v.co-origin)*scale for v in m.vertices]
 for v,p in zip(m.vertices,newpoints):v.co=p
 o.matrix_world=Matrix.Identity(4)
row={'source':str(source.relative_to(R)),'sha256':sha,'original_bounds':[list(mn),list(mx)],'normalization_scale':scale,'normalized_bounds':[[min((p-origin)[i]*scale for p in points)for i in range(3)],[max((p-origin)[i]*scale for p in points)for i in range(3)]],'meshes':rows,'rigs':sum(o.type=='ARMATURE'for o in bpy.data.objects),'actions':len(bpy.data.actions),'images':[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file)}for im in bpy.data.images if im.type=='IMAGE']};(D/'SourceIntake.json').write_text(json.dumps(row,indent=2))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('ReadOnlyMeshyReview');s.world.color=(.3,.3,.3)
for loc,power in [((2,-3,4),400),((-2,1,3),250)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=3;o.rotation_euler=(Vector((0,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();c=bpy.context.object;c.data.type='ORTHO';c.data.ortho_scale=1.25;s.camera=c
for name,loc in [('Front',(0,-3,.7)),('Side',(3,0,.7)),('Back',(0,3,.7)),('Game',(2,-2,3))]:
 c.location=loc;c.rotation_euler=(Vector((0,0,.4))-c.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(D/('Intake_'+name+'.png'));bpy.ops.render.render(write_still=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha;print('MESHY_INTAKE_COMPLETE',row)
