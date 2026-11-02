import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';rows=[]
for root in ['/Game/Environment/WestlandAssetLibrary','/Game/Environment/VisualV2EnvironmentV3','/Game/Environment/Westland/NaturalGroundV1','/Game/Environment/VisualV2HealingArtV4']:
 for path in unreal.EditorAssetLibrary.list_assets(root,True,False):
  if not any(x in path.lower()for x in ['flower','boulder','pebble','fern','moss','grass','wildbush']):continue
  a=unreal.load_asset(path)
  if isinstance(a,unreal.StaticMesh):
   b=a.get_bounding_box();rows.append(dict(path=a.get_path_name(),min=b.min.to_tuple(),max=b.max.to_tuple(),triangles=a.get_num_triangles(0),materials=[x.material_interface.get_path_name()if x.material_interface else None for x in a.static_materials]))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(D/'Assets.json').write_text(json.dumps(rows,indent=2))
