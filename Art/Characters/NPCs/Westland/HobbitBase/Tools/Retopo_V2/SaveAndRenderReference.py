import bpy,json,math
from pathlib import Path
from mathutils import Quaternion,Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/Retopo_V2'
s=bpy.data.scenes['Hobbit_NPC_Retopo_V2'];bpy.context.window.scene=s
for other in list(bpy.data.scenes):
 if other!=s and not other.objects:bpy.data.scenes.remove(other)
assert len(bpy.data.scenes)==1
hp=s.objects['RTV2_HP_REFERENCE_UNMODIFIED'];target=s.objects['RTV2_Head_MANUAL_RETOPO_REQUIRED']
# The file's default screen must open at a usable head close-up, not the default cube.
for w in bpy.data.workspaces:
 w.name='Hobbit Retopo V2' if w==bpy.context.workspace else w.name
for scr in bpy.data.screens:
 for area in scr.areas:
  if area.type=='VIEW_3D':
   space=area.spaces.active;space.region_3d.view_rotation=Quaternion((1,0,0),math.pi/2);space.region_3d.view_perspective='ORTHO';space.region_3d.view_location=(0,0,1.205);space.region_3d.view_distance=.7
   space.clip_start=.001;space.clip_end=100;space.shading.color_type='MATERIAL';space.overlay.show_floor=False;space.overlay.show_axis_x=False;space.overlay.show_axis_y=False;space.overlay.show_face_orientation=False
# Include genuinely useful, runnable read-only target QA inside the blend.
qa=bpy.data.texts.new('RTV2_CHECK_TARGET_READ_ONLY.py')
qa.write("""import bpy,bmesh\no=bpy.context.active_object\nassert o and o.type=='MESH' and o.name.startswith('RTV2_Head'), 'Select retopology target, not source'\nbm=bmesh.new();bm.from_mesh(o.data)\nprint({'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'quads':sum(len(f.verts)==4 for f in bm.faces),'triangles':sum(max(0,len(f.verts)-2) for f in bm.faces),'boundaries':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'loose_vertices':sum(not v.link_edges for v in bm.verts)})\nbm.free()\nprint('An open work-in-progress cage is NOT animation-ready merely because most faces are quads.')\n""")
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
# Render-only overrides: no source geometry or original material edits; do not save below.
clay=bpy.data.materials.new('RTV2_REVIEW_ONLY_Clay');clay.use_nodes=True;bs=next(n for n in clay.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.42,.39,.35,1);bs.inputs['Roughness'].default_value=.78
wire=clay.copy();wire.name='RTV2_REVIEW_ONLY_Wire';bs=next(n for n in wire.node_tree.nodes if n.type=='BSDF_PRINCIPLED');w=wire.node_tree.nodes.new('ShaderNodeWireframe');w.use_pixel_size=True;w.inputs['Size'].default_value=.5;mix=wire.node_tree.nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.55,.5,.44,1);mix.inputs[2].default_value=(.008,.012,.016,1);wire.node_tree.links.new(w.outputs[0],mix.inputs[0]);wire.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
views=[('01_Reference_Front','Front',None),('02_Reference_Right','Right',None),('03_Reference_Left','Left',None),('04_Reference_ThreeQuarter','ThreeQuarter',None),('05_Reference_Clay_Front','Front',clay),('06_Reference_Wire_Front','Front',wire),('07_Reference_2_5D','2_5D_Close',None),('08_Reference_Clay_ThreeQuarter','ThreeQuarter',clay),('09_Reference_Wire_Profile','Right',wire)]
manifest=[]
for name,camera,override in views:
 s.camera=s.objects['RTV2_Camera_'+camera];s.view_layers[0].material_override=override;s.render.filepath=str(P/'Previews'/(name+'.png'))
 assert not Path(s.render.filepath).exists()
 bpy.ops.render.render(write_still=True)
 manifest.append({'path':s.render.filepath,'subject':'Unchanged high-poly reference ONLY; no new low-poly head','camera':camera,'override':'clay' if override==clay else 'wire' if override==wire else 'original material','engine':s.render.engine,'samples':s.cycles.samples,'size':[s.render.resolution_x,s.render.resolution_y]})
 (P/'PreviewManifest.json').write_text(json.dumps(manifest,indent=2));print('RENDER_DONE',name,flush=True)
print('WORKSPACE_SAVE_AND_REFERENCE_RENDERS_COMPLETE',flush=True)
