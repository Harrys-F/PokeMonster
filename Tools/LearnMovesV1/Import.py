"""Bind only the sixteen audited gaps. Never reimport creatures or overwrite populated learn entries."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
O=R/'Saved/ProjectRefinement/LearnMovesV1';O.mkdir(exist_ok=True);report=O/'Migration.json';assert not report.exists()
plan=json.loads((R/'Tools/LearnMovesV1/Plan.json').read_text());assets={};changed=[]
def stable(v):return v.export_text()if hasattr(v,'export_text')else v.get_path_name()if isinstance(v,unreal.Object)else str(v)
def value(k,v):return getattr(unreal.PokeMonsterEffectKind,v)if k=='kind'else getattr(unreal.PokeMonsterCreatureStatus,v)if k=='status'else[getattr(unreal.PokeMonsterCreatureType,t)for t in v]if k=='immune_types'else v
for row in plan['rows']:
 path=row['path'];assert path.startswith('/Game/Data/Moves/LearnMovesV1/');props=dict(internal_id=row['id'],display_name=row['name'],type=getattr(unreal.PokeMonsterCreatureType,row['type']),category=getattr(unreal.PokeMonsterMoveCategory,row['category']),base_power=row['power'],accuracy=row['accuracy'],max_pp=row['max_pp'],priority=row['priority'],never_miss=row['never_miss'])
 effects=[]
 for c in row['components']:
  e=unreal.PokeMonsterMoveEffectComponent()
  for k,v in c.items():e.set_editor_property('_self'if k=='self'else 'bSecondary'if k=='secondary'else k,value(k,v))
  effects.append(e)
 m=unreal.load_asset(path)if unreal.EditorAssetLibrary.does_asset_exist(path)else None
 if m:
  for k,v in props.items():assert stable(m.get_editor_property(k))==stable(v),(path,k)
  assert[m.export_text()for m in m.effects]==[e.export_text()for e in effects],path
 else:
  f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',unreal.PokeMonsterMoveData);m=unreal.AssetToolsHelpers.get_asset_tools().create_asset(path.rsplit('/',1)[1],path.rsplit('/',1)[0],unreal.PokeMonsterMoveData,f);assert m
  for k,v in props.items():m.set_editor_property(k,v)
  m.set_editor_property('effects',effects);m.set_editor_property('effect',unreal.PokeMonsterMoveEffect(description='Pokémon Kristall / Generation 2; geprüfte Lernbindung V1.',chance_percent=100));assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
 assets[row['token']]=m
for name in sorted({x['species']for x in plan['bindings']}):
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);assert s
 protected=['internal_id','display_name','pokedex_number','base_capture_rate','primary_type','secondary_type','base_stats','gender','starting_level','growth_rate','evolutions','visuals','overworld','base_experience_yield']
 before={k:stable(s.get_editor_property(k))for k in protected};old=list(s.level_up_moves);oldtexts=[e.export_text()for e in old];new=list(old)
 for bind in[x for x in plan['bindings']if x['species']==name]:
  matches=[i for i,e in enumerate(old)if e.level==bind['level']and(e.move==assets[bind['token']]or(not e.move and str(e.unavailable_move_name)))];assert len(matches)==1,(name,bind)
  i=matches[0];new[i]=unreal.PokeMonsterLevelMove(level=bind['level'],move=assets[bind['token']]);changed.append(bind)
  # Everything outside this explicitly listed index must remain byte-equivalent in exported struct text.
 selected={i for i,(a,b)in enumerate(zip(oldtexts,[e.export_text()for e in new]))if a!=b};expected={i for i,e in enumerate(old)if any(x['species']==name and x['level']==e.level for x in plan['bindings'])};assert selected<=expected
 s.set_editor_property('level_up_moves',new);assert before=={k:stable(s.get_editor_property(k))for k in protected};assert unreal.EditorAssetLibrary.save_loaded_asset(s,False)
assert len(changed)==16 and len(assets)==15
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();report.write_text(json.dumps(dict(bindings=changed,new_assets=[m.get_path_name()for m in assets.values()],original_creature_properties_unchanged=True),ensure_ascii=False,indent=2))
