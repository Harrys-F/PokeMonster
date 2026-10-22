"""Real PIE input routing using explicit Slate simulations, never a hardware claim.
Positioning for the isolated wild/NPC cases is a diagnostic placement, not a footrun.
"""
import unreal,json,time,math,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement';label=json.loads((O/'SwitchProRequest.json').read_text())['label'];E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);ui=pc.get_overworld_widget();gi=unreal.GameplayStatics.get_game_instance(w)
enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi)
save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==gi)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';result={'simulated_inputs_not_hardware':True,'checks':[],'diagnostic_positioning':[]};route=[];last=time.monotonic();index=0
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right';X='Gamepad_FaceButton_Left'if backend else'Gamepad_FaceButton_Top';result['backend']=backend
initial_party=[c.instance_id.to_string()for c in enc.get_player_party()];start=p.get_actor_location();original_party=enc.get_player_party();wild=None

def widget_text(name):
 node=next(x for x in unreal.ObjectIterator(unreal.TextBlock)if x.get_name()==name and x.get_path_name().startswith(ui.get_path_name()))
 return str(node.get_editor_property('text'))

def command(s):unreal.SystemLibrary.execute_console_command(w,s)
def action(name,fn,delay=.22):route.append((name,fn,delay))
def check(name,fn):
 def run():
  assert fn(),name
  result['checks'].append(name)
 action(name,run)
def key(name,k,repeat=False):
 action(name+' down',lambda:command('pm.Input.Key '+k+' down'+(' repeat'if repeat else'')),.16)
 action(name+' up',lambda:command('pm.Input.Key '+k+' up'),.22)
def axis(k,v):command('pm.Input.Axis '+k+' '+str(v))
def stopped():axis('Gamepad_LeftX',0);axis('Gamepad_LeftY',0)
def finish_existing_encounter():
 for attempt in range(12):
  if not enc.is_encounter_active():return
  pr=enc.get_presenter()
  if pr.get_view().finished:return
  if pr.get_view().busy:
   if not pr.get_view().presentation_pending:pr.resolve_selection()
   pr.finish_presentation()
  if pr.get_view().finished:return
  if not enc.is_encounter_active():return
  assert pr.try_select_flee(),'Existing flee unavailable during diagnostic teardown'
  assert pr.resolve_selection()
  pr.finish_presentation()
 assert not enc.is_encounter_active(),'Diagnostic flee did not finish encounter'

def close_ui():
 if pc.is_menu_open():pc.close_menu()

# Reuse the existing injured-party/item fixture, then end its temporary battle through normal flee APIs.
command('pm.BattleV3.Start classic wild');assert enc.is_encounter_active();finish_existing_encounter()
inventory=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterInventorySubsystem)if x.get_outer()==gi)
healing=unreal.load_asset('/Game/Data/Items/DA_TestHealingItem');healing_index=1 # Fresh stock is Capture, followed by the fixture healing item.
initial_party=[c.instance_id.to_string()for c in enc.get_player_party()]
result['initial_party_ids']=initial_party
result['unsaved_item_fixture']={'source':'existing pm.BattleV3.Start classic wild, then existing guaranteed flee','existing_item':healing.get_path_name(),'quantity':inventory.get_quantity(healing)}

action('wait for existing encounter completion timer after fixture',lambda:None,1.8)
check('Fixture returned to world before input test',lambda:not enc.is_encounter_active())
action('stick forward',lambda:axis('Gamepad_LeftY',1),.55)
check('Analogstick moves via existing Enhanced Input',lambda:p.get_actor_location().distance(start)>20 and abs(p.character_movement.max_walk_speed-210)<.1)
key('L3 on','Gamepad_LeftThumbstick');check('L3 activates existing sprint speed',lambda:p.is_sprinting()and p.is_sprint_mode_enabled()and abs(p.character_movement.max_walk_speed-315)<.1)
action('stick released',stopped,.3);check('Stopping retains selected sprint mode',lambda:p.is_sprint_mode_enabled()and not p.is_sprinting())
key('X quick menu',X);check('X opens existing team menu',lambda:pc.is_menu_open()and ui.get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM)
key('repeat X',X,True);check('Held X cannot reopen or close menu',lambda:pc.is_menu_open())
check('Menu pauses sprint but preserves mode',lambda:p.is_overworld_input_locked()and not p.is_sprinting()and p.is_sprint_mode_enabled())
key('R category','Gamepad_RightShoulder');check('R reaches inventory',lambda:ui.get_section()==unreal.PokeMonsterOverworldMenuSection.INVENTORY)
key('L category','Gamepad_LeftShoulder');check('L returns to team',lambda:ui.get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM)
key('select second slot','Gamepad_DPad_Down');key('B selects team source',B);key('repeat B cannot confirm twice',B,True)
check('Repeat B preserves source selection',lambda:widget_text('SectionTitle').startswith('Zielplatz wählen'))
key('A cancels selection',A);check('A cancels sorting without closing menu',lambda:pc.is_menu_open()and not widget_text('SectionTitle').startswith('Zielplatz wählen'))
key('select second slot again',B);key('Dpad selects first target','Gamepad_DPad_Up');key('B swaps with first slot',B)
check('Team sorting preserves all IDs and updates slot one',lambda:len(initial_party)>1 and[c.instance_id.to_string()for c in enc.get_player_party()][0]==initial_party[1]and set(c.instance_id.to_string()for c in enc.get_player_party())==set(initial_party))
key('A closes quick menu',A);check('UI focus returns and player unlocked',lambda:not pc.is_menu_open()and not p.is_overworld_input_locked())
action('stick after menu',lambda:axis('Gamepad_LeftY',1),.35);check('Sprint mode resumes after menu',lambda:p.is_sprinting());action('stop',stopped)
key('L3 off at rest','Gamepad_LeftThumbstick');check('L3 toggles mode off',lambda:not p.is_sprint_mode_enabled())
heal_before={}
def heal_snapshot():
 team=enc.get_player_party();assert len(team)>1 and team[1].current_hp<team[1].calculated_stats.max_hp
 heal_before.update(hp=team[1].current_hp,quantity=inventory.get_quantity(healing))
action('record real healing target and item quantity',heal_snapshot)
key('X for healing item',X);key('R for healing item','Gamepad_RightShoulder')
for i in range(healing_index):key('select healing item '+str(i),'Gamepad_DPad_Down')
key('B selects overworld healing item',B);check('Overworld item opens existing team target selector',lambda:ui.get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM and'Ziel wählen'in widget_text('SectionTitle'))
key('A cancels overworld item target',A);check('Cancelling item target consumes nothing',lambda:inventory.get_quantity(healing)==heal_before['quantity']and ui.get_section()==unreal.PokeMonsterOverworldMenuSection.INVENTORY)
key('B selects same item again',B);key('Dpad selects injured second member','Gamepad_DPad_Down');key('B heals selected member',B)
check('Overworld B uses one item on valid target',lambda:inventory.get_quantity(healing)==heal_before['quantity']-1 and enc.get_player_party()[1].current_hp>heal_before['hp'])
key('A closes healed bag',A)
key('Plus main menu','Gamepad_Special_Right');check('Plus opens Main in existing widget',lambda:pc.is_menu_open()and ui.get_section()==unreal.PokeMonsterOverworldMenuSection.MAIN)
key('Plus resume','Gamepad_Special_Right');check('Plus closes main menu',lambda:not pc.is_menu_open())
key('keyboard Tab','Tab');key('keyboard I','I');check('Keyboard inventory shortcut retained',lambda:ui.get_section()==unreal.PokeMonsterOverworldMenuSection.INVENTORY);key('keyboard T','T');check('Keyboard team shortcut retained',lambda:ui.get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM);key('keyboard Escape','Escape')
key('Plus save menu','Gamepad_Special_Right');key('Save down one','Gamepad_DPad_Down');key('Save down two','Gamepad_DPad_Down');key('B saves through existing subsystem',B)
check('Main-menu save writes existing compatible slot',lambda:save.has_save_game()and'Spiel gespeichert'in widget_text('SectionTitle'))
key('A leave saved menu',A)
action('existing LoadGame',lambda:result.update(load_success=save.load_game()),.4);check('Save/Load retains sorted team',lambda:result.get('load_success')and[c.instance_id.to_string()for c in enc.get_player_party()][0]==initial_party[1])

def position_near(a):
 q=a.get_actor_location();p.set_actor_location(unreal.Vector(q.x+115,q.y,p.get_actor_location().z),False,False)
 result['diagnostic_positioning'].append({'actor':a.get_actor_label(),'player':p.get_actor_location().to_tuple()})
 yaw=math.radians(p.get_movement_basis_yaw());axis('Gamepad_LeftX',math.sin(yaw));axis('Gamepad_LeftY',-math.cos(yaw))
dialogue=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem)if x.get_outer()==gi)
npc=None
def prepare_npc():
 global npc
 npc=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPC)if a.get_actor_label()=='Slice_Wanderer_Hinweis')
 position_near(npc)
action('position for original Wanderer',prepare_npc,.16);action('stop near Wanderer',stopped,.35)
check('Existing NPC is the selected interaction target',lambda:p.find_interactable_in_range()==npc)
key('B starts original NPC dialogue',B);check('B opens dialogue without advancing twice',lambda:dialogue.is_dialogue_active()and dialogue.get_page_index()==0)
key('held B in dialogue',B,True);check('Held B does not skip dialogue pages',lambda:dialogue.get_page_index()==0)
key('B advances dialogue once',B);check('B confirms exactly one dialogue page',lambda:dialogue.get_page_index()==1)
key('A closes dialogue',A);check('A closes dialogue and restores world input',lambda:not dialogue.is_dialogue_active()and not p.is_overworld_input_locked())

def prepare_wild():
 global wild
 candidates=[a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor)if'Myrapla'in a.get_actor_label()and a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE]
 assert candidates,'No active original Myrapla available for isolated interaction test'
 wild=candidates[0];wild.overworld_movement.set_component_tick_enabled(False);position_near(wild)
action('position for existing calm Myrapla',prepare_wild,.16);action('stop near Myrapla',stopped,.35)
check('Wild challenge target is selected, not companion',lambda:p.find_interactable_in_range()==wild)
key('B challenges selected wild Pokemon',B);check('B starts one ClassicBattle',lambda:enc.is_encounter_active()and enc.get_battle_widget().is_classic_presentation())
key('X during battle',X);check('Battle blocks world quick menu',lambda:enc.is_encounter_active()and not pc.is_menu_open())
key('Plus during battle','Gamepad_Special_Right');check('Battle blocks world main menu',lambda:not pc.is_menu_open())
key('B opens battle moves',B);check('B selects battle command',lambda:enc.get_battle_widget().get_battle_menu()==unreal.PokeMonsterBattleMenu.MOVES)
key('A backs from moves',A);check('A returns to battle commands',lambda:enc.get_battle_widget().get_battle_menu()==unreal.PokeMonsterBattleMenu.COMMANDS)
# Flee through the existing deterministic fixture, then exercise a healing-item target and move selection.
action('finish wild diagnostic through existing session',finish_existing_encounter,.5)
action('existing Battle V3 injured fixture',lambda:command('pm.BattleV3.Start classic wild'),1.6)
action('wait for fixture initial menu focus',lambda:None,.7)
key('battle Bag down','Gamepad_DPad_Down');key('B opens bag',B);check('Bag selected through Dpad and B',lambda:enc.get_battle_widget().get_battle_menu()==unreal.PokeMonsterBattleMenu.BAG)
key('healing item right','Gamepad_DPad_Right');key('B selects healing item',B);check('Healing target team selection',lambda:enc.get_battle_widget().get_battle_menu()==unreal.PokeMonsterBattleMenu.TEAM)
key('B uses item on first team member',B);check('Healing action submitted once',lambda:enc.get_presenter().get_view().busy)
action('wait existing presentation',lambda:None,8)
key('B opens moves after item round',B);key('B chooses actual attack',B)
check('B submits an actual attack once',lambda:enc.get_presenter().get_view().busy)
action('wait actual attack presentation',lambda:None,8)
key('Dpad selects battle Team','Gamepad_DPad_Right');key('B opens battle Team',B)
check('Battle team page reached',lambda:enc.get_battle_widget().get_battle_menu()==unreal.PokeMonsterBattleMenu.TEAM)
key('B chooses enabled reserve',B);check('B submits actual battle switch',lambda:enc.get_presenter().get_view().busy)
action('wait switch presentation',lambda:None,8)
action('finish diagnostic encounter',finish_existing_encounter,.5)
action('wait for existing completion timer',lambda:None,1.6)
check('Battle ends and restores the world context',lambda:not enc.is_encounter_active()and not p.is_overworld_input_locked())

# Separate explicit three-species fixture proves that sorting updates the actual sole companion.
companion=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w)
def one_companion():
 return len([a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor)if'CreaturePartyCompanion'in[str(t)for t in a.tags]and not a.get_editor_property('hidden')])==1
def companion_mesh_matches(species_path):
 v=companion.get_visual();expected=unreal.load_asset(species_path).get_visuals().presentation.mesh
 return bool(v)and v.mesh.get_skeletal_mesh_asset()==expected and one_companion()
action('existing three-starter party fixture',lambda:command('pm.StarterReview.Party Zunderlauf Schiggy Bisasam'))
action('wait companion refresh',lambda:None,.7)
check('Exactly one visible companion uses party slot one Glumanda',lambda:companion_mesh_matches('/Game/Data/Creatures/DA_Zunderlauf'))
key('X for real companion swap',X);key('select Schiggy slot','Gamepad_DPad_Down');key('B selects Schiggy source',B);key('select leading target','Gamepad_DPad_Up');key('B makes Schiggy first',B)
action('wait new leading companion',lambda:None,.7)
check('Team reorder updates sole companion to Schiggy',lambda:companion_mesh_matches('/Game/Data/Creatures/DA_Schiggy'))
key('A returns from companion menu',A)
action('existing battle for companion pause',lambda:command('pm.BattleV3.Start classic wild'),.3)
companion_position={}
action('record paused companion position',lambda:companion_position.update(value=companion.get_visual().get_actor_location()))
action('observe battle pause',lambda:None,.7)
check('ClassicBattle hides and pauses existing companion',lambda:companion.get_visual().get_editor_property('hidden')and companion.get_visual().get_actor_location().distance(companion_position['value'])<.1)
action('finish companion battle fixture',finish_existing_encounter)
action('wait companion return',lambda:None,1.6)
check('Correct sole companion returns after battle',lambda:not enc.is_encounter_active()and companion_mesh_matches('/Game/Data/Creatures/DA_Zunderlauf'))

def finish(error=None):
 stopped();unreal.unregister_slate_post_tick_callback(unreal._switch_pro_probe)
 result['final_party_ids']=[c.instance_id.to_string()for c in enc.get_player_party()]
 result.update(passed=error is None,error=error,save_after_sha256=__import__('hashlib').sha256(slot.read_bytes()).hexdigest()if slot.exists()else None)
 (O/(label+'.json')).write_text(json.dumps(result,indent=2));unreal.log('SWITCH_PRO_PIE_RESULT '+str(result['passed']))
def tick(dt):
 global last,index
 try:
  if time.monotonic()-last<route[index][2]:return
  name,fn,_=route[index];fn();index+=1;last=time.monotonic()
  (O/(label+'_Progress.json')).write_text(json.dumps({'step':name,'checks':result['checks']},indent=2))
  if index>=len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._switch_pro_probe=unreal.register_slate_post_tick_callback(tick)
