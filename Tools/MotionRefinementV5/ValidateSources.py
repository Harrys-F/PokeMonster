"""Reopen packed candidates, verify original model shape and really roundtrip every exported FBX."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];rows=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['Glurak','Nebulak','Player']:
 A=R/('Art/Characters/YoungTrainer'if name=='Player'else'Art/Characters/Creatures/'+name);audit=json.loads((A/('MotionQualityV3_Audit.json'if name=='Player'else'MotionV5_Audit.json')).read_text());p=R/audit['source'];assert sha(p)==audit['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(p));rig=bpy.data.objects['Player_Meshy_Rig'if name=='Player'else name+'_Rig'];body=bpy.data.objects['Player_Meshy_Body'if name=='Player'else name+'_Body'];bones=len(rig.data.bones);body.data.calc_loop_triangles();triangles=len(body.data.loop_triangles);assert all(i.packed_file for i in bpy.data.images if i.type=='IMAGE'and i.users>0);exports=[]
 for x in audit['exports']:
  f=R/x['path'];assert sha(f)==x['sha256'];bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(f),automatic_bone_orientation=False);arms=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'];meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
  if x.get('static_mesh'):
   assert not arms and len(meshes)==1;meshes[0].data.calc_loop_triangles();assert len(meshes[0].data.loop_triangles)==audit['envelope_triangles'];assert meshes[0].data.color_attributes
  else:
   assert len(arms)==1 and len(arms[0].data.bones)==bones;assert len(meshes)==int(x['contains_mesh']);assert len(bpy.data.actions)==1
   if meshes:meshes[0].data.calc_loop_triangles();assert len(meshes[0].data.loop_triangles)==triangles
  exports.append(dict(role=x['role'],sha256=x['sha256'],passed=True))
 rows.append(dict(species=name,packed_source_reopened=True,bones=bones,body_triangles=triangles,exports=exports));print('SOURCE_AND_FBX_ROUNDTRIPS_PASS',name,len(exports),flush=True)
(R/'Saved/MotionRefinementV5/Roundtrips.json').write_text(json.dumps(rows,indent=2))
