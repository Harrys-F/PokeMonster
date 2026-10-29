"""Read-only original GLB mesh/material/UV audit plus small actual Blender preview renders."""
import bpy,bmesh,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/ModelsV4/Incoming';D.mkdir(parents=True,exist_ok=True);rows=[]
for p in sorted((R/'Art/Characters/Creatures/Incoming').glob('*.glb')):
 digest=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(p));objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[o.matrix_world@v.co for o in objects for v in o.data.vertices];mn=Vector([min(x[i]for x in pts)for i in range(3)]);mx=Vector([max(x[i]for x in pts)for i in range(3)]);row={'name':p.stem,'source':str(p.relative_to(R)),'sha256':digest,'original_bounds':[list(mn),list(mx)],'meshes':[],'rigs':sum(o.type=='ARMATURE'for o in bpy.data.objects),'animations':len(bpy.data.actions),'images':[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file)}for im in bpy.data.images if im.type=='IMAGE']}
 for o in objects:
  m=o.data;m.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(m);row['meshes'].append({'name':o.name,'triangles':len(m.loop_triangles),'materials':[x.name for x in m.materials],'uv_layers':len(m.uv_layers),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces)});bm.free()
 # Normalize only transient diagnostic copy; original GLB is never saved/replaced.
 scale=1/max(mx-mn);center=(mx+mn)/2
 for o in objects:
  for v in o.data.vertices:v.co=(o.matrix_world@v.co-center)*scale
  o.matrix_world.identity()
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=6;s.render.resolution_x=384;s.render.resolution_y=384;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('ReadOnlyIntake');s.world.color=(.35,.35,.35)
 for loc,power in [((2,-3,4),450),((-2,1,3),250)]:
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=3;o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add(location=(1.7,-3,1.4));c=bpy.context.object;c.rotation_euler=(-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=1.35;s.camera=c;s.render.filepath=str(D/(p.stem+'.png'));bpy.ops.render.render(write_still=True)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest;rows.append(row);(D/'Inventory.json').write_text(json.dumps(rows,indent=2));print('SOURCE_UNCHANGED',p.name,flush=True)
