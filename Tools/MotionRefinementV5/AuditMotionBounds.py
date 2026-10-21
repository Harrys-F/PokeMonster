"""Read-only deformed bounds over every Glurak frame; protects hover clearance/culling."""
import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures/Glurak/Source/Glurak_MotionV5.blend'));rig=bpy.data.objects['Glurak_Rig'];body=bpy.data.objects['Glurak_Body'];rows=[];lo=Vector((1e9,1e9,1e9));hi=-lo
for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy','Takeoff','Hover','Land']:
 a=bpy.data.actions['Glurak_'+role+'_MotionV5'];rig.animation_data.action=a;l=Vector((1e9,1e9,1e9));h=-l
 for f in range(int(a.frame_range[0]),int(a.frame_range[1])+1):
  bpy.context.scene.frame_set(f);ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh()
  co=np.empty((len(m.vertices),3),dtype=np.float32);m.vertices.foreach_get('co',co.ravel());q=co[:,[1,0,2]]*np.array([-100,100,100]);minimum=q.min(axis=0);maximum=q.max(axis=0)
  for k in range(3):l[k]=min(l[k],float(minimum[k]));h[k]=max(h[k],float(maximum[k]))
  ev.to_mesh_clear()
 for k in range(3):lo[k]=min(lo[k],l[k]);hi[k]=max(hi[k],h[k])
 rows.append(dict(role=role,minimum=list(l),maximum=list(h)))
(R/'Saved/MotionRefinementV5/GlurakMotionBounds.json').write_text(json.dumps(dict(frames='Every authored frame, original unchanged body topology',unreal_minimum=list(lo),unreal_maximum=list(hi),clips=rows),indent=2));print('MOTION_BOUNDS',list(lo),list(hi),flush=True)
