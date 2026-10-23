"""Guarded resumable data-only migration. Existing assets must match exactly; saves/maps/models are never changed."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();assert R==Path('/Users/harry/Developer/PokeMonster')
O=R/'Saved/MoveEffectsV4/Resume/AssetMigration.json';assert not O.exists(),'Already migrated: use the read-only validator'
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
plan=json.loads((R/'Tools/MoveEffectsV4/CrystalMovePlan.json').read_text());ref=json.loads((R/'Tools/CreatureProgressionV1/Gen2Reference.json').read_text());assets={};created=[];changed=[];species_changes=[]
def stable(v):
 if hasattr(v,'export_text'):return v.export_text()
 if isinstance(v,(list,tuple,unreal.Array)):return [stable(x)for x in v]
 if isinstance(v,unreal.Object):return v.get_path_name()
 return str(v)
def props(row):return dict(internal_id=row['id'],display_name=row['name'],type=getattr(unreal.PokeMonsterCreatureType,row['type']),category=getattr(unreal.PokeMonsterMoveCategory,row['category']),base_power=row['power'],accuracy=row['accuracy'],max_pp=row['max_pp'],priority=row['priority'],never_miss=row['never_miss'],bypass_protect=row['bypass_protect'],requires_sleeping_target=row['requires_sleeping_target'],critical_stage_bonus=row['critical_stage_bonus'])
def effect_value(k,v):
 return getattr(unreal.PokeMonsterEffectKind,v)if k=='kind'else getattr(unreal.PokeMonsterBattleStat,v)if k=='stat'else getattr(unreal.PokeMonsterCreatureStatus,v)if k=='status'else [getattr(unreal.PokeMonsterCreatureType,x)for x in v]if k=='immune_types'else v
for row in plan['rows']:
 path=row['path'];asset=unreal.load_asset(path)if unreal.EditorAssetLibrary.does_asset_exist(path)else None
 if row['previously_supported']:
  assert asset and str(asset.internal_id)==row['id'] and asset.max_pp==row['max_pp'] and asset.accuracy==row['accuracy']
  category=getattr(unreal.PokeMonsterMoveCategory,row['category'])
  if asset.category!=category:
   changed.append(dict(path=path,before=str(asset.category),after=str(category)));asset.set_editor_property('category',category);assert unreal.EditorAssetLibrary.save_loaded_asset(asset)
 else:
  # An interrupted migration may have saved exactly matching new assets. Never overwrite a mismatch.
  if asset:
   for k,v in props(row).items():assert stable(asset.get_editor_property(k))==stable(v),(path,k)
   assert len(asset.effects)==len(row['components'])
   for a,w in zip(asset.effects,row['components']):
    for k,v in w.items():assert stable(a.get_editor_property('_self'if k=='self'else k))==stable(effect_value(k,v)),(path,k)
  else:
   factory=unreal.DataAssetFactory();factory.set_editor_property('data_asset_class',unreal.PokeMonsterMoveData)
   asset=unreal.AssetToolsHelpers.get_asset_tools().create_asset(path.rsplit('/',1)[1],path.rsplit('/',1)[0],unreal.PokeMonsterMoveData,factory);assert asset
   for k,v in props(row).items():asset.set_editor_property(k,v)
   effects=[]
   for c in row['components']:
    e=unreal.PokeMonsterMoveEffectComponent()
    for k,v in c.items():e.set_editor_property('_self'if k=='self'else k,effect_value(k,v))
    effects.append(e)
   asset.set_editor_property('effects',effects);asset.set_editor_property('effect',unreal.PokeMonsterMoveEffect(description=row['description'],chance_percent=100));assert unreal.EditorAssetLibrary.save_loaded_asset(asset)
  created.append(path)
 assets[int(row['original_id'])]=asset
names={1:'Bisasam',4:'Zunderlauf',6:'Glurak',7:'Schiggy',25:'Pikachu',43:'Myrapla',54:'Enton',68:'Machomei',92:'Nebulak',94:'Gengar'}
protected=['internal_id','display_name','pokedex_number','base_capture_rate','primary_type','secondary_type','base_stats','gender','starting_level','growth_rate','evolutions','visuals','overworld','base_experience_yield']
for row in ref['species']:
 name=names[row['dex']];s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);assert s and str(s.get_internal_id())==name
 before={k:stable(s.get_editor_property(k))for k in protected};old=list(s.level_up_moves);assert len(old)==len(row['learnset'])
 entries=[]
 for existing,entry in zip(old,row['learnset']):
  assert existing.level==entry['level'];m=assets[int(entry['move_id'])]
  if existing.move:assert existing.move==m
  else:assert str(existing.unavailable_move_name)
  entries.append(unreal.PokeMonsterLevelMove(level=entry['level'],move=m))
 s.set_editor_property('level_up_moves',entries);assert {k:stable(s.get_editor_property(k))for k in protected}==before
 assert unreal.EditorAssetLibrary.save_loaded_asset(s);species_changes.append(dict(species=name,entries=len(entries),protected_properties_unchanged=before))
assert len(created)==49 and len(species_changes)==10
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
O.write_text(json.dumps(dict(created=created,category_changes=changed,species=species_changes),ensure_ascii=False,indent=2));unreal.log('V4_CRYSTAL_PRODUCTION_DATA_BOUND')
