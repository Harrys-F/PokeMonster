"""Reopen source and every exported FBX; check actual deform weights, scale and role closure."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Raichu';D=R/'Saved/ProjectRefinement/ModelsV4';bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Raichu_V4.blend'));rig=bpy.data.objects['Raichu_Rig'];body=bpy.data.objects['Raichu'];valid=set(rig.data.bones.keys());unweighted=[];sums=[]
for v in body.data.vertices:
 total=sum(g.weight for g in v.groups if body.vertex_groups[g.group].name in valid);sums.append(total)
 if total<.999:unweighted.append(v.index)
assert not unweighted and max(abs(v-1)for v in sums)<.0001
roles={};srcbones=len(rig.data.bones)
for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
 action=bpy.data.actions['Raichu_'+role];rig.animation_data.action=action;lo,hi=action.frame_range;poses=[]
 for frame in [lo,hi]:
  bpy.context.scene.frame_set(int(frame));bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();poses.append([v.co.copy()for v in m.vertices]);ev.to_mesh_clear()
 gap=max((a-b).length for a,b in zip(*poses));roles[role]={'loop_surface_gap_m':gap}
 if role in ['Idle','Walk','Run']:assert gap<.0001,(role,gap)
fbx=[]
for p in sorted((A/'Exports/V4').glob('*.fbx')):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(p));meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];rigs=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'];assert len(meshes)==1 and len(rigs)==1 and bpy.data.actions
 m=meshes[0];points=[m.matrix_world@v.co for v in m.data.vertices];height=max(v.z for v in points)-min(v.z for v in points);assert .77<height<.84,(p.name,height);assert len(rigs[0].data.bones)>=srcbones;assert len(m.data.uv_layers)>0;fbx.append({'file':p.name,'height_m':height,'bones':len(rigs[0].data.bones),'actions':len(bpy.data.actions),'scale':list(m.scale)})
(D/'SourceValidation.json').write_text(json.dumps({'weighted_vertices':len(sums),'weight_max_error':max(abs(v-1)for v in sums),'source_bones':srcbones,'roles':roles,'fbx_reopened':fbx},indent=2));print('SOURCE_VALIDATION_PASS',len(fbx))
