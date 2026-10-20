"""Repair UVs on the new cloth thickness rim; preserve its top design, silhouette and original sources."""
import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];p=R/'Art/HealingHouse/Source/HealingHouse_ArtV4.blend';bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['WovenRug'];m=o.data;uv=m.uv_layers.active
for f in m.polygons:
 if abs(f.normal.z)>.8:continue
 for li in f.loop_indices:
  v=m.vertices[m.loops[li].vertex_index].co
  uv.data[li].uv=((v.x/2.25+.5) if abs(f.normal.y)>abs(f.normal.x) else (v.y/1.6+.5),v.z/.002)
m.calc_loop_triangles();bad=[]
for t in m.loop_triangles:
 a,b,c=[uv.data[i].uv for i in t.loops];area=abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))*.5
 if area<1e-10:bad.append(t.index)
assert not bad,bad[:20]
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;pos=o.location.copy();o.location=(0,0,0);bpy.ops.export_scene.fbx(filepath=str(R/'Art/HealingHouse/Exports/SM_HH4_WovenRug.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False);o.location=pos;bpy.ops.wm.save_as_mainfile(filepath=str(p));(R/'Art/HealingHouse/ArtV4_RugUV.json').write_text(json.dumps({'cause':'Solidify copied coincident UVs to the thin cloth rim; Mikk tangent/binormal warning on these faces','repair':'Dedicated height-vs-length UV strips on rim; top/bottom motif UVs preserved','zero_uv_area_triangles':len(bad),'triangles':len(m.loop_triangles),'geometry_and_thickness_unchanged':True},indent=2));print('RUG_UV_RIM_FIXED')
