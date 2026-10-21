"""Audit and repair only peripheral wing vertices missed by the old height envelope."""
import bpy,json,hashlib,math,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Glurak';p=A/'Source/Glurak_PolishV4.blend';audit=json.loads((A/'PolishV4_Audit.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not __import__('subprocess').check_output(['git','ls-files','--',str(p.relative_to(R))],cwd=R).strip(),'Candidate is versioned: do not overwrite a released source';assert digest(p)==audit['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Glurak_Body'];rig=bpy.data.objects['Glurak_Rig'];s=bpy.context.scene;edges=np.array([e.vertices[:]for e in body.data.edges]);rest=np.array([tuple(v.co)for v in body.data.vertices]);lengths=np.linalg.norm(rest[edges[:,0]]-rest[edges[:,1]],axis=1);wing=(np.abs(rest[:,0])>.5)&(rest[:,2]>.76)&(rest[:,1]>-.23);selected=wing[edges[:,0]]&wing[edges[:,1]]
def stretch():
 rig.animation_data.action=bpy.data.actions['Glurak_Attack'];rows=[]
 for f in [7,13,19]:
  s.frame_set(f);ob=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh();co=np.array([tuple(v.co)for v in m.vertices]);growth=np.linalg.norm(co[edges[:,0]]-co[edges[:,1]],axis=1)-lengths;rows.append(dict(frame=f,max_edge_growth_cm=float(growth[selected].max()*100),edges_over_3cm=int(sum(growth[selected]>.03))));ob.to_mesh_clear()
 return rows
before=stretch();changed=[]
def dist(p,bone):
 b=rig.data.bones[bone];a=b.head_local;delta=b.tail_local-a;u=max(0,min(1,(p-a).dot(delta)/delta.length_squared));return (p-a-u*delta).length
for v in body.data.vertices:
 if not wing[v.index]:continue
 prior={body.vertex_groups[g.group].name:g.weight for g in v.groups}
 if sum(w for n,w in prior.items()if n.startswith('wing_'))>.995:continue
 side='L'if v.co.x>0 else'R';weights={n:1/max(.01,dist(v.co,n))**4 for n in ['wing_base_'+side,'wing_tip_'+side]};total=sum(weights.values());t=max(0,min(1,(abs(v.co.x)-.5)/.16));t=t*t*(3-2*t);new={n:w*(1-t)for n,w in prior.items()}
 for n,w in weights.items():new[n]=new.get(n,0)+t*w/total
 for g in body.vertex_groups:g.remove([v.index])
 for n,w in new.items():
  if w>1e-8:body.vertex_groups[n].add([v.index],w,'REPLACE')
 changed.append(v.index)
after=stretch();result=dict(before=before,after=after,changed_vertices=len(changed));(R/'Saved/CreaturePolishV4/WingSkinAudit.json').write_text(json.dumps(result,indent=2));print('WING_SKIN_AUDIT',json.dumps(result),flush=True)
assert changed and max(x['max_edge_growth_cm']for x in after)<max(x['max_edge_growth_cm']for x in before)*.8,'No demonstrated improvement: do not save'
rig.animation_data.action=bpy.data.actions['Glurak_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;f=A/'Exports/PolishV4/Glurak_Idle.fbx';bpy.ops.export_scene.fbx(filepath=str(f),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO',colors_type='LINEAR');bpy.ops.wm.save_as_mainfile(filepath=str(p));audit['source_sha256']=digest(p);audit['exports'][0]['sha256']=digest(f);audit['changes']['peripheral_wing_skin']=result;(A/'PolishV4_Audit.json').write_text(json.dumps(audit,indent=2))
