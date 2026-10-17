import bpy,json,math,numpy as np,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');C=R/'Art/Characters/NPCs/Ranger';O=C/'Review/V2';B=O/'BlenderProtected';B.mkdir(exist_ok=True);E=C/'Exports/V2_Protected';E.mkdir(exist_ok=True);target=C/'Source/Ranger_NPC_V2_Protected.blend';assert not target.exists()
s=bpy.context.scene;v1=s.objects['Ranger_Runtime_Pilot'];rig=s.objects['Ranger_Pilot_Rig'];assert len(rig.data.bones)==24;rig.data.pose_position='REST';s.frame_set(1)
reference_hash=hashlib.sha256(np.array([v.co[:] for v in v1.data.vertices],dtype=np.float32).tobytes()).hexdigest();bone_hash=hashlib.sha256(str([(b.name,b.parent.name if b.parent else None,[list(x) for x in b.matrix_local]) for b in rig.data.bones]).encode()).hexdigest()
coll=bpy.data.collections.new('RANGER_V2_LODS');s.collection.children.link(coll);objects=[];audits=[]
verts=[v.co.copy() for v in v1.data.vertices];faces=[tuple(p.vertices) for p in v1.data.polygons];bvh=BVHTree.FromPolygons(verts,faces,all_triangles=True)
for level,count in enumerate([55000,24000,10000]):
 obj=v1.copy();obj.data=v1.data.copy();obj.name='Ranger_V2_LOD'+str(level);coll.objects.link(obj);obj.hide_set(False);obj.hide_render=False
 for o in s.objects:o.select_set(False)
 obj.select_set(True);bpy.context.view_layer.objects.active=obj
 dec=obj.modifiers.new('V2_LOD_Reduction','DECIMATE');dec.ratio=count/len(obj.data.polygons);dec.use_collapse_triangulate=True
 protect=obj.vertex_groups.new(name='LOD_DetailProtect')
 protected=[v.index for v in obj.data.vertices if (v.co.z>1.47 if level<2 else v.co.z>1.47 and abs(v.co.x)<.18 and v.co.y<-.03) or abs(v.co.x)>.73]
 protect.add(protected,1.,'REPLACE');dec.vertex_group=protect.name;dec.vertex_group_factor=1000;dec.invert_vertex_group=True
 while list(obj.modifiers).index(dec)>0:bpy.ops.object.modifier_move_up(modifier=dec.name)
 bpy.ops.object.modifier_apply(modifier=dec.name);
 group=obj.vertex_groups.get('LOD_DetailProtect')
 if group:obj.vertex_groups.remove(group)
 m=obj.data;m.calc_loop_triangles();positions=[v.co.copy() for v in m.vertices];polys=[tuple(p.vertices) for p in m.polygons];target_bvh=BVHTree.FromPolygons(positions,polys,all_triangles=True);d=[target_bvh.find_nearest(v)[3] for v in verts];regions={}
 for name,test in [('head',lambda v:v.z>1.5 and abs(v.x)<.24),('hands',lambda v:abs(v.x)>.75),('cape',lambda v:v.y>.1 and v.z<1.4)]:
  a=[d[i]*1000 for i,v in enumerate(verts) if test(v)];regions[name]={'p95_mm':float(np.percentile(a,95)),'max_mm':max(a)} if a else {}
 weights=[sum(g.weight for g in v.groups) for v in m.vertices];assert min(weights)>.999 and max(weights)<1.001
 co=np.array([v.co[:] for v in m.vertices]);normals=np.array([n.vector[:] for n in m.corner_normals]);assert np.isfinite(co).all() and np.isfinite(normals).all()
 audit={'level':level,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'polygons':len(m.polygons),'material_slots':len(m.materials),'uv_layers':[u.name for u in m.uv_layers],'bounds_min_m':co.min(axis=0).tolist(),'bounds_max_m':co.max(axis=0).tolist(),'source_vertices_to_lod_surface_p95_mm':float(np.percentile(d,95)*1000),'source_vertices_to_lod_surface_max_mm':max(d)*1000,'regions':regions,'weights_sum':[min(weights),max(weights)],'protected_source_vertices':len(protected),'method':'Measured inverted vertex-group bias 1000 protects head/hands; LOD2 protects central face and hands. Simplification before Armature, protection group removed afterward. Original HP/V1/rig/actions unchanged.'};audits.append(audit);objects.append(obj)
 for o in s.objects:o.select_set(False)
 rig.hide_set(False);rig.select_set(True);obj.select_set(True);bpy.context.view_layer.objects.active=rig
 bpy.ops.export_scene.fbx(filepath=str(E/('SK_Ranger_NPC_V2_LOD'+str(level)+'.fbx')),use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim=False,path_mode='AUTO')
 obj.hide_render=True
# Preserve original rig/action names so Unreal can reuse the existing skeleton and animation clips.
rig.data.pose_position='POSE';rig.animation_data.action=bpy.data.actions['A_Ranger_Idle_Pilot'];s.frame_start=1;s.frame_end=91;s.frame_set(1);v1.hide_render=True
for a in bpy.data.actions:a.use_fake_user=True
for obj in objects:obj.hide_render=obj!=objects[0];obj.hide_set(obj!=objects[0])
for im in bpy.data.images:
 if im.source=='FILE' and im.users and not im.packed_file:im.pack()
s['version']='Ranger Quality V2 LOD candidates, not automatically released';s['bone_rest_hash']=bone_hash;s['V1_runtime_geometry_hash']=reference_hash
bpy.ops.wm.save_as_mainfile(filepath=str(target))
# Visual comparisons: identical neutral studio lighting, original UV/material, exact same rig pose.
s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=800;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
all_models=[v1]+objects
for view,loc,aim,scale in [('Front',(0,-5,.9),(0,0,.9),2.12),('ThreeQuarter',(3,-5,2.1),(0,0,.9),2.15),('Face',(0,-3,1.64),(0,0,1.64),.43)]:
 s.camera.data.type='ORTHO';s.camera.data.ortho_scale=scale;s.camera.location=loc;s.camera.rotation_euler=(Vector(aim)-s.camera.location).to_track_quat('-Z','Y').to_euler()
 for j,obj in enumerate(all_models):
  for x in all_models:x.hide_render=x!=obj;x.hide_set(False)
  s.frame_set(1);s.render.filepath=str(B/(('V1' if j==0 else 'V2_LOD'+str(j-1))+'_'+view+'.png'));bpy.ops.render.render(write_still=True)
# Full clip geometry checks, preserve the rig and animation channels unchanged.
clipchecks=[]
for action,end in [('A_Ranger_Idle_Pilot',91),('A_Ranger_Gesture_Pilot',61)]:
 rig.animation_data.action=bpy.data.actions[action];floors=[100.]*3
 for frame in range(1,end+1):
  s.frame_set(frame);dg=bpy.context.evaluated_depsgraph_get()
  for j,obj in enumerate(objects):
   obj.hide_set(False);ev=obj.evaluated_get(dg);m=ev.to_mesh();coords=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',coords);floors[j]=min(floors[j],float(coords.reshape(-1,3)[:,2].min()));ev.to_mesh_clear()
 clipchecks.append({'action':action,'frames':end,'minimum_surface_z_m_per_lod':floors})
(O/'BlenderProtectedLOD_Audit.json').write_text(json.dumps({'source':str(C/'Source/Ranger_NPC_V1.blend'),'file':str(target),'bones':len(rig.data.bones),'bone_rest_hash':bone_hash,'v1_geometry_hash':reference_hash,'lods':audits,'clips':clipchecks,'render_folder':str(B),'skeleton_animation_change':'None; reused existing 24-bone rig and both V1 actions'},indent=2));print('RANGER_V2_CREATED',flush=True)
