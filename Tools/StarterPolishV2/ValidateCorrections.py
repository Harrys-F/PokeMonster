"""Actual FBX reimport + original geometry/UV comparison + 61 poses per current starter clip."""
import bpy,json,numpy as np,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];rows=[]
for species in ['Zunderlauf','Bisasam']:
 A=R/'Art/Characters/Creatures'/species;a=json.loads((A/'PolishV2_AnimationAudit.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(R/a['reference']));expected_bones=len(bpy.data.objects['Glumanda_Meshy_Rig'if species=='Zunderlauf'else'Bisasam_Rig'].data.bones);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(R/a['export']),automatic_bone_orientation=False);rig=next(x for x in bpy.data.objects if x.type=='ARMATURE');body=next(x for x in bpy.data.objects if x.type=='MESH');assert len(rig.data.bones)==expected_bones;bpy.context.scene.frame_set(1);pts=[body.matrix_world@v.co for v in body.data.vertices];height=max(p.z for p in pts)-min(p.z for p in pts);assert abs(height-(.60 if species=='Zunderlauf'else .70))<.015,(species,height)
 row={'species':species,'fbx_reimport_height_m':height,'bone_count':len(rig.data.bones),'source_reopened':True};rows.append(row)
 if species=='Zunderlauf':
  bpy.ops.wm.open_mainfile(filepath=str(R/a['reference']));body=bpy.data.objects['Glumanda_Meshy'];rig=bpy.data.objects['Glumanda_Meshy_Rig']
  with bpy.data.libraries.load(str(R/a['source']),link=False)as(fr,to):to.actions=['Glumanda_Faint_PolishV2']
  roles=[('Faint',bpy.data.actions['Glumanda_Faint_PolishV2'])]
 else:
  bpy.ops.wm.open_mainfile(filepath=str(R/a['reference']));original=bpy.data.objects['Bisasam_Body'];geometry=[tuple(v.co)for v in original.data.vertices];polygons=[tuple(f.vertices)for f in original.data.polygons];uv=[tuple(x.uv)for x in original.data.uv_layers.active.data];bpy.ops.wm.open_mainfile(filepath=str(R/a['source']));body=bpy.data.objects['Bisasam_Body'];rig=bpy.data.objects['Bisasam_Rig'];assert geometry==[tuple(v.co)for v in body.data.vertices];assert polygons==[tuple(f.vertices)for f in body.data.polygons];assert uv==[tuple(x.uv)for x in body.data.uv_layers.active.data];row.update(geometry_identical=True,uv_identical=True,triangles_identical=True);roles=[(role,bpy.data.actions['Bisasam_'+role])for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']]
 es=np.array([e.vertices[:]for e in body.data.edges]);rest=np.array([tuple(v.co)for v in body.data.vertices]);length=np.linalg.norm(rest[es[:,0]]-rest[es[:,1]],axis=1);row['clips']=[]
 for role,act in roles:
  rig.animation_data.action=act;growth=[];ground=[]
  for f in np.linspace(*act.frame_range,61):
   bpy.context.scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([tuple(v.co)for v in m.vertices]);growth.append(float((np.linalg.norm(p[es[:,0]]-p[es[:,1]],axis=1)-length).max()));ground.append(float(p[:,2].min()));ev.to_mesh_clear()
  row['clips'].append({'role':role,'samples':61,'max_edge_growth_m':max(growth),'minimum_z_m':min(ground)})
 assert hashlib.sha256((R/a['reference']).read_bytes()).hexdigest()==a['reference_sha256']
(R/'Saved/StarterPolishV2/CorrectionValidation.json').write_text(json.dumps(rows,indent=2));print('FBX_REIMPORT_AND_GEOMETRY_PASS')
