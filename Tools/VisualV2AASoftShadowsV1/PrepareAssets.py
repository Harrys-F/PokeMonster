"""Create only new experimental decal assets. Never saves any map or existing material."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2AASoftShadowsV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world()
assert not e.get_game_world() and w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
root='/Game/Development/VisualV2AASoftShadowsV1';tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
assert not unreal.EditorAssetLibrary.does_directory_exist(root),'Never replace an earlier experiment'
unreal.EditorAssetLibrary.make_directory(root)
m=tools.create_asset('M_SoftGroundBlob',root,unreal.Material,unreal.MaterialFactoryNew())
m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT);m.set_editor_property('material_domain',unreal.MaterialDomain.MD_DEFERRED_DECAL)
uv=lib.create_material_expression(m,unreal.MaterialExpressionTextureCoordinate,-700,0)
custom=lib.create_material_expression(m,unreal.MaterialExpressionCustom,-400,0);custom.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT1);input_uv=unreal.CustomInput();input_uv.set_editor_property('input_name','UV');custom.set_editor_property('inputs',[input_uv])
custom.set_editor_property('code','float2 p=(UV-0.5)*2; float a=atan2(p.y,p.x); float edge=0.93+0.035*sin(a*3+0.4)+0.025*sin(a*5); float f=saturate((edge-length(p))/0.62); return f*f*(3-2*f);')
lib.connect_material_expressions(uv,'',custom,'UV')
density=lib.create_material_expression(m,unreal.MaterialExpressionScalarParameter,-400,200);density.set_editor_property('parameter_name','Density');density.set_editor_property('default_value',.18)
mul=lib.create_material_expression(m,unreal.MaterialExpressionMultiply,-100,0);lib.connect_material_expressions(custom,'',mul,'A');lib.connect_material_expressions(density,'',mul,'B');lib.connect_material_property(mul,'',unreal.MaterialProperty.MP_OPACITY)
black=lib.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-100,-200);black.set_editor_property('constant',unreal.LinearColor(0,0,0,1));lib.connect_material_property(black,'',unreal.MaterialProperty.MP_BASE_COLOR)
lib.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m)
for name,value in [('MI_TreeBlob',.45),('MI_FigureBlob',.5)]:
 mi=tools.create_asset(name,root,unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());lib.set_material_instance_parent(mi,m);lib.set_material_instance_scalar_parameter_value(mi,'Density',value);lib.update_material_instance(mi);assert unreal.EditorAssetLibrary.save_loaded_asset(mi)
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=scene(w)
(O/'TestScene.json').write_text(json.dumps(before,indent=2))
(O/'AssetsCreated.json').write_text(json.dumps({'assets':list(unreal.EditorAssetLibrary.list_assets(root)),'new_map_created':False,'central_comparison':'RunMapChecks.py, separate editor processes'},indent=2))
