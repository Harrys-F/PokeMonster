"""Export precisely three reviewed siblings. Source and V2 exports remain untouched."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/World/WestlandAssetLibrary';O=R/'Saved/WestlandAssetLibraryV3'
assert Path(bpy.data.filepath).name=='WestlandAssetLibrary_V3.blend' and (O/'ArtReviewAccepted.json').exists()
bpy.context.window.scene=bpy.data.scenes['WestlandAssetLibrary_V3_Source'];data=json.loads((A/'ArtQualityV3.json').read_text());dst=A/'Exports/V3';dst.mkdir(exist_ok=True);rows=[]
for a in data['assets']:
 bpy.ops.object.select_all(action='DESELECT');objs=[bpy.data.objects[n] for n in [a['object']]+a['collision_objects']]
 for o in objs:o.hide_set(False);o.hide_viewport=False;o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0];p=dst/(a['object']+'.fbx')
 bpy.ops.export_scene.fbx(filepath=str(p),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,mesh_smooth_type='FACE',use_tspace=True,use_custom_props=False)
 rows.append({'object':a['object'],'file':str(p.relative_to(R)),'normal_tangent_export':True})
(O/'Exports.json').write_text(json.dumps(rows,indent=2));print('V3_EXPORT_PASS',len(rows))
