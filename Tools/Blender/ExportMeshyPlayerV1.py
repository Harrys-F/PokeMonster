"""Export only the reviewed game-ready copy; never save the Meshy original."""
import bpy,json,math
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');E=R/'Art/Characters/YoungTrainer/Exports/MeshyV1'
assert Path(bpy.data.filepath).name=='Player_Meshy_GameReady_V1.blend'
arm=bpy.data.objects['Player_Meshy_Rig'];mesh=bpy.data.objects['Player_Meshy_Body']
for o in bpy.context.selected_objects:o.select_set(False)
arm.select_set(True);mesh.select_set(True);bpy.context.view_layer.objects.active=arm
settings=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
# Bind pose is T-pose; clips hold relaxed arms. No geometry deformation baked twice.
arm.data.pose_position='REST'
bpy.ops.export_scene.fbx(filepath=str(E/'SK_Player_Meshy.fbx'),bake_anim=False,**settings)
arm.data.pose_position='POSE'
for name,end in [('A_Player_Meshy_Idle',61),('A_Player_Meshy_Walk',31)]:
 arm.animation_data.action=bpy.data.actions[name];bpy.context.scene.frame_start=1;bpy.context.scene.frame_end=end;bpy.context.scene.frame_set(1)
 bpy.ops.export_scene.fbx(filepath=str(E/(name+'.fbx')),bake_anim=True,**settings)
arm.animation_data.action=bpy.data.actions['A_Player_Meshy_Idle'];bpy.context.scene.frame_end=61;bpy.context.scene.frame_set(1)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('Exported skeletal mesh plus Idle (2 s) and Walk (1 s), in-place, 23 bones.')
