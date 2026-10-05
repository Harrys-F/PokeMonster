"""Reopen and audit saved V3 source. Export requires explicit --export-reviewed.
Run without that flag first; inspect SourceReview.png before exporting.
"""
import bpy,bmesh,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'Art/HealingHouse';OUT=ROOT/'Saved/HealingQualityV3/Blender';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(A/'Source/HealingHouse_QualityV3.blend'));catalog=json.loads((A/'QualityV3/Props.json').read_text());audit=[]
for name,p in catalog.items():
 o=bpy.data.objects[p['object']];assert o.data.polygons and o.data.uv_layers and all(o.data.materials)
 bm=bmesh.new();bm.from_mesh(o.data);assert min(f.calc_area() for f in bm.faces)>1e-11;bm.free()
 assert all(abs(a-b/100)<1e-4 for a,b in zip(o.dimensions,p['size_cm']));audit.append({'name':name,'triangles':p['triangles'],'size_cm':p['size_cm']})
if '--export-reviewed' not in sys.argv:
 bpy.context.window.scene=bpy.data.scenes['Quality V3 Review'];bpy.context.scene.render.filepath=str(OUT/'SourceReview.png');bpy.ops.render.render(write_still=True)
 (OUT/'SourceAudit.json').write_text(json.dumps({'reopened':bpy.data.filepath,'props':audit},indent=2))
else:
 assert (OUT/'SourceReview.png').exists() and (OUT/'SourceAudit.json').exists()
 bpy.context.window.scene=bpy.data.scenes['HealingHouse_QualityV3']
 for name,p in catalog.items():
  bpy.ops.object.select_all(action='DESELECT');o=bpy.data.objects[p['object']];o.hide_set(False);o.hide_render=False;o.select_set(True);bpy.context.view_layer.objects.active=o
  folder=A/'Exports/QualityV3';folder.mkdir(parents=True,exist_ok=True)
  prefix='SM_HH_Q3_'
  bpy.ops.export_scene.fbx(filepath=str(folder/(prefix+name+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,mesh_smooth_type='FACE',use_custom_props=False)
print('QUALITY_V3_SOURCE_REOPEN_AND_REVIEW_PASSED',len(audit))
