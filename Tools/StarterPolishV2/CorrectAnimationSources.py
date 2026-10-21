"""Narrow, versioned corrections; never overwrite imported originals or existing sources."""
import bpy,numpy as np,json,math,hashlib,sys
from pathlib import Path
from mathutils import Matrix,Quaternion,Vector
R=Path(__file__).resolve().parents[2];out=R/'Saved/StarterPolishV2/AnimationCorrections';out.mkdir(exist_ok='--revise-generated' in sys.argv);rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sample(body,rig,action):
 rig.animation_data.action=action;es=np.array([e.vertices[:]for e in body.data.edges]);p=np.array([tuple(v.co)for v in body.data.vertices]);base=np.linalg.norm(p[es[:,0]]-p[es[:,1]],axis=1);result=[]
 for f in np.linspace(*action.frame_range,33):
  bpy.context.scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([tuple(v.co)for v in m.vertices]);g=np.linalg.norm(p[es[:,0]]-p[es[:,1]],axis=1)-base;result.append({'frame':float(f),'max_edge_growth_m':float(g.max()),'edges_over_3cm':int(sum(g>.03)),'minimum_z_m':float(p[:,2].min())});ev.to_mesh_clear()
 return result
def render(body,rig,action,name,frame):
 s=bpy.context.scene;rig.animation_data.action=action;s.frame_set(int(frame),subframe=frame-int(frame));s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=s.render.resolution_y=900;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('DiagnosticOnly');s.world.color=(.18,.18,.18)
 lights=[]
 for loc,power in [((1,-2,3),200),((-2,-1,2),130),((1,2,2),200)]:
  bpy.ops.object.light_add(type='AREA',location=loc);a=bpy.context.object;a.data.energy=power;a.data.size=2;a.rotation_euler=(Vector((0,0,.25))-a.location).to_track_quat('-Z','Y').to_euler();lights.append(a)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.location=(1,-2,.75);cam.rotation_euler=(Vector((0,0,.25))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.35;s.camera=cam;s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 for a in lights+[cam]:bpy.data.objects.remove(a,do_unlink=True)
for species,file,bodyname,rigname,prefix in [('Zunderlauf','Glumanda_Meshy_V11.blend','Glumanda_Meshy','Glumanda_Meshy_Rig','Glumanda'),('Bisasam','Bisasam_Meshy_V1.blend','Bisasam_Body','Bisasam_Rig','Bisasam')]:
 A=R/'Art/Characters/Creatures'/species;source=A/'Source'/file;digest=sha(source);bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;body=bpy.data.objects[bodyname];rig=bpy.data.objects[rigname];changed=[]
 if species=='Zunderlauf':
  old=bpy.data.actions[prefix+'_Faint'];before=sample(body,rig,old);render(body,rig,old,species+'_Before',34)
  idle=bpy.data.actions[prefix+'_Idle'];rig.animation_data.action=idle;s.frame_set(1);bpy.context.view_layer.update();basis={p.name:p.matrix_basis.copy()for p in rig.pose.bones};action=bpy.data.actions.new('Glumanda_Faint_PolishV2');action.use_fake_user=True;rig.animation_data.action=action;s.render.fps=30
  for f in range(34):
   t=f/33;q=t*t*(3-2*t);s.frame_set(f+1)
   for p in rig.pose.bones:p.matrix_basis=basis[p.name]
   root=rig.pose.bones['root'];root.rotation_mode='QUATERNION';root.matrix=Quaternion((0,1,0),math.radians(78)*q).to_matrix().to_4x4()@root.bone.matrix_local;bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();low=min(v.co.z for v in m.vertices);ev.to_mesh_clear();grounded=root.matrix.copy();grounded.translation.z+=.001-low;root.matrix=grounded;bpy.context.view_layer.update()
   for p in rig.pose.bones:
    p.rotation_mode='QUATERNION'
    for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=f+1,group=p.name)
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      for key in curve.keyframe_points:key.interpolation='LINEAR'
  after=sample(body,rig,action);assert max(x['max_edge_growth_m']for x in after)<.015;render(body,rig,action,species+'_After',34)
  sourceout=A/'Source'/'Glumanda_Faint_PolishV2.blend';export=A/'Exports/PolishV2'/'Glumanda_Faint.fbx';s.frame_start=1;s.frame_end=34
 else:
  action=bpy.data.actions['Bisasam_Run'];before=sample(body,rig,action);render(body,rig,action,species+'_Before',1)
  # The V1 sole mask extended across the central belly. Actual feet are laterally outside this region.
  for v in body.data.vertices:
   x,y,z=v.co
   if abs(x)>=.13 or z>=.080 or y<=-.10 or y>=.10:continue
   if sum(g.weight for g in v.groups if body.vertex_groups[g.group].name.endswith('_foot'))<.15:continue
   t=max(0,min(1,(y+.10)/.20));weights={'chest':1-t,'pelvis':t};changed.append({'vertex':v.index,'rest':list(v.co),'before':[(body.vertex_groups[g.group].name,g.weight)for g in v.groups],'after':weights})
   for g in body.vertex_groups:g.remove([v.index])
   for n,w in weights.items():
    if w>1e-7:body.vertex_groups[n].add([v.index],w,'REPLACE')
  assert changed;after=sample(body,rig,action);assert max(x['max_edge_growth_m']for x in after)<max(x['max_edge_growth_m']for x in before)*.8;render(body,rig,action,species+'_After',1);sourceout=A/'Source'/'Bisasam_Meshy_PolishV2.blend';export=A/'Exports/PolishV2'/'Bisasam_Skin.fbx';rig.animation_data.action=bpy.data.actions['Bisasam_Idle'];s.frame_start=1;s.frame_end=61
 assert (not sourceout.exists()and not export.exists())or '--revise-generated' in sys.argv;export.parent.mkdir(exist_ok=True);s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
 bpy.ops.export_scene.fbx(filepath=str(export),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=species=='Zunderlauf',bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO')
 if species=='Zunderlauf':
  for obj in list(bpy.data.objects):
   if obj!=rig:bpy.data.objects.remove(obj,do_unlink=True)
  for other in list(bpy.data.actions):
   if other!=action:bpy.data.actions.remove(other)
  for block in [bpy.data.meshes,bpy.data.materials,bpy.data.images]:
   for item in list(block):block.remove(item)
  s['ReferenceModel']=str(source.relative_to(R));s['Purpose']='Corrected Faint action; append unchanged reference mesh for skin inspection'
 bpy.ops.wm.save_as_mainfile(filepath=str(sourceout));bpy.ops.wm.open_mainfile(filepath=str(sourceout));assert sha(source)==digest
 result={'species':species,'reference':str(source.relative_to(R)),'reference_sha256':digest,'source':str(sourceout.relative_to(R)),'export':str(export.relative_to(R)),'before':before,'after':after,'changed_vertices':changed,'reopened':True,'reference_unchanged':True};rows.append(result);(A/'PolishV2_AnimationAudit.json').write_text(json.dumps(result,indent=2))
(out/'Result.json').write_text(json.dumps(rows,indent=2));print('POLISH_CORRECTIONS_PASS',[(r['species'],len(r['changed_vertices']))for r in rows])
