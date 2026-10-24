"""Read-only actual graph/API inventory for private, scoped dense canopy materials."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();L=unreal.MaterialEditingLibrary;rows={}
for path in ['/Game/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal','/Game/Environment/DevTestMapVisualV2/Materials/M_V2_BarkRevealBase','/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Stone']:
 m=unreal.load_asset(path);assert m
 source=L.get_material_property_input_node(m,unreal.MaterialProperty.MP_OPACITY_MASK)
 rows[path]={'blend_mode':str(m.blend_mode),'opacity_input':source.get_path_name()if source else None,'opacity_output':str(L.get_material_property_input_node_output_name(m,unreal.MaterialProperty.MP_OPACITY_MASK))if source else None,'nodes':[{'name':n.get_name(),'class':n.get_class().get_name()}for n in L.get_material_expressions(m)if isinstance(n,unreal.MaterialExpression)]}
rows['shadow_replace_available']=hasattr(unreal,'MaterialExpressionShadowReplace')
(R/'Saved/BiomeTestV11/ForestMaterialAPI.json').write_text(json.dumps(rows,indent=2))
