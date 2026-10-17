import bpy,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');C=R/'Art/Characters/NPCs/Ranger';I=R/'Art/Characters/NPCs/IntegrationV1';s=bpy.context.scene;mesh=s.objects['Ranger_Runtime_Pilot'];rig=s.objects['Ranger_Pilot_Rig']
# Back-carried sword must follow chest, not upper arm/head. Explicit Ranger-only ROI.
count=0
for v in mesh.data.vertices:
 x,y,z=v.co
 if x<-.17 and y>.10 and z>1.25:
  for g in mesh.vertex_groups:g.remove([v.index])
  mesh.vertex_groups['back_sword'].add([v.index],1,'REPLACE');count+=1
rig.animation_data.action=bpy.data.actions['A_Ranger_Idle_Pilot'];s.frame_start=1;s.frame_end=91;s.frame_set(1)
s['status']='Stationary Ranger V1; no Walk or finger animation approved';s['authored_npc_speed_cm_s']=0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
for o in s.objects:o.select_set(False)
rig.hide_set(False);mesh.hide_set(False);rig.select_set(True);mesh.select_set(True);bpy.context.view_layer.objects.active=rig
kw=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
rig.data.pose_position='REST';bpy.ops.export_scene.fbx(filepath=str(C/'Exports/SK_Ranger_NPC_V1.fbx'),bake_anim=False,**kw);rig.data.pose_position='POSE'
for name,end,out in [('A_Ranger_Idle_Pilot',91,'A_Ranger_Idle_V1'),('A_Ranger_Gesture_Pilot',61,'A_Ranger_Talk_V1')]:
 rig.animation_data.action=bpy.data.actions[name];s.frame_start=1;s.frame_end=end;s.frame_set(1);bpy.ops.export_scene.fbx(filepath=str(C/'Exports'/(out+'.fbx')),bake_anim=True,**kw)
rig.animation_data.action=bpy.data.actions['A_Ranger_Idle_Pilot'];s.frame_set(1);s.camera.location=(3,-5,2.1);s.camera.rotation_euler=(Vector((0,0,.9))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=2.1;s.render.filepath=str(C/'Previews/09_Idle_EquipmentFixed.png');bpy.ops.render.render(write_still=True)
# Exact same pose/light camera comparison of original vs reduced mesh before rig deformation.
rig.data.pose_position='REST';hp=next(o for o in s.objects if o.type=='MESH' and '_HP_' in o.name)
for name,show_hp in [('10_Reduction_A_HighPoly',True),('11_Reduction_B_Runtime',False)]:
 hp.hide_render=not show_hp;mesh.hide_render=show_hp;s.camera.location=(0,-5,.9);s.camera.rotation_euler=(Vector((0,0,.9))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=2.15;s.render.filepath=str(C/'Previews'/(name+'.png'));bpy.ops.render.render(write_still=True)
(I/'Ranger_Export.json').write_text(json.dumps({'back_equipment_vertices_corrected':count,'triangles':len(mesh.data.polygons),'bones':len(rig.data.bones),'exports':[str(x) for x in (C/'Exports').glob('*.fbx')],'walk':'not authored; no moving NPC in current map','status':'requires Unreal visual validation'},indent=2));print('RANGER_EXPORT_DONE',flush=True)
