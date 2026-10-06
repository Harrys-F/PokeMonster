"""Read two own checkpoints to compare the untouched original Blender scene.
Background use only; does not save either file.
"""
import bpy,json
from pathlib import Path
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
OUT=ROOT.parents[2]/'Saved/YoungTrainerV1'
def original():
 result={}
 for n in ['Cube','Camera','Light']:
  o=bpy.data.objects[n]
  result[n]={'type':o.type,'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale),'modifiers':[(m.name,m.type) for m in o.modifiers]}
  if o.type=='MESH':result[n]['mesh']={'vertices':[list(v.co) for v in o.data.vertices],'polygons':[list(p.vertices) for p in o.data.polygons]}
  elif o.type=='CAMERA':result[n]['camera']={'lens':o.data.lens,'sensor_width':o.data.sensor_width,'type':o.data.type}
  elif o.type=='LIGHT':result[n]['light']={'energy':o.data.energy,'color':list(o.data.color),'type':o.data.type}
 return result
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Source/Stages/01_Blockout.blend'));before=original()
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Source/YoungTrainer_Reference_V1.blend'));after=original()
assert before==after,'An original scene object changed.'
result={'original_scene_objects_unchanged':True,'compared_to':'Source/Stages/01_Blockout.blend','source_reopened':bpy.data.filepath,'objects':after}
(OUT/'Preservation.json').write_text(json.dumps(result,indent=2)+'\n')
print('ORIGINAL_SCENE_PRESERVED',list(after),'FINAL_SOURCE_REOPENED',flush=True)
