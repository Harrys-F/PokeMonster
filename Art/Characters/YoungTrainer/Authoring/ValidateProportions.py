"""Read-only validation of V2 against V1. Never changes rig or saves a blend."""
import bpy,bmesh,json,hashlib,math
from pathlib import Path
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
OUT=ROOT.parents[2]/'Saved/YoungTrainerProportions'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def serial(value):
 try:return list(value)
 except TypeError:return value
def snapshot():
 meshes=list(bpy.data.collections['YT_Character'].objects)
 arm=bpy.data.objects['YT_Rig']
 mats={}
 for m in bpy.data.materials:
  mats[m.name]={'diffuse':list(m.diffuse_color),'nodes':[],'links':[]}
  if m.node_tree:
   for n in m.node_tree.nodes:
    mats[m.name]['nodes'].append((n.name,n.bl_idname,n.image.name if n.type=='TEX_IMAGE' and n.image else None,
      [(s.identifier,serial(s.default_value)) for s in n.inputs if hasattr(s,'default_value')]))
   mats[m.name]['links']=[(l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in m.node_tree.links]
 return {'bones':[(b.name,list(b.head_local),list(b.tail_local),b.parent.name if b.parent else None,b.use_deform,
                   [list(row) for row in b.matrix_local]) for b in arm.data.bones],
  'pose':[(b.name,[list(row) for row in b.matrix_basis],[(c.name,c.type) for c in b.constraints]) for b in arm.pose.bones],
  'mesh':{o.name:{'vertices':[list(v.co) for v in o.data.vertices],
   'faces':[list(p.vertices) for p in o.data.polygons],
   'uv':[[list(d.uv) for d in layer.data] for layer in o.data.uv_layers],
   'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices],
   'material':[m.name for m in o.data.materials],
   'modifiers':[(m.name,m.type,m.object.name,m.use_deform_preserve_volume) for m in o.modifiers if m.type=='ARMATURE']}
   for o in meshes if o.type=='MESH'},
  'transforms':{o.name:([list(row) for row in o.matrix_basis],o.parent.name if o.parent else None) for o in meshes},
  'materials':mats,'actions':[a.name for a in bpy.data.actions],
  'base_scene':{o.name:(o.type,[list(row) for row in o.matrix_basis],
   [list(v.co) for v in o.data.vertices] if o.type=='MESH' else None) for o in bpy.data.scenes['Scene'].objects}}
def bounds(points):
 lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
 return {'min_m':lo,'max_m':hi,'dimensions_m':[b-a for a,b in zip(lo,hi)]}
old_path=ROOT/'Source/YoungTrainer_Reference_V1.blend'
new_path=ROOT/'Source/YoungTrainer_Proportions_V2.blend'
bpy.ops.wm.open_mainfile(filepath=str(old_path));before=snapshot()
bpy.ops.wm.open_mainfile(filepath=str(new_path));after=snapshot()
assert before==after,'Protected source geometry, rig, UV, material or weights changed'
stats=[];parts={};points=[]
for o in bpy.data.collections['YT_Character'].objects:
 if o.type!='MESH':continue
 keys=o.data.shape_keys.key_blocks
 assert [k.name for k in keys]==['Basis','Proportions_Silhouette_V2'] and keys[-1].value==1
 assert [list(v.co) for v in keys[0].data]==before['mesh'][o.name]['vertices']
 assert o.data.shape_keys.animation_data is None
 ps=[v.co.copy() for v in keys[-1].data];assert all(math.isfinite(c) for p in ps for c in p)
 bm=bmesh.new();bm.from_mesh(o.data)
 for v,p in zip(bm.verts,ps):v.co=p
 bm.normal_update()
 row={'name':o.name,'vertices':len(bm.verts),'faces':len(bm.faces),
  'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces),
  'boundary_edges':sum(e.is_boundary for e in bm.edges),
  'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)}
 assert row['zero_area_faces']==row['boundary_edges']==row['nonmanifold_edges']==0,row
 stats.append(row);bm.free();points+=ps
 parts[o['part']]={'before':bounds([v.co for v in keys[0].data]),'after':bounds(ps)}
all_bounds=bounds(points)
assert abs(all_bounds['min_m'][2])<1e-6 and abs(all_bounds['max_m'][2]-1.4)<1e-6
refs=bpy.data.collections['REF_CHARACTER'].objects;assert len(refs)==8
ref_rows=[]
for o in refs:
 assert o.type=='EMPTY' and o.empty_display_type=='IMAGE'
 assert all(o.lock_location) and all(o.lock_rotation) and all(o.lock_scale) and o.hide_select
 assert abs(o.color[3]-.4)<1e-6 and o.data.packed_file
 assert abs((o.rotation_euler.to_matrix()@__import__('mathutils').Vector((0,1,0))).z-1)<1e-6
 assert abs(o.location.z)<1e-6 and abs(o.empty_display_size/max(o.data.size)-o['scale_m_per_pixel'])<1e-7
 ref_rows.append({'name':o.name,'opacity':o.color[3],'size_m':o.empty_display_size,
  'image':o.data.filepath,'locked':True,'packed':True,'ground_z_m':0})
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
old_files=manifest['files'];assert all(sha(ROOT/r['path'])==r['sha256'] for r in old_files)
assert sha(old_path)==sha(ROOT/'Source/Stages/06_PreProportions.blend')
assert sha(old_path)=='985784203c7e346b4b6a4a0e1053bbc955b1dd0c5764d47cb3eb49def819b22b'
report={'status':'PASS','source_reopened':str(new_path),'height_m':1.4,'bounds':all_bounds,
 'protected_data_equal':True,'old_manifest_files_unchanged':len(old_files),'backup_byte_identical':True,
 'mesh_count':len(stats),'bone_count':len(bpy.data.objects['YT_Rig'].data.bones),
 'reference_count':len(ref_rows),'references':ref_rows,'mesh_checks':stats,'part_bounds':parts,
 'rig_refit_done':False,'animation_validation_done':False,'old_sha256':sha(old_path),'new_sha256':sha(new_path)}
(OUT/'Audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['references','mesh_checks','part_bounds']},indent=2))
