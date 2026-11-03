import unreal,json
from pathlib import Path
D=Path(unreal.Paths.project_dir()).resolve()/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7'
(D/'Dirty.json').write_text(json.dumps(dict(maps=[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],content=[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]),indent=2))
