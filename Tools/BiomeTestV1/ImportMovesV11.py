"""Four reviewed new data assets; only the existing V4 shared effect components, no combat implementation."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
O=R/'Saved/BiomeTestV11/MoveBindingsApplied.json';assert not O.exists();plan=json.loads((R/'Tools/BiomeTestV1/MoveBindingsV11.json').read_text());paths=[]
for row in plan['rows']:
 path=row['path'];assert path.startswith('/Game/Data/Moves/BiomeV11/')and not unreal.EditorAssetLibrary.does_asset_exist(path)
 f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',unreal.PokeMonsterMoveData);m=unreal.AssetToolsHelpers.get_asset_tools().create_asset(path.rsplit('/',1)[1],path.rsplit('/',1)[0],unreal.PokeMonsterMoveData,f);assert m
 for k,v in dict(internal_id=row['id'],display_name=row['name'],type=getattr(unreal.PokeMonsterCreatureType,row['type']),category=getattr(unreal.PokeMonsterMoveCategory,row['category']),base_power=row['power'],accuracy=row['accuracy'],max_pp=row['max_pp'],priority=row['priority']).items():m.set_editor_property(k,v)
 effects=[]
 for c in row['components']:
  e=unreal.PokeMonsterMoveEffectComponent()
  for k,v in c.items():
   value=getattr(unreal.PokeMonsterEffectKind,v)if k=='kind'else getattr(unreal.PokeMonsterBattleStat,v)if k=='stat'else getattr(unreal.PokeMonsterCreatureStatus,v)if k=='status'else[getattr(unreal.PokeMonsterCreatureType,t)for t in v]if k=='immune_types'else v;e.set_editor_property(k,value)
  effects.append(e)
 m.set_editor_property('effects',effects);m.set_editor_property('effect',unreal.PokeMonsterMoveEffect(description=row['description'],chance_percent=100));assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);paths.append(path)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();O.write_text(json.dumps({'new_assets':paths,'existing_moves_changed':False,'new_effect_logic':False},indent=2))
