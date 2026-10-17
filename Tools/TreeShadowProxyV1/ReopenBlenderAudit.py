import bpy,bmesh,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/World/TreeShadowProxyV1';assert bpy.app.background;assert Path(bpy.data.filepath)==A/'Source/OakAncient_ShadowProxy_V1.blend'
records=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);non=sum(not e.is_manifold for e in bm.edges);bm.free();assert non==0
 o.data.calc_loop_triangles();records.append({'object':o.name,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'non_manifold_edges':non,'dimensions_m':list(o.dimensions)})
assert len(records)==2
(A/'Review/BlenderReopen.json').write_text(json.dumps({'success':True,'saved_source_reopened':bpy.data.filepath,'scene':bpy.context.scene.name,'objects':records,'modified_on_reopen':False},indent=2));print('BLENDER_REOPEN_PASS',records)
