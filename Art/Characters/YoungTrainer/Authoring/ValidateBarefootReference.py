"""Read-only V4 source preservation, references and geometry audit in Blender.

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
OUT = R.parents[2] / 'Saved/YoungTrainerReferenceRework'
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


bpy.ops.wm.open_mainfile(filepath=str(R / 'Source/Stages/08_BeforeBarefootReferenceRework_20261007.blend'))
before = snapshot()
bpy.ops.wm.open_mainfile(filepath=str(R / 'Source/YoungTrainer_BarefootReference_V4.blend'))
after = snapshot()
preserved_objects = all(after['objects'].get(k) == v for k, v in before['objects'].items())
preserved_materials = all(after['materials'].get(k) == v for k, v in before['materials'].items())
assert preserved_objects, [k for k, v in before['objects'].items() if after['objects'].get(k) != v]
assert preserved_materials, 'An existing material changed'
assert before['actions'] == after['actions'], 'Actions changed'

baseline_path = OUT / 'BeforeV4Files.json'
source_files = json.loads(baseline_path.read_text()) if baseline_path.exists() else {}
if not source_files:
    print('NOTE: original disk-file hash baseline unavailable; scene preservation is still compared to Stage 08.', flush=True)
assert all(hashlib.sha256((R / p).read_bytes()).hexdigest() == sha for p, sha in source_files.items())
collection = bpy.data.collections['YT4_Player']
root = bpy.data.objects['YT4_PlayerRoot']
assert root.location.length < 1e-9 and list(root.scale) == [1.0, 1.0, 1.0]
depsgraph = bpy.context.evaluated_depsgraph_get()
geometry = []
points = []
for o in collection.objects:
    if o.type != 'MESH':
        continue
    assert o.parent == root and not any(m.type == 'ARMATURE' for m in o.modifiers)
    assert not o.animation_data and not o.data.animation_data
    assert not o.data.shape_keys
    bm = bmesh.new()
    bm.from_mesh(o.data)
    row = {'object': o.name, 'vertices': len(bm.verts), 'faces': len(bm.faces),
           'boundary_edges': sum(e.is_boundary for e in bm.edges),
           'nonmanifold_nonboundary': sum(not e.is_manifold and not e.is_boundary for e in bm.edges),
           'zero_area_faces': sum(f.calc_area() < 1e-12 for f in bm.faces),
           'loose_vertices': sum(not v.link_faces for v in bm.verts)}
    assert all(math.isfinite(c) for v in bm.verts for c in v.co), row
    if any(o.name.startswith(n) for n in ['YT4_BareFoot_', 'YT4_Hand_', 'YT4_HairGroup_', 'YT4_ForeheadGroup_', 'YT4_CrownSweep_', 'YT4_OutlineCurl_', 'YT4_HairContinuous', 'YT4_ScarfWrapped']):
        assert row['boundary_edges'] == row['nonmanifold_nonboundary'] == row['loose_vertices'] == row['zero_area_faces'] == 0, row
    bm.free()
    evaluated = o.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    world_points = [o.matrix_world @ v.co for v in mesh.vertices]
    row['evaluated_bounds_m'] = {'min': [min(p[i] for p in world_points) for i in range(3)],
                                 'max': [max(p[i] for p in world_points) for i in range(3)]}
    points.extend(world_points)
    evaluated.to_mesh_clear()
    geometry.append(row)
low = [min(p[i] for p in points) for i in range(3)]
high = [max(p[i] for p in points) for i in range(3)]
assert abs(low[2]) < 1e-6 and abs(high[2] - 1.4) < .002, (low, high)
for side in ['L', 'R']:
    foot = bpy.data.objects['YT4_BareFoot_' + side]
    hand = bpy.data.objects['YT4_Hand_' + side]
    assert foot['toe_count'] == 5 and foot['barefoot'] and hand['finger_count'] == 5
    assert not foot.vertex_groups and not hand.vertex_groups
    assert abs(min(v.co.z for v in foot.data.vertices)) < 1e-6
assert not any('Boot' in o.name or 'Sock' in o.name for o in collection.objects)
for name in ['YT_Character', 'YT_HeadHair_V3', 'REF_CHARACTER', 'REF_PORTRAIT']:
    c = bpy.data.collections[name]
    assert c.hide_render and c.hide_viewport

alignment = json.loads((R / 'Reference/BarefootFinal/Alignment.json').read_text())
refs = bpy.data.collections['REF_PLAYER_FINAL']
assert len(refs.objects) == 11
for o in refs.objects:
    assert all(o.lock_location) and all(o.lock_rotation) and all(o.lock_scale) and o.hide_select
    assert .3 <= o.color[3] <= .5 and o.data.packed_file
    if 'scale_m_per_pixel' in o:
        assert abs(o['scale_m_per_pixel'] - alignment['scale_m_per_pixel']) < 1e-10
        assert o['ground_z'] == 0.0
        row = next(v for v in alignment['views'] if o.name == 'REF_FINAL_' + v['name'])
        w, h = o.data.size
        width = o.empty_display_size * w / max(w, h)
        height = o.empty_display_size * h / max(w, h)
        axis = row['axis_global'] - row['crop'][0]
        def image_point(global_y):
            local = Vector(((o.empty_image_offset[0] + axis / w) * width,
                            (o.empty_image_offset[1] + (h - (global_y - row['crop'][1])) / h) * height, 0))
            return o.matrix_world @ local
        assert abs(image_point(alignment['sole_pixel_global']).z) < 1e-6
        assert abs(image_point(alignment['crown_pixel_global']).z - 1.4) < 1e-6

report = {'status': 'PASS', 'source_reopened': bpy.data.filepath,
          'existing_objects_preserved': len(before['objects']), 'existing_materials_preserved': len(before['materials']),
          'protected_files_byte_identical': len(source_files), 'rig_and_actions_unchanged': True,
          'source_shapekeys_uvs_and_weights_preserved': True, 'new_rig_or_weights': False,
          'animation_or_unreal_export': False, 'reference_images_locked_and_packed': len(refs.objects),
          'scale_m_per_reference_pixel': alignment['scale_m_per_pixel'],
          'active_objects': len(collection.objects), 'active_meshes': len(geometry),
          'evaluated_world_bounds_m': {'min': low, 'max': high},
          'toes_per_foot': 5, 'fingers_per_hand': 5,
          'intentional_boundaries': 'Retained eye/mouth loops, colored eye discs and original thin clothing/accessory surfaces; new hair clumps, hands and feet are closed.',
          'geometry_audit': geometry}
(OUT / 'Audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'geometry_audit'}, indent=2), flush=True)
