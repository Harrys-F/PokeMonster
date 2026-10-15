import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Source/Hobbit_NPC_MeshyBase_V2_Cleanup.blend';assert not P.exists()
s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V2_Cleanup'];bpy.context.window.scene=s
# Independently copy all imported model data and actions before any repair.
images={};materials={}
for o in s.objects:
 if o.data:o.data=o.data.copy();o.data.name=o.data.name.replace('HNM1_','HNM2_')
 o.name=o.name.replace('HNM1_','HNM2_').split('.')[0]
 if o.type=='MESH':
  for slot in o.material_slots:
   old=slot.material
   if old and old not in materials:
    m=old.copy();m.name=m.name.replace('HNM1_','HNM2_');materials[old]=m
    for n in m.node_tree.nodes:
     if n.type=='TEX_IMAGE' and n.image:
      im=n.image
      if im not in images:
       new=im.copy();new.name=new.name.replace('HNM1_','HNM2_');new.pack();images[im]=new
      n.image=images[im]
   if old:slot.material=materials[old]
rig=s.objects['HNM2_Rig'];o=s.objects['HNM2_Body'];old=o.data
for m in o.modifiers:
 if m.type=='ARMATURE':m.object=rig
actions=[]
for label in ['Idle_V2','Walk_V2','Run_V1']:
 original=next(a for a in bpy.data.actions if a.name.startswith('HNM1_'+label) and (not a.library));act=original.copy();act.name='HNM2_'+label;act.use_fake_user=True;actions.append(act)
rig.animation_data.action=actions[0]
if actions[0].slots:rig.animation_data.action_slot=actions[0].slots[0]
T=B/'Textures/MeshyBaseV2';T.mkdir(parents=True,exist_ok=True)
for im in images.values():
 label=next(t for t in ['BaseColor','ORM','Normal'] if t in im.name);path=T/('T_Hobbit_MeshyBase_V2_'+label+'.png');assert not path.exists();path.write_bytes(im.packed_file.data);im.filepath='//../Textures/MeshyBaseV2/'+path.name
 for packed in im.packed_files:packed.filepath=im.filepath
bpy.data.libraries.write(str(B/'Source/StagesMeshyBaseV2/Hobbit_MeshyBase_V2_00_BeforeCleanup.blend'),{s,*actions,*images.values()})
# Only exactly coincident active vertices with exactly equal weights can share a representative.
groupnames=[g.name for g in o.vertex_groups]
used=set(i for p in old.polygons for i in p.vertices);representative={};key_to_rep={};merged=[];weightdata={v.index:tuple((g.group,g.weight) for g in v.groups) for v in old.vertices}
for v in old.vertices:
 if v.index not in used:continue
 key=(tuple(v.co),weightdata[v.index])
 if key in key_to_rep:representative[v.index]=key_to_rep[key];merged.append([v.index,key_to_rep[key]])
 else:key_to_rep[key]=v.index;representative[v.index]=v.index
reps=sorted(set(representative.values()));index={v:i for i,v in enumerate(reps)};mapping={oldid:index[rep] for oldid,rep in representative.items()}
faces=[tuple(mapping[i] for i in p.vertices) for p in old.polygons];assert all(len(set(f))==len(f) for f in faces),'No collapsed triangle allowed'
uvs={u.name:[tuple(d.uv) for d in u.data] for u in old.uv_layers};normals=[tuple(n.vector) for n in old.corner_normals];smooth=[p.use_smooth for p in old.polygons];mindices=[p.material_index for p in old.polygons]
me=bpy.data.meshes.new('HNM2_CleanedMesh_ExactSurface');me.from_pydata([old.vertices[i].co for i in reps],[],faces);me.update()
for mat in old.materials:me.materials.append(mat)
for i,p in enumerate(me.polygons):p.use_smooth=smooth[i];p.material_index=mindices[i]
for name,values in uvs.items():
 u=me.uv_layers.new(name=name);u.data.foreach_set('uv',[x for pair in values for x in pair])
me.normals_split_custom_set(normals)
idattr=me.attributes.new('V1_OriginalVertexID','INT','POINT')
for i,orig in enumerate(reps):idattr.data[i].value=orig
o.data=me
if len(o.vertex_groups)==0:
 for name in groupnames:o.vertex_groups.new(name=name)
for group in o.vertex_groups:group.remove(list(range(len(me.vertices))))
for newi,oldi in enumerate(reps):
 for gi,w in weightdata[oldi]:o.vertex_groups[gi].add([newi],w,'REPLACE')
assert len(me.polygons)==len(old.polygons)
# Every rendered triangle, UV corner and deform weight must remain the same.
assert all(old.vertices[a].co==me.vertices[b].co for po,pn in zip(old.polygons,me.polygons) for a,b in zip(po.vertices,pn.vertices))
assert all(tuple(d.uv)==uvs[u.name][i] for u in me.uv_layers for i,d in enumerate(u.data))
assert all(tuple((g.group,g.weight) for g in me.vertices[i].groups)==weightdata[orig] for i,orig in enumerate(reps))
s['cleanup_scope']='Remove only non-face vertices/edges; merge only exactly coincident vertices with exactly identical deform weights. Every original face, UV and custom normal retained. Larger cracks remain.'
s['master_height_m']=1.40;s.frame_set(1)
for ob in s.objects:ob.select_set(False)
rig.select_set(True);bpy.context.view_layer.objects.active=rig
rig.data.pose_position=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='REST')
log={'source':str(B/'Source/Hobbit_NPC_MeshyBase_V1.blend'),'output':str(P),'vertices_before':len(old.vertices),'vertices_after':len(me.vertices),'faces_before':len(old.polygons),'faces_after':len(me.polygons),'removed_nonface_vertex_ids':sorted(set(range(len(old.vertices)))-used),'coincident_vertex_merges':merged,'coordinate_change_m':0,'all_original_face_surfaces_exact':True,'all_original_uv_corners_exact':True,'all_weights_exact':True,'custom_normals_retained':True,'added_or_deleted_faces':0,'global_remesh':False,'small_geometry_islands_removed':False,'skeleton_modified':False}
(B/'Review/MeshyBaseV2/Repairs.json').write_text(json.dumps(log,indent=2));bpy.data.libraries.write(str(P),{s,*actions,*images.values()},fake_user=True)
print('Saved V2 exact-surface cleanup',len(old.vertices),'->',len(me.vertices),'vertices;',len(merged),'coincident merges; no face changes')
