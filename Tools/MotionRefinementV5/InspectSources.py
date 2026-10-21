"""Read-only rigs, weights and contact audit before motion work."""
import bpy,json,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/MotionRefinementV5';rows={}
for key,path in {'Glurak':'Art/Characters/Creatures/Glurak/Source/Glurak_PolishV4.blend','Nebulak':'Art/Characters/Creatures/Nebulak/Source/Nebulak_PolishV4.blend','Player':'Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend','Sprint':'Art/Characters/YoungTrainer/Source/Player_Meshy_Sprint_V1.blend'}.items():
 bpy.ops.wm.open_mainfile(filepath=str(R/path));rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE'and o.animation_data);body=next(o for o in bpy.context.scene.objects if o.type=='MESH'and any(m.type=='ARMATURE'and m.object==rig for m in o.modifiers));co=np.array([tuple(v.co)for v in body.data.vertices]);row=dict(path=path,rig=rig.name,body=body.name,vertices=len(co),bbox=[co.min(0).tolist(),co.max(0).tolist()],fps=bpy.context.scene.render.fps,bones=[dict(name=b.name,parent=b.parent.name if b.parent else None,head=list(b.head_local),tail=list(b.tail_local),axis_matrix=[list(v)for v in b.matrix_local])for b in rig.data.bones],actions=[dict(name=a.name,frames=list(a.frame_range))for a in bpy.data.actions]);rows[key]=row
 if key=='Glurak':
  groups={g.index:g.name for g in body.vertex_groups};row['wing_weights']={}
  for name in groups.values():
   if not name.startswith('wing_'):continue
   ids=[v.index for v in body.data.vertices if any(groups[g.group]==name and g.weight>.01 for g in v.groups)];row['wing_weights'][name]=dict(count=len(ids),bbox=[co[ids].min(0).tolist(),co[ids].max(0).tolist()])
  edges=np.array([e.vertices[:]for e in body.data.edges]);rest=np.linalg.norm(co[edges[:,0]]-co[edges[:,1]],axis=1);rig.animation_data.action=bpy.data.actions['Glurak_Attack'];bpy.context.scene.frame_set(13);e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();posed=np.array([tuple(v.co)for v in m.vertices]);growth=np.linalg.norm(posed[edges[:,0]]-posed[edges[:,1]],axis=1)-rest;ix=np.argsort(growth)[-12:];row['original_attack_edge_growth']=[dict(cm=float(growth[i]*100),vertices=[dict(index=int(j),rest=co[j].tolist(),weights={groups[g.group]:g.weight for g in body.data.vertices[j].groups})for j in edges[i]])for i in ix];e.to_mesh_clear()
 print(key,row['vertices'],[(b['name'],[round(x,3)for x in b['head']],[round(x,3)for x in b['tail']])for b in row['bones']],flush=True)
(O/'SourceInspection.json').write_text(json.dumps(rows,indent=2))
