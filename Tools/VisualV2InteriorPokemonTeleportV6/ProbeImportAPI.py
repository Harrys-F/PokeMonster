import unreal,json
from pathlib import Path
D=Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();out={k:hasattr(unreal,k)for k in ['GLTFImportFactory','GLTFImportOptions','InterchangeManager','InterchangeGenericAssetsPipeline','InterchangeGenericMeshPipeline','InterchangeGenericMaterialPipeline','AssetImportTask']};print(out);(D/'ImportAPI.json').write_text(json.dumps(out,indent=2))
