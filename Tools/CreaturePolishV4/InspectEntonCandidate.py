import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures/Enton/Source/Enton_PolishV4.blend'));rig=bpy.data.objects['Enton_Rig'];body=bpy.data.objects['Enton_Body'];rig.animation_data.action=bpy.data.actions['Enton_Run'];rows=[]
for f in range(1,14):
 bpy.context.scene.frame_set(f);ob=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh();v=min(m.vertices,key=lambda v:v.co.z);o=body.data.vertices[v.index];rows.append(dict(frame=f,index=v.index,z=v.co.z,rest=list(o.co),weights=[(body.vertex_groups[g.group].name,g.weight)for g in o.groups]));ob.to_mesh_clear()
(R/'Saved/CreaturePolishV4/EntonCandidateMinima.json').write_text(json.dumps(rows,indent=2));print(rows[3])
