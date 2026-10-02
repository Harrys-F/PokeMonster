"""Export the saved proportion pass after architectural visual review."""
import bpy
import json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT/'Art/HealingHouse'
assert bpy.app.background
assert Path(bpy.data.filepath) == ART/'Source/HealingHouse_V2.blend'
scene = bpy.data.scenes['HealingHouse_V2']
assert scene.get('proportions_pass')
bpy.context.window.scene = scene
architecture = bpy.data.collections['HH_V2_Architecture']
wall = bpy.data.objects['HH_V2_Walls_Front']
tree = BVHTree.FromPolygons([v.co for v in wall.data.vertices],
                           [tuple(p.vertices) for p in wall.data.polygons])
for y in (-.84,0,.84):
    for z in (.02,1.4,2.14):
        assert tree.ray_cast(Vector((-5.5,-y,z)),Vector((1,0,0)),2)[0] is None, (y,z)
for y,z in ((-.86,1.4),(.86,1.4),(0,2.16)):
    assert tree.ray_cast(Vector((-5.5,-y,z)),Vector((1,0,0)),2)[0] is not None, (y,z)
options = dict(use_selection=True,object_types={'MESH'},global_scale=1,
    apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',
    axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,
    mesh_smooth_type='FACE',use_custom_props=False)
for obj in scene.objects: obj.select_set(obj.name in architecture.objects)
bpy.context.view_layer.objects.active = architecture.objects[0]
bpy.ops.export_scene.fbx(filepath=str(ART/'Exports/HealingHouse_V2.fbx'),**options)
audit = json.loads((ART/'Review/V2/GeometryAudit.json').read_text())
temp = ART/'Exports/V2Modules';temp.mkdir(exist_ok=True)
for name in audit['proportion_changed_modules']:
    for obj in scene.objects: obj.select_set(obj.name==name)
    bpy.context.view_layer.objects.active = bpy.data.objects[name]
    bpy.ops.export_scene.fbx(filepath=str(temp/('SM_'+name+'.fbx')),**options)
print('PROPORTION_EXPORT_SUCCESS '+str(len(audit['proportion_changed_modules']))+'; door BVH 170 x 215 cm passed')
