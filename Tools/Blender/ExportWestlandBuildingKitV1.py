"""Export independently reusable modules plus matching named UCX box bodies.
Requires a successful saved-source reopen/review; never saves the .blend.
"""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/Architecture/Westland'
assert bpy.app.background and Path(bpy.data.filepath)==ART/'Source/WestlandBuildingKit_V1.blend'
check=json.loads((ROOT/'Saved/WestlandKitV1/BlenderValidation.json').read_text())
assert check['reopened'] and check['manifold'] and (ROOT/'Saved/WestlandKitV1/Blender_Exterior.png').exists()
kit=json.loads((ART/'WestlandBuildingKit_V1.json').read_text())
for col in ('WL_ModuleLibrary','WL_CollisionSources'):bpy.data.collections[col].hide_viewport=False
options=dict(use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,mesh_smooth_type='FACE',use_custom_props=False)
for entry in kit['modules']:
 bpy.ops.object.select_all(action='DESELECT');o=bpy.data.objects[entry['mesh']];o.select_set(True)
 for c in bpy.data.collections['WL_CollisionSources'].objects:
  if c.name.startswith('UCX_'+o.name+'_'):c.select_set(True)
 bpy.context.view_layer.objects.active=o
 path=ART/'Exports/Modules'/(o.name+'.fbx');path.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.export_scene.fbx(filepath=str(path),**options)
print('WESTLAND_EXPORTED',len(kit['modules']),'modules; source not resaved')
