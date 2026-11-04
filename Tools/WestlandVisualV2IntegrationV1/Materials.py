"""Derive only the regional ground graph. All approved PBR sources stay byte-identical."""
import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';ROOT='/Game/Environment/WestlandVisualV2IntegrationV1';ML=unreal.MaterialEditingLibrary;E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_WestlandRegion';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not(D/'Materials.json').exists()
p=ROOT+'/Materials/M_WI_RegionalGround';assert not unreal.EditorAssetLibrary.does_asset_exist(p);m=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/VisualV2WorldRefinementV4/Materials/M_WR4_Ground',p);assert m
ML.delete_unused_expressions(m);nodes=ML.get_material_expressions(m);mask=next(n for n in nodes if isinstance(n,unreal.MaterialExpressionTextureSample)and n.texture and n.texture.get_name()=='T_WR4_GroundWeights');mask.texture=unreal.load_asset('/Game/Environment/WestlandRegion/Textures/T_WR_PathCoverage');assert mask.texture and not mask.texture.srgb
uv=next(n for n in nodes if isinstance(n,unreal.MaterialExpressionCustom)and'return (P.xy-float2(-6000,-3250))'in n.get_editor_property('code'));uv.set_editor_property('code','return float2((P.x+P.y)*.007071067812+500,400-(P.x-P.y)*.007071067812)/float2(1000,800);')
world=next(n for n in nodes if isinstance(n,unreal.MaterialExpressionWorldPosition));blend=ML.create_material_expression(m,unreal.MaterialExpressionCustom);blend.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT4);inputs=[]
for key in ['P','Road']:
 i=unreal.CustomInput();i.set_editor_property('input_name',key);inputs.append(i)
blend.set_editor_property('inputs',inputs);blend.set_editor_property('code','''float2 en=float2(P.x+P.y,P.x-P.y)*.007071067812;
float eastWood=exp(-(pow(abs((en.x-252)/100),4)+pow(abs((en.y-170)/126),4)));
float westWood=.75*exp(-(pow(abs((en.x+365)/38),4)+pow(abs((en.y-95)/160),4)));
float river=25+35*sin((en.y+70)/150)+200*max(0,(-en.y-80)/220);
float wet=(1-smoothstep(3.4,8.2,abs(en.x-river)))*.7;
float macro=saturate(.5+.22*sin(en.x*.07+sin(en.y*.043))+.16*cos(en.y*.11+en.x*.031));
return float4(Road.r,max(eastWood,westWood)*.88,wet,macro);''');assert ML.connect_material_expressions(world,'',blend,'P');assert ML.connect_material_expressions(mask,'RGBA',blend,'Road')
reconnected=0
for n in nodes:
 if isinstance(n,unreal.MaterialExpressionCustom)and any(str(i.get_editor_property('input_name'))=='M'for i in n.get_editor_property('inputs')):
  assert ML.connect_material_expressions(blend,'',n,'M');reconnected+=1
for n in ML.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom)and 'float pond=1-smoothstep'in n.get_editor_property('code'):
  code,count=re.subn(r'float pond=1-smoothstep.*?c=lerp\(c,soil\*float3\(.55,.50,.43\),submerged\*\.9\);','',n.get_editor_property('code'));assert count==1;n.set_editor_property('code',code)
assert reconnected==3,reconnected;assert not ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
# Own instances prevent an instancing usage edit to the licensed material/parent.
for name,src in [('FieldShrubs','/Game/Environment/VisualV2WorldOverhaulV3/Materials/MI_WOV_Shrubs'),('FabFlowers','/Game/Environment/VisualV2FabAssetTrialV1/Materials/MI_FAT_Flowers')]:
 dst=ROOT+'/Materials/MI_WI_'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(dst);mi=unreal.EditorAssetLibrary.duplicate_asset(src,dst);ML.set_material_usage_override(mi,unreal.MaterialUsage.MATUSAGE_INSTANCED_STATIC_MESHES,True,True);ML.update_material_instance(mi);assert unreal.EditorAssetLibrary.save_loaded_asset(mi,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
# Preserve the original buildings' CPD0 temporal cutaway instead of replacing it with opaque walls.
for name,src in [('Timber','/Game/Environment/VisualV2WorldRefinementV4/Materials/M_WR4_Timber'),('Plaster','/Game/Environment/VisualV2InteriorV7/Materials/M_V7_LimePlaster'),('Stone','/Game/Environment/VisualV2WorldRefinementV4/Materials/M_WR4_Stone'),('Roof','/Game/Environment/VisualV2WorldRefinementV4/Materials/M_WR4_Roof')]:
 dst=ROOT+'/Materials/M_WI_Fade'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(dst);material=unreal.EditorAssetLibrary.duplicate_asset(src,dst);ML.delete_unused_expressions(material);material.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED)
 fade=ML.create_material_expression(material,unreal.MaterialExpressionScalarParameter);fade.set_editor_property('parameter_name','HouseCutaway');fade.set_editor_property('default_value',0);fade.set_editor_property('use_custom_primitive_data',True);fade.set_editor_property('primitive_data_index',0)
 inv=ML.create_material_expression(material,unreal.MaterialExpressionOneMinus);assert ML.connect_material_expressions(fade,'',inv,str(ML.get_material_expression_input_names(inv)[0]));d=ML.create_material_expression(material,unreal.MaterialExpressionMaterialFunctionCall);d.set_material_function(unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA'));assert ML.connect_material_expressions(inv,'',d,'Alpha Threshold');assert ML.connect_material_property(d,'',unreal.MaterialProperty.MP_OPACITY_MASK);assert not ML.recompile_material(material);assert unreal.EditorAssetLibrary.save_loaded_asset(material,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()

assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(D/'Materials.json').write_text(json.dumps(dict(ground=p,regional_path_mask=mask.texture.get_path_name(),source_graph_unchanged=True,ground_geometry_unchanged=True,material_inputs='Actual regional road coverage plus existing woodland/shore coordinates; original local PBR textures'),indent=2))
