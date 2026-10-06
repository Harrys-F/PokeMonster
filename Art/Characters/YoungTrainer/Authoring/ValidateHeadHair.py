"""Read-only V2/V3 preservation and head geometry audit; no saves/rig changes."""
import bpy,bmesh,json,hashlib,math
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
OUT=R.parents[2]/'Saved/YoungTrainerHeadPass'
(OUT/'Audit.json').write_text(json.dumps({'status':'RUNNING'})+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def value(x):
 try:return list(x)
 except TypeError:return x
def snap():
 rig=bpy.data.objects['YT_Rig'];meshes={};materials={};refs={}
 for o in bpy.data.objects:
  if o.type!='MESH' or not o.name.startswith('YT_'):continue
  meshes[o.name]={'verts':[list(v.co) for v in o.data.vertices],'faces':[list(p.vertices) for p in o.data.polygons],
   'uv':[[list(v.uv) for v in layer.data] for layer in o.data.uv_layers],
   'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices],
   'keys':{k.name:[list(p.co) for p in k.data] for k in o.data.shape_keys.key_blocks},
   'key_values':{k.name:k.value for k in o.data.shape_keys.key_blocks},
   'materials':[m.name for m in o.data.materials],'material_indices':[p.material_index for p in o.data.polygons],
   'matrix':[list(row) for row in o.matrix_basis],'parent':o.parent.name if o.parent else None,
   'modifiers':[(m.type,m.object.name) for m in o.modifiers if m.type=='ARMATURE']}
 for m in bpy.data.materials:
  materials[m.name]={'color':list(m.diffuse_color),'nodes':[(n.name,n.bl_idname,n.image.name if n.type=='TEX_IMAGE' and n.image else None,
    [(s.identifier,value(s.default_value)) for s in n.inputs if hasattr(s,'default_value')]) for n in m.node_tree.nodes] if m.node_tree else [],
   'links':[(l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in m.node_tree.links] if m.node_tree else []}
 for o in bpy.data.collections['REF_CHARACTER'].objects:
  refs[o.name]=([list(row) for row in o.matrix_basis],list(o.color),o.empty_display_size,list(o.empty_image_offset),
   list(o.lock_location),list(o.lock_rotation),list(o.lock_scale),o.hide_select,
   hashlib.sha256(o.data.packed_file.data).hexdigest())
 return {'rig':{'bones':[(b.name,list(b.head_local),list(b.tail_local),[list(r) for r in b.matrix_local],b.parent.name if b.parent else None) for b in rig.data.bones],
  'pose':[(b.name,[list(r) for r in b.matrix_basis],[(c.name,c.type) for c in b.constraints]) for b in rig.pose.bones],
  'matrix':[list(r) for r in rig.matrix_basis],'actions':[a.name for a in bpy.data.actions]},
  'meshes':meshes,'materials':materials,'references':refs,
  'original_scene':{o.name:(o.type,[list(r) for r in o.matrix_basis]) for o in bpy.data.scenes['Scene'].objects}}
bpy.ops.wm.open_mainfile(filepath=str(R/'Source/YoungTrainer_Proportions_V2.blend'));before=snap()
bpy.ops.wm.open_mainfile(filepath=str(R/'Source/YoungTrainer_HeadHair_V3.blend'));after=snap()
assert before['rig']==after['rig'] and before['references']==after['references'] and before['original_scene']==after['original_scene']
assert all(after['materials'][name]==data for name,data in before['materials'].items())
for name,data in before['meshes'].items():
 current=after['meshes'][name]
 if name!='YT_Body':assert current==data,name
 else:
  assert {k:v for k,v in current.items() if k not in ['keys','key_values','materials','material_indices']}=={k:v for k,v in data.items() if k not in ['keys','key_values','materials','material_indices']}
  assert all(current['keys'][k]==v and current['key_values'][k]==data['key_values'][k] for k,v in data['keys'].items())
  o=bpy.data.objects[name];ear_ids={v.index for v in o.data.vertices if any(o.vertex_groups[g.group].name=='head' and g.weight>.95 for g in v.groups)}
  newkey=current['keys']['HeadHair_V3_EarsOnly'];baseline=data['keys']['Proportions_Silhouette_V2']
  assert all(newkey[i]==baseline[i] for i in range(len(newkey)) if i not in ear_ids)
  assert current['materials'][:len(data['materials'])]==data['materials']
  assert all(current['material_indices'][i]==data['material_indices'][i] for i,p in enumerate(o.data.polygons) if not all(v in ear_ids for v in p.vertices))
archive=bpy.data.collections['YT_HeadHair_Source_V2'];assert archive.hide_render and archive.hide_viewport
assert sorted(o.name for o in archive.objects)==['YT_Eyes','YT_Face','YT_Hair','YT_Head']
rows=[];allpoints=[]
for o in bpy.data.collections['YT_HeadHair_V3'].objects:
 assert o.type=='MESH' and o.parent.name=='YT_CharacterRoot' and not any(m.type=='ARMATURE' for m in o.modifiers)
 assert o.animation_data is None and o.data.animation_data is None and len(o.data.uv_layers)==0
 bm=bmesh.new();bm.from_mesh(o.data)
 row={'object':o.name,'vertices':len(bm.verts),'quads':sum(len(f.verts)==4 for f in bm.faces),
  'triangles':sum(len(f.verts)==3 for f in bm.faces),'ngons':sum(len(f.verts)>4 for f in bm.faces),
  'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_nonboundary':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),
  'loose_vertices':sum(not v.link_faces for v in bm.verts),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces)}
 assert row['ngons']==row['nonmanifold_nonboundary']==row['loose_vertices']==row['zero_area_faces']==0,row
 assert all(math.isfinite(c) for v in bm.verts for c in v.co)
 if 'Curl' in o.name or 'Sweep' in o.name:assert row['boundary_edges']==0,row
 rows.append(row);allpoints+=[v.co.copy() for v in bm.verts];bm.free()
head=bpy.data.objects['YT3_Head'];assert json.loads(head['facial_loops_json'])=={'EyeR':[40]*4,'EyeL':[40]*4,'Mouth':[20]*4}
assert next(r for r in rows if r['object']=='YT3_Head')['boundary_edges']==100
initial=json.loads((OUT/'InitialFiles.json').read_text());assert all(sha(R/p)==digest for p,digest in initial.items())
assert sha(R/'Source/Stages/07_PreHeadHair.blend')==sha(R/'Source/YoungTrainer_Proportions_V2.blend')
portrait=bpy.data.objects['REF_CharacterPortrait'];assert portrait.data.packed_file and all(portrait.lock_location) and all(portrait.lock_rotation) and all(portrait.lock_scale) and portrait.hide_select
low=[min(p[i] for p in allpoints) for i in range(3)];high=[max(p[i] for p in allpoints) for i in range(3)]
assert abs(high[2]-1.4)<1e-6
report={'status':'PASS','protected_old_files':len(initial),'rig_and_actions_unchanged':True,'existing_references_unchanged':True,
 'clothing_backpack_body_non_ear_vertices_unchanged':True,'original_materials_unchanged':True,'backup_byte_identical':True,
 'new_head_meshes':len(rows),'large_hair_groups':bpy.data.scenes['YoungTrainer_Reference_V1']['head_pass_hair_groups'],
 'head_region_bounds_m':{'min':low,'max':high},'facial_loop_counts':json.loads(head['facial_loops_json']),
 'intentional_boundaries':'Head: two eyes + mouth (100). Hair base: underside (48). Colored eye surfaces: disc perimeters.',
 'new_skinning_or_facial_rig':False,'animation_test_performed':False,'geometry_audit':rows,
 'v2_sha256':sha(R/'Source/YoungTrainer_Proportions_V2.blend'),'v3_sha256':sha(R/'Source/YoungTrainer_HeadHair_V3.blend')}
(OUT/'Audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='geometry_audit'},indent=2))
