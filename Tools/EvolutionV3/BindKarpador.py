"""Guarded addition of the one missing route whose two species are already playable."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EvolutionV3'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
s=unreal.load_asset('/Game/Data/Creatures/DA_Karpador');target=unreal.load_asset('/Game/Data/Creatures/DA_Garados')
assert s and target and s in unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species()and target in unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species()
ref=json.loads((R/'Tools/EvolutionV3/ReferenceSources.json').read_text());assert ref['selected_gyarados_row']['minimum_level']=='20'
before=[r.export_text()for r in s.get_evolutions()]
if not before:
 s.set_editor_property('evolutions',[unreal.PokeMonsterEvolutionData(target_species=unreal.PrimaryAssetId(unreal.PrimaryAssetType('CreatureSpecies'),'Garados'),trigger=unreal.PokeMonsterEvolutionTrigger.LEVEL,minimum_level=20)])
 assert unreal.EditorAssetLibrary.save_loaded_asset(s)
else:
 assert len(s.get_evolutions())==1 and str(s.get_evolutions()[0].target_species.primary_asset_name)=='Garados'and s.get_evolutions()[0].minimum_level==20,'Unexpected existing route; never overwrite'
(D/'BoundRoute.json').write_text(json.dumps({'before':before,'after':[r.export_text()for r in s.get_evolutions()],'only_asset':s.get_path_name(),'no_map_saved':True},indent=2))
