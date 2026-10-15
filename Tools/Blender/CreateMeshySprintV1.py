"""Author one new in-place run on the unchanged Meshy V2 rig; no mesh/weight edits."""
import bpy, math, json, ast
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');scene=bpy.context.scene
assert scene.name=='Meshy_Sprint_Work_V1'
arm=scene.objects['Player_Meshy_Rig'];obj=scene.objects['Player_Meshy_Body'];pb=arm.pose.bones
assert len(arm.data.bones)==25
# Reuse the reviewed V2 analytic leg solver; never rerun its weighting/rig construction.
s=(R/'Tools/Blender/AnimateMeshyPlayerV2.py').read_text();tree=ast.parse(s)
for n in tree.body:
 if isinstance(n,ast.FunctionDef) and n.name in ['rot','solve']:exec(ast.get_source_segment(s,n))
pose=next(ast.get_source_segment(s,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='pose')
pose=pose.replace('-.092+.006*math.cos(2*phase)','-.095+.012*math.cos(2*phase)')
pose=pose.replace('.045*math.sin(phase)','.060*math.sin(phase)').replace('.018+.012*math.sin(2*phase)','.060+.012*math.sin(2*phase)')
pose=pose.replace('.22*math.cos(a)','.34*math.cos(a)').replace('math.radians(7)','math.radians(18)')
start=pose.index('   u=(t+');end=pose.index('   solve(side,ankle,pitch)',start)
pose=pose[:start]+'''   u=(t+(0 if s==1 else .5))%1;stance=.42;span=3.15*duration*stance
   if u<stance:
    v=u/stance;forward=span*(.5-v);lift=0.;pitch=.03*math.sin(math.pi*v)
   else:
    v=(u-stance)/(1-stance);forward=-span*.5+span*(v*v*(3-2*v))
    lift=.105*math.sin(math.pi*v)**2;pitch=-.20*math.sin(math.pi*v)
   ankle=Vector((s*.16,-forward,.087+lift))
'''+pose[end:]
exec(pose)
scene.render.fps=60;count=28;duration=(count-1)/60
name='A_Player_Meshy_Run_V1';assert name not in bpy.data.actions
act=bpy.data.actions.new(name);act.use_fake_user=True
arm.animation_data_create();arm.animation_data.action=act;arm.data.pose_position='POSE'
for p in pb:p.rotation_mode='QUATERNION'
for f in range(1,count+1):pose(f,(f-1)/(count-1),True,duration)
for layer in act.layers:
 for strip in layer.strips:
  for cb in strip.channelbags:
   for curve in cb.fcurves:
    for key in curve.keyframe_points:key.interpolation='LINEAR'
scene.frame_start=1;scene.frame_end=count;scene.frame_set(1);bpy.context.view_layer.update()
# Validate real skin soles across a complete cycle, not only bone markers.
ids={s:[v.index for v in obj.data.vertices if v.co.z<.085 and ((v.co.x>0)==(s=='l'))] for s in ['l','r']}
audit=[]
for f in range(1,count+1):
 scene.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();e=obj.evaluated_get(dg);m=e.to_mesh()
 low={s:min(m.vertices[i].co.z for i in indices) for s,indices in ids.items()}
 audit.append({'frame':f,'sole_min_m':low,'root':list(pb['root'].matrix.translation)});e.to_mesh_clear()
assert min(v for row in audit for v in row['sole_min_m'].values())>=-.00001
assert all(Vector(row['root']).length<1e-6 for row in audit)
scene.frame_set(1);bpy.ops.file.pack_all()
P=R/'Art/Characters/YoungTrainer/Source/Player_Meshy_Sprint_V1.blend';assert not P.exists()
bpy.data.libraries.write(str(P),{scene},fake_user=True)
E=R/'Art/Characters/YoungTrainer/Exports/SprintV1';E.mkdir(parents=True,exist_ok=True)
for o in bpy.context.selected_objects:o.select_set(False)
arm.hide_set(False);obj.hide_set(False);arm.select_set(True);obj.select_set(True);bpy.context.view_layer.objects.active=arm
bpy.ops.export_scene.fbx(filepath=str(E/(name+'.fbx')),use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
O=R/'Saved/Sprint_20261014';(O/'BlenderRunAudit.json').write_text(json.dumps({'source':str(P),'duration_s':duration,'authored_speed_cm_s':315,'stride_m':3.15*duration,'stance_fraction':.42,'bones':25,'frames':audit,'reference_body_height_m':max(v.co.z for v in obj.data.vertices)-min(v.co.z for v in obj.data.vertices),'textures_packed':all(i.packed_file for i in bpy.data.images if i.source=='FILE' and i.users>0)},indent=2))
print('New run authored and exported; old source, skin and weights unchanged')
