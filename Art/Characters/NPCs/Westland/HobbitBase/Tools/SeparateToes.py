"""Local separation of the five toe tips; all edits belong to the new body."""
import bpy,bmesh,json
from pathlib import Path
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_Base_V1'];bpy.context.window.scene=s;body=bpy.data.objects['HNB_Body'];c=next(c for c in s.collection.children if c.name=='MODEL_WORK');k=json.loads((BASE/'Review/Calibration.json').read_text())['calibration_factor']
def active(o):
 for q in s.objects:q.select_set(False)
 o.select_set(True);bpy.context.view_layer.objects.active=o
for sign in [1,-1]:
 for i,x in enumerate([.079,.1045,.1285,.1505]):
  bpy.ops.mesh.primitive_cube_add(size=1,location=(sign*x*k,-.218*k,.044*k));o=bpy.context.object;o.name='HNB_Work_ToeGap_'+str(sign)+'_'+str(i)
  for col in list(o.users_collection):col.objects.unlink(o)
  c.objects.link(o);o.scale=(.004*k,.094*k,.12*k);active(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  b=o.modifiers.new('RoundedToeGap','BEVEL');b.width=.0015*k;b.segments=3;bpy.ops.object.modifier_apply(modifier=b.name)
  active(body);m=body.modifiers.new('SeparateToeTips','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=o;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(o,do_unlink=True)
active(body);m=body.modifiers.new('SoftenToeGrooves','BEVEL');m.width=.0006;m.segments=2;m.limit_method='ANGLE';m.angle_limit=.7;bpy.ops.object.modifier_apply(modifier=m.name)
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,0),plane_no=(1,0,0),clear_inner=True);bm.to_mesh(body.data);bm.free();m=body.modifiers.new('ExactBodySymmetry','MIRROR');m.use_mirror_merge=True;m.merge_threshold=.00001;bpy.ops.object.modifier_apply(modifier=m.name)
for p in body.data.polygons:p.use_smooth=True
bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V1.blend'),{s});print('Eight local rounded toe grooves; exactly mirrored body retained.')
