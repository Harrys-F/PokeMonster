"""Import each new owner GLB into a private static-inspection namespace. Source hashes checked."""
import unreal,json,hashlib,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';root='/Game/Characters/Creatures/ModelIntakeV6';manifest=D/'ImportedModels.json';out=json.loads(manifest.read_text())if manifest.exists()else[]
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
for info in json.loads((D/'IncomingInventory.json').read_text())['files']:
 if not(info.get('valid_glb')and info['new_since_v5']):continue
 name=Path(info['name']).stem.replace(' ','_');path=root+'/'+name;source=R/info['path'];assert hashlib.sha256(source.read_bytes()).hexdigest()==info['sha256']
 if any(x['source']==info['path']for x in out):continue
 if name=='Aquana':objects=[unreal.load_asset(p)for p in json.loads((D/'ImportOne.json').read_text())['paths']]
 else:
  assert not unreal.EditorAssetLibrary.does_directory_exist(path),path
  t=unreal.AssetImportTask();t.filename=str(source);t.destination_path=path;t.destination_name='SM_'+name+'_Import';t.automated=True;t.replace_existing=False;t.save=False
  unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);objects=t.get_objects()
 meshes=[a for a in objects if isinstance(a,unreal.StaticMesh)];assert len(meshes)==1,(name,meshes)
 mesh=meshes[0];b=mesh.get_bounds();slots=mesh.get_editor_property('static_materials');assert slots and all(x.material_interface for x in slots)
 for a in objects:
  if isinstance(a,unreal.Texture2D):
   role=int(a.get_name().split('_')[-1]);a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP if role==2 else unreal.TextureCompressionSettings.TC_DEFAULT);a.set_editor_property('srgb',role in [0,3])
  assert a.get_path_name().startswith(path+'/');assert unreal.EditorAssetLibrary.save_loaded_asset(a,False)
 out.append(dict(source=info['path'],sha256=info['sha256'],target='Modell:'+name,mesh=mesh.get_path_name(),objects=[dict(path=a.get_path_name(),kind=a.get_class().get_name())for a in objects],bounds_origin=b.origin.to_tuple(),bounds_extent=b.box_extent.to_tuple(),lods=mesh.get_num_lods(),materials=[x.material_interface.get_path_name()for x in slots],status='Static inspection only; no skeleton, weights or animations. Canonical species scale/facing and gameplay setup pending.'))
 manifest.write_text(json.dumps(out,indent=2));print('V6_IMPORTED',name,len(out));objects=[];meshes=[];mesh=None;t=None;gc.collect();unreal.SystemLibrary.collect_garbage()
assert len(out)==49
