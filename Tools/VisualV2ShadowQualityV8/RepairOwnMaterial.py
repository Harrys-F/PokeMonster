import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir());m=unreal.load_asset('/Game/Environment/VisualV2ShadowQualityV8/Materials/M_SV8_ShadowLift_Experimental');L=unreal.MaterialEditingLibrary;nodes=L.get_material_expressions(m);n=next(n for n in nodes if isinstance(n,unreal.MaterialExpressionCustom));n.set_editor_property('code',(R/'Art/World/VisualV2ShadowQualityV8/ShadowLift.hlsl').read_text())
for v in nodes:
 if isinstance(v,unreal.MaterialExpressionVectorParameter):assert L.connect_material_expressions(v,'RGBA',n,str(v.get_editor_property('parameter_name')))
L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
