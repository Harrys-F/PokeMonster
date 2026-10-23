import bpy,numpy as np,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/AnimationCorrectionsV61'
bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationCorrections_V6.blend'));b=bpy.data.objects['Player_Meshy_Body'];a=bpy.data.objects['Player_Meshy_Rig'];s=bpy.context.scene
co=np.array([tuple(v.co)for v in b.data.vertices]);tri=np.array([tuple(p.vertices)for p in b.data.polygons]);assert tri.shape[1]==3
uv=np.array([tuple(d.uv)for d in b.data.uv_layers.active.data]);uvv=np.zeros((len(co),2))
for l in b.data.loops:uvv[l.vertex_index]=uv[l.index]
im=next(n for n in b.data.materials[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].links[0].from_node.image;pix=np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4);rgb=pix[(uvv[:,1]*(im.size[1]-1)).astype(int),(uvv[:,0]*(im.size[0]-1)).astype(int),:3];names=[g.name for g in b.vertex_groups];weights=np.zeros((len(co),len(names)))
for v in b.data.vertices:
 for g in v.groups:weights[v.index,g.group]=g.weight
outs={};posed={}
for role,frame in [('Idle',1),('Walk',9),('Run',8)]:
 a.animation_data.action=bpy.data.actions['A_Player_'+role+'_V6'];s.frame_set(frame);ev=b.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();deformed=np.array([tuple(v.co)for v in me.vertices]);ev.to_mesh_clear();posed[role]=deformed
 edge=np.stack([tri[:,0],tri[:,1]],axis=1);edges=np.vstack([edge,tri[:,[1,2]],tri[:,[2,0]]]);stretch=np.linalg.norm(deformed[edges[:,0]]-deformed[edges[:,1]],axis=1)/np.maximum(np.linalg.norm(co[edges[:,0]]-co[edges[:,1]],axis=1),1e-6);bad=np.where((stretch>3)&(co[edges].mean(1)[:,2]<.65))[0];bad=bad[np.argsort(-stretch[bad])];outs[role]=[dict(stretch=float(stretch[i]),vertices=[dict(index=int(j),rest=co[j].tolist(),posed=deformed[j].tolist(),rgb=rgb[j].tolist(),weights={n:float(w)for n,w in zip(names,weights[j])if w>.001})for j in edges[i]])for i in bad[:50]]
np.savez_compressed(O/'PlayerGeometryDiagnosis.npz',co=co,tri=tri,weights=weights,names=names,rgb=rgb,**posed);(O/'PlayerStretchedEdges.json').write_text(json.dumps(outs,indent=2));print(json.dumps({k:len(v)for k,v in outs.items()}))
