"""Read-only connected graph proof. No material editor or shader mutation."""
import unreal,json,re

def graph(material):
 roots={};nodes={};todo=[]
 for key in ['MP_BASE_COLOR','MP_ROUGHNESS','MP_SPECULAR','MP_METALLIC','MP_OPACITY_MASK','MP_NORMAL','MP_WORLD_POSITION_OFFSET']:
  prop=getattr(unreal.MaterialProperty,key);n=unreal.MaterialEditingLibrary.get_material_property_input_node(material,prop);roots[key]=n.get_name() if n else None
  if n:todo.append(n)
 while todo:
  n=todo.pop();name=n.get_name()
  if name in nodes:continue
  d={'class':n.get_class().get_name(),'properties':{}}
  for key in ['parameter_name','default_value','texture','r','constant','const_a','const_b','const_exponent','const_coordinate','coordinate_index','u_tiling','v_tiling']:
   try:
    v=n.get_editor_property(key);d['properties'][key]=v.get_path_name() if isinstance(v,unreal.Object) else re.sub(r'0x[0-9a-fA-F]+','<address>',str(v))
   except Exception:pass
  inputs=unreal.MaterialEditingLibrary.get_inputs_for_material_expression(material,n);d['inputs']=[x.get_name() if x else None for x in inputs];todo.extend(x for x in inputs if x);nodes[name]=d
 return {'roots':roots,'connected_nodes':nodes}
