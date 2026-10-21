"""No source changes: classify Enton minimum vertices and wing/gas surfaces."""
import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/CreaturePolishV4';rows={}
for name in ['Enton','Nebulak','Glurak']:
 p=R/'Art/Characters/Creatures'/name/'Source'/(name+'_Meshy_V1.blend');bpy.ops.wm.open_mainfile(filepath=str(p));body=bpy.data.objects[name+'_Body'];rig=bpy.data.objects[name+'_Rig'];body.data.calc_loop_triangles();s=bpy.context.scene;row={'bones':[(b.name,list(b.head_local),list(b.tail_local))for b in rig.data.bones],'materials':[m.name for m in body.data.materials],'actions':[(a.name,list(a.frame_range))for a in bpy.data.actions],'minimum':[]}
 if name=='Enton':
  rig.animation_data.action=bpy.data.actions['Enton_Run']
  for f in range(1,14):
   s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();ob=body.evaluated_get(dg);mesh=ob.to_mesh();v=min(mesh.vertices,key=lambda v:v.co.z);orig=body.data.vertices[v.index];row['minimum'].append(dict(frame=f,index=v.index,z=v.co.z,rest=list(orig.co),weights=[(body.vertex_groups[g.group].name,g.weight)for g in orig.groups]));ob.to_mesh_clear()
 rows[name]=row
(O/'BlenderInventory.json').write_text(json.dumps(rows,indent=2));print('INSPECTION_DONE',flush=True)
