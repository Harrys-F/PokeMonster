import bpy,json,math
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V1'];bpy.context.window.scene=s;cam=s.camera;rig=s.objects['HNM1_Rig'];P=B/'Review/MeshyBaseV1/Previews'
rig.data.pose_position=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='REST');s.frame_set(1)
views=[('01_Front',(0,-4,.7),(0,0,.7),1.78),('02_Back',(0,4,.7),(0,0,.7),1.78),('03_Left',(-4,0,.7),(0,0,.7),1.60),('04_Right',(4,0,.7),(0,0,.7),1.60),('05_ThreeQuarter',(2.6,-4,1.65),(0,0,.7),1.90),('06_Camera25D',(2.6,-2.6,3.9),(0,0,.7),1.88)]
paths=[]
for name,loc,target,size in views:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=next(i.identifier for i in bpy.types.Camera.bl_rna.properties['type'].enum_items if i.identifier=='ORTHO');cam.data.ortho_scale=size
 s.render.filepath=str(P/('Hobbit_MeshyBase_V1_'+name+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath);print('RENDER_DONE',name,flush=True)
# Additional real rendered pose checks; no edits to action curves or weights.
rig.data.pose_position=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='POSE')
for label,aname,frame in [('Idle','HNM1_Idle_V2',1),('Walk_Left','HNM1_Walk_V2',8),('Walk_Right','HNM1_Walk_V2',25),('Run','HNM1_Run_V1',8)]:
 act=bpy.data.actions[aname];rig.animation_data.action=act
 if len(act.slots):rig.animation_data.action_slot=act.slots[0]
 s.frame_set(frame);bpy.context.view_layer.update();cam.location=(2.1,-4,1.4);cam.rotation_euler=(Vector((0,0,.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.7
 s.render.filepath=str(P/('Hobbit_MeshyBase_V1_Pose_'+label+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath);print('POSE_DONE',label,flush=True)
(B/'Review/MeshyBaseV1/PreviewPaths.json').write_text(json.dumps({'source':bpy.data.filepath,'images':paths,'source_saved_by_renderer':False,'studio_only_not_unreal':True},indent=2))
