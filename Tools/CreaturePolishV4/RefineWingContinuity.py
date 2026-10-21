"""Use original membrane UV color plus nearby ribs to close the remaining skin transition."""
import bpy,json,hashlib,numpy as np,math
from pathlib import Path
from mathutils.kdtree import KDTree
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Glurak';p=A/'Source/Glurak_PolishV4.blend';audit=json.loads((A/'PolishV4_Audit.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not __import__('subprocess').check_output(['git','ls-files','--',str(p.relative_to(R))],cwd=R).strip(),'Candidate is versioned: do not overwrite a released source';assert digest(p)==audit['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Glurak_Body'];rig=bpy.data.objects['Glurak_Rig'];s=bpy.context.scene;mat=body.data.materials[0];image=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].links[0].from_node.image;width,height=image.size;pixels=np.array(image.pixels[:]).reshape(height,width,4);uv=np.array([tuple(v.uv)for v in body.data.uv_layers.active.data]);indices=np.array([v.vertex_index for v in body.data.loops]);co=np.array([tuple(v.co)for v in body.data.vertices]);colors=pixels[(uv[:,1]%1*(height-1)).astype(int),(uv[:,0]%1*(width-1)).astype(int),:3];ratio=colors[:,1:].max(1)/(colors[:,0]+.002);valid=(ratio>1.1)&(np.abs(co[indices,0])>.22)&(co[indices,2]>.55)&(co[indices,1]<.55);seeds=np.unique(indices[valid]);assert len(seeds)>5000;kd=KDTree(len(seeds))
for i,index in enumerate(seeds):kd.insert(body.data.vertices[int(index)].co,i)
kd.balance();edges=np.array([e.vertices[:]for e in body.data.edges]);restlength=np.linalg.norm(co[edges[:,0]]-co[edges[:,1]],axis=1);region=(np.abs(co[:,0])>.3)&(co[:,2]>.55)&(co[:,1]<.55);selected=region[edges[:,0]]|region[edges[:,1]]
def stretch():
 rig.animation_data.action=bpy.data.actions['Glurak_Attack'];rows=[]
 for f in [7,13,19]:
  s.frame_set(f);ob=body.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ob.to_mesh();pts=np.array([tuple(v.co)for v in mesh.vertices]);growth=np.linalg.norm(pts[edges[:,0]]-pts[edges[:,1]],axis=1)-restlength;rank=np.flatnonzero(selected)[np.argmax(growth[selected])];rows.append(dict(frame=f,max_edge_growth_cm=float(growth[selected].max()*100),edges_over_3cm=int(sum(growth[selected]>.03)),max_edge_rest_m=float(restlength[rank]),max_edge_rest_vertices=co[edges[rank]].tolist()));ob.to_mesh_clear()
 return rows
before=stretch();changed=[]
def distance(p,n):
 b=rig.data.bones[n];a=b.head_local;v=b.tail_local-a;t=max(0,min(1,(p-a).dot(v)/v.length_squared));return(p-a-v*t).length
for v in body.data.vertices:
 x,y,z=v.co
 if abs(x)<.25 or z<.55 or y>.55:continue
 _,_,d=kd.find(v.co)
 if d>.14 and not(abs(x)>.5 and z>.75):continue
 side='L'if x>0 else'R';weights={n:1/max(.01,distance(v.co,n))**4 for n in ['wing_base_'+side,'wing_tip_'+side]};total=sum(weights.values());t=max(0,min(1,(abs(x)-.25)/.14));t=t*t*(3-2*t);prior={body.vertex_groups[g.group].name:g.weight for g in v.groups};new={n:w*(1-t)for n,w in prior.items()}
 for n,w in weights.items():new[n]=new.get(n,0)+t*w/total
 for g in body.vertex_groups:g.remove([v.index])
 for n,w in new.items():
  if w>1e-8:body.vertex_groups[n].add([v.index],w,'REPLACE')
 changed.append(v.index)
after=stretch();result=dict(before=before,after=after,changed_vertices=len(changed),membrane_seeds=len(seeds));(R/'Saved/CreaturePolishV4/WingContinuity.json').write_text(json.dumps(result,indent=2));print('WING_CONTINUITY',json.dumps(result),flush=True);assert max(x['max_edge_growth_cm']for x in after)<max(x['max_edge_growth_cm']for x in before)*.85
rig.animation_data.action=bpy.data.actions['Glurak_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;f=A/'Exports/PolishV4/Glurak_Idle.fbx';bpy.ops.export_scene.fbx(filepath=str(f),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO',colors_type='LINEAR');bpy.ops.wm.save_as_mainfile(filepath=str(p));audit['source_sha256']=digest(p);audit['exports'][0]['sha256']=digest(f);audit['changes']['wing_continuity']=result;(A/'PolishV4_Audit.json').write_text(json.dumps(audit,indent=2))
