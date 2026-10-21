"""Reopen packed sources and reimport every new FBX. Read-only files, no review renders."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];rows=[]
for name in ['Enton','Nebulak','Glurak']:
 A=R/'Art/Characters/Creatures'/name;a=json.loads((A/'PolishV4_Audit.json').read_text());p=R/a['source'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(p));body=bpy.data.objects[name+'_Body'];ref=bpy.data.objects[name+'_UNMODIFIED_GLB'];rig=bpy.data.objects[name+'_Rig'];assert len(body.data.vertices)==len(ref.data.vertices);assert [tuple(v.uv)for v in body.data.uv_layers.active.data]==[tuple(v.uv)for v in ref.data.uv_layers.active.data];assert all(i.packed_file for i in bpy.data.images if i.type=='IMAGE');bones=len(rig.data.bones);body.data.calc_loop_triangles();tri=len(body.data.loop_triangles);checks=[]
 for e in a['exports']:
  f=A/'Exports/PolishV4'/(name+'_'+e['role']+'.fbx');assert hashlib.sha256(f.read_bytes()).hexdigest()==e['sha256'];bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(f),automatic_bone_orientation=False);arms=[o for o in bpy.data.objects if o.type=='ARMATURE'];meshes=[o for o in bpy.data.objects if o.type=='MESH'];assert len(arms)==1 and len(arms[0].data.bones)==bones;assert len(meshes)==int(e['contains_mesh']);assert len(bpy.data.actions)==1
  if meshes:
   meshes[0].data.calc_loop_triangles();assert len(meshes[0].data.loop_triangles)==tri
   if name!='Enton':assert meshes[0].data.color_attributes
  checks.append(dict(role=e['role'],bones=bones,mesh=e['contains_mesh'],sha256=e['sha256']))
 rows.append(dict(species=name,packed_reopened=True,original_uvs=True,original_topology=True,roundtrips=checks));print('POLISH_ROUNDTRIP_PASS',name,flush=True)
(R/'Saved/CreaturePolishV4/Roundtrips.json').write_text(json.dumps(rows,indent=2))
