import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';rows=[]
for folder in ['Trees','Vegetation']:
 for p in sorted((R/'Content/Environment/WestlandAssetLibrary/Meshes'/folder).glob('*.uasset')):
  asset='/Game/'+str(p.relative_to(R/'Content').with_suffix(''));m=unreal.load_asset(asset);b=m.get_bounding_box();rows.append(dict(asset=asset,min=b.min.to_tuple(),max=b.max.to_tuple(),triangles=m.get_num_triangles(0),materials=[x.material_interface.get_path_name()if x.material_interface else None for x in m.static_materials]))
(D/'AssetDetails.json').write_text(json.dumps(rows,indent=2))
