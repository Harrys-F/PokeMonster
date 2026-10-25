"""Rebuild Blender-side original Meshy bindings omitted by static FBX material serialization."""
import bpy,json
from pathlib import Path
def apply(id,obj,C):
 R=Path('/Users/harry/Developer/PokeMonster');bindings=R/'Art/Characters/NPCs/IntegrationV1'/(id+'_MaterialBindings.json')
 if id=='HobbitBase':files={'Base Color':C/'Textures/MeshyBaseV2/T_Hobbit_MeshyBase_V2_BaseColor.png','Normal':C/'Textures/MeshyBaseV2/T_Hobbit_MeshyBase_V2_Normal.png','Roughness':C/'Textures/MeshyBaseV2/T_Hobbit_MeshyBase_V2_ORM.png'}
 else:files={k:C/'Textures'/Path(v).name for k,v in json.loads(bindings.read_text()).items() if k in ['Base Color','Normal','Roughness']}
 assert all(p.is_file() for p in files.values());mat=bpy.data.materials.new(id+'_OriginalMeshyBindings');mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF');links=mat.node_tree.links
 for role,path in files.items():
  im=bpy.data.images.load(str(path),check_existing=False);im.colorspace_settings.name='sRGB' if role=='Base Color' else 'Non-Color';im.pack();tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im
  if role=='Base Color':links.new(tex.outputs['Color'],p.inputs['Base Color'])
  elif role=='Normal':
   n=mat.node_tree.nodes.new('ShaderNodeNormalMap');links.new(tex.outputs['Color'],n.inputs['Color']);links.new(n.outputs['Normal'],p.inputs['Normal'])
  else:
   n=mat.node_tree.nodes.new('ShaderNodeSeparateColor');links.new(tex.outputs['Color'],n.inputs[0]);links.new(n.outputs[1],p.inputs['Roughness']);links.new(n.outputs[2],p.inputs['Metallic'])
 obj.data.materials.clear();obj.data.materials.append(mat)
