"""Export only the reopened/reviewed new library, never existing V3 sources."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/HealingHouse';REVIEW=ROOT/'Saved/HealingArt/Blender'
assert (REVIEW/'SourceAudit.json').is_file() and (REVIEW/'PropReview.png').is_file(), 'Reopen and visually review source first'
bpy.ops.wm.open_mainfile(filepath=str(ART/'Source/HealingHouse_ExpandedArt_V1.blend'));bpy.context.window.scene=bpy.data.scenes['HealingHouse_ExpandedArt_V1']
OUT=ART/'Exports/ExpandedArtV1';OUT.mkdir(parents=True,exist_ok=True)
for name,entry in json.loads((ART/'ExpandedArtV1/Props.json').read_text()).items():
 bpy.ops.object.select_all(action='DESELECT');o=bpy.data.objects[entry['object']];o.hide_set(False);o.hide_render=False;o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(OUT/('SM_HH_Art_'+name+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,mesh_smooth_type='FACE',use_custom_props=False)
print('EXPORT_COMPLETE')
