"""Replace the proven periodic V4 normal only in the two private V7 lime graphs."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';ROOT='/Game/Environment/VisualV2InteriorV7';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not(D/'PlasterPolished.json').exists();ML=unreal.MaterialEditingLibrary
path=ROOT+'/Textures/T_V7_PlasterGrainNormal'
if unreal.EditorAssetLibrary.does_asset_exist(path):tex=unreal.load_asset(path)
else:
 t=unreal.AssetImportTask();t.filename=str(R/'Art/World/VisualV2InteriorV7/Generated/PlasterGrainNormal.png');t.destination_path=ROOT+'/Textures';t.destination_name='T_V7_PlasterGrainNormal';t.automated=True;t.replace_existing=False;t.save=False;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);tex=unreal.load_asset(path)
assert tex;tex.set_editor_property('srgb',False);tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);assert unreal.EditorAssetLibrary.save_loaded_asset(tex,False)

for name in ['LimePlaster','SageLimewash']:
 m=unreal.load_asset(ROOT+'/Materials/M_V7_'+name);changed=0
 for n in ML.get_material_expressions(m):
  if isinstance(n,unreal.MaterialExpressionTextureSample)and n.texture and (n.texture.get_path_name().startswith('/Game/Environment/VisualV2WorldRefinementV4/Textures/T_WR4_PlasterMicroNormal')or n.texture.get_path_name().startswith(path+'.')):n.texture=tex;changed+=1
  if isinstance(n,unreal.MaterialExpressionCustom):
   c=n.get_editor_property('code')
   if '/48;'in c:n.set_editor_property('code',c.replace('/48;','/84;'))
 assert changed>=1;errors=ML.recompile_material(m);assert not errors,[str(x)for x in errors];assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
(D/'PlasterPolished.json').write_text(json.dumps(dict(reason='Periodic source micro-normal produced a visible regular pattern in actual QHD images',replacement=path,source=str(R/'Art/World/VisualV2InteriorV7/Generated/PlasterGrainNormal.png'),repeat_cm=84,originals_unchanged=True),indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
