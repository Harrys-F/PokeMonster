"""Read-only validation of all production bindings; never infers playable support from effect metadata alone."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();plan=json.loads((R/'Tools/MoveEffectsV4/CrystalMovePlan.json').read_text());ref=json.loads((R/'Tools/CreatureProgressionV1/Gen2Reference.json').read_text());migration=json.loads((R/'Docs/ATTACKENSYSTEM_V4_DATENANBINDUNG.json').read_text());byid={int(r['original_id']):r for r in plan['rows']};rows=[]
def stable(v):
 if hasattr(v,'export_text'):return v.export_text()
 if isinstance(v,(list,tuple,unreal.Array)):return [stable(x)for x in v]
 if isinstance(v,unreal.Object):return v.get_path_name()
 return str(v)
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
for m in plan['rows']:
 a=unreal.load_asset(m['path']);assert a and str(a.internal_id)==m['id']
 for k,v in [('max_pp',m['max_pp']),('base_power',m['power']),('accuracy',m['accuracy']),('priority',m['priority'])]:assert getattr(a,k)==v,(m['id'],k,getattr(a,k),v)
 assert a.type==getattr(unreal.PokeMonsterCreatureType,m['type']) and a.category==getattr(unreal.PokeMonsterMoveCategory,m['category'])
 if not m['previously_supported']:
  assert str(a.effect.description)==m['description'];assert a.never_miss==m['never_miss'] and a.bypass_protect==m['bypass_protect'] and a.requires_sleeping_target==m['requires_sleeping_target'] and a.critical_stage_bonus==m['critical_stage_bonus'];assert len(a.effects)==len(m['components'])
  for actual,want in zip(a.effects,m['components']):
   for k,v in want.items():
    expected=getattr(unreal.PokeMonsterEffectKind,v)if k=='kind'else getattr(unreal.PokeMonsterBattleStat,v)if k=='stat'else getattr(unreal.PokeMonsterCreatureStatus,v)if k=='status'else [getattr(unreal.PokeMonsterCreatureType,x)for x in v]if k=='immune_types'else v
    assert actual.get_editor_property('_self'if k=='self'else k)==expected,(m['id'],k)
 rows.append(dict(id=m['id'],path=m['path'],configured_data_verified=True,originally_missing=not m['previously_supported']))
names={1:'Bisasam',4:'Zunderlauf',6:'Glurak',7:'Schiggy',25:'Pikachu',43:'Myrapla',54:'Enton',68:'Machomei',92:'Nebulak',94:'Gengar'}
for row in ref['species']:
 name=names[row['dex']];s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);baseline=next(x for x in migration['species']if x['species']==name)['protected_properties_unchanged']
 assert {k:stable(s.get_editor_property(k))for k in baseline}==baseline
 assert len(s.level_up_moves)==len(row['learnset'])
 for actual,want in zip(s.level_up_moves,row['learnset']):
  assert actual.level==want['level'] and actual.move==unreal.load_asset(byid[want['move_id']]['path']) and not str(actual.unavailable_move_name) and not str(actual.unavailable_reason)
assert len(rows)==68 and sum(r['originally_missing']for r in rows)==49
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(R/'Saved/MoveEffectsV4/Resume/DataValidation.json').write_text(json.dumps(dict(passed=True,moves=rows,learnlist_entries=sum(len(s['learnset'])for s in ref['species']),unchanged_species_properties=True),indent=2));unreal.log('CRYSTAL_DATA_VALIDATED 68 moves, 49 newly bound')
