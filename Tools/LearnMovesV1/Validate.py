"""Read-only verification of exact productive data and every original learnlist entry."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P=json.loads((R/'Tools/LearnMovesV1/Plan.json').read_text());species=json.loads((R/'Tools/BiomeTestV1/SpeciesV11.json').read_text());report=[]
for row in P['rows']:
 m=unreal.load_asset(row['path']);assert m and str(m.internal_id)==row['id']and str(m.display_name)==row['name'];assert(m.base_power,m.accuracy,m.max_pp,m.priority)==(row['power'],row['accuracy'],row['max_pp'],row['priority']);assert m.type==getattr(unreal.PokeMonsterCreatureType,row['type'])and m.category==getattr(unreal.PokeMonsterMoveCategory,row['category']);assert len(m.effects)==len(row['components']);
 for e,c in zip(m.effects,row['components']):
  for k,v in c.items():
   actual=e.get_editor_property('_self'if k=='self'else'bSecondary'if k=='secondary'else k);expected=getattr(unreal.PokeMonsterEffectKind,v)if k=='kind'else getattr(unreal.PokeMonsterCreatureStatus,v)if k=='status'else[getattr(unreal.PokeMonsterCreatureType,t)for t in v]if k=='immune_types'else v
   assert list(actual)==expected if k=='immune_types'or k=='hit_weights'else actual==expected,(row['id'],k)
for name,data in species.items():
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);assert s;entries=list(s.level_up_moves);assert len(entries)==len(data['crystal_moves'])
 for e,(level,token)in zip(entries,data['crystal_moves']):
  assert e.level==level
  if token in{r['token']for r in P['rows']}:
   row=next(r for r in P['rows']if r['token']==token);assert e.move==unreal.load_asset(row['path'])and not str(e.unavailable_move_name)and not str(e.unavailable_reason);report.append(dict(species=name,level=level,move=row['id']))
assert len(report)==16
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(R/'Saved/ProjectRefinement/LearnMovesV1/ValidatedData.json').write_text(json.dumps(dict(passed=True,bindings=report,distinct_moves=15),ensure_ascii=False,indent=2))
