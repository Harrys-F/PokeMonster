"""Guarded data-only migration: ten existing species, three missing supported moves.
No map, visual, original model, or saved individual is modified.
"""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreatureProgressionV1';ref=json.loads((R/'Tools/CreatureProgressionV1/Gen2Reference.json').read_text())
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
names={1:'Bisasam',4:'Zunderlauf',6:'Glurak',7:'Schiggy',25:'Pikachu',43:'Myrapla',54:'Enton',68:'Machomei',92:'Nebulak',94:'Gengar'}
for name in names.values():
 existing=unreal.load_asset('/Game/Data/Creatures/DA_'+name);assert existing and not existing.get_evolutions(),'One-time migration already applied or preexisting routes require comparison: '+name
move_refs={};created=[];changes=[]
for m in ref['moves']:
 if not m['runtime_supported']:continue
 assert m['accuracy'] or m['identifier']=='withdraw','Only the verified self-target move maps null accuracy to unconditional success'
 name=''.join(x.title() for x in m['identifier'].split('-'));path='/Game/Data/Moves/DA_'+name
 if name in ['Flamethrower','Slam','HydroPump']:path='/Game/Data/Moves/ProgressionV1/DA_'+name
 existed=unreal.EditorAssetLibrary.does_asset_exist(path);asset=unreal.load_asset(path) if existed else None
 assert existed or name in ['Flamethrower','Slam','HydroPump'],path
 if not asset:
  factory=unreal.DataAssetFactory();factory.set_editor_property('data_asset_class',unreal.PokeMonsterMoveData)
  asset=unreal.AssetToolsHelpers.get_asset_tools().create_asset('DA_'+name,path.rsplit('/',1)[0],unreal.PokeMonsterMoveData,factory);assert asset
  vals=dict(internal_id=name,display_name=m['german_name'],type=unreal.PokeMonsterCreatureType.FIRE if name=='Flamethrower' else unreal.PokeMonsterCreatureType.WATER if name=='HydroPump' else unreal.PokeMonsterCreatureType.NORMAL,category=unreal.PokeMonsterMoveCategory.SPECIAL if name!='Slam' else unreal.PokeMonsterMoveCategory.PHYSICAL,base_power=int(m['power']),accuracy=int(m['accuracy'] or 100),max_pp=int(m['pp']),priority=int(m['priority']))
  for k,v in vals.items():asset.set_editor_property(k,v)
  if name=='Flamethrower':asset.set_editor_property('effect',unreal.PokeMonsterMoveEffect(effect_id='Burn',description='10 % Verbrennungschance.',chance_percent=10))
  assert unreal.EditorAssetLibrary.save_loaded_asset(asset);created.append(path)
 # Never rewrite an existing move just to make this validation pass.
 assert str(asset.internal_id)==name and int(asset.max_pp)==int(m['pp']) and int(asset.accuracy)==int(m['accuracy'] or 100),name
 if m['power']:assert int(asset.base_power)==int(m['power']),(name,m['power'],asset.base_power)
 move_refs[int(m['id'])]=asset
# Only verified normal level routes and Thunder Stone. Trade examples stay provisional.
routes={1:('Bisaknosp',16),4:('Glutexo',16),7:('Schillok',16),43:('Duflor',21),54:('Entoron',33),92:('Alpollo',25)}
metadata={int(m['id']):m for m in ref['moves']}
for row in ref['species']:
 name=names[row['dex']];asset=unreal.load_asset('/Game/Data/Creatures/DA_'+name);assert asset and str(asset.get_internal_id())==name
 visuals=asset.get_visuals().presentation.get_path_name();stats=tuple(getattr(asset.get_base_stats(),k)for k in ['hp','attack','defense','special_attack','special_defense','speed']);growth=str(asset.get_growth_rate());entries=[]
 for e in row['learnset']:
  m=metadata[e['move_id']]
  if m['runtime_supported']:entry=unreal.PokeMonsterLevelMove(level=e['level'],move=move_refs[e['move_id']])
  else:entry=unreal.PokeMonsterLevelMove(level=e['level'],unavailable_move_name=m['german_name'],unavailable_reason=m['unavailable_reason'])
  entries.append(entry)
 asset.set_editor_property('level_up_moves',entries)
 evolutions=list(asset.get_evolutions());assert not evolutions,'Preexisting evolution data requires manual comparison'
 if row['dex'] in routes:
  target,level=routes[row['dex']];evolutions=[unreal.PokeMonsterEvolutionData(target_species=unreal.PrimaryAssetId(unreal.PrimaryAssetType('CreatureSpecies'),target),trigger=unreal.PokeMonsterEvolutionTrigger.LEVEL,minimum_level=level)]
 elif row['dex']==25:evolutions=[unreal.PokeMonsterEvolutionData(target_species=unreal.PrimaryAssetId(unreal.PrimaryAssetType('CreatureSpecies'),'Raichu'),trigger=unreal.PokeMonsterEvolutionTrigger.ITEM,required_item_id='ThunderStone')]
 asset.set_editor_property('evolutions',evolutions)
 assert asset.get_visuals().presentation.get_path_name()==visuals and tuple(getattr(asset.get_base_stats(),k)for k in ['hp','attack','defense','special_attack','special_defense','speed'])==stats and str(asset.get_growth_rate())==growth
 assert unreal.EditorAssetLibrary.save_loaded_asset(asset)
 changes.append(dict(species=name,entries=len(entries),supported=sum(e['move_id'] in move_refs for e in row['learnset']),growth_unchanged=growth,evolutions=[str(e) for e in evolutions]))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(O/'DataMigration.json').write_text(json.dumps(dict(source_commit=ref['source_commit'],created=created,species=changes),indent=2));unreal.log('PROGRESSION_DATA_READY')
