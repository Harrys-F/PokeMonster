"""Export only the twenty reopened and visually reviewed V2 revisions to existing FBX paths."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/World/WestlandAssetLibrary';O=R/'Saved/WestlandAssetLibraryV2'
assert Path(bpy.data.filepath).name=='WestlandAssetLibrary_V2.blend' and (O/'ArtReviewAccepted.json').exists()
bpy.context.window.scene=bpy.data.scenes['WestlandAssetLibrary_Source'];data=json.loads((A/'Assets.json').read_text());rows=[]
for a in data['assets']:
 if a.get('art_status')!='V2_review_pending':continue
 bpy.ops.object.select_all(action='DESELECT');objects=[bpy.data.objects[n] for n in [a['object']]+a['collision_objects']]
 for o in objects:o.hide_set(False);o.hide_viewport=False;o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];p=A/'Exports'/(a['object']+'.fbx')
 bpy.ops.export_scene.fbx(filepath=str(p),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,mesh_smooth_type='FACE',use_tspace=True,use_custom_props=False)
 rows.append({'id':a['id'],'path':str(p.relative_to(R)),'export_normals_and_tangents':True})
assert len(rows)==20;(O/'Exports.json').write_text(json.dumps(rows,indent=2));print('V2_EXPORT_PASS',len(rows))
