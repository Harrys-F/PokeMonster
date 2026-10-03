"""Export explicitly saved/reviewed V3 modules without cameras or review props."""
import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/HealingHouse'
assert bpy.app.background and Path(bpy.data.filepath)==ART/'Source/HealingHouse_V3.blend'
scene=bpy.data.scenes['HealingHouse_V3'];bpy.context.window.scene=scene
review=ART/'Review/V3/Front';audit=json.loads((review/'GeometryAudit.json').read_text())
assert (review/'Blender_Exterior.png').exists()
wall=bpy.data.objects['HH_V2_Walls_Front'];tree=BVHTree.FromPolygons([v.co for v in wall.data.vertices],[list(p.vertices) for p in wall.data.polygons])
for y in (-.74,0,.74):
 for z in (.02,1.4,2.14):assert tree.ray_cast(Vector((-5.5,y,z)),Vector((1,0,0)),2)[0] is None,(y,z)
for y,z in ((-.76,1.4),(.76,1.4),(0,2.16)):
 assert tree.ray_cast(Vector((-5.5,y,z)),Vector((1,0,0)),2)[0] is not None,(y,z)
glass=bpy.data.objects['HH_V2_Glass_Loft'];ys=[v.co.y for v in glass.data.vertices]
assert abs((min(ys)+max(ys))/2)<.001
foundation=bpy.data.objects['HH_V2_Foundation'];ys=[v.co.y for v in foundation.data.vertices];xs=[v.co.x for v in foundation.data.vertices]
assert abs(max(ys)-min(ys)-9)<.001 and abs(max(xs)-min(xs)-9.3)<.001
options=dict(use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,mesh_smooth_type='FACE',use_custom_props=False)
folder=ART/'Exports/V3Modules';folder.mkdir(parents=True,exist_ok=True)
architecture=bpy.data.collections['HH_V2_Architecture']
for o in scene.objects:o.select_set(o.name in architecture.objects)
bpy.context.view_layer.objects.active=architecture.objects[0]
bpy.ops.export_scene.fbx(filepath=str(ART/'Exports/HealingHouse_V3.fbx'),**options)
for name in audit['changed_front_modules']:
 for o in scene.objects:o.select_set(o.name==name)
 bpy.context.view_layer.objects.active=bpy.data.objects[name]
 bpy.ops.export_scene.fbx(filepath=str(folder/('SM_'+name+'.fbx')),**options)
props=bpy.data.collections.get('HH_V3_Props')
if props:
 for obj in props.objects:
  placement=obj.matrix_world.copy()
  from mathutils import Matrix
  obj.matrix_world=Matrix.Identity(4)
  for o in scene.objects:o.select_set(o==obj)
  bpy.context.view_layer.objects.active=obj
  bpy.ops.export_scene.fbx(filepath=str(folder/('SM_'+obj.name+'.fbx')),**options)
  obj.matrix_world=placement
print('V3_EXPORT_OK door150x215 axis0; front modules',len(audit['changed_front_modules']))
