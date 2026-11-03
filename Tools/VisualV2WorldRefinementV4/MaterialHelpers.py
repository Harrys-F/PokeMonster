import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Common.py')))
def node(m,cls):return ML.create_material_expression(m,cls)
def new(name):
 p=ROOT+'/Materials/M_WR4_'+name;m=unreal.load_asset(p)if unreal.EditorAssetLibrary.does_asset_exist(p)else AT.create_asset('M_WR4_'+name,ROOT+'/Materials',unreal.Material,unreal.MaterialFactoryNew());ML.delete_all_material_expressions(m);return m
def custom(m,code,inputs,typ=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 n=node(m,unreal.MaterialExpressionCustom);n.set_editor_property('code',code);n.set_editor_property('output_type',typ);vals=[]
 for k in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',k);vals.append(i)
 n.set_editor_property('inputs',vals)
 for k,(v,pin)in inputs.items():assert ML.connect_material_expressions(v,pin,n,k)
 return n
def sample(m,path,uv,normal=False):
 n=node(m,unreal.MaterialExpressionTextureSample);n.texture=unreal.load_asset(path);assert n.texture,path
 if normal:n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
 elif n.texture.get_editor_property('compression_settings')==unreal.TextureCompressionSettings.TC_MASKS:n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
 assert ML.connect_material_expressions(uv,'',n,'UVs');return n
def scalar(m,v,prop):n=node(m,unreal.MaterialExpressionConstant);n.r=v;assert ML.connect_material_property(n,'',prop)
def finish(m):
 m.set_editor_property('used_with_instanced_static_meshes',True);errors=ML.recompile_material(m);assert not errors,(m.get_name(),[str(x)for x in errors]);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
