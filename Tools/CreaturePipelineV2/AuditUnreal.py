"""Read-only live registry audit. No imports, reimports, asset writes or map saves."""
import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreaturePipelineV2';O.mkdir(exist_ok=True)
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
def dirty():return {'maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
assert not E.get_game_world() and not any(dirty().values()),dirty()
reg=unreal.AssetRegistryHelpers.get_asset_registry();reg.wait_for_completion();species=[];blueprints=[]
for row in reg.get_assets_by_path('/Game',recursive=True):
 cls=str(row.asset_class_path.asset_name)
 if cls=='Blueprint':blueprints.append(str(row.package_name))
 if cls!='PokeMonsterCreatureSpeciesData':continue
 a=row.get_asset();v=a.get_editor_property('visuals');p=v.get_editor_property('presentation');match=re.search(r"Presentation=[^,)]*?(/Game/[A-Za-z0-9_/.]+)",v.export_text());p=p if isinstance(p,unreal.PokeMonsterCreaturePresentationData) else (unreal.load_asset(match.group(1)) if match else None)
 item={'asset':a.get_path_name(),'internal_id':str(a.get_internal_id()),'pokedex_number':a.get_pokedex_number(),'stable_primary_id':'CreatureSpecies:'+str(a.get_internal_id()),'presentation':p.get_path_name() if p else None}
 if p:
  m=p.get_editor_property('mesh');clips=p.get_editor_property('clips');item['mesh']=m.get_path_name();item['skeleton']=m.skeleton.get_path_name();item['clips']={str(k):{'asset':v.get_path_name(),'skeleton':v.get_editor_property('skeleton').get_path_name(),'seconds':v.get_play_length()} for k,v in clips.items()};item['validation_errors']=list(p.get_validation_errors()) if hasattr(p,'get_validation_errors') else 'not implemented in V1'
 species.append(item)
result={'species':species,'blueprints':blueprints,'world':E.get_editor_world().get_path_name(),'dirty':dirty(),'read_only':True};assert not any(dirty().values());(O/'UnrealInventory.json').write_text(json.dumps(result,indent=2));unreal.log('CREATURE_PIPELINE_V2_AUDIT_PASS')
