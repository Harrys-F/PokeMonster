"""Creates an unbound diagnostic asset only. Does not edit the map or its materials."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2ShadowQualityV8';A=R/'Art/World/VisualV2ShadowQualityV8';D='/Game/Environment/VisualV2ShadowQualityV8/Materials';L=unreal.MaterialEditingLibrary
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not unreal.EditorAssetLibrary.does_asset_exist(D+'/M_SV8_ShadowLift_Experimental')
m=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_SV8_ShadowLift_Experimental',D,unreal.Material,unreal.MaterialFactoryNew());assert m
m.set_editor_property('material_domain',unreal.MaterialDomain.MD_POST_PROCESS);m.set_editor_property('blendable_location',unreal.BlendableLocation.BL_SCENE_COLOR_AFTER_TONEMAPPING)
n=L.create_material_expression(m,unreal.MaterialExpressionCustom,800,0);n.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3);n.set_editor_property('code',(A/'ShadowLift.hlsl').read_text())
inputs=[]
for key in ['Color','Diffuse','Normal','Position','AO','Gain','Low','High','Debug']+['Contact'+str(i) for i in range(16)]:
 inp=unreal.CustomInput();inp.set_editor_property('input_name',key);inputs.append(inp)
n.set_editor_property('inputs',inputs)
for key,kind in [('Color',unreal.SceneTextureId.PPI_POST_PROCESS_INPUT0),('Diffuse',unreal.SceneTextureId.PPI_DIFFUSE_COLOR),('Normal',unreal.SceneTextureId.PPI_WORLD_NORMAL),('AO',unreal.SceneTextureId.PPI_AMBIENT_OCCLUSION)]:
 node=L.create_material_expression(m,unreal.MaterialExpressionSceneTexture,-600,0);node.set_editor_property('scene_texture_id',kind);assert L.connect_material_expressions(node,'Color' if key!='AO' else 'Color',n,key)
node=L.create_material_expression(m,unreal.MaterialExpressionWorldPosition,-600,200);assert L.connect_material_expressions(node,'',n,'Position')
for key,v in [('Gain',0),('Low',.18),('High',.58),('Debug',0)]:
 node=L.create_material_expression(m,unreal.MaterialExpressionScalarParameter,-600,400);node.set_editor_property('parameter_name',key);node.set_editor_property('default_value',v);assert L.connect_material_expressions(node,'',n,key)
for i in range(16):
 node=L.create_material_expression(m,unreal.MaterialExpressionVectorParameter,-600,600);node.set_editor_property('parameter_name','Contact'+str(i));node.set_editor_property('default_value',unreal.LinearColor(100000,100000,0,1));assert L.connect_material_expressions(node,'RGBA',n,'Contact'+str(i))
assert L.connect_material_property(n,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR);assert all(L.get_inputs_for_material_expression(m,n));L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(S/'Prepared.json').write_text(json.dumps({'asset':m.get_path_name(),'map_modified':False,'method':'Post-tonemap albedo/normal/AO floor classification; approximate, no direct VSM shadow-mask access','automatic_adoption':False},indent=2));unreal.log('SV8_EXPERIMENTAL_ASSET_READY')
