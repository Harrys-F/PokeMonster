"""Read-only Unreal asset inventory. Incoming GLBs are not playable species."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EvolutionV3';D.mkdir(parents=True,exist_ok=True)
registry=unreal.AssetRegistryHelpers.get_asset_registry();registry.search_all_assets(True)
playable=unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species();ids={s.get_path_name()for s in playable};rows=[]
for a in registry.get_assets_by_path('/Game/Data/Creatures',True):
 s=a.get_asset()
 if not isinstance(s,unreal.PokeMonsterCreatureSpeciesData):continue
 v=s.get_visuals().presentation
 rows.append({'path':s.get_path_name(),'id':str(s.get_internal_id()),'name':str(s.get_display_name()),'dex':s.get_pokedex_number(),'playable':s.get_path_name()in ids,'presentation':v.get_path_name()if v else None,'size_cm':v.reference_size_cm if v else None,'clips':{str(k):x.get_path_name()if x else None for k,x in v.clips.items()}if v else {},'routes':[x.export_text()for x in s.get_evolutions()]})
items=[]
for a in registry.get_assets_by_path('/Game/Data/Items',True):
 x=a.get_asset()
 if isinstance(x,unreal.PokeMonsterItemData):items.append({'path':x.get_path_name(),'id':str(x.get_internal_id()),'name':str(x.get_display_name()),'category':str(x.get_category()),'configured':x.is_configured(),'overworld':x.can_use_in_overworld()})
result={'species':sorted(rows,key=lambda x:x['dex']),'playable_count':len(playable),'items':items,'incoming':[p.name for p in sorted((R/'Art/Characters/Creatures/Incoming').glob('*.glb'))]}
(D/'AssetAudit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False));print('EVOLUTION_V3_AUDIT',len(rows),'species assets,',len(playable),'playable,',len(items),'items')
