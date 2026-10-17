import bpy,numpy as np,json
from pathlib import Path
s=bpy.context.scene;src=s.objects['Ranger_Runtime_Pilot'];rig=s.objects['Ranger_Pilot_Rig'];rig.data.pose_position='REST';out=[]
for inv in [False,True]:
 o=src.copy();o.data=src.data.copy();s.collection.objects.link(o);o.hide_set(False);g=o.vertex_groups.new(name='LOD_DetailProtect')
 ids=[v.index for v in o.data.vertices if v.co.z>1.47 or abs(v.co.x)>.73];g.add(ids,1.,'REPLACE');d=o.modifiers.new('BiasProbe','DECIMATE');d.ratio=55000/len(o.data.polygons);d.vertex_group=g.name;d.vertex_group_factor=1000;d.invert_vertex_group=inv;d.use_collapse_triangulate=True
 while list(o.modifiers).index(d)>0:bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_move_up(modifier=d.name)
 bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=d.name);out.append({'invert':inv,'protected_source_vertices':len(ids),'head_vertices':sum(v.co.z>1.47 for v in o.data.vertices),'hand_vertices':sum(abs(v.co.x)>.73 for v in o.data.vertices),'total':len(o.data.vertices)});bpy.data.objects.remove(o,do_unlink=True)
print('BIAS_RESULT',json.dumps(out));Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/V2/BiasProbe.json').write_text(json.dumps(out,indent=2))
