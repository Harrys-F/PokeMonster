"""Keep the existing ground-length armored cloak hem separate from foot weights."""
import bpy,json,numpy as np
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');C=R/'Art/Characters/NPCs/DarkArmored';P=C/'Source/DarkArmored_NPCLibrary.blend';assert P.exists();bpy.ops.wm.open_mainfile(filepath=str(P),load_ui=False);bpy.context.preferences.filepaths.save_version=0;obj=bpy.data.objects['DarkArmored_LibraryMesh'];rig=bpy.data.objects['DarkArmored_LibraryRig'];ids=[]
for v in obj.data.vertices:
 if (v.co.z<.18 and (v.co.y>.03 or abs(v.co.x)>.24)) or (abs(v.co.x)<.145 and v.co.y<-.20 and v.co.z<1.05):
  ids.append(v.index)
  for g in obj.vertex_groups:g.remove([v.index])

  t=max(0,min(1,(v.co.z-.12)/.80));t=t*t*(3-2*t)
  obj.vertex_groups['root'].add([v.index],1-t,'REPLACE')
  if t>0:obj.vertex_groups['pelvis'].add([v.index],t,'REPLACE')
assert ids
O=R/'Saved/ProjectRefinement/NPCExpansion/AnimationViews/DarkArmored/Audit.json';audit=json.loads(O.read_text());s=bpy.context.scene
for row in audit['clips']:
 rig.animation_data.action=bpy.data.actions[row['name']];minimum=100
 for frame in np.linspace(1,row['frames'],17):
  s.frame_set(int(frame),subframe=float(frame%1));ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();minimum=min(minimum,min(v.co.z for v in me.vertices));ev.to_mesh_clear()
 row['minimum_surface_z_m']=minimum

 assert minimum>-.003,(row['role'],minimum)
audit['armor_hem_rooted_vertices']=len(ids);audit['limits']='Ground-length cloak rim remains rooted; walking only, no run. Rigid armor retains conservative joint motion.';O.write_text(json.dumps(audit,indent=2));rig.animation_data.action=bpy.data.actions['A_DarkArmored_Idle_Library'];s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(P),compress=True)
for o in s.objects:o.select_set(False)
obj.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;rig.data.pose_position='REST';bpy.ops.export_scene.fbx(filepath=str(C/'Exports/Library/SK_DarkArmored_Library.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim=False,path_mode='AUTO');print('ARMOR_HEM_FIXED',len(ids),flush=True)
