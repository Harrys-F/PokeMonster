"""Reject unreliable broad skin experiments. Preserve original skin and keep only bounded wing motion.
The V4 belly/foot IK correction, masks, source geometry, UVs and all other channels remain.
"""
import bpy,json,hashlib,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Glurak';p=A/'Source/Glurak_PolishV4.blend';audit=json.loads((A/'PolishV4_Audit.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not __import__('subprocess').check_output(['git','ls-files','--',str(p.relative_to(R))],cwd=R).strip(),'Candidate is versioned: do not overwrite a released source';assert digest(p)==audit['source_sha256'];original=A/'Source/Glurak_Meshy_V1.blend';oldsha=digest(original);bpy.ops.wm.open_mainfile(filepath=str(original));b=bpy.data.objects['Glurak_Body'];rig=bpy.data.objects['Glurak_Rig'];groups=[g.name for g in b.vertex_groups];weights=[[(g.group,g.weight)for g in v.groups]for v in b.data.vertices];wing_names=[n for n in rig.pose.bones.keys()if n.startswith('wing_')];original_pose={}
for a in bpy.data.actions:
 rig.animation_data.action=a;frames={}
 for f in range(int(a.frame_range[0]),int(a.frame_range[1])+1):
  bpy.context.scene.frame_set(f);frames[f]={n:rig.pose.bones[n].rotation_quaternion.copy()for n in wing_names}
 original_pose[a.name]=frames
bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Glurak_Body'];rig=bpy.data.objects['Glurak_Rig'];s=bpy.context.scene;assert groups==[g.name for g in body.vertex_groups];candidate={}
for a in bpy.data.actions:
 rig.animation_data.action=a;frames={}
 for f in original_pose[a.name]:
  s.frame_set(f);frames[f]={n:rig.pose.bones[n].rotation_quaternion.copy()for n in wing_names}
 candidate[a.name]=frames
for g in body.vertex_groups:g.remove(list(range(len(body.data.vertices))))
for v in body.data.vertices:
 for group,weight in weights[v.index]:body.vertex_groups[group].add([v.index],weight,'REPLACE')
co=np.array([tuple(v.co)for v in body.data.vertices]);edges=np.array([e.vertices[:]for e in body.data.edges]);length=np.linalg.norm(co[edges[:,0]]-co[edges[:,1]],axis=1);region=(np.abs(co[:,0])>.25)&(co[:,2]>.55)&(co[:,1]<.7);selected=region[edges[:,0]]|region[edges[:,1]];report={}
def pose(action,factor):
 rig.animation_data.action=action
 for f in original_pose[action.name]:
  s.frame_set(f)
  for n in wing_names:
   bone=rig.pose.bones[n];bone.rotation_quaternion=original_pose[action.name][f][n].slerp(candidate[action.name][f][n],factor);bone.keyframe_insert(data_path='rotation_quaternion',frame=f)
def measure(action):
 rig.animation_data.action=action;maximum=0.;minimum=1e9
 for f in original_pose[action.name]:
  s.frame_set(f);o=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=o.to_mesh();pts=np.array([tuple(v.co)for v in m.vertices]);growth=np.linalg.norm(pts[edges[:,0]]-pts[edges[:,1]],axis=1)-length;maximum=max(maximum,float(growth[selected].max()));minimum=min(minimum,float(pts[:,2].min()));o.to_mesh_clear()
 return maximum,minimum
for action in bpy.data.actions:
 pose(action,0);baseline,_=measure(action);limit=max(baseline+.01,baseline*1.15);chosen=0;maximum=baseline;low=0
 for factor in [.15,.10,.05,0]:
  pose(action,factor);maximum,low=measure(action)
  if maximum<=limit:chosen=factor;break
 assert maximum<=limit+1e-6;role=action.name.split('_')[-1];report[role]=dict(accepted_extra_motion_fraction=chosen,original_skin_max_edge_growth_cm=baseline*100,accepted_max_edge_growth_cm=maximum*100,min_z_cm=low*100)
for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
 action=bpy.data.actions['Glurak_'+role];rig.animation_data.action=action;s.frame_start=int(action.frame_range[0]);s.frame_end=int(action.frame_range[1]);s.frame_set(s.frame_start);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(role=='Idle');bpy.context.view_layer.objects.active=rig;f=A/'Exports/PolishV4'/('Glurak_'+role+'.fbx');bpy.ops.export_scene.fbx(filepath=str(f),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO',colors_type='LINEAR')
 for e in audit['exports']:
  if e['role']==role:e['sha256']=digest(f)
 audit['minima'][role]['min_z_cm']=report[role]['min_z_cm']
rig.animation_data.action=bpy.data.actions['Glurak_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p));assert digest(original)==oldsha;audit['source_sha256']=digest(p)
for k in ['peripheral_wing_skin','wing_continuity','final_wing_skin']:audit['changes'].pop(k,None)
audit['changes']['final_wing_policy']='Original weights preserved; large-flap skin experiments rejected. Only bounded small secondary movement accepted; larger opening/attack flap remains open.';audit['changes']['wing_motion_limits']=report;(A/'PolishV4_Audit.json').write_text(json.dumps(audit,indent=2));(R/'Saved/CreaturePolishV4/FinalWingLimits.json').write_text(json.dumps(report,indent=2));print('BOUNDED_WING_SOURCE',json.dumps(report),flush=True)
