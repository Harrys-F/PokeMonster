"""Owned road material only: world-space coverage preserves seams at intersections.
May be applied while PIE is idle. No map, collision or shared material change.
"""
import unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();base='/Game/Environment/WestlandRegion';path=base+'/Textures/T_WR_PathCoverage';tex=unreal.load_asset(path)
if not tex:
 task=unreal.AssetImportTask();task.filename=str(R/'Art/World/WestlandRegion/Textures/T_WR_PathCoverage.png');task.destination_path=base+'/Textures';task.automated=True;task.save=True;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);tex=unreal.load_asset(path)
assert tex;tex.set_editor_property('srgb',False);tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS);tex.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS);tex.set_editor_property('address_x',unreal.TextureAddress.TA_CLAMP);tex.set_editor_property('address_y',unreal.TextureAddress.TA_CLAMP);unreal.EditorAssetLibrary.save_loaded_asset(tex,False)
m=unreal.load_asset(base+'/Materials/M_WR_PathBlend');lib=unreal.MaterialEditingLibrary;c=next(x for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom) if x.get_outer()==m);code=c.get_editor_property('code')
if 'RoadTex' not in code:
 inputs=list(c.get_editor_property('inputs'));item=unreal.CustomInput();item.set_editor_property('input_name','RoadTex');inputs.append(item);c.set_editor_property('inputs',inputs)
 code=code.replace('float alpha=1-smoothstep(.65,.99,edge);','float2 mapUV=float2((p.x+p.y)*.007071067812+500,400-(p.x-p.y)*.007071067812)/float2(1000,800);\nfloat alpha=Texture2DSample(RoadTex,RoadTexSampler,mapUV).r;')
 code=code.replace('alpha*ends','alpha');c.set_editor_property('code',code);obj=lib.create_material_expression(m,unreal.MaterialExpressionTextureObjectParameter);obj.set_editor_property('parameter_name','RegionalPathCoverage');obj.set_editor_property('texture',tex);lib.connect_material_expressions(obj,'',c,'RoadTex');lib.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,False)
assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);unreal.log('REGION_PATH_COVERAGE_DONE')
