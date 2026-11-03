"""Correct only own imported color-texture roles; preserve embedded bytes, all original sources/parents."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';rows=[]
for info in json.loads((D/'ImportedModels.json').read_text()):
 for item in info['objects']:
  if item['kind']!='Texture2D':continue
  t=unreal.load_asset(item['path']);index=int(t.get_name().split('_')[-1]);assert index in [0,1,2,3]
  color=index in [0,3];normal=index==2;compression=unreal.TextureCompressionSettings.TC_NORMALMAP if normal else unreal.TextureCompressionSettings.TC_DEFAULT
  if t.srgb!=color or t.compression_settings!=compression:
   rows.append(dict(path=t.get_path_name(),before_srgb=t.srgb,before_compression=str(t.compression_settings),after_srgb=color,after_compression=str(compression)))
   t.set_editor_property('compression_settings',compression);t.set_editor_property('srgb',color);assert unreal.EditorAssetLibrary.save_loaded_asset(t,False)
assert len(rows)==2,rows
(D/'TextureRoleCorrection.json').write_text(json.dumps(rows,indent=2))
