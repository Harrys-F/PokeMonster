import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';V=Path('/Users/Shared/UnrealEngine/Launcher/VaultCache/FabLibrary');AT=unreal.AssetToolsHelpers.get_asset_tools();rows=[]
for folder,prefix in [('Uncut_Grass-1b93f569','Grass'),('Mossy_Forest_Floor-31b154e8','Forest'),('Cracked_Wooden_Planks-95c7a8b6','Timber')]:
 for src in(V/folder).rglob('*'):
  if not src.is_file():continue
  end=src.stem.rsplit('_',1)[-1];kind={'B':'BaseColor','N':'Normal','ORM':'ORM'}.get(end,end)
  if kind not in['BaseColor','Normal','ORM','Roughness']:continue
  name='T_WR4_'+prefix+'_'+kind;path='/Game/Fab/VisualV2RefinementLocal/Textures/'+name
  if unreal.EditorAssetLibrary.does_asset_exist(path):continue
  task=unreal.AssetImportTask();task.filename=str(src);task.destination_path=path.rsplit('/',1)[0];task.destination_name=name;task.automated=True;task.save=False;task.replace_existing=False;AT.import_asset_tasks([task]);a=unreal.load_asset(path);assert a
  if kind in['ORM','Roughness']:a.set_editor_property('srgb',False);a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
  if kind=='Normal':a.set_editor_property('srgb',False);a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP)
  assert unreal.EditorAssetLibrary.save_loaded_asset(a,False);rows.append(dict(source=str(src),asset=a.get_path_name(),kind=kind))
(D/'ImportedSurfaces.json').write_text(json.dumps(rows,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
