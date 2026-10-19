"""Read-only source reopen and geometry/UV diagnostics, background Blender only."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtV5';p=R/'Art/World/VisualV2WorldArtV5/Source/Westland_ThreeBiomes_Details_V5.blend';assert bpy.app.background;bpy.ops.wm.open_mainfile(filepath=str(p));rows=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();uv=m.uv_layers.active;assert uv and m.color_attributes.get('Col');bad_uv=0
 for t in m.loop_triangles:
  a,b,c=[uv.data[i].uv for i in t.loops]
  if abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))<1e-12:bad_uv+=1
 row={'object':o.name,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'zero_area_faces':sum(f.area<1e-12 for f in m.polygons),'zero_normal_faces':sum(f.normal.length<.99 for f in m.polygons),'nonfinite_vertices':sum(not all(math.isfinite(x) for x in v.co) for v in m.vertices),'degenerate_uv_triangles':bad_uv,'uv_layers':len(m.uv_layers),'material_slots':len(m.materials),'single_sided_leaf_surfaces_intentional':True}
 assert not any(row[k] for k in ['zero_area_faces','zero_normal_faces','nonfinite_vertices','degenerate_uv_triangles']),row;rows.append(row)
assert len(rows)==3;images=[{'name':i.name,'packed':bool(i.packed_file),'size':list(i.size)} for i in bpy.data.images if i.source=='FILE'];assert all(x['packed'] for x in images)
(S/'BlenderDetailsAudit.json').write_text(json.dumps({'source':str(p),'opened_successfully':True,'meshes':rows,'images':images,'saved_or_modified':False},indent=2));print('BLENDER READONLY AUDIT PASS',flush=True)
