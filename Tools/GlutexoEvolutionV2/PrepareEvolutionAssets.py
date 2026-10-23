"""One guarded Glutexo rule and a capture-only effect material. No original model or map reimport."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
s=unreal.load_asset('/Game/Data/Creatures/DA_Glutexo');a=unreal.load_asset('/Game/Data/Creatures/DA_Zunderlauf');assert s and a
routes=list(a.get_evolutions());assert len(routes)==1 and str(routes[0].target_species.primary_asset_name)=='Glutexo' and routes[0].minimum_level==16
assert not s.get_evolutions(),'Never replace an existing reviewed route'
s.set_editor_property('evolutions',[unreal.PokeMonsterEvolutionData(target_species=unreal.PrimaryAssetId(unreal.PrimaryAssetType('CreatureSpecies'),'Glurak'),minimum_level=36,trigger=unreal.PokeMonsterEvolutionTrigger.LEVEL)])
assert unreal.EditorAssetLibrary.save_loaded_asset(s)
P='/Game/Characters/Creatures/Shared/EvolutionV2';assert not unreal.EditorAssetLibrary.does_asset_exist(P+'/M_EvolutionGlow')
m=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_EvolutionGlow',P,unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_ADDITIVE);m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT);m.set_editor_property('two_sided',True);m.set_editor_property('used_with_skeletal_mesh',True)
L=unreal.MaterialEditingLibrary
c=L.create_material_expression(m,unreal.MaterialExpressionConstant3Vector);c.set_editor_property('constant',unreal.LinearColor(1,.86,.52,1))
f=L.create_material_expression(m,unreal.MaterialExpressionScalarParameter);f.set_editor_property('parameter_name','Strength');f.set_editor_property('default_value',0.)
mult=L.create_material_expression(m,unreal.MaterialExpressionMultiply);L.connect_material_expressions(c,'',mult,'A');L.connect_material_expressions(f,'',mult,'B');L.connect_material_property(mult,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
one=L.create_material_expression(m,unreal.MaterialExpressionConstant);one.set_editor_property('r',1.);L.connect_material_property(one,'',unreal.MaterialProperty.MP_OPACITY);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m)
(R/'Saved/GlutexoEvolutionV2/EvolutionAssets.json').write_text(json.dumps({'source_route':'Zunderlauf >=16 -> Glutexo (existing, unchanged)','new_route':'Glutexo >=36 -> Glurak','capture_only_material':m.get_path_name(),'no_map_saved':True},indent=2))
