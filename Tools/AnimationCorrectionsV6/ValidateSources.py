"""Reopen each packed source and actually reimport every V6 FBX; no source writes."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];rows=[]
for name in ['Player','Glurak','Nebulak','Machomei','Myrapla']:
 A=R/('Art/Characters/YoungTrainer'if name=='Player'else'Art/Characters/Creatures/'+name);a=json.loads((A/'AnimationCorrectionsV6_Audit.json').read_text());source=R/a['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==a['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(source));rig=bpy.data.objects['Player_Meshy_Rig'if name=='Player'else name+'_Rig'];bones=len(rig.data.bones);assert all(bpy.data.actions.get(x)for x in a['actions'].values());images=[im for im in bpy.data.images if im.type=='IMAGE'and im.size[0]>0];assert images and all(im.packed_file for im in images)
 for x in a['exports']:
  p=R/x['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'];bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(p),use_anim=True);rigs=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'];assert len(rigs)==1 and len(rigs[0].data.bones)==bones,(name,x['role']);assert bpy.data.actions;meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert bool(meshes)==x['mesh'];rows.append(dict(species=name,role=x['role'],bones=bones,meshes=len(meshes),sha256=x['sha256']));print('ROUNDTRIP_OK',name,x['role'],flush=True)
(R/'Saved/AnimationCorrectionsV6/Roundtrips.json').write_text(json.dumps(rows,indent=2))
