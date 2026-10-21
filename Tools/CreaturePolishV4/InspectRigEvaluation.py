import bpy,json,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[2];rows=[]
for file in ['Glurak_Meshy_V1.blend','Glurak_PolishV4.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures/Glurak/Source'/file));b=bpy.data.objects['Glurak_Body'];r=bpy.data.objects['Glurak_Rig'];s=bpy.context.scene;r.animation_data.action=bpy.data.actions['Glurak_Idle'];s.frame_set(1);row=dict(file=file,mods=[dict(name=m.name,type=m.type,object=m.object.name if m.type=='ARMATURE'else None)for m in b.modifiers],vertices=len(b.data.vertices),object_matrix=[list(x)for x in b.matrix_world],rig_matrix=[list(x)for x in r.matrix_world],slot=str(r.animation_data.action_slot),bones={n:dict(mode=r.pose.bones[n].rotation_mode,quat=list(r.pose.bones[n].rotation_quaternion),matrix=[list(x)for x in r.pose.bones[n].matrix])for n in ['wing_base_L','wing_tip_L','root']})
 r.data.pose_position='REST';bpy.context.view_layer.update();ob=b.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh();row['evaluated_vertices']=len(m.vertices);row['rest_max_coordinate_delta']=max((a.co-c.co).length for a,c in zip(b.data.vertices,m.vertices));ob.to_mesh_clear();rows.append(row)
(R/'Saved/CreaturePolishV4/RigEvaluation.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows),flush=True)
