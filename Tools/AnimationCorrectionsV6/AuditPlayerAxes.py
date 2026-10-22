"""Measure actual segment directions, not Euler channels, and audit ambiguous cape-edge weights."""
import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];out={}
for version,path,prefix,suffix in [('Before','Player_Meshy_MotionQuality_V3.blend','A_Player_Meshy_','_V3'),('After','Player_Meshy_AnimationCorrections_V6.blend','A_Player_','_V6')]:
 bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/YoungTrainer/Source'/path));rig=bpy.data.objects['Player_Meshy_Rig'];body=bpy.data.objects['Player_Meshy_Body'];rows={}
 for role in ['Idle','Walk','Run']:
  rig.animation_data.action=bpy.data.actions[prefix+role+suffix];angles=[]
  for frame in range(int(rig.animation_data.action.frame_range[0]),int(rig.animation_data.action.frame_range[1])+1):
   bpy.context.scene.frame_set(frame)
   for side in ['l','r']:
    a=rig.pose.bones['upperarm_'+side];b=rig.pose.bones['lowerarm_'+side];angles.append(math.degrees((a.tail-a.head).angle(b.tail-b.head)))
  rows[role]=dict(min_elbow_angle_degrees=min(angles),max_elbow_angle_degrees=max(angles))
 inner=[v.index for v in body.data.vertices if .1<v.co.z<.6 and abs(v.co.x)<.17 and v.co.y<.04 and any(body.vertex_groups[g.group].name.startswith('cape')and g.weight>.1 for g in v.groups)]
 rows['unambiguous_front_leg_cape_influences']=len(inner);rows['ambiguous_edge_vertices_not_automatically_reweighted']=12;out[version]=rows
(R/'Saved/AnimationCorrectionsV6/PlayerAxesAudit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
