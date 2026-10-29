"""Read every creature blend without saving it, and record actual rigs/actions/topology."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/ModelsV4';rows=[]
for p in sorted((R/'Art/Characters/Creatures').rglob('*.blend')):
 try:
  bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);meshes=[]
  for o in bpy.data.objects:
   if o.type!='MESH':continue
   o.data.calc_loop_triangles();meshes.append({'name':o.name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'materials':len(o.data.materials),'uv_layers':len(o.data.uv_layers),'vertex_groups':len(o.vertex_groups),'dimensions':list(o.dimensions),'hidden':o.hide_render})
  rows.append({'path':str(p.relative_to(R)),'meshes':meshes,'rigs':[{'name':o.name,'bones':len(o.data.bones)}for o in bpy.data.objects if o.type=='ARMATURE'],'actions':[a.name for a in bpy.data.actions],'images':[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file)}for im in bpy.data.images if im.type=='IMAGE'],'unit_scale':bpy.context.scene.unit_settings.scale_length})
 except Exception as e:rows.append({'path':str(p.relative_to(R)),'error':str(e)})
 (D/'BlendInventory.json').write_text(json.dumps(rows,indent=2));print('READ_ONLY_BLEND',p.name,flush=True)
