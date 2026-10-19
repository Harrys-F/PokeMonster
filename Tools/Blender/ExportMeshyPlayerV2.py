"""Export reviewed Animation Quality V2 only; V1 exports and sources are preserved."""
import bpy
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');E=R/'Art/Characters/YoungTrainer/Exports/MeshyV2';E.mkdir(exist_ok=True,parents=True)
assert Path(bpy.data.filepath).name=='Player_Meshy_AnimationQuality_V2.blend'
a=bpy.data.objects['Player_Meshy_Rig'];m=bpy.data.objects['Player_Meshy_Body']
for o in bpy.context.selected_objects:o.select_set(False)
a.select_set(True);m.select_set(True);bpy.context.view_layer.objects.active=a
kw=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
a.data.pose_position='REST';bpy.ops.export_scene.fbx(filepath=str(E/'SK_Player_Meshy_V2.fbx'),bake_anim=False,**kw);a.data.pose_position='POSE'
for n,end in [('A_Player_Meshy_Idle_V2',181),('A_Player_Meshy_Walk_V2',34)]:
 a.animation_data.action=bpy.data.actions[n];bpy.context.scene.frame_start=1;bpy.context.scene.frame_end=end;bpy.context.scene.frame_set(1)
 bpy.ops.export_scene.fbx(filepath=str(E/(n+'.fbx')),bake_anim=True,**kw)
a.animation_data.action=bpy.data.actions['A_Player_Meshy_Idle_V2'];bpy.context.scene.frame_end=181;bpy.context.scene.frame_set(1)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('V2 exports complete; 25 bones, 3 s idle, 0.55 s stride')
