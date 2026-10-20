"""Read-only material appearance and usage fingerprint, usable in the live editor or NullRHI commandlet."""
import unreal,json,re,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();m=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_MossStone');assert isinstance(m,unreal.MaterialInterface);root=m
while isinstance(root,unreal.MaterialInstanceConstant):root=root.parent
def properties(o):
 keys=set(dir(o))|{'r','g','b','a','constant','code','output_type','parameter_name','default_value','texture','sampler_type','shading_model','two_sided','blend_mode','opacity_mask_clip_value','used_with_instanced_static_meshes','used_with_skeletal_mesh','use_material_attributes','dithered_lod_transition','parent','scalar_parameter_values','vector_parameter_values','texture_parameter_values','base_property_overrides','has_static_permutation_resource'};d={}
 for k in sorted(keys):
  if k.startswith('_'):continue
  try:v=o.get_editor_property(k)
  except Exception:continue
  if isinstance(v,unreal.Object):v=v.get_path_name()
  elif not isinstance(v,(str,int,float,bool,type(None))):v=re.sub(r'0x[0-9a-fA-F]+','PTR',v.export_text() if hasattr(v,'export_text') else str(v))
  d[k]=v
 return d
appearance={};usage={}
for k,v in properties(m).items():
 if k.startswith('used_with_'):usage[k]=v
 elif k not in ['state_id','lighting_guid','preview_mesh']:appearance[k]=v
nodes=[]
for n in unreal.MaterialEditingLibrary.get_material_expressions(root):nodes.append({'name':n.get_name(),'class':n.get_class().get_name(),'properties':properties(n),'input_nodes':[a.get_path_name() if a else None for a in unreal.MaterialEditingLibrary.get_inputs_for_material_expression(root,n)]})
j={'appearance':appearance,'nodes':nodes,'usage':usage,'root_properties':properties(root),'file_sha256':__import__('hashlib').sha256((R/'Content/Environment/WestlandAssetLibrary/Materials/MI_WLA_MossStone.uasset').read_bytes()).hexdigest()};label='Disk' if __import__('os').environ.get('PM_MATERIAL_DISK_READ')=='1' else 'Live';(R/'Saved/ArtPassV4'/('Stone'+label+'.json')).write_text(json.dumps(j,indent=2));unreal.log('STONE_FINGERPRINT '+label)
