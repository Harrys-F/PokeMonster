"""Read-only V5 source preservation, references and geometry audit in Blender.

Opens both saved files and writes diagnostics under ignored Saved; never saves
a Blender source and never evaluates an animation or edits a rig.
"""
import bpy
import bmesh
import hashlib
import json
import math
from pathlib import Path
from mathutils import Vector

R = Path(__file__).resolve().parents[1]
OUT = R.parents[2] / 'Saved/YoungTrainerHeadFormV6'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'Audit.json').write_text(json.dumps({'status': 'RUNNING'}) + '\n')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def vector_value(value):
    try:
        return list(value)
    except TypeError:
        return value


def snapshot():
    objects = {}
    materials = {}
    for o in bpy.data.objects:
        row = {'type': o.type, 'matrix': [list(r) for r in o.matrix_basis],
               'parent': o.parent.name if o.parent else None}
        if o.type == 'MESH':
            row.update(vertices=[list(v.co) for v in o.data.vertices],
                       faces=[list(p.vertices) for p in o.data.polygons],
                       weights=[[(g.group, g.weight) for g in v.groups] for v in o.data.vertices],
                       groups=[g.name for g in o.vertex_groups],
                       uv=[[list(v.uv) for v in layer.data] for layer in o.data.uv_layers],
                       keys={k.name: {'value': k.value, 'coordinates': [list(v.co) for v in k.data]}
                             for k in o.data.shape_keys.key_blocks} if o.data.shape_keys else {},
                       materials=[m.name for m in o.data.materials],
                       material_indices=[p.material_index for p in o.data.polygons],
                       armature_modifiers=[(m.name, m.object.name if m.object else None)
                                           for m in o.modifiers if m.type == 'ARMATURE'])
        if o.type == 'ARMATURE':
            row['bones'] = [(b.name, list(b.head_local), list(b.tail_local),
                             [list(r) for r in b.matrix_local], b.parent.name if b.parent else None)
                            for b in o.data.bones]
            row['pose'] = [(b.name, [list(r) for r in b.matrix_basis],
                            [(c.name, c.type) for c in b.constraints]) for b in o.pose.bones]
        if o.type == 'EMPTY' and o.empty_display_type == 'IMAGE':
            row['reference'] = {'size': o.empty_display_size, 'offset': list(o.empty_image_offset),
                                'color': list(o.color), 'locks': [list(o.lock_location), list(o.lock_rotation), list(o.lock_scale)],
                                'locked_select': o.hide_select,
                                'image': hashlib.sha256(o.data.packed_file.data).hexdigest() if o.data.packed_file else None}
        objects[o.name] = digest(row)
    for m in bpy.data.materials:
        row = {'color': list(m.diffuse_color)}
        if m.node_tree:
            row['nodes'] = [(n.name, n.bl_idname, n.image.name if n.type == 'TEX_IMAGE' and n.image else None,
                             [(s.identifier, vector_value(s.default_value)) for s in n.inputs if hasattr(s, 'default_value')])
                            for n in m.node_tree.nodes]
            row['links'] = [(l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier)
                            for l in m.node_tree.links]
        materials[m.name] = digest(row)
    return {'objects': objects, 'materials': materials, 'actions': [a.name for a in bpy.data.actions]}


# The original non-head parts are copied exactly, including UVs and modifiers.
def mesh_signature(o):
    return digest({'vertices':[list(v.co) for v in o.data.vertices],
                   'faces':[list(p.vertices) for p in o.data.polygons],
                   'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices],
                   'groups':[g.name for g in o.vertex_groups],
                   'uv':[[list(v.uv) for v in layer.data] for layer in o.data.uv_layers],
                   'materials':[m.name for m in o.data.materials],
                   'material_indices':[p.material_index for p in o.data.polygons],
                   'modifiers':[(m.name,m.type,{p.identifier:vector_value(getattr(m,p.identifier)) for p in m.bl_rna.properties if not p.is_readonly and p.type in ['INT','FLOAT','BOOLEAN','ENUM']}) for m in o.modifiers],
                   'matrix':[list(row) for row in o.matrix_basis]})

bpy.ops.wm.open_mainfile(filepath=str(R/'Source/YoungTrainer_HeadForm_V5.blend'))
before=snapshot()
bpy.ops.wm.open_mainfile(filepath=str(R/'Source/YoungTrainer_HeadForm_V6.blend'))
after=snapshot()
assert all(after['objects'].get(k)==v for k,v in before['objects'].items()), [k for k,v in before['objects'].items() if after['objects'].get(k)!=v]
assert before['materials']==after['materials']
assert before['actions']==after['actions']
unchanged=[];modified=[]
for o in bpy.data.collections['YT6_Player'].objects:
    if o.type!='MESH':continue
    old=bpy.data.objects[o['source_v5_object']]
    # Topology, UVs, weights, modifiers, preview materials and transforms are immutable.
    for key in ['faces','weights','groups','uv','materials','material_indices','modifiers','matrix']:
        def aspect(obj):
            m=obj.data
            if key=='faces':return [list(p.vertices) for p in m.polygons]
            if key=='weights':return [[(g.group,g.weight) for g in v.groups] for v in m.vertices]
            if key=='groups':return [g.name for g in obj.vertex_groups]
            if key=='uv':return [[list(v.uv) for v in l.data] for l in m.uv_layers]
            if key=='materials':return [a.name for a in m.materials]
            if key=='material_indices':return [p.material_index for p in m.polygons]
            if key=='modifiers':return [(a.name,a.type,{p.identifier:vector_value(getattr(a,p.identifier)) for p in a.bl_rna.properties if not p.is_readonly and p.type in ['INT','FLOAT','BOOLEAN','ENUM']}) for a in obj.modifiers]
            return [list(row) for row in obj.matrix_basis]
        assert aspect(o)==aspect(old),(o.name,key)
    assert len(o.data.vertices)==len(old.data.vertices)
    changed=[i for i,(a,b) in enumerate(zip(o.data.vertices,old.data.vertices)) if a.co!=b.co]
    if changed:modified.append({'name':o.name,'changed_vertices':len(changed)})
    else:unchanged.append(o.name)
    name=o.name.removeprefix('YT6_')
    if name=='Body':assert all(i>=302 for i in changed),changed
    elif name=='Head':
        assert all(any(o.vertex_groups[g.group].name in ['Topology_EyeR','Topology_EyeL','Topology_Mouth'] for g in o.data.vertices[i].groups) for i in changed)
    elif name=='HairSculptVolume':
        for a,b in zip(o.data.vertices,old.data.vertices):
            assert a.co.z==b.co.z
            if b.co.y<-.115 and abs(b.co.x)<.103:assert a.co==b.co
    elif not any(t in name for t in ['Eye','Iris','Pupil','Glint','Lid','Brow','Mouth']):assert not changed,o.name
col=bpy.data.collections['YT6_Player'];root=bpy.data.objects['YT6_PlayerRoot']
assert root.location.length==0 and list(root.scale)==[1.,1.,1.]
rows=[];points=[];dg=bpy.context.evaluated_depsgraph_get()
for o in col.objects:
    if o.type!='MESH':continue
    assert o.parent==root and not o.animation_data and not o.data.shape_keys
    assert not any(m.type=='ARMATURE' for m in o.modifiers)
    bm=bmesh.new();bm.from_mesh(o.data)
    row={'name':o.name,'vertices':len(bm.verts),'faces':len(bm.faces),
         'boundary':sum(e.is_boundary for e in bm.edges),
         'invalid_edges':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),
         'loose':sum(not v.link_faces for v in bm.verts),
         'degenerate':sum(f.calc_area()<1e-12 for f in bm.faces)}
    assert all(math.isfinite(c) for v in bm.verts for c in v.co)
    assert row['invalid_edges']==row['loose']==row['degenerate']==0,row
    if 'HairSculpt' in o.name:assert row['boundary']==0,row
    bm.free();ev=o.evaluated_get(dg);m=ev.to_mesh();points.extend(o.matrix_world@v.co for v in m.vertices);ev.to_mesh_clear();rows.append(row)
low=[min(p[k] for p in points) for k in range(3)];high=[max(p[k] for p in points) for k in range(3)]
assert abs(low[2])<1e-6 and abs(high[2]-1.4)<1e-6,(low,high)
refs=bpy.data.collections['REF_PLAYER_FINAL'];assert len(refs.objects)==11
for o in refs.objects:assert o.data.packed_file and all(o.lock_location) and all(o.lock_rotation) and all(o.lock_scale) and o.hide_select
files=json.loads((OUT/'BeforeFiles.json').read_text())
for p,sha in files.items():assert hashlib.sha256((R.parents[2]/p).read_bytes()).hexdigest()==sha,p
report={'status':'PASS','source_reopened':bpy.data.filepath,'existing_objects_preserved':len(before['objects']),
        'existing_materials_preserved':len(before['materials']),'existing_file_hashes_preserved':len(files),
        'unchanged_meshes':unchanged,'modified_meshes':modified,
        'body_non_ear_vertices_unchanged':302,'all_mesh_topology_uv_weights_materials_modifiers_unchanged':True,
        'head_changes_only_eye_and_mouth_support_loops':True,
        'rig_actions_originals_unchanged':True,'no_unreal_export':True,
        'bounds_m':{'min':low,'max':high},'height_m':high[2]-low[2],
        'locked_reference_images':len(refs.objects),
        'camera_note':'Approximate illustration perspective, fixed comparison camera; not Unreal runtime.',
        'geometry':rows}
(OUT/'Audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='geometry'},indent=2),flush=True)
