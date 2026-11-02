"""Small surface/volume balance after direct review; original reference unchanged."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();m=unreal.load_asset('/Game/Environment/WestlandEnvironmentPolishV2/Materials/M_WEP_FlowingRiver');ML=unreal.MaterialEditingLibrary
for prop,v in [(unreal.MaterialProperty.MP_OPACITY,.32),(unreal.MaterialProperty.MP_ROUGHNESS,.11)]:
 n=ML.get_material_property_input_node(m,prop);assert isinstance(n,unreal.MaterialExpressionConstant);n.set_editor_property('r',v)
ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(D/'WaterSurfaceBalance.json').write_text(json.dumps(dict(opacity=.32,roughness=.11,reason='More visible moving surface/reflections while preserving volume transmission'),indent=2))
