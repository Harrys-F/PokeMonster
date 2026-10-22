"""Candidate-only gait correction on the exact preserved player mesh/rest rig."""
import bpy,ast,math,json,hashlib,sys,subprocess
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/YoungTrainer';original=A/'Source/Player_Meshy_MotionQuality_V3.blend';dest=A/'Source/Player_Meshy_AnimationCorrections_V6.blend';assert not dest.exists()or('--refine-unreleased'in sys.argv and subprocess.run(['git','ls-files','--error-unmatch',str(dest.relative_to(R))],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(original);bpy.ops.wm.open_mainfile(filepath=str(original));bpy.context.preferences.filepaths.save_version=0;arm=bpy.data.objects['Player_Meshy_Rig'];obj=bpy.data.objects['Player_Meshy_Body'];pb=arm.pose.bones;scene=bpy.context.scene
geometry=[tuple(v.co)for v in obj.data.vertices];weights=[[(g.group,g.weight)for g in v.groups]for v in obj.data.vertices]
s=(R/'Tools/Blender/AnimateMeshyPlayerV2.py').read_text();tree=ast.parse(s)
for node in tree.body:
 if isinstance(node,ast.FunctionDef)and node.name in ['rot','solve']:exec(ast.get_source_segment(s,node))
# Reuse the V5 coherent IK function after its documented curve corrections; no old script execution.
s=(R/'Tools/MotionRefinementV5/BuildPlayerSource.py').read_text();prefix=s[s.index("s=(R/'Tools/Blender/"):s.index("exec(text);scene.render.fps")];exec(prefix)
text=text.replace("ankle=Vector((s*.16,-forward,.087+lift))","ankle=Vector((s*.12,-forward,.087+lift))")
text=text.replace("ankle=arm.data.bones['foot_'+side].head_local.copy();targets", "ankle=arm.data.bones['foot_'+side].head_local.copy();ankle.x=s*.12;targets")
text=text.replace("(-.045-.018*math.sin(2*phase-.5)) if walk else -.012", "(.085+.022*math.sin(2*phase-.5)+( .035 if running else 0)) if walk else .055")
text=text.replace("(-.035-k*math.sin(2*phase-offset)) if walk else -.008", "(.035+k*.65*math.sin(2*phase-offset)) if walk else .018")
text=text.replace("rot('lowerarm_'+side,(0,1,0),s*math.radians(7))", "rot('lowerarm_'+side,(1,0,0),-(.24+(.13 if running else .08)*math.sin(a-.45)) if walk else -.14)\n  rot('clavicle_'+side,(0,0,1),s*.015*math.sin(a-.25) if walk else 0.)")
text=text.replace("(.30 if running else .20)","(.39 if running else .25)")
exec(text)
rest_axis_rot=rot
def rot(n,axis,angle):
 if not n.startswith('lowerarm_'):return rest_axis_rot(n,axis,angle)
 # The upper arm is already lowered from the T rest pose. Convert through the ACTUAL
 # posed parent, not only the bone rest basis, or elbow flex becomes a forearm twist.
 bpy.context.view_layer.update();m=pb[n].matrix.copy();q=Quaternion(axis,angle)@m.to_quaternion();pb[n].matrix=Matrix.Translation(m.translation)@q.to_matrix().to_4x4()@Matrix.Diagonal((*m.to_scale(),1))
 bpy.context.view_layer.update()
scene.render.fps=60;created={};metrics={}
for role,count in [('Idle',181),('Walk',34),('Run',28)]:
 running=role=='Run';a=bpy.data.actions.new('A_Player_'+role+'_V6');a.use_fake_user=True;arm.animation_data.action=a;created[role]=a;duration=(count-1)/60
 for f in range(1,count+1):pose(f,(f-1)/(count-1),role!='Idle',duration)
 lows=[];gaps=[];width=[]
 for f in range(1,count+1):
  scene.frame_set(f);ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();lows.append(min(v.co.z for v in me.vertices));ev.to_mesh_clear();gaps.append(max((pb['shin_'+side].tail-pb['foot_'+side].head).length for side in ['l','r']));width.append(abs(pb['foot_l'].head.x-pb['foot_r'].head.x))
 assert min(lows)>-.001 and max(gaps)<.004,(role,min(lows),max(gaps));metrics[role]=dict(duration=duration,min_z_cm=min(lows)*100,max_chain_gap_cm=max(gaps)*100,foot_center_width_cm=sum(width)/len(width)*100)
assert geometry==[tuple(v.co)for v in obj.data.vertices]and weights==[[(g.group,g.weight)for g in v.groups]for v in obj.data.vertices]
arm.animation_data.action=created['Idle'];scene.frame_start=1;scene.frame_end=181;scene.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));assert sha(original)==before
(A/'AnimationCorrectionsV6_Audit.json').write_text(json.dumps(dict(source=str(dest.relative_to(R)),source_sha256=sha(dest),previous_sha256=before,geometry_weights_uv_rest_unchanged=True,metrics=metrics,actions={k:v.name for k,v in created.items()}),indent=2));print('V6_PLAYER_SOURCE_OK',metrics,flush=True)
