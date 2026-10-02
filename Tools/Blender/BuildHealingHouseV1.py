"""Run in Blender: creates a separate scene, preserves every existing scene/object.

Metres, common ground-plane origin, applied transforms; FBX contains meshes only.
The user explicitly requested this complete local blockout/export/import prototype.
"""
import bpy
import bmesh
import json
import math
from pathlib import Path
from mathutils import Matrix, Vector, Quaternion

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'Art/HealingHouse'
SOURCE = ART / 'Source/HealingHouse_V1.blend'
EXPORT = ART / 'Exports/HealingHouse_V1.fbx'
if SOURCE.exists() or EXPORT.exists() or bpy.data.scenes.get('HealingHouse_V1'):
    raise RuntimeError('V1 already exists; do not overwrite user work.')
scene = bpy.data.scenes.new('HealingHouse_V1')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
architecture = bpy.data.collections.new('HH_Architecture')
scene.collection.children.link(architecture)
guides = bpy.data.collections.new('HH_ReviewOnly')
scene.collection.children.link(guides)
palette = {
    'Plaster': (0.73, 0.61, 0.43, 1), 'Wood': (0.31, 0.17, 0.075, 1),
    'Timber': (0.13, 0.075, 0.035, 1), 'Stone': (0.39, 0.40, 0.35, 1),
    'Roof': (0.48, 0.13, 0.065, 1), 'Metal': (0.15, 0.16, 0.14, 1),
    'Glass': (0.95, 0.60, 0.19, 1),
}
materials = {}
for name, color in palette.items():
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = color
    shader = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    shader.inputs[0].default_value = color
    shader.inputs[2].default_value = 0.8
    if name == 'Metal': shader.inputs[1].default_value = 0.5
    if name == 'Glass':
        shader.inputs[28].default_value = color
        shader.inputs[29].default_value = 0.15
    materials[name] = mat


def mesh(name, vertices, faces, material, collection=architecture):
    data = bpy.data.meshes.new(name + '_Geometry')
    data.from_pydata(vertices, [], faces)
    data.materials.append(materials[material])
    data.update()
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    return obj


def box(name, center, size, material, collection=architecture):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts:
        v.co = Vector(tuple(center[i] + v.co[i] * size[i] for i in range(3)))
    data = bpy.data.meshes.new(name + '_Geometry')
    bm.to_mesh(data)
    bm.free()
    data.materials.append(materials[material])
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    return obj


def boolean(obj, cutter, operation='DIFFERENCE'):
    mod = obj.modifiers.new('Opening_' + cutter.name, 'BOOLEAN')
    mod.operation = operation
    mod.solver = 'EXACT'
    mod.object = cutter
    bpy.context.view_layer.objects.active = obj
    with bpy.context.temp_override(object=obj, active_object=obj):
        bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def merge(name, objects):
    # Join disconnected solids without introducing duplicate faces or transforms.
    for o in scene.objects: o.select_set(False)
    for o in objects: o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    objects[0].name = name
    return objects[0]


def beam(name, start, end, width=0.15, depth=0.15, material='Timber'):
    direction = Vector(end) - Vector(start)
    obj = box(name, (0, 0, 0), (width, depth, direction.length), material)
    rotation = Vector((0, 0, 1)).rotation_difference(direction.normalized()).to_matrix().to_4x4()
    obj.data.transform(Matrix.Translation((Vector(start) + Vector(end)) / 2) @ rotation)
    return obj


# Original Unreal wall centre lines remain X +/-4.5, Y +/-5; door X=-4.5.
# Floors end at z=0 so the existing continuous gameplay ground has no step.
box('HH_Floor', (0, 0, -0.08), (8.7, 9.7, 0.16), 'Wood')
box('HH_Foundation', (0, 0, -0.22), (9.3, 10.3, 0.28), 'Stone')
front = box('HH_Walls_Front', (-4.5, 0, 1.3), (0.3, 10, 2.6), 'Plaster')
boolean(front, box('DoorCutter', (-4.5, 0, 1.13), (0.9, 2.4, 2.34), 'Plaster'))
openings = [{'id': 'main_door', 'wall': front.name, 'kind': 'door',
             'width_m': 2.4, 'height_m': 2.3, 'threshold_m': 0,
             'destination': 'free central aisle', 'depth_m': 0.3}]
camera_side = box('HH_Walls_CameraSide', (0, 5, 1.3), (8.7, 0.3, 2.6), 'Plaster')
rear = box('RearWallSolid', (4.5, 0, 1.3), (0.3, 10, 2.6), 'Plaster')
far = box('FarWallSolid', (0, -5, 1.3), (8.7, 0.3, 2.6), 'Plaster')
window_parts = {'Front': [], 'CameraSide': [], 'Back': []}
glass_parts = {'Front': [], 'CameraSide': [], 'Back': []}


def window(wall, mark, plane, horizontal, group):
    sill, height, width = 1.15, 1.05, 1.1
    z = sill + height / 2
    if plane == 'X':
        center = (wall.data.vertices[0].co.x, horizontal, z)
        # The first cube vertex is an outer surface; use the declared centre line.
        center = (-4.5 if group == 'Front' else 4.5, horizontal, z)
        cutter_size = (0.9, width, height)
        outer = center[0] + (-0.19 if group == 'Front' else 0.19)
        glass = box(mark + '_Glass', (center[0], horizontal, z), (0.035, width-0.1, height-0.1), 'Glass')
        for y in (horizontal-width/2-0.065, horizontal+width/2+0.065):
            window_parts[group].append(box(mark+'_Post', (outer, y, z), (0.15, 0.13, height+0.26), 'Wood'))
        for zz in (sill-0.06, sill+height+0.06):
            window_parts[group].append(box(mark+'_Cross', (outer, horizontal, zz), (0.15, width, 0.12), 'Wood'))
        window_parts[group].append(box(mark+'_Mullion', (outer, horizontal, z), (0.10, 0.07, height), 'Wood'))
    else:
        y = 5 if group == 'CameraSide' else -5
        center = (horizontal, y, z)
        cutter_size = (width, 0.9, height)
        outer = y + (0.19 if y > 0 else -0.19)
        glass = box(mark+'_Glass', center, (width-0.1, 0.035, height-0.1), 'Glass')
        for x in (horizontal-width/2-0.065, horizontal+width/2+0.065):
            window_parts[group].append(box(mark+'_Post', (x, outer, z), (0.13, 0.15, height+0.26), 'Wood'))
        for zz in (sill-0.06, sill+height+0.06):
            window_parts[group].append(box(mark+'_Cross', (horizontal, outer, zz), (width, 0.15, 0.12), 'Wood'))
        window_parts[group].append(box(mark+'_Mullion', (horizontal, outer, z), (0.07, 0.10, height), 'Wood'))
    boolean(wall, box(mark+'_Cutter', center, cutter_size, 'Plaster'))
    glass_parts[group].append(glass)
    openings.append({'id': mark, 'wall': wall.name, 'kind': 'window', 'width_m': width,
                     'height_m': height, 'sill_m': sill, 'depth_m': 0.3})


for y in (-3.1, 3.1): window(front, 'FrontWindow'+str(y), 'X', y, 'Front')
for x in (-2.3, 2.3):
    window(camera_side, 'CameraWindow'+str(x), 'Y', x, 'CameraSide')
    window(far, 'FarWindow'+str(x), 'Y', x, 'Back')
merge('HH_Walls', [rear, far])
for group in window_parts:
    merge('HH_WindowFrames' + ('' if group == 'Back' else '_'+group), window_parts[group])
    merge('HH_Glass_'+group, glass_parts[group])

# Closed triangular gables, individually removable on the camera-facing end.
def gable(name, x):
    verts = [(xx, y, z) for xx in (x-0.12, x+0.12) for y,z in ((-5,2.6),(5,2.6),(0.6,6.3))]
    return mesh(name, verts, [(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)], 'Plaster')
gable('HH_Gable_Front', -4.5)
gable('HH_Gable_Rear', 4.5)

# Asymmetrical, sealed roof slabs; no individually modelled shingles in V1.
def roof_slab(name, x0, x1, y0, z0, y1, z1):
    verts = [(x,y,z+dz) for dz in (-0.13,0) for x,y,z in
             ((x0,y0,z0),(x1,y0,z0),(x1,y1,z1),(x0,y1,z1))]
    return mesh(name, verts, [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)], 'Roof')
merge('HH_Roof_Main', [roof_slab('RoofLeft', -4.95,4.95,-5.55,2.68,0.6,6.4),
                           roof_slab('RoofRight', -4.95,4.95,0.6,6.4,5.55,2.68)])
# Small side canopy is open to the exterior, with real support posts and no closed false door.
roof_slab('HH_Roof_Porch', -3.45,0.1,-6.35,2.05,-4.95,2.68)
porch_parts = [box('PorchPost', (x,-6.16,1.01), (0.18,0.18,2.02), 'Timber') for x in (-3.25,-0.1)]
porch_parts.append(beam('PorchFrontBeam', (-3.4,-6.16,1.97),(0.02,-6.16,1.97),0.17,0.17))
merge('HH_Timber_Porch', porch_parts)
box('HH_PorchFloor', (-1.675,-5.8,-0.08),(3.55,1.7,0.16),'Stone')

timber = {'Front': [], 'CameraSide': [], 'Back': []}
for x, group in ((-4.7,'Front'),(4.7,'Back')):
    for y in (-4.85,-1.4,1.4,4.85):
        timber[group].append(box('Post', (x,y,1.3),(0.18,0.18,2.6),'Timber'))
    timber[group].append(beam('Eaves', (x,-5.1,2.57),(x,5.1,2.57),0.19,0.19))
    timber[group].append(beam('GableEdge', (x,-5,2.65),(x,0.6,6.3),0.19,0.19))
    timber[group].append(beam('GableEdge', (x,0.6,6.3),(x,5,2.65),0.19,0.19))
    timber[group].append(beam('GableKingPost', (x,0.6,2.6),(x,0.6,6.2),0.18,0.18))
for y, group in ((5.2,'CameraSide'),(-5.2,'Back')):
    for x in (-4.25,0,4.25): timber[group].append(box('SidePost',(x,y,1.3),(0.18,0.18,2.6),'Timber'))
    timber[group].append(beam('SideEaves',(-4.4,y,2.57),(4.4,y,2.57),0.19,0.19))
for group, parts in timber.items(): merge('HH_Timber' + ('' if group=='Back' else '_'+group), parts)
merge('HH_DoorFrame', [box('DoorJamb',(-4.7,y,1.15),(0.18,0.18,2.3),'Stone') for y in (-1.3,1.3)]
      + [box('DoorHead',(-4.7,0,2.42),(0.18,2.8,0.24),'Stone')])
merge('HH_Chimney', [box('ChimneyShaft',(2.8,-1.45,4.55),(0.85,0.9,4.7),'Stone'),
                     box('ChimneyCrown',(2.8,-1.45,6.86),(1.03,1.08,0.18),'Stone')])
box('HH_ChimneyCap', (2.8,-1.45,6.98),(0.91,0.96,0.08),'Metal')
# Counter follows the original functional counter footprint and healer location.
merge('HH_Counter', [box('CounterBase',(2.2,-0.8,0.42),(0.8,3.4,0.84),'Wood'),
                     box('CounterTop',(2.2,-0.8,0.88),(0.94,3.5,0.08),'Stone')])
box('HH_ScaleReference_140cm',(-6.4,1,0.7),(0.45,0.3,1.4),'Wood',guides)

# Recalculate all mesh normals and independently audit closed solids/transforms.
report = {'source': str(SOURCE.relative_to(ROOT)), 'export': str(EXPORT.relative_to(ROOT)),
          'units': 'metres; Unreal import 100 centimetres per metre', 'openings': openings,
          'material_slots': list(palette), 'modules': [], 'review_only': ['HH_ScaleReference_140cm'],
          'walkable_floor_z_m': 0, 'reserved_creature_beds_m': [[-1.7,-3.45],[0.2,-3.45]],
          'central_aisle_m': [[-6,0],[-3.3,0.45],[0.6,0],[1.45,-0.8]],
          'reference': 'Art/HealingHouse/Review/Concept_HealingHouse.png'}
all_points = []
for obj in architecture.objects:
    # Unreal is left-handed. Author Blender Y mirrored so FBX conversion restores
    # the original Unreal wall coordinates and camera-side module identities.
    for vertex in obj.data.vertices: vertex.co.y *= -1
    bm = bmesh.new(); bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    nonmanifold = sum(not e.is_manifold for e in bm.edges)
    zero_area = sum(f.calc_area() < 1e-8 for f in bm.faces)
    volume = bm.calc_volume(signed=True)
    bm.free()
    obj.data.calc_loop_triangles()
    points = [obj.matrix_world @ v.co for v in obj.data.vertices]
    all_points += points
    mins = [min(v[i] for v in points) for i in range(3)]
    maxs = [max(v[i] for v in points) for i in range(3)]
    report['modules'].append({'name': obj.name, 'triangles': len(obj.data.loop_triangles),
        'vertices': len(obj.data.vertices), 'nonmanifold_edges': nonmanifold,
        'zero_area_faces': zero_area, 'volume_m3': volume, 'bounds_min_m': mins, 'bounds_max_m': maxs,
        'unreal_bounds_min_m': [mins[0],-maxs[1],mins[2]],
        'unreal_bounds_max_m': [maxs[0],-mins[1],maxs[2]]})
    if nonmanifold or zero_area or volume <= 0: raise RuntimeError('Geometry audit failed: '+obj.name)
    assert tuple(obj.scale)==(1,1,1) and tuple(obj.rotation_euler)==(0,0,0)
report['bounds_min_m'] = [min(v[i] for v in all_points) for i in range(3)]
report['bounds_max_m'] = [max(v[i] for v in all_points) for i in range(3)]
report['total_triangles'] = sum(m['triangles'] for m in report['modules'])
report['coordinate_mapping'] = 'Unreal X=Blender X; Unreal Y=-Blender Y; Unreal Z=Blender Z'
assert report['total_triangles'] < 5000
for directory in (SOURCE.parent, EXPORT.parent, ART/'Review'): directory.mkdir(parents=True,exist_ok=True)
(ART/'Review/GeometryAudit.json').write_text(json.dumps(report,indent=2)+'\n')
# Only the authored scene and dependencies enter the source file; user's original scene survives untouched.
bpy.data.libraries.write(str(SOURCE), {scene}, fake_user=True, compress=True)
for obj in scene.objects: obj.select_set(obj in architecture.objects[:])
bpy.context.view_layer.objects.active = architecture.objects[0]
bpy.ops.export_scene.fbx(filepath=str(EXPORT), use_selection=True, object_types={'MESH'},
    global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_UNITS',
    axis_forward='X', axis_up='Z', use_mesh_modifiers=True, bake_anim=False,
    use_triangles=True, mesh_smooth_type='FACE', use_custom_props=False)
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        space = area.spaces.active
        space.shading.color_type = 'MATERIAL'
        space.overlay.show_overlays = False
        space.region_3d.view_location = Vector((0,-0.3,2.4))
        space.region_3d.view_distance = 21
        space.region_3d.view_rotation = Vector((-1,1,1)).to_track_quat('Z','Y')
print(json.dumps({'source':str(SOURCE),'export':str(EXPORT),'triangles':report['total_triangles'],
                  'modules':[m['name'] for m in report['modules']]}))
