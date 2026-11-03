"""Original GLB read only; isolated derived static inspection assets, never playable replacements."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';root='/Game/Characters/Creatures/ModelIntakeV6/Aquana';assert not unreal.EditorAssetLibrary.does_directory_exist(root)
t=unreal.AssetImportTask();t.filename=str(R/'Art/Characters/Creatures/Incoming/Aquana.glb');t.destination_path=root;t.destination_name='SM_Aquana_Import';t.automated=True;t.replace_existing=False;t.save=False
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);assets=t.get_objects();rows=[]
for a in assets:
 row=dict(path=a.get_path_name(),kind=a.get_class().get_name())
 if isinstance(a,unreal.StaticMesh):row.update(bounds=str(a.get_bounds()),materials=[a.get_material(i).get_path_name()if a.get_material(i)else None for i in range(a.get_num_sections(0))],lods=a.get_num_lods())
 rows.append(row)
(D/'ImportOne.json').write_text(json.dumps(dict(objects=rows,paths=list(t.imported_object_paths)),indent=2));print(rows)
assert any(isinstance(a,unreal.StaticMesh)for a in assets)
for a in assets:
 if isinstance(a,unreal.Texture2D):
  role=int(a.get_name().split('_')[-1]);a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP if role==2 else unreal.TextureCompressionSettings.TC_DEFAULT);a.set_editor_property('srgb',role in [0,3])
 assert a.get_path_name().startswith(root+'/');unreal.EditorAssetLibrary.save_loaded_asset(a,False)
