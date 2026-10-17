"""Read-only V2 pose analysis in a separate background Blender process."""
import bpy, json, math
from pathlib import Path
from mathutils import Vector
R = Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster')
O = R/'Art/Characters/NPCs/Ranger/Review/AnimationV3/Data'
s = bpy.context.scene
r = s.objects['Ranger_Pilot_Rig']
assert bpy.app.background and Path(bpy.data.filepath).name == 'Ranger_NPC_AnimationQuality_V2.blend'
r.data.pose_position = 'POSE'
r.animation_data.action = bpy.data.actions['A_Ranger_Walk_AQV2']
def vec(v): return [round(float(x), 6) for x in v]
a = {'source': bpy.data.filepath, 'rig_world': [vec(v) for v in r.matrix_world], 'rest': {}, 'frames': []}
for n in ['pelvis','thigh_l','shin_l','foot_l','thigh_r','shin_r','foot_r']:
 b=r.data.bones[n]
 a['rest'][n]={'head':vec(b.head_local),'tail':vec(b.tail_local),'matrix':[vec(v) for v in b.matrix_local]}
for f in [1, 7.75, 14.5, 21.25, 28, 34.75, 41.5, 48.25, 55]:
 s.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update()
 row={'frame':f,'time':(f-1)/60,'bones':{}}
 for n in a['rest']:
  p=r.pose.bones[n];q=p.matrix.to_quaternion()
  row['bones'][n]={'head':vec(p.head),'tail':vec(p.tail),'basis_euler':vec(p.matrix_basis.to_euler()),'posed_rest_delta_euler':vec((q@r.data.bones[n].matrix_local.to_quaternion().inverted()).to_euler())}
 a['frames'].append(row)
(O/'V2_AxisDiagnosis.json').write_text(json.dumps(a,indent=2))
print(json.dumps(a['frames'][2],indent=2),flush=True)
