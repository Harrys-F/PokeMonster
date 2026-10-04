"""Reopen the saved source, audit geometry, render a local review; never save it."""
import bpy,bmesh,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/HealingHouse';OUT=ROOT/'Saved/HealingArt/Blender';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ART/'Source/HealingHouse_ExpandedArt_V1.blend'))
catalog=json.loads((ART/'ExpandedArtV1/Props.json').read_text());audit=[]
for name,entry in catalog.items():
 o=bpy.data.objects[entry['object']];assert o.type=='MESH' and o.data.polygons and o.data.uv_layers
 assert all(m for m in o.data.materials);assert all(abs(a-b/100)<.0001 for a,b in zip(o.dimensions,entry['size_cm']))
 bm=bmesh.new();bm.from_mesh(o.data);areas=[f.calc_area() for f in bm.faces];bm.free()
 assert min(areas)>1e-11,(name,min(areas))
 audit.append({'name':name,'dimensions_cm':entry['size_cm'],'triangles':entry['triangles'],'materials':entry['materials']})
(OUT/'SourceAudit.json').write_text(json.dumps({'reopened':bpy.data.filepath,'props':audit,'total_triangles':sum(x['triangles'] for x in audit)},indent=2))
bpy.context.window.scene=bpy.data.scenes['Prop Review'];bpy.context.scene.render.filepath=str(OUT/'PropReview.png');bpy.ops.render.render(write_still=True)
from mathutils import Vector
cam=bpy.context.scene.camera;cam.location=(-14,-17,22);cam.rotation_euler=(Vector((8,6,0))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.render.filepath=str(OUT/'PropReviewFront.png');bpy.ops.render.render(write_still=True)
print('SOURCE_REOPEN_AUDIT_PASSED')
