"""Measure actual deformed edge stretch and weights; never alter a working source."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];rows={}
for name in ['Schiggy','Bisasam']:
 bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures'/name/'Source'/(name+'_Meshy_V1.blend')));rig=bpy.data.objects[name+'_Rig'];body=bpy.data.objects[name+'_Body'];rig.animation_data.action=bpy.data.actions[name+'_Walk'];bpy.context.scene.frame_set(5);bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();edges=[]
 for e in body.data.edges:
  a,b=e.vertices;old=(body.data.vertices[a].co-body.data.vertices[b].co).length;new=(m.vertices[a].co-m.vertices[b].co).length
  if new-old>.03:edges.append({'rest_length':old,'posed_length':new,'points':[{'rest':list(body.data.vertices[i].co),'posed':list(m.vertices[i].co),'weights':{body.vertex_groups[g.group].name:g.weight for g in body.data.vertices[i].groups}}for i in [a,b]]})
 rows[name]=sorted(edges,key=lambda x:x['posed_length']-x['rest_length'],reverse=True)[:12];ev.to_mesh_clear()
(R/'Saved/StarterExpansionV1/SkinDiagnosis.json').write_text(json.dumps(rows,indent=2))
