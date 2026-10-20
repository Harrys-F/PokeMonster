"""Read-only validation of the authored Gen-2 subset and preserved creature presentation."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();rows=[]
for name,power,pp,kind,typ,effect,chance in [('Scratch',40,35,unreal.PokeMonsterMoveCategory.PHYSICAL,unreal.PokeMonsterCreatureType.NORMAL,'None',100),('Growl',0,40,unreal.PokeMonsterMoveCategory.STATUS,unreal.PokeMonsterCreatureType.NORMAL,'AttackDown',100),('Ember',40,25,unreal.PokeMonsterMoveCategory.SPECIAL,unreal.PokeMonsterCreatureType.FIRE,'Burn',10)]:
 m=unreal.load_asset('/Game/Data/Moves/DA_'+name);assert m
 assert str(m.get_editor_property('internal_id'))==name and m.base_power==power and m.max_pp==pp and m.accuracy==100 and m.category==kind and m.type==typ and str(m.effect.effect_id)==effect and m.effect.chance_percent==chance
 rows.append({'asset':m.get_path_name(),'power':power,'pp':pp,'accuracy':100,'effect':effect,'chance_percent':chance})
s=unreal.load_asset('/Game/Data/Creatures/DA_Zunderlauf');assert str(s.get_internal_id())=='Zunderlauf' and str(s.get_display_name())=='Glumanda' and s.get_base_experience_yield()==65
assert [(e.level,e.move.get_name())for e in s.get_editor_property('level_up_moves')]==[(1,'DA_Scratch'),(1,'DA_Growl'),(7,'DA_Ember')]
i=unreal.load_asset('/Game/Data/Items/DA_TestHealingItem');assert str(i.get_internal_id())=='TestHealingItem' and i.get_heal_amount()==20 and i.can_use_in_battle() and i.can_use_in_overworld()
p=unreal.load_asset('/Game/Data/Encounters/DA_Zunderlauf_Wild');assert all(not e.moves for e in p.entries)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(R/'Saved/BattleSystemV3/DataValidation.json').write_text(json.dumps({'passed':True,'moves':rows,'item_amount':20,'species_id':str(s.get_internal_id())},indent=2))
