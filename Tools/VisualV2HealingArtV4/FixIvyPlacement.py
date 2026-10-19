"""Move private thin ivy leaves to the original protruding face and orient them outward."""
from pathlib import Path
import bpy,json,shutil
R=Path(__file__).resolve().parents[2];A=R/'Art/World/VisualV2HealingArtV4';S=R/'Saved/VisualV2HealingArtV4';p=A/'Source/HealingHouse_GardenDetails_V4.blend';assert bpy.app.background;backup=S/'GardenDetails_BeforeIvyPlacement.blend';assert not backup.exists();shutil.copy2(p,backup);bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;rows=[]
for key in ['IvySprigA','IvySprigB']:
 o=bpy.data.objects['HA4_'+key];m=o.data
 for v in m.vertices:v.co.x-=.50
 for f in m.polygons:
  if f.normal.x>0:f.flip()
 m.update();location=o.location.copy();o.location=(0,0,0);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_HA4_'+key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False,path_mode='COPY',embed_textures=False);o.location=location;rows.append({'mesh':key,'local_x_shift_m':-.50,'world_x_shift_cm_under_existing_scale':-3.5,'outward_faces':sum(f.normal.x<0 for f in m.polygons),'faces':len(m.polygons)})
bpy.ops.wm.save_as_mainfile(filepath=str(p));(S/'IvyPlacementFix.json').write_text(json.dumps(rows,indent=2));print(rows)
