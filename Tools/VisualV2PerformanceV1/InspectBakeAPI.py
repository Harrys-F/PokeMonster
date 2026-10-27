import unreal,json
from pathlib import Path
D=Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2PerformanceV1';L=unreal.MaterialEditingLibrary
r={'render_functions':{n:getattr(unreal.RenderingLibrary,n).__doc__ for n in ['create_render_target2d','draw_material_to_render_target','export_render_target']},'material_functions':{n:getattr(L,n).__doc__ for n in ['get_material_property_input_node','connect_material_property','get_inputs_for_material_expression','disconnect_material_property']if hasattr(L,n)},'texture_format':str(unreal.TextureRenderTargetFormat.RTF_RGBA8)}
(D/'BakeAPI.json').write_text(json.dumps(r,indent=2))
