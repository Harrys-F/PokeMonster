"""Adjust the existing V2 mesh data; never scale the whole building actor.

Run in background Blender with the current V2 source loaded. Preserve its
materials, window forms, component origins, depth, heights and counter.
Export is deliberately separate and follows the review of the saved source.
"""
import bpy
import bmesh
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'Art/HealingHouse'
SOURCE = ART / 'Source/HealingHouse_V2.blend'
REVIEW = ART / 'Review/V2/Proportions'
assert bpy.app.background and Path(bpy.data.filepath) == SOURCE
scene = bpy.data.scenes['HealingHouse_V2']
if scene.get('proportions_pass'):
    raise RuntimeError('Already adjusted; do not apply twice.')
bpy.context.window.scene = scene
architecture = bpy.data.collections['HH_V2_Architecture']
assert len(architecture.objects) == 39
baseline_audit = json.loads((ART/'Review/V2/GeometryAudit.json').read_text())
baseline_topology = {m['name']:m['non_manifold_edges'] for m in baseline_audit['modules']}
REVIEW.mkdir(parents=True, exist_ok=True)
preserved = ART / 'Source/HealingHouse_V2_PreProportions.blend'
if preserved.exists():
    assert hashlib.sha256(preserved.read_bytes()).digest() == hashlib.sha256(SOURCE.read_bytes()).digest(), 'Pre-pass source differs; inspect before applying.'
else:
    shutil.copy2(SOURCE, preserved)
shutil.copy2(ART/'Review/V2/GeometryAudit.json', REVIEW/'BeforeGeometryAudit.json')
for filename in ('PIE_V2_Forecourt_2500.png', 'PIE_V2_AtCounter_2500.png'):
    shutil.copy2(ART/'Review/V2'/filename, REVIEW/('Before_'+filename))

def facade_y(y):
    # Windows retain their width in the middle strip; only the free doorway
    # and outer infill strips contract. Outside extensions move with the wall.
    sign = 1 if y >= 0 else -1
    a = abs(y)
    if a <= 1.2: out = a * .85 / 1.2
    elif a <= 3.85: out = a - .35
    elif a <= 5: out = 3.5 + (a-3.85) * .85/1.15
    else: out = a - .65
    return sign * out

def islands(data):
    parent = list(range(len(data.vertices)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for edge in data.edges:
        a,b = edge.vertices
        parent[find(a)] = find(b)
    result = {}
    for vertex in data.vertices:
        result.setdefault(find(vertex.index), []).append(vertex)
    return result.values()

roof_ratio = 9/10.3
loft_shift = .6 * (roof_ratio-1)
changed = []
for obj in architecture.objects:
    name = obj.name.removeprefix('HH_V2_')
    before = [tuple(v.co) for v in obj.data.vertices]
    # Work in authoring Unreal metres, undoing the one FBX handedness mirror.
    for vertex in obj.data.vertices: vertex.co.y *= -1
    vertices = obj.data.vertices
    if name == 'Foundation':
        for v in vertices: v.co.y *= 9/10.3
    elif name == 'Floor':
        for v in vertices: v.co.y *= 8.4/9.7
    elif name in ('Walls_Front', 'Walls_Rear', 'Stone_Front', 'Stone_Rear'):
        for v in vertices:
            old_y = v.co.y
            v.co.y = facade_y(old_y)
            if name == 'Walls_Front' and abs(abs(old_y)-1.2)<.001 and abs(v.co.z-2.3)<.001:
                v.co.z = 2.15
    elif name in ('Walls_CameraSide','Glass_CameraSide','Windows_CameraSide',
                  'Timber_CameraSide','Stone_CameraSide','InteriorBeams_CameraSide'):
        for v in vertices: v.co.y -= .65
    elif name in ('Walls_Far','Glass_Far','Windows_Far','Timber_Far','Stone_Far'):
        for v in vertices: v.co.y += .65
    elif name in ('Roof_Main','Roof_Trim','Gable_Front','Gable_Rear'):
        for v in vertices:
            old_y = v.co.y
            radius = ((old_y-.6)**2+(v.co.z-4.45)**2)**.5
            v.co.y = old_y * roof_ratio
            if name == 'Gable_Front' and abs(radius-.47)<.002:
                v.co.y = old_y + loft_shift
    elif name in ('Glass_Loft','Windows_Loft'):
        for v in vertices: v.co.y += loft_shift
    elif name in ('Glass_Front','Windows_Front'):
        for part in islands(obj.data):
            centre = (min(v.co.y for v in part)+max(v.co.y for v in part))/2
            delta = -.35 if centre > 0 else .35
            for v in part: v.co.y += delta
    elif name in ('Timber_Front','Timber_Rear'):
        for part in islands(obj.data):
            lo,hi = min(v.co.y for v in part),max(v.co.y for v in part)
            if min(v.co.z for v in part) >= 2.6:
                for v in part: v.co.y *= roof_ratio
            elif hi-lo < .5:
                delta = facade_y((lo+hi)/2)-(lo+hi)/2
                for v in part: v.co.y += delta
            else:
                for v in part: v.co.y = facade_y(v.co.y)
    elif name in ('Roof_Porch','Timber_Porch','PorchFloor'):
        for v in vertices: v.co.y += .65
    elif name in ('Roof_Entry','Timber_Entry'):
        for v in vertices:
            v.co.y *= 2.4/3.1
            v.co.z -= .15
    elif name == 'DoorFrame':
        for part in islands(obj.data):
            lo,hi = min(v.co.y for v in part),max(v.co.y for v in part)
            if hi-lo < .5:
                delta = -.35 if (lo+hi)>0 else .35
                for v in part: v.co.y += delta
            else:
                for v in part: v.co.y *= (hi-lo-.7)/(hi-lo)
            for v in part: v.co.z *= 2.15/2.3
    elif name == 'DoorLeaf':
        for v in vertices:
            v.co.x = -4.56 + (v.co.x+4.56)*1.7/2.4
            v.co.y += .35
            v.co.z *= 2.15/2.3
    elif name == 'InteriorBeams':
        for part in islands(obj.data):
            lo,hi = min(v.co.y for v in part),max(v.co.y for v in part)
            if hi-lo > 8:
                for v in part: v.co.y *= 8.2/9.5
            else:
                for v in part: v.co.y += .65
    elif name == 'InteriorStone':
        for v in vertices: v.co.y *= 8.15/9.45
    elif name not in ('Counter','Chimney','ChimneyCap'):
        raise RuntimeError('Unhandled module: '+name)
    for v in vertices: v.co.y *= -1
    obj.data.update()
    if before != [tuple(v.co) for v in vertices]: changed.append(obj.name)

modules = []
for obj in architecture.objects:
    bm = bmesh.new(); bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    nonmanifold = sum(not edge.is_manifold for edge in bm.edges)
    volume = bm.calc_volume(signed=True)
    # The existing bevelled interior beam has eight boundary edges. This pass
    # preserves mesh connectivity and must not introduce additional openings.
    assert nonmanifold == baseline_topology[obj.name] and volume > 0, (obj.name, nonmanifold, volume)
    bm.to_mesh(obj.data); bm.free(); obj.data.update()
    obj.data.calc_loop_triangles()
    coords = [v.co for v in obj.data.vertices]
    mins = [min(v[i] for v in coords) for i in range(3)]
    maxs = [max(v[i] for v in coords) for i in range(3)]
    modules.append({'name':obj.name,'triangles':len(obj.data.loop_triangles),
        'non_manifold_edges':nonmanifold,'volume_m3':volume,
        'unreal_bounds_min_m':[mins[0],-maxs[1],mins[2]],
        'unreal_bounds_max_m':[maxs[0],-mins[1],maxs[2]],
        'materials':[m.name for m in obj.data.materials]})
audit = json.loads((ART/'Review/V2/GeometryAudit.json').read_text())
audit['modules'] = modules
audit['functional_dimensions_m']['main'] = [9.3,9.0]
audit['functional_dimensions_m']['door'] = [1.7,2.15]
for opening in audit['openings']:
    if opening['id']=='main_door':
        opening['width_m']=1.7; opening['height_m']=2.15
audit['proportion_changed_modules'] = changed
audit['total_triangles'] = sum(m['triangles'] for m in modules)
scene['proportions_pass'] = 'Door 1.70 x 2.15 m; main width 9.00 m; no global actor scale'
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
(ART/'Review/V2/GeometryAudit.json').write_text(json.dumps(audit,indent=2)+'\n')
(REVIEW/'GeometryChanges.json').write_text(json.dumps({
    'source':str(SOURCE),'preserved_source':str(preserved),'changed_modules':changed,
    'old_door_m':[2.4,2.3],'new_door_m':[1.7,2.15],
    'old_width_m':10.3,'new_width_m':9.0,'counter_changed':False,
    'height_and_depth_unchanged':True,'global_actor_scale_used':False},indent=2)+'\n')
print('PROPORTIONS_SAVED '+json.dumps({'changed':len(changed),'triangles':audit['total_triangles']}))
