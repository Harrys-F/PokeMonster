"""Only export reviewed source. Reopen audits recorded separately, metres->cm via FBX."""
import bpy,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/World/WestlandAssetLibrary';OUT=ROOT/'Saved/WestlandAssetLibrary';hero='HeroReview' in bpy.data.filepath
assert bpy.app.background and Path(bpy.data.filepath).exists();assert (OUT/('HeroReviewAccepted.json' if hero else 'FamilyReviewAccepted.json')).exists()
data=json.loads((ART/('Heroes.json' if hero else 'Assets.json')).read_text());audit=[]
for a in data['assets']:
 collection=bpy.data.collections[a['id']];
 if collection.name not in bpy.context.scene.collection.children:bpy.context.scene.collection.children.link(collection)
 collection.hide_viewport=False;collection.hide_render=False
 # Owned source cells only; review instances excluded from export.
 objects=[bpy.data.objects[n] for n in [a['object']]+a['collision_objects']]
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.hide_set(False);o.hide_viewport=False;o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 p=ART/'Exports'/(a['object']+'.fbx')
 if p.exists():
  old=OUT/'PreCleanupExports'/p.name;old.parent.mkdir(exist_ok=True)
  if not old.exists():shutil.copy2(p,old)
 bpy.ops.export_scene.fbx(filepath=str(p),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,mesh_smooth_type='FACE',use_custom_props=False)
 audit.append({'id':a['id'],'fbx':str(p),'collision_bodies':len(a['collision_objects'])})
(OUT/('HeroExports.json' if hero else 'Exports.json')).write_text(json.dumps({'source_reopened':True,'exports':audit},indent=2)+'\n');print('WLA_REOPEN_EXPORT_PASSED',len(audit))
