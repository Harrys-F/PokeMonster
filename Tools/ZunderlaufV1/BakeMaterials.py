"""Bake only material information, never lights or ambient occlusion into base colour."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Zunderlauf';bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Zunderlauf_V1.blend'));bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8;s.render.bake.margin=16;s.render.bake.use_pass_direct=False;s.render.bake.use_pass_indirect=False;s.render.bake.use_pass_color=True
body=bpy.data.objects['Zunderlauf'];bpy.data.objects['Zunderlauf_Rig'].data.pose_position='REST';bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
T=A/'Textures';T.mkdir(exist_ok=True);images={}
for typ,color in [('DIFFUSE',True),('NORMAL',False),('ROUGHNESS',False)]:
 image=bpy.data.images.new('Zunderlauf_'+typ,width=2048,height=2048,alpha=False);image.colorspace_settings.name='sRGB' if color else 'Non-Color';image.filepath_raw=str(T/(image.name+'.png'));image.file_format='PNG'
 for m in body.data.materials:
  nodes=m.node_tree.nodes
  for n in nodes:n.select=False
  n=nodes.new('ShaderNodeTexImage');n.image=image;n.select=True;nodes.active=n
 bpy.ops.object.bake(type=typ);image.save();image.pack();images[typ]=image
for m in body.data.materials:
 p=m.node_tree.nodes.get('Principled BSDF');ns=m.node_tree.nodes;links=m.node_tree.links
 for key,socket in [('DIFFUSE','Base Color'),('ROUGHNESS','Roughness')]:
  n=next(n for n in ns if n.type=='TEX_IMAGE' and n.image==images[key]);links.new(n.outputs['Color'],p.inputs[socket])
 n=next(n for n in ns if n.type=='TEX_IMAGE' and n.image==images['NORMAL']);normal=ns.new('ShaderNodeNormalMap');links.new(n.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs[0],p.inputs['Normal'])
bpy.data.objects['Zunderlauf_Rig'].data.pose_position='POSE';bpy.ops.wm.save_as_mainfile(filepath=str(A/'Source/Zunderlauf_V1.blend'));(A/'BakeAudit.json').write_text(json.dumps({'resolution':[2048,2048],'passes':list(images),'direct_light':False,'indirect_light':False,'normal_convention':'OpenGL tangent; Unreal flip green','margin_px':16,'packed':True},indent=2));print('BAKE_PASS')
