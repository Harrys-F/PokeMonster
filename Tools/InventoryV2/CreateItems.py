"""Create only Inventory V2 item/device assets. Legacy assets and species remain untouched."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/InventoryV2';T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.EditorAssetLibrary
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
def asset(name,folder,cls):
 path=folder+'/'+name
 if L.does_asset_exist(path):return unreal.load_asset(path)
 f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',cls);return T.create_asset(name,folder,cls,f)
def props(a,**kw):
 for k,v in kw.items():a.set_editor_property(k,v)
def item(id,name,category,description,**kw):
 a=asset('DA_'+id,'/Game/Data/Items',unreal.PokeMonsterItemData)
 props(a,internal_id=id,display_name=name,description=description,category=category,max_stack_size=99,**kw)
 assert a.is_configured(),id
 assert L.save_loaded_asset(a,False);return a
C=unreal.PokeMonsterItemCategory;E=unreal.PokeMonsterMedicineEffect;rows=[]
for id,name,bonus,guarantee in [('PokeBall','Pokéball',1.,False),('GreatBall','Superball',1.5,False),('UltraBall','Hyperball',2.,False),('MasterBall','Meisterball',1.,True)]:
 d=asset('DA_'+id+'Device','/Game/Data/Capture',unreal.PokeMonsterCaptureDeviceData);props(d,internal_id=id,display_name=name,capture_bonus=bonus,bGuaranteedCapture=guarantee);assert d.is_configured();assert L.save_loaded_asset(d,False)
 a=item(id,name,C.CAPTURE,('Garantierter Fang eines regulär fangbaren wilden Pokémon.' if guarantee else f'Fanggerät für wilde Pokémon. Fangbonus: {bonus:g}×.')+' Ein geworfener Ball wird verbraucht.',bUsableInBattle=True,capture_device=d);rows.append(a)
for id,name,hp in [('SuperPotion','Supertrank',50),('HyperPotion','Hypertrank',200),('MaxPotion','Top-Trank',0)]:
 rows.append(item(id,name,C.HEALING,('Stellt alle KP' if hp==0 else f'Stellt {hp} KP')+' eines nicht kampfunfähigen Pokémon wieder her.',medicine_effect=E.RESTORE_HP,heal_amount=hp,bFullRestore=hp==0,bUsableInOverworld=True,bUsableInBattle=True))
for id,name,status,label in [('Antidote','Gegengift',4,'Vergiftung'),('BurnHeal','Feuerheiler',1,'Verbrennung'),('IceHeal','Eisheiler',5,'Einfrieren'),('Awakening','Aufwecker',3,'Schlaf'),('ParalyzeHeal','Para-Heiler',2,'Paralyse'),('FullHeal','Hyperheiler',0,'alle primären Statusprobleme sowie Verwirrung im Kampf')]:
 rows.append(item(id,name,C.HEALING,f'Heilt {label}. Keine Wirkung bei einem ungeeigneten oder kampfunfähigen Ziel.',medicine_effect=E.CURE_STATUS,cured_status=status,bAllStatuses=status==0,bUsableInOverworld=True,bUsableInBattle=True))
for id,name,full in [('Revive','Beleber',False),('MaxRevive','Top-Beleber',True)]:
 rows.append(item(id,name,C.HEALING,'Hilft einem kampfunfähigen Pokémon auf und stellt '+('alle KP' if full else 'die Hälfte seiner maximalen KP (mindestens 1)')+' wieder her.',medicine_effect=E.REVIVE,bFullRestore=full,bUsableInOverworld=True,bUsableInBattle=True))
for id,name,allmoves,full in [('Ether','Äther',False,False),('MaxEther','Top-Äther',False,True),('Elixir','Elixier',True,False),('MaxElixir','Top-Elixier',True,True)]:
 rows.append(item(id,name,C.HEALING,('Stellt alle AP' if full else 'Stellt bis zu 10 AP')+(' aller aktiven Attacken' if allmoves else ' einer ausgewählten aktiven Attacke')+' wieder her. Das persönliche Repertoire bleibt synchron.',medicine_effect=E.RESTORE_PP,restore_pp_amount=0 if full else 10,bAllMoves=allmoves,bFullRestore=full,bUsableInOverworld=True,bUsableInBattle=True))
for id,name in [('FireStone','Feuerstein'),('WaterStone','Wasserstein'),('ThunderStone','Donnerstein'),('LeafStone','Blattstein'),('MoonStone','Mondstein'),('SunStone','Sonnenstein')]:
 rows.append(item(id,name,C.EVOLUTION,'Kann eine passende, vollständig verfügbare Entwicklung auslösen. Verbrauch nur nach erfolgreicher Entwicklung und Speicherung.',bUsableInOverworld=True))
# Explicit technical fixture only: no lore, quest assignment, world placement or starting stock.
key=item('DevelopmentInventoryKey','Entwickler-Prüfmarke',C.KEY_ITEM,'Rein technischer Inventar-Prüfgegenstand. Kein endgültiger Spiel- oder Questinhalt.',bConsumeOnUse=False,bProtectedItem=True)
legacy=unreal.load_asset('/Game/Data/Items/DA_TestHealingItem')
(D/'ItemAssets.json').write_text(json.dumps({'new':[{'id':str(a.get_internal_id()),'path':a.get_path_name(),'name':str(a.get_display_name()),'category':str(a.get_category()),'configured':a.is_configured()}for a in rows],'development_only_key':key.get_path_name(),'legacy_heal_amount':legacy.get_heal_amount()},indent=2,ensure_ascii=False))
print('INVENTORY_V2_ITEMS',len(rows),'legacy heal unchanged',legacy.get_heal_amount())
