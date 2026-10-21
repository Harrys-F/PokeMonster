"""Only the verified own V4 candidate: prevent low central belly following opposite legs."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Enton';p=A/'Source/Enton_PolishV4.blend';a=json.loads((A/'PolishV4_Audit.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not __import__('subprocess').check_output(['git','ls-files','--',str(p.relative_to(R))],cwd=R).strip(),'Candidate is versioned: do not overwrite a released source';assert digest(p)==a['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Enton_Body'];rig=bpy.data.objects['Enton_Rig'];count=0
for v in body.data.vertices:
 x,y,z=v.co
 if abs(x)>=.115 or y<-.04 or y>.16 or z>=.22 or z<=.045:continue
 t=max(0.,min(1.,(.115-abs(x))/.045))*max(0.,min(1.,(.22-z)/.05));t=t*t*(3-2*t)
 if t<1e-6:continue
 weights={body.vertex_groups[g.group].name:g.weight*(1-t)for g in v.groups};weights['pelvis']=weights.get('pelvis',0)+t
 for g in body.vertex_groups:g.remove([v.index])
 for n,w in weights.items():
  if w>1e-8:body.vertex_groups[n].add([v.index],w,'REPLACE')
 count+=1
s=bpy.context.scene
for role in a['minima']:
 rig.animation_data.action=bpy.data.actions['Enton_'+role];lo,hi=map(int,rig.animation_data.action.frame_range);zs=[]
 for f in range(lo,hi+1):
  s.frame_set(f);ob=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh();zs.append(min(v.co.z for v in m.vertices));ob.to_mesh_clear()
 a['minima'][role]={'min_z_cm':min(zs)*100,'max_min_z_cm':max(zs)*100}
assert a['minima']['Run']['min_z_cm']>-.01,a['minima']['Run']
rig.animation_data.action=bpy.data.actions['Enton_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;dest=A/'Exports/PolishV4/Enton_Idle.fbx';bpy.ops.export_scene.fbx(filepath=str(dest),use_selection=True,object_types={'ARMATURE','MESH'},axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO');bpy.ops.wm.save_as_mainfile(filepath=str(p));a['source_sha256']=digest(p);a['exports'][0]['sha256']=digest(dest);a['changes']['central_belly_weight_vertices']=count;(A/'PolishV4_Audit.json').write_text(json.dumps(a,indent=2));print('ENTON_CORE_FIXED',count,a['minima'],flush=True)
