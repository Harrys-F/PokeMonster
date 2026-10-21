"""New player clips on the exact existing mesh/weights/rest rig; C1 recovery and coherent IK clearance."""
import bpy,ast,math,json,hashlib
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/YoungTrainer';P=A/'Source/Player_Meshy_MotionQuality_V3.blend';assert not P.exists();original=A/'Source/Player_Meshy_AnimationQuality_V2.blend';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(original);bpy.ops.wm.open_mainfile(filepath=str(original));bpy.context.preferences.filepaths.save_version=0;arm=bpy.data.objects['Player_Meshy_Rig'];obj=bpy.data.objects['Player_Meshy_Body'];pb=arm.pose.bones;scene=bpy.context.scene;original_vertices=[tuple(v.co)for v in obj.data.vertices];original_weights=[[(g.group,g.weight)for g in v.groups]for v in obj.data.vertices];original_uvs=[tuple(v.uv)for v in obj.data.uv_layers.active.data]
s=(R/'Tools/Blender/AnimateMeshyPlayerV2.py').read_text();tree=ast.parse(s)
for node in tree.body:
 if isinstance(node,ast.FunctionDef)and node.name in ['rot','solve']:exec(ast.get_source_segment(s,node))
text=next(ast.get_source_segment(s,node)for node in tree.body if isinstance(node,ast.FunctionDef)and node.name=='pose');text=text.replace('phase=2*math.pi*t','phase=2*math.pi*t;targets={}')
text=text.replace('-.092+.006*math.cos(2*phase)','(-.134 if running else -.108)+(.010 if running else .006)*math.cos(2*phase)')
text=text.replace('(.22*math.cos(a) if walk else .004*math.sin(a))','((.30 if running else .20)*math.cos(a) if walk else .006*math.sin(a))');text=text.replace("rot('chest',(1,0,0),.018+.012*math.sin(2*phase))","rot('chest',(1,0,0),(.05 if running else .018)+.012*math.sin(2*phase))")
text=text.replace(" else:\n  rot('chest'", " else:\n  pb['pelvis'].location=(.003*math.sin(phase),-.008+.001*math.cos(phase),0)\n  rot('chest'",1)
a=text.index('   u=(t+');b=text.index('   solve(side,ankle,pitch)',a)
text=text[:a]+'''   u=(t+(0 if s==1 else .5))%1;stance=.42 if running else .5;speed=3.15 if running else 2.1;span=speed*duration*stance
   if u<stance:
    v=u/stance;forward=span*(.5-v);lift=0.;pitch=-.06*(1-min(1,v/.18))+.11*max(0,(v-.8)/.2)
   else:
    v=(u-stance)/(1-stance);m=-speed*duration*(1-stance)/span
    h=(-2*v**3+3*v**2)+m*((v**3-2*v*v+v)+(v**3-v*v))
    forward=-span*.5+span*h;lift=(.105 if running else .066)*math.sin(math.pi*v)**2;pitch=-.12*math.sin(math.pi*v)
   ankle=Vector((s*.16,-forward,.087+lift));targets[side]=(ankle,pitch)
'''+text[b:]
text=text.replace(' # Enforce foot sole clearance',"  else:\n   ankle=arm.data.bones['foot_'+side].head_local.copy();targets[side]=(ankle,0.);solve(side,ankle,0.)\n # Enforce foot sole clearance")
text=text.replace("   m=pb['foot_'+side].matrix.copy();m.translation.z+=.0005-low;pb['foot_'+side].matrix=m", "   ankle,pitch=targets[side];ankle=ankle+Vector((0,0,.0005-low));solve(side,ankle,pitch)")
a=text.index(' # Enforce foot sole clearance');b=text.index(' for p in pb:',a)
text=text[:a]+''' # Evaluate soles before updating the dependency graph again.
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=obj.evaluated_get(dg);em=ev.to_mesh()
 lows={side:min(em.vertices[v.index].co.z for v in obj.data.vertices if v.co.z<.085 and ((v.co.x>0)==(side=='l')))for side in ['l','r']};ev.to_mesh_clear()
 for side in ['l','r']:
  if lows[side]<.0005:
   ankle,pitch=targets[side];solve(side,ankle+Vector((0,0,.0005-lows[side])),pitch)
'''+text[b:]
exec(text);scene.render.fps=60;metrics={};created={}
for role,count in [('Idle',181),('Walk',34),('Run',28)]:
 running=role=='Run';a=bpy.data.actions.new('A_Player_Meshy_'+role+'_V3');a.use_fake_user=True;arm.animation_data.action=a;created[role]=a;duration=(count-1)/60
 for f in range(1,count+1):pose(f,(f-1)/(count-1),role!='Idle',duration)
 for layer in a.layers:
  for strip in layer.strips:
   for cb in strip.channelbags:
    for curve in cb.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
 lows=[];gaps=[]
 for f in range(1,count+1):
  scene.frame_set(f);e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();lows.append(min(v.co.z for v in m.vertices));e.to_mesh_clear();gaps.append(max((pb['shin_'+side].tail-pb['foot_'+side].head).length for side in ['l','r']))
 metrics[role]=dict(duration=duration,minimum_z_cm=min(lows)*100,max_knee_ankle_join_gap_cm=max(gaps)*100);print(role,metrics[role],flush=True)
 assert min(lows)>-.0001 and max(gaps)<.004,(role,min(lows),max(gaps))
assert original_vertices==[tuple(v.co)for v in obj.data.vertices];assert original_weights==[[(g.group,g.weight)for g in v.groups]for v in obj.data.vertices];assert original_uvs==[tuple(v.uv)for v in obj.data.uv_layers.active.data]
arm.animation_data.action=created['Idle'];scene.frame_start=1;scene.frame_end=181;scene.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P));assert sha(original)==before;(A/'MotionQualityV3_Audit.json').write_text(json.dumps(dict(source=str(P.relative_to(R)),source_sha256=sha(P),original_sha256=before,mesh_weights_uvs_and_rest_skeleton_unchanged=True,metrics=metrics,recovery_curve='Cubic Hermite matches stance velocity at both endpoints',authored_speeds_cm_s=dict(Walk=210,Run=315)),indent=2));print('PLAYER_MOTION_SOURCE_SAVED',flush=True)
