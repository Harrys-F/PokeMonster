import bpy
from mathutils import Vector
from pathlib import Path
s=bpy.data.scenes['Hobbit_NPC_V4_HeadSculpt'];bpy.context.window.scene=s
for other in list(bpy.data.scenes):
 if other!=s and not other.objects:bpy.data.scenes.remove(other)
body=next(o for o in s.objects if o.name.startswith('HNV4_Body'))
for o in s.objects:o.select_set(False)
body.hide_set(False);body.select_set(True);bpy.context.view_layer.objects.active=body;body.active_shape_key_index=1
modes=[i.identifier for i in bpy.ops.object.mode_set.get_rna_type().properties['mode'].enum_items]
if body.mode!='SCULPT':bpy.ops.object.mode_set(mode=next(i for i in modes if i=='SCULPT'))
sc=s.tool_settings.sculpt;sc.use_symmetry_x=True;sc.use_symmetry_y=False;sc.use_symmetry_z=False
bpy.context.window.workspace.name='Hobbit V4 Head Sculpt'
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  sp=area.spaces.active;rv=sp.region_3d;rv.view_location=(0,0,1.16);rv.view_distance=.42;rv.view_rotation=Vector((0,1,0)).to_track_quat('-Z','Y')
  rv.view_perspective=next(i.identifier for i in bpy.types.RegionView3D.bl_rna.properties['view_perspective'].enum_items if i.identifier=='ORTHO')
  sp.overlay.show_floor=False;sp.overlay.show_extras=False;sp.overlay.show_relationship_lines=False
  sp.shading.type=next(i.identifier for i in bpy.types.View3DShading.bl_rna.properties['type'].enum_items if i.identifier=='SOLID')
  with bpy.context.temp_override(area=area,region=next(r for r in area.regions if r.type=='WINDOW')):
   axis=next(i.identifier for i in bpy.ops.view3d.view_axis.get_rna_type().properties['type'].enum_items if i.identifier=='FRONT');bpy.ops.view3d.view_axis(type=axis,align_active=False);rv.view_location=(0,0,1.16);rv.view_distance=.42
   enum=next(i.identifier for i in bpy.ops.brush.asset_activate.get_rna_type().properties['asset_library_type'].enum_items if i.identifier=='ESSENTIALS')
   bpy.ops.brush.asset_activate(asset_library_type=enum,relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Grab')
if sc.brush:
 sc.brush.size=65;sc.brush.strength=.20;sc.brush.use_frontface=True
# Include the manual instructions in the .blend itself as well as a sidecar Markdown.
p=Path(bpy.data.filepath).parents[2]/'Review/V4/MANUELLER_SCULPT_WORKFLOW.md'
if p.exists():
 t=bpy.data.texts.get('V4_Manual_Sculpt_Readme') or bpy.data.texts.new('V4_Manual_Sculpt_Readme');t.clear();t.write(p.read_text())
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('Final V4 workspace saved; mode',body.mode,'brush',sc.brush.name if sc.brush else None,'height unchanged')
