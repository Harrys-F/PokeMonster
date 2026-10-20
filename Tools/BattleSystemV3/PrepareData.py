"""Author only the verified Gen-2 starter data and enable the existing healing item."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/BattleSystemV3';O.mkdir(exist_ok=True)
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert all(x.get_path_name()=='/Game/Data/Moves/DA_Scratch' for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
A=unreal.AssetToolsHelpers.get_asset_tools();rows=[];moves=[]
for name,german,typ,category,power,pp,effect,chance in [('Scratch','Kratzer',unreal.PokeMonsterCreatureType.NORMAL,unreal.PokeMonsterMoveCategory.PHYSICAL,40,35,'',100),('Growl','Heuler',unreal.PokeMonsterCreatureType.NORMAL,unreal.PokeMonsterMoveCategory.STATUS,0,40,'AttackDown',100),('Ember','Glut',unreal.PokeMonsterCreatureType.FIRE,unreal.PokeMonsterMoveCategory.SPECIAL,40,25,'Burn',10)]:
 path='/Game/Data/Moves/DA_'+name
 assert not (R/('Content/Data/Moves/DA_'+name+'.uasset')).exists(),'Already saved move must be inspected: '+path
 f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',unreal.PokeMonsterMoveData)
 m=unreal.find_object(None,path+'.DA_'+name) or A.create_asset('DA_'+name,'/Game/Data/Moves',unreal.PokeMonsterMoveData,f);assert m
 for k,v in dict(internal_id=name,display_name=german,type=typ,category=category,base_power=power,accuracy=100,max_pp=pp,priority=0,effect=unreal.PokeMonsterMoveEffect(effect_id=effect,description=('Senkt den Angriff des Ziels um eine Stufe.' if name=='Growl' else '10 % Verbrennungschance.' if name=='Ember' else ''),chance_percent=chance)).items():m.set_editor_property(k,v)
 assert str(m.get_editor_property('internal_id'))==name;assert unreal.EditorAssetLibrary.save_loaded_asset(m);moves.append(m);rows.append({'asset':path,'name':german,'power':power,'accuracy':100,'pp':pp,'effect':effect,'chance':chance})
s=unreal.load_asset('/Game/Data/Creatures/DA_Zunderlauf');assert s and str(s.get_internal_id())=='Zunderlauf'
assert len(s.get_editor_property('level_up_moves'))==0
s.set_editor_property('level_up_moves',[unreal.PokeMonsterLevelMove(level=level,move=m)for level,m in zip([1,1,7],moves)]);s.set_editor_property('base_experience_yield',65);assert unreal.EditorAssetLibrary.save_loaded_asset(s)
p=unreal.load_asset('/Game/Data/Encounters/DA_Zunderlauf_Wild');entries=list(p.get_editor_property('entries'));assert entries
before=[]
for e in entries:
 assert e.get_editor_property('species')==s
 before.append({'min':e.min_level,'max':e.max_level,'moves':[str(x)for x in e.moves]});e.set_editor_property('moves',[])
p.set_editor_property('entries',entries);assert unreal.EditorAssetLibrary.save_loaded_asset(p)
i=unreal.load_asset('/Game/Data/Items/DA_TestHealingItem');assert i and i.get_category()==unreal.PokeMonsterItemCategory.HEALING and i.get_heal_amount()>0
item_before={'id':str(i.get_internal_id()),'name':str(i.get_display_name()),'heal_amount':i.get_heal_amount(),'battle':i.can_use_in_battle()}
i.set_editor_property('bUsableInBattle',True);i.set_editor_property('display_name','Trank');assert unreal.EditorAssetLibrary.save_loaded_asset(i)
legacy={}
for n in ['TestNormalPhysical','TestFireSpecial','TestStatus']:
 m=unreal.load_asset('/Game/Data/Moves/DA_'+n);legacy[n]=str(m.get_editor_property('internal_id'))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(O/'DataAuthoring.json').write_text(json.dumps({'moves':rows,'species':s.get_path_name(),'wild_before':before,'healing_before':item_before,'legacy_ids':legacy},indent=2));unreal.log('BATTLE_V3_DATA_READY')
