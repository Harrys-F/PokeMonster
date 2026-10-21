"""Guarded local sole-weight delta on this session's sources. Never regenerate rigs or actions."""
import bpy,json,hashlib,sys,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2];name=sys.argv[sys.argv.index('--')+1];assert name in ['Myrapla','Enton'];O=R/'Saved/CreatureExpansionV3';proof=next(x for x in json.loads((O/'SolePatchOwnership.json').read_text())if x['species']==name);source=R/proof['source'];digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert digest(source)==proof['sha256'],'Changed since ownership proof; no write';assert not(O/('SolePatch'+name+'.json')).exists();A=source.parents[1];validation='MyraplaValidationCorrected'if name=='Myrapla'else'EntonValidationFinal';checked=json.loads((O/validation/'Result.json').read_text())
for entry in checked['roundtrips']:assert digest(A/'Exports/MeshyV1'/(name+'_'+entry['role']+'.fbx'))==entry['sha256']
assert bpy.app.background;bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects[name+'_Body'];rig=bpy.data.objects[name+'_Rig'];scene=bpy.context.scene

def action_hash():
 rows=[]
 for action in sorted(bpy.data.actions,key=lambda a:a.name):
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:rows.append((action.name,curve.data_path,curve.array_index,[(tuple(k.co),k.interpolation)for k in curve.keyframe_points]))
 return hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
def invariant_hash():
 rows={'vertices':[tuple(v.co)for v in body.data.vertices],'faces':[tuple(p.vertices)for p in body.data.polygons],'uv':[tuple(v.uv)for v in body.data.uv_layers.active.data],'bones':[(b.name,[[float(v)for v in row]for row in b.matrix_local],b.parent.name if b.parent else None)for b in rig.data.bones],'materials':[m.name for m in body.data.materials],'images':[(i.name,hashlib.sha256(i.packed_file.data).hexdigest())for i in bpy.data.images if i.type=='IMAGE']}
 return hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
old_actions=action_hash();old_invariants=invariant_hash();old_action=rig.animation_data.action;old_range=(scene.frame_start,scene.frame_end,scene.frame_current);limit=.035 if name=='Myrapla'else .045;delta=[]
for vertex in body.data.vertices:
 if vertex.co.z>=limit:continue
 foot='foot_L'if round(vertex.co.x,6)>0 else'foot_R';before={body.vertex_groups[g.group].name:g.weight for g in vertex.groups}
 if before=={foot:1.}:continue
 delta.append({'vertex':vertex.index,'before':before,'after':{foot:1.}})
assert delta
# Preserve the exact local inverse delta before touching any weights; not a source/project backup.
(O/('SoleWeightDelta_'+name+'.json')).write_text(json.dumps({'source_before_sha256':proof['sha256'],'actions_sha256':old_actions,'delta':delta},indent=2))
for change in delta:
 for group in body.vertex_groups:group.remove([change['vertex']])
 body.vertex_groups[next(iter(change['after']))].add([change['vertex']],1.,'REPLACE')
assert action_hash()==old_actions and invariant_hash()==old_invariants;audit=json.loads((A/'MeshyV1_AnimationAudit.json').read_text());ground={}
for role in ['Walk','Run']:
 rig.animation_data.action=bpy.data.actions[name+'_'+role];heights=[]
 for frame in range(1,audit[role]['frames']+1):
  scene.frame_set(frame);bpy.context.view_layer.update();obj=body.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=obj.to_mesh();heights.append(min(v.co.z for v in mesh.vertices));obj.to_mesh_clear()
 ground[role]={'before_min_z_m':audit[role]['min_z_m'],'after_min_z_m':min(heights)};audit[role]['min_z_m']=min(heights);audit[role]['max_min_z_m']=max(heights)
assert all(d['after_min_z_m']>=d['before_min_z_m']-.00001 for d in ground.values()),ground
exports=[]
for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
 rig.animation_data.action=bpy.data.actions[name+'_'+role];scene.frame_start=1;scene.frame_end=audit[role]['frames'];scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(True);bpy.context.view_layer.objects.active=rig;dest=A/'Exports/MeshyV1'/(name+'_'+role+'.fbx');bpy.ops.export_scene.fbx(filepath=str(dest),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO');exports.append({'role':role,'sha256':digest(dest)})
rig.animation_data.action=old_action;scene.frame_start,scene.frame_end=old_range[:2];scene.frame_set(old_range[2]);assert action_hash()==old_actions and invariant_hash()==old_invariants;bpy.ops.wm.save_as_mainfile(filepath=str(source));(A/'MeshyV1_AnimationAudit.json').write_text(json.dumps(audit,indent=2));result={'species':name,'source_before_sha256':proof['sha256'],'source_after_sha256':digest(source),'changed_vertices':len(delta),'sole_threshold_m':limit,'actions_unchanged_sha256':old_actions,'geometry_uv_rig_materials_images_unchanged_sha256':old_invariants,'ground':ground,'exports':exports};(O/('SolePatch'+name+'.json')).write_text(json.dumps(result,indent=2));print('LOCAL_SOLE_DELTA',name,json.dumps(ground),flush=True)
