"""Read-only final graph/instance verification. Does not mistake transient construction warnings for final shader validity."""
from pathlib import Path
import unreal,json
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV6';A=R/'Art/World/VisualV2WorldArtV6';L=unreal.MaterialEditingLibrary;manifest=json.loads((A/'AssetManifest.json').read_text());rows=[]
for entry in manifest['materials']:
 m=unreal.load_asset(entry['new']);assert m and m.get_path_name().startswith('/Game/Environment/VisualV2WorldArtV6/');nodes=L.get_material_expressions(m);color=next(n for n in nodes if isinstance(n,unreal.MaterialExpressionCustom) and n.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3);assert color.get_editor_property('code')==entry['color_after'];connected=L.get_inputs_for_material_expression(m,color);assert connected and all(connected)
 args=[str(i.get_editor_property('input_name')) for i in color.get_editor_property('inputs')];assert len(args)==len(set(args)) and args.count('W6Earth')==1
 texture=next(n for n in nodes if isinstance(n,unreal.MaterialExpressionTextureObjectParameter) and str(n.get_editor_property('parameter_name'))=='W6Earth');assert texture.get_editor_property('texture').get_path_name()=='/Game/Environment/VisualV2HealingArtV4/Textures/T_HA4_Earth.T_HA4_Earth'
 for alpha in entry['opacity']:
  node=next(n for n in nodes if n.get_name()==alpha['node']);assert node.get_editor_property('code')==alpha['after'];assert all(L.get_inputs_for_material_expression(m,node))
 rows.append({'path':m.get_path_name(),'all_custom_inputs_connected':True,'earth_source':texture.get_editor_property('texture').get_path_name(),'opacity_nodes_modified':len(entry['opacity']),'source_graph_matches_manifest':True})
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(S/'MaterialVerification.json').write_text(json.dumps({'materials':rows,'is_runtime_shader_validation':False,'runtime_validation':'Actual final fresh PIE/native captures and fresh engine logs are required separately.'},indent=2));unreal.log('WA6_MATERIAL_GRAPH_VERIFICATION_PASS')
