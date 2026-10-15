import bpy,json,time
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1';T=B/'Textures/GameReady_Test_V1';s=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'];bpy.context.window.scene=s;hp=s.objects['GRT_HighPoly_Reference'];source=hp.data.materials[0]
s.cycles.samples=16;s.cycles.use_denoising=False
s.cycles.device=next(i.identifier for i in s.cycles.bl_rna.properties['device'].enum_items if i.identifier=='CPU')
s.render.bake.use_selected_to_active=True;s.render.bake.margin=2;s.render.bake.use_clear=True;s.render.bake.use_cage=True
pr=next(n for n in source.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
proxy=hp.copy();proxy.name='GRT_Transient_BakeSource';s.collection.objects.link(proxy)
channel_sources={}
for channel in ['Roughness','Metallic']:
 mat=source.copy();mat.name='GRT_BakeSource_'+channel;nt=mat.node_tree;cp=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Strength'].default_value=1
 if cp.inputs[channel].is_linked:nt.links.new(cp.inputs[channel].links[0].from_socket,em.inputs['Color'])
 else:em.inputs['Color'].default_value=(*([cp.inputs[channel].default_value]*3),1)
 for link in list(out.inputs['Surface'].links):nt.links.remove(link)
 nt.links.new(em.outputs[0],out.inputs['Surface']);channel_sources[channel]=mat
proxy.material_slots[0].link=next(i.identifier for i in bpy.types.MaterialSlot.bl_rna.properties['link'].enum_items if i.identifier=='OBJECT');proxy.hide_render=True
records={}
for name in ['HeadHair','Torso']:
 o=s.objects['GRT_'+name];mat=bpy.data.materials.new('GRT_Baked_'+name);mat.use_nodes=True;o.data.materials.clear();o.data.materials.append(mat);bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');maps={};o.hide_render=False
 s.render.bake.cage_extrusion=.002 if name=='HeadHair' else .004;s.render.bake.max_ray_distance=.015 if name=='HeadHair' else .025
 for channel,kind in [('BaseColor','DIFFUSE'),('Normal','NORMAL'),('Roughness','EMIT'),('Metallic','EMIT'),('AO','AO')]:
  im=bpy.data.images.new('GRT_'+name+'_'+channel,width=2048,height=2048,alpha=True,float_buffer=False);im.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color';node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.name='Bake_'+channel;node.image=im
  for n in mat.node_tree.nodes:n.select=False
  node.select=True;mat.node_tree.nodes.active=node
  for obj in s.objects:obj.select_set(False)
  o.select_set(True);bpy.context.view_layer.objects.active=o
  if channel in channel_sources:hp.hide_render=True;proxy.hide_render=False;proxy.material_slots[0].material=channel_sources[channel];proxy.select_set(True)
  else:hp.hide_render=False;proxy.hide_render=True;hp.select_set(True)
  other=s.objects['GRT_'+('Torso' if name=='HeadHair' else 'HeadHair')];other.hide_render=True
  t=time.time();print('BAKE_START',name,channel,flush=True)
  typ=next(i.identifier for i in bpy.ops.object.bake.get_rna_type().properties['type'].enum_items if i.identifier==kind)
  kwargs={'type':typ}
  if channel=='BaseColor':kwargs['pass_filter']={next(i.identifier for i in bpy.ops.object.bake.get_rna_type().properties['pass_filter'].enum_items if i.identifier=='COLOR')}
  if channel=='Normal':kwargs['normal_space']=next(i.identifier for i in bpy.ops.object.bake.get_rna_type().properties['normal_space'].enum_items if i.identifier=='TANGENT')
  result=bpy.ops.object.bake(**kwargs)
  im.filepath_raw=str(T/(im.name+'.png'));im.file_format=next(i.identifier for i in bpy.types.Image.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG');im.save();im.pack()
  for pf in im.packed_files:pf.filepath=im.filepath
  maps[channel]={'image':im.name,'path':im.filepath,'size':list(im.size),'colorspace':im.colorspace_settings.name,'status':list(result),'seconds':time.time()-t};print('BAKE_DONE',name,channel,maps[channel]['seconds'],flush=True)
 # Bind the baked maps; AO retained separately, never burned into color.
 nodes={channel:next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.name==data['image']) for channel,data in maps.items()}
 mat.node_tree.links.new(nodes['BaseColor'].outputs['Color'],bs.inputs['Base Color']);mat.node_tree.links.new(nodes['Roughness'].outputs['Color'],bs.inputs['Roughness']);mat.node_tree.links.new(nodes['Metallic'].outputs['Color'],bs.inputs['Metallic']);nm=mat.node_tree.nodes.new('ShaderNodeNormalMap');mat.node_tree.links.new(nodes['Normal'].outputs['Color'],nm.inputs['Color']);mat.node_tree.links.new(nm.outputs['Normal'],bs.inputs['Normal']);bs.inputs['Alpha'].default_value=1;mat.use_backface_culling=False
 records[name]={'maps':maps,'selected_to_active':True,'margin_pixels':2,'cage_extrusion_m':s.render.bake.cage_extrusion,'max_ray_distance_m':s.render.bake.max_ray_distance,'samples':16,'normal_convention':'Tangent-space OpenGL +Y; Unreal import later needs explicit normal convention verification','base_color_pass':'DIFFUSE COLOR only: no direct/indirect studio light','AO':'Separate diagnostic texture, not multiplied into Base Color and not bound to Principled'}
 o.hide_render=True
# Proxy and generated emission materials are transient, do not alter original reference material.
bpy.data.objects.remove(proxy,do_unlink=True)
for mat in channel_sources.values():bpy.data.materials.remove(mat)
hp.hide_render=False;s.cycles.samples=24;s.cycles.use_denoising=True
(P/'BakeTrial.json').write_text(json.dumps(records,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(B/'Source/Hobbit_NPC_GameReady_Test_V1.blend'));print('BAKED_STAGE_SAVED',flush=True)
