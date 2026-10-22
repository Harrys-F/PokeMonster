"""Export only V6 sources; never overwrite released exports. Mesh included only in Idle."""
import bpy,json,hashlib,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['Player','Glurak','Nebulak','Machomei','Myrapla']
if '--refine-unreleased'in sys.argv:names=[sys.argv[-1]];assert names[0]in ['Machomei','Glurak','Player']
for name in names:
 A=R/('Art/Characters/YoungTrainer'if name=='Player'else'Art/Characters/Creatures/'+name);ap=A/'AnimationCorrectionsV6_Audit.json';audit=json.loads(ap.read_text());source=R/audit['source'];assert sha(source)==audit['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(source));rig=bpy.data.objects['Player_Meshy_Rig'if name=='Player'else name+'_Rig'];body=bpy.data.objects['Player_Meshy_Body'if name=='Player'else name+'_Body'];s=bpy.context.scene;E=A/'Exports/AnimationV6';assert not E.exists()or('--refine-unreleased'in sys.argv and not subprocess.check_output(['git','ls-files','--',str(E.relative_to(R))],cwd=R).strip());E.mkdir(parents=True,exist_ok='--refine-unreleased'in sys.argv);exports=[]
 for role,action in audit['actions'].items():
  a=bpy.data.actions[action];rig.animation_data.action=a;s.frame_start=int(a.frame_range[0]);s.frame_end=int(a.frame_range[1]);s.frame_set(s.frame_start);bpy.ops.object.select_all(action='DESELECT');rig.hide_set(False);rig.select_set(True);body.hide_set(False);body.select_set(role=='Idle'and name!='Player');bpy.context.view_layer.objects.active=rig;p=E/(name+'_'+role+'.fbx');kw=dict(use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO',colors_type='LINEAR')
  if name=='Player':kw.update(use_armature_deform_only=True,apply_scale_options='FBX_SCALE_UNITS')
  bpy.ops.export_scene.fbx(filepath=str(p),**kw);exports.append(dict(role=role,path=str(p.relative_to(R)),sha256=sha(p),fps=s.render.fps,mesh=role=='Idle'and name!='Player',seconds=(s.frame_end-s.frame_start)/s.render.fps))
 audit['exports']=exports;ap.write_text(json.dumps(audit,indent=2));print('V6_EXPORTED',name,len(exports),flush=True)
