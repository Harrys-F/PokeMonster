"""Read-only full comparison of ten runtime learnsets with the pinned Gen2 extract."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();ref=json.loads((R/'Tools/CreatureProgressionV1/Gen2Reference.json').read_text());meta={int(m['id']):m for m in ref['moves']};names={1:'Bisasam',4:'Zunderlauf',6:'Glurak',7:'Schiggy',25:'Pikachu',43:'Myrapla',54:'Enton',68:'Machomei',92:'Nebulak',94:'Gengar'};rows=[]
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
for row in ref['species']:
 name=names[row['dex']];s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);assert s and str(s.get_internal_id())==name
 entries=list(s.level_up_moves);assert len(entries)==len(row['learnset']);supported=0
 for entry,expected in zip(entries,row['learnset']):
  m=meta[expected['move_id']];assert entry.level==expected['level']
  if m['runtime_supported']:
   assert entry.move and not str(entry.unavailable_move_name);asset=entry.move;supported+=1
   assert str(asset.internal_id)==''.join(t.title()for t in m['identifier'].split('-'))
   assert asset.max_pp==int(m['pp'])and asset.accuracy==int(m['accuracy']or 100)and asset.priority==int(m['priority'])
   if m['power']:assert asset.base_power==int(m['power'])
   effect_map={'ember':('Burn',10),'flamethrower':('Burn',10),'growl':('AttackDown',100),'tail-whip':('DefenseDown',100),'leer':('DefenseDown',100),'withdraw':('DefenseUp',100),'bubble':('SpeedDown',10),'absorb':('DrainHalf',100),'leech-seed':('LeechSeed',100),'night-shade':('UserLevelDamage',100),'seismic-toss':('UserLevelDamage',100)}
   effect,chance=effect_map.get(m['identifier'],('None',100));assert str(asset.effect.effect_id)==effect and asset.effect.chance_percent==chance
  else:assert entry.move is None and str(entry.unavailable_move_name)==m['german_name'] and str(entry.unavailable_reason)
 rows.append(dict(species=name,dex_identity_unchanged=s.get_pokedex_number(),entries=len(entries),supported=supported,unsupported=len(entries)-supported,growth=str(s.get_growth_rate())))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(R/'Saved/CreatureProgressionV1/DataValidation.json').write_text(json.dumps(dict(passed=True,source_commit=ref['source_commit'],species=rows),indent=2));unreal.log('PROGRESSION_DATA_VALIDATED')
