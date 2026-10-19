import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster');C=R/'Art/Characters/NPCs/ElvenArcher';s=bpy.context.scene;obj=s.objects['ElvenArcher_Runtime'];rig=s.objects['ElvenArcher_Rig'];count=0
for v in obj.data.vertices:
 x,y,z=v.co
 # Only the rear head/upper-gear band, above sleeve bulk, in the source's local coordinates.
 if y>.07 and abs(x)<.44 and z>1.545:
  for g in obj.vertex_groups:g.remove([v.index])
  obj.vertex_groups['back_sword'].add([v.index],1,'REPLACE');count+=1
rig.animation_data.action=bpy.data.actions['A_ElvenArcher_Idle_V1'];s.frame_start=1;s.frame_end=91;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
for o in s.objects:o.select_set(False)
obj.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
kw=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
rig.data.pose_position='REST';bpy.ops.export_scene.fbx(filepath=str(C/'Exports/SK_ElvenArcher_NPC_V1.fbx'),bake_anim=False,**kw);rig.data.pose_position='POSE'
for n,end in [('A_ElvenArcher_Idle_V1',91),('A_ElvenArcher_Talk_V1',61)]:
 rig.animation_data.action=bpy.data.actions[n];s.frame_start=1;s.frame_end=end;s.frame_set(1);bpy.ops.export_scene.fbx(filepath=str(C/'Exports'/(n+'.fbx')),bake_anim=True,**kw)
rig.animation_data.action=bpy.data.actions['A_ElvenArcher_Idle_V1'];s.frame_set(1);s.camera.location=(3,-5,2.2);s.camera.rotation_euler=(Vector((0,0,.98))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=2.45;s.render.filepath=str(C/'Previews/07_GearCorrected.png');bpy.ops.render.render(write_still=True)
(R/'Art/Characters/NPCs/IntegrationV1/ArcherGearCorrection.json').write_text(json.dumps({'vertices':count,'limitation':'Rear long hair within gear band remains mostly chest-driven; no full hair retargeting approved','render':s.render.filepath},indent=2))
