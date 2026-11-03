"""Remove unconnected nodes left by authoring retries; private V7 graphs only."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());D=R/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';ML=unreal.MaterialEditingLibrary;assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();rows=[]
for name in ['LimePlaster','SageLimewash','OakFloor','OakJoinery','ReviewWater']:
 m=unreal.load_asset('/Game/Environment/VisualV2InteriorV7/Materials/M_V7_'+name);before=len(ML.get_material_expressions(m));ML.delete_unused_expressions(m);errors=ML.recompile_material(m);assert not errors,[str(x)for x in errors];after=len(ML.get_material_expressions(m));assert after<=before;assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);rows.append(dict(material=m.get_path_name(),before=before,after=after,shader_errors=0))
(D/'MaterialPruned.json').write_text(json.dumps(rows,indent=2))
