"""Read-only Blender audit; no source save or automatic topology repairs."""
import bpy,json,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/AnimationCorrectionsV6';rows={}
sources={'Player':'Art/Characters/YoungTrainer/Source/Player_Meshy_MotionQuality_V3.blend','Glurak':'Art/Characters/Creatures/Glurak/Source/Glurak_MotionV5.blend','Nebulak':'Art/Characters/Creatures/Nebulak/Source/Nebulak_MotionV5.blend','Machomei':'Art/Characters/Creatures/Machomei/Source/Machomei_Meshy_V1.blend','Myrapla':'Art/Characters/Creatures/Myrapla/Source/Myrapla_Meshy_V1.blend'}
for key,path in sources.items():
 bpy.ops.wm.open_mainfile(filepath=str(R/path));rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');body=next(o for o in bpy.context.scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==rig for m in o.modifiers));co=np.array([tuple(v.co)for v in body.data.vertices]);row=dict(path=path,rig=rig.name,body=body.name,vertices=len(co),triangles=sum(len(p.vertices)-2 for p in body.data.polygons),bbox=[co.min(0).tolist(),co.max(0).tolist()],bones=[dict(name=b.name,head=list(b.head_local),tail=list(b.tail_local),axes=[list(x)for x in b.matrix_local])for b in rig.data.bones],materials=[m.name if m else None for m in body.data.materials],attributes=[a.name for a in body.data.color_attributes],actions=[dict(name=a.name,frames=list(a.frame_range))for a in bpy.data.actions]);groups={g.index:g.name for g in body.vertex_groups}
 row['weights']={}
 for n in groups.values():
  ids=[v.index for v in body.data.vertices if any(groups[g.group]==n and g.weight>.15 for g in v.groups)]
  if ids:row['weights'][n]=dict(count=len(ids),bbox=[co[ids].min(0).tolist(),co[ids].max(0).tolist()])
 if key=='Player':
  ids=[v.index for v in body.data.vertices if .10<v.co.z<.6 and abs(v.co.x)<.19 and v.co.y<.075 and any(groups[g.group].startswith('cape')and g.weight>.1 for g in v.groups)];row['inner_leg_cape_weights']=dict(count=len(ids),examples=[dict(index=i,co=list(body.data.vertices[i].co),weights={groups[g.group]:g.weight for g in body.data.vertices[i].groups})for i in ids[:15]])
 # UV seams duplicate vertices: geometric edge-incidence audit after virtual welding, separately per material.
 _,inv=np.unique(np.rint(co/1e-5).astype(np.int64),axis=0,return_inverse=True)
 row['material_surfaces']=[]
 for mi in range(len(body.data.materials)):
  polys=[p for p in body.data.polygons if p.material_index==mi];ee=np.array([(inv[a],inv[b])for p in polys for a,b in zip(p.vertices,list(p.vertices[1:])+[p.vertices[0]])]);ee=np.sort(ee,axis=1);ends,counts=np.unique(ee,axis=0,return_counts=True);row['material_surfaces'].append(dict(slot=mi,faces=len(polys),boundary_edges=int((counts==1).sum()),nonmanifold_edges=int((counts>2).sum()),bbox=[co[np.unique([v for p in polys for v in p.vertices])].min(0).tolist(),co[np.unique([v for p in polys for v in p.vertices])].max(0).tolist()]))
 rows[key]=row;print(key,row['vertices'],row['materials'],row['material_surfaces'],flush=True)
(O/'SourceInspection.json').write_text(json.dumps(rows,indent=2))
