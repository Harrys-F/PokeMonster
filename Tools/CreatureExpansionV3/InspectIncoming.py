"""Read-only, anatomical intake. Diagnostic renders are not Unreal acceptance evidence."""
import bpy,bmesh,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];O=R/'Saved/CreatureExpansionV3/Intake';O.mkdir(exist_ok=False)
for name,height in [('Pikachu',.4),('Myrapla',.5),('Enton',.8),('Machomei',1.6),('Nebulak',1.3),('Gengar',1.5),('Glurak',1.7)]:
 bpy.ops.wm.read_factory_settings(use_empty=True);source=R/'Art/Characters/Creatures/Incoming'/(name+'.glb');digest=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.import_scene.gltf(filepath=str(source));objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[o.matrix_world@v.co for o in objects for v in o.data.vertices];mn=Vector(tuple(min(p[i]for p in pts)for i in range(3)));mx=Vector(tuple(max(p[i]for p in pts)for i in range(3)));center=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z));scale=height/(mx.z-mn.z);rows=[]
 for body in objects:
  m=body.data;m.calc_loop_triangles();points=[(body.matrix_world@v.co-center)*scale for v in m.vertices];bm=bmesh.new();bm.from_mesh(m)
  rows.append(dict(name=body.name,vertices=len(m.vertices),triangles=len(m.loop_triangles),materials=[{'name':s.name,'blend':s.surface_render_method if hasattr(s,'surface_render_method')else None,'nodes':[n.bl_idname for n in s.node_tree.nodes]}for s in m.materials],uv_layers=[u.name for u in m.uv_layers],boundary_edges=sum(e.is_boundary for e in bm.edges),nonmanifold=sum(not e.is_manifold for e in bm.edges),degenerate=sum(f.calc_area()<1e-12 for f in bm.faces)))
  bm.free()
  for v,p in zip(m.vertices,points):v.co=p
  body.matrix_world.identity();m.update()
 row=dict(species_filename=name,source=str(source.relative_to(R)),sha256=digest,source_bounds=[list(mn),list(mx)],diagnostic_uniform_scale=scale,assumed_total_height_m=height,meshes=rows,rigs=[o.name for o in bpy.data.objects if o.type=='ARMATURE'],actions=[a.name for a in bpy.data.actions],textures=[dict(name=i.name,size=list(i.size),packed=bool(i.packed_file))for i in bpy.data.images if i.type=='IMAGE'],normalized_bounds=[[min((p-center)[i]*scale for p in pts)for i in range(3)],[max((p-center)[i]*scale for p in pts)for i in range(3)]])
 (O/(name+'.json')).write_text(json.dumps(row,indent=2))
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('IntakeWorld');s.world.color=(.25,.25,.25)
 for loc,power,size in [((2,-3,4),550,4),((-3,-1,3),350,3),((1,3,3),400,3)]:
  bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.size=size;l.rotation_euler=(Vector((0,0,height/2))-l.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=max(height*1.4,(mx.x-mn.x)*scale*1.2,(mx.y-mn.y)*scale*1.2)
 for view,loc in [('Front',(0,-4,height*.65)),('Side',(4,0,height*.65)),('Back',(0,4,height*.65))]:
  cam.location=loc;cam.rotation_euler=(Vector((0,0,height/2))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(name+'_'+view+'.png'));bpy.ops.render.render(write_still=True)
 assert hashlib.sha256(source.read_bytes()).hexdigest()==digest;print('INTAKE_DONE',name,flush=True)
