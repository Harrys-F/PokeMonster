"""Read-only weight-solver diagnostics on temporary helper copies; never save a source."""
import bpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/CreatureExpansionV3/HeatProbe01';O.mkdir(exist_ok=False);rows=[]
for name in ['Pikachu','Myrapla','Enton']:
 bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures'/name/'Source'/(name+'_Meshy_V1.blend')));rig=bpy.data.objects[name+'_Rig'];rig.animation_data_clear();rig.data.pose_position='REST';body=bpy.data.objects[name+'_Body'];temp=body.copy();temp.data=body.data.copy();bpy.context.scene.collection.objects.link(temp);temp.parent=None;temp.matrix_world.identity();temp.vertex_groups.clear()
 for m in list(temp.modifiers):temp.modifiers.remove(m)
 for b in rig.data.bones:b.use_deform=b.name!='root'and not b.name.startswith(('tail_','ear_','leaf_','gas_','wing_'))
 bpy.ops.object.select_all(action='DESELECT');temp.select_set(True);bpy.context.view_layer.objects.active=temp;bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=.000001);bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.parent_set(type='ARMATURE_AUTO');sums=[sum(g.weight for g in v.groups)for v in temp.data.vertices];row=dict(species=name,vertices=len(sums),unweighted=sum(x<1e-6 for x in sums),groups={g.name:sum(any(x.group==g.index and x.weight>1e-6 for x in v.groups)for v in temp.data.vertices)for g in temp.vertex_groups});rows.append(row);print('HEAT_PROBE',row,flush=True)
(O/'Result.json').write_text(json.dumps(rows,indent=2))
