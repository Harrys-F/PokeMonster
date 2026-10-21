"""Read-only samples of all 21 real source clips; retain worst poses as Blender diagnostics."""
import bpy,numpy as np,json,hashlib,math,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];O=R/'Saved/StarterPolishV2/AnimationBaseline';O.mkdir(exist_ok=False);rows=[]
for species,source,rig_name,body_name,prefix in [('Zunderlauf','Glumanda_Meshy_V11.blend','Glumanda_Meshy_Rig','Glumanda_Meshy','Glumanda'),('Schiggy','Schiggy_Meshy_V1.blend','Schiggy_Rig','Schiggy_Body','Schiggy'),('Bisasam','Bisasam_Meshy_V1.blend','Bisasam_Rig','Bisasam_Body','Bisasam')]:
 p=R/'Art/Characters/Creatures'/species/'Source'/source;digest=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p));body=bpy.data.objects[body_name];rig=bpy.data.objects[rig_name];s=bpy.context.scene;rest=np.zeros(len(body.data.vertices)*3,dtype=np.float32);body.data.vertices.foreach_get('co',rest);rest=rest.reshape(-1,3);edges=np.array([e.vertices[:]for e in body.data.edges]);restlen=np.linalg.norm(rest[edges[:,0]]-rest[edges[:,1]],axis=1);clips=[]
 for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
  action=bpy.data.actions[prefix+'_'+role];rig.animation_data.action=action;start,end=map(float,action.frame_range);samples=[]
  for f in np.linspace(start,end,17):
   s.frame_set(int(f),subframe=float(f-int(f)));bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();points=np.zeros(len(m.vertices)*3,dtype=np.float32);m.vertices.foreach_get('co',points);points=points.reshape(-1,3);newlen=np.linalg.norm(points[edges[:,0]]-points[edges[:,1]],axis=1);growth=newlen-restlen;i=int(np.argmax(growth));samples.append({'frame':float(f),'min_z_m':float(points[:,2].min()),'max_edge_growth_m':float(growth[i]),'edges_growing_over_3cm':int(np.sum(growth>.03)),'worst_edge_vertices':[int(x)for x in edges[i]],'posed_edge_length_m':float(newlen[i]),'rest_edge_length_m':float(restlen[i])});ev.to_mesh_clear()
  clips.append({'role':role,'samples':samples,'worst':max(samples,key=lambda x:x['max_edge_growth_m'])})
 row={'species':species,'source':str(p.relative_to(R)),'source_sha256':digest,'clips':clips};rows.append(row);assert hashlib.sha256(p.read_bytes()).hexdigest()==digest;print('POLISH_ANIMATION_SAMPLES',species,json.dumps({c['role']:c['worst']['max_edge_growth_m']for c in clips}),flush=True)
 # Diagnostic render, not a substitute for actual Unreal acceptance.
 s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=s.render.resolution_y=800;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('PolishAuditWorld');s.world.color=(.18,.18,.18)
 for loc,power in [((1,-2,3),200),((-2,-1,2),130),((1,2,2),200)]:
  bpy.ops.object.light_add(type='AREA',location=loc);a=bpy.context.object;a.data.energy=power;a.data.size=2;a.rotation_euler=(Vector((0,0,.3))-a.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.1
 for clip in clips:
  if clip['role'] not in ['Walk','Run','Attack','Faint','Happy']:continue
  rig.animation_data.action=bpy.data.actions[prefix+'_'+clip['role']];f=clip['worst']['frame'];s.frame_set(int(f),subframe=f-int(f));cam.location=(1,-2,.85);cam.rotation_euler=(Vector((0,0,.30))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(species+'_'+clip['role']+'.png'));bpy.ops.render.render(write_still=True)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
(O/'Result.json').write_text(json.dumps({'sources_unchanged':True,'rows':rows},indent=2))
