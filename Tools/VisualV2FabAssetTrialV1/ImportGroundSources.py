"""Import only already downloaded licensed ground maps into local-only Fab folder."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';V=Path('/Users/Shared/UnrealEngine/Launcher/VaultCache/FabLibrary');rows=[]
for folder in ['Forest_Floor-dae56d09','Forest_Path-6614ed94','Grass_And_Rubble-f0eff48c']:
 for src in (V/folder).rglob('*.png'):
  if not any(src.stem.endswith('_'+s)for s in ['B','N','ORM']):continue
  dest='/Game/Fab/VisualV2TrialLocal/Ground/'+src.stem;assert not unreal.EditorAssetLibrary.does_asset_exist(dest)
  t=unreal.AssetImportTask();t.filename=str(src);t.destination_path=dest.rsplit('/',1)[0];t.destination_name=src.stem;t.automated=True;t.save=False;t.replace_existing=False;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);a=unreal.load_asset(dest);assert a
  if src.stem.endswith('_ORM'):a.set_editor_property('srgb',False);a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
  assert unreal.EditorAssetLibrary.save_loaded_asset(a,False);rows.append(dict(source=str(src),asset=a.get_path_name(),size=[a.blueprint_get_size_x(),a.blueprint_get_size_y()]))
(D/'ImportedLocalSources.json').write_text(json.dumps(rows,indent=2))
