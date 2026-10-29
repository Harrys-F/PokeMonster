"""Real UMG/input/pickup/save acceptance. Refuses storage outside this task's isolated UserDir."""
import unreal,json,time,math,traceback,os,stat,hashlib,shutil,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/InventoryV2';q=json.loads((D/'Active.json').read_text());O=D/q['label'];route=[];s={'start':time.monotonic(),'i':0,'at':time.monotonic(),'ready':False};r={'cases':[],'checks':[],'pickups':[],'performance':[],'software_input_only':True};state={};W=PC=E=S=I=C=P=None
locs=json.loads((D/'PickupLocations.json').read_text());ids=[x['id'] for x in json.loads((D/'ItemAssets.json').read_text())['new']]
if 'Potion'not in ids:ids.insert(4,'TestHealingItem')
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def key(x):cmd('pm.Input.Key '+x+' tap')
def item(id):return unreal.load_asset('/Game/Data/Items/DA_'+('TestHealingItem'if id=='Potion'else id))
def team():return E.get_player_party()
def add(name,f,delay=.35):route.append((name,f,delay))
def check(name,p,delay=.35):
 def go():assert p(),name;r['checks'].append(name)
 add(name,go,delay)
def widget():return PC.get_overworld_widget()
def snap():return {'party':[c.export_text()for c in team()],'inventory':[x.export_text()for x in I.get_stacks()],'flags':{x['id']:E.is_encounter_completed(x['id'])for x in locs}}
def shot(name):cmd('Shot filename="'+str(O/(name+'.png'))+'" -nosuffix -showui')
def place(pos):P.set_actor_location(unreal.Vector(*pos),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def feed(x=0,y=0):
 yaw=math.radians(P.get_movement_basis_yaw());Input.inject_input_vector_for_action(Move,unreal.Vector(-math.sin(yaw)*x+math.cos(yaw)*y,math.cos(yaw)*x+math.sin(yaw)*y,0),[],[])
def edit_team(index,hp=None,status=None,pp=None):
 cmd('pm.InventoryReview.Target '+str(index+1)+' '+str(hp if hp is not None else -1)+' '+('poison'if status==unreal.PokeMonsterCreatureStatus.POISON else 'keep')+' '+str(pp if pp is not None else -1))
def selected_inventory(id):
 rows=widget().get_view().inventory;idx=next(n for n,x in enumerate(rows)if x.item==item(id));state['selection']=id
 for unused in range(idx):key('Down')
 key('Enter')
def block_write():
 folder=Path(unreal.Paths.project_saved_dir())/'SaveGames';assert folder.resolve().is_relative_to(D);state['blocked']=(folder,stat.S_IMODE(folder.stat().st_mode));os.chmod(folder,0o555)
def unblock_write():
 folder,mode=state.pop('blocked');os.chmod(folder,mode)
def pickup(id):return next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterWorldItem)if str(a.pickup_id)==id)
def perf(name,start=True):
 if start:cmd('csvprofile startfile=IV2_'+name);cmd('csvprofile start');state['perf']={'name':name,'frames':[],'start':time.monotonic()}
 else:
  cmd('csvprofile stop');state.setdefault('pending_csv',[]).append(name);x=state.pop('perf');x['seconds']=time.monotonic()-x['start'];r['performance'].append(x)
def build():
 add('Load isolated pre-schema11 fixture',lambda:state.update(load_requested=S.load_game()),.1)
 check('Older save loads and regular team present',lambda:not S.is_load_in_progress()and len(team())==3,1.8)
 if q.get('restart_read'):
  expected=json.loads((D/'RestartExpected.json').read_text());check('Fresh process restores party inventory and all twelve flags',lambda:snap()==expected['snapshot'],2)
  check('Fresh process retains rendering C',lambda:unreal.SystemLibrary.get_console_variable_int_value('r.Lumen.HardwareRayTracing')==0 and unreal.SystemLibrary.get_console_variable_int_value('r.Lumen.FinalGatherMethod')==0 and unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')==75)
  return
 def stock():
  assert I.restore_stacks([])
  for id in ids:assert I.add_item(item(id),3)
  r['fixture']='Three real team members from isolated legacy fixture; 26 item assets at three each; no user slot. Damage/status/AP injected only into transient test copies.'
 add('Stock all real item assets in isolated test inventory',stock)
 def quest_fixture(completed=False):
  Q=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterQuestSubsystem)if x.get_outer()==unreal.GameplayStatics.get_game_instance(W))
  state['quest']=Q;state['questid']=str(unreal.load_asset('/Game/Data/Quests/DA_SliceArchiveQuest').internal_id)
  cmd('pm.InventoryReview.Quest '+('complete'if completed else 'active'))
 add('Existing quest fixture active, not completed',quest_fixture)
 check('Incomplete quest cannot grant reward',lambda:not state['quest'].grant_item_reward(state['questid'],'InventoryV2TechnicalReward',item('DevelopmentInventoryKey'),1))
 add('Complete only existing technical quest fixture',lambda:quest_fixture(True))
 def quest_key():
  Q=state['quest'];key_item=item('DevelopmentInventoryKey');qid=state['questid']
  assert key_item and key_item.is_configured()and not key_item.can_discard()
  assert Q.grant_item_reward(qid,'InventoryV2TechnicalReward',key_item,1),S.get_last_storage_message()
  assert I.get_quantity(key_item)==1 and not I.discard_item(key_item,1)
  assert not Q.grant_item_reward(qid,'InventoryV2TechnicalReward',key_item,1)and I.get_quantity(key_item)==1
  r['checks'].append('Existing quest reward requires completion, persists once and protects a technical key item; no new quest/story authored')
 add('Key item reward and discard protection',quest_key)
 add('Prepare real medicine target',lambda:edit_team(0,hp=1,status=unreal.PokeMonsterCreatureStatus.POISON,pp=0))
 add('Open existing bag',lambda:PC.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY),.6)
 add('QHD opened bag',lambda:shot('01_Bag'),1)
 add('Sort by category',lambda:key('S'))
 add('Sort by German name',lambda:key('S'))
 add('Restore existing order',lambda:key('S'))
 add('Filter balls',lambda:key('Right'))
 add('Return all categories',lambda:key('Left'))
 add('Choose potion through existing input',lambda:selected_inventory('Potion'),.7)
 check('Existing team target selection opens',lambda:widget().get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM)
 add('QHD item target selection',lambda:shot('02_Target'),.8)
 add('Confirm potion target',lambda:key('Enter'))
 check('Potion heals exactly20 and consumes one',lambda:team()[0].current_hp==21 and I.get_quantity(item('Potion'))==2,.7)
 add('Close menu for direct transaction tests',lambda:PC.close_menu())
 def cures():
  before=I.get_quantity(item('Antidote'));assert E.use_healing_item_on_party_member(item('Antidote'),0);assert team()[0].status==unreal.PokeMonsterCreatureStatus.NONE
  assert not E.use_healing_item_on_party_member(item('Antidote'),0);assert I.get_quantity(item('Antidote'))==before-1
  r['checks'].append('Correct status cured; invalid repeated use consumes nothing')
 add('Use status cure via shared production service',cures)
 add('Prepare unconscious bench member',lambda:edit_team(1,hp=0))
 check('Revive restores half HP without AP regeneration',lambda:E.use_healing_item_on_party_member(item('Revive'),1)and team()[1].current_hp==team()[1].calculated_stats.max_hp//2)
 add('Open bag for PP targeting',lambda:PC.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY))
 add('Choose Ether',lambda:selected_inventory('Ether'))
 add('Choose first team member for Ether',lambda:key('Enter'))
 add('QHD AP move selection',lambda:shot('03_PP_Target'),.7)
 add('Confirm first move',lambda:key('Enter'))
 check('Ether restores10AP through real menu and repertoire',lambda:team()[0].get_editor_property('move_slots')[0].get_editor_property('current_pp')==10 and I.get_quantity(item('Ether'))==2,.7)
 add('Close bag before failure simulation',lambda:PC.close_menu())
 add('Snapshot before forced save refusal',lambda:state.update(before_failure=snap()))
 add('Make only own isolated save directory read-only',block_write)
 check('Medicine rollback on actual filesystem failure',lambda:not E.use_healing_item_on_party_member(item('Potion'),0)and snap()==state['before_failure'])
 check('Discard rollback on actual filesystem failure',lambda:not I.discard_item(item('PokeBall'),1)and snap()==state['before_failure'])
 check('Pickup rollback includes world flag',lambda:not I.collect_item(item('Potion'),1,'Pickup.InventoryV2.FailureProbe')and not E.is_encounter_completed('Pickup.InventoryV2.FailureProbe')and snap()==state['before_failure'])
 add('Restore own save directory permissions',unblock_write)
 add('Open bag for discard',lambda:PC.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY))
 add('Select two Pokeballs to discard',lambda:(key('Delete'),key('Down')))
 add('Request final discard confirmation',lambda:key('Enter'))
 add('Cancel discard',lambda:key('Escape'))
 check('Cancel keeps quantity',lambda:I.get_quantity(item('PokeBall'))==3)
 add('Discard quantity two with both confirmations',lambda:(key('Delete'),key('Down'),key('Enter'),key('Enter')))
 check('Confirmed discard persists exactly two',lambda:I.get_quantity(item('PokeBall'))==1,.7)
 add('Close bag',lambda:PC.close_menu())
 def invalid_stone():
  before=snap();assert E.prepare_item_evolution_offer(item('ThunderStone'),2)==-1;assert snap()==before;r['checks'].append('Real ThunderStone safely refused for missing Raichu; no item consumed')
 add('Missing stone target safely refused',invalid_stone)
 # Short performance windows exclude screenshots and include the ordinary world/AI.
 for label,pos in [('VillageBefore',(-2500,-1700,50.15)),('ForestBefore',(-4350,1200,50.15))]:
  add('Move to '+label,lambda pos=pos:place(pos),1)
  add('Start '+label,lambda label=label:perf(label),2.5)
  add('Stop '+label,lambda label=label:perf(label,False),10)
 add('Open bag benchmark',lambda:PC.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY))
 add('Start BagOpen benchmark',lambda:perf('BagOpen'),1)
 add('Stop BagOpen benchmark',lambda:perf('BagOpen',False),10)
 add('Close benchmark bag',lambda:PC.close_menu())
 # Each site is approached using real movement and normal E interaction. Teleports only relocate between sites.
 for n,loc in enumerate(locs):
  id=loc['id'];name=id.rsplit('.',1)[-1]
  add('Relocate to safe approach '+name,lambda loc=loc:place(loc['approach']),.5)
  add('Record initial approach '+name,lambda:state.update(walk_start=P.get_actor_location().to_tuple()),1)
  add('Walk toward '+name,lambda:state.update(walk_to=True))
  add('Stop near '+name,lambda:(state.pop('walk_to',None),feed()),.42)
  def before(id=id,loc=loc):
   a=pickup(id);state['picked_before']=I.get_quantity(a.item);state['pickup_item']=a.item
   delta=P.get_actor_location()-unreal.Vector(*state['walk_start']);assert delta.length()>20,(id,'No real movement',delta)
   assert not E.is_encounter_completed(id);r['pickups'].append({'id':id,'location':loc['position'],'approach':state['walk_start'],'reached':P.get_actor_location().to_tuple(),'actual_walk_cm':delta.length()})
  add('Verify walk and item '+name,before,.5)
  if n in [0,7]:add('QHD world item '+name,lambda name=name:shot('04_World_'+name),.8)
  add('Interact using normal E '+name,lambda:key('E'),.4)
  check('Collected once '+name,lambda id=id,loc=loc:E.is_encounter_completed(id)and I.get_quantity(state['pickup_item'])==state['picked_before']+loc['quantity']and pickup(id).get_editor_property('hidden'),.8)
  if n in [0,7]:add('QHD pickup message '+name,lambda name=name:shot('05_Received_'+name),.6)
  check('Repeated collection rejected '+name,lambda id=id:not I.collect_item(pickup(id).item,pickup(id).quantity,id))
 add('Village after pickup performance position',lambda:place((-2500,-1700,50.15)),.5)
 add('Start AfterPickup benchmark',lambda:perf('AfterPickup'),2.5)
 add('Stop AfterPickup benchmark',lambda:perf('AfterPickup',False),10)
 add('Snapshot all individual data and pickup state',lambda:state.update(saved=snap()))
 check('Manual save',lambda:S.save_current_game(),1)
 add('Load saved state',lambda:S.load_game(),1)
 check('Save/load restores exact team and all item quantities and pickup flags',lambda:not S.is_load_in_progress()and snap()==state['saved'],2)
 check('All12 hidden after load',lambda:all(a.get_editor_property('hidden')for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterWorldItem)))
 add('Start AfterLoad benchmark',lambda:perf('AfterLoad'),1)
 add('Stop AfterLoad benchmark',lambda:perf('AfterLoad',False),10)
 def export_restart():
  assert S.save_current_game();paths=list((Path(unreal.Paths.project_saved_dir())/'SaveGames').glob('*.sav'));p=next(x for x in paths if x.name=='PokeMonster_Dev.sav')if not q.get('pie') else next(x for x in paths if x.name=='PokeMonster_SaveV2_Test_InventoryV2PIE01.sav')
  assert p.resolve().is_relative_to(D);shutil.copyfile(p,O/'RestartFixture.sav');(D/'RestartExpected.json').write_text(json.dumps({'snapshot':snap(),'from':str(p)},indent=2))
 add('Export only isolated fixture for fresh-process readback',export_restart)
 check('Default renderer and120-minute day unchanged',lambda:unreal.SystemLibrary.get_console_variable_int_value('r.Lumen.HardwareRayTracing')==0 and unreal.SystemLibrary.get_console_variable_int_value('r.Lumen.FinalGatherMethod')==0 and C.get_real_minutes_per_day()==120)
def finish(error=None):
 try:
  if 'blocked'in state:unblock_write()
  if 'perf'in state:perf('Interrupted',False)
  if P and 'Input'in globals():feed()
 except Exception:r['cleanup_error']=traceback.format_exc()
 r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2));unreal.unregister_slate_post_tick_callback(unreal._iv2_gameplay)
 if q.get('pie'):unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
 elif W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def handle_pickup_encounter(now):
 # A moving wild Pokémon can win the normal interaction focus. Complete that genuine
 # encounter through the existing capture/presentation path, then retry the untouched pickup.
 if E.is_encounter_active():
  presenter=E.get_presenter();view=presenter.get_view()
  if view.busy or view.presentation_pending or view.finished:return True
  assert I.get_quantity(item('MasterBall'))>0,'Normal encounter interrupted pickup but no test ball remains'
  assert presenter.try_select_capture_item(item('MasterBall'));assert presenter.resolve_selection()
  r.setdefault('natural_pickup_encounters',[]).append({'step':s['i'],'ball':'MasterBall','party_before':len(team())})
  return True
 if now-state.get('pickup_retry_at',0)>2:
  state['pickup_retry_at']=now;key('E')
 return True

def tick(dt):
 global W,PC,E,S,I,C,P,Input,Move
 try:
  now=time.monotonic();frame_elapsed=(now-s.get('last_tick',now))*1000;s['last_tick']=now;assert now-s['start']<700,'Bounded inventory acceptance'
  if not s['ready']:
   if now-s['start']<12:return
   worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name().endswith('Dev_TestMap_VisualV2')and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:return
   W=worlds[0];PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==GI)
   E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);I=sub(unreal.PokeMonsterInventorySubsystem);C=sub(unreal.PokeMonsterWorldClock)
   assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D),'User saves forbidden'
   Input=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if 'LocalPlayer'in x.get_outer().get_class().get_name());Move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==P and x.get_name()=='MoveAction')
   cmd('pm.Evolution.Auto 0');cmd('pm.EnvPerf2.Viewport 2560 1440');r['rendering']={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.GPUCsvStatsEnabled','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.ScreenPercentage','r.TemporalAA.Upsampling','r.Shadow.Virtual.SMRT.RayCountDirectional','r.VSync','t.MaxFPS']};cmd('pm.Graphics status');build();s.update(ready=True,at=now)
  else:
   if 'perf'in state:state['perf']['frames'].append(frame_elapsed)
   for csv_name in list(state.get('pending_csv',[])):
    path=Path(unreal.Paths.project_saved_dir())/'Profiling/CSV'/('IV2_'+csv_name+'.csv')
    if path.exists()and path.stat().st_size>1000:shutil.copyfile(path,O/('Perf_'+csv_name+'.csv'));state['pending_csv'].remove(csv_name)
   if state.get('walk_to'):feed(0,1)
   if s['i']>=len(route):finish();return
   name,f,delay=route[s['i']]
   if name.startswith('Collected once ') and (E.is_encounter_active() or not E.is_encounter_completed(locs[len(r['pickups'])-1]['id'])):
    assert now-s['at']<50,'Pickup interrupted or not reachable within bounded retry'
    if now-s['at']>delay:handle_pickup_encounter(now)
    return
   if now-s['at']<delay:return
   f();r['cases'].append({'step':name});s['i']+=1;s['at']=now;(O/'Progress.json').write_text(json.dumps({'step':s['i'],'total':len(route),'name':name}))
 except Exception:finish(traceback.format_exc())
unreal._iv2_gameplay=unreal.register_slate_post_tick_callback(tick)
