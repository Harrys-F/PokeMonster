"""Reopen, inspect packed sources, and actually reimport every FBX without saving reference changes."""
import bpy,json,math,hashlib,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];label=sys.argv[sys.argv.index('--')+1]if '--'in sys.argv else'BlenderValidation';assert label.isalnum();O=R/'Saved/StarterExpansionV1'/label;O.mkdir(exist_ok=False);rows=[]
for name in ['Schiggy','Bisasam']:
 A=R/'Art/Characters/Creatures'/name;source=A/'Source'/(name+'_Meshy_V1.blend');digest=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));body=bpy.data.objects[name+'_Body'];rig=bpy.data.objects[name+'_Rig'];ref=bpy.data.objects[name+'_UNMODIFIED_GLB'];audit=json.loads((A/'MeshyV1_ModelAudit.json').read_text());assert len(bpy.data.actions)==7;assert all(i.packed_file for i in bpy.data.images if i.type=='IMAGE');assert len(body.data.polygons)==audit['triangles'];assert len(ref.data.polygons)==audit['triangles'];assert len(body.data.uv_layers.active.data)==len(ref.data.uv_layers.active.data);assert all((a.uv-b.uv).length<1e-8 for a,b in zip(body.data.uv_layers.active.data,ref.data.uv_layers.active.data));assert all(abs(sum(g.weight for g in v.groups)-1)<.0001 for v in body.data.vertices)
 row={'species':name,'source_sha256':digest,'packed_images':len([i for i in bpy.data.images if i.type=='IMAGE']),'bones':len(rig.data.bones),'triangles':audit['triangles'],'uv_identical':True,'normalized_weights':True,'fbx':[]}
 s=bpy.context.scene;s.world=bpy.data.worlds.new('ValidationWorld');s.world.color=(.18,.18,.18);s.render.engine='CYCLES';s.cycles.samples=16;s.render.resolution_x=850;s.render.resolution_y=850;s.render.resolution_percentage=100;h=audit['height_m']
 for loc,power,size in [((1,-2,3),220,3),((-2,-1,2),140,2),((1,2,2),220,2)]:
  bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,h/2))-l.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=h*1.7;cam.location=(1,-2,h*1.15);cam.rotation_euler=(Vector((0,0,h/2))-cam.location).to_track_quat('-Z','Y').to_euler()
 for clip,frame in [('Idle',1),('Walk',5),('Walk',12),('Run',4),('Attack',13),('Faint',37)]:
  rig.animation_data.action=bpy.data.actions[name+'_'+clip];s.frame_set(frame);s.render.filepath=str(O/(name+'_'+clip+'_'+str(frame)+'.png'));bpy.ops.render.render(write_still=True)
 assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
 for clip in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(A/'Exports/MeshyV1'/(name+'_'+clip+'.fbx')));meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];arms=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'];assert len(meshes)==len(arms)==1;mesh=meshes[0].data;mesh.calc_loop_triangles();assert len(mesh.loop_triangles)==audit['triangles'];assert len(arms[0].data.bones)==row['bones'];assert len(bpy.data.actions)==1;row['fbx'].append({'clip':clip,'triangles':len(mesh.loop_triangles),'bones':len(arms[0].data.bones),'actions':len(bpy.data.actions)})
 rows.append(row);print('STARTER_BLENDER_VALIDATED',name,flush=True)
(O/'Result.json').write_text(json.dumps({'passed':True,'models':rows},indent=2))
