"""Bone heat on an ephemeral welded helper; only normalized skin weights are transferred."""
import bpy,json
from pathlib import Path
from mathutils.kdtree import KDTree

def assign_heat(body,rig):
 rig.data.pose_position='REST';rig.data.bones['root'].use_deform=False
 temp=body.copy();temp.data=body.data.copy();bpy.context.scene.collection.objects.link(temp);temp.name='WEIGHT_SOLVER_ONLY';temp.parent=None;temp.matrix_world.identity();temp.vertex_groups.clear()
 for mod in list(temp.modifiers):temp.modifiers.remove(mod)
 bpy.ops.object.select_all(action='DESELECT');temp.select_set(True);bpy.context.view_layer.objects.active=temp;bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=.000001);bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.parent_set(type='ARMATURE_AUTO')
 sums=[sum(g.weight for g in v.groups)for v in temp.data.vertices]
 assert all(x>1e-6 for x in sums),'Bone heat incomplete; do not transfer'
 for v,total in zip(temp.data.vertices,sums):
  for g in v.groups:temp.vertex_groups[g.group].add([v.index],g.weight/total,'REPLACE')
 kd=KDTree(len(temp.data.vertices))
 for v in temp.data.vertices:kd.insert(v.co,v.index)
 kd.balance();body.vertex_groups.clear()
 for g in temp.vertex_groups:body.vertex_groups.new(name=g.name)
 error=0.
 for v in body.data.vertices:
  pos,index,d=kd.find(v.co);assert d<.000002;error=max(error,d)
  for g in temp.data.vertices[index].groups:body.vertex_groups[g.group].add([v.index],g.weight,'REPLACE')
 result={'method':'Blender bone heat on temporary 1-micrometre welded helper; normalized weights only','helper_vertices':len(temp.data.vertices),'unweighted_vertices':0,'maximum_transfer_distance_m':error,'original_geometry_unchanged':True}
 bpy.data.objects.remove(temp,do_unlink=True);rig.data.pose_position='POSE';return result

if __name__=='__main__':
 R=Path(__file__).resolve().parents[2]
 for name in ['Schiggy','Bisasam']:
  A=R/'Art/Characters/Creatures'/name;source=A/'Source'/(name+'_Meshy_V1.blend');bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0;rig=bpy.data.objects[name+'_Rig'];rig.animation_data_clear();audit=json.loads((A/'MeshyV1_ModelAudit.json').read_text());audit['weights']=assign_heat(bpy.data.objects[name+'_Body'],rig);(A/'MeshyV1_ModelAudit.json').write_text(json.dumps(audit,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(source))
