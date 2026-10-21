"""Smooth rear-side geometric wing mask in this task's new candidate only."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Glurak';p=A/'Source/Glurak_PolishV4.blend';a=json.loads((A/'PolishV4_Audit.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not __import__('subprocess').check_output(['git','ls-files','--',str(p.relative_to(R))],cwd=R).strip(),'Candidate is versioned: do not overwrite a released source';assert digest(p)==a['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects['Glurak_Body'];rig=bpy.data.objects['Glurak_Rig'];normals=[tuple(v.normal) for v in body.data.vertices];color=body.data.color_attributes['PolishV4'];count=0
for i,loop in enumerate(body.data.loops):
 v=body.data.vertices[loop.vertex_index];x,y,z=v.co;mask=0.
 if abs(x)>.22 and z>.85 and y>-.05:
  t=max(0.,min(1.,normals[loop.vertex_index][1]/.22));mask=t*t*(3-2*t)
 color.data[i].color=(mask,0,0,1);count+=mask>.01
assert count>30000
s=bpy.context.scene;rig.animation_data.action=bpy.data.actions['Glurak_Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;file=A/'Exports/PolishV4/Glurak_Idle.fbx';bpy.ops.export_scene.fbx(filepath=str(file),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO',colors_type='LINEAR');bpy.ops.wm.save_as_mainfile(filepath=str(p));a['source_sha256']=digest(p);a['exports'][0]['sha256']=digest(file);a['changes']['rear_wing_corners']=count;a['changes']['rear_wing_mask']='smooth vertex-normal mask over rear wing geometry; no texture-color threshold';(A/'PolishV4_Audit.json').write_text(json.dumps(a,indent=2));print('WING_MASK_REFINED',count,flush=True)
