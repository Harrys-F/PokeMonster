"""Animation FBX contains bones/curves only; geometry is stored once in each mesh FBX."""
import bpy,json
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');rows=[]
for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
 id=a['id'];C=R/'Art/Characters/NPCs'/id if id!='HobbitBase' else R/'Art/Characters/NPCs/Westland/HobbitBase';bpy.ops.wm.open_mainfile(filepath=str(C/'Source'/(id+'_NPCLibrary.blend')),load_ui=False);s=bpy.context.scene;rig=next(o for o in s.objects if o.type=='ARMATURE')
 for o in s.objects:o.select_set(False)
 rig.select_set(True);bpy.context.view_layer.objects.active=rig;rig.data.pose_position='POSE';audit=json.loads((R/'Saved/ProjectRefinement/NPCExpansion/AnimationViews'/id/'Audit.json').read_text())
 for clip in audit['clips']:
  action=bpy.data.actions[clip['name']];rig.animation_data.action=action;s.frame_start=1;s.frame_end=clip['frames'];s.frame_set(1);dst=C/'Exports/Library'/(clip['name']+'.fbx');before=dst.stat().st_size;bpy.ops.export_scene.fbx(filepath=str(dst),use_selection=True,object_types={'ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,bake_anim=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO');rows.append({'id':id,'clip':clip['name'],'old_bytes':before,'new_bytes':dst.stat().st_size})
(R/'Saved/ProjectRefinement/NPCExpansion/AnimationOnlyExports.json').write_text(json.dumps(rows,indent=2))
