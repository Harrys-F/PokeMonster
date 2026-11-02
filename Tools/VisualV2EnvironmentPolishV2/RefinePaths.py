"""One local material correction after actual PIE review: remove mulch dominance."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();m=unreal.load_asset('/Game/Environment/VisualV2EnvironmentPolishV2/Materials/M_EP2_Ground');ML=unreal.MaterialEditingLibrary
for n in ML.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionTextureSample)and n.texture:
  q=n.texture.get_path_name()
  if 'T_ugsnfawlw_2K_B'in q:n.texture=unreal.load_asset('/Game/Fab/VisualV2TrialLocal/Ground/T_pjwey0_2K_B')
  if 'T_ugsnfawlw_2K_N'in q:n.texture=unreal.load_asset('/Game/Fab/VisualV2TrialLocal/Ground/T_pjwey0_2K_N')
 if isinstance(n,unreal.MaterialExpressionCustom)and'float3 dirt='in n.get_editor_property('code'):
  n.set_editor_property('code','float g=dot(T,float3(.299,.587,.114));float3 dirt=lerp(T*float3(1.0,.81,.60),g*float3(1.12,.91,.69),.78);return lerp(C,dirt*.90,M);')
ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);(D/'PathRefinement.json').write_text(json.dumps(dict(reason='PIE review still showed woody Forest Path debris; use existing Grass And Rubble fine soil/gravel with muted warm earth tint',material=m.get_path_name(),no_geometry_or_collision_changes=True),indent=2))
