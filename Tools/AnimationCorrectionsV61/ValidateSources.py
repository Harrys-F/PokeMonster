"""Reopen both packed sources, compare original topology/UV/rig/actions and really reimport the FBX."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];out=[]
def sample(path,name):
 bpy.ops.wm.open_mainfile(filepath=str(path));b=bpy.data.objects['Player_Meshy_Body'if name=='Player'else'Glurak_Body'];r=bpy.data.objects['Player_Meshy_Rig'if name=='Player'else'Glurak_Rig'];actions={}
 for a in bpy.data.actions:
  values=[]
  for layer in a.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for f in bag.fcurves:values.append((f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points]))
  actions[a.name]=hashlib.sha256(repr(values).encode()).hexdigest()
 return dict(coords=[tuple(v.co)for v in b.data.vertices],uv=[tuple(v.uv)for v in b.data.uv_layers.active.data],faces=[tuple(p.vertices)for p in b.data.polygons],materials=[p.material_index for p in b.data.polygons],rest={x.name:(x.parent.name if x.parent else None,[list(row)for row in x.matrix_local])for x in r.data.bones},actions=actions,images=[dict(name=i.name,packed=bool(i.packed_file))for i in bpy.data.images if i.size[0]>0 and i.source not in {'VIEWER','GENERATED'}],weights=[{b.vertex_groups[g.group].name:g.weight for g in v.groups if g.weight>0}for v in b.data.vertices])
for name in ['Player','Glurak']:
 A=R/('Art/Characters/YoungTrainer'if name=='Player'else'Art/Characters/Creatures/Glurak');audit=json.loads((A/'AnimationCorrectionsV61_Audit.json').read_text());old=sample(R/audit['previous'],name);new=sample(R/audit['source'],name)
 for k in ['coords','uv','faces','materials','rest','actions']:assert new[k]==old[k],(name,k)
 assert all(x['packed']for x in new['images']),new['images']
 if name=='Glurak':assert old['weights']==new['weights']
 for w in new['weights']:assert abs(sum(w.values())-1)<.001 and len(w)<=4
 source=R/audit['export'];assert hashlib.sha256(source.read_bytes()).hexdigest()==audit['export_sha256'];bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(source),use_anim=True);arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');mesh=next(o for o in bpy.context.scene.objects if o.type=='MESH');assert len(arm.data.bones)==len(new['rest']);assert abs(mesh.dimensions.z-(1.4 if name=='Player'else 1.7))<.01
 out.append(dict(name=name,source=audit['source'],export=audit['export'],original_topology_uv_material_slots_rest_and_all_actions_exact=True,all_images_packed=True,fbx_reimported=True,imported_idle_pose_height_m=mesh.dimensions.z,rest_bones=len(arm.data.bones),changed_entries=len(audit['changes'])))
 print('V61_SOURCE_VALID',name,flush=True)
(R/'Saved/AnimationCorrectionsV61/SourceValidation.json').write_text(json.dumps(out,indent=2))
