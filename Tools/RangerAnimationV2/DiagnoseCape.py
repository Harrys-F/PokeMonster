import bpy
from pathlib import Path
from mathutils import Vector
s=bpy.context.scene;rig=s.objects['Ranger_Pilot_Rig'];run=s.objects['Ranger_V2_LOD0'];rig.data.pose_position='POSE';rig.animation_data.action=bpy.data.actions['A_Ranger_Idle_Pilot'];s.frame_set(1)
for o in s.objects:
 if o.type=='MESH':o.hide_render=o!=run
s.render.resolution_x=720;s.render.resolution_y=900;s.render.resolution_percentage=100;s.cycles.samples=4;s.camera.location=(3,5,1.9);s.camera.rotation_euler=(Vector((0,0,.9))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=2.1;s.render.filepath=str(Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Blender/V1_Cape_Back.png'));bpy.ops.render.render(write_still=True)
