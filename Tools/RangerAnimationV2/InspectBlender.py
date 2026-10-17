import bpy,json,numpy as np
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data';s=bpy.context.scene;r=s.objects['Ranger_Pilot_Rig'];r.data.pose_position='REST';m=s.objects['Ranger_Runtime_Pilot'];co=np.array([v.co[:] for v in m.data.vertices]);a={'source':bpy.data.filepath,'objects':[],'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'head':b.head_local[:],'tail':b.tail_local[:]} for b in r.data.bones],'actions':[{'name':x.name,'range':x.frame_range[:]} for x in bpy.data.actions],'slices':{}}
for o in s.objects:
 if o.type=='MESH':a['objects'].append({'name':o.name,'verts':len(o.data.vertices),'polys':len(o.data.polygons),'modifiers':[(x.name,x.type) for x in o.modifiers]})
for z in [.1,.2,.35,.5,.7,.85,1,1.2,1.4]:
 sel=co[np.abs(co[:,2]-z)<.015];a['slices'][str(z)]={'x_range':sel[:,0].min().item() if len(sel) else None,'x_max':sel[:,0].max().item() if len(sel) else None,'y_quantiles':np.quantile(sel[:,1],[0,.1,.25,.5,.75,.9,1]).tolist() if len(sel) else []}
a['weights_by_bone']={g.name:sum(any(q.group==g.index and q.weight>.1 for q in v.groups) for v in m.data.vertices) for g in m.vertex_groups}
(O/'BlenderBefore.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2),flush=True)
