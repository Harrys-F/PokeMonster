"""Read original GLBs without saving sources. Diagnostic Blender views are not Unreal evidence."""
import bpy,bmesh,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];O=R/'Saved/BiomeTestV11/Intake';O.mkdir(exist_ok=False)
for name in ['Karpador','Garados','Raupy','Hornliu','Smettbo','Bibor','Habitak']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 source=R/'Art/Characters/Creatures/Incoming'/(name+'.glb');digest=hashlib.sha256(source.read_bytes()).hexdigest()
 bpy.ops.import_scene.gltf(filepath=str(source));meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
 mn=Vector(tuple(min(p[i]for p in pts)for i in range(3)));mx=Vector(tuple(max(p[i]for p in pts)for i in range(3)));size=mx-mn;centre=(mn+mx)*.5;scale=1/max(size);rows=[]
 for o in meshes:
  me=o.data;me.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me)
  rows.append(dict(name=o.name,vertices=len(me.vertices),triangles=len(me.loop_triangles),materials=[m.name for m in me.materials],uv_layers=[u.name for u in me.uv_layers],boundary_edges=sum(e.is_boundary for e in bm.edges),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),degenerate_faces=sum(f.calc_area()<1e-12 for f in bm.faces)));bm.free()
  points=[(o.matrix_world@v.co-centre)*scale for v in me.vertices]
  o.matrix_world.identity()
  for v,p in zip(me.vertices,points):v.co=p
  me.update()
 (O/(name+'.json')).write_text(json.dumps(dict(name=name,source=str(source.relative_to(R)),sha256=digest,raw_bounds=[list(mn),list(mx)],raw_size=list(size),meshes=rows,rigs=[o.name for o in bpy.data.objects if o.type=='ARMATURE'],actions=[a.name for a in bpy.data.actions],textures=[dict(name=i.name,size=list(i.size),packed=bool(i.packed_file))for i in bpy.data.images if i.type=='IMAGE']),indent=2))
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('IntakeWorld');s.world.color=(.2,.2,.2)
 for loc,power in [((2,-3,4),500),((-3,-1,3),320),((1,3,3),350)]:
  bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.size=4;l.rotation_euler=(-l.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.25
 for view,loc in [('Front',(0,-4,.5)),('Side',(4,0,.5)),('Back',(0,4,.5))]:
  cam.location=loc;cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(name+'_'+view+'.png'));bpy.ops.render.render(write_still=True)
 assert hashlib.sha256(source.read_bytes()).hexdigest()==digest;print('INTAKE_V11_DONE',name,flush=True)
